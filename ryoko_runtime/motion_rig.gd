extends Node2D
# Live 2D weighted deformation. Existing facial artwork is rendered into a
# transparent viewport and deformed together, preserving registration.
var face
var effects_viewport: SubViewport
var effects_surface: MeshInstance2D
var effects_material: ShaderMaterial
var effects_uniforms: Array[StringName] = []
var surface: MeshInstance2D
var skin_material: ShaderMaterial
var target = Vector3.ZERO # tilt, horizontal offset, vertical offset
var current = Vector3.ZERO
var body_target = Vector3.ZERO
var body_current = Vector3.ZERO
var body_follow = true
var body_proof = false
var secondary_proof = false
var chest_offset = Vector2.ZERO
var chest_velocity = Vector2.ZERO
var chest_anchor = Vector2.ZERO
var chest_initialized = false
var chest_enabled = true
var bounce_position = 0.0
var bounce_velocity = 0.0
const CHEST_LIMIT = 8.0 # source pixels, below four review pixels
const CHEST_FREQUENCY = 12.0
const CHEST_DAMPING = 0.42
var clock_time = 0.0
var auto_blink = true
var next_blink = 2.8
var blink_until = -1.0
var manual_blink = -1.0
var speech = false
var mouse_follow = false
var external_controls = false
var proof = false
var proof_stage = -1
var hud: Label
var hint: Label
var proof_log
var rig_ready = false
var expression_ids=[]
var expression_index=-1
var audio_mouth
var audio_proof=false
var audio_proof_started=false
var gestures=preload("res://gesture_driver.gd").new()
var gesture_proof=false
var gesture_events={}
var eyelids=preload("res://eyelid_driver.gd").new()
var eyelid_proof=false
var eyelid_events={}
var pose_store=preload("res://pose_store.gd").new()
var pose_proof=false
var pose_events={}
var pose_notice=""
var pose_status:Label
var clip=preload("res://clip_player.gd").new()
var clip_proof=false
var clip_proof_time=0.0
var clip_events={}
var clip_channels={}
var hair=preload("res://hair_secondary.gd").new()
var hair_proof=false
var live_input=preload("res://live_input.gd").new()
var live_proof=false
var gaze=preload("res://gaze_driver.gd").new()
var gaze_proof=false
var gaze_profiles={}
var gaze_profile_name="neutral"
var breathing=preload("res://breath_driver.gd").new()
var breath_proof=false
var breath_events={}
var brows=preload("res://brow_driver.gd").new()
var brow_proof=false

var attention=preload("res://look_at_driver.gd").new()
var look_proof=false
var look_stage=-1

var ornament=preload("res://ornament_driver.gd").new()
var ornament_pivot:Node2D
var ornament_sprite:Sprite2D
var ornament_proof=false
var ornament_stage=-1
var loose_hair_enabled=true
var loose_hair={"screen_left":preload("res://loose_hair_driver.gd").new(),"screen_right":preload("res://loose_hair_driver.gd").new()}
var earrings_enabled=true
var earrings={}
var earring_metadata={}
var earring_pivots={}
var earring_sprites={}

func _ready():
    var viewport = SubViewport.new()
    viewport.name = "RegisteredFaceViewport"
    viewport.size = Vector2i(1136,1384)
    viewport.transparent_bg = true
    viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS
    add_child(viewport)
    face = load("res://preview.tscn").instantiate()
    viewport.add_child(face)
    expression_ids=face.emotion_eyes.keys()
    expression_ids.sort()
    surface = MeshInstance2D.new()
    surface.name = "WeightedHeadNeckTorsoMesh"
    surface.texture = viewport.get_texture()
    surface.position=Vector2(6,70)
    surface.scale=Vector2(0.49,0.49)
    surface.mesh=_build_grid(32,40)
    skin_material=ShaderMaterial.new()
    skin_material.shader=load("res://motion_deform.gdshader")
    for side in ["screen_left","screen_right"]:
        for layer in ["iris","sclera","aperture","brow","brow_skin","brow_allow"]:
            skin_material.set_shader_parameter(layer+"_"+side,load("res://rig_assets/"+layer+"_"+side+".png"))
    _setup_gaze_profiles()
    surface.material=skin_material
    add_child(surface)
    # The ornament samples the existing viewport directly. No new/edited art.
    ornament_pivot=Node2D.new()
    ornament_pivot.name="RigidHairpinOrnamentPivot"
    # Do not draw an unpositioned cutout at the viewport origin on startup.
    ornament_pivot.visible=false
    surface.add_child(ornament_pivot)
    ornament_sprite=Sprite2D.new()
    ornament_sprite.texture=viewport.get_texture()
    ornament_sprite.centered=false
    ornament_sprite.region_enabled=true
    ornament_sprite.region_rect=ornament.SOURCE_RECT
    ornament_sprite.region_filter_clip_enabled=true
    ornament_sprite.position=ornament.SOURCE_RECT.position-ornament.PIVOT
    ornament_pivot.add_child(ornament_sprite)
    _setup_earrings()
    _setup_optional_effects()
    hud=Label.new();hud.position=Vector2(18,10);hud.add_theme_font_size_override("font_size",20);add_child(hud)
    hint=Label.new();hint.position=Vector2(18,42);hint.add_theme_font_size_override("font_size",14);add_child(hint)
    proof="--motion-proof" in OS.get_cmdline_user_args()
    if proof: proof_log=FileAccess.open("user://motion_proof.jsonl",FileAccess.WRITE)
    audio_mouth=load("res://audio_mouth_driver.gd").new()
    add_child(audio_mouth)
    audio_proof="--audio-proof" in OS.get_cmdline_user_args()
    audio_mouth.deterministic=audio_proof
    if audio_proof:audio_mouth.load_wav("res://audio_fixture.wav")
    var args=OS.get_cmdline_user_args()
    var ai=args.find("--audio-file")
    if ai>=0 and ai+1<args.size():
        if audio_mouth.load_wav(args[ai+1]):audio_mouth.play()
        else:push_error(audio_mouth.error_message)
    secondary_proof="--secondary-proof" in OS.get_cmdline_user_args()
    body_proof="--body-proof" in OS.get_cmdline_user_args()
    gesture_proof="--gesture-proof" in OS.get_cmdline_user_args()
    eyelid_proof="--eyelid-proof" in OS.get_cmdline_user_args()
    pose_proof="--pose-proof" in OS.get_cmdline_user_args()
    if pose_proof:pose_store.path="user://proof_poses.json"
    if not pose_store.load_disk():push_warning(pose_store.error_message)
    pose_status=Label.new();pose_status.position=Vector2(18,62);pose_status.add_theme_font_size_override("font_size",12);add_child(pose_status)
    clip_proof="--clip-proof" in OS.get_cmdline_user_args()
    hair_proof="--hair-proof" in OS.get_cmdline_user_args()
    brow_proof="--brow-proof" in args
    breath_proof="--breath-proof" in args
    gaze_proof="--gaze-proof" in args
    look_proof="--look-proof" in args

    ornament_proof="--ornament-proof" in args
    live_proof="--live-proof" in args
    if "--live-input" in args:
        var error=live_input.start()
        if error!=OK:push_error(live_input.status)
    rig_ready=true
    print("MOTION_RIG_READY profiles=",expression_ids.size()," mesh_vertices=1353 triangles=2560")

func _build_grid(columns,rows):
    var vertices=PackedVector3Array();var uvs=PackedVector2Array();var indices=PackedInt32Array()
    for row in range(rows+1):
        for col in range(columns+1):
            var uv=Vector2(float(col)/columns,float(row)/rows)
            vertices.append(Vector3(uv.x*1136,uv.y*1384,0));uvs.append(uv)
    for row in range(rows):
        for col in range(columns):
            var a=row*(columns+1)+col;var b=a+1;var c=a+columns+1;var d=c+1
            indices.append_array(PackedInt32Array([a,c,b,b,c,d]))
    var arrays=[];arrays.resize(Mesh.ARRAY_MAX);arrays[Mesh.ARRAY_VERTEX]=vertices;arrays[Mesh.ARRAY_TEX_UV]=uvs;arrays[Mesh.ARRAY_INDEX]=indices
    var mesh=ArrayMesh.new();mesh.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES,arrays);return mesh

func apply_controls(data, source="external"):
    # Validate the complete optional-effects patch before any mutations, even reset.
    if not data is Dictionary:return false
    if data.has("effects") and not preload("res://optional_effects.gd").valid(data.effects):return false
    # Loaded clips are already validated. Also reject a stale/mutated expression
    # cue before any of its other controls or ownership flags can be applied.
    if source=="clip" and data.has("expression"):
        if not data.expression is String or (data.expression!="neutral" and not face.emotion_eyes.has(data.expression)):return false
    if source in ["external","clip"]:external_controls=true
    if source=="clip":_track_clip_channels(data)
    if data.get("clip_stop",false):stop_clip()
    if data.has("clip_paused"):pause_clip(bool(data.clip_paused))
    var pose_ok=true
    if data.get("clip_play",false):pose_ok=play_clip("res://demo_clip.json")
    if data.has("pose_load"):pose_ok=recall_pose(int(data.pose_load))
    if data.get("reset",false):
        for earring in earrings.values():earring.reset()
        for lock in loose_hair.values():lock.reset()
        ornament.reset();attention.reset();brows.reset();breathing.reset();gaze.reset();hair.reset();stop_clip();eyelids.reset();gestures.cancel();audio_mouth.stop();body_follow=true;body_target=Vector3.ZERO;target=Vector3.ZERO;face.reset_neutral();expression_index=-1;manual_blink=-1.0;speech=false;mouse_follow=false;auto_blink=true;external_controls=false
    if data.has("effects"):face.optional_effects.apply(data.effects)
    if data.has("brow_raise"):brows.set_both(data.brow_raise)
    if data.has("brow_screen_left"):brows.set_side("screen_left",data.brow_screen_left)
    if data.has("brow_screen_right"):brows.set_side("screen_right",data.brow_screen_right)
    if data.has("breath_level"):breathing.hold(data.breath_level)
    if data.get("breath_trigger",false):breathing.trigger(data.get("breath_strength",1.0))
    if data.get("breath_cancel",false):breathing.cancel()
    if data.get("look_release",false):attention.release()
    if data.has("look_x") or data.has("look_y"):
        mouse_follow=false;gaze.mouse_follow=false
        attention.mouse_follow=false
        attention.aim(data.get("look_x",attention.target.x),data.get("look_y",attention.target.y))
    if data.has("gaze_x") or data.has("gaze_y"):
        gaze.mouse_follow=false
        gaze.set_target(data.get("gaze_x",gaze.target.x),data.get("gaze_y",gaze.target.y))
    if data.has("head_tilt"):target.x=clamp(float(data.head_tilt),-1.0,1.0)
    if data.has("head_x"):target.y=clamp(float(data.head_x),-1.0,1.0)
    if data.has("head_y"):target.z=clamp(float(data.head_y),-1.0,1.0)
    if data.has("body_tilt") or data.has("body_x") or data.has("body_y"):
        body_follow=false
        if data.has("body_tilt"):body_target.x=_finite_axis(data.body_tilt)
        if data.has("body_x"):body_target.y=_finite_axis(data.body_x)
        if data.has("body_y"):body_target.z=_finite_axis(data.body_y)
    if data.get("bounce",false):bounce_velocity=-280.0
    if data.has("ornament_secondary"):ornament.enabled=bool(data.ornament_secondary)
    if data.has("earring_secondary"):earrings_enabled=bool(data.earring_secondary)
    if data.has("loose_hair_secondary"):loose_hair_enabled=bool(data.loose_hair_secondary)
    if data.has("hair_secondary"):hair.enabled=bool(data.hair_secondary)
    if data.has("chest_secondary"):chest_enabled=bool(data.chest_secondary)
    if data.has("body_follow"):body_follow=bool(data.body_follow)
    var accepted=pose_ok
    if data.has("expression"):
        var expression_ok=_set_expression(String(data.expression))
        accepted=accepted and expression_ok
    if data.has("gesture"):
        var gesture_ok=gestures.trigger(String(data.gesture),data.get("gesture_strength",1.0))
        accepted=accepted and gesture_ok
    if data.get("gesture_cancel",false):gestures.cancel()
    if data.get("release_eye_controls",false):eyelids.reset()
    if data.has("eye_screen_left"):eyelids.set_hold("screen_left",float(data.eye_screen_left))
    if data.has("eye_screen_right"):eyelids.set_hold("screen_right",float(data.eye_screen_right))
    if data.has("wink"):
        var eye_ok=eyelids.trigger(String(data.wink),data.get("wink_duration",0.28))
        accepted=accepted and eye_ok
    if data.has("audio_level"):audio_mouth.set_level(float(data.audio_level))
    if data.get("audio_stop",false):audio_mouth.stop();face.release_speech()
    if data.has("mouth"):audio_mouth.stop();face.set_mouth(data.mouth)
    if data.has("speech_active") and not data.speech_active:face.release_speech()
    if data.has("blink"):
        manual_blink=float(data.blink);face.set_blink(manual_blink,manual_blink)
    if data.has("auto_blink"):auto_blink=bool(data.auto_blink);manual_blink=-1.0
    if data.has("pose_save"):
        var saved=save_pose(int(data.pose_save))
        accepted=accepted and saved
    return accepted

func _set_expression(id:String)->bool:
    if not face.set_expression(id):return false
    expression_index=expression_ids.find(face.expression)
    return true

func _unhandled_key_input(event):
    if not event.is_pressed() or event.echo:return
    if event.keycode in [KEY_A,KEY_D,KEY_LEFT,KEY_RIGHT,KEY_UP,KEY_DOWN,KEY_Q,KEY_E,KEY_W,KEY_S,KEY_Z,KEY_C,KEY_M,KEY_O,KEY_I,KEY_Y,KEY_V]:stop_clip()
    if event.keycode in [KEY_M,KEY_A,KEY_D,KEY_LEFT,KEY_RIGHT,KEY_UP,KEY_DOWN,KEY_B,KEY_SPACE,KEY_Q,KEY_E,KEY_W,KEY_S,KEY_Z,KEY_C,KEY_H]:external_controls=false
    if event.keycode in [KEY_Q,KEY_E,KEY_W,KEY_S,KEY_Z,KEY_C]:body_follow=false
    if event.keycode==KEY_O and not event.shift_pressed:brows.set_both(1 if brows.target==Vector2.ZERO else 0)
    if event.keycode==KEY_I:breathing.trigger()
    if event.keycode==KEY_Y:
        if attention.mouse_follow:attention.release()
        else:
            attention.mouse_follow=true;mouse_follow=false;gaze.mouse_follow=false
    if event.keycode==KEY_V:
        attention.release();gaze.mouse_follow=not gaze.mouse_follow
    if event.keycode==KEY_O and event.shift_pressed:
        ornament.enabled=not ornament.enabled
        pose_notice="Hairpin ornament motion on" if ornament.enabled else "Hairpin ornament motion off"
    if event.keycode==KEY_F and event.shift_pressed:
        stop_clip()
        earrings_enabled=not earrings_enabled
        pose_notice="Earring motion on" if earrings_enabled else "Earring motion off"
    if event.keycode==KEY_F and not event.shift_pressed:
        hair.enabled=not hair.enabled
        pose_notice="Crown hair motion on" if hair.enabled else "Crown hair motion off"
    if event.keycode==KEY_X:
        stop_clip();loose_hair_enabled=not loose_hair_enabled
        pose_notice="Loose hair motion on" if loose_hair_enabled else "Loose hair motion off"
    if event.keycode==KEY_T:play_clip("res://demo_bust_clip.json" if event.shift_pressed else "res://demo_clip.json")
    if event.keycode==KEY_P:pause_clip(not clip.paused)
    if event.keycode==KEY_ESCAPE:stop_clip()
    if event.keycode in [KEY_1,KEY_2,KEY_3]:
        var slot=int(event.keycode-KEY_1)+1
        if event.ctrl_pressed:save_pose(slot)
        else:recall_pose(slot)
    if event.keycode==KEY_J:eyelids.trigger("screen_left")
    if event.keycode==KEY_K:eyelids.trigger("screen_right")
    if event.keycode==KEY_U:eyelids.reset()
    if event.keycode==KEY_N:gestures.trigger("acknowledge")
    if event.keycode==KEY_G:gestures.trigger("greet")
    if event.keycode==KEY_ESCAPE:gestures.cancel()
    if event.keycode==KEY_H:body_follow=true
    if event.keycode==KEY_L:
        if audio_mouth.active:audio_mouth.stop();face.release_speech()
        elif audio_mouth.load_wav("res://audio_fixture.wav"):audio_mouth.play()
    if event.keycode==KEY_M:mouse_follow=not mouse_follow
    if event.keycode==KEY_R:apply_controls({"reset":true})
    if event.keycode==KEY_COMMA or event.keycode==KEY_PERIOD:
        stop_clip()
        # Derive from the selected face, including clip/live/direct API changes.
        expression_index=posmod(expression_ids.find(face.expression)+(-1 if event.keycode==KEY_COMMA else 1),expression_ids.size())
        _set_expression(expression_ids[expression_index])

func _process(delta):
    if not rig_ready:return
    live_input.poll(delta,self)
    if live_proof:
        print("LIVE_FRAME ",JSON.stringify({"time":clock_time,"accepted":live_input.accepted,"rejected":live_input.rejected,"status":live_input.status,"head":target.x,"body":body_target.x,"expression":face.expression,"mouth":face.mouth_state}))
        if clock_time>=18.0:get_tree().quit()
    if clip_proof:
        clip_proof_time+=delta
        _run_clip_proof()
    if clip.paused:
        # Expression selection can change while the clock is paused. Never
        # leave another expression's iris layers painted over the new face.
        _sync_gaze_render_state()
        return
    var dispatch=clip.dispatch_id
    for controls in clip.step(delta):
        if not apply_controls(controls,"clip"):
            pose_notice="Clip stopped: rejected control"
            stop_clip()
            break
        if clip.dispatch_id!=dispatch:break
    pose_status.text="" if pose_proof or clip_proof else pose_notice
    clock_time+=delta
    if brow_proof:_run_brow_proof()
    elif breath_proof:_run_breath_proof()
    elif look_proof:_run_look_proof()
    elif ornament_proof:_run_ornament_proof()
    elif gaze_proof:_run_gaze_proof()
    elif hair_proof:_run_hair_proof()
    elif clip_proof:pass
    elif pose_proof:_run_pose_proof()
    elif eyelid_proof:_run_eyelid_proof()
    elif gesture_proof:_run_gesture_proof()
    elif secondary_proof:_run_secondary_proof()
    elif body_proof:_run_body_proof()
    elif audio_proof:_run_audio_proof()
    elif proof:_run_proof()
    elif not external_controls:
        if mouse_follow:
            var p=(get_global_mouse_position()-Vector2(284,380))/Vector2(284,380)
            apply_controls({"head_x":p.x,"head_y":p.y,"head_tilt":p.x*0.55},"local")
        else:
            apply_controls({"head_tilt":float(Input.is_physical_key_pressed(KEY_D))-float(Input.is_physical_key_pressed(KEY_A)),"head_x":float(Input.is_physical_key_pressed(KEY_RIGHT))-float(Input.is_physical_key_pressed(KEY_LEFT)),"head_y":float(Input.is_physical_key_pressed(KEY_DOWN))-float(Input.is_physical_key_pressed(KEY_UP))},"local")
        if not body_follow:
            body_target=Vector3(float(Input.is_physical_key_pressed(KEY_E))-float(Input.is_physical_key_pressed(KEY_Q)),float(Input.is_physical_key_pressed(KEY_C))-float(Input.is_physical_key_pressed(KEY_Z)),float(Input.is_physical_key_pressed(KEY_S))-float(Input.is_physical_key_pressed(KEY_W)))
        speech=Input.is_physical_key_pressed(KEY_SPACE)
        manual_blink=1.0 if Input.is_physical_key_pressed(KEY_B) else -1.0
        hud.text="RYOKO / LIVE MOTION RIG"
        hint.text="T play clip · P pause/resume · Esc stop · 1/2/3 recall · R reset"
    if attention.mouse_follow:
        var pointer=(get_global_mouse_position()-Vector2(284,315))/Vector2(284,250)
        attention.aim(pointer.x,pointer.y)
    attention.step(delta)
    gestures.sample(delta)
    var effective_head=(target+gestures.head+attention.head).clamp(Vector3(-1,-1,-1),Vector3.ONE)
    current=current.lerp(effective_head,1.0-exp(-delta/0.22))
    if body_follow:body_target=target
    var effective_body=(body_target+gestures.body).clamp(Vector3(-1,-1,-1),Vector3.ONE)
    body_current=body_current.lerp(effective_body,1.0-exp(-delta/0.22))
    breathing.step(delta)
    skin_material.set_shader_parameter("controlled_breath",breathing.amount)
    _step_bounce(delta)
    _step_chest(delta)
    var head_anchor=Vector2(0,-550).rotated(current.x*deg_to_rad(6.0)+body_current.x*deg_to_rad(3.0))+Vector2(current.y*16+body_current.y*8,current.z*12+body_current.z*5+bounce_position)
    hair.step(head_anchor,delta)
    var ornament_anchor=deform_independent(ornament.PIVOT+hair.offset*hair.weight(ornament.PIVOT),current,body_current,sin(clock_time*TAU/6.0))
    ornament_anchor+=Vector2(0,bounce_position)
    var ornament_frame=current.x*deg_to_rad(6.0)+body_current.x*deg_to_rad(3.0)
    ornament.step(ornament_anchor,ornament_frame,delta)
    ornament_pivot.position=ornament_anchor
    ornament_pivot.rotation=ornament_frame+ornament.angle
    ornament_pivot.visible=ornament.enabled
    skin_material.set_shader_parameter("ornament_separate",ornament.enabled)
    _step_earrings(delta,ornament_frame)
    _step_loose_hair(delta,ornament_frame)
    skin_material.set_shader_parameter("hair_offset",hair.offset)
    skin_material.set_shader_parameter("chest_offset",chest_offset)
    skin_material.set_shader_parameter("head_tilt",current.x*deg_to_rad(6.0))
    skin_material.set_shader_parameter("head_offset",Vector2(current.y*16.0,current.z*12.0))
    skin_material.set_shader_parameter("spine_tilt",body_current.x*deg_to_rad(3.0))
    skin_material.set_shader_parameter("torso_offset",Vector2(body_current.y*8.0,body_current.z*5.0+bounce_position))
    skin_material.set_shader_parameter("breath",sin(clock_time*TAU/6.0))
    if live_proof:
        hud.text="RYOKO / LOCAL LIVE INPUT"
        hint.text=live_input.status+" · packets "+str(live_input.accepted)+" · separate Python sender"
    eyelids.step(delta)
    if eyelids.busy():
        blink_until=-1.0
        next_blink=max(next_blink,clock_time+0.6)
    if auto_blink and not eyelids.busy() and clock_time>=next_blink:
        blink_until=clock_time+0.14;next_blink=clock_time+3.2
    var closed=manual_blink if manual_blink>=0.0 else (1.0 if auto_blink and clock_time<blink_until else 0.0)
    var eyes=eyelids.resolve(closed)
    # Existing L artwork sits on screen-right; R artwork on screen-left.
    face.set_blink(eyes.y,eyes.x)
    if gaze.mouse_follow:
        var pointer=(get_global_mouse_position()-Vector2(284,315))/Vector2(284,250)
        gaze.set_target(pointer.x,pointer.y)
    gaze.step(delta)
    skin_material.set_shader_parameter("gaze_direction",(gaze.current+attention.eye).clamp(Vector2(-1,-1),Vector2.ONE))
    brows.step(delta)
    skin_material.set_shader_parameter("brow_amount",brows.current)
    _sync_gaze_render_state()
    if audio_mouth.active:
        var shape=audio_mouth.step(delta)
        if shape=="REST":face.release_speech()
        else:face.set_mouth(shape)
    elif speech:face.set_mouth(["A","E","I","O","U"][int(clock_time*7.0)%5])
    elif not proof and not external_controls:face.release_speech()

func _setup_optional_effects():
    # Separate post-gaze layer, sharing the exact face geometry and vertex source.
    # This avoids both overwritten tears and another sampler in the face shader.
    effects_viewport = SubViewport.new()
    effects_viewport.name = "RegisteredOptionalEffectsViewport"
    effects_viewport.size = Vector2i(1136, 1384)
    effects_viewport.transparent_bg = true
    effects_viewport.render_target_update_mode = SubViewport.UPDATE_DISABLED
    add_child(effects_viewport)
    face.optional_effects.reparent(effects_viewport, false)
    effects_surface = MeshInstance2D.new()
    effects_surface.name = "OptionalEffectsDeformedMesh"
    effects_surface.mesh = surface.mesh
    effects_surface.texture = effects_viewport.get_texture()
    effects_material = ShaderMaterial.new()
    effects_material.shader = load("res://optional_effects.gdshader")
    effects_surface.material = effects_material
    add_child(effects_surface)
    # All uniforms in the effects shader come from the shared vertex include.
    # Discover them rather than maintain a second, drifting parameter list.
    for uniform in effects_material.shader.get_shader_uniform_list():
        effects_uniforms.append(StringName(uniform.name))
    _sync_optional_effects()

func _sync_optional_effects():
    if effects_surface == null:return
    var enabled = true in face.optional_effects.state.values()
    effects_surface.visible = enabled
    effects_viewport.render_target_update_mode = SubViewport.UPDATE_ALWAYS if enabled else SubViewport.UPDATE_DISABLED
    effects_surface.transform = surface.transform
    for key in effects_uniforms:
        effects_material.set_shader_parameter(key, skin_material.get_shader_parameter(key))

func _setup_earrings():
    earring_metadata=JSON.parse_string(FileAccess.get_file_as_string("res://rig_assets/earring_layers.json")).layers
    for side in ["screen_left","screen_right"]:
        var entry=earring_metadata[side]
        var pivot=Vector2(entry.pivot[0],entry.pivot[1])
        var box=entry.source_rect
        var rect=Rect2(box[0],box[1],box[2],box[3])
        earrings[side]=load("res://earring_driver.gd").new()
        var node=Node2D.new();node.name="EarringPivot_"+side;node.visible=false;surface.add_child(node)
        earring_pivots[side]=node
        var sprite=Sprite2D.new()
        sprite.texture=load("res://rig_assets/earring_"+side+".png")
        sprite.centered=false;sprite.region_enabled=true;sprite.region_rect=rect
        sprite.region_filter_clip_enabled=true;sprite.position=rect.position-pivot
        node.add_child(sprite);earring_sprites[side]=sprite
    skin_material.set_shader_parameter("earring_underpaint",load("res://rig_assets/earring_underpaint.png"))
    skin_material.set_shader_parameter("earring_clear_masks",load("res://rig_assets/earring_clear_masks.png"))

func _setup_gaze_profiles():
    # Neutral retains the already-approved textures and rendering path.
    var neutral={}
    for side in ["screen_left","screen_right"]:
        for layer in ["iris","sclera","aperture"]:
            var key=layer+"_"+side
            neutral[key]=load("res://rig_assets/"+key+".png")
    gaze_profiles["neutral"]=neutral
    var manifest=JSON.parse_string(FileAccess.get_file_as_string("res://rig_assets/expression_gaze/profiles.json"))
    for id in manifest.profiles:
        if not face.emotion_eyes.has(id):
            push_error("Unknown expression gaze profile: "+id);continue
        var profile={}
        for side in ["screen_left","screen_right"]:
            for layer in ["iris","sclera","aperture"]:
                profile[layer+"_"+side]=load("res://"+manifest.profiles[id][side][layer])
        gaze_profiles[id]=profile

func _sync_gaze_render_state():
    _sync_optional_effects()
    expression_index=expression_ids.find(face.expression)
    skin_material.set_shader_parameter("brow_enabled",face.expression=="neutral")
    var supported=_select_gaze_profile(face.expression)
    skin_material.set_shader_parameter("gaze_open",Vector2(1 if supported and not face.blink_right else 0,1 if supported and not face.blink_left else 0))

func _select_gaze_profile(id:String)->bool:
    var supported=gaze_profiles.has(id)
    var selected=id if supported else "neutral"
    if gaze_profile_name!=selected:
        for key in gaze_profiles[selected]:skin_material.set_shader_parameter(key,gaze_profiles[selected][key])
        gaze_profile_name=selected
    return supported

func _step_loose_hair(delta,frame_angle):
    for side in loose_hair:
        var root_position=Vector2(340,570) if side=="screen_left" else Vector2(780,570)
        # Exclude periodic breathing so a held pose has no invented idle sway.
        var anchor=deform_independent(root_position,current,body_current,0)+Vector2(0,bounce_position)
        var lock=loose_hair[side]
        lock.enabled=loose_hair_enabled;lock.step(anchor,delta)
        var local_offset=lock.offset.rotated(-frame_angle)
        skin_material.set_shader_parameter("loose_hair_left" if side=="screen_left" else "loose_hair_right",local_offset)

func _step_earrings(delta,frame_angle):
    var separated=Vector2.ZERO
    for side in ["screen_left","screen_right"]:
        var entry=earring_metadata[side]
        var pivot=Vector2(entry.pivot[0],entry.pivot[1])
        var anchor=deform_independent(pivot,current,body_current,sin(clock_time*TAU/6.0))+Vector2(0,bounce_position)
        var driver=earrings[side]
        driver.enabled=earrings_enabled
        driver.step(anchor,frame_angle,delta)
        var node=earring_pivots[side]
        node.position=anchor;node.rotation=frame_angle+driver.angle
        # Exact neutral pixels use original art; separation activates only when
        # the pendant departs from its inherited head orientation.
        node.visible=earrings_enabled and abs(driver.angle)>.00001
        if side=="screen_left":separated.x=1.0 if node.visible else 0.0
        else:separated.y=1.0 if node.visible else 0.0
    skin_material.set_shader_parameter("earring_separate",separated)

func _run_proof():
    var t=clock_time
    var stage=0 if t<3 else (1 if t<7 else (2 if t<9 else (3 if t<13 else (4 if t<15 else (5 if t<17 else (6 if t<21 else 7))))))
    var labels=["REST / settled posture","LEAN LEFT / linked upper torso","SETTLE / return to center","LEAN RIGHT / linked upper torso","SETTLE / return to center","SMALL NOD / relaxed follow","SPEAK / held pose + blink","REST / quiet recovery"]
    var poses=[Vector3.ZERO,Vector3(-0.60,-0.25,0),Vector3.ZERO,Vector3(0.60,0.25,0),Vector3.ZERO,Vector3(0,0,0.5),Vector3(-0.22,0,0),Vector3.ZERO]
    if stage!=proof_stage:
        proof_stage=stage
        var pose=poses[stage]
        apply_controls({"head_tilt":pose.x,"head_x":pose.y,"head_y":pose.z})
        proof_log.store_line(JSON.stringify({"time":t,"stage":labels[stage],"target":[pose.x,pose.y,pose.z]}));proof_log.flush()
        print("MOTION_STAGE ",labels[stage])
    hud.text="RYOKO / "+labels[stage]
    hint.text="Held poses, eased transitions · one shoulder/chest frame · existing art"
    speech=stage==6
    if not speech:face.release_speech()
    if t>=25.0:proof_log.close();get_tree().quit()

# CPU reference of the hierarchical shader, for coupling invariants.
func deform_point(rest:Vector2,controls:Vector3,breath:float)->Vector2:
    return deform_independent(rest,controls,controls,breath)

func deform_independent(rest:Vector2,controls:Vector3,body:Vector3,breath:float)->Vector2:
    var head_weight=1.0-smoothstep(710.0,855.0,rest.y)
    var head=(rest-Vector2(568,790)).rotated(controls.x*deg_to_rad(6.0))+Vector2(568,790)+Vector2(controls.y*16,controls.z*12)
    var neck=rest.lerp(head,head_weight)
    var torso_weight=1.0-smoothstep(1260.0,1384.0,rest.y)
    var torso=(neck-Vector2(568,1340)).rotated(body.x*deg_to_rad(3.0))+Vector2(568,1340)+Vector2(body.y*8,body.z*5)-Vector2(0,breath*1.2)
    return neck.lerp(torso,torso_weight)

func _run_audio_proof():
    if clock_time>=2.0 and not audio_proof_started:
        audio_proof_started=true
        audio_mouth.play()
    target=Vector3(-0.22,0,0) if clock_time>6.0 and clock_time<11.0 else Vector3.ZERO
    hud.text="RYOKO / AUDIO-DRIVEN MOUTH"
    var state="SILENCE / resting mouth" if audio_mouth.level<0.045 else "AUDIO / opening follows loudness"
    hint.text=state+" · synthetic tone test, not phoneme recognition"
    if clock_time>=16.0:get_tree().quit()

func _finite_axis(value)->float:
    var v=float(value)
    return clamp(v,-1.0,1.0) if is_finite(v) else 0.0

func _run_body_proof():
    var t=clock_time
    var stage=0 if t<3 else (1 if t<6 else (2 if t<8 else (3 if t<11 else (4 if t<13 else (5 if t<16 else 6)))))
    var labels=["REST / independent controls", "HEAD ONLY / shoulders stay still", "SETTLE / relaxed neutral", "TORSO LED / head rides with body", "SETTLE / relaxed neutral", "COUNTERPOSE / head stays upright", "RECOVER / return to neutral"]
    var heads=[Vector3.ZERO,Vector3(.55,0,0),Vector3.ZERO,Vector3.ZERO,Vector3.ZERO,Vector3(-.35,0,0),Vector3.ZERO]
    var bodies=[Vector3.ZERO,Vector3.ZERO,Vector3.ZERO,Vector3(.7,0,0),Vector3.ZERO,Vector3(.7,0,0),Vector3.ZERO]
    target=heads[stage];body_target=bodies[stage];body_follow=false
    hud.text="RYOKO / "+labels[stage]
    hint.text="Separate head / torso channels · shoulders and chest remain coupled"
    if t>=20.0:get_tree().quit()

# A damped mass follows the actual torso frame, not time or head input.
# Movement creates a small inertial lag; a held pose decays to exactly rest.
# Breath is deliberately excluded, so breathing cannot drive repeated bounce.
func _step_chest(delta):
    var anchor=Vector2(0,-210).rotated(body_current.x*deg_to_rad(3))+Vector2(body_current.y*8,body_current.z*5+bounce_position)
    if not chest_initialized or not chest_enabled:
        chest_anchor=anchor;chest_initialized=true;chest_offset=Vector2.ZERO;chest_velocity=Vector2.ZERO
        return
    var dt=clamp(delta,0.0,0.1)
    chest_offset-=(anchor-chest_anchor)*0.9
    chest_anchor=anchor
    var count=maxi(1,int(ceil(dt*240.0)))
    var step=dt/count
    for i in range(count):
        chest_velocity+=(-CHEST_FREQUENCY*CHEST_FREQUENCY*chest_offset-2.0*CHEST_DAMPING*CHEST_FREQUENCY*chest_velocity)*step
        chest_offset+=chest_velocity*step
        if chest_offset.length()>CHEST_LIMIT:
            chest_offset=chest_offset.limit_length(CHEST_LIMIT)
            var outward=chest_velocity.dot(chest_offset.normalized())
            if outward>0:chest_velocity-=chest_offset.normalized()*outward
    if chest_offset.length()<0.00001 and chest_velocity.length()<0.0001:
        chest_offset=Vector2.ZERO;chest_velocity=Vector2.ZERO

func chest_weight(rest:Vector2)->float:
    return smoothstep(920.0,1050.0,rest.y)*(1.0-smoothstep(1280.0,1384.0,rest.y))*(1.0-smoothstep(310.0,480.0,abs(rest.x-568.0)))

# A user-triggered small torso lift, followed by damped recovery. No idle cycle.
func _step_bounce(delta):
    var dt=clamp(delta,0.0,0.1)
    var count=maxi(1,int(ceil(dt*240.0)))
    var step=dt/count
    for i in range(count):
        bounce_velocity+=(-81.0*bounce_position-10.8*bounce_velocity)*step
        bounce_position+=bounce_velocity*step
    if abs(bounce_position)<.0001 and abs(bounce_velocity)<.001:
        bounce_position=0.0;bounce_velocity=0.0

func _run_secondary_proof():
    var t=clock_time
    var stage=0 if t<2 else (1 if t<5 else (2 if t<8 else (3 if t<11 else 4)))
    if stage!=proof_stage:
        proof_stage=stage
        if stage in [1,2,3]:apply_controls({"bounce":true})
    target=Vector3.ZERO;body_target=Vector3.ZERO;body_follow=false
    var labels=["REST / no idle bounce","SMALL BOUNCE / soft follow-through","SMALL BOUNCE / repeat","SMALL BOUNCE / repeat","REST / fully settled"]
    hud.text="RYOKO / "+labels[stage]
    hint.text="Torso rises and settles · whole chest follows with a soft delay"
    if t>=14.0:get_tree().quit()

func _run_gesture_proof():
    var t=clock_time
    var events={2.0:"acknowledge",6.0:"greet",11.0:"greet"}
    for time in events:
        if t>=time and not gesture_events.has(time):
            gestures.trigger(events[time]);gesture_events[time]=true
    if t>=11.7 and not gesture_events.has("cancel"):
        gestures.cancel();gesture_events["cancel"]=true
    # A nonzero live posture makes return-to-live-pose visible.
    target=Vector3(.2,0,0) if t>=9.0 else Vector3.ZERO
    var label="REST / live neutral"
    if t>=2.0 and t<5.0:label="ACKNOWLEDGE / one gentle dip"
    elif t>=6.0 and t<9.0:label="GREET / one lean and return"
    elif t>=9.0 and t<11.0:label="LIVE POSE / slight held tilt"
    elif t>=11.0 and t<11.7:label="GREET / layered over live pose"
    elif t>=11.7:label="CANCEL / return to live pose"
    hud.text="RYOKO / "+label
    hint.text="One-shot gestures · original controls remain live · no looping"
    if t>=16.0:get_tree().quit()

func _run_eyelid_proof():
    var t=clock_time
    auto_blink=t>=14.0
    var actions={2.0:{"wink":"screen_left","wink_duration":0.5},5.0:{"wink":"screen_right","wink_duration":0.5},8.0:{"eye_screen_left":1.0,"eye_screen_right":0.0,"gesture":"greet"},10.0:{"release_eye_controls":true},12.0:{"wink":"both","wink_duration":0.35}}
    for time in actions:
        if t>=time and not eyelid_events.has(time):
            apply_controls(actions[time]);eyelid_events[time]=true
    var label="REST / ready" if t<14.0 else "REST / automatic blink"
    if t>=2.0 and t<4.0:label="WINK / screen-left eye"
    elif t>=5.0 and t<7.0:label="WINK / screen-right eye"
    elif t>=8.0 and t<10.0:label="HOLD / left eye + greeting"
    elif t>=10.0 and t<12.0:label="RELEASE / return to auto blink"
    elif t>=12.0 and t<14.0:label="BOTH / explicit blink"
    hud.text="RYOKO / "+label
    hint.text="Screen-left = your left · existing eyelid artwork · independent controls"
    if t>=16.0:get_tree().quit()

func save_pose(slot:int)->bool:
    var saved_body=target if body_follow else body_target
    var data={"head_tilt":target.x,"head_x":target.y,"head_y":target.z,"body_tilt":saved_body.x,"body_x":saved_body.y,"body_y":saved_body.z,"body_follow":body_follow}
    var ok=pose_store.save_slot(slot,data)
    pose_notice="Saved pose "+str(slot) if ok else pose_store.error_message
    return ok

func recall_pose(slot:int)->bool:
    var data=pose_store.recall(slot)
    if data.is_empty():pose_notice="Pose "+str(slot)+" is empty";return false
    target=Vector3(data.head_tilt,data.head_x,data.head_y)
    body_target=Vector3(data.body_tilt,data.body_x,data.body_y)
    body_follow=data.body_follow;external_controls=true;mouse_follow=false
    pose_notice="Recalled pose "+str(slot)
    return true

func _run_pose_proof():
    var t=clock_time
    var actions={2.0:{"head_tilt":-.45,"head_x":-.2,"body_tilt":-.3,"pose_save":1},5.0:{"head_tilt":.35,"head_x":.2,"body_tilt":.45,"pose_save":2},8.0:{"head_tilt":0,"head_x":0,"body_tilt":0},10.0:{"pose_load":1},13.0:{"pose_load":2},14.0:{"gesture":"acknowledge"},17.0:{"head_tilt":0,"head_x":0,"body_tilt":0}}
    for time in actions:
        if t>=time and not pose_events.has(time):
            apply_controls(actions[time]);pose_events[time]=true
    var label="REST / live neutral"
    if t>=2.0 and t<5.0:label="SAVE 1 / relaxed left pose"
    elif t>=5.0 and t<8.0:label="SAVE 2 / right pose"
    elif t>=8.0 and t<10.0:label="NEUTRAL / release position"
    elif t>=10.0 and t<13.0:label="RECALL 1 / smooth return"
    elif t>=13.0 and t<17.0:label="RECALL 2 / gesture still works"
    elif t>=17.0:label="RECOVER / live neutral"
    hud.text="RYOKO / "+label
    hint.text="Saved head/body poses · eased recall · facial controls remain live"
    if t>=20.0:get_tree().quit()

func play_clip(path:String)->bool:
    var was_active=clip.active or clip.paused
    if not clip.load_file(path,expression_ids):pose_notice=clip.error_message;return false
    if was_active:_release_clip_channels()
    clip_channels.clear()
    audio_mouth.player.stream_paused=false
    external_controls=true
    pose_notice="Clip playing"
    return clip.play()

func pause_clip(paused:bool):
    if not clip.active:return
    clip.paused=paused;audio_mouth.player.stream_paused=paused
    pose_notice="Clip paused" if paused else "Clip playing"
    if pose_status!=null:pose_status.text=pose_notice

func stop_clip():
    var was_active=clip.active or clip.paused
    clip.stop()
    if was_active:_release_clip_channels()
    clip_channels.clear()
    if audio_mouth!=null:
        audio_mouth.player.stream_paused=false
        if was_active:
            audio_mouth.stop();face.release_speech();gestures.cancel();eyelids.reset()
            pose_notice="Clip stopped"

func _track_clip_channels(data):
    for key in data:
        if key=="effects":
            for effect in data.effects:clip_channels["effect:"+effect]=true
        elif key in ["gaze_x","gaze_y"]:clip_channels["gaze"]=true
        elif key in ["brow_raise","brow_screen_left","brow_screen_right"]:clip_channels["brows"]=true
        elif key=="breath_level" or (key in ["breath_trigger","breath_cancel"] and data[key]):clip_channels["breath"]=true
        elif key in ["look_x","look_y"] or (key=="look_release" and data[key]):clip_channels["look"]=true

func _release_clip_channels():
    # Only release channels this clip actually touched. Old clips do not take
    # ownership of new live controls. Persistent secondary toggles stay set.
    for effect in preload("res://optional_effects.gd").NAMES:
        if clip_channels.has("effect:"+effect):face.optional_effects.apply({effect:false})
    if clip_channels.has("gaze"):gaze.set_target(0,0);gaze.mouse_follow=false
    if clip_channels.has("brows"):brows.set_both(0)
    if clip_channels.has("breath"):breathing.cancel()
    if clip_channels.has("look"):attention.release()

func _run_clip_proof():
    var t=clip_proof_time
    if t>=1.0 and not clip_events.has("start"):
        play_clip("res://demo_clip.json");clip_events["start"]=true
    if t>=5.8 and not clip_events.has("pause"):
        pause_clip(true);clip_events["pause"]=true
    if t>=7.3 and not clip_events.has("resume"):
        pause_clip(false);clip_events["resume"]=true
    hud.text="RYOKO / "+("CLIP PAUSED" if clip.paused else ("CUE CLIP / combined performance" if clip.active else "CLIP COMPLETE / resting"))
    if not clip_events.has("start"):hud.text="RYOKO / READY / timed clip"
    hint.text="Timed pose + gesture + wink + silent mouth cues · one-shot playback"
    if t>=19.0:get_tree().quit()

func _run_hair_proof():
    var t=clock_time
    var stage=0 if t<2 else (1 if t<5 else (2 if t<8 else (3 if t<11 else (4 if t<14 else 5))))
    var heads=[Vector3.ZERO,Vector3(-.65,-.25,0),Vector3(.65,.25,0),Vector3.ZERO,Vector3(-.65,-.25,0),Vector3.ZERO]
    target=heads[stage];body_target=Vector3.ZERO;body_follow=false
    hair.enabled=stage<4
    hud.text="RYOKO / "+["REST / hair settles","LEAN LEFT / crown follows","LEAN RIGHT / crown follows","HOLD / no idle hair loop","OFF / rigid comparison","OFF / return neutral"][stage]
    hint.text="Small crown/bun lag · roots fixed above eyes · existing artwork"
    if t>=17.0:get_tree().quit()

func _exit_tree():
    live_input.stop()

func _run_gaze_proof():
    external_controls=true
    var t=clock_time
    var d=Vector2.ZERO
    var label="CENTER / rigid iris rest"
    if t>=2 and t<5:d=Vector2(-1,0);label="GLANCE / screen-left"
    elif t>=5 and t<8:d=Vector2(1,0);label="GLANCE / screen-right"
    elif t>=8 and t<10:d=Vector2(0,-1);label="GLANCE / up"
    elif t>=10 and t<12:d=Vector2(0,1);label="GLANCE / down"
    elif t>=12 and t<15:d=Vector2(-.7,0);label="GLANCE + head tilt / mouth + blink"
    gaze.set_target(d.x,d.y)
    target=Vector3(.45,0,0) if t>=12 and t<15 else Vector3.ZERO
    body_target=Vector3.ZERO;body_follow=false
    if t>=12 and t<15:face.set_mouth("E")
    else:face.release_speech()
    auto_blink=true
    hud.text="RYOKO / "+label
    hint.text="Rigid iris translation · fixed eyelids and hair · V mouse gaze"
    if t>=18:get_tree().quit()

func _run_breath_proof():
    external_controls=true
    var t=clock_time
    for start in [2.0,10.0]:
        if t>=start and not breath_events.has(start):breathing.trigger();breath_events[start]=true
    target=Vector3(.25,0,0) if t>=9 else Vector3.ZERO
    body_target=Vector3(-.2,0,0) if t>=9 else Vector3.ZERO
    body_follow=false
    var label="REST / no repeating breath"
    if breathing.active:
        label="INHALE / connected ribs and shoulders" if breathing.elapsed<2.4 else "EXHALE / gentle return to rest"
    hud.text="RYOKO / "+label
    hint.text="Optional one-shot breath · no head bob · I trigger · original rig preserved"
    if t>=18:get_tree().quit()

func _run_brow_proof():
    external_controls=true
    var t=clock_time
    var value=Vector2.ZERO
    var label="REST / original neutral brows"
    if t>=2 and t<5:value=Vector2.ONE;label="RAISE / both brows"
    elif t>=5 and t<8:value=-Vector2.ONE;label="LOWER / both brows"
    elif t>=8 and t<11:value=Vector2(1,0);label="RAISE / screen-left brow"
    elif t>=11 and t<14:value=Vector2(0,1);label="RAISE / screen-right brow + mouth"
    brows.target=value
    if t>=11 and t<14:face.set_mouth("E")
    else:face.release_speech()
    target=Vector3(.25,0,0) if t>=11 and t<14 else Vector3.ZERO
    body_target=Vector3.ZERO;body_follow=false
    hud.text="RYOKO / "+label
    hint.text="Rigid brow translation · hair stays in front · neutral face only · O raise"
    if t>=17:get_tree().quit()

func _run_look_proof():
    var stage=min(int(clock_time/3.0),5)
    if stage!=look_stage:
        look_stage=stage
        if stage==0:apply_controls({"reset":true,"body_follow":false})
        elif stage==1:apply_controls({"look_x":-.9,"look_y":-.25})
        elif stage==2:apply_controls({"look_x":.9,"look_y":.15})
        elif stage==3:apply_controls({"look_x":-.55,"look_y":-.8})
        elif stage==4:apply_controls({"look_x":.5,"look_y":.55,"mouth":"E"})
        else:apply_controls({"look_release":true,"mouth":"RELEASE"})
    external_controls=true
    hud.text="RYOKO / "+["REST / look-at off","LOOK SCREEN LEFT / eyes lead","LOOK SCREEN RIGHT / head follows","LOOK UP LEFT / held target","LOOK DOWN RIGHT / mouth layered","RELEASE / return to original pose"][stage]
    hint.text="Coordinated rigid iris + head · torso anchored · Y pointer look-at"
    if clock_time>=18.0:get_tree().quit()


func _run_ornament_proof():
    var t=clock_time
    var stage=0 if t<2 else (1 if t<5 else (2 if t<8 else (3 if t<11 else (4 if t<14 else (5 if t<17 else 6)))))
    var labels=["REST / original ornament", "HEAD LEFT / hangs from fixed pin", "HEAD RIGHT / inertial follow-through", "TORSO + LIFT / anchor-driven sway", "HOLD / settles without an idle loop", "OFF / original attached ornament", "RESET / quiet neutral"]
    if stage!=ornament_stage:
        ornament_stage=stage
        var controls=[
            {"reset":true,"auto_blink":false,"body_follow":false},
            {"head_tilt":-.75,"head_x":-.6,"body_tilt":0},
            {"head_tilt":.75,"head_x":.6,"body_tilt":0},
            {"head_tilt":0,"head_x":0,"body_tilt":-.8,"body_x":-.5,"bounce":true},
            {"head_tilt":0,"body_tilt":.6,"body_x":0},
            {"head_tilt":.5,"body_tilt":0,"ornament_secondary":false},
            {"reset":true,"auto_blink":false,"ornament_secondary":true,"body_follow":false}
        ]
        apply_controls(controls[stage])
        print("ORNAMENT_STAGE ",JSON.stringify({"time":t,"stage":stage,"label":labels[stage]}))
    hud.text="RYOKO / HAIRPIN ORNAMENT"
    hint.text=labels[stage]
    if Engine.get_process_frames()%15==0:
        print("ORNAMENT_SAMPLE ",JSON.stringify({"time":t,"stage":stage,"angle":ornament.angle,"swing":ornament.swing,"enabled":ornament.enabled,"pivot":[ornament_pivot.position.x,ornament_pivot.position.y]}))
    if t>=20.0:get_tree().quit()

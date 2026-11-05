extends Node2D
# Live 2D weighted deformation. Existing facial artwork is rendered into a
# transparent viewport and deformed together, preserving registration.
var face
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
    surface.material=skin_material
    add_child(surface)
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
    if source=="external":external_controls=true
    if data.get("reset",false):
        eyelids.reset();gestures.cancel();audio_mouth.stop();body_follow=true;body_target=Vector3.ZERO;target=Vector3.ZERO;face.reset_neutral();manual_blink=-1.0;speech=false;mouse_follow=false;auto_blink=true;external_controls=false
    if data.has("head_tilt"):target.x=clamp(float(data.head_tilt),-1.0,1.0)
    if data.has("head_x"):target.y=clamp(float(data.head_x),-1.0,1.0)
    if data.has("head_y"):target.z=clamp(float(data.head_y),-1.0,1.0)
    if data.has("body_tilt") or data.has("body_x") or data.has("body_y"):
        body_follow=false
        if data.has("body_tilt"):body_target.x=_finite_axis(data.body_tilt)
        if data.has("body_x"):body_target.y=_finite_axis(data.body_x)
        if data.has("body_y"):body_target.z=_finite_axis(data.body_y)
    if data.get("bounce",false):bounce_velocity=-280.0
    if data.has("chest_secondary"):chest_enabled=bool(data.chest_secondary)
    if data.has("body_follow"):body_follow=bool(data.body_follow)
    var accepted=true
    if data.has("expression"):accepted=face.set_expression(String(data.expression))
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
    return accepted

func _unhandled_key_input(event):
    if not event.is_pressed() or event.echo:return
    if event.keycode in [KEY_M,KEY_A,KEY_D,KEY_LEFT,KEY_RIGHT,KEY_UP,KEY_DOWN,KEY_B,KEY_SPACE,KEY_Q,KEY_E,KEY_W,KEY_S,KEY_Z,KEY_C,KEY_H]:external_controls=false
    if event.keycode in [KEY_Q,KEY_E,KEY_W,KEY_S,KEY_Z,KEY_C]:body_follow=false
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
        expression_index=posmod(expression_index+(-1 if event.keycode==KEY_COMMA else 1),expression_ids.size())
        face.set_expression(expression_ids[expression_index])

func _process(delta):
    if not rig_ready:return
    clock_time+=delta
    if eyelid_proof:_run_eyelid_proof()
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
        hint.text="J/K screen-side wink · U release eyes · N dip · G greet · R reset"
    gestures.sample(delta)
    var effective_head=(target+gestures.head).clamp(Vector3(-1,-1,-1),Vector3.ONE)
    current=current.lerp(effective_head,1.0-exp(-delta/0.22))
    if body_follow:body_target=target
    var effective_body=(body_target+gestures.body).clamp(Vector3(-1,-1,-1),Vector3.ONE)
    body_current=body_current.lerp(effective_body,1.0-exp(-delta/0.22))
    _step_bounce(delta)
    _step_chest(delta)
    skin_material.set_shader_parameter("chest_offset",chest_offset)
    skin_material.set_shader_parameter("head_tilt",current.x*deg_to_rad(6.0))
    skin_material.set_shader_parameter("head_offset",Vector2(current.y*16.0,current.z*12.0))
    skin_material.set_shader_parameter("spine_tilt",body_current.x*deg_to_rad(3.0))
    skin_material.set_shader_parameter("torso_offset",Vector2(body_current.y*8.0,body_current.z*5.0+bounce_position))
    skin_material.set_shader_parameter("breath",sin(clock_time*TAU/6.0))
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
    if audio_mouth.active:
        var shape=audio_mouth.step(delta)
        if shape=="REST":face.release_speech()
        else:face.set_mouth(shape)
    elif speech:face.set_mouth(["A","E","I","O","U"][int(clock_time*7.0)%5])
    elif not proof and not external_controls:face.release_speech()

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

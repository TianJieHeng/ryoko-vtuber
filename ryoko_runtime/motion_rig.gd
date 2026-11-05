extends Node2D
# Live 2D weighted deformation. Existing facial artwork is rendered into a
# transparent viewport and deformed together, preserving registration.
var face
var surface: MeshInstance2D
var skin_material: ShaderMaterial
var target = Vector3.ZERO # tilt, horizontal offset, vertical offset
var current = Vector3.ZERO
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
        target=Vector3.ZERO;face.reset_neutral();manual_blink=-1.0;speech=false;mouse_follow=false;auto_blink=true;external_controls=false
    if data.has("head_tilt"):target.x=clamp(float(data.head_tilt),-1.0,1.0)
    if data.has("head_x"):target.y=clamp(float(data.head_x),-1.0,1.0)
    if data.has("head_y"):target.z=clamp(float(data.head_y),-1.0,1.0)
    var accepted=true
    if data.has("expression"):accepted=face.set_expression(String(data.expression))
    if data.has("mouth"):face.set_mouth(data.mouth)
    if data.has("speech_active") and not data.speech_active:face.release_speech()
    if data.has("blink"):
        manual_blink=float(data.blink);face.set_blink(manual_blink,manual_blink)
    if data.has("auto_blink"):auto_blink=bool(data.auto_blink);manual_blink=-1.0
    return accepted

func _unhandled_key_input(event):
    if not event.is_pressed() or event.echo:return
    if event.keycode in [KEY_M,KEY_A,KEY_D,KEY_LEFT,KEY_RIGHT,KEY_UP,KEY_DOWN,KEY_B,KEY_SPACE]:external_controls=false
    if event.keycode==KEY_M:mouse_follow=not mouse_follow
    if event.keycode==KEY_R:apply_controls({"reset":true})
    if event.keycode==KEY_COMMA or event.keycode==KEY_PERIOD:
        expression_index=posmod(expression_index+(-1 if event.keycode==KEY_COMMA else 1),expression_ids.size())
        face.set_expression(expression_ids[expression_index])

func _process(delta):
    if not rig_ready:return
    clock_time+=delta
    if proof:_run_proof()
    elif not external_controls:
        if mouse_follow:
            var p=(get_global_mouse_position()-Vector2(284,380))/Vector2(284,380)
            apply_controls({"head_x":p.x,"head_y":p.y,"head_tilt":p.x*0.55},"local")
        else:
            apply_controls({"head_tilt":float(Input.is_physical_key_pressed(KEY_D))-float(Input.is_physical_key_pressed(KEY_A)),"head_x":float(Input.is_physical_key_pressed(KEY_RIGHT))-float(Input.is_physical_key_pressed(KEY_LEFT)),"head_y":float(Input.is_physical_key_pressed(KEY_DOWN))-float(Input.is_physical_key_pressed(KEY_UP))},"local")
        speech=Input.is_physical_key_pressed(KEY_SPACE)
        manual_blink=1.0 if Input.is_physical_key_pressed(KEY_B) else -1.0
        hud.text="RYOKO / LIVE MOTION RIG"
        hint.text="A/D tilt · arrows move · M mouse · Space mouth · B blink · R reset"
    current=current.lerp(target,1.0-exp(-delta/0.22))
    skin_material.set_shader_parameter("head_tilt",current.x*deg_to_rad(6.0))
    skin_material.set_shader_parameter("head_offset",Vector2(current.y*16.0,current.z*12.0))
    skin_material.set_shader_parameter("spine_tilt",current.x*deg_to_rad(3.0))
    skin_material.set_shader_parameter("torso_offset",Vector2(current.y*8.0,current.z*5.0))
    skin_material.set_shader_parameter("breath",sin(clock_time*TAU/6.0))
    if auto_blink and clock_time>=next_blink:
        blink_until=clock_time+0.14;next_blink=clock_time+3.2
    var closed=manual_blink if manual_blink>=0.0 else (1.0 if auto_blink and clock_time<blink_until else 0.0)
    face.set_blink(closed,closed)
    if speech:face.set_mouth(["A","E","I","O","U"][int(clock_time*7.0)%5])
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
    var head_weight=1.0-smoothstep(710.0,855.0,rest.y)
    var head=(rest-Vector2(568,790)).rotated(controls.x*deg_to_rad(6.0))+Vector2(568,790)+Vector2(controls.y*16,controls.z*12)
    var neck=rest.lerp(head,head_weight)
    var torso_weight=1.0-smoothstep(1260.0,1384.0,rest.y)
    var torso=(neck-Vector2(568,1340)).rotated(controls.x*deg_to_rad(3.0))+Vector2(568,1340)+Vector2(controls.y*8,controls.z*5)-Vector2(0,breath*1.2)
    return neck.lerp(torso,torso_weight)

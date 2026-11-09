extends SceneTree
var checks=0
var failures=0
func check(ok:bool,label:String):
    checks+=1
    if not ok:failures+=1;push_error(label)
func _initialize():call_deferred("run")
func run():
    var rig=load("res://yawn_rig.tscn").instantiate();root.add_child(rig)
    await process_frame;rig.set_process(false)
    for i in range(1001):
        var value=i/1000.0;rig.face.set_mouth_open(value)
        check(abs(rig.face.oral_objects.cavity.material.get_shader_parameter("opening")-value*0.55)<.000001,"Shader aperture obeys normalized cap")
        check(rig.face.oral_objects.upper_teeth.position==Vector2(533,626),"Upper teeth must remain attached to the fixed upper lip")
        for name in rig.face.oral_objects:
            var n=rig.face.oral_objects[name]
            check(n.scale==Vector2.ONE,"Oral object scale changed")
            check(n.modulate.a==1.0,"Oral object opacity changed")
        check(abs(rig.face.oral_objects.lower_lip.position.y-(620+54*value*rig.face.MAX_MOUTH_APERTURE))<.0001,"Lower lip exceeds reference cap")
    print("TEETH_CHECKS_PASS checks=%d failures=%d"%[checks,failures])
    quit(0 if failures==0 else 1)

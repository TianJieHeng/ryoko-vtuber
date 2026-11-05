extends SceneTree
var checks=0
var failures=0
func verify(value,label):
    checks+=1
    if not value:push_error(label);failures+=1
func _initialize():call_deferred("run")
func run():
    var rig=load("res://motion_rig.tscn").instantiate();root.add_child(rig);await process_frame
    rig.set_process(false)
    rig.apply_controls({"head_tilt":.7,"head_x":.4,"head_y":-.2})
    for i in range(30):
        rig._process(1.0/30)
        verify(rig.current.distance_to(rig.body_current)<.00001,"legacy follow preserved")
    rig.apply_controls({"head_tilt":.7,"body_tilt":0,"body_x":0,"body_y":0})
    for i in range(90):rig._process(1.0/30)
    verify(not rig.body_follow and rig.body_current.length()<.0001,"head only")
    var points=[Vector2(260,920),Vector2(850,920),Vector2(420,1030),Vector2(710,1030),Vector2(568,1200)]
    for head_tilt in [-1.0,0.0,1.0]:
        for body_tilt in [-1.0,-.5,0.0,.5,1.0]:
            for body_x in [-1.0,0.0,1.0]:
                var h=Vector3(head_tilt,.3,.4);var b=Vector3(body_tilt,body_x,.5)
                for point in points:
                    var expected=(point-Vector2(568,1340)).rotated(body_tilt*deg_to_rad(3))+Vector2(568,1340)+Vector2(body_x*8,.5*5)
                    verify(rig.deform_independent(point,h,b,0).distance_to(expected)<.001,"chest shoulder rigid body frame")
                    verify(abs(rig.deform_independent(point,h,b,0).distance_to(rig.deform_independent(points[0],h,b,0))-point.distance_to(points[0]))<.001,"no chest stretch")
                verify(rig.deform_independent(Vector2(568,1384),h,b,0).distance_to(Vector2(568,1384))<.001,"bottom anchored")
    var left=rig.deform_independent(Vector2(400,500),Vector3(-.35,0,0),Vector3(.7,0,0),0)
    var right=rig.deform_independent(Vector2(700,500),Vector3(-.35,0,0),Vector3(.7,0,0),0)
    verify(abs(left.y-right.y)<.001,"counterpose upright head")
    rig.apply_controls({"body_tilt":55,"body_x":-55,"body_y":NAN});verify(rig.body_target==Vector3(1,-1,0),"finite clamp")
    rig._process(.1);verify(rig.body_target==Vector3(1,-1,0),"body API persists")
    rig.apply_controls({"body_follow":true});var prior=rig.body_current;rig._process(.001)
    verify(rig.body_current.distance_to(prior)<.02,"follow switch eases")
    rig.apply_controls({"audio_level":.8,"body_tilt":.4,"head_tilt":-.2});rig._process(.2)
    verify(rig.face.mouth_state=="A" and is_equal_approx(rig.body_target.x,.4),"audio and body coexist")
    rig.apply_controls({"reset":true});verify(rig.body_follow and rig.body_target==Vector3.ZERO,"reset default follow")
    rig.set_process(true)
    var key=InputEventKey.new();key.keycode=KEY_E;key.physical_keycode=KEY_E;key.pressed=true;Input.parse_input_event(key)
    await process_frame;await process_frame
    verify(rig.body_target.x==1.0 and not rig.body_follow,"body keyboard")
    key=InputEventKey.new();key.keycode=KEY_E;key.physical_keycode=KEY_E;key.pressed=false;Input.parse_input_event(key)
    await process_frame;await process_frame
    verify(rig.body_target.x==0.0,"body key release")
    if failures==0:print("INDEPENDENT_BODY_CHECKS_PASS count=",checks)
    quit(1 if failures else 0)

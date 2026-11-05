extends SceneTree
var checks=0
func verify(v,msg):
    checks+=1
    if not v:push_error(msg);quit(1)
func _initialize():call_deferred("run_tests")
func run_tests():
    var rig=load("res://motion_rig.tscn").instantiate();root.add_child(rig);await process_frame
    verify(rig.rig_ready,"ready");verify(rig.expression_ids.size()==93,"profiles")
    for tilt in [-1.0,-0.5,0.0,0.5,1.0]:
        for hx in [-1.0,0.0,1.0]:
            for hy in [-1.0,0.0,1.0]:
                for breath in [-1.0,0.0,1.0]:
                    var controls=Vector3(tilt,hx,hy)
                    # These landmarks encompass both shoulders and the chest.
                    var points=[Vector2(260,920),Vector2(850,920),Vector2(420,1030),Vector2(710,1030),Vector2(568,1200)]
                    for p in points:
                        var expected=(p-Vector2(568,1340)).rotated(tilt*deg_to_rad(3))+Vector2(568,1340)+Vector2(hx*8,hy*5)-Vector2(0,breath*1.2)
                        verify(rig.deform_point(p,controls,breath).distance_to(expected)<0.001,"shoulder/chest identical rigid frame")
                    for p in points:
                        verify(abs(rig.deform_point(p,controls,breath).distance_to(rig.deform_point(points[0],controls,breath))-p.distance_to(points[0]))<0.001,"no chest/shoulder stretching")
                    for x in [0.0,568.0,1136.0]:verify(rig.deform_point(Vector2(x,1384),controls,breath).distance_to(Vector2(x,1384))<0.001,"lower edge anchor")
    # Exponential response is monotonic and cannot overshoot a held target.
    for goal in [-1.0,-0.5,0.5,1.0]:
        var value=0.0
        for frame in range(180):
            var next=lerpf(value,goal,1-exp(-(1.0/30.0)/0.22))
            verify(abs(goal-next)<=abs(goal-value)+0.000001,"settle monotonic")
            verify(next>=min(0.0,goal)-0.000001 and next<=max(0.0,goal)+0.000001,"no overshoot")
            value=next
    rig.apply_controls({"head_tilt":99,"head_x":-99,"head_y":99});verify(rig.target==Vector3(1,-1,1),"clamp")
    await process_frame;await process_frame;verify(rig.target==Vector3(1,-1,1),"API persists")
    rig.apply_controls({"expression":"EXP-004","mouth":"O","head_tilt":0.3})
    verify(rig.face.expression=="EXP-004" and rig.face.mouths.O.visible and is_equal_approx(rig.target.x,0.3),"combined command")
    rig.apply_controls({"blink":1});await process_frame;verify(rig.face.blink_left and rig.face.blink_right,"blink")
    rig.apply_controls({"reset":true});verify(rig.target==Vector3.ZERO and rig.face.expression=="neutral","smooth reset target")
    var key=InputEventKey.new();key.keycode=KEY_D;key.physical_keycode=KEY_D;key.pressed=true;Input.parse_input_event(key)
    await process_frame;await process_frame;verify(rig.target.x==1.0,"physical key drives rig")
    key=InputEventKey.new();key.keycode=KEY_D;key.physical_keycode=KEY_D;key.pressed=false;Input.parse_input_event(key)
    await process_frame;await process_frame;verify(rig.target.x==0.0,"release target returns")
    print("COUPLED_MOTION_RIG_CHECKS_PASS count=",checks);quit()

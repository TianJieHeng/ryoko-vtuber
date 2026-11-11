extends SceneTree
var checks = 0
var failures = []
var rig
func _initialize():call_deferred("run")
func check(ok,label):
    checks += 1
    if not ok:failures.append(label)
func run():
    rig = load("res://full_body/full_body_rig.tscn").instantiate();root.add_child(rig)
    rig.expression_rig.set_process(false)
    check(rig.ready_for_controls,"assembly readiness")
    if not rig.ready_for_controls:print(rig.last_error);quit(1);return
    check(rig.list_expressions().size() == 47,"all 47 approved profiles retained")
    check(rig.joints.size() == 17,"17 named anatomical joints")
    check(rig.layer_nodes.size() == 17,"17 registered body layers")
    check(not rig.expression_rig.body.visible,"legacy bust duplicate hidden")
    check(rig.expression_rig.head.get_parent() == rig.joints.head,"existing head attached to head bone")
    check(rig.expression_rig.face.objects.stationary_backing.visible,"approved face skin retained")
    var neutral = rig.get_body_state()
    var face_neutral = rig.expression_rig.face.snapshot()
    for control in rig.body_controls:
        for value in [-1.0,1.0]:
            rig.reset()
            check(rig.apply_body_controls({control:value}),control+" endpoint accepted")
            if rig.body_control_joints.has(control):
                var spec = rig.body_control_joints[control]
                var expected:float = spec.range_degrees[0] if value < 0 else spec.range_degrees[1]
                check(abs(rad_to_deg(rig.joints[spec.id].rotation)-expected)<0.0001,control+" exact degree mapping")
            for node in rig.joints.values():check(node.scale.is_equal_approx(Vector2.ONE),control+" unit bone scale")
            check(rig.expression_rig.face.snapshot() == face_neutral,control+" no facial mutation")
            rig.reset();check(rig.get_body_state().joints == neutral.joints,control+" exact skeleton reset")
    rig.apply_body_controls({"head_tilt":.6,"chest_tilt":.4})
    var before = rig.get_body_state().controls
    for invalid in [{"head_tilt":2},{"head_tilt":true},{"head_tilt":"1"},{"head_tilt":NAN},{"head_tilt":INF},{"unknown":0},{"reset":true,"head_tilt":2},{"frame_x":.5,"head_tilt":2}]:
        check(not rig.apply_body_controls(invalid),"invalid transaction rejected "+str(invalid))
        check(rig.get_body_state().controls == before,"no partial bone mutation")
    check(not rig.apply_body_controls([]),"non-dictionary rejected")
    check(rig.apply_controls({"blink_L":.7,"gaze_x":.5,"mouth_open":.3}),"live facial controls accepted while posed")
    check(abs(rig.expression_rig.pose_now().blink_L - .7) < .00001,"same eyelid control")
    check(rig.expression_rig.pose_now().gaze_x == .5,"same gaze control")
    check(rig.get_body_state().controls == before,"face controls preserve body pose")
    for item in rig.list_expressions():
        check(rig.play_expression(item.id),item.id+" starts on full body")
        check(rig.expression_rig.advance(.1),item.id+" advances on full body")
        check(rig.get_body_state().controls == before,item.id+" does not steal body ownership")
    rig.reset()
    check(rig.get_body_state().joints == neutral.joints,"global reset restores skeleton")
    check(rig.expression_rig.face.snapshot() == face_neutral,"global reset restores approved face")
    var result = {"status":"PASS" if failures.is_empty() else "FAIL","checks":checks,"failures":failures,"scope":"Actual Godot headless node transforms, control rejection, reset and existing facial player. Does not establish rendered seam quality or native pixel parity."}
    var file = FileAccess.open("res://full_body/review/headless_checks.json",FileAccess.WRITE)
    file.store_string(JSON.stringify(result,"  "));file.close();print(JSON.stringify(result));quit(0 if failures.is_empty() else 1)

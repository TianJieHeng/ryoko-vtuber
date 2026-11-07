extends SceneTree
const Limits=preload("res://control_limits.gd")
const IDS=["EXP-163","EXP-005","EXP-001","EXP-006","EXP-107","EXP-007","EXP-002","EXP-160"]
var rig
var checks=0
var failures=[]
func _initialize():call_deferred("run")
func check(ok,label):
    checks+=1
    if not ok:
        failures.append(label)
        if failures.size()<20:push_error(label)
func state():
    var s=rig.get_state();s.erase("last_error");s.face=rig.face.snapshot();s.elapsed=rig.elapsed;return s
func offset(x,y,e):return Vector2(x*4,y*(2 if y<0 else 1)+e*Limits.GAZE_DOWN_EXTRA_PIXELS)
func verify(x,y,e):
    var expected=offset(x,y,e)
    check(Limits.gaze_pixels(Vector2(x,y),e).is_equal_approx(expected),"physical additive calibration")
    check(expected.x>=-4 and expected.x<=4 and expected.y>=-2 and expected.y<=6,"combined domain bounded")
    var p=rig.pose_now();check(is_equal_approx(p.gaze_down_extra,e),"state extra")
    check(is_equal_approx(rig.displayed_pose().gaze_down_extra,e),"display extra")
    check(is_equal_approx(rig.face.gaze_down_extra,e),"face extra")
    for side in ["screen_left","screen_right"]:
        var key="iris_"+side
        check(rig.face.homes[key].node.position.is_equal_approx(rig.face.homes[key].pivot+expected),"rigid iris sum "+side)
        check(rig.face.objects[key].material.get_shader_parameter("rigid_gaze").is_equal_approx(expected),"shader sum "+side)
        check(rig.face.homes["sclera_"+side].node.position==rig.face.homes["sclera_"+side].pivot,"stationary sclera")
    for key in rig.face.objects:
        var s=rig.face.objects[key];var n=rig.face.homes[key].node
        check(s.scale==Vector2.ONE and n.scale==Vector2.ONE,"unit feature scale")
        check(s.modulate.a==1 and n.modulate.a==1,"fixed anatomical opacity")
    check(rig.face.oral_objects.upper_teeth.position==Vector2(533,626),"white upper enamel fixed")
func run():
    rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
    check(rig.rig_ready and rig.registry_ready,"ready");check(rig.list_expressions().size()==11,"ten approved profiles plus scoped164")
    check(rig.pose_now().gaze_down_extra==0,"new default zero")
    check(Limits.GAZE_DOWN_PIXELS==1 and Limits.GAZE_DOWN_EXTRA_PIXELS==5,"old mapping1 and selected extra5")
    for id in ["EXP-003","EXP-161","EXP-153"]:check(rig.registry.definition(id).is_empty(),"unapproved profile absent")
    for i in range(1001):
        var t=float(i)/1000;var x=sin(t*TAU*3);var y=cos(t*TAU*2);var e=sin(t*PI)
        check(rig.apply_controls({"gaze_x":x,"gaze_y":y,"gaze_down_extra":e,"blink_R":t,"blink_L":1-t,"hair_sway":.07*sin(t*TAU)}),"fractional controls")
        verify(x,y,e)
    for x in [-1.,0.,1.]:
        for y in [-1.,0.,1.]:
            for e in [0.,.5,1.]:
                for lid in [0.,.4,1.]:
                    rig.apply_controls({"gaze_x":x,"gaze_y":y,"gaze_down_extra":e,"blink":lid});verify(x,y,e)
    for id in IDS:
        var d=rig.registry.definition(id)
        for k in d.keyframes:
            check(not k.values.has("gaze_down_extra"),"existing profile not rewritten")
            check(rig.sample_expression(id,k.time).gaze_down_extra==0,"missing timeline channel defaults zero")
        for ending in ["finish","release","repeat_release","retrigger","reset","manual"]:
            rig.reset();rig.apply_controls({"gaze_x":-.7,"gaze_y":1.0,"gaze_down_extra":1.0,"auto_blink":true})
            var before=rig.displayed_pose();check(rig.play_expression(id),"trigger accepted");check(rig.displayed_pose()==before,"trigger continuous from extra")
            rig.advance(.1);check(rig.pose_now().gaze_down_extra>0 and rig.pose_now().gaze_down_extra<1,"shared restart interpolates extra")
            if ending=="retrigger":
                before=rig.displayed_pose();rig.play_expression("EXP-005");check(rig.displayed_pose()==before,"retrigger C0")
                rig.advance(10)
            elif ending in ["release","repeat_release"]:
                before=rig.displayed_pose();rig.release();check(rig.displayed_pose()==before,"release C0 extra");rig.advance(.1)
                if ending=="repeat_release":
                    before=rig.displayed_pose();rig.release();check(rig.displayed_pose()==before,"repeat release C0")
                rig.advance(.5)
            elif ending=="reset":rig.reset()
            elif ending=="manual":
                rig.apply_controls({"gaze_down_extra":.4});check(rig.active_performance=="" and rig.release_time<0 and not rig.auto_blink_pending_restore,"manual extra owns takeover")
                rig.advance(10);check(is_equal_approx(rig.pose_now().gaze_down_extra,.4),"manual extra persists");rig.reset()
            else:rig.advance(10)
            check(rig.pose_now()==rig.neutral_pose(),"exact neutral all channels")
            check(rig.face.gaze_down_extra==0,"no stale cap extension")
            check(rig.auto_blink==(ending not in ["reset","manual"]),"auto blink existing restoration policy")
    for mode in ["manual","performance","release"]:
        rig.reset();rig.apply_controls({"gaze_down_extra":.6,"auto_blink":true})
        if mode!="manual":rig.play_expression("EXP-007");rig.advance(.1)
        if mode=="release":rig.release();rig.advance(.1)
        var before=state()
        for bad in [-.000001,1.000001,NAN,INF,-INF,"0.5",null,true,[],{}]:
            check(not rig.apply_controls({"reset":true,"gaze_down_extra":bad,"mouth_open":.3}),"invalid extra rejected")
            check(state()==before,"invalid extra atomic in "+mode)
        for data in [{"gaze_down_extra":.2,"unknown":1},{"gaze_down_extra":.2,"mouth_open":2},{"perform_expression":"EXP-005","gaze_down_extra":.2}]:
            check(not rig.apply_controls(data),"invalid mixed transaction rejected");check(state()==before,"mixed rejection atomic")
        for data in [{},{"reset":false},{"release_performance":false}]:
            check(rig.apply_controls(data),"old no-op accepted");check(state()==before,"old no-op preserves extra")
    var viewer=load("res://expression_viewer.tscn").instantiate();root.add_child(viewer);viewer.set_process(false);viewer.rig.set_process(false)
    check(viewer.sliders.has("gaze_down_extra"),"UI bounded extra slider")
    viewer.sliders.gaze_down_extra.value=.75;check(is_equal_approx(viewer.rig.pose_now().gaze_down_extra,.75),"actual slider signal")
    viewer.rig.reset();viewer._process(0);check(viewer.sliders.gaze_down_extra.value==0,"slider neutral sync")
    var bridge=viewer.control_bridge;bridge.rig=viewer.rig;var cap=bridge.capabilities()
    check(cap.controls.gaze_down_extra==[0.,1.],"adapter schema")
    check(cap.gaze.down_extension.combined_y_range==[-2.,6.] and cap.gaze.down_extension.default==0,"advertised physical range")
    bridge.session=1;bridge.external_enabled=true;bridge.discovered=true
    bridge.dispatch(JSON.stringify({"protocol":1,"id":1,"session":1,"verb":"apply_controls","args":{"gaze_y":1,"gaze_down_extra":1}}).to_utf8_buffer())
    var response=JSON.parse_string(bridge.outgoing.get_string_from_utf8());bridge.outgoing.clear()
    check(response.ok and response.result.rig.controls.gaze_down_extra==1,"preparation-only dispatch")
    check(not bridge.enabled and not bridge.server.is_listening(),"no socket opened")
    print("DOWN_EXTRA_RUNTIME_", "PASS" if failures.is_empty() else "FAIL"," checks=",checks," failures=",failures.size())
    quit(0 if failures.is_empty() else 1)

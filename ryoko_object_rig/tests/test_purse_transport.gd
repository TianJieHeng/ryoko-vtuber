extends SceneTree
## Shared-coordinate transport only. Geometry and source ownership have separate tests.
const AXIS="mouth_purse"
const PRIOR_IDS=["EXP-163","EXP-005","EXP-001","EXP-006","EXP-107"]
var rig
var checks=0
var failures=[]
func _initialize():call_deferred("run")
func check(ok:bool,label:String):
    checks+=1
    if not ok:
        if failures.size()<20:push_error("PURSE_TRANSPORT "+label)
        failures.append(label)
func state()->Dictionary:
    var s=rig.get_state();s.erase("last_error")
    s.current=rig.current_pose.duplicate(true)
    s.restart=rig.restart_pose.duplicate(true)
    s.release=rig.release_pose.duplicate(true)
    s.performance=rig.performance.duplicate(true)
    s.elapsed=rig.elapsed
    s.oral_mode=rig.oral_mode
    s.manual_mouth_purse=rig.manual_mouth_purse
    return s
func coordinate(value:float,label:String):
    var s=rig.get_state()
    check(rig.pose_now()[AXIS]==value and rig.displayed_pose()[AXIS]==value,label+" pose/display")
    check(s.controls[AXIS]==value and s.displayed_controls[AXIS]==value,label+" public state")
    check(rig.current_pose[AXIS]==value and rig.manual_mouth_purse==value,label+" current/manual")
    check(rig.face.mouth_purse==value,label+" face parameter")
func run():
    rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
    check(rig.rig_ready and rig.registry_ready,"rig ready")
    if not rig.rig_ready or not rig.registry_ready:quit(2);return
    check(rig.neutral_pose()[AXIS]==0.0,"neutral contains zero coordinate")
    coordinate(0.0,"initial default")
    check(rig.Registry.CHANNEL_BOUNDS[AXIS]==[0.0,1.0],"registry bounds")
    var bridge=load("res://control_bridge.gd").new();bridge.rig=rig
    var caps=bridge.capabilities();bridge.free()
    check(caps.controls[AXIS]==[0.0,1.0],"bridge bounds")
    check(caps.lip_purse=={"control":AXIS,"default":0.0,"scope":"bounded shared control"},"bridge generic coordinate only")
    check(not caps.ai_model_connected and not caps.tts_connected,"preparation-only integration")
    check(rig.registry.resolve("relief")=="EXP-007" and rig.registry.resolve("relieved-smile")=="EXP-007","authored relief aliases")
    check(rig.list_expressions().size()==6 and rig.registry.resolve("EXP-003")=="","only six authored profiles")

    for value in [0.0,.000001,.25,.5,.75,.999999,1.0,0.0]:
        check(rig.apply_controls({AXIS:value}),"valid bounded coordinate")
        coordinate(value,"manual value")
    # An omitted coordinate in older data is an exact zero, never inherited.
    for id in PRIOR_IDS:
        var definition=rig.registry.definition(id)
        for frame in definition.keyframes:check(not frame.values.has(AXIS),"prior authored data has no purse "+id)
        for hz in [30,60]:
            rig.reset();rig.play_expression(id)
            for i in range(int(ceil(definition.duration*hz))+1):
                var t=minf(float(i)/hz,definition.duration)
                check(rig.sample_expression(id,t)[AXIS]==0.0,"prior sample defaults zero "+id)
                coordinate(0.0,"prior playback "+id)
                rig.advance(1.0/hz)
    var omitted=rig.neutral_pose();omitted.erase(AXIS)
    rig.apply_controls({AXIS:.9});rig._apply_performance_pose(omitted)
    coordinate(0.0,"omitted applied pose defaults zero")
    rig.reset()

    # Reject the whole transaction before any ownership, clock or state changes.
    for mode in ["neutral","manual","active","release"]:
        rig.reset()
        if mode!="neutral":rig.apply_controls({AXIS:.73,"mouth_open":.2})
        if mode in ["active","release"]:rig.play_expression("EXP-007");rig.advance(.1)
        if mode=="release":rig.release();rig.advance(.07)
        for invalid in [-.000001,1.000001,NAN,INF,-INF,true,false,"1",null,{},[]]:
            var before=state()
            check(not rig.apply_controls({"reset":true,"mouth_open":.7,AXIS:invalid}),"invalid coordinate rejected in "+mode)
            check(state()==before,"invalid coordinate atomic in "+mode)
        for bad in [{AXIS:.6,"blink":true},{AXIS:.6,"unknown":0},{AXIS:.6,"perform_expression":"EXP-007"},{AXIS:.6,"release_performance":true}]:
            var before=state()
            check(not rig.apply_controls(bad),"mixed invalid transaction rejected")
            check(state()==before,"mixed invalid transaction atomic")
        for noop in [{},{"reset":false},{"release_performance":false}]:
            var before=state()
            check(rig.apply_controls(noop),"no-op accepted")
            check(state()==before,"no-op retains coordinate and ownership")

    # Trigger, interruption, retrigger, handover, manual takeover and return use
    # the same coordinate as all other channels, never expression-specific code.
    for entry in rig.list_expressions():
        rig.reset();rig.apply_controls({AXIS:.82,"mouth_open":.3})
        var before=rig.displayed_pose()
        check(rig.play_expression(entry.id),"trigger "+entry.id)
        check(rig.displayed_pose()==before and rig.restart_pose[AXIS]==.82,"trigger C0 and restart coordinate")
        rig.advance(.1);before=rig.displayed_pose()
        rig.play_expression(entry.id)
        check(rig.displayed_pose()==before,"retrigger C0")
        rig.advance(.05);before=rig.displayed_pose()
        rig.release()
        check(rig.displayed_pose()==before and rig.release_pose[AXIS]==before[AXIS],"release C0 and saved coordinate")
        rig.advance(.1);before=rig.displayed_pose()
        rig.play_expression(entry.id)
        check(rig.displayed_pose()==before,"interrupted release C0")
        rig.advance(.05)
        for destination in rig.list_expressions():
            before=rig.displayed_pose();rig.play_expression(destination.id)
            check(rig.displayed_pose()==before,"cross-expression C0")
            rig.advance(.02)
        rig.apply_controls({AXIS:.35})
        check(rig.active_performance=="" and rig.release_time<0 and rig.face.owners.mouth=="manual","manual purse owns pose")
        rig.advance(.7);coordinate(.35,"manual persists without stale resume")
        rig.release();rig.advance(rig.RELEASE_SECONDS)
        coordinate(0.0,"release exact zero")
        check(rig.displayed_pose()==rig.neutral_pose(),"release exact neutral")
        rig.apply_controls({AXIS:1.0});rig.play_expression(entry.id);rig.advance(entry.duration)
        coordinate(0.0,"completion exact zero")
        check(rig.displayed_pose()==rig.neutral_pose(),"completion exact neutral")
        rig.apply_controls({AXIS:.67});rig.reset();coordinate(0.0,"reset exact zero")
        check(rig.restart_pose.is_empty() and rig.release_pose.is_empty() and rig.performance.is_empty(),"reset clears saved lifecycle")

    # Test-only in-memory profile; never added to the shipping catalogue.
    var fixture={"id":"TEST-PURSE","title":"Transport fixture","duration":1.0,"keyframes":[{"time":0.0,"phase":"neutral","values":{}},{"time":.5,"phase":"purse","values":{AXIS:1.0}},{"time":1.0,"phase":"neutral","values":{}}]}
    check(rig.registry.validate_definition(fixture,fixture.id),"timeline accepts coordinate")
    check(rig._sample(fixture,.25)[AXIS]==.5 and rig._sample(fixture,.5)[AXIS]==1.0,"shared smooth interpolation")
    check(rig._sample(fixture,0)[AXIS]==0.0 and rig._sample(fixture,1)[AXIS]==0.0,"timeline endpoints exact zero")
    var isolated=rig.Registry.new()
    var catalogue={"schema_version":1,"entries":[{"id":fixture.id,"path":"res://test-only-purse.json"}]}
    check(isolated.load_catalogue(catalogue,{"res://test-only-purse.json":fixture}),"isolated profile accepted")
    var held=isolated.definition(fixture.id)
    for invalid in [-.000001,1.000001,NAN,INF,-INF,true,false,"1",null,{},[]]:
        var bad=fixture.duplicate(true);bad.keyframes[1].values[AXIS]=invalid
        check(not isolated.load_catalogue(catalogue,{"res://test-only-purse.json":bad}),"invalid timeline rejected")
        check(isolated.definition(fixture.id)==held,"registry failure atomic")
    check(rig.registry.resolve(fixture.id)=="" and rig.list_expressions().size()==6,"fixture remains unregistered")

    # Exercise the actual UI signal and display synchronization, without a socket.
    var viewer=load("res://expression_viewer.tscn").instantiate();root.add_child(viewer)
    viewer.set_process(false);viewer.rig.set_process(false)
    check(viewer.sliders.has(AXIS),"viewer slider present")
    var slider=viewer.sliders[AXIS]
    check(slider.min_value==0.0 and slider.max_value==1.0,"viewer slider bounds")
    viewer.rig.play_expression("EXP-007");viewer.rig.advance(.6)
    slider.value=.321
    check(is_equal_approx(viewer.rig.pose_now()[AXIS],.321) and viewer.rig.active_performance=="","slider manual takeover")
    check(not viewer.control_bridge.external_enabled,"slider does not enable external control")
    viewer.rig.apply_controls({AXIS:.654});viewer._process(0)
    check(is_equal_approx(slider.value,.654),"viewer reflects displayed coordinate")
    viewer.apply_controls({"reset":true});viewer._process(0)
    check(slider.value==0.0,"viewer reset synchronized")
    viewer.free()
    print("PURSE_TRANSPORT checks=",checks," failures=",failures.size())
    quit(1 if failures.size() else 0)

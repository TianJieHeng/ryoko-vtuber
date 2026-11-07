extends SceneTree
## Seven-profile lifecycle coverage including the selected EXP-002 brief closure.
## Deterministic shared-controller and UI/adapter tests; no listening socket.
var rig
var checks=0
var failures=[]
const IDS=["EXP-163","EXP-005","EXP-001","EXP-006","EXP-107","EXP-007","EXP-002"]
func _initialize():call_deferred("run")
func check(ok,label):
    checks+=1
    if not ok:
        failures.append(label)
        if failures.size()<30:push_error(label)
func state():
    var s=rig.get_state();s.erase("last_error");s.elapsed=rig.elapsed;s.face=rig.face.snapshot()
    return s
func pending(wanted,label):
    check(not rig.auto_blink and rig.auto_blink_pending_restore==wanted,label+" actual suspended and intent preserved")
    var s=rig.get_state()
    check(s.auto_blink==rig.auto_blink and s.auto_blink_pending_restore==wanted,label+" honest state")
func neutral(wanted,label):
    check(rig.active_performance=="" and rig.release_time<0,label+" neutral ownership")
    check(rig.pose_now()==rig.neutral_pose() and rig.displayed_pose()==rig.neutral_pose(),label+" exact open neutral")
    check(rig.auto_blink==wanted and not rig.auto_blink_pending_restore,label+" restoration consumed once")
    for joint in rig.face.smile_eye_joints:check(not rig.face.objects[joint.key].visible,label+" no smiling lash owner")
    check(rig.face.oral_objects.upper_teeth.position==Vector2(533,626),label+" fixed white enamel")
func begin(id,wanted):
    rig.reset();rig.apply_controls({"auto_blink":wanted});rig.advance(4.03)
    var before=rig.displayed_pose()
    check(rig.play_expression(id),"play "+id)
    check(rig.displayed_pose()==before,"trigger C0 "+id)
    pending(wanted,id)
func blink_cycle(wanted,label):
    # The restored clock starts at 0; these are the unchanged base timing points.
    if wanted:check(rig.elapsed==0.0,label+" open-phase clock restart")
    rig.advance(3.86);check(rig.face.closure==Vector2.ZERO,label+" existing open interval")
    rig.advance(.085);check(is_equal_approx(rig.face.closure.x,sin(PI*.25) if wanted else 0.0),label+" closing")
    rig.advance(.085);check(is_equal_approx(rig.face.closure.x,1.0 if wanted else 0.0),label+" fully closed")
    rig.advance(.085);check(is_equal_approx(rig.face.closure.x,sin(PI*.75) if wanted else 0.0),label+" reopening")
    rig.advance(.085);check(rig.face.closure.length()<.000001,label+" fully reopened")
    for joint in rig.face.smile_eye_joints:check(not rig.face.objects[joint.key].visible,label+" no retained laughter family")
func affection_peak(label):
    var pose=rig.pose_now()
    check(is_equal_approx(pose.eye_smile_R,.90) and is_equal_approx(pose.eye_smile_L,.90),label+" authored upward hold")
    check(rig.face.smile_eyes.is_equal_approx(Vector2(.90,.90)),label+" actual smiling-eye controls")
    check(pose.mouth_open==0.0 and pose.gaze_x==0.0 and pose.gaze_y==0.0 and pose.hair_sway==0.0,label+" sealed/still approved acting")
    var visible_joints=0
    for joint in rig.face.smile_eye_joints:
        if rig.face.objects[joint.key].visible:visible_joints+=1
    check(visible_joints>0,label+" smiling contour actually selected before recovery")
func ordinary_family(label):
    check(rig.face.smile_eyes==Vector2.ZERO,label+" actual zero smile family")
    for joint in rig.face.smile_eye_joints:check(not rig.face.objects[joint.key].visible,label+" no retained affection/laughter contour")
    for key in rig.face.manifest.objects:
        var part=rig.face.manifest.objects[key]
        if part.has("eye_role") and int(part.eye_role)==4:
            check(rig.face.objects[key].visible,label+" ordinary closed-lid owner restored")
func run_affection_edges():
    check(rig.registry.resolve("EXP-002")=="EXP-002" and rig.list_expressions().size()==7,"seven authored profiles including affection")
    check(rig.registry.definition("EXP-002").duration==1.9,"affection duration unchanged")
    var sample=rig.sample_expression("EXP-002",.50)
    check(is_equal_approx(sample.eye_smile_R,.015) and is_equal_approx(sample.eye_smile_L,.015),"affection selected OPEN KP4 preserved")
    for wanted in [false,true]:
        for ending in ["complete","release","retrigger","to_laughter","from_laughter"]:
            begin("EXP-002",wanted);rig.advance(.75);affection_peak("EXP002 before "+ending)
            pending(wanted,"EXP002 selected hold")
            if ending=="complete":
                rig.advance(.30);check(is_equal_approx(rig.pose_now().eye_smile_R,.010),"EXP002 renews open contact at1.05");check(is_equal_approx(rig.pose_now().mouth_smile,.24),"EXP002 retains smile after closure")
                rig.advance(1.9)
            elif ending=="release":
                var before=rig.displayed_pose();rig.release();check(before==rig.displayed_pose(),"EXP002 hold release C0")
                rig.advance(.449999);pending(wanted,"EXP002 recovery not complete")
                rig.advance(.0000011)
            elif ending=="retrigger":
                var before=rig.displayed_pose();rig.play_expression("EXP-002");check(before==rig.displayed_pose(),"EXP002 hold retrigger C0")
                pending(wanted,"EXP002 retrigger retains intent");rig.advance(.75);affection_peak("EXP002 retriggered hold");rig.advance(1.9)
            elif ending=="to_laughter":
                var before=rig.displayed_pose();rig.play_expression("EXP-005");check(before==rig.displayed_pose(),"EXP002 to laughter C0")
                pending(wanted,"EXP002 to laughter intent");rig.advance(.9);rig.release();rig.advance(.45)
            else:
                begin("EXP-005",wanted);rig.advance(.9)
                var before=rig.displayed_pose();rig.play_expression("EXP-002");check(before==rig.displayed_pose(),"laughter to EXP002 C0")
                pending(wanted,"laughter to EXP002 intent");rig.advance(.75);affection_peak("EXP002 incoming from laughter");rig.advance(1.9)
            neutral(wanted,"EXP002 "+ending);ordinary_family("EXP002 "+ending)
            blink_cycle(wanted,"EXP002 "+ending+" restored ordinary idle")
            ordinary_family("EXP002 after full close/reopen")
    for mode in ["performance","release"]:
        for command in [{"auto_blink":false},{"reset":true},{"mouth_open":.13}]:
            begin("EXP-002",true);rig.advance(.75);affection_peak("EXP002 cancellation before "+mode)
            if mode=="release":rig.release();rig.advance(.1)
            check(not rig.auto_blink and rig.auto_blink_pending_restore,"EXP002 actual already false with pending intent")
            check(rig.apply_controls(command),"EXP002 explicit cancellation accepted")
            check(not rig.auto_blink and not rig.auto_blink_pending_restore and rig.active_performance=="" and rig.release_time<0,"EXP002 cancellation immediately owns pose")
            var pose=rig.pose_now();var displayed=rig.displayed_pose();rig.advance(20)
            check(rig.pose_now()==pose and rig.displayed_pose()==displayed and not rig.auto_blink,"EXP002 no delayed restoration after cancel")
            rig.play_expression("EXP-002");rig.advance(1.9);neutral(false,"EXP002 later trigger cannot resurrect canceled preference")
    var ui=load("res://expression_viewer.tscn").instantiate();root.add_child(ui);ui.set_process(false);ui.rig.set_process(false)
    var index=ui.expression_ids.find("EXP-002")
    check(index>=0,"EXP002 selectable in shared viewer")
    if index>=0:
        ui.selector.select(index)
        for mode in ["performance","release"]:
            ui.apply_controls({"reset":true,"auto_blink":true});check(ui.play_selected(),"UI selects EXP002")
            check(ui.rig.active_performance=="EXP-002","UI actual selected ID")
            ui.rig.advance(.9)
            if mode=="release":ui.apply_controls({"release_performance":true});ui.rig.advance(.1)
            ui._process(0)
            check(ui.auto_blink_button.button_pressed and not ui.rig.auto_blink and ui.rig.auto_blink_pending_restore,"EXP002 UI saved preference differs honestly from actual")
            check("paused" in ui.auto_blink_status.text and "neutral recovery" in ui.auto_blink_status.text,"EXP002 UI explains pending recovery")
            ui.auto_blink_button.button_pressed=false;ui._process(0)
            check(not ui.rig.auto_blink_pending_restore and not ui.rig.auto_blink and ui.rig.active_performance=="" and ui.rig.release_time<0,"EXP002 UI false-to-false manual cancellation")
            check("off" in ui.auto_blink_status.text,"EXP002 UI cancellation status")
            var pose=ui.rig.pose_now();ui.rig.advance(10)
            check(ui.rig.pose_now()==pose and not ui.rig.auto_blink,"EXP002 UI canceled recovery stays canceled")
        ui.apply_controls({"reset":true,"auto_blink":true});ui.play_selected();ui.rig.advance(1.9);ui._process(0)
        check(ui.rig.auto_blink and not ui.rig.auto_blink_pending_restore and "active" in ui.auto_blink_status.text,"EXP002 UI completed recovery reports actual active")
    ui.free()
func run():
    rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
    check(rig.rig_ready and rig.registry_ready,"ready")
    if not rig.rig_ready or not rig.registry_ready:quit(2);return
    neutral(false,"default remains disabled")
    run_affection_edges()
    for wanted in [false,true]:
        for id in IDS:
            for ending in ["completion","release","repeated_release","zero_delta"]:
                begin(id,wanted)
                var duration=rig.registry.definition(id).duration
                if ending=="completion":
                    rig.advance(duration-.000001);pending(wanted,id+" before completion")
                    rig.advance(.0000011)
                elif ending=="zero_delta":
                    var before=rig.displayed_pose();rig.advance(0.0)
                    check(rig.displayed_pose()==before and rig.performance_time==0.0 and rig.active_performance==id,"zero delta keeps pose, clock and owner")
                    pending(wanted,"zero delta keeps restore intent")
                    rig.play_expression(id);pending(wanted,"zero-duration retrigger")
                    rig.release();rig.release();rig.advance(0.0);pending(wanted,"zero-duration releases")
                    check(rig.release_time==0,"zero elapsed remains release");rig.advance(.45)
                else:
                    rig.advance(.6);var before=rig.displayed_pose();rig.release()
                    check(rig.displayed_pose()==before,"release C0");pending(wanted,"release")
                    check(rig.active_performance=="" and rig.release_time==0,"empty active_expression is not recovery completion")
                    rig.advance(.2);pending(wanted,"partial recovery")
                    if ending=="repeated_release":
                        before=rig.displayed_pose();rig.release();check(before==rig.displayed_pose(),"repeat release C0")
                        rig.advance(.449999);pending(wanted,"repeat release not prematurely restored");rig.advance(.0000011)
                    else:rig.advance(.25)
                neutral(wanted,id+" "+ending);blink_cycle(wanted,id+" "+ending)
            # All cross-profile handoffs and a retrigger inside interrupted release.
            for target in IDS:
                begin(id,wanted);rig.advance(.6);rig.release();rig.advance(.2)
                var before=rig.displayed_pose();rig.play_expression(target)
                check(rig.displayed_pose()==before,"cross-profile release handoff C0")
                pending(wanted,"cross-profile saved intent")
                rig.advance(.15);rig.play_expression(target);pending(wanted,"retrigger saved intent")
                rig.advance(rig.registry.definition(target).duration);neutral(wanted,"cross-profile finish")
    for mode in ["performance","release"]:
        for command in [{"auto_blink":false},{"reset":true},{"mouth_open":.2},{"blink":.4},{"auto_blink":true},{"reset":true,"auto_blink":true},{"reset":false,"mouth_open":.1}]:
            begin("EXP-005",true);rig.advance(.6)
            if mode=="release":rig.release();rig.advance(.1)
            check(rig.apply_controls(command),"manual command accepted")
            check(rig.active_performance=="" and rig.release_time<0 and not rig.auto_blink_pending_restore,"manual cancels pending even for false-to-false")
            var expected=command.get("auto_blink",false)
            check(rig.auto_blink==expected,"manual actual setting")
            var pose=rig.pose_now();rig.advance(20)
            check(rig.pose_now()==pose and rig.auto_blink==expected and not rig.auto_blink_pending_restore,"no stale deferred restoration")
            # New performance must capture the latest setting, not old deferred intent.
            rig.play_expression("EXP-007");rig.advance(3.2);neutral(expected,"latest preference after manual action")
        begin("EXP-005",true);rig.advance(.7)
        if mode=="release":rig.release();rig.advance(.1)
        var before=state()
        for command in [{},{"reset":false},{"release_performance":false}]:
            check(rig.apply_controls(command),"genuine no-op");check(state()==before,"no-op preserves pending")
        for command in [{"auto_blink":false,"mouth_open":2},{"auto_blink":1},{"perform_expression":"absent"},{"reset":true,"unknown":1}]:
            check(not rig.apply_controls(command),"invalid rejected");check(state()==before,"invalid atomic including pending")
        for delta in [-1,NAN,INF]:
            check(not rig.advance(delta),"invalid advance rejected");check(state()==before,"invalid time preserves pending")
        rig.sample_expression("EXP-005",1);rig.get_state();rig.list_expressions();rig.auto_blink_policy()
        check(state()==before,"read-only calls preserve intent")
        # No timer can finish a paused rig. Engine frames do not advance set_process(false).
        for i in range(3):await process_frame
        check(state()==before,"paused processing cannot resurrect blink")
        rig.advance(20);neutral(true,"explicit deterministic resume")
    # Release directly from idle also captures the preference and displayed blink.
    for wanted in [false,true]:
        rig.reset();rig.apply_controls({"auto_blink":wanted});rig.advance(4.03)
        var before=rig.displayed_pose();rig.release();check(before==rig.displayed_pose(),"idle release C0")
        pending(wanted,"idle release");rig.advance(.45);neutral(wanted,"idle release completion")
    # Exact floating-point threshold, not a neutral-looking sampled pose, owns restore.
    begin("EXP-007",true);rig.advance(.6);rig.release();rig.advance(.15);rig.advance(.30)
    pending(true,"split release below threshold");check(rig.release_time<rig.RELEASE_SECONDS,"rounding remains below threshold")
    rig.advance(rig.RELEASE_SECONDS-rig.release_time);neutral(true,"exact remaining release")
    var viewer=load("res://expression_viewer.tscn").instantiate();root.add_child(viewer);viewer.set_process(false);viewer.rig.set_process(false)
    viewer.apply_controls({"auto_blink":true});viewer.play_selected();viewer._process(0)
    check(viewer.auto_blink_button.button_pressed and not viewer.rig.auto_blink,"UI preference checked while actual paused")
    check("paused" in viewer.auto_blink_status.text and "neutral recovery" in viewer.auto_blink_status.text,"UI explains suspension")
    viewer.auto_blink_button.button_pressed=false
    check(not viewer.rig.auto_blink_pending_restore and viewer.rig.active_performance=="","unchecking pending preference is explicit manual takeover")
    viewer._process(0);check("off" in viewer.auto_blink_status.text,"UI cancellation is off")
    viewer.apply_controls({"auto_blink":true});viewer.play_selected();viewer.rig.advance(10);viewer._process(0)
    check(viewer.auto_blink_button.button_pressed and "active" in viewer.auto_blink_status.text,"UI restored actual active")
    var bridge=viewer.control_bridge;bridge.rig=viewer.rig
    var capabilities=bridge.capabilities()
    check(capabilities.auto_blink_policy.restore_after_neutral_recovery,"capabilities report correction")
    check(not capabilities.ai_model_connected and not capabilities.tts_connected and not bridge.enabled,"preparation only / no listener")
    capabilities.auto_blink_policy.reset_disables=false
    check(bridge.capabilities().auto_blink_policy.reset_disables,"capabilities detached")
    var saved=viewer.rig.get_state();saved.auto_blink_pending_restore=true
    check(not viewer.rig.get_state().auto_blink_pending_restore,"state detached")
    # Exercise the real parser/dispatch/envelope without calling start/listen.
    bridge.session=1;bridge.external_enabled=true
    var request={"protocol":1,"id":1,"verb":"capabilities"}
    bridge.dispatch(JSON.stringify(request).to_utf8_buffer())
    var response=JSON.parse_string(bridge.outgoing.get_string_from_utf8());bridge.outgoing.clear()
    check(response.ok and response.result.auto_blink_policy.pending_state_field=="auto_blink_pending_restore","dispatched capabilities describe pending intent")
    check(JSON.stringify(response).to_utf8_buffer().size()<bridge.MAX_RESPONSE_BYTES,"capability response within bounded capacity")
    viewer.rig.play_expression("EXP-005")
    request={"protocol":1,"id":2,"verb":"get_state"};bridge.dispatch(JSON.stringify(request).to_utf8_buffer())
    response=JSON.parse_string(bridge.outgoing.get_string_from_utf8());bridge.outgoing.clear()
    check(response.ok and not response.result.rig.auto_blink and response.result.rig.auto_blink_pending_restore,"dispatched state distinguishes actual and pending")
    request={"protocol":1,"id":3,"session":1,"verb":"apply_controls","args":{"auto_blink":false}}
    bridge.dispatch(JSON.stringify(request).to_utf8_buffer())
    response=JSON.parse_string(bridge.outgoing.get_string_from_utf8());bridge.outgoing.clear()
    check(response.ok and not response.result.rig.auto_blink_pending_restore and response.result.rig.active_expression=="","dispatch explicit false cancels deferred intent")
    check(not bridge.enabled and not bridge.server.is_listening(),"no real socket opened by callable dispatch")
    # The ordinary renderer/clock remain byte-identical; active API uses same closure floor.
    print("AUTO_BLINK_LIFECYCLE_", "PASS" if failures.is_empty() else "FAIL"," checks=",checks," failures=",failures.size())
    quit(0 if failures.is_empty() else 1)

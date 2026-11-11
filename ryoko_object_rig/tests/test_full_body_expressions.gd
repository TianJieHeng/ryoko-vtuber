extends SceneTree
## Focused viewer wiring check. Does not rewrite the frozen full_body/review evidence.
var checks = 0
var failures:Array = []
func _initialize():call_deferred("run")
func check(ok:bool,label:String):
    checks += 1
    if not ok:failures.append(label)
func key(viewer,code):
    var event = InputEventKey.new();event.pressed = true;event.keycode = code
    viewer._input(event)
func bridge_request(bridge,id:int,verb:String,args:Dictionary = {})->Dictionary:
    bridge.outgoing.clear()
    var request = {"protocol":1,"id":id,"verb":verb,"args":args}
    if verb in bridge.WRITE_VERBS:request.session = bridge.session
    bridge.dispatch(JSON.stringify(request).to_utf8_buffer())
    var result = JSON.parse_string(bridge.outgoing.get_string_from_utf8())
    return result if result is Dictionary else {}
func check_full_controls(viewer):
    var rig = viewer.rig
    var face = rig.expression_rig
    var bridge = viewer.control_bridge
    bridge.set_process(false)
    check(not bridge.enabled and not bridge.server.is_listening(),"bridge starts off with no listener")
    check(bridge.rig == rig and rig.registry_ready,"bridge controller is the ready full-body rig")
    check(rig.auto_blink_policy() == face.auto_blink_policy(),"original auto-blink policy exposed")
    var expected:Array = []
    for channel in face.CHANNELS:
        if channel not in face.SCOPED_CHANNELS:expected.append(channel)
    var actual:Array = viewer.face_sliders.keys();actual.sort();expected.sort()
    check(actual == expected,"all original manual face channels retained")
    var bounds_match = true
    for channel in actual:
        var bounds:Array = face.Registry.CHANNEL_BOUNDS[channel]
        var slider:HSlider = viewer.face_sliders[channel]
        bounds_match = bounds_match and is_equal_approx(slider.min_value,bounds[0]) and is_equal_approx(slider.max_value,bounds[1]) and is_equal_approx(slider.step,.001)
    check(bounds_match,"original normalized face limits and precision retained")
    viewer.auto_blink_button.button_pressed = true
    check(face.auto_blink,"auto-blink checkbox enables original policy")
    viewer.play_selected_expression();viewer._process(0)
    check(not face.auto_blink and face.auto_blink_pending_restore and viewer.auto_blink_button.button_pressed,"auto-blink preference survives performance pause")
    viewer.stop_expression();face.advance(face.RELEASE_SECONDS);viewer._process(0)
    check(face.auto_blink and not face.auto_blink_pending_restore,"auto-blink resumes after release")
    viewer.apply_controls({"reset":true});viewer._process(0)
    check(not face.auto_blink and not viewer.auto_blink_button.button_pressed,"reset disables auto-blink and updates checkbox")
    viewer.face_sliders.mouth_width_screen_left.value = .4;viewer._process(0)
    check(not viewer.face_sliders.mouth_open.editable,"positive width disables mouth opening")
    viewer.face_sliders.mouth_width_screen_left.value = 0;viewer._process(0)
    viewer.face_sliders.mouth_open.value = .3;viewer._process(0)
    check(not viewer.face_sliders.mouth_width_screen_left.editable and not viewer.face_sliders.mouth_width_screen_right.editable and not viewer.face_sliders.mouth_kiss.editable,"opening disables sealed-mouth width and kiss sliders")
    viewer.face_sliders.mouth_open.value = 0;viewer._process(0)
    viewer.face_sliders.mouth_kiss.value = .5;viewer._process(0)
    check(not viewer.face_sliders.mouth_open.editable and is_equal_approx(face.pose_now().mouth_kiss,.5),"kiss blend works and protects opening interlock")
    viewer.apply_controls({"reset":true});viewer._process(0)
    check(viewer.face_sliders.mouth_open.editable and viewer.face_sliders.mouth_width_screen_left.editable,"neutral reset unlocks mouth controls")
    viewer.face_sliders.brow_inner_lift_screen_left.value = .2
    viewer.face_sliders.gaze_down_extra.value = .3
    check(is_equal_approx(face.pose_now().brow_inner_lift_screen_left,.2) and is_equal_approx(face.pose_now().gaze_down_extra,.3),"added brow and extra-gaze sliders reach original controller")
    viewer.apply_controls({"reset":true})
    # Exercise the unchanged dispatch/takeover logic in memory. Never call start()
    # or bind a port; the fake enabled flag only allows manual-lock behavior.
    bridge.enabled = true;bridge.external_enabled = true;bridge.session = 1
    var response = bridge_request(bridge,1,"capabilities")
    check(response.get("ok",false) and response.result.expressions.size() == 47,"bridge capabilities fit bounded response and retain 47 profiles")
    response = bridge_request(bridge,2,"play_expression",{"expression_id":viewer.expression_ids[0]})
    check(response.get("ok",false) and face.active_performance == viewer.expression_ids[0],"bridge expression command reaches attached head")
    rig.apply_body_controls({"head_tilt":.5});rig.play_bounce_demo();rig.advance_secondary_motion(.1)
    response = bridge_request(bridge,3,"get_state")
    check(response.get("ok",false) and response.result.rig.body.controls.head_tilt == .5,"bridge state includes full-body pose within response bound")
    response = bridge_request(bridge,4,"reset")
    check(response.get("ok",false) and rig.body_controls.head_tilt == 0 and not rig.secondary_motion.snapshot().demo_active and face.active_performance == "","bridge reset clears face, body, and bounce together")
    viewer.play_selected_expression();viewer._process(0)
    check(not bridge.external_enabled and viewer.bridge_button.visible,"manual Play locks external control and exposes recovery")
    await process_frame
    check(viewer.get_viewport_rect().encloses(viewer.bridge_button.get_global_rect()),"external-control recovery visible outside scroll panel")
    viewer.bridge_button.pressed.emit()
    check(bridge.external_enabled and not bridge.discovered,"re-enable starts fresh control session")
    viewer.stop_expression();check(not bridge.external_enabled,"manual Stop takes bridge ownership")
    bridge.allow_external();viewer.face_sliders.blink_L.value = .3
    check(not bridge.external_enabled,"manual face slider takes bridge ownership")
    bridge.allow_external();viewer.body_sliders.head_tilt.value = .3
    check(not bridge.external_enabled,"manual body slider takes bridge ownership")
    bridge.allow_external();viewer.auto_blink_button.button_pressed = true
    check(not bridge.external_enabled,"auto-blink preference takes bridge ownership")
    bridge.allow_external();key(viewer,KEY_0)
    check(not bridge.external_enabled,"keyboard reset takes bridge ownership")
    bridge.allow_external();viewer.apply_controls({"reset":false})
    check(bridge.external_enabled,"no-op control does not take bridge ownership")
    check(not bridge.server.is_listening(),"focused bridge checks never bind a network port")
    bridge.stop()
func run():
    var viewer = load("res://full_body/full_body_viewer.tscn").instantiate();root.add_child(viewer)
    viewer.set_process(false)
    var rig = viewer.rig
    check(rig.ready_for_controls,"full-body viewer ready")
    if not rig.ready_for_controls:print(rig.last_error);quit(1);return
    rig.set_physics_process(false);rig.expression_rig.set_process(false)
    await process_frame
    await process_frame
    var face = rig.expression_rig
    var head = face.head
    var head_bind:Transform2D = head.transform
    var entries:Array = rig.list_expressions()
    var play:Button = viewer.find_child("ExpressionPlay",true,false)
    var stop:Button = viewer.find_child("ExpressionStop",true,false)
    check(entries.size() == 47 and viewer.expression_selector.item_count == 47,"all 47 existing profiles exposed")
    check(viewer.expression_selector.get_index() < viewer.body_sliders.frame_x.get_index(),"expression picker precedes body sliders")
    check(viewer.view_mode == "Full body","viewer opens on full body")
    check(play != null and stop != null,"visible play and stop controls")
    var viewport:Rect2 = viewer.get_viewport_rect()
    check(viewport.encloses(viewer.expression_selector.get_global_rect()) and viewport.encloses(play.get_global_rect()) and viewport.encloses(stop.get_global_rect()),"picker and playback controls visible without scrolling")
    var neutral:Dictionary = face.neutral_pose()
    for index in entries.size():
        var entry:Dictionary = entries[index]
        rig.reset();rig.apply_body_controls({"head_tilt":.4,"chest_tilt":.3})
        var body_pose:Dictionary = rig.get_body_state().controls
        viewer.expression_selector.select(index);play.pressed.emit()
        check(face.active_performance == entry.id,entry.id + " picker plays original profile")
        var definition:Dictionary = face.registry.definition(entry.id)
        var sample_time = .5
        var best_weight = 0.0
        for frame in definition.keyframes:
            var weight = 0.0
            for value in frame.values.values():weight += absf(float(value))
            if weight > best_weight:best_weight = weight;sample_time = float(frame.time)
        face.advance(sample_time);viewer._process(0)
        check(face.displayed_pose() != neutral,entry.id + " drives non-neutral live face")
        check(viewer.expression_status.text.contains(entry.id),entry.id + " visible playback state")
        check(rig.get_body_state().controls == body_pose,entry.id + " playback preserves body pose")
        check(head.get_parent() == rig.joints.head and head.transform.is_equal_approx(head_bind),entry.id + " playback preserves attached head transform")
        check(face.body == null and face.get_node_or_null("FixedNeckTorso") == null,entry.id + " no legacy bust")
        stop.pressed.emit();face.advance(face.RELEASE_SECONDS)
        check(face.active_performance == "" and face.displayed_pose() == neutral,entry.id + " stop releases to neutral")
        check(rig.get_body_state().controls == body_pose and head.transform.is_equal_approx(head_bind),entry.id + " stop preserves body and head bind")
        play.pressed.emit();face.advance(float(entry.duration))
        check(face.active_performance == "" and face.displayed_pose() == neutral,entry.id + " natural end restores neutral")
        rig.reset()
        check(head.get_parent() == rig.joints.head and head.transform.is_equal_approx(head_bind),entry.id + " reset preserves attached head transform")
    viewer.expression_selector.select(0);key(viewer,KEY_P)
    check(face.active_performance == entries[0].id,"P plays selected expression")
    face.advance(.5);key(viewer,KEY_P)
    check(face.performance_time == 0.0,"repeated Play restarts original performance")
    key(viewer,KEY_SPACE);check(face.active_performance == "","Space stops expression")
    key(viewer,KEY_P);face.advance(.5);viewer.face_sliders.blink_L.value = .6
    check(face.active_performance == "" and is_equal_approx(face.pose_now().blink_L,.6),"existing face slider takes manual ownership")
    rig.play_bounce_demo();rig.advance_secondary_motion(.1)
    var bounce:Dictionary = rig.secondary_motion.snapshot()
    key(viewer,KEY_P);stop.pressed.emit()
    check(bounce.demo_active and rig.secondary_motion.snapshot() == bounce,"expression stop leaves bounce running")
    key(viewer,KEY_0)
    check(face.displayed_pose() == neutral and rig.get_body_state().controls.head_tilt == 0.0,"0 resets face and body")
    check(head.transform.is_equal_approx(head_bind) and face.body == null,"reset retains full-body attachment without bust")
    await check_full_controls(viewer)
    var result = {"status":"PASS" if failures.is_empty() else "FAIL","checks":checks,"profiles":entries.size(),"failures":failures,"scope":"Headless Godot viewer controls and original facial playback on approved full-body assembly. Does not establish rendered pixel parity."}
    print(JSON.stringify(result));quit(0 if failures.is_empty() else 1)

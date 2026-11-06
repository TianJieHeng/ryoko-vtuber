extends SceneTree
var checks=0
var fails=0
var rig
func ck(ok:bool,label:String):
    checks+=1
    if not ok:fails+=1;push_error("YAWN_TEST "+label)
func _initialize():call_deferred("run")
func run():
    rig=load("res://yawn_rig.tscn").instantiate();root.add_child(rig);await process_frame;rig.set_process(false)
    rig.apply_controls({"reset":true});var neutral=rig.face.snapshot()
    ck(rig.face.mouth_opening==0,"neutral mouth")
    var face_texture=rig.face.objects.stationary_backing.texture
    var head_transform=rig.head.transform
    for cycle in range(2):
        ck(rig.apply_controls({"perform_expression":"EXP-163"}),"trigger")
        for frame in range(348):
            rig._process(1.0/60.0)
            ck(rig.face.objects.stationary_backing.texture==face_texture,"immutable face source")
            ck(rig.head.transform==head_transform,"stationary jaw/head")
            ck(rig.face.mouth_variant=="continuous_neutral_split","no A/O switch")
            ck(not rig.face.mouth_sprite.visible and not rig.face.objects.neutral_lips.visible,"no duplicate neutral or viseme")
            for key in rig.face.objects:
                var n=rig.face.objects[key];var pivot=rig.face.homes[key].node
                ck(n.scale==Vector2.ONE and pivot.scale==Vector2.ONE,"unit local scale "+key)
                ck(n.modulate.a==1.0,"full object opacity "+key)
        rig._process(.001)
        ck(rig.active_performance=="","complete release")
        ck(rig.pose_now()==rig.neutral_pose(),"exact neutral values after cycle")
    # Retrigger does not jump at trigger; owns no timers/tweens after reset.
    for i in range(20):
        rig.apply_controls({"perform_expression":"EXP-163"});rig._process(.9+i*.031)
        var before=rig.pose_now()
        ck(rig.apply_controls({"perform_expression":"EXP-163"}),"retrigger")
        ck(rig.pose_now()==before,"retrigger continuity at transaction")
        rig._process(.01)
        var moved=rig.pose_now()
        ck(abs(moved.mouth_open-before.mouth_open)<.01,"bounded retrigger first step")
        ck(rig.apply_controls({"release_performance":true}),"release")
        rig._process(.45);ck(rig.pose_now()==rig.neutral_pose(),"interrupted smooth release")
        rig.apply_controls({"perform_expression":"EXP-163"});rig._process(2.2)
        ck(rig.apply_controls({"mouth_open":.24,"blink_R":.42}),"manual interruption")
        ck(rig.active_performance=="" and rig.face.mouth_opening==.24,"manual owns mouth")
        rig._process(2);ck(rig.face.mouth_opening==.24,"no stale performance writer")
        ck(rig.apply_controls({"reset":true}),"reset")
        ck(rig.face.snapshot()==neutral,"deterministic reset state")
    for shape in ["A","E","I","O","U"]:
        var before=rig.face.snapshot()
        ck(not rig.apply_controls({"mouth":shape}),"unapproved discrete aperture bypass rejected")
        ck(not rig.apply_controls({"viseme":shape}),"unapproved discrete alias rejected")
        ck(rig.face.snapshot()==before,"discrete rejection atomic")
        ck(rig.apply_controls({"mouth":"REST"}),"explicit continuous REST")
    # Invalid input has no partial mutation.
    rig.apply_controls({"perform_expression":"EXP-163"});rig._process(1.7)
    var saved=rig.face.snapshot();var time=rig.performance_time
    for data in [{"perform_expression":"EXP-005"},{"expression":"EXP-163"},{"mouth_open":-0.1},{"mouth_open":1.01},{"mouth_open":NAN},{"mouth_open":INF},{"mouth_open":"yes"},{"blink":.5,"head_tilt":1},{"mouth_open":.5,"mouth":"A"},{"perform_expression":"EXP-163","reset":true},{"release_performance":1},{"hair_sway":rig.MAX_HAIR_SWAY+0.000001},{"hair_sway":-rig.MAX_HAIR_SWAY-0.000001},{"blink":.8,"hair_sway":1},{"reset":true,"hair_sway":-1},{"mouth_open":.3,"hair_sway":.071},{"gaze_x":.1,"mouth_open":.3}]:
        ck(not rig.apply_controls(data),"reject invalid "+str(data));ck(rig.face.snapshot()==saved and rig.performance_time==time,"atomic rejection")
    for id in JSON.parse_string(FileAccess.get_file_as_string("res://legacy_expression_ids.json")).legacy_expression_ids:
        ck(not rig.apply_controls({"expression":id}),"all static expression IDs still gated "+id)
    rig.apply_controls({"reset":true})
    for i in range(1001):
        var t=i*rig.DURATION/1000.0;var p=rig.sample_yawn(t)
        ck(p.mouth_open>=0 and p.mouth_open<=1,"bounded sampler")
        ck(abs(p.hair_sway)<=rig.MAX_HAIR_SWAY,"timeline remains inside verified hair range")
    var stage=load("res://yawn_stage.tscn").instantiate();root.add_child(stage);stage.set_process(false);stage.primary.set_process(false)
    stage.apply_controls({"reset":true,"auto_blink":true});stage.advance(4.0)
    ck(stage.primary.face.closure.x>0,"stage auto-blink is visible")
    for closeup in stage.closeups:ck(closeup.face.closure==stage.primary.face.closure,"closeups follow displayed auto-blink closure")
    stage.apply_controls({"reset":true});stage.apply_controls({"perform_expression":"EXP-163"})
    for i in range(180):
        stage.advance(1.0/30.0)
        for closeup in stage.closeups:
            ck(closeup.face.closure==stage.primary.face.closure,"stage yawn eye sync")
            ck(closeup.face.mouth_opening==stage.primary.face.mouth_opening,"stage yawn mouth sync")
    print("YAWN_CHECKS_", "PASS" if fails==0 else "FAIL", " checks=",checks," failures=",fails)
    quit(0 if fails==0 else 1)

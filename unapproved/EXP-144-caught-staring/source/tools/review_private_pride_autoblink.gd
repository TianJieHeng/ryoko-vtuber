extends SceneTree
## Sparse actual-Godot phase samples, not a normal-speed video.
## Run only after copying into the final integration project; no sockets or model.
var rig
var out=""
var checks=0
var failures=[]
var frames=[]
func _initialize():call_deferred("run")
func check(ok,label):
    checks+=1
    if not ok:failures.append(label);push_error(label)
func hash_bytes(bytes):
    var h=HashingContext.new();h.start(HashingContext.HASH_SHA256);h.update(bytes);return h.finish().hex_encode()
func capture(label):
    rig._write_pose() # Refresh clip uniforms after the fixed review placement.
    await process_frame;await RenderingServer.frame_post_draw
    var im=root.get_texture().get_image()
    check(im.save_png(out+"/"+label+".png")==OK,"capture "+label)
    var digest=hash_bytes(im.get_data())
    frames.append({"label":label,"pixels_sha256":digest,"state":rig.get_state(),"elapsed":rig.elapsed})
    return digest
func start_private_pride():
    rig.reset();rig.apply_controls({"auto_blink":true});rig.advance(4.03)
    var before=rig.displayed_pose();check(rig.play_expression("EXP-152"),"start private_pride")
    check(rig.displayed_pose()==before,"private_pride incoming automatic closure C0")
    check(not rig.auto_blink and rig.auto_blink_pending_restore,"private_pride saves enabled preference")
func neutral(label):
    check(rig.auto_blink and not rig.auto_blink_pending_restore,label+" restored enabled preference")
    check(rig.active_performance=="" and rig.release_time<0 and rig.pose_now()==rig.neutral_pose(),label+" true neutral completion")
    check(rig.face.closure==Vector2.ZERO and rig.face.smile_eyes==Vector2.ZERO,label+" open ordinary eyes")
    check(rig.elapsed==0,label+" existing clock restarts open")
    for joint in rig.face.smile_eye_joints:check(not rig.face.objects[joint.key].visible,label+" smiling contour released")
func run():
    for arg in OS.get_cmdline_user_args():
        if arg.begins_with("--output="):out=arg.trim_prefix("--output=")
    if out.is_empty():quit(2);return
    DirAccess.make_dir_recursive_absolute(out);root.size=Vector2i(1136,1384)
    rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
    check(rig.rig_ready and rig.registry_ready and rig.registry.resolve("EXP-152")=="EXP-152","private_pride shared rig ready")
    if not rig.rig_ready or not rig.registry_ready or rig.registry.resolve("EXP-152")!="EXP-152":quit(2);return
    rig.hud.hide();rig.hint.hide();rig.pose_status.hide()
    rig.head.position=Vector2.ZERO;rig.body.position=Vector2.ZERO;rig.head.scale=Vector2.ONE;rig.body.scale=Vector2.ONE
    # Native direct-idle reference. Compare every restored phase, including hair edges.
    var reference=[]
    rig.reset();rig.apply_controls({"auto_blink":true});rig.advance(3.86)
    for i in range(9):
        if i>0:rig.advance(.0425)
        reference.append(await capture("ordinary_reference_%02d"%i))
    for ending in ["complete","release"]:
        start_private_pride();rig.advance(.75)
        check(rig.face.smile_eyes==Vector2.ZERO and rig.face.closure.is_equal_approx(Vector2(.42,.42)) and rig.face.gaze_down_extra==1,"actual pride ordinary lids and down-look")
        await capture("private_pride_"+ending+"_held")
        if ending=="complete":rig.advance(1.9)
        else:
            var before=rig.displayed_pose();rig.release();check(rig.displayed_pose()==before,"private_pride release C0")
            rig.advance(.449999);check(not rig.auto_blink and rig.auto_blink_pending_restore,"release still suspended just before boundary")
            rig.advance(.0000011)
        neutral("private_pride "+ending)
        check(await capture("private_pride_"+ending+"_recovered")==reference[0],"recovered ordinary neutral pixels "+ending)
        rig.advance(3.86)
        for i in range(9):
            if i>0:rig.advance(.0425)
            check(await capture("private_pride_"+ending+"_blink_%02d"%i)==reference[i],"restored ordinary blink/hair phase "+ending+" "+str(i))
            for joint in rig.face.smile_eye_joints:check(not rig.face.objects[joint.key].visible,"no held private pride eye or gaze state during idle blink")
        print("PRIVATE_PRIDE_AUTOBLINK_PHASES ",ending)
    # Interrupted release and two-way family handoff, without redundant blink movies.
    for handoff in ["release_retrigger","from_laughter","to_laughter"]:
        start_private_pride();rig.advance(.75)
        if handoff=="release_retrigger":
            rig.release();rig.advance(.2);var before=rig.displayed_pose();rig.play_expression("EXP-152")
            check(rig.displayed_pose()==before,"partial-release retrigger C0")
        elif handoff=="from_laughter":
            rig.play_expression("EXP-005");rig.advance(.9);var before=rig.displayed_pose();rig.play_expression("EXP-152")
            check(rig.displayed_pose()==before,"laughter to private_pride C0")
        else:
            var before=rig.displayed_pose();rig.play_expression("EXP-005");check(rig.displayed_pose()==before,"private_pride to laughter C0")
        check(not rig.auto_blink and rig.auto_blink_pending_restore,"handoff preserves suspended intent")
        rig.advance(10);neutral(handoff)
        check(await capture("handoff_"+handoff+"_recovered")==reference[0],"handoff restores ordinary pixels")
    # Disabled preference remains disabled, and explicit false-to-false cancels pending.
    for cancel in ["disable","manual","reset"]:
        start_private_pride();rig.advance(.75);rig.release();rig.advance(.1)
        check(not rig.auto_blink and rig.auto_blink_pending_restore,"before false-to-false cancellation")
        if cancel=="disable":rig.apply_controls({"auto_blink":false})
        elif cancel=="manual":rig.apply_controls({"mouth_open":.13})
        else:rig.reset()
        check(not rig.auto_blink and not rig.auto_blink_pending_restore and rig.release_time<0,"cancel actual and pending "+cancel)
        var before=await capture("cancel_"+cancel+"_before");rig.advance(4.03)
        check(await capture("cancel_"+cancel+"_after")==before,"canceled pose stays pixel-identical "+cancel)
        rig.play_expression("EXP-152");rig.advance(1.9);rig.advance(4.03)
        check(not rig.auto_blink and not rig.auto_blink_pending_restore and rig.face.closure==Vector2.ZERO,"later private_pride cannot resurrect cancellation")
    var record={"checks":checks,"failures":failures,"frames":frames,"normal_speed_playback_performed":false,"ai_model_connected":false,"tts_connected":false,"socket_test_performed":false,"phase_sample_elapsed_seconds":[3.86,3.9025,3.945,3.9875,4.03,4.0725,4.115,4.1575,4.2],"note":"Sparse deterministic phase samples, not continuous video. UI signal cancellation is separately covered by test_auto_blink_lifecycle.gd."}
    var file=FileAccess.open(out+"/evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify(record,"  ",true,true));file.close()
    print("PRIVATE_PRIDE_AUTOBLINK_RENDER_","PASS" if failures.is_empty() else "FAIL"," checks=",checks," failures=",failures.size()," frames=",frames.size())
    quit(0 if failures.is_empty() else 1)

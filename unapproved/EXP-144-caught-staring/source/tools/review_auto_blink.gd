extends SceneTree
## Deterministic actual-Godot raster samples. No real-time playback claim.
var rig
var out=""
var baseline_only=false
var checks=0
var failures=[]
var frames=[]
var parity=[]
const IDS=["EXP-163","EXP-005","EXP-001","EXP-006","EXP-107","EXP-007"]
func _initialize():call_deferred("run")
func check(ok,label):
    checks+=1
    if not ok:failures.append(label);push_error(label)
func hash_bytes(bytes):
    var h=HashingContext.new();h.start(HashingContext.HASH_SHA256);h.update(bytes);return h.finish().hex_encode()
func capture(label):
    rig._write_pose()
    await process_frame;await RenderingServer.frame_post_draw
    var im=root.get_texture().get_image();check(im.save_png(out+"/"+label+".png")==OK,"capture "+label)
    var digest=hash_bytes(im.get_data())
    frames.append({"label":label,"pixels_sha256":digest,"state":rig.get_state(),"elapsed":rig.elapsed})
    return digest
func parity_state():
    var s=rig.get_state();s.erase("auto_blink_pending_restore")
    s.face=rig.face.snapshot();s.elapsed=rig.elapsed;s.restart=rig.restart_pose;s.release=rig.release_pose;s.current=rig.current_pose
    return hash_bytes(JSON.stringify(s,"",true,true).to_utf8_buffer())
func run():
    for arg in OS.get_cmdline_user_args():
        if arg.begins_with("--output="):out=arg.trim_prefix("--output=")
        if arg=="--baseline-only":baseline_only=true
    if out.is_empty():quit(2);return
    DirAccess.make_dir_recursive_absolute(out)
    root.size=Vector2i(1136,1384)
    rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
    check(rig.rig_ready and rig.registry_ready,"ready")
    if not rig.rig_ready or not rig.registry_ready:quit(2);return
    rig.hud.hide();rig.hint.hide();rig.pose_status.hide()
    rig.head.position=Vector2.ZERO;rig.body.position=Vector2.ZERO;rig.head.scale=Vector2.ONE;rig.body.scale=Vector2.ONE
    # Full controller/object-state parity for disabled runs; only named samples are rendered.
    for id in IDS:
        rig.reset()
        for cycle in range(2):
            rig.play_expression(id)
            var hashes=[]
            for tick in range(int(ceil(rig.registry.definition(id).duration*30))+2):
                rig.advance(1.0/30.0);hashes.append(parity_state())
            parity.append({"id":id,"cycle":cycle,"hashes":hashes})
        rig.reset();rig.play_expression(id);rig.advance(.6)
        await capture("disabled_"+id+"_pose")
        rig.release();rig.advance(.45)
        await capture("disabled_"+id+"_release")
    if not baseline_only:
        var reference=[]
        rig.reset();rig.apply_controls({"auto_blink":true});rig.advance(3.86)
        for i in range(9):
            if i>0:rig.advance(.0425)
            reference.append(await capture("reference_blink_%02d"%i))
        for id in IDS:
            for ending in ["complete","release"]:
                rig.reset();rig.apply_controls({"auto_blink":true});rig.advance(4.03)
                rig.play_expression(id)
                if ending=="complete":rig.advance(rig.registry.definition(id).duration)
                else:rig.advance(.6);rig.release();rig.advance(.45)
                check(rig.auto_blink and not rig.auto_blink_pending_restore,id+" "+ending+" restored")
                check(rig.pose_now()==rig.neutral_pose() and rig.face.closure==Vector2.ZERO,id+" "+ending+" open neutral")
                check(rig.elapsed==0,id+" "+ending+" existing clock restarted")
                var recovered=await capture(id+"_"+ending+"_recovered")
                check(recovered==reference[0],id+" "+ending+" recovered pixels match neutral")
                rig.advance(3.86)
                for i in range(9):
                    if i>0:rig.advance(.0425)
                    var digest=await capture(id+"_"+ending+"_blink_%02d"%i)
                    check(digest==reference[i],id+" "+ending+" ordinary eyelid/hair pixels "+str(i))
                    for joint in rig.face.smile_eye_joints:check(not rig.face.objects[joint.key].visible,"no stale smiling lash geometry")
                print("AUTO_BLINK_RENDER ",id," ",ending)
        for cancellation in ["disable","manual","reset"]:
            rig.reset();rig.apply_controls({"auto_blink":true});rig.play_expression("EXP-005");rig.advance(.6);rig.release();rig.advance(.1)
            if cancellation=="disable":rig.apply_controls({"auto_blink":false})
            elif cancellation=="manual":rig.apply_controls({"mouth_open":.13})
            else:rig.reset()
            check(not rig.auto_blink and not rig.auto_blink_pending_restore,"cancel "+cancellation)
            var before=await capture("cancel_"+cancellation+"_before")
            rig.advance(4.03)
            check(await capture("cancel_"+cancellation+"_after")==before,"cancel stays pixel-identical "+cancellation)
            rig.play_expression("EXP-007");rig.advance(3.2);rig.advance(4.03)
            check(not rig.auto_blink and not rig.auto_blink_pending_restore and rig.face.closure==Vector2.ZERO,"cancel not resurrected by new performance")
    var record={"checks":checks,"failures":failures,"frames":frames,"disabled_state_parity":parity,"normal_speed_playback_performed":false,"ai_model_connected":false,"tts_connected":false,"socket_test_performed":false,"blink_sample_seconds":[3.86,3.9025,3.945,3.9875,4.03,4.0725,4.115,4.1575,4.2]}
    var f=FileAccess.open(out+"/evidence.json",FileAccess.WRITE);f.store_string(JSON.stringify(record,"  ",true,true));f.close()
    print("AUTO_BLINK_RENDER_","PASS" if failures.is_empty() else "FAIL"," checks=",checks," failures=",failures.size()," frames=",frames.size())
    quit(0 if failures.is_empty() else 1)

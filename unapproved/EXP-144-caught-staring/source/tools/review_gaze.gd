extends SceneTree
## Asserted actual-Godot diagnostics through the SAME public controller.
## Use --baseline only in an isolated unchanged approved baseline copy.
var rig
var out=""
var native=false
var baseline=false
var full=false
var records=[]
func _initialize():call_deferred("run")
func require(ok:bool,message:String):
    if not ok:
        push_error("GAZE_CAPTURE_FAILED "+message);quit(2)
        assert(false,message)
func command(data:Dictionary):
    require(rig.apply_controls(data),"Command rejected: "+JSON.stringify(data)+" / "+rig.last_error)
func advance(seconds:float):require(rig.advance(seconds),"advance rejected")
func snap(label:String):
    await process_frame
    await RenderingServer.frame_post_draw
    var im=root.get_texture().get_image();require(im.save_png(out+"/"+label+".png")==OK,"save failed")
    records.append({"label":label,"pose":rig.pose_now(),"face":rig.face.snapshot(),"state":rig.get_state()})
func manual(lid:float,gaze:Vector2,hair:float=0.0):
    command({"reset":true,"blink":lid,"gaze_x":gaze.x,"gaze_y":gaze.y,"hair_sway":hair})
    require(rig.face.closure==Vector2.ONE*lid,"lid mismatch")
    require(rig.face.gaze==gaze,"gaze mismatch")
    require(rig.active_performance=="" and rig.release_time<0,"manual ownership mismatch")
func run():
    for arg in OS.get_cmdline_user_args():
        if arg.begins_with("--output="):out=arg.trim_prefix("--output=")
        if arg=="--native":native=true
        if arg=="--baseline":baseline=true
        if arg=="--full":full=true
    require(not out.is_empty(),"output directory required")
    DirAccess.make_dir_recursive_absolute(out)
    root.size=Vector2i(1136,1384) if native else Vector2i(1136,800)
    rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
    rig.hud.hide();rig.hint.hide();rig.pose_status.hide()
    if native:
        rig.body.position=Vector2.ZERO;rig.body.scale=Vector2.ONE
        rig.head.position=Vector2.ZERO;rig.head.scale=Vector2.ONE
    await process_frame
    var directions=[Vector2.ZERO] if baseline else [Vector2.ZERO,Vector2(-1,0),Vector2(1,0),Vector2(0,-1),Vector2(0,1),Vector2(-1,-1),Vector2(1,-1),Vector2(-1,1),Vector2(1,1)]
    var hairs=[-.07,0.0,.07] if full else [0.0]
    for hair in hairs:
        for lid in [0.0,.25,.5,.75,1.0]:
            for gaze in directions:
                manual(lid,gaze,hair)
                var name="lid_%03d_gaze_%d_%d"%[roundi(lid*100),roundi(gaze.x),roundi(gaze.y)]
                if hair!=0:name+="_hair_%d"%roundi(hair*1000)
                await snap(name)
    command({"reset":true});await snap("neutral_return")
    # Separate transactions are essential: mixed reset+trigger is rejected.
    for t in [0.0,.8,1.5,2.2,3.0,3.8,4.5,5.8]:
        command({"reset":true});command({"perform_expression":"EXP-163"});advance(t)
        require(is_equal_approx(rig.performance_time,t),"yawn time did not advance")
        if t>0 and t<5.8:
            require(rig.active_performance=="EXP-163","yawn ownership inactive")
            require(rig.face.owners.eyes=="EXP-163","yawn eye owner inactive")
            require(rig.pose_now()!=rig.neutral_pose(),"yawn pose is static neutral")
        await snap("yawn_%03d"%roundi(t*100))
    if full and not baseline:
        for side in ["blink_R","blink_L"]:
            for lid in [.25,.5,.75,1.0]:
                for gaze in [Vector2(-1,-1),Vector2(1,-1),Vector2(-1,1),Vector2(1,1)]:
                    manual(0,gaze);command({side:lid})
                    await snap("unilateral_%s_%03d_%d_%d"%[side,roundi(lid*100),roundi(gaze.x),roundi(gaze.y)])
        # Ownership isolation is actual Godot sprite visibility, not CPU artwork.
        for gaze in [Vector2.ZERO,Vector2(-1,0),Vector2(1,0)]:
            manual(0,gaze)
            for prefix in ["iris_","sclera_","hair_"]:
                var changed=[]
                for key in rig.face.objects:
                    if key.begins_with(prefix):
                        changed.append(key);rig.face.objects[key].hide()
                await snap("hide_%s_gaze_%d"%[prefix.trim_suffix("_"),roundi(gaze.x)])
                for key in changed:rig.face.objects[key].show()
        # Fractional forward/reversal frames must match at the same controls.
        for direction in ["forward","reverse"]:
            var indices=range(33) if direction=="forward" else range(32,-1,-1)
            for i in indices:
                var phase=float(i)/32.0*TAU
                var gaze=Vector2(sin(phase),cos(phase));var lid=(1.0-cos(phase*2.0))*.45
                manual(lid,gaze,sin(phase)*.07)
                await snap("sweep_%s_%03d"%[direction,i])
        manual(.4,Vector2(1,-1));command({"perform_expression":"EXP-163"});await snap("lifecycle_trigger")
        advance(.08);await snap("lifecycle_trigger_blend")
        command({"gaze_x":-1.0,"gaze_y":1.0,"blink_L":.75});require(rig.active_performance=="","manual takeover failed");await snap("lifecycle_manual")
        command({"release_performance":true});require(rig.release_time==0,"release did not start");await snap("lifecycle_release_start")
        advance(.1);await snap("lifecycle_release_middle")
        advance(1.0);require(rig.pose_now()==rig.neutral_pose(),"release did not restore neutral");await snap("lifecycle_release_end")
        manual(1,Vector2(-1,-1));command({"reset":true});require(rig.face.gaze==Vector2.ZERO and rig.face.closure==Vector2.ZERO,"reset failed");await snap("lifecycle_reset_reopen")
    var file=FileAccess.open(out+"/controls.json",FileAccess.WRITE);file.store_string(JSON.stringify(records));file.close()
    print("GAZE_RENDER_CAPTURE_PASS frames=",records.size()," native=",native," baseline=",baseline," full=",full);quit()

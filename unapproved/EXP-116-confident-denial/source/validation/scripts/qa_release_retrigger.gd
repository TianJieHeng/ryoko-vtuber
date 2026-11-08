extends SceneTree
var stage
var out=""
var records=[]
func _initialize():call_deferred("run")
func frame(path:String):
    await process_frame
    await RenderingServer.frame_post_draw
    root.get_texture().get_image().save_png(out+"/"+path+".png")
func run():
    for arg in OS.get_cmdline_user_args():
        if arg.begins_with("--capture-dir="):out=arg.trim_prefix("--capture-dir=")
    DirAccess.make_dir_recursive_absolute(out+"/frames")
    stage=load("res://yawn_stage.tscn").instantiate();root.add_child(stage)
    stage.set_process(false);stage.primary.set_process(false)
    stage.apply_controls({"reset":true})
    await frame("initial")
    for i in range(341):
        var event=""
        if i in [0,90,140]:event="trigger"
        if i==55:event="release"
        if event!="":
            await frame("event_%03d_before"%i)
            var ok=stage.apply_controls({"release_performance":true} if event=="release" else {"perform_expression":"EXP-163"})
            assert(ok)
            await frame("event_%03d_after"%i)
        stage.advance(1.0/30.0)
        stage.status.text="Independent release/retrigger check"
        records.append({"frame":i,"event":event,"pose":stage.primary.pose_now(),"phase":stage.primary.performance_phase})
        await frame("frames/frame_%04d"%i)
    var f=FileAccess.open(out+"/metadata.json",FileAccess.WRITE);f.store_string(JSON.stringify(records,"  "));f.close()
    print("RELEASE_RETRIGGER_CAPTURE_COMPLETE 341 frames");quit()

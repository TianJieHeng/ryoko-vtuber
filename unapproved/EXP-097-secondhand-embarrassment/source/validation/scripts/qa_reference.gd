extends SceneTree
var rig
var out=""
func _initialize():call_deferred("run")
func run():
    for arg in OS.get_cmdline_user_args():
        if arg.begins_with("--capture-dir="):out=arg.trim_prefix("--capture-dir=")
    DirAccess.make_dir_recursive_absolute(out)
    root.size=Vector2i(786,626);root.content_scale_size=Vector2i(786,626)
    rig=load("res://yawn_rig.tscn").instantiate();root.add_child(rig);await process_frame;rig.set_process(false)
    rig.hud.hide();rig.hint.hide();rig.pose_status.hide()
    rig.head.position=Vector2(-92.6296146,-73.57915221);rig.head.scale=Vector2(.79132826,.79132826)
    rig.body.position=rig.head.position;rig.body.scale=rig.head.scale
    rig.apply_controls({"mouth_open":1,"blink":1})
    await process_frame;await RenderingServer.frame_post_draw
    root.get_texture().get_image().save_png(out+"/reference_matched_manual_max.png")
    rig.apply_controls({"reset":true});rig.apply_controls({"perform_expression":"EXP-163"});rig._process(2.2)
    await process_frame;await RenderingServer.frame_post_draw
    root.get_texture().get_image().save_png(out+"/reference_matched_yawn_peak.png")
    quit()

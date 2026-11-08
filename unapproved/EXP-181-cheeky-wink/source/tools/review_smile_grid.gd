extends SceneTree
var rig
var out=""
func _initialize():call_deferred("run")
func shot(name:String):
    await process_frame
    await RenderingServer.frame_post_draw
    root.get_texture().get_image().save_png(out+"/"+name+".png")
func run():
    for arg in OS.get_cmdline_user_args():
        if arg.begins_with("--output="):out=arg.trim_prefix("--output=")
    if out.is_empty():quit(2);return
    DirAccess.make_dir_recursive_absolute(out)
    root.size=Vector2i(1136,1100)
    rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
    rig.head.position=Vector2(0,-150);rig.head.scale=Vector2.ONE;rig.body.position=Vector2(0,-150);rig.body.scale=Vector2.ONE
    rig.hud.hide();rig.hint.hide();rig.pose_status.hide()
    await process_frame
    for i in range(11):
        var a=i/10.0;rig.apply_controls({"reset":true,"eye_smile_R":a,"eye_smile_L":a,"mouth_smile":a,"mouth_open":a})
        await shot("combined_%02d"%i)
    for i in range(11):
        var a=i/10.0;rig.apply_controls({"reset":true,"mouth_smile":1.0,"mouth_open":a})
        await shot("mouth_%02d"%i)
    for i in range(11):
        var a=i/10.0;rig.apply_controls({"reset":true,"eye_smile_R":a,"eye_smile_L":a})
        await shot("eyes_%02d"%i)
    for o in [.5,1.0]:
        for i in range(11):
            var a=i/10.0;rig.apply_controls({"reset":true,"mouth_smile":a,"mouth_open":o})
            await shot("fraction_"+str(o)+"_%02d"%i)
    quit()

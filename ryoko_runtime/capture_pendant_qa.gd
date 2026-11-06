extends SceneTree
var output=""
var rig
func _initialize():call_deferred("run")
func capture(name):
    rig.hud.hide();rig.hint.hide();rig.pose_status.hide()
    await process_frame;await RenderingServer.frame_post_draw
    if root.get_texture().get_image().save_png(output+"/"+name+".png")!=OK:push_error("Pendant QA write failed");quit(1)
    print("PENDANT_QA ",JSON.stringify({"name":name,"angle":rig.pendant.angle,"visible":rig.pendant_pivot.visible,"enabled":rig.pendant.enabled,"pivot":[rig.pendant_pivot.position.x,rig.pendant_pivot.position.y]}))
func settle(count=120):
    for i in range(count):rig._process(1.0/30)
func reset():
    rig.apply_controls({"reset":true,"auto_blink":false,"body_follow":false,"pendant_secondary":true})
    settle(180)
func run():
    var args=OS.get_cmdline_user_args()
    if args.size()!=1:push_error("Expected QA output directory");quit(1);return
    output=args[0];DirAccess.make_dir_recursive_absolute(output)
    rig=load("res://motion_rig.tscn").instantiate();root.add_child(rig)
    await process_frame;rig.set_process(false)
    reset()
    await capture("neutral_on")
    rig.apply_controls({"pendant_secondary":false})
    await capture("neutral_off")
    rig.apply_controls({"pendant_secondary":true})
    for pair in [["limit_minus",-10.0],["limit_plus",10.0]]:
        rig.pendant.angle=deg_to_rad(pair[1]);rig._sync_pendant_render_state()
        await capture(pair[0])
    reset()
    rig.apply_controls({"head_tilt":0.9,"head_x":0.8,"head_y":0.7})
    settle()
    await capture("head_only")
    reset()
    rig.apply_controls({"body_tilt":0.8,"body_x":0.7,"bounce":true})
    settle(8)
    await capture("bounce")
    reset()
    rig.apply_controls({"body_tilt":-0.8,"breath_level":1.0,"expression":"EXP-064","mouth":"E","effects":{"blush_L":true,"sparkle":true}})
    settle(90)
    await capture("combined_breath")
    rig.apply_controls({"pendant_secondary":false})
    await capture("combined_off")
    print("PENDANT_QA_COMPLETE");quit()

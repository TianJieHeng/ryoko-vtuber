extends SceneTree
func _initialize():call_deferred("run")
func capture(rig,name):
    rig.hud.text="RYOKO / EXISTING-EXPRESSION GAZE CHECK"
    rig.hint.text="Same pose and original expression"
    rig.pose_status.text=""
    for i in range(3):await process_frame
    await RenderingServer.frame_post_draw
    root.get_texture().get_image().save_png("user://"+name+".png")
func run():
    var rig=load("res://motion_rig.tscn").instantiate();root.add_child(rig);await process_frame;rig.set_process(false)
    for id in ["EXP-064","EXP-189"]:
        rig.apply_controls({"reset":true,"auto_blink":false,"body_follow":false,"expression":id})
        rig.clock_time=0;rig._process(0)
        rig.skin_material.set_shader_parameter("gaze_open",Vector2.ZERO);await capture(rig,id+"_original")
        rig.skin_material.set_shader_parameter("gaze_open",Vector2.ONE);await capture(rig,id+"_center")
        for direction in ["left","right","up","down"]:
            rig.gaze.current=Vector2(-1,0) if direction=="left" else (Vector2(1,0) if direction=="right" else (Vector2(0,-1) if direction=="up" else Vector2(0,1)))
            rig._process(0);await capture(rig,id+"_"+direction)
        rig.apply_controls({"eye_screen_left":1,"mouth":"A"});rig._process(.1)
        await capture(rig,id+"_blink_mouth")
    rig.apply_controls({"reset":true,"auto_blink":false,"expression":"EXP-041"});rig.clock_time=0;rig._process(0)
    await capture(rig,"unsupported_center")
    rig.gaze.current=Vector2(1,-1);rig._process(0);await capture(rig,"unsupported_gaze")
    print("EXPRESSION_GAZE_GPU_QA_CAPTURED");quit()

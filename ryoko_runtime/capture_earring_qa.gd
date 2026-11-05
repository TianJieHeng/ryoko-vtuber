extends SceneTree
func _initialize():call_deferred("run")
func capture(rig,name):
    rig.hud.text="RYOKO / EARRING COMPOSITION CHECK"
    rig.hint.text="Same pose, source versus rigid pendants"
    rig.pose_status.text=""
    for i in range(3):await process_frame
    await RenderingServer.frame_post_draw
    root.get_texture().get_image().save_png("user://"+name+".png")
func run():
    var rig=load("res://motion_rig.tscn").instantiate();root.add_child(rig);await process_frame;rig.set_process(false)
    rig.apply_controls({"reset":true,"auto_blink":false,"body_follow":false,"earring_secondary":false})
    rig.clock_time=0;rig._process(0);await capture(rig,"earring_neutral_off")
    rig.apply_controls({"earring_secondary":true});rig._process(0);await capture(rig,"earring_neutral_on")
    rig.apply_controls({"head_tilt":1,"body_tilt":1,"head_x":.6})
    for i in range(180):rig._process(1.0/30)
    await capture(rig,"earring_held_max_tilt")
    rig.apply_controls({"head_tilt":-1,"body_tilt":-1,"head_x":-.6})
    for i in range(7):rig._process(1.0/30)
    await capture(rig,"earring_reversal")
    rig.apply_controls({"expression":rig.expression_ids[0],"mouth":"A","eye_screen_left":1})
    rig._process(.1);await capture(rig,"earring_expression_blink")
    print("EARRING_GPU_QA_CAPTURED");quit()

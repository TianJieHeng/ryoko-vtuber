extends SceneTree
func _initialize():call_deferred("run")
func capture(rig,name):
    rig.hud.text="RYOKO / INTEGRATED BUST RIG"
    rig.hint.text=name.replace("_"," ")
    for i in range(3):await process_frame
    await RenderingServer.frame_post_draw
    var image=root.get_texture().get_image()
    image.save_png("user://"+name+".png")
func run():
    var rig=load("res://motion_rig.tscn").instantiate();root.add_child(rig)
    await process_frame;rig.set_process(false)
    rig.apply_controls({"reset":true,"auto_blink":false,"body_follow":false})
    rig.clock_time=0;rig._process(0)
    await capture(rig,"integrated_neutral")
    rig.apply_controls({"look_x":.9,"look_y":-.3,"brow_screen_left":1,"brow_screen_right":-.5,"breath_level":1,"ornament_secondary":true,"mouth":"A","body_tilt":-.4})
    for i in range(120):rig._process(1.0/60)
    await capture(rig,"integrated_combined")
    rig.apply_controls({"expression":rig.expression_ids[0]})
    rig._process(.1)
    await capture(rig,"integrated_expression_fallback")
    rig.apply_controls({"expression":"neutral","eye_screen_left":1,"eye_screen_right":1})
    for i in range(30):rig._process(1.0/60)
    await capture(rig,"integrated_blink")
    rig.apply_controls({"reset":true,"auto_blink":false,"body_follow":false})
    for i in range(120):rig._process(1.0/60)
    await capture(rig,"integrated_reset")
    print("INTEGRATED_GPU_QA_CAPTURED")
    quit()

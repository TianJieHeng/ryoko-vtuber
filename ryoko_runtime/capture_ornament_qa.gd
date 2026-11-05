extends SceneTree
func _initialize():call_deferred("run")
func capture(rig,name):
    for i in range(3):await process_frame
    await RenderingServer.frame_post_draw
    var image=root.get_texture().get_image()
    image.save_png("user://"+name+".png")
func run():
    var rig=load("res://motion_rig.tscn").instantiate();root.add_child(rig)
    await process_frame;rig.set_process(false)
    rig.apply_controls({"reset":true,"auto_blink":false,"body_follow":false})
    rig.clock_time=0;rig._process(0)
    rig.hud.text="RYOKO / ORNAMENT RENDER CHECK"
    rig.hint.text="Identical pose / original source versus rigid ornament"
    rig.ornament.enabled=false;rig._process(0)
    await capture(rig,"ornament_disabled")
    rig.ornament.enabled=true;rig._process(0)
    await capture(rig,"ornament_enabled")
    rig.apply_controls({"head_tilt":.9,"body_tilt":.8,"head_x":.6})
    for i in range(150):rig._process(1.0/30)
    await capture(rig,"ornament_held_tilt")
    rig.apply_controls({"head_tilt":-.9,"body_tilt":-.8,"head_x":-.6})
    for i in range(5):rig._process(1.0/30)
    await capture(rig,"ornament_reversal")
    print("ORNAMENT_GPU_QA_CAPTURED")
    quit()

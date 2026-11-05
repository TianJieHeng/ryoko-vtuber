extends SceneTree
func _initialize():call_deferred("run")
func capture(rig,name):
    rig.hud.text="RYOKO / LOWER HAIR COMPOSITION CHECK"
    rig.hint.text="Same frozen pose and expression"
    rig.pose_status.text=""
    for i in range(3):await process_frame
    await RenderingServer.frame_post_draw
    root.get_texture().get_image().save_png("user://"+name+".png")
func run():
    var rig=load("res://motion_rig.tscn").instantiate();root.add_child(rig);await process_frame;rig.set_process(false)
    rig.apply_controls({"reset":true,"auto_blink":false,"body_follow":false,"loose_hair_secondary":false})
    rig.clock_time=0;rig._process(0);await capture(rig,"loose_hair_neutral_off")
    rig.apply_controls({"loose_hair_secondary":true});rig._process(0);await capture(rig,"loose_hair_neutral_on")
    rig.apply_controls({"head_tilt":1,"head_x":.5,"body_tilt":.4})
    for i in range(120):rig._process(1.0/30)
    rig.apply_controls({"head_tilt":-1,"head_x":-.5,"body_tilt":-.4})
    for i in range(5):rig._process(1.0/30)
    await capture(rig,"loose_hair_reversal_on")
    var left=rig.skin_material.get_shader_parameter("loose_hair_left");var right=rig.skin_material.get_shader_parameter("loose_hair_right")
    rig.skin_material.set_shader_parameter("loose_hair_left",Vector2.ZERO);rig.skin_material.set_shader_parameter("loose_hair_right",Vector2.ZERO)
    await capture(rig,"loose_hair_reversal_off")
    RenderingServer.set_default_clear_color(Color(.94,.94,.94,1))
    await capture(rig,"loose_hair_light_off")
    rig.skin_material.set_shader_parameter("loose_hair_left",left);rig.skin_material.set_shader_parameter("loose_hair_right",right)
    await capture(rig,"loose_hair_light_on")
    RenderingServer.set_default_clear_color(Color(.12,.13,.14,1))
    rig.apply_controls({"expression":"EXP-041","mouth":"A","eye_screen_left":1});rig._process(1.0/30)
    await capture(rig,"loose_hair_expression_blink")
    print("LOOSE_HAIR_GPU_QA_CAPTURED");quit()

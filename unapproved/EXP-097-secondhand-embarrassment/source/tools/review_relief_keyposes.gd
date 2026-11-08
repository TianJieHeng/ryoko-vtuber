extends SceneTree
var rig
var out=""
func _initialize():call_deferred("run")
func capture(path):
 rig._write_pose()
 await process_frame;await RenderingServer.frame_post_draw
 root.get_texture().get_image().save_png(path)
func run():
 for arg in OS.get_cmdline_user_args():
  if arg.begins_with("--output="):out=arg.trim_prefix("--output=")
 if out.is_empty():quit(2);return
 DirAccess.make_dir_recursive_absolute(out)
 root.size=Vector2i(1136,1384)
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 if not rig.rig_ready or not rig.registry_ready:push_error(rig.last_error);quit(2);return
 rig.hud.hide();rig.hint.hide();rig.pose_status.hide()
 rig.head.position=Vector2.ZERO;rig.body.position=Vector2.ZERO;rig.head.scale=Vector2.ONE;rig.body.scale=Vector2.ONE
 for t in [0.0,.25,.55,.9,1.3,1.65,2.1,2.65,3.2]:
  rig.reset();rig.play_expression("EXP-007");rig.advance(t)
  await capture(out+"/native_%04d.png"%int(round(t*100)))
 print("RELIEF_KEYPOSES_PASS");quit(0)

extends SceneTree
var rig
var out=""
var rows=[]
func _initialize():call_deferred("run")
func run():
 for arg in OS.get_cmdline_user_args():
  if arg.begins_with("--output="):out=arg.trim_prefix("--output=")
 if out.is_empty():quit(2);return
 DirAccess.make_dir_recursive_absolute(out)
 root.size=Vector2i(1136,1384)
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 if not rig.rig_ready or not rig.registry_ready:quit(2);return
 rig.hud.hide();rig.hint.hide();rig.pose_status.hide()
 rig.head.position=Vector2.ZERO;rig.body.position=Vector2.ZERO;rig.head.scale=Vector2.ONE;rig.body.scale=Vector2.ONE
 for pair in [[.18,.42],[.24,.60],[.30,.65],[.35,.70],[.40,.80]]:
  for eyes in [.045,.90]:
   rig.reset();rig.apply_controls({"mouth_smile":pair[0],"mouth_corner_lift":pair[1],"eye_smile_R":eyes,"eye_smile_L":eyes,"brow_screen_left":.08,"brow_screen_right":.08,"brow_tilt_screen_left":-.12,"brow_tilt_screen_right":.12});rig._write_pose()
   await process_frame;await RenderingServer.frame_post_draw
   var name="smile_%03d_corner_%03d_eyes_%03d.png"%[roundi(pair[0]*100),roundi(pair[1]*100),roundi(eyes*1000)]
   root.get_texture().get_image().save_png(out+"/"+name)
   rows.append({"name":name,"pose":rig.pose_now(),"face":rig.face.snapshot()})
 var f=FileAccess.open(out+"/states.json",FileAccess.WRITE);f.store_string(JSON.stringify(rows,"  "));f.close();print("AFFECTION_MOUTH_PROBE_PASS");quit(0)

extends SceneTree
var rig
var out=""
var records=[]
func _initialize():call_deferred("run")
func capture(label):
 rig._write_pose()
 await process_frame;await RenderingServer.frame_post_draw
 var im=root.get_texture().get_image();im.save_png(out+"/"+label+".png")
 var hash=HashingContext.new();hash.start(HashingContext.HASH_SHA256);hash.update(im.get_data())
 records.append({"label":label,"sha256":hash.finish().hex_encode(),"state":rig.get_state(),"face":rig.face.snapshot()})
func run():
 for arg in OS.get_cmdline_user_args():
  if arg.begins_with("--output="):out=arg.trim_prefix("--output=")
 DirAccess.make_dir_recursive_absolute(out)
 root.size=Vector2i(1136,1384)
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 if not rig.rig_ready or not rig.registry_ready:push_error(rig.last_error);quit(2);return
 rig.hud.hide();rig.hint.hide();rig.pose_status.hide()
 rig.head.position=Vector2.ZERO;rig.body.position=Vector2.ZERO;rig.head.scale=Vector2.ONE;rig.body.scale=Vector2.ONE
 rig.reset();await capture("neutral")
 for source in ["EXP-003","EXP-005"]:
  for action in ["release","retrigger","handoff","manual","reset"]:
   var label=source+"_"+action
   rig.reset();rig.play_expression(source);rig.advance(.9 if source=="EXP-003" else 1.5);await capture(label+"_before")
   if action=="release":rig.release()
   elif action=="retrigger":rig.play_expression(source)
   elif action=="handoff":rig.play_expression("EXP-005" if source=="EXP-003" else "EXP-003")
   elif action=="manual":rig.apply_controls({"eye_smile_R":.35,"eye_smile_L":.15,"mouth_corner_lift":.1})
   else:rig.reset()
   await capture(label+"_at")
   for step in range(10):rig.advance(.05);await capture(label+"_%02d"%step)
   if action=="manual":rig.reset()
   else:rig.advance(10)
   await capture(label+"_end")
 var f=FileAccess.open(out+"/evidence.json",FileAccess.WRITE);f.store_string(JSON.stringify({"frames":records,"normal_speed_playback":false},"  "));f.close()
 print("CONTENTMENT_LIFECYCLE_CAPTURE_PASS frames=",records.size());quit(0)

extends SceneTree
var rig
var out=""
var records=[]
func _initialize():call_deferred("run")
func run():
 for arg in OS.get_cmdline_user_args():
  if arg.begins_with("--output="):out=arg.trim_prefix("--output=")
 DirAccess.make_dir_recursive_absolute(out)
 root.size=Vector2i(1136,1384)
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 if not rig.rig_ready or not rig.registry_ready:push_error(rig.last_error);quit(2);return
 rig.hud.hide();rig.hint.hide();rig.pose_status.hide()
 rig.head.position=Vector2.ZERO;rig.body.position=Vector2.ZERO;rig.head.scale=Vector2.ONE;rig.body.scale=Vector2.ONE
 var original=rig.registry.definition("EXP-003")
 for value in [.30,.32,.34,.36]:
  var definition=original.duplicate(true)
  definition.keyframes[3].values.eye_smile_R=value;definition.keyframes[3].values.eye_smile_L=value
  rig.registry._entries["EXP-003"].definition=definition
  for t in [.50,.55,.60,.65,.70,.75]:
   rig.reset();rig.play_expression("EXP-003");rig.advance(t);rig._write_pose()
   await process_frame;await RenderingServer.frame_post_draw
   var name="eye_%03d_t%04d"%[roundi(value*100),roundi(t*1000)]
   root.get_texture().get_image().save_png(out+"/"+name+".png")
   records.append({"name":name,"value_at_kp4":value,"time":t,"state":rig.get_state(),"face":rig.face.snapshot()})
 var f=FileAccess.open(out+"/states.json",FileAccess.WRITE);f.store_string(JSON.stringify(records,"  "));f.close()
 print("CONTENTMENT_KP4_PROBE_PASS");quit(0)

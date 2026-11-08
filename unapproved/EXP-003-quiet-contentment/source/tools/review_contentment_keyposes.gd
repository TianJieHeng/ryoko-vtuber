extends SceneTree
var rig
var out=""
var states=[]
func _initialize():call_deferred("run")
func capture(t,kind):
 rig.reset();rig.play_expression("EXP-003");rig.advance(t);rig._write_pose()
 await process_frame;await RenderingServer.frame_post_draw
 var name=kind+"_%04d.png"%roundi(t*1000)
 root.get_texture().get_image().save_png(out+"/"+name)
 states.append({"name":name,"time":t,"pose":rig.pose_now(),"state":rig.get_state(),"face":rig.face.snapshot()})
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
 for t in [0.0,.15,.30,.50,.75,1.05,1.35,1.65,1.9]:await capture(t,"key")
 for t in [.32,.34,.36,.38,.40,.42,.44,.46,.48,1.08,1.11,1.14,1.17,1.20,1.23,1.26,1.29,1.32]:await capture(t,"transition")
 var f=FileAccess.open(out+"/states.json",FileAccess.WRITE);f.store_string(JSON.stringify(states,"  "));f.close()
 print("CONTENTMENT_KEYPOSES_PASS");quit(0)

extends SceneTree
var rig
var out=""
var states=[]
func _initialize():call_deferred("run")
func capture(name, controls):
 rig.apply_controls({"reset":true,"auto_blink":false})
 if not rig.apply_controls(controls):push_error(rig.last_error);quit(2);return
 rig._write_pose()
 await process_frame;await RenderingServer.frame_post_draw
 root.get_texture().get_image().save_png(out+"/"+name+".png")
 states.append({"name":name,"controls":controls,"pose":rig.pose_now(),"face":rig.face.snapshot()})
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
 await capture("neutral",{})
 for a in [0.0,.15,.3,.4,.5,.55,.6,.65,.7,.75,.8,.85,.9,.95,1.0]:
  await capture("smile_%03d"%roundi(a*100),{"eye_smile_R":a,"eye_smile_L":a,"mouth_corner_lift":.16,"mouth_purse":.22})
 for a in [.15,.30,.50,.70,1.0]:
  await capture("blink_%03d"%roundi(a*100),{"blink":a,"mouth_corner_lift":.16,"mouth_purse":.22})
 var f=FileAccess.open(out+"/states.json",FileAccess.WRITE);f.store_string(JSON.stringify(states,"  "));f.close()
 print("CONTENTMENT_CAPABILITY_PASS");quit(0)

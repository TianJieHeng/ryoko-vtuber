extends SceneTree
var rig
var out=""
var states=[]
var failures=[]
var checks=0
var lid_probe=false
func _initialize():call_deferred("run")
func check(ok,label):
 checks+=1
 if not ok:failures.append(label);push_error(label)
func capture(t,kind,lid=-1.0):
 rig.reset();check(rig.play_expression("EXP-152"),"play");check(rig.advance(t),"advance");
 if lid>=0:check(rig.apply_controls({"blink":lid}),"manual lid diagnostic")
 rig._write_pose()
 var pose=rig.pose_now()
 check(pose.eye_smile_R==0 and pose.eye_smile_L==0,"ordinary eyes")
 check(pose.mouth_open==0 and pose.mouth_purse==0 and pose.mouth_oral_lift==0,"sealed mouth")
 check(pose.gaze_x==0 and pose.blush_intensity==0 and pose.hair_sway==0,"quiet acting")
 check(rig.face.gaze_down_extra==pose.gaze_down_extra,"actual extra")
 var offset=rig.Limits.gaze_pixels(Vector2(pose.gaze_x,pose.gaze_y),pose.gaze_down_extra)
 for side in ["screen_left","screen_right"]:
  var key="iris_"+side
  check(rig.face.homes[key].node.position.is_equal_approx(rig.face.homes[key].pivot+offset),"actual rigid iris offset")
  check(rig.face.objects[key].material.get_shader_parameter("rigid_gaze").is_equal_approx(offset),"actual shader offset")
 await process_frame;await RenderingServer.frame_post_draw
 var name=kind+"_%04d.png"%roundi((lid if lid>=0 else t)*1000)
 check(root.get_texture().get_image().save_png(out+"/"+name)==OK,"save")
 states.append({"name":name,"time":t,"pose":pose,"state":rig.get_state(),"face":rig.face.snapshot(),"source_iris_offset":[offset.x,offset.y],"viewer_scale":rig.head.scale.x})
func run():
 for arg in OS.get_cmdline_user_args():
  if arg.begins_with("--output="):out=arg.trim_prefix("--output=")
  if arg=="--lid-probe":lid_probe=true
 if out.is_empty():quit(2);return
 DirAccess.make_dir_recursive_absolute(out)
 root.size=Vector2i(568,800)
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 if not rig.rig_ready or not rig.registry_ready:push_error(rig.last_error);quit(2);return
 rig.hud.hide();rig.hint.hide();rig.pose_status.hide()
 if lid_probe:
  for lid in [.22,.32,.42]:await capture(.75,"full_lid",lid)
 else:
  for t in [0.0,.15,.30,.50,.75,1.05,1.35,1.65,1.9]:await capture(t,"full")
 root.size=Vector2i(1136,1384);rig.head.position=Vector2.ZERO;rig.body.position=Vector2.ZERO;rig.head.scale=Vector2.ONE;rig.body.scale=Vector2.ONE
 if lid_probe:
  for lid in [.22,.32,.42]:await capture(.75,"native_lid",lid)
 else:
  for t in [0.0,.15,.30,.50,.75,1.05,1.35,1.65,1.9]:await capture(t,"native")
 var f=FileAccess.open(out+"/states.json",FileAccess.WRITE);f.store_string(JSON.stringify({"states":states,"checks":checks,"failures":failures},"  "));f.close()
 print("PRIVATE_PRIDE_KEYPOSES_", "PASS" if failures.is_empty() else "FAIL"," checks=",checks," failures=",failures.size());quit(0 if failures.is_empty() else 1)

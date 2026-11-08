extends SceneTree
var rig
var out=""
func _initialize():call_deferred("run")
func require(ok:bool,s:String):
 if not ok:push_error(s);quit(2);assert(false,s)
func snap(label:String):
 await process_frame
 await RenderingServer.frame_post_draw
 require(root.get_texture().get_image().save_png(out+"/"+label+".png")==OK,"save")
func run():
 for arg in OS.get_cmdline_user_args():
  if arg.begins_with("--output="):out=arg.trim_prefix("--output=")
 require(not out.is_empty(),"output required");DirAccess.make_dir_recursive_absolute(out)
 root.size=Vector2i(1136,1384)
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 rig.hud.hide();rig.hint.hide();rig.pose_status.hide()
 rig.body.position=Vector2.ZERO;rig.body.scale=Vector2.ONE;rig.head.position=Vector2.ZERO;rig.head.scale=Vector2.ONE
 await process_frame
 require(rig.apply_controls({"blink":0.7128896,"gaze_x":-0.904827,"gaze_y":-0.425779,"hair_sway":-0.063338}),"pose rejected")
 await snap("reported_all")
 for prefix in ["upper_lash_","closed_lash_","lower_contour_","upper_surround_","hair_","iris_","sclera_"]:
  for key in rig.face.objects:
   if key.begins_with(prefix):rig.face.objects[key].hide()
  await snap("reported_hide_"+prefix)
  for key in rig.face.objects:
   if key.begins_with(prefix):rig.face.objects[key].show()
 for value in [0.0,.05,.1,.25,.5,.55,.6,.625,.65,.675,.7,.7128896,.725,.75,.775,.8,.825,.85,.875,.9,.95,1.0]:
  require(rig.apply_controls({"blink":value,"hair_sway":0.0,"gaze_x":0.0,"gaze_y":0.0}),"sweep rejected")
  await snap("lid_%05d"%roundi(value*10000))
 require(rig.apply_controls({"reset":true}),"reset")
 for key in rig.face.objects:
  if key.begins_with("hair_"):rig.face.objects[key].hide()
 await snap("neutral_hide_hair")
 print("REPORTED_TRANSITION_CAPTURE_PASS");quit()

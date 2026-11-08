extends SceneTree
var rig
var out=""
var rows=[]
const IDS=["EXP-163","EXP-005","EXP-001","EXP-006","EXP-107","EXP-007","EXP-002","EXP-152","EXP-160"]
func _initialize():call_deferred("run")
func capture(label):
 rig._write_pose()
 await process_frame;await RenderingServer.frame_post_draw
 var im=root.get_texture().get_image();im.save_png(out+"/frame_%03d.png"%rows.size())
 var hash=HashingContext.new();hash.start(HashingContext.HASH_SHA256);hash.update(im.get_data())
 rows.append({"label":label,"sha256":hash.finish().hex_encode(),"state":rig.get_state(),"face":rig.face.snapshot()})
func run():
 for a in OS.get_cmdline_user_args():
  if a.begins_with("--output="):out=a.trim_prefix("--output=")
 DirAccess.make_dir_recursive_absolute(out)
 root.size=Vector2i(1136,1384)
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 if not rig.rig_ready or not rig.registry_ready:push_error(rig.last_error);quit(2);return
 rig.hud.hide();rig.hint.hide();rig.pose_status.hide()
 rig.head.position=Vector2.ZERO;rig.body.position=Vector2.ZERO;rig.head.scale=Vector2.ONE;rig.body.scale=Vector2.ONE
 for id in IDS:
  var d=rig.registry.definition(id);var count=d.keyframes.size()
  for index in [0,int((count-1)/3),int(2*(count-1)/3),count-2]:
   var t=d.keyframes[index].time;rig.reset();rig.play_expression(id);rig.advance(t)
   await capture(id+"_key_%02d_t_%04d"%[index,int(round(t*1000))])
 var controls=[
  {"gaze_x":-1.0,"gaze_y":1.0,"gaze_down_extra":1.0},
  {"gaze_x":1.0,"gaze_y":1.0,"gaze_down_extra":1.0},
  {"gaze_x":0.0,"gaze_y":1.0,"gaze_down_extra":.6,"blink_L":.4,"blink_R":.4},
  {"gaze_x":0.0,"gaze_y":-1.0,"gaze_down_extra":0.0},
  {"brow_inner_lift_screen_left":1.0,"brow_inner_lift_screen_right":0.0,"brow_tilt_screen_left":-1.0},
  {"brow_inner_lift_screen_left":0.0,"brow_inner_lift_screen_right":1.0,"brow_tilt_screen_right":1.0},
  {"brow_inner_lift_screen_left":1.0,"brow_inner_lift_screen_right":1.0,"brow_tilt_screen_left":-1.0,"brow_tilt_screen_right":1.0},
  {"mouth_open":.4,"mouth_smile":.5,"mouth_purse":.3,"mouth_oral_lift":.6},
  {"mouth_open":.6,"mouth_smile":.9,"mouth_spread":.8,"mouth_corner_lift":.4}]
 for i in range(controls.size()):
  rig.reset();rig.apply_controls(controls[i]);await capture("manual_%02d"%i)
 for t in [3.9,4.03,4.2]:
  rig.reset();rig.apply_controls({"auto_blink":true});rig.advance(t);await capture("idle_blink_%04d"%int(round(t*1000)))
 var f=FileAccess.open(out+"/evidence.json",FileAccess.WRITE);f.store_string(JSON.stringify({"frames":rows,"fresh_current_main_sanity":true,"normal_speed_observed":false},"  "));f.close()
 print("MEDITATIVE_CURRENT_MAIN_SANITY_PASS frames=",rows.size());quit(0)

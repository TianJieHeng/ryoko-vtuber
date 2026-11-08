extends SceneTree
var rig
var out=""
var records=[]
var checks=0
var failures=[]
func _initialize():call_deferred("run")
func check(ok,label):
 checks+=1
 if not ok:failures.append(label)
func capture(label):
 check(rig.head.position==Vector2.ZERO and rig.body.position==Vector2.ZERO and rig.head.scale==Vector2.ONE and rig.body.scale==Vector2.ONE,"fixed native registration "+label)
 if rig.active_performance=="EXP-177" and rig.performance_time>=.3:
  for k in rig.CHANNELS:
   if k not in ["blink_R","blink_L"]:check(rig.pose_now()[k]==0,"177 zero default "+k+" "+label)
  if rig.performance_time>=1.2 and rig.performance_time<=2.35:check(rig.face.closure==Vector2.ONE,"actual long closure "+label)
 if label.ends_with("_end") or label in ["neutral","restored_open"]:
  check(rig.pose_now()==rig.neutral_pose() and rig.active_performance=="" and rig.release_time<0,"exact recovered neutral "+label)
 for key in rig.face.objects:
  var n=rig.face.objects[key];check(n.scale==Vector2.ONE and rig.face.homes[key].node.scale==Vector2.ONE and n.modulate.a==1,"rigid opaque "+label)
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
 for source in ["EXP-177","EXP-005"]:
  for action in ["release","repeat_release","retrigger","release_retrigger","handoff","manual","reset","disable"]:
   var label=source+"_"+action
   rig.reset();rig.apply_controls({"auto_blink":true});rig.play_expression(source);rig.advance(1.75 if source=="EXP-177" else 1.5);await capture(label+"_before")
   if action=="release":rig.release()
   elif action=="repeat_release":rig.release();rig.advance(.2);await capture(label+"_first_release");rig.release()
   elif action=="release_retrigger":rig.release();rig.advance(.2);await capture(label+"_first_release");rig.play_expression(source)
   elif action=="disable":rig.apply_controls({"auto_blink":false});rig.release()
   elif action=="retrigger":rig.play_expression(source)
   elif action=="handoff":rig.play_expression("EXP-005" if source=="EXP-177" else "EXP-177")
   elif action=="manual":rig.apply_controls({"eye_smile_R":.35,"eye_smile_L":.15,"mouth_corner_lift":.1})
   else:rig.reset()
   await capture(label+"_at")
   for step in range(10):rig.advance(.05);await capture(label+"_%02d"%step)
   if action=="manual":rig.reset()
   else:rig.advance(10)
   await capture(label+"_end")
 for t in [.4,.85,2.85,3.35]:
  for action in ["release","retrigger"]:
   var label="partial_%04d_%s"%[int(round(t*1000)),action]
   rig.reset();rig.apply_controls({"auto_blink":true});rig.play_expression("EXP-177");rig.advance(t);await capture(label+"_before")
   if action=="release":rig.release()
   else:rig.play_expression("EXP-177")
   await capture(label+"_at")
   for dt in [.05,.1,.15,.15]:rig.advance(dt);await capture(label+"_step_%04d"%int(round((rig.release_time if action=="release" else rig.performance_time)*1000)))
   rig.advance(10);await capture(label+"_end")
 for prior in ["EXP-152","EXP-160"]:
  for direction in ["incoming","outgoing"]:
   var label=prior+"_"+direction
   rig.reset();rig.apply_controls({"auto_blink":true});rig.play_expression(prior if direction=="incoming" else "EXP-177")
   rig.advance((.75 if prior=="EXP-152" else 1.35) if direction=="incoming" else 1.75);await capture(label+"_before")
   rig.play_expression("EXP-177" if direction=="incoming" else prior);await capture(label+"_at")
   for dt in [.05,.1,.15,.3,.6,.55]:rig.advance(dt);await capture(label+"_step_%04d"%int(round(rig.performance_time*1000)))
   rig.advance(10);await capture(label+"_end")
 rig.reset();rig.apply_controls({"auto_blink":true});rig.play_expression("EXP-177");rig.advance(1.75);await capture("new_controls_manual_before")
 rig.apply_controls({"gaze_y":.6,"gaze_down_extra":.7,"brow_inner_lift_screen_left":.6,"brow_inner_lift_screen_right":.4});await capture("new_controls_manual_at")
 rig.advance(1);await capture("new_controls_manual_persist");rig.reset();await capture("new_controls_manual_end")
 rig.reset();rig.apply_controls({"auto_blink":true});rig.play_expression("EXP-177");rig.advance(3.9);await capture("restored_open")
 for step in range(130):rig.advance(1.0/30);await capture("restored_blink_%03d"%step)
 var f=FileAccess.open(out+"/evidence.json",FileAccess.WRITE);f.store_string(JSON.stringify({"frames":records,"checks":checks,"failures":failures,"normal_speed_playback":false},"  "));f.close()
 print("MEDITATIVE_LIFECYCLE_CAPTURE_", "PASS" if failures.is_empty() else "FAIL"," frames=",records.size()," checks=",checks," failures=",failures);quit(0 if failures.is_empty() else 1)

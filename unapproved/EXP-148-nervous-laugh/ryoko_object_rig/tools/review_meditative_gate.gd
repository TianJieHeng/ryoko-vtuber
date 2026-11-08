extends SceneTree
var rig
var out=""
var checks=0
var failures=[]
var rows=[]
var dense=false
func _initialize():call_deferred("run")
func check(ok,label):
 checks+=1
 if not ok:failures.append(label)
func capture(label):
 rig._write_pose()
 await process_frame;await RenderingServer.frame_post_draw
 var im=root.get_texture().get_image();im.save_png(out+"/"+label+".png")
 var hash=HashingContext.new();hash.start(HashingContext.HASH_SHA256);hash.update(im.get_data())
 rows.append({"label":label,"sha256":hash.finish().hex_encode(),"state":rig.get_state(),"face":rig.face.snapshot()})
func run():
 for a in OS.get_cmdline_user_args():
  if a.begins_with("--output="):out=a.trim_prefix("--output=")
  if a=="--dense":dense=true
 DirAccess.make_dir_recursive_absolute(out)
 root.size=Vector2i(1136,1384)
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 check(rig.rig_ready and rig.registry_ready,"ready")
 if not rig.rig_ready or not rig.registry_ready:quit(2);return
 rig.hud.hide();rig.hint.hide();rig.pose_status.hide()
 rig.head.position=Vector2.ZERO;rig.body.position=Vector2.ZERO;rig.head.scale=Vector2.ONE;rig.body.scale=Vector2.ONE
 var times=[0.0,.4866515881418201,.6400595242051585,1.2,1.75,2.35,2.85,3.35,3.9]
 for i in range(9):
  var t=times[i];rig.reset();rig.apply_controls(rig.sample_expression("EXP-177",t));await capture("static_%02d"%(i+1))
  var pose=rig.pose_now();rig.reset();rig.play_expression("EXP-177");rig.advance(t)
  check(rig.pose_now()==pose,"played equals static key");await capture("played_%02d"%(i+1))
 if dense:
  rig.reset();rig.play_expression("EXP-177")
  for i in range(73):
   if i>0:rig.advance(1.0/60)
   check(is_equal_approx(rig.performance_time,i/60.0),"actual incremental closing time")
   for key in rig.CHANNELS:
    if key not in ["blink_R","blink_L"]:check(rig.pose_now()[key]==0,"only ordinary lids "+key)
   await capture("closing_%03d"%i)
 var f=FileAccess.open(out+"/evidence.json",FileAccess.WRITE);f.store_string(JSON.stringify({"frames":rows,"checks":checks,"failures":failures,"normal_speed_observed":false},"  "));f.close()
 print("MEDITATIVE_GATE_", "PASS" if failures.is_empty() else "FAIL"," frames=",rows.size()," checks=",checks," failures=",failures);quit(0 if failures.is_empty() else 1)

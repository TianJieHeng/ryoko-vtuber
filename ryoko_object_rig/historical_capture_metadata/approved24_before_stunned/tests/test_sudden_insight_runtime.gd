extends SceneTree
var rig
var w="/tmp/ryoko_insight_integration"
var failures=[]
var checks=0
var records=[]
var visual=false
func _initialize():
 visual="--capture" in OS.get_cmdline_user_args()
 call_deferred("run")
func check(ok,label):
 checks+=1
 if not ok:failures.append(label)
func snap(path,detail):
 root.size=Vector2i(568,800);root.canvas_transform=Transform2D.IDENTITY
 if detail:
  root.size=Vector2i(400,360)
  var camera=Transform2D.IDENTITY.scaled(Vector2.ONE/.49);camera.origin=-Vector2(6,70)/.49-Vector2(380,380);root.canvas_transform=camera
 await process_frame;await process_frame;await RenderingServer.frame_post_draw
 var im=root.get_texture().get_image()
 check(im.save_png(path)==OK,"saved "+path)
 var ctx=HashingContext.new();ctx.start(HashingContext.HASH_SHA256);ctx.update(im.get_data());return ctx.finish().hex_encode()
func run():
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false);rig.auto_blink=false
 check(rig.rig_ready and rig.registry_ready,"ready");check(rig.list_expressions().size()==24,"approved24 registry")
 if not failures.is_empty():quit(1);return
 rig.hud.hide();rig.hint.hide();rig.pose_status.hide();rig.reset()
 var baseline=rig.face.snapshot();var head=rig.head.transform;var body=rig.body.transform
 check(rig.play_expression("EXP-125"),"play")
 if visual:
  DirAccess.make_dir_recursive_absolute(w+"/motion/full");DirAccess.make_dir_recursive_absolute(w+"/motion/detail")
 var first=[];var last=[]
 for i in range(109):
  if i>0:check(rig.advance(maxf(0.0,float(i)/30.0-rig.performance_time)),"advance "+str(i))
  var p=rig.pose_now()
  check(rig.Registry.scoped_valid(p),"scope "+str(i));check(rig.Registry.sealed_mouth_valid(p),"sealed "+str(i))
  check(rig.head.transform==head and rig.body.transform==body,"fixed body "+str(i))
  check(p.gaze_x==0 and p.gaze_y==0 and p.blush_intensity==0,"excluded controls "+str(i))
  var hashes=[]
  if visual:
   hashes.append(await snap(w+"/motion/full/%04d.png"%i,false));hashes.append(await snap(w+"/motion/detail/%04d.png"%i,true))
  if i==0:first=hashes
  if i==108:last=hashes
  records.append({"frame":i,"time":float(i)/30,"pose":p,"hashes":hashes})
 check(rig.face.snapshot()==baseline,"end exact object neutral")
 if visual:check(first==last,"end exact pixel neutral")
 for t in [.45,.95,1.45,2.35,3.1]:
  rig.reset();rig.play_expression("EXP-125");rig.advance(t)
  var before=rig.displayed_pose();rig.play_expression("EXP-125");check(rig.displayed_pose()==before,"restart continuous "+str(t))
  rig.advance(.4);before=rig.displayed_pose();rig.release();check(rig.displayed_pose()==before,"release continuous "+str(t))
  for j in range(16):rig.advance(1.0/30)
  check(rig.face.snapshot()==baseline,"release neutral "+str(t))
  rig.play_expression("EXP-125");rig.advance(t);rig.reset();check(rig.face.snapshot()==baseline,"reset neutral "+str(t))
 for entry in rig.list_expressions():
  for pair in [["EXP-125",entry.id],[entry.id,"EXP-125"]]:
   rig.reset();check(rig.play_expression(pair[0]),"handoff source");rig.advance(rig.performance.duration*.5)
   check(rig.play_expression(pair[1]),"handoff target")
   for step in range(11):
    rig.advance(.03);check(rig.Registry.scoped_valid(rig.pose_now()),"handoff composition");check(rig.Registry.sealed_mouth_valid(rig.pose_now()),"handoff mouth domain")
   rig.reset();check(rig.face.snapshot()==baseline,"handoff reset neutral")
 var result={"checks":checks,"failures":failures,"status":"PASS" if failures.is_empty() else "FAIL","frames":109,"fps":30,"duration":3.6,"visual_capture":visual,"renderer":RenderingServer.get_video_adapter_name(),"display":DisplayServer.get_name(),"records":records,"production_registry_tested":true,"normal_speed_observed":false}
 var f=FileAccess.open(w+("/motion_checks.json" if visual else "/motion_state_checks.json"),FileAccess.WRITE);f.store_string(JSON.stringify(result,"  "));f.close()
 print("MOTION_",result.status," checks=",checks," failures=",failures);quit(0 if failures.is_empty() else 1)

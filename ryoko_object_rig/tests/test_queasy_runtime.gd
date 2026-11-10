extends SceneTree
var rig
var w="res://validation/approved_batch36/regression_queasy_runtime"
var failures=[]
var checks=0
var records=[]
var visual=false
const ACTING_CHANNELS=["blink_L","blink_R","brow_screen_left","brow_screen_right","brow_inner_lift_screen_left","brow_inner_lift_screen_right","mouth_purse","mouth_lip_press"]
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
 check(rig.rig_ready and rig.registry_ready,"ready");check(rig.list_expressions().size()==36,"approved36 registry")
 if not failures.is_empty():quit(1);return
 rig.hud.hide();rig.hint.hide();rig.pose_status.hide();rig.reset()
 var baseline=rig.face.snapshot();var head=rig.head.transform;var body=rig.body.transform
 check(rig.play_expression("EXP-090"),"play")
 if visual:
  DirAccess.make_dir_recursive_absolute(w+"/motion/full");DirAccess.make_dir_recursive_absolute(w+"/motion/detail")
 var first=[];var last=[]
 for i in range(121):
  if i>0:check(rig.advance(maxf(0.0,float(i)/30.0-rig.performance_time)),"advance "+str(i))
  var p=rig.pose_now()
  check(rig.Registry.scoped_valid(p),"scope "+str(i));check(rig.Registry.sealed_mouth_valid(p),"sealed "+str(i))
  check(rig.head.transform==head and rig.body.transform==body,"fixed body "+str(i))
  for key in p:
   if key not in ACTING_CHANNELS:check(p[key]==0,"excluded "+key+" "+str(i))
  check(not rig.auto_blink,"no automatic blink "+str(i))
  var hashes=[]
  if visual:
   hashes.append(await snap(w+"/motion/full/%04d.png"%i,false));hashes.append(await snap(w+"/motion/detail/%04d.png"%i,true))
  if i==0:first=hashes
  if i==120:last=hashes
  records.append({"frame":i,"time":float(i)/30,"pose":p,"hashes":hashes})
 check(rig.face.snapshot()==baseline,"end exact object neutral")
 if visual:check(first==last,"end exact pixel neutral")
 for t in [.45,.85,1.5,2.7,3.5]:
  rig.reset();rig.play_expression("EXP-090");rig.advance(t)
  var before=rig.displayed_pose();rig.play_expression("EXP-090");check(rig.displayed_pose()==before,"restart continuous "+str(t))
  rig.advance(.4);before=rig.displayed_pose();rig.release();check(rig.displayed_pose()==before,"release continuous "+str(t))
  for j in range(16):rig.advance(1.0/30)
  check(rig.face.snapshot()==baseline,"release neutral "+str(t))
  rig.play_expression("EXP-090");rig.advance(t);rig.reset();check(rig.face.snapshot()==baseline,"reset neutral "+str(t))
 for alias in ["queasy"]:
  rig.reset();check(rig.play_expression(alias),"alias "+alias);check(rig.performance.id=="EXP-090","alias resolves "+alias)
 rig.reset();rig.play_expression("EXP-090");rig.advance(1.3);var frozen=rig.displayed_pose()
 for i in range(21):
  rig.advance(1.0/30);check(rig.displayed_pose()==frozen,"fixed queasy hold "+str(i))
 for entry in rig.list_expressions():
  for pair in [["EXP-090",entry.id],[entry.id,"EXP-090"]]:
   rig.reset();check(rig.play_expression(pair[0]),"handoff source");rig.advance(rig.performance.duration*.5)
   var before=rig.displayed_pose();check(rig.play_expression(pair[1]),"handoff target");check(rig.displayed_pose()==before,"handoff continuous")
   for step in range(11):
    rig.advance(.03);check(rig.Registry.scoped_valid(rig.pose_now()),"handoff composition "+str(pair)+" step "+str(step));check(rig.Registry.sealed_mouth_valid(rig.pose_now()),"handoff mouth domain "+str(pair)+" step "+str(step))
   rig.reset();check(rig.face.snapshot()==baseline,"handoff reset neutral")
 var result={"checks":checks,"failures":failures,"status":"PASS" if failures.is_empty() else "FAIL","approved_profile_count":36,"frames":121,"fps":30,"duration":4.0,"visual_capture":visual,"renderer":RenderingServer.get_video_adapter_name(),"display":DisplayServer.get_name(),"records":records,"production_registry_tested":true,"normal_speed_observed":false,"approval":"USER_APPROVED"}
 var f=FileAccess.open(w+("/motion_checks.json" if visual else "/motion_state_checks.json"),FileAccess.WRITE);f.store_string(JSON.stringify(result,"  "));f.close()
 print("MOTION_",result.status," checks=",checks," failures=",failures);quit(0 if failures.is_empty() else 1)

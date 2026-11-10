extends SceneTree
var rig
var w="res://validation/approved_mental_arithmetic"
var failures=[]
var checks=0
var records=[]
var visual=false
var BASELINE_COUNT=37
const ACTING_CHANNELS=["brow_screen_left","brow_screen_right","brow_tilt_screen_left","brow_tilt_screen_right","blink_L","blink_R","mouth_purse","gaze_y"]
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
 var expected=Vector2i(400,360) if detail else Vector2i(568,800)
 check(im.get_size()==expected,"native dimensions "+path+" expected="+str(expected)+" actual="+str(im.get_size()))
 if im.get_size()!=expected:return ""
 check(im.save_png(path)==OK,"saved "+path)
 var ctx=HashingContext.new();ctx.start(HashingContext.HASH_SHA256);ctx.update(im.get_data());return ctx.finish().hex_encode()
func run():
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false);rig.auto_blink=false
 check(rig.rig_ready and rig.registry_ready,"ready");check(rig.list_expressions().size()==BASELINE_COUNT,"approved37 production")
 if not failures.is_empty():quit(1);return
 rig.hud.hide();rig.hint.hide();rig.pose_status.hide();rig.reset()
 var baseline=rig.face.snapshot();var head=rig.head.transform;var body=rig.body.transform
 check(rig.play_expression("EXP-129"),"play")
 if visual:
  DirAccess.make_dir_recursive_absolute(w+"/motion/full");DirAccess.make_dir_recursive_absolute(w+"/motion/detail")
 var first=[];var last=[]
 for i in range(121):
  if i>0:check(rig.advance(maxf(0.0,float(i)/30.0-rig.performance_time)),"advance "+str(i))
  var p=rig.pose_now()
  check(rig.Registry.scoped_valid(p),"scope "+str(i));check(rig.Registry.sealed_mouth_valid(p),"sealed "+str(i))
  check(rig.head.transform==head and rig.body.transform==body,"fixed body "+str(i))
  check(p.blink_L==p.blink_R and p.blink_L<=.080001,"bounded symmetric subtle lids "+str(i))
  check(p.gaze_y<=0 and p.gaze_y>=-.800001,"bounded upward gaze "+str(i))
  for key in p:
   var bounds=rig.Registry.CHANNEL_BOUNDS[key]
   check(p[key]>=bounds[0] and p[key]<=bounds[1],"bounded "+key+" "+str(i))
   if key not in ACTING_CHANNELS:check(p[key]==0,"excluded "+key+" "+str(i))
  check(not rig.auto_blink,"no automatic blink "+str(i))
  var hashes=[]
  if visual:
   hashes.append(await snap(w+"/motion/full/%04d.png"%i,false));hashes.append(await snap(w+"/motion/detail/%04d.png"%i,true))
  if i==0:first=hashes
  if i==120:last=hashes
  records.append({"frame":i,"time":float(i)/30,"pose":p,"hashes":hashes})
 # Expression-specific temporal checks independent of the copied lifecycle harness.
 var left=records[33].pose;var right=records[60].pose;var pinch=records[20].pose
 check(pinch.brow_screen_left<-.5 and pinch.brow_screen_right<-.5,"pinch precedes lifts")
 check(left.brow_screen_left>.6 and left.brow_screen_right<-.3,"first lift screen left")
 check(left.gaze_y<-.79,"brief upward glance with first lift")
 check(right.brow_screen_right>.6 and right.brow_screen_left<-.3,"second lift screen right")
 check(right.gaze_y==0,"gaze returns before second lift")
 check(records[80].pose.mouth_purse==0,"purse fully released before brow settle")
 for record in records:
  if record.time<=.2 or record.time>=3.7:
   for value in record.pose.values():check(value==0,"neutral hold "+str(record.time))
  if record.time>=1.45:check(record.pose.gaze_y==0,"glance finished "+str(record.time))
  check(record.pose.mouth_open==0,"no speech "+str(record.time))
 for i in range(1,records.size()):
  for key in ACTING_CHANNELS:check(absf(records[i].pose[key]-records[i-1].pose[key])<.20,"bounded frame step "+key+" "+str(i))
 check(rig.face.snapshot()==baseline,"end exact object neutral")
 check(rig.registry.resolve("EXP-129")=="EXP-129","approved production registration")
 if visual:check(first==last,"end exact pixel neutral")
 for t in [.35,.65,1.1,1.45,1.95,2.2,2.65,3.15,3.7]:
  rig.reset();rig.play_expression("EXP-129");rig.advance(t)
  var before=rig.displayed_pose();rig.play_expression("EXP-129");check(rig.displayed_pose()==before,"restart continuous "+str(t))
  rig.advance(.4);before=rig.displayed_pose();rig.release();check(rig.displayed_pose()==before,"release continuous "+str(t))
  for j in range(16):rig.advance(1.0/30)
  check(rig.face.snapshot()==baseline,"release neutral "+str(t))
  rig.play_expression("EXP-129");rig.advance(t);rig.reset();check(rig.face.snapshot()==baseline,"reset neutral "+str(t))
 for alias in ["mental_arithmetic"]:
  rig.reset();check(rig.play_expression(alias),"alias plays");check(rig.performance.id=="EXP-129","alias resolves")
 var cross_cases=0;var cross_samples=0
 for entry in rig.list_expressions():
  if entry.id=="EXP-129":continue
  for pair in [["EXP-129",entry.id],[entry.id,"EXP-129"]]:
   rig.reset();check(rig.play_expression(pair[0]),"cross source");rig.advance(rig.performance.duration*.5)
   var before=rig.displayed_pose();check(rig.play_expression(pair[1]),"cross target");check(rig.displayed_pose()==before,"cross C0 "+str(pair))
   var last_time=0.0
   for t in [0.0,.000001,.075,.149999,.15,.150001,.225,.299999,.3,.300001,.61]:
    check(rig.advance(t-last_time),"cross advance");last_time=t;cross_samples+=1
    var p=rig.pose_now()
    check(rig.Registry.scoped_valid(p),"cross scope "+str(pair)+" "+str(t))
    check(rig.Registry.sealed_mouth_valid(p),"cross mouth "+str(pair)+" "+str(t))
    check(rig.head.transform==head and rig.body.transform==body,"cross fixed body")
    for key in p:
     var bounds=rig.Registry.CHANNEL_BOUNDS[key]
     check(rig.Registry.number(p[key]) and p[key]>=bounds[0] and p[key]<=bounds[1],"cross bounded "+key)
   rig.advance(rig.registry.definition(pair[1]).duration)
   check(rig.face.snapshot()==baseline and rig.pose_now()==rig.neutral_pose(),"cross completion exact neutral "+str(pair))
   check(rig.active_performance=="" and rig.release_time<0,"cross ownership cleared")
   cross_cases+=1
  print("MENTAL_CROSS_DONE ",entry.id)
 var result={"checks":checks,"failures":failures,"status":"PASS" if failures.is_empty() else "FAIL","production_profile_count":37,"frames":121,"fps":30,"duration":4.0,"visual_capture":visual,"renderer":RenderingServer.get_video_adapter_name(),"display":DisplayServer.get_name(),"records":records,"actual_object_directed_cross_cases":cross_cases,"actual_object_cross_samples":cross_samples,"runtime_sha256":FileAccess.get_sha256("res://expression_rig.gd"),"production_registry_tested":true,"normal_speed_observed":false,"approval":"USER_APPROVED","scope":"Actual instantiated production scene and face setters. Full 121-frame EXP-129 control trajectory, restart/release/reset at nine anchors, alias, bidirectional midpoint transitions with every prior36 profile at 11 boundary checkpoints and exact neutral completion. Headless state checks do not prove rendered transitions or live pacing."}
 var f=FileAccess.open(w+"/motion_state_checks.json",FileAccess.WRITE);f.store_string(JSON.stringify(result,"  "));f.close()
 print("MOTION_",result.status," checks=",checks," failures=",failures);quit(0 if failures.is_empty() else 1)

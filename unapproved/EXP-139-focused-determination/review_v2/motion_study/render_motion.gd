extends SceneTree
var rig
var w=get_script().resource_path.get_base_dir()
var failures=[]
var checks=0
var records=[]
var visual=false
var baseline_freeze=JSON.parse_string(FileAccess.get_file_as_string(w+"/../BASELINE_FREEZE.json"))
var BASELINE_COUNT=int(baseline_freeze.baseline_profile_count)
const ACTING_CHANNELS=["brow_screen_left","brow_screen_right","brow_tilt_screen_left","brow_tilt_screen_right","mouth_lip_press","mouth_width_screen_left","mouth_width_screen_right","blink_L","blink_R"]
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
 check(rig.rig_ready and rig.registry_ready,"ready");check(rig.list_expressions().size()==BASELINE_COUNT,baseline_freeze.baseline+" baseline")
 if not failures.is_empty():quit(1);return
 rig.hud.hide();rig.hint.hide();rig.pose_status.hide();rig.reset()
 var baseline=rig.face.snapshot();var head=rig.head.transform;var body=rig.body.transform
 var registry_text=FileAccess.get_file_as_string("res://expressions/registry.json")
 var cat=JSON.parse_string(registry_text);var defs={}
 for entry in cat.entries:defs[entry.path]=JSON.parse_string(FileAccess.get_file_as_string(entry.path))
 cat.entries.append({"id":"EXP-139","path":"res://candidate-139.json","aliases":[],"trigger_phase":"neutral"})
 defs["res://candidate-139.json"]=JSON.parse_string(FileAccess.get_file_as_string(w+"/EXP-139.json"))
 check(rig.registry.load_catalogue(cat,defs),"candidate catalogue: "+rig.registry.last_error)
 check(rig.list_expressions().size()==BASELINE_COUNT+1,baseline_freeze.baseline+" plus one in-memory candidate")
 if not failures.is_empty():quit(1);return
 var static_plan=JSON.parse_string(FileAccess.get_file_as_string(w+"/../plan.json"));var selected={}
 for row in static_plan:
  if row.name=="c_strongest_open":selected=row.pose
 check(not selected.is_empty(),"selected static C exists")
 var dense_max_blink=0.0
 for j in range(4001):
  var t=float(j)/1000.0;var sample=rig.sample_expression("EXP-139",t)
  check(rig.Registry.scoped_valid(sample) and rig.Registry.sealed_mouth_valid(sample),"dense valid domain "+str(j))
  check(sample.blink_L==sample.blink_R and sample.eye_smile_L==0 and sample.eye_smile_R==0,"dense symmetric ordinary blink "+str(j))
  dense_max_blink=maxf(dense_max_blink,sample.blink_L)
  if t<=.36 or t>=.70:check(is_zero_approx(sample.blink_L) and is_zero_approx(sample.blink_R),"blink confined to onset "+str(j))
  if t>=.78 and t<=2.40:
   for key in sample:check(is_equal_approx(sample[key],float(selected.get(key,0))),"exact open-eyed C hold "+str(j)+" "+key)
 check(dense_max_blink==1.0,"one full refocusing closure reached")
 check(rig.play_expression("EXP-139"),"play")
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
  check(p.blink_L==p.blink_R and p.eye_smile_L==0 and p.eye_smile_R==0,"ordinary symmetric lids "+str(i))
  if float(i)/30.0>=.70:check(p.blink_L==0 and p.blink_R==0,"peak and recovery eyes fully open "+str(i))
  var hashes=[]
  if visual:
   hashes.append(await snap(w+"/motion/full/%04d.png"%i,false));hashes.append(await snap(w+"/motion/detail/%04d.png"%i,true))
  if i==0:first=hashes
  if i==120:last=hashes
  records.append({"frame":i,"time":float(i)/30,"pose":p,"hashes":hashes})
 check(rig.face.snapshot()==baseline,"end exact object neutral")
 if visual:check(first==last,"end exact pixel neutral")
 for t in [.30,.42,.50,.62,.78,1.5,2.4,3.0,3.5]:
  rig.reset();rig.play_expression("EXP-139");rig.advance(t)
  var before=rig.displayed_pose();rig.play_expression("EXP-139");check(rig.displayed_pose()==before,"restart continuous "+str(t))
  rig.advance(.4);before=rig.displayed_pose();rig.release();check(rig.displayed_pose()==before,"release continuous "+str(t))
  for j in range(16):rig.advance(1.0/30)
  check(rig.face.snapshot()==baseline,"release neutral "+str(t))
  rig.play_expression("EXP-139");rig.advance(t);rig.reset();check(rig.face.snapshot()==baseline,"reset neutral "+str(t))
 check(FileAccess.get_file_as_string("res://expressions/registry.json")==registry_text,"production disk registry byte exact")
 var result={"checks":checks,"failures":failures,"status":"PASS" if failures.is_empty() else "FAIL","baseline":baseline_freeze.baseline,"baseline_profile_count":BASELINE_COUNT,"frames":121,"fps":30,"duration":4.0,"visual_capture":visual,"renderer":RenderingServer.get_video_adapter_name(),"display":DisplayServer.get_name(),"records":records,"production_registry_unchanged":true,"normal_speed_observed":false,"approval":"UNAPPROVED"}
 var f=FileAccess.open(w+("/motion_checks.json" if visual else "/motion_state_checks.json"),FileAccess.WRITE);f.store_string(JSON.stringify(result,"  "));f.close()
 print("MOTION_",result.status," checks=",checks," failures=",failures);quit(0 if failures.is_empty() else 1)

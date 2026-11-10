extends SceneTree
var rig
var w=get_script().resource_path.get_base_dir()
var failures=[]
var checks=0
var records=[]
var visual=false
var baseline_freeze=JSON.parse_string(FileAccess.get_file_as_string(w+"/BASELINE_FREEZE.json"))
var BASELINE_COUNT=int(baseline_freeze.baseline_profile_count)
const ACTING_CHANNELS=["brow_screen_left","brow_screen_right","brow_tilt_screen_left","brow_tilt_screen_right","blink_L","blink_R","mouth_lip_press"]
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
 check(rig.rig_ready and rig.registry_ready,"ready");check(rig.list_expressions().size()==BASELINE_COUNT,baseline_freeze.baseline+" baseline")
 if not failures.is_empty():quit(1);return
 rig.hud.hide();rig.hint.hide();rig.pose_status.hide();rig.reset()
 var baseline=rig.face.snapshot();var head=rig.head.transform;var body=rig.body.transform
 var registry_text=FileAccess.get_file_as_string("res://expressions/registry.json")
 var cat=JSON.parse_string(registry_text);var defs={}
 for entry in cat.entries:defs[entry.path]=JSON.parse_string(FileAccess.get_file_as_string(entry.path))
 cat.entries.append({"id":"EXP-041","path":"res://candidate-041.json","aliases":[],"trigger_phase":"neutral"})
 defs["res://candidate-041.json"]=JSON.parse_string(FileAccess.get_file_as_string(w+"/EXP-041.json"))
 check(rig.registry.load_catalogue(cat,defs),"candidate catalogue: "+rig.registry.last_error)
 check(rig.list_expressions().size()==BASELINE_COUNT+1,baseline_freeze.baseline+" plus one in-memory candidate")
 if not failures.is_empty():quit(1);return
 check(rig.play_expression("EXP-041"),"play")
 if visual:
  DirAccess.make_dir_recursive_absolute(w+"/motion/full");DirAccess.make_dir_recursive_absolute(w+"/motion/detail")
 var first=[];var last=[]
 for i in range(121):
  if i>0:check(rig.advance(maxf(0.0,float(i)/30.0-rig.performance_time)),"advance "+str(i))
  var p=rig.pose_now()
  check(rig.Registry.scoped_valid(p),"scope "+str(i));check(rig.Registry.sealed_mouth_valid(p),"sealed "+str(i))
  check(rig.head.transform==head and rig.body.transform==body,"fixed body "+str(i))
  check(p.blink_L==p.blink_R and p.blink_L<=.260001,"bounded symmetric narrow lids "+str(i))
  check(p.gaze_y==0 and p.gaze_x==0,"fixed gaze "+str(i))
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
 var peak=records[45].pose;var easing=records[77].pose
 check(is_equal_approx(peak.brow_screen_left,-.7) and is_equal_approx(peak.brow_tilt_screen_left,.65),"moderate inward/down brow peak")
 check(is_equal_approx(peak.blink_L,.26) and is_equal_approx(peak.mouth_lip_press,.65),"narrow fixed eyes and restrained pressure")
 check(easing.mouth_lip_press<.4 and easing.brow_screen_left<-.69 and easing.blink_L>.259,"pressure eases before brows and eyes")
 for i in range(41,64):check(records[i].pose==peak,"still held peak "+str(i))
 for record in records:
  if record.time<=.2 or record.time>=3.7:
   for value in record.pose.values():check(value==0,"neutral hold "+str(record.time))
  check(record.pose.gaze_y==0 and record.pose.gaze_x==0,"fixed gaze "+str(record.time))
  check(record.pose.mouth_open==0,"no speech "+str(record.time))
 for i in range(1,records.size()):
  for key in ACTING_CHANNELS:check(absf(records[i].pose[key]-records[i-1].pose[key])<.20,"bounded frame step "+key+" "+str(i))
 check(rig.face.snapshot()==baseline,"end exact object neutral")
 check(rig.registry.resolve("EXP-041")=="EXP-041","candidate exists only in loaded memory")
 if visual:check(first==last,"end exact pixel neutral")
 for t in [.35,.6,.95,1.35,2.1,2.55,3.0,3.35,3.7]:
  rig.reset();rig.play_expression("EXP-041");rig.advance(t)
  var before=rig.displayed_pose();rig.play_expression("EXP-041");check(rig.displayed_pose()==before,"restart continuous "+str(t))
  rig.advance(.4);before=rig.displayed_pose();rig.release();check(rig.displayed_pose()==before,"release continuous "+str(t))
  for j in range(16):rig.advance(1.0/30)
  check(rig.face.snapshot()==baseline,"release neutral "+str(t))
  rig.play_expression("EXP-041");rig.advance(t);rig.reset();check(rig.face.snapshot()==baseline,"reset neutral "+str(t))
 check(FileAccess.get_file_as_string("res://expressions/registry.json")==registry_text,"production disk registry byte exact")
 var result={"checks":checks,"failures":failures,"status":"PASS" if failures.is_empty() else "FAIL","baseline":baseline_freeze.baseline,"baseline_profile_count":BASELINE_COUNT,"frames":121,"fps":30,"duration":4.0,"visual_capture":visual,"renderer":RenderingServer.get_video_adapter_name(),"display":DisplayServer.get_name(),"records":records,"production_registry_unchanged":true,"normal_speed_observed":false,"approval":"UNAPPROVED"}
 var f=FileAccess.open(w+("/motion_checks.json" if visual else "/motion_state_checks.json"),FileAccess.WRITE);f.store_string(JSON.stringify(result,"  "));f.close()
 print("MOTION_",result.status," checks=",checks," failures=",failures);quit(0 if failures.is_empty() else 1)

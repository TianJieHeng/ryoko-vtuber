extends Node
var root
var exit_code=0
var rig
var w="/workspace/scratch/42f2baf55663/mild_disgust_work"
var failures=[]
var checks=0
var records=[]
var visual=false
var baseline_freeze=JSON.parse_string(FileAccess.get_file_as_string(w+"/BASELINE_FREEZE.json"))
var BASELINE_COUNT=int(baseline_freeze.baseline_profile_count)
const ACTING_CHANNELS=["brow_screen_left","brow_screen_right","brow_tilt_screen_left","brow_tilt_screen_right","blink_L","blink_R","mouth_open","mouth_purse","mouth_corner_lift_screen_right"]
func _ready():
 root=get_tree().root
 visual=true
 call_deferred("run")
func check(ok,label):
 checks+=1
 if not ok:failures.append(label)
func snap(path,detail):
 root.size=Vector2i(568,800);root.canvas_transform=Transform2D.IDENTITY
 if detail:
  root.size=Vector2i(400,360)
  var camera=Transform2D.IDENTITY.scaled(Vector2.ONE/.49);camera.origin=-Vector2(6,70)/.49-Vector2(380,380);root.canvas_transform=camera
 await get_tree().process_frame;await get_tree().process_frame;await RenderingServer.frame_post_draw
 var im=root.get_texture().get_image()
 var expected=Vector2i(400,360) if detail else Vector2i(568,800)
 check(im.get_size()==expected,"native dimensions "+path+" expected="+str(expected)+" actual="+str(im.get_size()))
 if im.get_size()!=expected:return ""
 check(im.save_png(path)==OK,"saved "+path)
 var ctx=HashingContext.new();ctx.start(HashingContext.HASH_SHA256);ctx.update(im.get_data());return ctx.finish().hex_encode()
func run():
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false);rig.auto_blink=false
 check(rig.rig_ready and rig.registry_ready,"ready");check(rig.list_expressions().size()==BASELINE_COUNT,baseline_freeze.baseline+" baseline")
 if not failures.is_empty():finish(1);return
 rig.hud.hide();rig.hint.hide();rig.pose_status.hide();rig.reset()
 var baseline=rig.face.snapshot();var head=rig.head.transform;var body=rig.body.transform
 var brow_home={};var lash_home={}
 for side in ["screen_left","screen_right"]:
  brow_home[side]=rig.face.homes["brow_"+side].node.position
  lash_home[side]=rig.face.homes["upper_lash_"+side].node.position
 var registry_text=FileAccess.get_file_as_string("res://expressions/registry.json")
 var cat=JSON.parse_string(registry_text);var defs={}
 for entry in cat.entries:defs[entry.path]=JSON.parse_string(FileAccess.get_file_as_string(entry.path))
 cat.entries.append({"id":"EXP-081","path":"res://candidate-081.json","aliases":[],"trigger_phase":"neutral"})
 defs["res://candidate-081.json"]=JSON.parse_string(FileAccess.get_file_as_string(w+"/EXP-081.json"))
 check(rig.registry.load_catalogue(cat,defs),"candidate catalogue: "+rig.registry.last_error)
 check(rig.list_expressions().size()==BASELINE_COUNT+1,baseline_freeze.baseline+" plus one in-memory candidate")
 if not failures.is_empty():finish(1);return
 check(rig.play_expression("EXP-081"),"play")
 if visual:
  DirAccess.make_dir_recursive_absolute(w+"/motion/full");DirAccess.make_dir_recursive_absolute(w+"/motion/detail")
 var first=[];var last=[]
 for i in range(121):
  if i>0:check(rig.advance(maxf(0.0,float(i)/30.0-rig.performance_time)),"advance "+str(i))
  var p=rig.pose_now()
  check(rig.Registry.scoped_valid(p),"scope "+str(i));check(rig.Registry.sealed_mouth_valid(p),"sealed "+str(i))
  check(rig.head.transform==head and rig.body.transform==body,"fixed body "+str(i))
  check(p.blink_R>=p.blink_L and p.blink_R<=.340001 and p.blink_L<=.180001,"bounded uneven lids "+str(i))
  check(p.gaze_x==0 and p.gaze_y==0,"fixed forward gaze "+str(i))
  for side in ["screen_left","screen_right"]:
   var node=rig.face.homes["brow_"+side].node
   var angle=deg_to_rad(8.0*p["brow_tilt_"+side])
   var a=rig.Registry.Limits.BROW_OUTER_ANCHORS[side]-rig.face.homes["brow_"+side].pivot
   var expected=Vector2(0,-10.0*p["brow_"+side])
   check((node.position-brow_home[side]).distance_to(expected)<.0001,"timeline actual brow position "+side+" "+str(i))
   check(is_equal_approx(node.rotation,angle),"timeline actual brow rotation "+side+" "+str(i))
   var delta=rig.face.homes["upper_lash_"+side].node.position-lash_home[side]
   var closure=p.blink_R if side=="screen_left" else p.blink_L
   check(delta.distance_to(Vector2(0,36.0*closure))<.0001,"timeline actual ordinary lash travel "+side+" "+str(i))
   check(is_equal_approx(rig.face.objects["iris_"+side].material.get_shader_parameter("closure"),closure),"timeline iris closure "+side+" "+str(i))
   check(rig.face.objects["iris_"+side].material.get_shader_parameter("rigid_gaze").is_equal_approx(Vector2.ZERO),"timeline iris fixed "+side+" "+str(i))
  var actual_gap=rig.face._smile_lip_offset(39.5,false,false)-rig.face._smile_lip_offset(39.5,true,false)
  var expected_gap=maxf(0.0,p.mouth_open*0.55*54.0-1.5*p.mouth_purse*minf(p.mouth_open*4.0,1.0))
  check(is_equal_approx(actual_gap,expected_gap),"timeline actual central mouth gap "+str(i))
  check(is_equal_approx(rig.face._spread_x(4.0),14.0*p.mouth_purse) and is_equal_approx(rig.face._spread_x(75.0),-14.0*p.mouth_purse),"timeline actual symmetric purse "+str(i))
  for x in [4.0,39.5,75.0]:
   var radius=absf((x-39.5)/35.5)
   var expected_upper=p.mouth_purse*(4.0+8.0*radius*radius)-12.0*p.mouth_corner_lift_screen_right*pow(maxf((x-39.5)/35.5,0.0),3)
   var actual_upper=rig.face._smile_lip_offset(x,true,false)
   var actual_lower=rig.face._smile_lip_offset(x,false,false)
   check(is_equal_approx(actual_upper,expected_upper),"timeline common upper contour "+str(x)+" "+str(i))
   check(actual_lower>=actual_upper,"timeline nonnegative lip gap "+str(x)+" "+str(i))
  check(is_equal_approx(rig.face._smile_lip_offset(4.0,false,false)-rig.face._smile_lip_offset(75.0,false,false),12.0*p.mouth_corner_lift_screen_right),"timeline both lips share corner bias "+str(i))
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
  records.append({"frame":i,"time":float(i)/30,"pose":p,"hashes":hashes,"central_lip_gap_native_px":actual_gap})
 # Source-specific temporal relationships, distinct from taste or nausea.
 var detect=records[18].pose;var peak=records[42].pose;var sealed=records[65].pose
 check(detect.brow_screen_left<-.139 and detect.mouth_open==0 and detect.mouth_corner_lift_screen_right==0,"asymmetric detection leads mouth bias")
 check(peak.brow_screen_left<-.439 and peak.brow_screen_right>-.121,"one brow lowers more strongly")
 check(peak.blink_R>.339 and peak.blink_L<.181,"unequal mild narrowed eyes")
 check(peak.mouth_open>.179 and peak.mouth_corner_lift_screen_right>.319,"brief small parted common-corner lift")
 check(is_equal_approx(records[42].central_lip_gap_native_px,5.2164),"small peak central gap")
 for key in ACTING_CHANNELS:check(is_equal_approx(records[42].pose[key],records[52].pose[key]),"brief peak hold "+key)
 check(sealed.mouth_open==0 and sealed.brow_screen_left<-.37 and sealed.mouth_corner_lift_screen_right>.11,"mouth seals while objection persists")
 check(records[81].pose.mouth_corner_lift_screen_right==0 and records[81].pose.brow_screen_left<-.199,"mouth bias releases before brow tension")
 check(records[98].pose.mouth_purse==0,"purse releases before final brow settle")
 for record in records:
  if record.time<=.2 or record.time>=3.7:
   for value in record.pose.values():check(value==0,"neutral hold "+str(record.time))
  check(record.pose.brow_inner_lift_screen_left==0 and record.pose.brow_inner_lift_screen_right==0,"no queasy inner-brow lift "+str(record.time))
  check(record.pose.mouth_width_screen_left==0 and record.pose.mouth_width_screen_right==0,"no incompatible sealed-only width "+str(record.time))
  check(record.pose.eye_smile_R==0 and record.pose.eye_smile_L==0 and record.pose.mouth_smile==0,"no smile-eye or smile "+str(record.time))
 for i in range(1,records.size()):
  for key in ACTING_CHANNELS:check(absf(records[i].pose[key]-records[i-1].pose[key])<.20,"bounded frame step "+key+" "+str(i))
 check(rig.face.snapshot()==baseline,"end exact object neutral")
 check(rig.registry.resolve("EXP-081")=="EXP-081","candidate exists only in loaded memory")
 if visual:check(first==last,"end exact pixel neutral")
 for t in [.35,.6,1.0,1.4,1.75,2.15,2.7,3.25,3.7]:
  rig.reset();rig.play_expression("EXP-081");rig.advance(t)
  var before=rig.displayed_pose();rig.play_expression("EXP-081");check(rig.displayed_pose()==before,"restart continuous "+str(t))
  rig.advance(.4);before=rig.displayed_pose();rig.release();check(rig.displayed_pose()==before,"release continuous "+str(t))
  for j in range(16):rig.advance(1.0/30)
  check(rig.face.snapshot()==baseline,"release neutral "+str(t))
  rig.play_expression("EXP-081");rig.advance(t);rig.reset();check(rig.face.snapshot()==baseline,"reset neutral "+str(t))
 check(FileAccess.get_file_as_string("res://expressions/registry.json")==registry_text,"production disk registry byte exact")
 var result={"checks":checks,"failures":failures,"status":"PASS" if failures.is_empty() else "FAIL","baseline":baseline_freeze.baseline,"baseline_profile_count":BASELINE_COUNT,"frames":121,"fps":30,"duration":4.0,"visual_capture":visual,"profile_sha256":FileAccess.get_sha256(w+"/EXP-081.json"),"baseline_freeze_sha256":FileAccess.get_sha256(w+"/BASELINE_FREEZE.json"),"lifecycle_interruption_times":[.35,.6,1.0,1.4,1.75,2.15,2.7,3.25,3.7],"lifecycle_assertions":36,"renderer":RenderingServer.get_video_adapter_name(),"display":DisplayServer.get_name(),"records":records,"production_registry_unchanged":true,"normal_speed_observed":false,"approval":"UNAPPROVED"}
 var f=FileAccess.open(w+("/motion_checks.json" if visual else "/motion_state_checks.json"),FileAccess.WRITE);f.store_string(JSON.stringify(result,"  "));f.close()
 print("MOTION_",result.status," checks=",checks," failures=",failures);finish(0 if failures.is_empty() else 1)

func finish(code):
 exit_code=code
 if is_instance_valid(rig):rig.queue_free()
 queue_free()

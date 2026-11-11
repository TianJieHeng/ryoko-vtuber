extends SceneTree
var rig
var w=get_script().resource_path.get_base_dir()
var failures=[]
var checks=0
var records=[]
var visual=false
var baseline_freeze=JSON.parse_string(FileAccess.get_file_as_string(w+"/BASELINE_FREEZE.json"))
var BASELINE_COUNT=int(baseline_freeze.baseline_profile_count)
const ACTING_CHANNELS=["brow_screen_left","brow_screen_right","brow_tilt_screen_left","brow_tilt_screen_right","blink_L","blink_R","mouth_lip_press","mouth_purse"]
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
 var brow_home={};var lash_home={}
 for side in ["screen_left","screen_right"]:
  brow_home[side]=rig.face.homes["brow_"+side].node.position
  lash_home[side]=rig.face.homes["upper_lash_"+side].node.position
 var registry_text=FileAccess.get_file_as_string("res://expressions/registry.json")
 var cat=JSON.parse_string(registry_text);var defs={}
 for entry in cat.entries:defs[entry.path]=JSON.parse_string(FileAccess.get_file_as_string(entry.path))
 cat.entries.append({"id":"EXP-096","path":"res://candidate-096.json","aliases":[],"trigger_phase":"neutral"})
 defs["res://candidate-096.json"]=JSON.parse_string(FileAccess.get_file_as_string(w+"/EXP-096.json"))
 check(rig.registry.load_catalogue(cat,defs),"candidate catalogue: "+rig.registry.last_error)
 check(rig.list_expressions().size()==BASELINE_COUNT+1,baseline_freeze.baseline+" plus one in-memory candidate")
 if not failures.is_empty():quit(1);return
 check(rig.play_expression("EXP-096"),"play")
 if visual:
  DirAccess.make_dir_recursive_absolute(w+"/motion/full");DirAccess.make_dir_recursive_absolute(w+"/motion/detail")
 var first=[];var last=[]
 for i in range(121):
  if i>0:check(rig.advance(maxf(0.0,float(i)/30.0-rig.performance_time)),"advance "+str(i))
  var p=rig.pose_now()
  check(rig.Registry.scoped_valid(p),"scope "+str(i));check(rig.Registry.sealed_mouth_valid(p),"sealed "+str(i))
  check(rig.head.transform==head and rig.body.transform==body,"fixed body "+str(i))
  check(p.blink_R==p.blink_L and p.blink_L<=1,"ordinary bilateral lid range "+str(i))
  check(p.gaze_x==0 and p.gaze_y==0 and p.gaze_down_extra==0 and p.opening_px==0 and p.eye_smile_L==0 and p.eye_smile_R==0,"no ordinary gaze or opening conflicts "+str(i))
  check(p.aversion_px==0 and p.mouth_open==0 and p.mouth_purse<=.050001,"sealed tiny-purse frontal scope "+str(i))
  var iris_geometry={}
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
   var offset=rig.face.objects["iris_"+side].material.get_shader_parameter("rigid_gaze")
   var delta_iris=rig.face.homes["iris_"+side].node.position-rig.face.homes["iris_"+side].pivot
   check(offset.is_equal_approx(Vector2(p.aversion_px,0)),"timeline iris aversion shader "+side+" "+str(i))
   check(delta_iris.distance_to(Vector2(p.aversion_px,0))<.0001,"timeline iris aversion sprite "+side+" "+str(i))
   check(rig.face.objects["sclera_"+side].material.get_shader_parameter("rigid_gaze").is_equal_approx(Vector2(p.aversion_px,0)),"timeline sclera aversion shader "+side+" "+str(i))
   iris_geometry[side]={"sprite_delta_source_px":[delta_iris.x,delta_iris.y],"iris_shader_offset_source_px":[offset.x,offset.y]}
  var pressure_owners=[]
  for entry in rig.face.pressed_lip_owners:
   var amount=entry.node.material.get_shader_parameter("lip_press")
   check(is_equal_approx(amount,p.mouth_lip_press),"timeline pressure shader "+str(i))
   check(entry.node.visible==(p.mouth_lip_press>0),"timeline pressure visibility "+str(i))
   pressure_owners.append({"name":entry.node.name,"amount":amount,"visible":entry.node.visible})
  check(not pressure_owners.is_empty(),"pressure owners present "+str(i))
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
  records.append({"frame":i,"time":float(i)/30,"pose":p,"iris_geometry":iris_geometry,"pressure_owners":pressure_owners,"hashes":hashes,"central_lip_gap_native_px":actual_gap})
 # Source KP5-6 closed, KP7 softens before any reopening.
 var onset=records[18].pose;var peak=records[48].pose;var soften=records[84].pose
 check(onset.brow_screen_left<0 and onset.blink_L>0 and onset.blink_L<1,"tension starts with progressive lid closure")
 check(is_equal_approx(peak.brow_screen_left,-.55) and peak.brow_screen_left==peak.brow_screen_right,"equal lowered peak brows")
 check(is_equal_approx(peak.brow_tilt_screen_left,.65) and is_equal_approx(peak.brow_tilt_screen_right,-.65),"opposed peak brow tilts")
 check(peak.blink_L==1 and peak.blink_R==1,"KP5-6 fully closed ordinary lids")
 check(is_equal_approx(peak.mouth_lip_press,.65) and is_equal_approx(peak.mouth_purse,.05),"sealed pressed tiny purse peak")
 for i in range(48,73):
  for key in ACTING_CHANNELS:check(is_equal_approx(peak[key],records[i].pose[key]),"sustained headache hold "+str(i)+" "+key)
 for i in range(48,85):check(records[i].pose.blink_L==1 and records[i].pose.blink_R==1,"closed through KP7 "+str(i))
 check(soften.brow_screen_left>peak.brow_screen_left and soften.brow_tilt_screen_left<peak.brow_tilt_screen_left and soften.mouth_lip_press<peak.mouth_lip_press and soften.mouth_purse==0,"KP7 brow and mouth soften while closed")
 for i in range(1,49):check(records[i].pose.blink_L>=records[i-1].pose.blink_L,"monotone heavy closure "+str(i))
 for i in range(85,121):check(records[i].pose.blink_L<=records[i-1].pose.blink_L,"monotone delayed reopening "+str(i))
 check(is_equal_approx(records[96].pose.blink_L,.18) and records[96].pose.mouth_lip_press==0,"reopen after tension release")
 for record in records:
  if record.time<=.2 or record.time>=3.7:
   for value in record.pose.values():check(value==0,"neutral hold "+str(record.time))
  check(record.pose.brow_inner_lift_screen_left==0 and record.pose.brow_inner_lift_screen_right==0,"no effortful inner-brow lift "+str(record.time))
  check(record.pose.mouth_width_screen_left==0 and record.pose.mouth_width_screen_right==0,"no incompatible sealed-only width "+str(record.time))
  check(record.pose.eye_smile_R==0 and record.pose.eye_smile_L==0 and record.pose.mouth_smile==0,"no smile-eye or smile "+str(record.time))
 for i in range(1,records.size()):
  for key in ACTING_CHANNELS:check(absf(records[i].pose[key]-records[i-1].pose[key])<.20,"bounded frame step "+key+" "+str(i))
 check(rig.face.snapshot()==baseline,"end exact object neutral")
 check(rig.registry.resolve("EXP-096")=="EXP-096","candidate exists only in loaded memory")
 if visual:check(first==last,"end exact pixel neutral")
 var lifecycle_records=[]
 for t in [.35,.6,1.0,1.6,2.4,2.8,3.2,3.5,3.7]:
  rig.reset();rig.play_expression("EXP-096");rig.advance(t)
  var before=rig.displayed_pose();rig.play_expression("EXP-096");check(rig.displayed_pose()==before,"restart continuous "+str(t))
  for j in range(12):
   check(rig.advance(1.0/30),"restart advance")
   var lp=rig.pose_now();check(rig.Registry.scoped_valid(lp),"restart scoped invariant")
   lifecycle_records.append({"interruption_time":t,"stage":"restart","step":j+1,"pose":lp})
  rig.reset();rig.play_expression("EXP-096");rig.advance(t)
  before=rig.displayed_pose();rig.release();check(rig.displayed_pose()==before,"release continuous "+str(t))
  for j in range(16):
   check(rig.advance(1.0/30),"release advance")
   var lp=rig.pose_now();check(rig.Registry.scoped_valid(lp),"release scoped invariant")
   lifecycle_records.append({"interruption_time":t,"stage":"release","step":j+1,"pose":lp})
  check(rig.face.snapshot()==baseline,"release neutral "+str(t))
  rig.play_expression("EXP-096");rig.advance(t);rig.reset();check(rig.face.snapshot()==baseline,"reset neutral "+str(t))
 check(FileAccess.get_file_as_string("res://expressions/registry.json")==registry_text,"production disk registry byte exact")
 var result={"checks":checks,"failures":failures,"status":"PASS" if failures.is_empty() else "FAIL","baseline":baseline_freeze.baseline,"baseline_profile_count":BASELINE_COUNT,"frames":121,"fps":30,"duration":4.0,"visual_capture":visual,"profile_sha256":FileAccess.get_sha256(w+"/EXP-096.json"),"baseline_freeze_sha256":FileAccess.get_sha256(w+"/BASELINE_FREEZE.json"),"lifecycle_interruption_times":[.35,.6,1.0,1.6,2.4,2.8,3.2,3.5,3.7],"lifecycle_assertions":36,"lifecycle_scoped_samples":lifecycle_records,"renderer":RenderingServer.get_video_adapter_name(),"display":DisplayServer.get_name(),"records":records,"production_registry_unchanged":true,"normal_speed_observed":false,"approval":"UNAPPROVED"}
 var f=FileAccess.open(w+("/motion_checks.json" if visual else "/motion_state_checks.json"),FileAccess.WRITE);f.store_string(JSON.stringify(result,"  "));f.close()
 print("MOTION_",result.status," checks=",checks," failures=",failures);quit(0 if failures.is_empty() else 1)

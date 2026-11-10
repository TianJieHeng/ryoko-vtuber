extends SceneTree
var rig
var failures=[]
var checks=0
var records=[]
var w=get_script().resource_path.get_base_dir()
var visual=false
var baseline_freeze=JSON.parse_string(FileAccess.get_file_as_string(w+"/BASELINE_FREEZE.json"))
var BASELINE_COUNT=int(baseline_freeze.baseline_profile_count)
const ACTING_CHANNELS=["brow_screen_left","brow_screen_right","brow_tilt_screen_left","brow_tilt_screen_right","blink_L","blink_R","mouth_purse","mouth_open"]
func _initialize():
 visual="--capture" in OS.get_cmdline_user_args()
 call_deferred("run")
func check(ok,label):
 checks+=1
 if not ok:failures.append(label)
func capture(label,detail):
 root.size=Vector2i(568,800);root.canvas_transform=Transform2D.IDENTITY
 if detail:
  root.size=Vector2i(400,360)
  var camera=Transform2D.IDENTITY.scaled(Vector2.ONE/.49);camera.origin=-Vector2(6,70)/.49-Vector2(380,380);root.canvas_transform=camera
 await process_frame;await process_frame;await RenderingServer.frame_post_draw
 check(root.get_texture().get_image().save_png(w+"/capture/"+label+".png")==OK,"saved "+label)
func run():
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false);rig.auto_blink=false
 check(rig.rig_ready and rig.registry_ready,"rig ready")
 if not failures.is_empty():quit(1);return
 rig.hud.hide();rig.hint.hide();rig.pose_status.hide();rig.reset()
 var baseline=rig.face.snapshot();var head=rig.head.transform;var body=rig.body.transform
 var textures={};var scales={};var modulates={};var self_modulates={}
 for key in rig.face.objects:
  var node=rig.face.objects[key];textures[key]=node.texture;scales[key]=node.scale;modulates[key]=node.modulate;self_modulates[key]=node.self_modulate
 var brow_home={}
 for side in ["screen_left","screen_right"]:brow_home[side]=rig.face.homes["brow_"+side].node.position
 var lash_home={}
 for side in ["screen_left","screen_right"]:lash_home[side]=rig.face.homes["upper_lash_"+side].node.position
 var plan=JSON.parse_string(FileAccess.get_file_as_string(w+"/plan.json"))
 if visual:DirAccess.make_dir_recursive_absolute(w+"/capture")
 var registry_text=FileAccess.get_file_as_string("res://expressions/registry.json")
 var cat=JSON.parse_string(registry_text);var defs={}
 for entry in cat.entries:defs[entry.path]=JSON.parse_string(FileAccess.get_file_as_string(entry.path))
 check(rig.list_expressions().size()==BASELINE_COUNT,baseline_freeze.baseline+" baseline unchanged")
 check(plan.size()==7,"seven isolated study poses")
 for row in plan:
  var id="PROBE-093-"+row.name;var path="res://probe-093-"+row.name+".json"
  cat.entries.append({"id":id,"path":path,"aliases":[],"trigger_phase":"neutral"})
  defs[path]={"id":id,"title":row.name,"duration":3.0,"keyframes":[{"time":0.0,"phase":"neutral","values":{}},{"time":1.0,"phase":"probe","values":row.pose},{"time":2.0,"phase":"hold","values":row.pose},{"time":3.0,"phase":"neutral_return","values":{}}]}
 check(rig.registry.load_catalogue(cat,defs),"static probe catalogue: "+rig.registry.last_error)
 if not failures.is_empty():quit(1);return
 for row in plan:
  rig.reset()
  check(rig.play_expression("PROBE-093-"+row.name),row.name+" play: "+rig.last_error)
  check(rig.advance(1.5),row.name+" advance")
  var p=rig.pose_now()
  check(rig.Registry.scoped_valid(p),row.name+" scope")
  check(rig.Registry.sealed_mouth_valid(p),row.name+" mouth domain")
  check(rig.head.transform==head and rig.body.transform==body,row.name+" fixed body")
  check(not rig.auto_blink,row.name+" no automatic blink")
  check(p.blink_L==p.blink_R and p.blink_L<=.400001 and p.eye_smile_L==0 and p.eye_smile_R==0,row.name+" bounded ordinary narrowing lids only")
  check(p.mouth_open<=.450001 and p.mouth_corner_lift==0 and p.mouth_corner_lift_screen_left==0 and p.mouth_corner_lift_screen_right==0 and p.mouth_smile==0 and p.mouth_lip_press==0,row.name+" bounded unsmiling open/purse only")
  var geometry={}
  for side in ["screen_left","screen_right"]:
   var node=rig.face.homes["brow_"+side].node
   var delta=node.position-brow_home[side]
   check(absf(delta.y+10.0*float(row.pose.get("brow_"+side,0)))<0.0001,row.name+" actual vertical brow travel "+side)
   check(is_equal_approx(rad_to_deg(node.rotation),8.0*float(row.pose.get("brow_tilt_"+side,0))),row.name+" actual brow rotation "+side)
   check(is_zero_approx(delta.x),row.name+" no invented horizontal brow translation "+side)
   geometry[side]={"pivot_delta_source_px":[delta.x,delta.y],"rotation_degrees":rad_to_deg(node.rotation)}
  var lash_geometry={}
  for side in ["screen_left","screen_right"]:
   var node=rig.face.homes["upper_lash_"+side].node
   var delta=node.position-lash_home[side]
   var amount=p.blink_L if side=="screen_left" else p.blink_R
   check(is_equal_approx(delta.y,36.0*amount),row.name+" actual rigid upper-lash travel "+side)
   check(is_zero_approx(delta.x),row.name+" no horizontal upper-lash travel "+side)
   check(is_equal_approx(rig.face.objects["iris_"+side].material.get_shader_parameter("closure"),amount),row.name+" iris uses matching closure "+side)
   lash_geometry[side]={"pivot_delta_source_px":[delta.x,delta.y],"closure":amount}
  var mouth_width=[rig.face._spread_x(4.0),rig.face._spread_x(75.0)]
  check(is_equal_approx(mouth_width[0],14.0*p.mouth_purse) and is_equal_approx(mouth_width[1],-14.0*p.mouth_purse),row.name+" actual purse horizontal travel")
  var lip_offsets=[]
  for x in [4.0,22.0,39.5,57.0,75.0]:
   var upper=rig.face._smile_lip_offset(x,true,false)
   var lower=rig.face._smile_lip_offset(x,false,false)
   var radius=clampf(abs((x-39.5)/35.5),0,1)
   var common=p.mouth_purse*(4.0+8.0*radius*radius)
   var width=1.0-14.0*p.mouth_purse/35.5
   var cavity=38.0-12.0*p.mouth_open*.55-14.0*p.mouth_purse
   var h=clampf(abs((x-39.5)*width)/cavity,0,1)
   var curve=lerpf(1.0,sqrt(maxf(0,1-h*h)),p.mouth_purse)
   var gap=maxf(0,p.mouth_open*.55*54*curve-1.5*p.mouth_purse*minf(p.mouth_open*4,1))
   check(is_equal_approx(upper,common),row.name+" upper follows downward common contour "+str(x))
   check(absf(lower-upper-gap)<.0001,row.name+" actual lower lip gap "+str(x))
   check(upper>=0 and lower>=upper and lower-upper<=.55*54,row.name+" no upper lift or negative/unbounded separation "+str(x))
   lip_offsets.append({"x":x,"upper_y":upper,"lower_y":lower,"gap_source_px":lower-upper})
  var joints=[]
  for joint in rig.face.smile_lip_joints:
   var node=rig.face.homes[joint.key].node
   var delta=node.position-rig.face.homes[joint.key].pivot
   var expected=rig.face._smile_lip_offset(joint.center,joint.upper,joint.corner)
   check(absf(delta.y-expected)<.0001,row.name+" actual lip pivot y "+joint.key)
   check(absf(delta.x-rig.face._spread_x(joint.center))<.0001,row.name+" actual lip pivot x "+joint.key)
   check(node.scale==Vector2.ONE,row.name+" unit rigid lip pivot "+joint.key)
   joints.append({"key":joint.key,"upper":joint.upper,"source_x":joint.center,"delta_source_px":[delta.x,delta.y],"rotation_degrees":rad_to_deg(node.rotation),"visible":rig.face.objects[joint.key].visible})
  check(rig.face.oral_objects.upper_teeth.position==rig.face.oral_homes.upper_teeth,row.name+" fixed upper enamel")
  check(rig.face.oral_objects.upper_lip.visible==(p.mouth_purse==0),row.name+" single lip owner selection")
  for key in rig.face.objects:
   var node=rig.face.objects[key]
   check(node.texture==textures[key],row.name+" immutable texture identity "+key)
   check(node.scale==scales[key],row.name+" immutable local scale "+key)
   check(node.modulate==modulates[key] and node.self_modulate==self_modulates[key],row.name+" immutable pigment opacity "+key)
  records.append({"name":row.name,"pose":p,"brow_geometry":geometry,"lash_geometry":lash_geometry,"actual_mouth_side_delta_source_px":mouth_width,"lip_contour_offsets":lip_offsets,"actual_lip_joints":joints})
  for key in p:
   var bounds=rig.Registry.CHANNEL_BOUNDS[key]
   check(p[key]>=bounds[0] and p[key]<=bounds[1],row.name+" bounded "+key)
   check(is_equal_approx(float(p[key]),float(row.pose.get(key,0))),row.name+" requested pose "+key)
   if key not in ACTING_CHANNELS:check(p[key]==0,row.name+" excluded control "+key)
  if visual:
   await capture(row.name+"_detail",true);await capture(row.name+"_bust",false)
  rig.reset();check(rig.face.snapshot()==baseline,row.name+" exact reset")
 check(rig.list_expressions().size()==BASELINE_COUNT+7,"seven in-memory probes only")
 check(FileAccess.get_file_as_string("res://expressions/registry.json")==registry_text,"production disk registry byte exact")
 var result={"status":"PASS" if failures.is_empty() else "FAIL","checks":checks,"failures":failures,"visual_capture":visual,"baseline":baseline_freeze.baseline,"baseline_profile_count":BASELINE_COUNT,"study_poses":7,"production_registry_unchanged":true,"records":records,"scope":"Seven Bitter Taste anchors with actual brow, upper-lash and open/purse geometry checks. State and geometry do not establish native visual fidelity, normal-speed observation or approval."}
 var f=FileAccess.open(w+("/capture/checks.json" if visual else "/state_checks.json"),FileAccess.WRITE);f.store_string(JSON.stringify(result,"  "));f.close()
 print(JSON.stringify(result));quit(0 if failures.is_empty() else 1)

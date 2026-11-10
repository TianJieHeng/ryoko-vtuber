extends SceneTree
var rig
var failures=[]
var checks=0
var records=[]
var w=get_script().resource_path.get_base_dir()
var visual=false
var baseline_freeze=JSON.parse_string(FileAccess.get_file_as_string(w+"/BASELINE_FREEZE.json"))
var BASELINE_COUNT=int(baseline_freeze.baseline_profile_count)
const ACTING_CHANNELS=["brow_screen_left","brow_screen_right","brow_tilt_screen_left","brow_tilt_screen_right","blink_L","blink_R","mouth_purse","gaze_y"]
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
 var im=root.get_texture().get_image()
 var expected=Vector2i(400,360) if detail else Vector2i(568,800)
 check(im.get_size()==expected,"native dimensions "+label+" expected="+str(expected)+" actual="+str(im.get_size()))
 if im.get_size()!=expected:return
 check(im.save_png(w+"/capture/"+label+".png")==OK,"saved "+label)
func run():
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false);rig.auto_blink=false
 check(rig.rig_ready and rig.registry_ready,"rig ready")
 if not failures.is_empty():quit(1);return
 rig.hud.hide();rig.hint.hide();rig.pose_status.hide();rig.reset()
 var baseline=rig.face.snapshot();var head=rig.head.transform;var body=rig.body.transform
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
 check(plan.size()==8,"eight isolated study poses")
 for row in plan:
  var id="PROBE-129-"+row.name;var path="res://probe-129-"+row.name+".json"
  cat.entries.append({"id":id,"path":path,"aliases":[],"trigger_phase":"neutral"})
  defs[path]={"id":id,"title":row.name,"duration":3.0,"keyframes":[{"time":0.0,"phase":"neutral","values":{}},{"time":1.0,"phase":"probe","values":row.pose},{"time":2.0,"phase":"hold","values":row.pose},{"time":3.0,"phase":"neutral_return","values":{}}]}
 check(rig.registry.load_catalogue(cat,defs),"static probe catalogue: "+rig.registry.last_error)
 if not failures.is_empty():quit(1);return
 for row in plan:
  rig.reset()
  check(rig.play_expression("PROBE-129-"+row.name),row.name+" play: "+rig.last_error)
  check(rig.advance(1.5),row.name+" advance")
  var p=rig.pose_now()
  check(rig.Registry.scoped_valid(p),row.name+" scope")
  check(rig.Registry.sealed_mouth_valid(p),row.name+" mouth domain")
  check(rig.head.transform==head and rig.body.transform==body,row.name+" fixed body")
  check(not rig.auto_blink,row.name+" no automatic blink")
  check(p.blink_L==p.blink_R and p.blink_L<=.080001 and p.eye_smile_L==0 and p.eye_smile_R==0,row.name+" bounded ordinary subtle lids only")
  check(p.mouth_open==0 and p.mouth_corner_lift==0 and p.mouth_corner_lift_screen_left==0 and p.mouth_corner_lift_screen_right==0 and p.mouth_smile==0 and p.mouth_lip_press==0,row.name+" sealed unsmiling purse only")
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
  for side in ["screen_left","screen_right"]:
   var offset=rig.face.objects["iris_"+side].material.get_shader_parameter("rigid_gaze")
   check(offset.is_equal_approx(Vector2(0,2.0*float(row.pose.get("gaze_y",0)))),row.name+" actual upward iris travel "+side)
  var mouth_width=[rig.face._spread_x(4.0),rig.face._spread_x(75.0)]
  check(is_equal_approx(mouth_width[0],14.0*p.mouth_purse) and is_equal_approx(mouth_width[1],-14.0*p.mouth_purse),row.name+" actual sealed purse horizontal travel")
  var lip_offsets=[]
  for x in [4.0,39.5,75.0]:
   var upper=rig.face._smile_lip_offset(x,true,false)
   var lower=rig.face._smile_lip_offset(x,false,false)
   check(is_equal_approx(upper,lower),row.name+" no independent lower-lip push "+str(x))
   check(is_equal_approx(upper,p.mouth_purse*(4.0+8.0*pow(abs((x-39.5)/35.5),2))),row.name+" existing closed contour articulation "+str(x))
   lip_offsets.append({"x":x,"upper_y":upper,"lower_y":lower})
  records.append({"name":row.name,"pose":p,"brow_geometry":geometry,"lash_geometry":lash_geometry,"actual_mouth_side_delta_source_px":mouth_width,"lip_contour_offsets":lip_offsets})
  for key in p:
   var bounds=rig.Registry.CHANNEL_BOUNDS[key]
   check(p[key]>=bounds[0] and p[key]<=bounds[1],row.name+" bounded "+key)
   check(is_equal_approx(float(p[key]),float(row.pose.get(key,0))),row.name+" requested pose "+key)
   if key not in ACTING_CHANNELS:check(p[key]==0,row.name+" excluded control "+key)
  if visual:
   await capture(row.name+"_detail",true);await capture(row.name+"_bust",false)
  rig.reset();check(rig.face.snapshot()==baseline,row.name+" exact reset")
 check(rig.list_expressions().size()==BASELINE_COUNT+8,"eight in-memory probes only")
 check(FileAccess.get_file_as_string("res://expressions/registry.json")==registry_text,"production disk registry byte exact")
 var result={"status":"PASS" if failures.is_empty() else "FAIL","checks":checks,"failures":failures,"visual_capture":visual,"baseline":baseline_freeze.baseline,"baseline_profile_count":BASELINE_COUNT,"study_poses":8,"production_registry_unchanged":true,"records":records,"scope":"Eight Mental Arithmetic anchors with actual brow, upper-lash and sealed-purse geometry checks. State and geometry do not establish native visual fidelity, normal-speed observation or approval."}
 var f=FileAccess.open(w+("/capture/checks.json" if visual else "/state_checks.json"),FileAccess.WRITE);f.store_string(JSON.stringify(result,"  "));f.close()
 print(JSON.stringify(result));quit(0 if failures.is_empty() else 1)

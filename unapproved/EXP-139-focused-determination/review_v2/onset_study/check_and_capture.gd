extends SceneTree
var rig
var failures=[]
var checks=0
var records=[]
var w=get_script().resource_path.get_base_dir()
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
 var brow_home={}
 for side in ["screen_left","screen_right"]:brow_home[side]=rig.face.homes["brow_"+side].node.position
 var lip_y={}
 for joint in rig.face.smile_lip_joints:lip_y[joint.key]=rig.face.homes[joint.key].node.position.y
 var plan=JSON.parse_string(FileAccess.get_file_as_string(w+"/plan.json"))
 if visual:DirAccess.make_dir_recursive_absolute(w+"/capture")
 var registry_text=FileAccess.get_file_as_string("res://expressions/registry.json")
 var cat=JSON.parse_string(registry_text);var defs={}
 for entry in cat.entries:defs[entry.path]=JSON.parse_string(FileAccess.get_file_as_string(entry.path))
 check(rig.list_expressions().size()==BASELINE_COUNT,baseline_freeze.baseline+" baseline unchanged")
 check(plan.size()==6,"six isolated study poses")
 for row in plan:
  var id="PROBE-139-"+row.name;var path="res://probe-139-"+row.name+".json"
  cat.entries.append({"id":id,"path":path,"aliases":[],"trigger_phase":"neutral"})
  defs[path]={"id":id,"title":row.name,"duration":3.0,"keyframes":[{"time":0.0,"phase":"neutral","values":{}},{"time":1.0,"phase":"probe","values":row.pose},{"time":2.0,"phase":"hold","values":row.pose},{"time":3.0,"phase":"neutral_return","values":{}}]}
 check(rig.registry.load_catalogue(cat,defs),"static probe catalogue: "+rig.registry.last_error)
 if not failures.is_empty():quit(1);return
 for row in plan:
  rig.reset()
  check(rig.play_expression("PROBE-139-"+row.name),row.name+" play: "+rig.last_error)
  check(rig.advance(1.5),row.name+" advance")
  var p=rig.pose_now()
  check(rig.Registry.scoped_valid(p),row.name+" scope")
  check(rig.Registry.sealed_mouth_valid(p),row.name+" mouth domain")
  check(rig.head.transform==head and rig.body.transform==body,row.name+" fixed body")
  check(not rig.auto_blink,row.name+" no automatic blink")
  check(p.blink_L==p.blink_R and p.eye_smile_L==0 and p.eye_smile_R==0,row.name+" symmetric ordinary blink only")
  if row.name in ["neutral","reopened","selected_focus","neutral_return"]:check(p.blink_L==0 and p.blink_R==0,row.name+" fully reopened neutral lids")
  check(p.mouth_open==0 and p.mouth_corner_lift==0 and p.mouth_corner_lift_screen_left==0 and p.mouth_corner_lift_screen_right==0 and p.mouth_smile==0 and p.mouth_purse==0,row.name+" sealed unsmiling unpursed mouth")
  var geometry={}
  for side in ["screen_left","screen_right"]:
   var node=rig.face.homes["brow_"+side].node
   var delta=node.position-brow_home[side]
   check(is_equal_approx(delta.y,-10.0*float(row.pose.get("brow_"+side,0))),row.name+" actual vertical brow travel "+side)
   check(is_equal_approx(rad_to_deg(node.rotation),8.0*float(row.pose.get("brow_tilt_"+side,0))),row.name+" actual brow rotation "+side)
   check(is_zero_approx(delta.x),row.name+" no invented horizontal brow translation "+side)
   geometry[side]={"pivot_delta_source_px":[delta.x,delta.y],"rotation_degrees":rad_to_deg(node.rotation)}
  var mouth_width=[rig.face._spread_x(4.0),rig.face._spread_x(75.0)]
  check(is_equal_approx(mouth_width[0],-20.0*p.mouth_width_screen_left) and is_equal_approx(mouth_width[1],20.0*p.mouth_width_screen_right),row.name+" actual sealed mouth horizontal travel")
  for joint in rig.face.smile_lip_joints:check(is_equal_approx(rig.face.homes[joint.key].node.position.y,lip_y[joint.key]),row.name+" no outer lip vertical displacement "+joint.key)
  records.append({"name":row.name,"pose":p,"brow_geometry":geometry,"actual_mouth_side_delta_source_px":mouth_width})
  for key in p:
   check(is_equal_approx(float(p[key]),float(row.pose.get(key,0))),row.name+" requested pose "+key)
   if key not in ACTING_CHANNELS:check(p[key]==0,row.name+" excluded control "+key)
  if visual:
   await capture(row.name+"_detail",true);await capture(row.name+"_bust",false)
  rig.reset();check(rig.face.snapshot()==baseline,row.name+" exact reset")
 check(rig.list_expressions().size()==BASELINE_COUNT+6,"six in-memory probes only")
 check(FileAccess.get_file_as_string("res://expressions/registry.json")==registry_text,"production disk registry byte exact")
 var result={"status":"PASS" if failures.is_empty() else "FAIL","checks":checks,"failures":failures,"visual_capture":visual,"baseline":baseline_freeze.baseline,"baseline_profile_count":BASELINE_COUNT,"study_poses":6,"production_registry_unchanged":true,"records":records,"scope":"Neutral, half blink, closed blink, reopened face, selected C peak and neutral return. Static onset geometry/scope/reset checks only; newly authored blink, not recovered reference motion. No visual fit or approval implied."}
 var f=FileAccess.open(w+("/capture/checks.json" if visual else "/state_checks.json"),FileAccess.WRITE);f.store_string(JSON.stringify(result,"  "));f.close()
 print(JSON.stringify(result));quit(0 if failures.is_empty() else 1)

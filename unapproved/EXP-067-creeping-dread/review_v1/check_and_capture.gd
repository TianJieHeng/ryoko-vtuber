extends SceneTree
var rig
var failures=[]
var checks=0
var w=get_script().resource_path.get_base_dir()
var visual=false
var baseline_freeze=JSON.parse_string(FileAccess.get_file_as_string(w+"/BASELINE_FREEZE.json"))
var BASELINE_COUNT=int(baseline_freeze.baseline_profile_count)
const ACTING_CHANNELS=["brow_inner_lift_screen_left","brow_inner_lift_screen_right","opening_px","mouth_open","mouth_lip_press","mouth_purse"]
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
 var geometry=[]
 var plan=JSON.parse_string(FileAccess.get_file_as_string(w+"/plan.json"))
 if visual:DirAccess.make_dir_recursive_absolute(w+"/capture")
 var registry_text=FileAccess.get_file_as_string("res://expressions/registry.json")
 var cat=JSON.parse_string(registry_text);var defs={}
 for entry in cat.entries:defs[entry.path]=JSON.parse_string(FileAccess.get_file_as_string(entry.path))
 check(rig.list_expressions().size()==BASELINE_COUNT,baseline_freeze.baseline+" baseline unchanged")
 check(plan.size()==7,"seven isolated study poses")
 for row in plan:
  var id="PROBE-067-"+row.name;var path="res://probe-067-"+row.name+".json"
  cat.entries.append({"id":id,"path":path,"aliases":[],"trigger_phase":"neutral"})
  defs[path]={"id":id,"title":row.name,"duration":3.0,"keyframes":[{"time":0.0,"phase":"neutral","values":{}},{"time":1.0,"phase":"probe","values":row.pose},{"time":2.0,"phase":"hold","values":row.pose},{"time":3.0,"phase":"neutral_return","values":{}}]}
 check(rig.registry.load_catalogue(cat,defs),"static probe catalogue: "+rig.registry.last_error)
 if not failures.is_empty():quit(1);return
 for row in plan:
  rig.reset()
  check(rig.play_expression("PROBE-067-"+row.name),row.name+" play: "+rig.last_error)
  check(rig.advance(1.5),row.name+" advance")
  var p=rig.pose_now()
  check(rig.Registry.scoped_valid(p),row.name+" scope")
  check(rig.Registry.sealed_mouth_valid(p),row.name+" mouth domain")
  check(rig.head.transform==head and rig.body.transform==body,row.name+" fixed body")
  check(not rig.auto_blink,row.name+" no automatic blink")
  for key in p:
   check(is_equal_approx(float(p[key]),float(row.pose.get(key,0))),row.name+" requested pose "+key)
   if key not in ACTING_CHANNELS:check(p[key]==0,row.name+" excluded control "+key)
  check(is_equal_approx(rig.scoped_parts.eye.opening_px,float(p.opening_px)),row.name+" actual opening part")
  check(rig.face.closure==Vector2.ZERO and rig.face.gaze==Vector2.ZERO,row.name+" centered unclosed eyes")
  var pose_geometry={"name":row.name,"upper_opening_native_px":rig.scoped_parts.eye.opening_px,"brows":{}}
  for side in ["screen_left","screen_right"]:
   var home=rig.face.homes["brow_"+side]
   var anchor=rig.face.GazeLimits.BROW_OUTER_ANCHORS[side]
   var actual=home.node.transform*(anchor-home.pivot)
   check(actual.distance_to(anchor)<0.0002,row.name+" fixed outer brow anchor "+side)
   check(home.node.scale==Vector2.ONE,row.name+" unit brow scale "+side)
   pose_geometry.brows[side]={"rotation_degrees":rad_to_deg(home.node.rotation),"anchor_error_native_px":actual.distance_to(anchor)}
  var upper=rig.face._smile_lip_offset(39.5,true,false)
  var lower=rig.face._smile_lip_offset(39.5,false,false)
  pose_geometry.central_lip_gap_native_px=lower-upper
  pose_geometry.central_lip_gap_bust_px=(lower-upper)*0.49
  var expected_gap=float(p.mouth_open)*0.55*54.0-1.5*float(p.mouth_purse)*minf(float(p.mouth_open)*4.0,1.0)
  check(is_equal_approx(lower-upper,maxf(0.0,expected_gap)),row.name+" actual central lip gap")
  geometry.append(pose_geometry)
  if visual:
   await capture(row.name+"_detail",true);await capture(row.name+"_bust",false)
  rig.reset();check(rig.face.snapshot()==baseline,row.name+" exact reset")
  if not visual:await process_frame
 check(rig.list_expressions().size()==BASELINE_COUNT+7,"seven in-memory probes only")
 check(FileAccess.get_file_as_string("res://expressions/registry.json")==registry_text,"production disk registry byte exact")
 var result={"status":"PASS" if failures.is_empty() else "FAIL","checks":checks,"failures":failures,"visual_capture":visual,"baseline":baseline_freeze.baseline,"baseline_profile_count":BASELINE_COUNT,"study_poses":7,"geometry":geometry,"production_registry_unchanged":true,"scope":"Seven isolated pose/scope/reset checks only. No approval, visual fit or complete performance claim."}
 var f=FileAccess.open(w+("/capture/checks.json" if visual else "/state_checks.json"),FileAccess.WRITE);f.store_string(JSON.stringify(result,"  "));f.close()
 print(JSON.stringify(result));quit(0 if failures.is_empty() else 1)

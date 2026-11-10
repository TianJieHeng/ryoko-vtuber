extends SceneTree
var rig
var failures=[]
var checks=0
var records=[]
var w=get_script().resource_path.get_base_dir()
var visual=false
var baseline_freeze=JSON.parse_string(FileAccess.get_file_as_string(w+"/BASELINE_FREEZE.json"))
var BASELINE_COUNT=int(baseline_freeze.baseline_profile_count)
const ACTING_CHANNELS=["brow_screen_left","brow_screen_right","opening_px","mouth_open","mouth_purse","mouth_lip_press"]
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
  var id="PROBE-061-"+row.name;var path="res://probe-061-"+row.name+".json"
  cat.entries.append({"id":id,"path":path,"aliases":[],"trigger_phase":"neutral"})
  defs[path]={"id":id,"title":row.name,"duration":3.0,"keyframes":[{"time":0.0,"phase":"neutral","values":{}},{"time":1.0,"phase":"probe","values":row.pose},{"time":2.0,"phase":"hold","values":row.pose},{"time":3.0,"phase":"neutral_return","values":{}}]}
 check(rig.registry.load_catalogue(cat,defs),"static probe catalogue: "+rig.registry.last_error)
 if not failures.is_empty():quit(1);return
 for row in plan:
  rig.reset()
  check(rig.play_expression("PROBE-061-"+row.name),row.name+" play: "+rig.last_error)
  check(rig.advance(1.5),row.name+" advance")
  var p=rig.pose_now()
  check(rig.Registry.scoped_valid(p),row.name+" scope")
  check(rig.Registry.sealed_mouth_valid(p),row.name+" mouth domain")
  check(rig.head.transform==head and rig.body.transform==body,row.name+" fixed body")
  check(not rig.auto_blink,row.name+" no automatic blink")
  check(p.blink_L==0 and p.blink_R==0 and p.eye_smile_L==0 and p.eye_smile_R==0,row.name+" unclosed eyes")
  check(p.mouth_smile==0 and p.mouth_spread==0,row.name+" no smile or spread")
  var geometry={}
  for side in ["screen_left","screen_right"]:
   var node=rig.face.homes["brow_"+side].node
   var delta=node.position-brow_home[side]
   check(absf(delta.y+10.0*float(row.pose.get("brow_"+side,0)))<0.0001,row.name+" actual vertical brow travel "+side)
   check(is_zero_approx(node.rotation),row.name+" no inner brow rotation "+side)
   check(is_zero_approx(delta.x),row.name+" no horizontal brow translation "+side)
   check(node.scale==Vector2.ONE,row.name+" unit brow scale "+side)
   geometry[side]={"pivot_delta_source_px":[delta.x,delta.y],"rotation_degrees":rad_to_deg(node.rotation)}
  check(is_equal_approx(rig.scoped_parts.eye.opening_px,float(p.opening_px)),row.name+" actual upper opening part")
  check(rig.face.closure==Vector2.ZERO and rig.face.gaze==Vector2.ZERO,row.name+" centered unclosed eyes")
  var upper=rig.face._smile_lip_offset(39.5,true,false)
  var lower=rig.face._smile_lip_offset(39.5,false,false)
  var expected_gap=float(p.mouth_open)*0.55*54.0-1.5*float(p.mouth_purse)*minf(float(p.mouth_open)*4.0,1.0)
  check(is_equal_approx(lower-upper,maxf(0.0,expected_gap)),row.name+" actual central lip gap")
  records.append({"name":row.name,"pose":p,"brow_geometry":geometry,"upper_opening_native_px":rig.scoped_parts.eye.opening_px,"central_lip_gap_native_px":lower-upper,"central_lip_gap_bust_px":(lower-upper)*.49})
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
 var result={"status":"PASS" if failures.is_empty() else "FAIL","checks":checks,"failures":failures,"visual_capture":visual,"baseline":baseline_freeze.baseline,"baseline_profile_count":BASELINE_COUNT,"study_poses":8,"production_registry_unchanged":true,"records":records,"scope":"Eight Broad Surprise anchors with actual brow translation, bounded eye opening and split-lip gap checks. State and geometry do not establish native visual fidelity, normal-speed observation or approval."}
 var f=FileAccess.open(w+("/capture/checks.json" if visual else "/state_checks.json"),FileAccess.WRITE);f.store_string(JSON.stringify(result,"  "));f.close()
 print(JSON.stringify(result));quit(0 if failures.is_empty() else 1)

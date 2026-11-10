extends SceneTree
var rig
var failures=[]
var checks=0
var records=[]
var w=get_script().resource_path.get_base_dir()
var visual=false
var baseline_freeze=JSON.parse_string(FileAccess.get_file_as_string(w+"/BASELINE_FREEZE.json"))
var BASELINE_COUNT=int(baseline_freeze.baseline_profile_count)
const ACTING_CHANNELS=["brow_screen_left","brow_screen_right","blink_L","blink_R","eye_smile_L","eye_smile_R","mouth_smile","mouth_corner_lift"]
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
 var brow_home={};var lash_home={}
 for side in ["screen_left","screen_right"]:
  brow_home[side]=rig.face.homes["brow_"+side].node.position
  lash_home[side]=rig.face.homes["upper_lash_"+side].node.position
 var plan=JSON.parse_string(FileAccess.get_file_as_string(w+"/plan.json"))
 if visual:DirAccess.make_dir_recursive_absolute(w+"/capture")
 var registry_text=FileAccess.get_file_as_string("res://expressions/registry.json")
 var cat=JSON.parse_string(registry_text);var defs={}
 for entry in cat.entries:defs[entry.path]=JSON.parse_string(FileAccess.get_file_as_string(entry.path))
 check(rig.list_expressions().size()==BASELINE_COUNT,baseline_freeze.baseline+" baseline unchanged")
 check(rig.registry.resolve("EXP-003")=="","candidate absent from baseline")
 check(plan.size()==7,"six primary anchors plus one alternative")
 for row in plan:
  var id="PROBE-003-"+row.name;var path="res://probe-003-"+row.name+".json"
  cat.entries.append({"id":id,"path":path,"aliases":[],"trigger_phase":"neutral"})
  defs[path]={"id":id,"title":row.name,"duration":3.0,"keyframes":[{"time":0.0,"phase":"neutral","values":{}},{"time":1.0,"phase":"probe","values":row.pose},{"time":2.0,"phase":"hold","values":row.pose},{"time":3.0,"phase":"neutral_return","values":{}}]}
 check(rig.registry.load_catalogue(cat,defs),"static probes: "+rig.registry.last_error)
 if not failures.is_empty():quit(1);return
 for row in plan:
  rig.reset();check(rig.play_expression("PROBE-003-"+row.name),row.name+" play");check(rig.advance(1.5),row.name+" advance")
  var p=rig.pose_now()
  check(rig.Registry.scoped_valid(p),row.name+" scope");check(rig.Registry.sealed_mouth_valid(p),row.name+" sealed mouth domain")
  check(rig.head.transform==head and rig.body.transform==body,row.name+" fixed body")
  check(not rig.auto_blink,row.name+" no automatic blink")
  check(is_equal_approx(p.eye_smile_L,p.eye_smile_R) and is_equal_approx(p.blink_L,p.blink_R),row.name+" symmetric eye controls")
  check(p.mouth_open==0 and p.mouth_spread==0 and p.mouth_purse==0,row.name+" sealed small smile, no widening or purse")
  var geometry={}
  for side in ["screen_left","screen_right"]:
   var node=rig.face.homes["brow_"+side].node;var delta=node.position-brow_home[side]
   check(absf(delta.y+10.0*float(row.pose.get("brow_"+side,0)))<.0001,row.name+" actual brow lowering "+side)
   check(is_zero_approx(delta.x) and is_zero_approx(node.rotation),row.name+" no additional brow tilt or horizontal shift "+side)
   var smile=p.eye_smile_L if side=="screen_left" else p.eye_smile_R
   var blink=p.blink_L if side=="screen_left" else p.blink_R
   var closure=maxf(blink,minf(smile*2.0,1.0));var shape=clampf((smile-.5)*2.0,0.0,1.0)
   var lash=rig.face.homes["upper_lash_"+side].node;var lash_delta=lash.position-lash_home[side]
   check(absf(lash_delta.y-36.0*closure)<.0001 and is_zero_approx(lash_delta.x),row.name+" actual ordinary upper-lash handoff travel "+side)
   check(is_equal_approx(rig.face.objects["iris_"+side].material.get_shader_parameter("closure"),closure),row.name+" actual canonical aperture closure "+side)
   var joint_count=0;var max_travel=0.0
   for joint in rig.face.smile_eye_joints:
    if joint.side!=side:continue
    joint_count+=1
    var eye_node=rig.face.objects[joint.key]
    var common=lerpf(joint.old_center,joint.new_center,shape)
    var offset=common-(joint.old_center if joint.old else joint.new_center)
    var actual=rig.face.homes[joint.key].node.position-rig.face.homes[joint.key].pivot
    var angle=atan(joint.slope_delta*(shape if joint.old else shape-1.0))
    check(absf(actual.y-offset)<.0001 and is_zero_approx(actual.x),row.name+" rigid smiling eye joint "+joint.key)
    check(is_equal_approx(rig.face.homes[joint.key].node.rotation,angle),row.name+" eye joint rotation "+joint.key)
    check(eye_node.visible==(shape>0.0),row.name+" curved eye owner handoff "+joint.key)
    check(is_equal_approx(eye_node.material.get_shader_parameter("shape"),shape),row.name+" shape shader "+joint.key)
    if eye_node.visible:max_travel=maxf(max_travel,absf(actual.y))
   check(joint_count>0,row.name+" preserved smiling eye joints exist")
   geometry[side]={"brow_pivot_delta_source_px":[delta.x,delta.y],"brow_rotation_degrees":rad_to_deg(node.rotation),"ordinary_upper_lash_delta_source_px":[lash_delta.x,lash_delta.y],"effective_closure":closure,"closed_eye_shape":shape,"smile_eye_joint_count":joint_count,"max_visible_eye_joint_travel_source_px":max_travel}
  var lip_offsets=[]
  for x in [4.0,21.75,39.5,57.25,75.0]:
   var upper=rig.face._smile_lip_offset(x,true,false);var lower=rig.face._smile_lip_offset(x,false,false)
   var radius=absf((x-39.5)/35.5)
   var expected=-4.0*p.mouth_smile*pow(radius,1.5)-12.0*p.mouth_corner_lift*pow(radius,3)
   check(is_equal_approx(upper,lower),row.name+" sealed lip contours "+str(x))
   check(is_equal_approx(upper,expected),row.name+" actual gentle symmetric lip curve "+str(x))
   check(is_zero_approx(rig.face._spread_x(x)),row.name+" no mouth widening "+str(x))
   lip_offsets.append({"x":x,"upper_y":upper,"lower_y":lower})
  records.append({"name":row.name,"pose":p,"geometry":geometry,"lip_offsets_source_px":lip_offsets})
  for key in p:
   var bounds=rig.Registry.CHANNEL_BOUNDS[key]
   check(p[key]>=bounds[0] and p[key]<=bounds[1],row.name+" bounded "+key)
   check(is_equal_approx(float(p[key]),float(row.pose.get(key,0))),row.name+" requested pose "+key)
   if key not in ACTING_CHANNELS:check(p[key]==0,row.name+" excluded control "+key)
  if visual:await capture(row.name+"_detail",true);await capture(row.name+"_bust",false)
  rig.reset();check(rig.face.snapshot()==baseline,row.name+" exact object reset")
 check(rig.list_expressions().size()==BASELINE_COUNT+7,"seven in-memory probes only")
 check(FileAccess.get_file_as_string("res://expressions/registry.json")==registry_text,"production disk registry unchanged")
 var result={"status":"PASS" if failures.is_empty() else "FAIL","checks":checks,"failures":failures,"visual_capture":visual,"baseline":baseline_freeze.baseline,"baseline_profile_count":BASELINE_COUNT,"study_poses":7,"production_registry_unchanged":true,"records":records,"scope":"Actual node, shader and lip-curve geometry only. Ordinary upper-lash travel is a closure/handoff measure, not proof that a lash is visible. Native visual fidelity, perception and approval remain unverified."}
 var f=FileAccess.open(w+("/capture/checks.json" if visual else "/state_checks.json"),FileAccess.WRITE);f.store_string(JSON.stringify(result,"  "));f.close()
 print("STATIC_",result.status," checks=",checks," failures=",failures);quit(0 if failures.is_empty() else 1)

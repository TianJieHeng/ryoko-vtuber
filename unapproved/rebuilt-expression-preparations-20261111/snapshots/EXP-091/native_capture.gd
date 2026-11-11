extends SceneTree
# PREPARATION ONLY. This fresh scaffold has NOT been parsed or run by Godot.
# Prior native launches were denied. No alternate headless/display route is allowed.
# A new authorized revision and author freeze are required before enabling it.
const NATIVE_EXECUTION_ALLOWED=false
var w=get_script().resource_path.get_base_dir()
var rig
var failures=[]
var checks=0
var frame_records=[]
var static_records=[]
var lifecycle_records=[]
var frozen
var definition
var head
var body
var registry_text
func _initialize():
 if not NATIVE_EXECUTION_ALLOWED:
  push_error("BLOCKED: native execution disabled. No renderer, state test or capture authorized.")
  quit(2)
  return
 if DisplayServer.get_name()=="headless":
  push_error("Headless output is not native review evidence.");quit(2);return
 call_deferred("run")
func check(ok,label):
 checks+=1
 if not ok:failures.append(label)
func hash_file(path):return FileAccess.get_sha256(path)
func json_file(path):return JSON.parse_string(FileAccess.get_file_as_string(path))
func fail_fast():
 if not failures.is_empty():
  push_error(str(failures));quit(1);return true
 return false
func audit_pose(p,label):
 check(rig.Registry.scoped_valid(p),label+" valid scope")
 check(rig.Registry.sealed_mouth_valid(p),label+" valid mouth domain")
 check(rig.head.transform==head and rig.body.transform==body,label+" fixed head/body")
 check(p.blink_L==p.blink_R and p.eye_smile_L==p.eye_smile_R,label+" symmetric eyes")
 for key in p:
  var bounds=rig.Registry.CHANNEL_BOUNDS[key]
  check(p[key]>=bounds[0] and p[key]<=bounds[1],label+" bounds "+key)
 for key in ["opening_px","aversion_px","uneasy_weight","gaze_x","gaze_y","gaze_down_extra","hair_sway","mouth_spread","mouth_kiss","mouth_oral_lift","mouth_width_screen_left","mouth_width_screen_right","mouth_corner_lift_screen_left","mouth_corner_lift_screen_right"]:
  check(p[key]==0,label+" excluded "+key)
 for side in ["screen_left","screen_right"]:
  var eye=p.eye_smile_R if side=="screen_left" else p.eye_smile_L
  var blink=p.blink_R if side=="screen_left" else p.blink_L
  var closure=maxf(blink,minf(eye*2.0,1.0))
  check(is_equal_approx(rig.face.objects["iris_"+side].material.get_shader_parameter("closure"),closure),label+" effective iris closure "+side)
  var lash=rig.face.homes["upper_lash_"+side]
  check((lash.node.position-lash.pivot).distance_to(Vector2(0,36.0*closure))<.0001,label+" effective rigid lash travel "+side)
  var brow=rig.face.homes["brow_"+side]
  var legacy=deg_to_rad(8*p["brow_tilt_"+side])
  var lift=deg_to_rad((-26 if side=="screen_left" else 26)*p["brow_inner_lift_"+side])
  var a=rig.Registry.Limits.BROW_OUTER_ANCHORS[side]-brow.pivot
  var expected=Vector2(0,-10*p["brow_"+side])+(a-a.rotated(lift)).rotated(legacy)
  check((brow.node.position-brow.pivot).distance_to(expected)<.0001,label+" rigid brow position "+side)
  check(is_equal_approx(brow.node.rotation,legacy+lift),label+" rigid brow angle "+side)
  check(brow.node.scale==Vector2.ONE,label+" rigid brow scale "+side)
 for joint in rig.face.smile_eye_joints:
  var eye=p.eye_smile_R if joint.side=="screen_left" else p.eye_smile_L
  var shape=clampf((eye-.5)*2,0,1)
  var node=rig.face.objects[joint.key]
  check(is_equal_approx(node.material.get_shader_parameter("shape"),shape),label+" actual curved lash shape "+joint.key)
  check(node.visible==(shape>0),label+" curved lash visibility "+joint.key)
 for x in [4.0,39.5,75.0]:
  var radius=absf((x-39.5)/35.5)
  var expected=-4*p.mouth_smile*pow(radius,1.5)-12*p.mouth_corner_lift*pow(radius,3)+p.mouth_purse*(4+8*radius*radius)
  var upper=rig.face._smile_lip_offset(x,true,false)
  var lower=rig.face._smile_lip_offset(x,false,false)
  check(is_equal_approx(upper,expected),label+" lip contour "+str(x))
  check(lower>=upper-.00001,label+" nonnegative gap "+str(x))
  if p.mouth_open==0:check(is_equal_approx(lower,upper),label+" sealed actual lips "+str(x))
 check(is_equal_approx(rig.face._spread_x(4),14*p.mouth_purse),label+" inward left lip")
 check(is_equal_approx(rig.face._spread_x(75),-14*p.mouth_purse),label+" inward right lip")
 for owner in rig.face.pressed_lip_owners:
  check(is_equal_approx(owner.node.material.get_shader_parameter("lip_press"),p.mouth_lip_press),label+" pressure amount")
  check(owner.node.visible==(p.mouth_lip_press>0),label+" pressure owner")
 check(is_equal_approx(rig.face.blush_intensity,p.blush_intensity),label+" separate blush amount")
 check(not rig.auto_blink,label+" auto-blink disabled")
func snap(relative,detail):
 root.size=Vector2i(568,800);root.canvas_transform=Transform2D.IDENTITY
 if detail:
  root.size=Vector2i(400,360)
  var camera=Transform2D.IDENTITY.scaled(Vector2.ONE/.49)
  camera.origin=-Vector2(6,70)/.49-Vector2(380,380)
  root.canvas_transform=camera
 await process_frame;await process_frame;await RenderingServer.frame_post_draw
 var im=root.get_texture().get_image()
 var expected=Vector2i(400,360) if detail else Vector2i(568,800)
 check(im.get_size()==expected,"actual capture dimensions "+relative)
 check(im.get_format()==Image.FORMAT_RGBA8,"actual capture RGBA8 "+relative)
 if not failures.is_empty():return {}
 check(im.save_png(w+"/capture/"+relative)==OK,"save "+relative)
 var ctx=HashingContext.new();ctx.start(HashingContext.HASH_SHA256);ctx.update(im.get_data())
 return {"path":relative,"width":expected.x,"height":expected.y,"rgba_sha256":ctx.finish().hex_encode(),"file_sha256":hash_file(w+"/capture/"+relative)}
func run():
 check(not DirAccess.dir_exists_absolute(w+"/capture"),"preserve existing captures")
 if fail_fast():return
 frozen=json_file(w+"/INPUT_FREEZE.json")
 check(frozen!=null,"input freeze exists")
 if fail_fast():return
 for file in frozen.files:check(hash_file(w+"/"+file)==frozen.files[file],"frozen input "+file)
 if fail_fast():return
 definition=json_file(w+"/EXP-091.json")
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false);rig.auto_blink=false
 check(rig.rig_ready and rig.registry_ready,"rig ready")
 check(rig.list_expressions().size()==39,"approved39 count")
 if fail_fast():return
 rig.hud.hide();rig.hint.hide();rig.pose_status.hide();rig.reset()
 head=rig.head.transform;body=rig.body.transform
 var baseline=rig.face.snapshot()
 registry_text=FileAccess.get_file_as_string("res://expressions/registry.json")
 var cat=JSON.parse_string(registry_text);var definitions={}
 for e in cat.entries:definitions[e.path]=json_file(e.path)
 cat.entries.append({"id":"EXP-091","path":"res://preview-091.json","aliases":[],"trigger_phase":"neutral"})
 definitions["res://preview-091.json"]=definition
 check(rig.registry.load_catalogue(cat,definitions),"in-memory candidate validation")
 check(rig.list_expressions().size()==40,"39 plus one preview only")
 if fail_fast():return
 DirAccess.make_dir_recursive_absolute(w+"/capture/static")
 DirAccess.make_dir_recursive_absolute(w+"/capture/full")
 DirAccess.make_dir_recursive_absolute(w+"/capture/detail")
 var plan=json_file(w+"/plan.json")
 for row in plan:
  rig.reset();check(rig.apply_controls(row.pose),"static controls "+row.name)
  var p=rig.pose_now();audit_pose(p,row.name)
  for key in p:check(is_equal_approx(p[key],float(row.pose.get(key,0))),"requested static pose "+row.name+key)
  if fail_fast():return
  static_records.append({"name":row.name,"pose":p,"views":[await snap("static/"+row.name+"_full.png",false),await snap("static/"+row.name+"_detail.png",true)]})
 rig.reset();check(rig.play_expression("EXP-091"),"play candidate")
 for i in range(121):
  if i>0:check(rig.advance(maxf(0,float(i)/30-rig.performance_time)),"timeline advance")
  var p=rig.pose_now();audit_pose(p,"frame "+str(i))
  if fail_fast():return
  frame_records.append({"frame":i,"time":float(i)/30,"pose":p,"views":[await snap("full/%04d.png"%i,false),await snap("detail/%04d.png"%i,true)]})
 check(rig.face.snapshot()==baseline,"exact object neutral return")
 for view in range(2):check(frame_records[0].views[view].rgba_sha256==frame_records[-1].views[view].rgba_sha256,"exact neutral pixels")
 for t in [.35,.55,.9,1.25,1.65,2.25,2.75,3.3,3.75]:
  for stage in ["restart","release"]:
   rig.reset();rig.play_expression("EXP-091");rig.advance(t)
   var source=rig.pose_now()
   if stage=="restart":rig.play_expression("EXP-091")
   else:rig.release()
   check(rig.pose_now()==source,"interruption continuity")
   for step in range(13 if stage=="restart" else 17):
    if step>0:rig.advance(1.0/30)
    var p=rig.pose_now();audit_pose(p,"lifecycle")
    lifecycle_records.append({"interruption_time":t,"stage":stage,"step":step,"pose":p})
   if stage=="release":check(rig.pose_now()==rig.neutral_pose(),"release exact neutral")
   rig.reset();check(rig.face.snapshot()==baseline,"interrupted reset neutral")
 check(FileAccess.get_file_as_string("res://expressions/registry.json")==registry_text,"disk registry unchanged")
 var receipt={"status":"PASS" if failures.is_empty() else "FAIL","failures":failures,"checks":checks,"visual_capture":true,"display":DisplayServer.get_name(),"renderer":RenderingServer.get_current_rendering_method(),"input_freeze_sha256":hash_file(w+"/INPUT_FREEZE.json"),"profile_sha256":hash_file(w+"/EXP-091.json"),"baseline_profile_count":39,"fps":30,"duration":4.0,"frames":121,"records":frame_records,"static_records":static_records,"lifecycle_records":lifecycle_records,"source_fidelity":"PENDING independent visual review","approval":"UNAPPROVED"}
 var f=FileAccess.open(w+"/capture/evidence.json",FileAccess.WRITE);f.store_string(JSON.stringify(receipt,"  "));f.close()
 quit(0 if failures.is_empty() else 1)

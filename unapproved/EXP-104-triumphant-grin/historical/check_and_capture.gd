extends SceneTree
var rig
var failures=[]
var checks=0
var records=[]
var w=get_script().resource_path.get_base_dir()
var visual=false
var baseline_freeze=JSON.parse_string(FileAccess.get_file_as_string(w+"/BASELINE_FREEZE.json"))
var BASELINE_COUNT=int(baseline_freeze.baseline_profile_count)
const ACTING_CHANNELS=["brow_screen_left","brow_screen_right","brow_tilt_screen_left","brow_tilt_screen_right","blink_L","blink_R","mouth_smile","mouth_spread","mouth_open"]
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
  var id="PROBE-104-"+row.name;var path="res://probe-104-"+row.name+".json"
  cat.entries.append({"id":id,"path":path,"aliases":[],"trigger_phase":"neutral"})
  defs[path]={"id":id,"title":row.name,"duration":3.0,"keyframes":[{"time":0.0,"phase":"neutral","values":{}},{"time":1.0,"phase":"probe","values":row.pose},{"time":2.0,"phase":"hold","values":row.pose},{"time":3.0,"phase":"neutral_return","values":{}}]}
 check(rig.registry.load_catalogue(cat,defs),"static probe catalogue: "+rig.registry.last_error)
 if not failures.is_empty():quit(1);return
 for row in plan:
  rig.reset()
  check(rig.play_expression("PROBE-104-"+row.name),row.name+" play: "+rig.last_error)
  check(rig.advance(1.5),row.name+" advance")
  var p=rig.pose_now()
  check(rig.Registry.scoped_valid(p),row.name+" scope")
  check(rig.Registry.sealed_mouth_valid(p),row.name+" mouth domain")
  check(rig.head.transform==head and rig.body.transform==body,row.name+" fixed body")
  check(not rig.auto_blink,row.name+" no automatic blink")
  check(p.blink_R==p.blink_L and p.blink_R<=.120001 and p.eye_smile_L==0 and p.eye_smile_R==0,row.name+" equal focused ordinary partial lids")
  check(p.mouth_corner_lift==0 and p.mouth_corner_lift_screen_left==0 and p.mouth_corner_lift_screen_right==0 and p.mouth_purse==0,row.name+" no purse or independent/common corner lift")
  check(p.mouth_width_screen_left==0 and p.mouth_width_screen_right==0 and p.mouth_kiss==0,row.name+" no sealed-only width or kiss during open mouth")
  var geometry={}
  for side in ["screen_left","screen_right"]:
   var node=rig.face.homes["brow_"+side].node
   var delta=node.position-brow_home[side]
   var legacy=deg_to_rad(8.0*float(row.pose.get("brow_tilt_"+side,0)))
   var inner=float(row.pose.get("brow_inner_lift_"+side,0))
   var lift=deg_to_rad((-26.0 if side=="screen_left" else 26.0)*inner)
   var pivot=rig.face.homes["brow_"+side].pivot
   var outer=rig.Registry.Limits.BROW_OUTER_ANCHORS[side]
   var a=outer-pivot
   var vertical=Vector2(0,-10.0*float(row.pose.get("brow_"+side,0)))
   var expected=vertical+(a-a.rotated(lift)).rotated(legacy)
   check(delta.distance_to(expected)<.0001,row.name+" actual outer-anchor brow travel "+side)
   check(is_equal_approx(node.rotation,legacy+lift),row.name+" actual composed brow rotation "+side)
   check((node.position+a.rotated(node.rotation)).is_equal_approx(pivot+vertical+a.rotated(legacy)),row.name+" inner lift preserves transformed outer anchor "+side)
   check(node.scale==Vector2.ONE,row.name+" rigid brow unit scale "+side)
   geometry[side]={"pivot_delta_source_px":[delta.x,delta.y],"rotation_degrees":rad_to_deg(node.rotation),"inner_lift":inner,"outer_anchor":[outer.x,outer.y]}
  var lash_geometry={}
  for side in ["screen_left","screen_right"]:
   var node=rig.face.homes["upper_lash_"+side].node
   var delta=node.position-lash_home[side]
   var amount=p.blink_R if side=="screen_left" else p.blink_L
   check(absf(delta.y-36.0*amount)<.0001,row.name+" actual rigid upper-lash travel "+side)
   check(is_zero_approx(delta.x),row.name+" no horizontal upper-lash travel "+side)
   check(is_equal_approx(rig.face.objects["iris_"+side].material.get_shader_parameter("closure"),amount),row.name+" iris uses matching closure "+side)
   lash_geometry[side]={"pivot_delta_source_px":[delta.x,delta.y],"closure":amount}
  for side in ["screen_left","screen_right"]:
   var offset=rig.face.objects["iris_"+side].material.get_shader_parameter("rigid_gaze")
   check(offset.is_equal_approx(Vector2.ZERO),row.name+" fixed forward iris position "+side)
  check(is_equal_approx(rig.face.mouth_spread,p.mouth_spread*p.mouth_smile),"effective spread includes smile product")
  for tooth in rig.face.spread_teeth:
   var left=tooth.name.ends_with("left")
   var spread=p.mouth_spread*p.mouth_smile
   var anchor=Vector2(553 if left else 577,619)
   var origin=Vector2(532 if left else 553,605)
   var angle=(1.0 if left else -1.0)*.12*spread
   var expected=anchor+(origin-anchor).rotated(angle)+Vector2((-20.0 if left else 20.0)*spread,9.0*spread)
   check(tooth.position.distance_to(expected)<.0001,"passively coupled upper tooth support position")
   check(is_equal_approx(tooth.rotation,angle),"passively coupled upper tooth support rotation")
   check(tooth.visible==(spread>0),"coupled tooth support visibility flag, not pixel exposure")
  var mouth_width=[rig.face._spread_x(4.0),rig.face._spread_x(75.0)]
  check(is_equal_approx(mouth_width[0],-20.0*p.mouth_spread*p.mouth_smile) and is_equal_approx(mouth_width[1],--20.0*p.mouth_spread*p.mouth_smile),row.name+" actual symmetric effective spread travel")
  check(is_zero_approx(rig.face._spread_x(39.5)),row.name+" mouth center does not translate")
  check(is_zero_approx(mouth_width[0]+mouth_width[1]),row.name+" symmetric horizontal mouth width, no translation")
  for x in range(4,75):
   check(float(x+1)+rig.face._spread_x(x+1)>float(x)+rig.face._spread_x(x),row.name+" horizontal contour monotonic "+str(x))
  var lip_offsets=[]
  for x in [4.0,39.5,75.0]:
   var upper=rig.face._smile_lip_offset(x,true,false)
   var lower=rig.face._smile_lip_offset(x,false,false)
   check(lower>=upper,row.name+" nonnegative opening "+str(x))
   check(is_equal_approx(upper,-4.0*p.mouth_spread*p.mouth_smile-(4.0+5.0*p.mouth_spread*p.mouth_smile)*p.mouth_smile*pow(abs((x-39.5)/35.5),1.5)),row.name+" symmetric smile upper contour "+str(x))
   lip_offsets.append({"x":x,"upper_y":upper,"lower_y":lower})
  var upper=rig.face._smile_lip_offset(39.5,true,false)
  var lower=rig.face._smile_lip_offset(39.5,false,false)
  var expected_gap=maxf(0.0,float(p.mouth_open)*0.55*54.0-1.5*float(p.mouth_purse)*minf(float(p.mouth_open)*4.0,1.0))
  check(is_equal_approx(lower-upper,expected_gap),row.name+" actual central split-lip gap")
  check(is_equal_approx(rig.face.mouth_lip_press,p.mouth_lip_press),row.name+" actual pressure state")
  check(is_equal_approx(rig.face._smile_lip_offset(4.0,false,false)-rig.face._smile_lip_offset(75.0,false,false),12.0*p.mouth_corner_lift_screen_right),row.name+" corner lift moves both lip contours, not upper lip alone")
  records.append({"name":row.name,"pose":p,"brow_geometry":geometry,"lash_geometry":lash_geometry,"actual_mouth_side_delta_source_px":mouth_width,"lip_contour_offsets":lip_offsets,"central_lip_gap_native_px":lower-upper,"central_lip_gap_bust_px":(lower-upper)*.49})
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
 var result={"status":"PASS" if failures.is_empty() else "FAIL","checks":checks,"failures":failures,"visual_capture":visual,"plan_sha256":FileAccess.get_sha256(w+"/plan.json"),"baseline_freeze_sha256":FileAccess.get_sha256(w+"/BASELINE_FREEZE.json"),"baseline":baseline_freeze.baseline,"baseline_profile_count":BASELINE_COUNT,"study_poses":8,"production_registry_unchanged":true,"records":records,"scope":"Eight Triumphant Grin anchors with bilateral low inward-angled brows, equal ordinary focused lids and a centered tooth-bearing then more open smile. Existing tooth support is coupled to smile/spread; no independent dental control, clench or new anatomy. State and geometry do not establish native visual fidelity, normal-speed observation or approval."}
 var f=FileAccess.open(w+("/capture/checks.json" if visual else "/state_checks.json"),FileAccess.WRITE);f.store_string(JSON.stringify(result,"  "));f.close()
 print(JSON.stringify(result));quit(0 if failures.is_empty() else 1)

extends SceneTree
const ID="EXP-181"
const PRIOR=["EXP-163","EXP-005","EXP-001","EXP-006","EXP-107","EXP-007","EXP-002","EXP-152","EXP-160","EXP-177","EXP-164","EXP-021"]
const ALLOWED=["blink_R","blink_L","eye_smile_L","brow_screen_left","brow_tilt_screen_left","brow_tilt_screen_right","mouth_smile","mouth_spread","mouth_open","mouth_corner_lift_screen_right"]
var rig
var checks=0
var failures=[]
var pigment={}
var head_home
var body_home
func _initialize():call_deferred("run")
func check(ok,label):
 checks+=1
 if not ok:
  failures.append(label)
  if failures.size()<15:push_error(label)
func state():
 var s=rig.get_state();s.erase("last_error");s.face=rig.face.snapshot();return s
func neutral(label,blink=false):
 check(rig.pose_now()==rig.neutral_pose(),label+" exact neutral")
 check(rig.active_performance=="" and rig.release_time<0,label+" idle")
 check(rig.auto_blink==blink and not rig.auto_blink_pending_restore,label+" blink policy")
func anatomy():
 check(rig.head.transform==head_home and rig.body.transform==body_home,"fixed head/neck/body")
 check(rig.face.oral_objects.upper_teeth.position==Vector2(533,626),"fixed central enamel")
 for k in rig.face.objects:
  var n=rig.face.objects[k];var p=rig.face.homes[k].node
  check(n.scale==Vector2.ONE and p.scale==Vector2.ONE and n.modulate==Color.WHITE and n.self_modulate==Color.WHITE,"rigid opaque owner")
  check([n.texture,n.region_rect,n.region_enabled,n.offset,n.flip_h,n.flip_v]==pigment[k],"fixed texture UV")
func run():
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 check(rig.rig_ready and rig.registry_ready,"ready")
 if not rig.rig_ready or not rig.registry_ready:quit(2);return
 head_home=rig.head.transform;body_home=rig.body.transform
 for k in rig.face.objects:
  var n=rig.face.objects[k];pigment[k]=[n.texture,n.region_rect,n.region_enabled,n.offset,n.flip_h,n.flip_v]
 var ids=[]
 for e in rig.list_expressions():ids.append(e.id)
 check(ids==["EXP-163","EXP-005","EXP-001","EXP-006","EXP-107","EXP-007","EXP-002","EXP-152","EXP-160","EXP-177","EXP-164","EXP-021","EXP-158","EXP-181","EXP-102","EXP-116","EXP-050","EXP-186"],"exact eighteen approved registry IDs")
 for id in ["EXP-003","EXP-097","EXP-139","EXP-170"]:check(rig.registry.resolve(id)=="","no unrelated profile "+id)
 for a in [ID,"cheeky-wink","cheeky_wink"]:check(rig.registry.resolve(a)==ID,"alias")
 var d=rig.registry.definition(ID)
 check(d.duration==3.10 and d.keyframes.size()==10,"ten authored keys and3.10s")
 check(d.timing_origin.contains("Newly authored") and d.timing_origin.contains("unimplemented reference"),"honest static source timing")
 var anchors=JSON.parse_string(FileAccess.get_file_as_string("res://source_references/cheeky_wink_source_anchor_map.json"))
 var static_plan=JSON.parse_string(FileAccess.get_file_as_string("res://source_references/cheeky_wink_accepted_static_plan.json"))
 for a in anchors.anchors:
  var p=rig.sample_expression(ID,a.time)
  for k in rig.CHANNELS:check(is_equal_approx(p[k],a.values.get(k,0)),"exact authored source anchor")
  for e in static_plan.candidate_cases:
   if e.source_key!=a.key_pose:continue
   for k in rig.CHANNELS:check(is_equal_approx(p[k],e.values.get(k,0)),"accepted static pose exact")
 var prev=rig.neutral_pose()
 for i in range(3101):
  var t=i*.001;var p=rig.sample_expression(ID,t)
  for k in p:
   var b=rig.Registry.CHANNEL_BOUNDS[k];check(p[k]>=b[0] and p[k]<=b[1],"bounded trajectory")
   if k not in ALLOWED:check(p[k]==0,"unrelated channel zero "+k)
  check(p.blink_R<=.060001 and p.eye_smile_R==0,"opposite eye attentive")
  check(p.mouth_open<=.160001 and p.mouth_corner_lift_screen_right<=.850001 and p.mouth_smile<=.760001 and p.mouth_spread<=.950001,"accepted source envelope")
  if t<=1.02 or t>=1.62:check(p.mouth_open<.000001,"sealed outside single enamel pulse")
  if t>=.68 and t<=1.62:check(is_equal_approx(p.blink_L,1) and is_equal_approx(p.eye_smile_L,.7),"single sustained tightened wink")
  if i>0 and t<=1.24:check(p.mouth_corner_lift_screen_right>=prev.mouth_corner_lift_screen_right-.000001,"one monotone smile build")
  if t>1.24:check(p.mouth_corner_lift_screen_right<=prev.mouth_corner_lift_screen_right+.000001,"one smile recovery")
  prev=p
 for origin in [.1,.299999,.3,.68,1.02,1.24,1.62,2.08,2.94,3.09]:
  for wanted in [false,true]:
   for action in ["release","repeat_release","retrigger","manual","reset"]+PRIOR:
    rig.reset();rig.apply_controls({"auto_blink":wanted});rig.play_expression(ID);rig.advance(origin);var before=rig.displayed_pose()
    if action in ["release","repeat_release"]:
     check(rig.release() and rig.displayed_pose()==before,"release C0")
     if action=="repeat_release":rig.advance(.17);before=rig.displayed_pose();check(rig.release() and rig.displayed_pose()==before,"repeat release C0")
     rig.advance(.45);neutral("release",wanted)
    elif action=="retrigger" or action in PRIOR:
     var destination=ID if action=="retrigger" else action
     check(rig.play_expression(destination) and rig.displayed_pose()==before,"handover C0")
     rig.advance(rig.registry.definition(destination).duration);neutral("destination",wanted)
    elif action=="manual":
     check(rig.apply_controls({"mouth_corner_lift_screen_right":.3}),"manual takeover")
     var held=rig.pose_now();rig.advance(8);check(rig.pose_now()==held and rig.active_performance=="" and rig.release_time<0 and not rig.auto_blink_pending_restore and not rig.auto_blink,"manual stays owner")
     rig.reset();neutral("manual reset")
    else:rig.reset();neutral("reset")
    anatomy()
 for id in PRIOR:
  rig.reset();rig.apply_controls({"auto_blink":true});rig.play_expression(id);rig.advance(rig.registry.definition(id).duration*.5);var before=rig.displayed_pose()
  check(rig.play_expression(ID) and rig.displayed_pose()==before,"incoming C0");rig.advance(3.1);neutral("incoming completion",true)
 for action in ["natural","release","retrigger"]:
  rig.reset();rig.apply_controls({"auto_blink":true});rig.advance(4.03);check(rig.face.closure.x>.99,"initial visible blink")
  var before=rig.displayed_pose();check(rig.play_expression(ID) and rig.displayed_pose()==before and not rig.auto_blink and rig.auto_blink_pending_restore,"blink suspension C0");rig.advance(1.24)
  if action=="release":rig.release();rig.advance(.45)
  elif action=="retrigger":rig.play_expression(ID);rig.advance(3.1)
  else:rig.advance(3.1)
  neutral("blink restores",true);rig.advance(4.03);check(rig.face.closure.x>.99,"restored cycle works")
 for mode in ["manual","active","release"]:
  rig.reset();rig.play_expression(ID);rig.advance(1.24)
  if mode=="release":rig.release();rig.advance(.17)
  if mode=="manual":rig.apply_controls({"mouth_open":.3})
  for key in rig.Registry.CHANNEL_BOUNDS:
   var b=rig.Registry.CHANNEL_BOUNDS[key]
   for bad in [b[0]-.000001,b[1]+.000001,NAN,INF,true,"1",null]:
    var saved=state();check(not rig.apply_controls({"reset":true,key:bad}),"invalid input rejected");check(state()==saved,"invalid input atomic")
 var defs={};var cat=JSON.parse_string(FileAccess.get_file_as_string("res://expressions/registry.json"))
 for e in cat.entries:defs[e.path]=JSON.parse_string(FileAccess.get_file_as_string(e.path))
 for mode in ["bad_time","bad_end","bad_side"]:
  var bad=defs.duplicate(true);var entry=bad["res://expressions/EXP-181.json"]
  if mode=="bad_time":entry.keyframes[2].time=.1
  elif mode=="bad_end":entry.keyframes[9].values.mouth_corner_lift_screen_right=.1
  else:entry.keyframes[4].values.mouth_corner_lift_screen_right=1.01
  var held=rig.registry.definition(ID);check(not rig.registry.load_catalogue(cat,bad),"invalid profile rejected");check(rig.registry.definition(ID)==held,"registry reload atomic")
 rig.reset();var snapshots=[]
 for hz in [30,60]:
  for cycle in range(2):
   rig.play_expression(ID)
   for i in range(int(ceil(3.1*hz))+1):
    rig.advance(1.0/hz);anatomy()
    var expected=rig.sample_expression(ID,rig.performance_time)
    if rig.performance_time<rig.RESTART_SECONDS:
     var weight=smoothstep(0.0,rig.RESTART_SECONDS,rig.performance_time)
     for k in rig.CHANNELS:expected[k]=lerpf(rig.restart_pose.get(k,0),expected[k],weight)
    for k in rig.CHANNELS:
     check(is_equal_approx(rig.pose_now()[k],expected[k]),"player matches sampler plus restart")
     if k not in ALLOWED:check(rig.pose_now()[k]==0,"actual unused field zero")
    if rig.pose_now().mouth_open==0:
     for joint in rig.face.smile_lip_joints:
      if joint.upper:
       var peer=("mouth_corner_lower_" if joint.corner else "lower_lip_joint_")+str(joint.index)
       check(rig.face.homes[joint.key].node.transform==rig.face.homes[peer].node.transform,"sealed rigid seam remains exact")
    if hz==60:
     if cycle==0:snapshots.append(rig.face.snapshot())
     else:check(rig.face.snapshot()==snapshots[i],"second cycle state exact")
   neutral("natural complete")
 var out=""
 for a in OS.get_cmdline_user_args():
  if a.begins_with("--output="):out=a.trim_prefix("--output=")
 if not out.is_empty():
  var f=FileAccess.open(out,FileAccess.WRITE);f.store_string(JSON.stringify({"checks":checks,"failures":failures,"status":"PASS" if failures.is_empty() else "FAIL","normal_speed_playback_observed":false},"  "));f.close()
 print("CHEEKY_WINK_RUNTIME checks=",checks," failures=",failures.size());quit(0 if failures.is_empty() else 1)

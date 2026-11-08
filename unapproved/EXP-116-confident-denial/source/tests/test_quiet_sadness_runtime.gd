extends SceneTree
## Data-only EXP-021 tests on the unchanged shared player.
const ID="EXP-021"
const PRIOR=["EXP-163","EXP-005","EXP-001","EXP-006","EXP-107","EXP-007","EXP-002","EXP-152","EXP-160","EXP-177","EXP-164"]
const ALLOWED=["blink_R","blink_L","brow_screen_left","brow_screen_right","brow_inner_lift_screen_left","brow_inner_lift_screen_right","gaze_y","gaze_down_extra"]
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
  if failures.size()<12:push_error(label)
func state():
 var s=rig.get_state();s.erase("last_error");s.face=rig.face.snapshot();return s
func neutral(label,blink=false):
 check(rig.pose_now()==rig.neutral_pose(),label+" exact neutral")
 check(rig.active_performance=="" and rig.release_time<0,label+" idle ownership")
 check(rig.auto_blink==blink and not rig.auto_blink_pending_restore,label+" blink policy")
func anatomy():
 check(rig.head.transform==head_home and rig.body.transform==body_home,"fixed canonical head neck body")
 for k in rig.face.objects:
  var n=rig.face.objects[k];var owner=rig.face.homes[k].node
  check(n.scale==Vector2.ONE and owner.scale==Vector2.ONE and n.modulate==Color.WHITE and n.self_modulate==Color.WHITE,"rigid opaque owner")
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
 check(ids==PRIOR+[ID],"eleven approved profiles plus local021")
 for id in ["EXP-003","EXP-139","EXP-153","EXP-161","EXP-170"]:check(rig.registry.resolve(id)=="","excluded "+id)
 for alias in [ID,"quiet-sadness","quiet_sadness"]:check(rig.registry.resolve(alias)==ID,"alias")
 var d=rig.registry.definition(ID)
 check(d.duration==3.65 and d.keyframes.size()==5,"five-key continuous timing")
 check(d.timing_origin.contains("Newly authored") and d.timing_origin.contains("unimplemented reference"),"honest static timing")
 var peak=d.keyframes[1].values
 check(peak==d.keyframes[2].values,"single sustained exact peak")
 check(peak.blink_R==.4 and peak.blink_L==.4 and peak.brow_inner_lift_screen_left==.82 and peak.brow_inner_lift_screen_right==.65,"accepted static peak")
 var anchors=JSON.parse_string(FileAccess.get_file_as_string("res://source_references/quiet_sadness_source_anchor_map.json"))
 for a in anchors.anchors:
  var p=rig.sample_expression(ID,a.time)
  for k in rig.CHANNELS:check(is_equal_approx(p[k],a.values[k]),"documented interpolated source anchor")
 var previous=rig.neutral_pose()
 for i in range(3651):
  var t=i*.001;var p=rig.sample_expression(ID,t)
  for k in p:
   var b=rig.Registry.CHANNEL_BOUNDS[k];check(p[k]>=b[0] and p[k]<=b[1],"bounded "+k)
   if k not in ALLOWED:check(p[k]==0,"unrelated channel zero "+k)
  check(p.blink_R<=.400001 and p.blink_L<=.400001,"partial open-eye bound")
  var strength=p.brow_inner_lift_screen_left
  var old=previous.brow_inner_lift_screen_left
  if i>0 and t<=1.4:check(strength>=old,"single monotonic sink")
  if t>=1.4 and t<=2.05:check(is_equal_approx(strength,.82),"still hold")
  if t>=2.05:check(strength<=old+.000001,"single monotonic recovery")
  previous=p
 # Handoffs from onset, mid-build, hold, recovery and near-end, with both blink policies.
 for origin in [.10,.299999,.30,.62,1.05,1.4,1.7,2.05,2.65,3.05,3.4999,3.6499]:
  for wanted in [false,true]:
   for action in ["release","repeat_release","retrigger","manual","reset","disable"]+PRIOR:
    rig.reset();rig.apply_controls({"auto_blink":wanted});rig.play_expression(ID);rig.advance(origin);var before=rig.displayed_pose()
    if action in ["release","repeat_release"]:
     check(rig.release() and rig.displayed_pose()==before,"release C0")
     if action=="repeat_release":
      rig.advance(.17);before=rig.displayed_pose();check(rig.release() and rig.displayed_pose()==before,"repeat release C0")
     rig.advance(.45);neutral("released",wanted)
    elif action=="retrigger" or action.begins_with("EXP-"):
     var destination=ID if action=="retrigger" else action
     check(rig.play_expression(destination) and rig.displayed_pose()==before,"handoff C0")
     rig.advance(rig.registry.definition(destination).duration);neutral("destination completion",wanted)
    elif action=="manual":
     check(rig.apply_controls({"blink_R":.13,"brow_inner_lift_screen_left":.22}),"manual accepted")
     var p=rig.pose_now();rig.advance(8)
     check(rig.pose_now()==p and rig.active_performance=="" and rig.release_time<0 and not rig.auto_blink_pending_restore and not rig.auto_blink,"manual remains owner")
     rig.reset();neutral("manual reset")
    elif action=="disable":
     rig.apply_controls({"auto_blink":false});var p=rig.pose_now();rig.advance(8)
     check(rig.pose_now()==p and not rig.auto_blink_pending_restore and not rig.auto_blink and rig.active_performance=="","explicit disable takeover")
     rig.reset();neutral("disable reset")
    else:rig.reset();neutral("reset")
    anatomy()
 for id in PRIOR:
  for origin in [.1,rig.registry.definition(id).duration*.5]:
   rig.reset();rig.apply_controls({"auto_blink":true});rig.play_expression(id);rig.advance(origin);var before=rig.displayed_pose()
   check(rig.play_expression(ID) and rig.displayed_pose()==before,"incoming C0")
   rig.advance(3.65);neutral("incoming full completion",true)
 for action in ["natural","release","retrigger","handoff"]:
  rig.reset();rig.apply_controls({"auto_blink":true});rig.advance(4.03);check(rig.face.closure.x>.99,"visible initial blink")
  var before=rig.displayed_pose();rig.play_expression(ID);check(rig.displayed_pose()==before and not rig.auto_blink and rig.auto_blink_pending_restore,"suspend displayed blink C0")
  rig.advance(1.7)
  if action=="release":rig.release();rig.advance(.45)
  elif action=="retrigger":rig.play_expression(ID);rig.advance(3.65)
  elif action=="handoff":rig.play_expression("EXP-005");rig.advance(5.4)
  else:rig.advance(3.65)
  neutral("restore "+action,true);rig.advance(4.03);check(rig.face.closure.x>.99,"restored clock runs")
 for mode in ["manual","active","release"]:
  rig.reset();rig.play_expression(ID);rig.advance(1.7)
  if mode=="release":rig.release();rig.advance(.17)
  if mode=="manual":rig.apply_controls({"mouth_open":.3})
  for key in rig.Registry.CHANNEL_BOUNDS:
   var b=rig.Registry.CHANNEL_BOUNDS[key]
   for invalid in [b[0]-.000001,b[1]+.000001,NAN,INF,true,"1",null]:
    var saved=state();check(not rig.apply_controls({"reset":true,key:invalid}),"invalid controls rejected");check(state()==saved,"invalid transaction atomic")
 var defs={};var cat=JSON.parse_string(FileAccess.get_file_as_string("res://expressions/registry.json"))
 for e in cat.entries:defs[e.path]=JSON.parse_string(FileAccess.get_file_as_string(e.path))
 for mode in ["bad_time","nonneutral_end","bad_control"]:
  var bad=defs.duplicate(true);var entry=bad["res://expressions/EXP-021.json"]
  if mode=="bad_time":entry.keyframes[2].time=.1
  elif mode=="nonneutral_end":entry.keyframes[4].values.blink_R=.1
  else:entry.keyframes[1].values.blink_R=1.01
  var held=rig.registry.definition(ID);check(not rig.registry.load_catalogue(cat,bad),"bad profile rejected");check(rig.registry.definition(ID)==held,"registry atomic")
 rig.reset();var snapshots=[]
 for hz in [30,60]:
  for cycle in range(2):
   rig.play_expression(ID)
   for i in range(int(ceil(3.65*hz))+1):
    rig.advance(1.0/hz);anatomy()
    var expected=rig.sample_expression(ID,rig.performance_time)
    if rig.performance_time<rig.RESTART_SECONDS:
     var weight=smoothstep(0.0,rig.RESTART_SECONDS,rig.performance_time)
     for k in rig.CHANNELS:expected[k]=lerpf(rig.restart_pose.get(k,0),expected[k],weight)
    for k in rig.CHANNELS:
     check(is_equal_approx(rig.pose_now()[k],expected[k]),"actual player matches sampler and restart")
     if k not in ALLOWED:check(rig.pose_now()[k]==0,"actual excluded channel zero")
    check(rig.face.mouth_opening==0 and rig.face.mouth_purse==0 and rig.face.smile_mouth==0,"actual sealed unchanged mouth")
    if hz==60:
     if cycle==0:snapshots.append(rig.face.snapshot())
     else:check(rig.face.snapshot()==snapshots[i],"repeat state exact without reset")
   neutral("repeat neutral")
 var out=""
 for arg in OS.get_cmdline_user_args():
  if arg.begins_with("--output="):out=arg.trim_prefix("--output=")
 var result={"checks":checks,"failures":failures,"status":"PASS" if failures.is_empty() else "FAIL","normal_speed_playback_observed":false,"socket_test_performed":false}
 if not out.is_empty():var f=FileAccess.open(out,FileAccess.WRITE);f.store_string(JSON.stringify(result,"  "));f.close()
 print("QUIET_SADNESS_RUNTIME checks=",checks," failures=",failures.size());quit(0 if failures.is_empty() else 1)

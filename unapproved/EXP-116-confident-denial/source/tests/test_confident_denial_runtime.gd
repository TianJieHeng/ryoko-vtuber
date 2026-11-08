extends SceneTree
const ID="EXP-116"
const PRIOR=["EXP-163", "EXP-005", "EXP-001", "EXP-006", "EXP-107", "EXP-007", "EXP-002", "EXP-152", "EXP-160", "EXP-177", "EXP-164", "EXP-021", "EXP-158", "EXP-181", "EXP-102"]
const ALLOWED=["blink_R", "blink_L", "brow_screen_left", "brow_screen_right", "brow_tilt_screen_left", "brow_tilt_screen_right", "mouth_smile", "mouth_spread", "mouth_corner_lift_screen_right", "mouth_width_screen_left", "mouth_width_screen_right"]
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
 check(ids==PRIOR+[ID],"all fifteen existing plus local EXP-116 only")
 for id in ["EXP-139","EXP-170"]:check(rig.registry.resolve(id)=="","no unrelated profile "+id)
 for a in [ID,"confident-denial","confident_denial"]:check(rig.registry.resolve(a)==ID,"alias")
 var d=rig.registry.definition(ID)
 check(d.duration==2.85 and d.keyframes.size()==10,"ten authored keys and 2.85 seconds")
 check(d.timing_origin.contains("Newly authored") and d.timing_origin.contains("not recovered animation"),"honest static source timing")
 var anchors=JSON.parse_string(FileAccess.get_file_as_string("res://source_references/confident_denial_source_anchor_map.json"))
 var static_plan=JSON.parse_string(FileAccess.get_file_as_string("res://source_references/confident_denial_accepted_static_plan.json"))
 for a in anchors.anchors:
  var p=rig.sample_expression(ID,a.time)
  for k in rig.CHANNELS:check(is_equal_approx(p[k],a.values.get(k,0)),"exact authored source anchor")
  for e in static_plan.candidate_cases:
   if e.source_key!=a.key_pose:continue
   for k in rig.CHANNELS:check(is_equal_approx(p[k],e.values.get(k,0)),"accepted static pose exact")
 var prev=rig.neutral_pose()
 for i in range(2851):
  var t=i*.001;var p=rig.sample_expression(ID,t)
  for k in p:
   var b=rig.Registry.CHANNEL_BOUNDS[k];check(p[k]>=b[0] and p[k]<=b[1],"bounded trajectory")
   if k not in ALLOWED:check(p[k]==0,"unrelated channel zero "+k)
  check(p.blink_R<=.160001 and p.blink_L<=.090001 and p.eye_smile_R==0 and p.eye_smile_L==0,"ordinary weighted lids only")
  check(p.mouth_open==0 and p.mouth_corner_lift_screen_right<=1 and p.mouth_smile<=.150001 and p.mouth_spread<=1,"sealed accepted source envelope")
  check(p.mouth_width_screen_left<=.200001 and p.mouth_width_screen_right<=.820001,"both width fields bounded")
  if t<=.85 or t>=1.70:
   for k in p:
    if k.begins_with("mouth_"):check(p[k]==0,"firm preparation and late recovery mouth off")
  if t>=1.70 and t<2.65:check(p.brow_screen_left<0 and p.blink_R>0,"brow and lid tension outlast mouth")
  if i>0 and i<=1080:check(p.mouth_corner_lift_screen_right>=prev.mouth_corner_lift_screen_right-.000001,"single brief release onset")
  if i>1080:check(p.mouth_corner_lift_screen_right<=prev.mouth_corner_lift_screen_right+.000001,"single release recovery")
  prev=p
 for origin in [.1,.299999,.3,.85,1.08,1.32,1.70,2.20,2.649999,2.849999]:
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
  check(rig.play_expression(ID) and rig.displayed_pose()==before,"incoming C0");rig.advance(2.85);neutral("incoming completion",true)
 for action in ["natural","release","retrigger"]:
  rig.reset();rig.apply_controls({"auto_blink":true});rig.advance(4.03);check(rig.face.closure.x>.99,"initial visible blink")
  var before=rig.displayed_pose();check(rig.play_expression(ID) and rig.displayed_pose()==before and not rig.auto_blink and rig.auto_blink_pending_restore,"blink suspension C0");rig.advance(1.08)
  if action=="release":rig.release();rig.advance(.45)
  elif action=="retrigger":rig.play_expression(ID);rig.advance(2.85)
  else:rig.advance(2.85)
  neutral("blink restores",true);rig.advance(4.03);check(rig.face.closure.x>.99,"restored cycle works")
 for mode in ["manual","active","release"]:
  rig.reset();rig.play_expression(ID);rig.advance(1.08)
  if mode=="release":rig.release();rig.advance(.17)
  if mode=="manual":check(rig.apply_controls({"mouth_open":.3,"mouth_width_screen_left":0.0,"mouth_width_screen_right":0.0}),"atomic open manual takeover")
  for key in rig.Registry.CHANNEL_BOUNDS:
   var b=rig.Registry.CHANNEL_BOUNDS[key]
   for bad in [b[0]-.000001,b[1]+.000001,NAN,INF,true,"1",null]:
    var saved=state();check(not rig.apply_controls({"reset":true,key:bad}),"invalid input rejected");check(state()==saved,"invalid input atomic")
 for blink in [false,true]:
  for origin in [.85,1.08,1.32,1.70]:
   for other in PRIOR:
    for incoming in [false,true]:
     var source=other if incoming else ID;var target=ID if incoming else other
     rig.reset();rig.apply_controls({"auto_blink":blink});rig.play_expression(source)
     rig.advance(rig.registry.definition(source).duration*.5 if incoming else origin)
     var before=rig.displayed_pose();check(rig.play_expression(target) and rig.displayed_pose()==before,"ordered handover C0")
     var expected_mode=bridge_mode(before,rig.registry.definition(target));check(rig.mouth_bridge_mode==expected_mode,"trigger-fixed whole-timeline mode")
     var last=0.0
     for time in [0.0,.000001,.075,.149999,.15,.150001,.225,.299999,.30,.300001,.44,.66]:
      rig.advance(time-last);last=time;bridge_expected(before,target,time,expected_mode)
     rig.advance(rig.registry.definition(target).duration);neutral("ordered handover completion",blink)
  for direction in ["open_to_width","width_to_open"]:
   for reversal_time in [.075,.149999,.15,.150001,.225,.299999]:
    rig.reset();rig.apply_controls({"auto_blink":blink})
    var source="EXP-005" if direction=="open_to_width" else ID
    var target=ID if direction=="open_to_width" else "EXP-005"
    rig.play_expression(source);rig.advance(1.5 if source=="EXP-005" else 1.08);rig.play_expression(target);rig.advance(reversal_time)
    var before=rig.displayed_pose();check(rig.play_expression(source) and rig.displayed_pose()==before,"mid-bridge reversal C0")
    var mode=bridge_mode(before,rig.registry.definition(source));var last=0.0
    for time in [0.0,.000001,.149999,.15,.150001,.299999,.30,.300001]:
     rig.advance(time-last);last=time;bridge_expected(before,source,time,mode)
    rig.advance(rig.registry.definition(source).duration);neutral("reversal complete",blink)
 # Dense 0.5 ms sweeps around the full .30 s staged interval and delayed target opening.
 for incoming in [false,true]:
  rig.reset();var source="EXP-005" if incoming else ID;var target=ID if incoming else "EXP-005"
  rig.play_expression(source);rig.advance(1.5 if incoming else 1.08);var before=rig.displayed_pose();rig.play_expression(target)
  var mode=bridge_mode(before,rig.registry.definition(target));var last=0.0
  for i in range(1201):
   var time=i*.0005;rig.advance(time-last);last=time;bridge_expected(before,target,time,mode)
 # Large steps must not depend on observing the midpoint or a first positive target aperture.
 for incoming in [false,true]:
  for dt in [.149999,.15,.150001,.299999,.3,.300001,.66,2.85,8.0]:
   rig.reset();var source="EXP-005" if incoming else ID;var target=ID if incoming else "EXP-005"
   rig.play_expression(source);rig.advance(1.5 if incoming else 1.08);var before=rig.displayed_pose();rig.play_expression(target)
   var mode=bridge_mode(before,rig.registry.definition(target));rig.advance(dt)
   if dt<rig.registry.definition(target).duration:bridge_expected(before,target,dt,mode)
   else:neutral("large-step completion")
 # Retained authored widths participate in manual transactions and reject atomically.
 for stage in ["active","release"]:
  rig.reset();rig.play_expression(ID);rig.advance(1.08)
  if stage=="release":rig.release();rig.advance(.1)
  var saved=state();check(not rig.apply_controls({"mouth_open":.2}),"retained widths block opening");check(state()==saved,"overlap reject atomic")
  check(rig.apply_controls({"mouth_open":.2,"mouth_width_screen_left":0.0,"mouth_width_screen_right":0.0}),"complete trio manual handover")
  check(rig.pose_now().mouth_open>.19 and rig.pose_now().mouth_width_screen_left==0 and rig.pose_now().mouth_width_screen_right==0,"atomic open result")
 var defs={};var cat=JSON.parse_string(FileAccess.get_file_as_string("res://expressions/registry.json"))
 for e in cat.entries:defs[e.path]=JSON.parse_string(FileAccess.get_file_as_string(e.path))
 for mode in ["bad_time","bad_end","bad_side","overlap","segment_overlap"]:
  var bad=defs.duplicate(true);var entry=bad["res://expressions/EXP-116.json"]
  if mode=="bad_time":entry.keyframes[2].time=.1
  elif mode=="bad_end":entry.keyframes[9].values.mouth_corner_lift_screen_right=.1
  elif mode=="bad_side":entry.keyframes[4].values.mouth_width_screen_right=1.01
  elif mode=="overlap":entry.keyframes[4].values.mouth_open=.1
  else:entry.keyframes[3].values.mouth_open=.1
  var held=rig.registry.definition(ID);check(not rig.registry.load_catalogue(cat,bad),"invalid profile rejected");check(rig.registry.definition(ID)==held,"registry reload atomic")
 rig.reset();var snapshots=[]
 for hz in [30,60]:
  for cycle in range(2):
   rig.play_expression(ID)
   for i in range(int(ceil(2.85*hz))+1):
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
 print("CONFIDENT_DENIAL_RUNTIME checks=",checks," failures=",failures.size());quit(0 if failures.is_empty() else 1)

func bridge_mode(source,definition):
 var width=false;var opening=false
 for frame in definition.keyframes:
  width=width or frame.values.get("mouth_width_screen_left",0)>0 or frame.values.get("mouth_width_screen_right",0)>0
  opening=opening or frame.values.get("mouth_open",0)>0
 var source_width=source.mouth_width_screen_left>0 or source.mouth_width_screen_right>0
 if not source_width and not width:return "legacy"
 return "staged" if (source_width and opening) or (source.mouth_open>0 and width) else "bounded_direct"
func bridge_expected(source,target,time,mode):
 var raw=rig.sample_expression(target,time);var expected=raw.duplicate();var duration=rig.registry.definition(target).duration
 if time<.30:
  var w=smoothstep(0.0,.30,time)
  for key in rig.CHANNELS:expected[key]=lerpf(source[key],raw[key],w)
 if mode!="legacy":
  var T=minf(.30,duration);var u=time/T
  for key in ["mouth_open","mouth_width_screen_left","mouth_width_screen_right"]:
   if time>=T:expected[key]=raw[key]
   elif mode=="bounded_direct":expected[key]=lerpf(source[key],raw[key],smoothstep(0.0,1.0,u))
   elif u<=.5:expected[key]=source[key]*(1.0-smoothstep(0.0,.5,u))
   else:expected[key]=raw[key]*smoothstep(.5,1.0,u)
 var actual=rig.pose_now()
 for key in rig.CHANNELS:check(abs(actual[key]-expected[key])<.000002,"generic composed pose including widths "+key)
 check(actual.mouth_open==0 or (actual.mouth_width_screen_left==0 and actual.mouth_width_screen_right==0),"no opening/width overlap")
 check(rig.mouth_transition_state().mode==mode,"mode stays fixed even before later opening")
 check(rig.mouth_transition_state().duration==(.30 if mode=="legacy" else minf(.30,duration)),"mode duration")
 if mode=="staged" and time==.15:check(actual.mouth_open==0 and actual.mouth_width_screen_left==0 and actual.mouth_width_screen_right==0,"explicit zero trio midpoint")

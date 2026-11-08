extends SceneTree
## EXP-164 data-only contract on the unchanged shared player. No socket or capture.
const ID="EXP-164"
const PRIOR=["EXP-163","EXP-005","EXP-001","EXP-006","EXP-107","EXP-007","EXP-002","EXP-152","EXP-160","EXP-177"]
const ALLOWED=["blink_R","blink_L","brow_screen_left","brow_screen_right","brow_tilt_screen_left","brow_tilt_screen_right","brow_inner_lift_screen_left","brow_inner_lift_screen_right","mouth_purse"]
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
  if failures.size()<20:push_error(label)
func state():
 var s=rig.get_state();s.erase("last_error");s.face=rig.face.snapshot();s.restart=rig.restart_pose.duplicate(true);s.release=rig.release_pose.duplicate(true);return s
func neutral(label,blink=false):
 check(rig.pose_now()==rig.neutral_pose(),label+" exact neutral")
 check(rig.active_performance=="" and rig.release_time<0,label+" idle ownership")
 check(rig.auto_blink==blink and not rig.auto_blink_pending_restore,label+" blink policy")
func anatomy(sealed=false):
 check(rig.head.transform==head_home and rig.body.transform==body_home,"fixed head neck body")
 for k in rig.face.objects:
  var n=rig.face.objects[k];var owner=rig.face.homes[k].node
  check(n.scale==Vector2.ONE and owner.scale==Vector2.ONE and n.modulate==Color.WHITE and n.self_modulate==Color.WHITE,"rigid opaque owner")
  check([n.texture,n.region_rect,n.region_enabled,n.offset,n.flip_h,n.flip_v]==pigment[k],"fixed texture UV")
 check(rig.face.oral_objects.upper_teeth.position==Vector2(533,626),"fixed white enamel")
 check(rig.face.MAX_MOUTH_APERTURE==.55,"published physical mouth cap")
 for x in range(81):
  var gap=rig.face._smile_lip_offset(x,false,false)-rig.face._smile_lip_offset(x,true,false)
  check(gap>=-.000001 and gap<=30.800001,"physical aperture bound")
  if sealed:check(absf(gap)<.000001,"zero geometric lip gap throughout fighting sleep")
func run():
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 check(rig.rig_ready and rig.registry_ready,"ready")
 if not rig.rig_ready or not rig.registry_ready:quit(2);return
 head_home=rig.head.transform;body_home=rig.body.transform
 for k in rig.face.objects:
  var n=rig.face.objects[k];pigment[k]=[n.texture,n.region_rect,n.region_enabled,n.offset,n.flip_h,n.flip_v]
 var ids=[]
 for e in rig.list_expressions():ids.append(e.id)
 check(ids==PRIOR+[ID],"ten approved profiles plus only164")
 for id in ["EXP-003","EXP-153","EXP-161"]:check(rig.registry.resolve(id)=="","excluded "+id)
 for alias in [ID,"fighting-sleep","fighting_sleep"]:check(rig.registry.resolve(alias)==ID,"alias")
 var d=rig.registry.definition(ID)
 check(d.duration==3.47 and d.keyframes.size()==15,"new 3.47-second fifteen-key pacing")
 check(d.timing_origin.contains("Newly authored") and d.timing_origin.contains("unimplemented reference"),"honest static-source timing")
 var accepted=JSON.parse_string(FileAccess.get_file_as_string("res://source_references/fighting_sleep_accepted_pose_plan.json"))
 var mapping=JSON.parse_string(FileAccess.get_file_as_string("res://source_references/fighting_sleep_pose_timing_map.json"))
 for source_pose in accepted.poses:
  for t in mapping.key_pose_times[str(int(source_pose.key_pose))]:
   var p=rig.sample_expression(ID,t)
   for channel in rig.CHANNELS:check(is_equal_approx(p[channel],source_pose.values[channel]),"accepted key pose preserved")
 # Continuous sampled trajectory bounds at 1ms, not a visual acceptance claim.
 for i in range(3471):
  var t=i*.001;var p=rig.sample_expression(ID,t)
  for k in p:
   var b=rig.Registry.CHANNEL_BOUNDS[k];check(p[k]>=b[0] and p[k]<=b[1],"bounded "+k)
   if k not in ALLOWED:check(p[k]==0,"unrelated channel zero "+k)
  check(p.blink_R<=.700001 and p.blink_L<=.700001,"never overclose amber-trace candidate")
  check(p.mouth_purse<=.200001,"modest sealed purse cap")
  if t<=.90 or t>=2.71:check(p.mouth_purse==0,"mouth cue only middle effort")
  if t>=1.10 and t<=2.29:check(is_equal_approx(p.mouth_purse,.2),"middle cue held through second reopen")
 check(rig.sample_expression(ID,.82).blink_R>rig.sample_expression(ID,1.84).blink_R,"first sink deeper")
 check(rig.sample_expression(ID,1.10).brow_tilt_screen_left>rig.sample_expression(ID,2.15).brow_tilt_screen_left,"first reopen firmer")
 # Every meaningful anchor, purse handoff neighborhood and first-entry blend.
 for origin in [0.0,.05,.299999,.3,.4436559139784946,.82,.90,.9001,1.0,1.10,1.26,1.84,1.92,2.15,2.29,2.50,2.7099,2.71,3.01,3.469999]:
  for wanted in [false,true]:
   for action in ["release","repeat_release","retrigger","manual","reset","disable"]+PRIOR:
    rig.reset();rig.apply_controls({"auto_blink":wanted});rig.play_expression(ID);rig.advance(origin);var before=rig.displayed_pose()
    if action in ["release","repeat_release"]:
     check(rig.release() and rig.displayed_pose()==before,"release C0")
     if action=="repeat_release":
      rig.advance(.17);before=rig.displayed_pose();check(rig.release() and rig.displayed_pose()==before,"repeated release C0")
     rig.advance(.45);neutral("released",wanted)
    elif action=="retrigger" or action.begins_with("EXP-"):
     var destination=ID if action=="retrigger" else action
     check(rig.play_expression(destination) and rig.displayed_pose()==before,"retrigger handoff C0")
     rig.advance(rig.registry.definition(destination).duration);neutral("destination completion",wanted)
    elif action=="manual":
     check(rig.apply_controls({"mouth_purse":.11,"blink_R":.17,"brow_screen_left":.13}),"manual accepted")
     var manual=rig.pose_now();rig.advance(7)
     check(rig.pose_now()==manual and rig.active_performance=="" and rig.release_time<0 and not rig.auto_blink_pending_restore and not rig.auto_blink,"manual cannot stale resume")
     rig.reset();neutral("manual reset")
    elif action=="disable":
     rig.apply_controls({"auto_blink":false});var manual=rig.pose_now();rig.advance(7)
     check(rig.pose_now()==manual and not rig.auto_blink_pending_restore and not rig.auto_blink and rig.active_performance=="","explicit disable is takeover")
     rig.reset();neutral("disable reset")
    else:rig.reset();neutral("reset")
    anatomy()
 for id in PRIOR:
  var duration=rig.registry.definition(id).duration
  for origin in [.05,.29,duration*.5,duration-.001]:
   rig.reset();rig.apply_controls({"auto_blink":true});rig.play_expression(id);rig.advance(origin);var before=rig.displayed_pose()
   check(rig.play_expression(ID) and rig.displayed_pose()==before,"incoming C0")
   rig.advance(3.47);neutral("incoming full completion",true)
 for action in ["natural","release","retrigger","handoff"]:
  rig.reset();rig.apply_controls({"auto_blink":true});rig.advance(4.03)
  check(rig.face.closure.x>.99,"visible initial blink")
  var before=rig.displayed_pose();rig.play_expression(ID);check(rig.displayed_pose()==before and not rig.auto_blink and rig.auto_blink_pending_restore,"suspend displayed blink C0")
  rig.advance(1.26)
  if action=="release":rig.release();rig.advance(.45)
  elif action=="retrigger":rig.play_expression(ID);rig.advance(3.47)
  elif action=="handoff":rig.play_expression("EXP-005");rig.advance(5.4)
  else:rig.advance(3.47)
  neutral("restore "+action,true);rig.advance(4.03);check(rig.face.closure.x>.99,"restored clock runs")
 var catalogue=JSON.parse_string(FileAccess.get_file_as_string("res://expressions/registry.json"));var defs={}
 for e in catalogue.entries:defs[e.path]=JSON.parse_string(FileAccess.get_file_as_string(e.path))
 for mode in ["manual","active","release"]:
  rig.reset();rig.play_expression(ID);rig.advance(1.26)
  if mode=="release":rig.release();rig.advance(.17)
  if mode=="manual":rig.apply_controls({"mouth_open":.3})
  for key in rig.Registry.CHANNEL_BOUNDS:
   var b=rig.Registry.CHANNEL_BOUNDS[key]
   for invalid in [b[0]-.000001,b[1]+.000001,NAN,INF,true,"1",null]:
    var saved=state();check(not rig.apply_controls({"reset":true,key:invalid}),"invalid control rejected");check(state()==saved,"invalid controls atomic")
    var bad=defs.duplicate(true);bad["res://expressions/EXP-164.json"].keyframes[5].values[key]=invalid
    var held=rig.registry.definition(ID);check(not rig.registry.load_catalogue(catalogue,bad),"invalid definition rejected");check(rig.registry.definition(ID)==held,"registry atomic")
 for field in ["time","values","phase"]:
  var bad=defs.duplicate(true);bad["res://expressions/EXP-164.json"].keyframes[5][field]=null
  check(not rig.registry.load_catalogue(catalogue,bad),"invalid164 key field")
 rig.reset();var snapshots=[]
 for hz in [30,60]:
  for cycle in range(2):
   check(rig.play_expression(ID),"repeat start")
   for i in range(int(3.47*hz)+1):
    rig.advance(1.0/hz);anatomy(true)
    var expected=rig.sample_expression(ID,rig.performance_time)
    if rig.performance_time<rig.RESTART_SECONDS:
     var weight=smoothstep(0.0,rig.RESTART_SECONDS,rig.performance_time)
     for k in rig.CHANNELS:expected[k]=lerpf(rig.restart_pose.get(k,0),expected[k],weight)
    for k in rig.CHANNELS:check(is_equal_approx(rig.pose_now()[k],expected[k]),"actual playback matches expected timeline coordinate")
    for k in rig.CHANNELS:
     if k not in ALLOWED:check(rig.pose_now()[k]==0,"actual unrelated channel zero")
    if hz==60:
     if cycle==0:snapshots.append(rig.face.snapshot())
     else:check(rig.face.snapshot()==snapshots[i],"two cycles identical state without reset")
   neutral("repeat neutral")
 print("FIGHTING_SLEEP_RUNTIME checks=",checks," failures=",failures.size())
 var out=""
 for arg in OS.get_cmdline_user_args():
  if arg.begins_with("--output="):out=arg.trim_prefix("--output=")
 if not out.is_empty():
  var f=FileAccess.open(out,FileAccess.WRITE);f.store_string(JSON.stringify({"checks":checks,"failures":failures,"status":"PASS" if failures.is_empty() else "FAIL","normal_speed_playback_observed":false,"socket_test_performed":false},"  "));f.close()
 quit(0 if failures.is_empty() else 1)

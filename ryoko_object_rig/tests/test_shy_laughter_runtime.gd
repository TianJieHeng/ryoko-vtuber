extends SceneTree
## Source-specific data contract and lifecycle through the existing shared player.
const ID="EXP-160"
const PRIOR=["EXP-163","EXP-005","EXP-001","EXP-006","EXP-107","EXP-007","EXP-002","EXP-152"]
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
func anatomy():
 check(rig.head.transform==head_home and rig.body.transform==body_home,"fixed head/neck and body")
 for k in rig.face.objects:
  var n=rig.face.objects[k];var owner=rig.face.homes[k].node
  check(n.scale==Vector2.ONE and owner.scale==Vector2.ONE and n.modulate==Color.WHITE,"rigid opaque owner")
  check([n.texture,n.region_rect,n.region_enabled]==pigment[k],"fixed texture/UV")
 check(rig.face.oral_objects.upper_teeth.position==Vector2(533,626),"fixed white teeth")
 for x in range(81):
  var gap=rig.face._smile_lip_offset(x,false,false)-rig.face._smile_lip_offset(x,true,false)
  check(gap>=-.000001 and gap<=30.800001,"physical mouth cap")
func run():
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 check(rig.rig_ready and rig.registry_ready,"ready")
 if not rig.rig_ready or not rig.registry_ready:quit(2);return
 head_home=rig.head.transform;body_home=rig.body.transform
 for k in rig.face.objects:
  var n=rig.face.objects[k];pigment[k]=[n.texture,n.region_rect,n.region_enabled]
 var ids=[]
 for e in rig.list_expressions():ids.append(e.id)
 check(ids==PRIOR+[ID,"EXP-177","EXP-164"],"ten approved profiles plus scoped164")
 for id in ["EXP-003","EXP-153","EXP-161"]:check(rig.registry.resolve(id)=="","excluded "+id)
 for alias in [ID,"shy-laughter","shy_laughter"]:check(rig.registry.resolve(alias)==ID,"aliases")
 var d=rig.registry.definition(ID)
 check(d.duration==3.4 and d.keyframes.size()==12,"new 3.4-second twelve-key pacing")
 check(d.timing_origin.contains("Newly authored") and d.timing_origin.contains("unimplemented reference"),"honest static-source timing")
 var peak=d.keyframes[5].values
 check(peak.mouth_open==.85 and peak.eye_smile_L==1 and peak.eye_smile_R==1,"small opening and smiling crescents")
 check(peak.brow_tilt_screen_left==-1 and peak.brow_tilt_screen_right==1,"legacy inward tilt")
 check(is_equal_approx(peak.brow_inner_lift_screen_left,24.0/26) and is_equal_approx(peak.brow_inner_lift_screen_right,24.0/26),"32-degree total outer-anchor fit")
 check(d.keyframes[6].values.mouth_open==.65 and d.keyframes[7].values.mouth_open==.8,"two restrained newly authored accents")
 for i in range(3401):
  var t=i*.001;var p=rig.sample_expression(ID,t)
  for k in p:
   var b=rig.Registry.CHANNEL_BOUNDS[k];check(p[k]>=b[0] and p[k]<=b[1],"bounded "+k)
  for k in ["blink_L","blink_R","gaze_x","gaze_y","hair_sway","mouth_purse","brow_screen_left","brow_screen_right"]:check(p[k]==0,"no extra acting "+k)
  check(p.mouth_open<=.850001,"small opening cap")
  if t>=1.85 and t<=2.2:
   for k in ["mouth_smile","mouth_spread","mouth_corner_lift","mouth_lip_press","mouth_oral_lift","eye_smile_L","eye_smile_R","blush_intensity","brow_tilt_screen_left","brow_inner_lift_screen_left"]:check(is_equal_approx(p[k],peak[k]),"hold warmth until sealed "+k)
  if t>=2.2:check(p.mouth_open==0,"source afterglow stays sealed")
 check(d.keyframes[9].values.eye_smile_L==.88 and d.keyframes[10].values.eye_smile_L==.04,"closed-eye then reopened-eye afterglow")
 for origin in [0.0,.05,.299999,.3,.5,.533333,.65,1.0,1.1,1.35,1.6,1.85,2.1,2.2,2.4,2.65,2.8,3.399999]:
  for action in ["release","repeat_release","retrigger","manual","reset","disable"]+PRIOR:
   rig.reset();rig.apply_controls({"auto_blink":true});rig.play_expression(ID);rig.advance(origin);var before=rig.displayed_pose()
   if action in ["release","repeat_release"]:
    check(rig.release() and rig.displayed_pose()==before,"release C0")
    if action=="repeat_release":
     rig.advance(.17);before=rig.displayed_pose();check(rig.release() and rig.displayed_pose()==before,"repeated release C0")
    rig.advance(.45);neutral("released",true)
   elif action=="retrigger" or action.begins_with("EXP-"):
    var destination=ID if action=="retrigger" else action
    check(rig.play_expression(destination) and rig.displayed_pose()==before,"retrigger/handoff C0")
    rig.advance(rig.registry.definition(destination).duration);neutral("destination completion",true)
   elif action=="manual":
    check(rig.apply_controls({"mouth_open":.13,"mouth_smile":.4}),"manual accepted")
    var manual=rig.pose_now();rig.advance(7)
    check(rig.pose_now()==manual and rig.active_performance=="" and rig.release_time<0 and not rig.auto_blink_pending_restore and not rig.auto_blink,"manual no stale resume")
    rig.reset();neutral("manual reset")
   elif action=="disable":
    rig.apply_controls({"auto_blink":false});var manual=rig.pose_now();rig.advance(7)
    check(rig.pose_now()==manual and not rig.auto_blink_pending_restore and not rig.auto_blink and rig.active_performance=="","explicit disable is manual takeover")
    rig.reset();neutral("disable reset")
   else:rig.reset();neutral("reset")
   anatomy()
 for id in PRIOR:
  var duration=rig.registry.definition(id).duration
  for origin in [.05,.29,duration*.5,duration-.001]:
   rig.reset();rig.apply_controls({"auto_blink":true});rig.play_expression(id);rig.advance(origin);var before=rig.displayed_pose()
   check(rig.play_expression(ID) and rig.displayed_pose()==before,"incoming C0")
   rig.advance(3.4);neutral("incoming full completion",true)
 # Start during a real displayed auto-blink; restore the existing clock only after completion.
 for action in ["natural","release","retrigger","handoff"]:
  rig.reset();rig.apply_controls({"auto_blink":true});rig.advance(4.03)
  check(rig.face.closure.x>.99,"visible initial blink")
  var before=rig.displayed_pose();rig.play_expression(ID);check(rig.displayed_pose()==before and not rig.auto_blink and rig.auto_blink_pending_restore,"suspend displayed blink continuously")
  rig.advance(1.35)
  if action=="release":rig.release();rig.advance(.45)
  elif action=="retrigger":rig.play_expression(ID);rig.advance(3.4)
  elif action=="handoff":rig.play_expression("EXP-005");rig.advance(5.4)
  else:rig.advance(3.4)
  neutral("restored "+action,true);rig.advance(4.03);check(rig.face.closure.x>.99,"restored blink visibly runs")
 # Complete schema reload is atomic for invalid shy channels and chronology.
 var catalogue=JSON.parse_string(FileAccess.get_file_as_string("res://expressions/registry.json"));var defs={}
 for e in catalogue.entries:defs[e.path]=JSON.parse_string(FileAccess.get_file_as_string(e.path))
 for mode in ["manual","active","release"]:
  rig.reset();rig.play_expression(ID);rig.advance(1.35)
  if mode=="release":rig.release();rig.advance(.17)
  if mode=="manual":rig.apply_controls({"mouth_open":.3})
  for key in rig.Registry.CHANNEL_BOUNDS:
   var b=rig.Registry.CHANNEL_BOUNDS[key]
   for invalid in [b[0]-.000001,b[1]+.000001,NAN,INF,true,"1",null]:
    var saved=state();check(not rig.apply_controls({"reset":true,key:invalid}),"invalid control rejected")
    check(state()==saved,"invalid controls atomic")
    var bad=defs.duplicate(true);bad["res://expressions/EXP-160.json"].keyframes[5].values[key]=invalid
    var held=rig.registry.definition(ID);check(not rig.registry.load_catalogue(catalogue,bad),"invalid definition rejected");check(rig.registry.definition(ID)==held,"registry atomic")
 for field in ["time","values","phase"]:
  var bad=defs.duplicate(true);bad["res://expressions/EXP-160.json"].keyframes[5][field]=null
  check(not rig.registry.load_catalogue(catalogue,bad),"invalid shy keyframe field")
 rig.reset();var snapshots=[]
 for hz in [30,60]:
  for cycle in range(2):
   check(rig.play_expression(ID),"repeat start")
   for i in range(int(3.4*hz)+1):
    rig.advance(1.0/hz);anatomy()
    if hz==60:
     if cycle==0:snapshots.append(rig.face.snapshot())
     else:check(rig.face.snapshot()==snapshots[i],"two cycles exact visual state")
   neutral("repeat neutral")
 print("SHY_LAUGHTER_RUNTIME checks=",checks," failures=",failures.size());quit(0 if failures.is_empty() else 1)

extends SceneTree
var rig
var checks=0
var failures=[]
const ID="EXP-177"
const PRIOR=["EXP-163","EXP-005","EXP-001","EXP-006","EXP-107","EXP-007","EXP-002","EXP-152","EXP-160"]
const TIMES=[0.0,.4866515881418201,.6400595242051585,1.2,1.75,2.35,2.85,3.35,3.9]
const VALUES=[0.0,.36,.55,1.0,1.0,1.0,.64,.42,0.0]
func _initialize():call_deferred("run")
func check(ok,label):
 checks+=1
 if not ok:
  failures.append(label)
  if failures.size()<12:push_error(label)
func neutral(label,enabled=false):
 check(rig.pose_now()==rig.neutral_pose(),label+" exact neutral")
 check(rig.active_performance=="" and rig.release_time<0,label+" no stale owner")
 check(rig.auto_blink==enabled and not rig.auto_blink_pending_restore,label+" blink intent")
func quiet_pose(p,label):
 check(is_equal_approx(p.blink_R,p.blink_L),label+" bilateral lids")
 for k in p:
  if k not in ["blink_R","blink_L"]:check(p[k]==0,label+" neutral "+k)
func run():
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 check(rig.rig_ready and rig.registry_ready,"ready")
 if not rig.rig_ready or not rig.registry_ready:quit(2);return
 check(rig.registry.resolve("meditate")==ID and rig.registry.resolve("meditative-calm")==ID,"aliases")
 check(rig.list_expressions().size()==10,"nine published plus local177")
 for id in ["EXP-003","EXP-161","EXP-153"]:check(rig.registry.resolve(id)=="","unapproved profile absent")
 var d=rig.registry.definition(ID)
 check(d.duration==3.9 and d.keyframes.size()==7,"seven timeline keys, nine source-comparison poses, same3.9seconds")
 for n in range(9):
  var p=rig.sample_expression(ID,TIMES[n]);quiet_pose(p,"key")
  check(is_equal_approx(p.blink_R,VALUES[n]),"source aperture order")
  rig.reset();rig.play_expression(ID);rig.advance(TIMES[n])
  for k in p:check(is_equal_approx(rig.pose_now()[k],p[k]),"played key equals static key")
 for n in range(3901):
  var t=n*.001;var p=rig.sample_expression(ID,t);quiet_pose(p,"dense")
  check(p.blink_R>=0 and p.blink_R<=1,"bounded ordinary closure")
  if t>=1.2 and t<=2.35:check(p.blink_R==1,"1.15second true closed plateau")
 var h=rig.head.transform;var b=rig.body.transform;var fixed={}
 for k in rig.face.objects:
  var n=rig.face.objects[k];fixed[k]={"texture":n.texture,"region_enabled":n.region_enabled,"region_rect":n.region_rect,"modulate":n.modulate}
 for t in [0.0,.000001,.299999,.3,.4,.85,1.19,1.2,1.75,2.35,2.351,2.85,3.35,3.899999]:
  for action in ["release","repeat_release","retrigger","release_retrigger","EXP-163","EXP-005","EXP-001","EXP-006","EXP-107","EXP-007","EXP-002","EXP-152","EXP-160","manual","reset","disable"]:
   rig.reset();rig.apply_controls({"auto_blink":true});rig.play_expression(ID);rig.advance(t);var before=rig.displayed_pose()
   if action in ["release","repeat_release","release_retrigger"]:
    check(rig.release() and rig.displayed_pose()==before,"release C0")
    rig.advance(.2);before=rig.displayed_pose()
    if action=="repeat_release":check(rig.release() and rig.displayed_pose()==before,"repeated release C0")
    elif action=="release_retrigger":check(rig.play_expression(ID) and rig.displayed_pose()==before,"retrigger release C0")
    rig.advance(10);neutral(action,true)
   elif action=="retrigger" or action.begins_with("EXP-"):
    check(rig.play_expression(ID if action=="retrigger" else action),"handoff accepted")
    check(rig.displayed_pose()==before,"handoff C0");rig.advance(10);neutral(action,true)
   elif action=="manual":
    check(rig.apply_controls({"blink_R":.24,"blink_L":.38}),"manual")
    check(not rig.auto_blink_pending_restore and rig.active_performance=="" and rig.release_time<0,"manual owns")
    rig.advance(10);check(is_equal_approx(rig.face.closure.x,.24) and is_equal_approx(rig.face.closure.y,.38),"no stale resumption")
    rig.reset();neutral(action)
   elif action=="disable":
    check(rig.apply_controls({"auto_blink":false}),"disable")
    rig.release();rig.advance(.45);neutral(action,false)
   else:rig.reset();neutral(action,false)
 for old in PRIOR:
  for t in [.1,.3,.9,1.5,2.8,4.5]:
   rig.reset();rig.apply_controls({"auto_blink":true});rig.play_expression(old);rig.advance(t)
   var before=rig.displayed_pose();check(rig.play_expression(ID) and rig.displayed_pose()==before,"incoming C0")
   rig.advance(1.75);quiet_pose(rig.pose_now(),"after incoming hold")
   check(rig.face.closure==Vector2.ONE,"incoming ordinary full closure")
   for j in rig.face.smile_eye_joints:check(not rig.face.objects[j.key].visible,"no pleased crescent")
   rig.advance(3.9);neutral("incoming",true)
 for hz in [30,60]:
  rig.reset();rig.apply_controls({"auto_blink":true})
  for cycle in range(3):
   rig.play_expression(ID)
   for n in range(int(hz*3.9)+1):
    rig.advance(1.0/hz);quiet_pose(rig.pose_now(),"continuous")
    check(rig.head.transform==h and rig.body.transform==b,"fixed registration")
    check(rig.face.oral_objects.upper_teeth.position==Vector2(533,626),"fixed enamel")
    for k in rig.face.objects:
     var node=rig.face.objects[k];var owner=rig.face.homes[k].node
     check(node.scale==Vector2.ONE and owner.scale==Vector2.ONE and node.modulate==fixed[k].modulate and node.modulate.a==1,"rigid opaque anatomy")
     check(node.texture==fixed[k].texture and node.region_enabled==fixed[k].region_enabled and node.region_rect==fixed[k].region_rect,"fixed texture region and UV")
   neutral("continuous end",true)
 rig.reset();rig.apply_controls({"auto_blink":true});rig.advance(4.03)
 check(rig.face.closure.x>.99,"preexisting automatic blink")
 var before=rig.displayed_pose();rig.play_expression(ID)
 check(rig.displayed_pose()==before and not rig.auto_blink and rig.auto_blink_pending_restore,"autoblink interruption C0")
 rig.advance(2.2);check(rig.face.closure==Vector2.ONE and not rig.auto_blink,"long authored hold")
 rig.advance(1.7);neutral("completed restores intent",true)
 check(rig.elapsed==0 and rig.face.closure==Vector2.ZERO,"restoration restarts open")
 rig.advance(4.03);check(rig.face.closure.x>.99,"restored idle blink actually executes")
 rig.advance(.17);check(rig.face.closure==Vector2.ZERO,"idle blink returns open")
 print("MEDITATIVE_RUNTIME checks=",checks," failures=",failures.size());quit(1 if failures.size() else 0)

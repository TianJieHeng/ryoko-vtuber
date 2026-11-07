extends SceneTree
var rig
var checks=0
var failures=[]
func _initialize():call_deferred("run")
func check(ok,label):
 checks+=1
 if not ok:
  failures.append(label)
  if failures.size()<20:push_error(label)
func neutral(label):
 check(rig.pose_now()==rig.neutral_pose(),label+" exact neutral")
 check(rig.active_performance=="" and rig.release_time<0,label+" no stale owner")
func run():
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 check(rig.rig_ready and rig.registry_ready,"ready")
 if not rig.rig_ready or not rig.registry_ready:quit(2);return
 check(rig.registry.resolve("reassure")=="EXP-107" and rig.registry.resolve("confident-reassurance")=="EXP-107","aliases")
 check(rig.list_expressions().size()==6 and rig.registry.resolve("EXP-003")=="" and rig.registry.resolve("EXP-007")=="EXP-007","narrow six-profile scope")
 var d=rig.registry.definition("EXP-107");check(d.duration==3.0 and d.keyframes.size()==11,"eleven keys / three seconds")
 var peaks=[]
 for i in range(1,d.keyframes.size()-1):
  if d.keyframes[i].values.mouth_open>d.keyframes[i-1].values.mouth_open and d.keyframes[i].values.mouth_open>d.keyframes[i+1].values.mouth_open:peaks.append([d.keyframes[i].time,d.keyframes[i].values.mouth_open])
 check(peaks==[[1.20,.60]],"one restrained open accent")
 check(rig.sample_expression("EXP-107",.60).mouth_open==0 and rig.sample_expression("EXP-107",1.56).mouth_open==0,"closed smiles before and after open")
 check(rig.sample_expression("EXP-107",1.2).mouth_oral_lift==1.0,"peak lower oral surface")
 for i in range(3001):
  var p=rig.sample_expression("EXP-107",i*.001)
  for k in p:
   var bounds=rig.Registry.CHANNEL_BOUNDS[k];check(p[k]>=bounds[0] and p[k]<=bounds[1],"bounded "+k)
  for k in ["blink_R","blink_L","gaze_x","gaze_y","hair_sway","blush_intensity"]:check(p[k]==0,"no unnecessary acting "+k)
  check(p.mouth_open<=.600001 and p.eye_smile_R<=.030001 and p.eye_smile_L<=.030001,"restrained mouth/direct eyes")
 var h=rig.head.transform;var b=rig.body.transform
 for t in [0.0,.000001,.2,.299999,.3,.4,.6,.88,1.2,1.56,1.92,2.35,2.68,2.999999]:
  for action in ["release","EXP-107","EXP-163","EXP-005","EXP-001","EXP-006","manual","reset"]:
   rig.reset();rig.play_expression("EXP-107");rig.advance(t);var before=rig.displayed_pose()
   if action=="release":
    check(rig.release(),"release");check(rig.displayed_pose()==before,"release C0");rig.advance(.45);neutral("release")
   elif action.begins_with("EXP-"):
    check(rig.play_expression(action),"handover");check(rig.displayed_pose()==before,"handover C0");rig.advance(10);neutral("handover")
   elif action=="manual":
    check(rig.apply_controls({"mouth_open":.13,"mouth_oral_lift":.41}),"manual")
    check(rig.active_performance=="" and rig.release_time<0,"manual takeover");rig.advance(1)
    check(rig.pose_now().mouth_oral_lift==.41,"no stale resume");rig.reset();neutral("manual/reset")
   else:rig.reset();neutral("reset")
   check(rig.head.transform==h and rig.body.transform==b,"fixed head/body registration")
   check(rig.face.oral_objects.upper_teeth.position==Vector2(533,626),"fixed enamel")
 for id in ["EXP-163","EXP-005","EXP-001","EXP-006"]:
  for t in [.1,.3,1.3,1.91,2.53,4.5]:
   rig.reset();rig.play_expression(id);rig.advance(t);var before=rig.displayed_pose()
   rig.play_expression("EXP-107");check(rig.displayed_pose()==before,"incoming C0");rig.advance(3);neutral("incoming")
 rig.reset();rig.play_expression("EXP-107");rig.advance(1.2);rig.release();rig.advance(.2)
 var before=rig.displayed_pose();rig.play_expression("EXP-107");check(rig.displayed_pose()==before,"retrigger during release C0");rig.advance(3);neutral("release interrupted")
 for hz in [30,60]:
  for cycle in range(5):
   rig.play_expression("EXP-107")
   for i in range(hz*3+1):
    rig.advance(1.0/hz)
    check(rig.head.transform==h and rig.body.transform==b,"continuous fixed registration")
    check(rig.face.oral_objects.upper_teeth.position==Vector2(533,626),"continuous enamel anchor")
    for x in range(81):
     var aperture=rig.face._smile_lip_offset(x,false,false)-rig.face._smile_lip_offset(x,true,false)
     check(aperture>=-.000001 and aperture<=30.800001,"mouth cap")
   neutral("repeat")
 print("REASSURANCE_RUNTIME checks=",checks," failures=",failures.size());quit(1 if failures.size() else 0)

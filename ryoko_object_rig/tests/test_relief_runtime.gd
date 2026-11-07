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
func neutral(label,blink_enabled=false):
 check(rig.pose_now()==rig.neutral_pose(),label+" exact neutral")
 check(rig.active_performance=="" and rig.release_time<0,label+" no stale owner")
 check(rig.auto_blink==blink_enabled,label+" expected auto-blink preference")
func run():
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 check(rig.rig_ready and rig.registry_ready,"ready")
 if not rig.rig_ready or not rig.registry_ready:quit(2);return
 check(rig.registry.resolve("relief")=="EXP-007" and rig.registry.resolve("relieved-smile")=="EXP-007","aliases")
 check(rig.list_expressions().size()==6 and rig.registry.resolve("EXP-003")=="","narrow six-profile scope")
 var d=rig.registry.definition("EXP-007");check(d.duration==3.2 and d.keyframes.size()==9,"nine keys /3.2seconds")
 check(d.keyframes[1].values.brow_tilt_screen_left<0 and d.keyframes[1].values.brow_tilt_screen_right>0,"inner brow ends rise")
 for i in [2,3]:
  var p=d.keyframes[i].values
  check(p.mouth_open>0 and p.mouth_smile==0 and p.mouth_spread==0 and p.mouth_corner_lift==0 and p.mouth_lip_press==1,"parted exhale distinct from smile")
 check(d.keyframes[4].values.mouth_smile>.6 and d.keyframes[5].values.mouth_open==0,"open smile then closed relief")
 for i in range(3201):
  var p=rig.sample_expression("EXP-007",i*.001)
  for k in p:
   var bounds=rig.Registry.CHANNEL_BOUNDS[k];check(p[k]>=bounds[0] and p[k]<=bounds[1],"bounded "+k)
  for k in ["eye_smile_R","eye_smile_L","gaze_x","gaze_y","hair_sway","blush_intensity"]:check(p[k]==0,"no extra acting "+k)
  check(p.mouth_open<=.780001 and p.mouth_purse<=.720001 and p.blink_R<=.090001 and p.blink_L<=.090001,"restrained mouth/open eyes")
 var h=rig.head.transform;var b=rig.body.transform;var fixed={}
 for k in rig.face.objects:
  var n=rig.face.objects[k];fixed[k]={"texture":n.texture,"region_enabled":n.region_enabled,"region_rect":n.region_rect,"modulate":n.modulate}
 for t in [0.0,.000001,.25,.299999,.3,.55,.9,.900001,.91,1.3,1.65,2.1,2.65,3.199999]:
  for action in ["release","EXP-007","EXP-163","EXP-005","EXP-001","EXP-006","EXP-107","manual","reset"]:
   rig.reset();rig.play_expression("EXP-007");rig.advance(t);var before=rig.displayed_pose()
   if action=="release":
    check(rig.release(),"release");check(rig.displayed_pose()==before,"release C0");rig.advance(.45);neutral("release")
   elif action.begins_with("EXP-"):
    check(rig.play_expression(action),"handover");check(rig.displayed_pose()==before,"handover C0");rig.advance(10);neutral("handover")
   elif action=="manual":
    check(rig.apply_controls({"mouth_open":.13,"mouth_oral_lift":.41}),"manual")
    check(rig.active_performance=="" and rig.release_time<0,"manual takeover");rig.advance(1)
    check(rig.pose_now().mouth_oral_lift==.41,"no stale resume");rig.reset();neutral("manual/reset")
   else:rig.reset();neutral("reset")
   check(rig.head.transform==h and rig.body.transform==b,"fixed registration")
   check(rig.face.oral_objects.upper_teeth.position==Vector2(533,626),"fixed enamel")
 for id in ["EXP-163","EXP-005","EXP-001","EXP-006","EXP-107"]:
  for t in [.1,.3,1.3,1.91,2.53,4.5]:
   rig.reset();rig.play_expression(id);rig.advance(t);var before=rig.displayed_pose()
   rig.play_expression("EXP-007");check(rig.displayed_pose()==before,"incoming C0");rig.advance(.9)
   for j in rig.face.smile_eye_joints:check(not rig.face.objects[j.key].visible,"laugh family restored to ordinary eyes")
   rig.advance(3.2);neutral("incoming")
 rig.reset();rig.apply_controls({"auto_blink":true});rig.advance(4.03)
 check(rig.face.closure.x>.99,"active auto-blink visible")
 var before=rig.displayed_pose();rig.play_expression("EXP-007")
 check(rig.displayed_pose()==before and not rig.auto_blink,"incoming auto-blink C0 and disabled")
 rig.advance(3.2);neutral("auto-blink complete",true)
 check(rig.apply_controls({"auto_blink":true}) and rig.auto_blink,"manual auto-blink reenable directly after completion")
 check(rig.active_performance=="" and rig.release_time<0,"reenable keeps manual idle ownership")
 rig.play_expression("EXP-007");rig.advance(.9);rig.release();rig.advance(.45);neutral("auto-blink release",true)
 check(rig.apply_controls({"auto_blink":true}) and rig.auto_blink,"manual auto-blink reenable directly after release")
 rig.reset();rig.apply_controls({"auto_blink":true});rig.advance(4.03)
 check(rig.face.closure.x>.99,"manual auto-blink reenabled after reset")
 rig.reset();rig.play_expression("EXP-007");rig.advance(1.3);rig.release();rig.advance(.2)
 before=rig.displayed_pose();rig.play_expression("EXP-007");check(rig.displayed_pose()==before,"retrigger during release C0");rig.advance(3.2);neutral("release interrupted")
 for hz in [30,60]:
  for cycle in range(3):
   rig.play_expression("EXP-007")
   for i in range(int(hz*3.2)+1):
    rig.advance(1.0/hz)
    check(rig.head.transform==h and rig.body.transform==b,"continuous fixed registration")
    check(rig.face.oral_objects.upper_teeth.position==Vector2(533,626),"continuous enamel anchor")
    for k in rig.face.objects:
     var n=rig.face.objects[k];var owner=rig.face.homes[k].node
     check(n.scale==Vector2.ONE and owner.scale==Vector2.ONE and n.modulate==fixed[k].modulate and n.modulate.a==1,"rigid opaque anatomy")
     check(n.texture==fixed[k].texture and n.region_enabled==fixed[k].region_enabled and n.region_rect==fixed[k].region_rect,"fixed texture region/UV")
    for x in range(81):
     var aperture=rig.face._smile_lip_offset(x,false,false)-rig.face._smile_lip_offset(x,true,false)
     check(aperture>=-.000001 and aperture<=30.800001,"mouth cap")
   neutral("repeat")
 print("RELIEF_RUNTIME checks=",checks," failures=",failures.size());quit(1 if failures.size() else 0)

extends SceneTree
var rig
var checks=0
var failures=[]
const IDS=["EXP-163","EXP-005","EXP-001","EXP-006","EXP-107","EXP-007","EXP-002"]
func _initialize():call_deferred("run")
func check(ok,label):
 checks+=1
 if not ok:
  failures.append(label)
  if failures.size()<20:push_error(label)
func neutral(label, expected_blink=false):
 check(rig.pose_now()==rig.neutral_pose(),label+" exact neutral")
 check(rig.active_performance=="" and rig.release_time<0,label+" no stale owner")
 check(rig.auto_blink==expected_blink,label+" expected idle blink state")
 check(not rig.auto_blink_pending_restore,label+" no stale pending preference")
 for j in rig.face.smile_eye_joints:check(not rig.face.objects[j.key].visible,label+" ordinary idle family")
func run():
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 check(rig.rig_ready and rig.registry_ready,"ready")
 if not rig.rig_ready or not rig.registry_ready:quit(2);return
 var ids=[]
 for e in rig.list_expressions():ids.append(e.id)
 check(ids==IDS,"seven authored profiles")
 for alias in ["affection","affectionate-warmth"]:check(rig.registry.resolve(alias)=="EXP-002","alias "+alias)
 var d=rig.registry.definition("EXP-002")
 check(d.duration==1.9 and d.keyframes.size()==9,"exact source proposal times")
 check(d.keyframes[3].values.eye_smile_R<.1 and d.keyframes[5].values.eye_smile_R<.1,"open eyes before and after brief closure")
 check(d.keyframes[4].values.mouth_smile==d.keyframes[5].values.mouth_smile and d.keyframes[7].values.mouth_smile>0,"smile lingers beyond renewed contact")
 check(d.keyframes[4].values.eye_smile_R>=.85 and d.keyframes[4].values.eye_smile_L>=.85,"upward pleased hold not ordinary blink")
 var fixed={};var h=rig.head.transform;var b=rig.body.transform
 for k in rig.face.objects:
  var n=rig.face.objects[k];fixed[k]={"texture":n.texture,"region_enabled":n.region_enabled,"region_rect":n.region_rect,"modulate":n.modulate,"self_modulate":n.self_modulate}
 for i in range(1901):
  var p=rig.sample_expression("EXP-002",i*.001)
  for k in p:
   var bounds=rig.Registry.CHANNEL_BOUNDS[k];check(p[k]>=bounds[0] and p[k]<=bounds[1],"bounded "+k)
  for k in ["mouth_open","mouth_spread","mouth_purse","mouth_oral_lift","mouth_lip_press","blink_R","blink_L","gaze_x","gaze_y","hair_sway","blush_intensity"]:check(p[k]==0,"sealed quiet acting "+k)
  check(p.eye_smile_R==p.eye_smile_L and p.brow_screen_left==p.brow_screen_right,"symmetric controls")
 for t in [0.0,.000001,.15,.299999,.3,.32,.36,.40,.44,.48,.5,.75,1.05,1.14,1.2,1.26,1.35,1.65,1.899999]:
  for action in ["release","manual","reset"]+IDS:
   rig.reset();rig.play_expression("EXP-002");rig.advance(t);var before=rig.displayed_pose()
   if action=="release":
    check(rig.release(),"release");check(rig.displayed_pose()==before,"release C0");rig.advance(.45);neutral("release")
   elif action=="manual":
    check(rig.apply_controls({"eye_smile_R":.37,"mouth_corner_lift":.13}),"manual takeover")
    check(rig.active_performance=="" and rig.release_time<0,"manual owns rig")
    rig.advance(1);check(is_equal_approx(rig.pose_now().eye_smile_R,.37),"no stale resume");rig.reset();neutral("manual reset")
   elif action=="reset":rig.reset();neutral("reset")
   else:
    check(rig.play_expression(action),"handoff");check(rig.displayed_pose()==before,"handoff C0");rig.advance(10);neutral("handoff")
   check(rig.head.transform==h and rig.body.transform==b,"fixed registration")
 for id in IDS:
  for t in [.1,.3,.66,1.3,1.91,2.53,4.5]:
   rig.reset();rig.play_expression(id);rig.advance(t);var before=rig.displayed_pose()
   check(rig.play_expression("EXP-002"),"incoming "+id);check(rig.displayed_pose()==before,"incoming C0 "+id)
   rig.advance(1.9);neutral("incoming "+id)
 rig.reset();rig.apply_controls({"auto_blink":true});rig.advance(4.03)
 check(rig.face.closure.x>.99,"active ordinary auto-blink")
 var before=rig.displayed_pose();rig.play_expression("EXP-002")
 check(rig.displayed_pose()==before and not rig.auto_blink,"auto-blink incoming C0")
 rig.advance(1.9);neutral("auto-blink completion",true)
 check(rig.elapsed==0,"restored ordinary clock starts open")
 check(rig.apply_controls({"auto_blink":true}) and rig.auto_blink,"safe manual reenable")
 var target_wait=fposmod(4.03-fposmod(rig.elapsed,4.2),4.2)
 rig.advance(target_wait);check(rig.face.closure.x>.99,"ordinary auto-blink after restoration and explicit reenable")
 rig.reset();rig.play_expression("EXP-002");rig.advance(.9);rig.release();rig.advance(.2)
 before=rig.displayed_pose();rig.play_expression("EXP-002");check(rig.displayed_pose()==before,"release retrigger C0");rig.advance(1.9);neutral("release retrigger")
 for hz in [30,60]:
  for cycle in range(3):
   rig.play_expression("EXP-002")
   for i in range(int(ceil(hz*1.9))+1):
    rig.advance(1.0/hz)
    check(rig.head.transform==h and rig.body.transform==b,"repeat fixed registration")
    check(rig.face.oral_objects.upper_teeth.position==Vector2(533,626),"fixed enamel")
    check(rig.face.mouth_opening==0,"sealed mouth")
    for k in rig.face.objects:
     var n=rig.face.objects[k];var owner=rig.face.homes[k].node
     check(n.scale==Vector2.ONE and owner.scale==Vector2.ONE and n.modulate==fixed[k].modulate and n.self_modulate==fixed[k].self_modulate and n.modulate.a==1,"rigid full-opacity anatomy")
     check(n.texture==fixed[k].texture and n.region_enabled==fixed[k].region_enabled and n.region_rect==fixed[k].region_rect,"fixed pigment UV")
   neutral("repeat")
 print("AFFECTION_RUNTIME checks=",checks," failures=",failures.size());quit(1 if failures.size() else 0)

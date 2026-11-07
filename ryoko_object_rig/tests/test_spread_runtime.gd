extends SceneTree
var rig
var checks=0
var fails=[]
func _initialize():call_deferred("run")
func check(ok:bool,label:String):
 checks+=1
 if not ok:fails.append(label);push_error(label)
func state_without_error():
 var s=rig.get_state();s.erase("last_error");return s
func run():
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 check(rig.registry_ready and rig.face.ready_for_controls,"ready with every imported texture")
 check(rig.list_expressions().size()==7,"seven registered scoped definitions")
 check(rig.Registry.CHANNEL_BOUNDS.mouth_spread==[0.0,1.0],"spread registry bounds")
 var d=rig.registry.definition("EXP-001")
 check(d.duration==3.0 and d.keyframes.size()==9,"nine-key greeting")
 check(rig.face.oral_objects.upper_teeth.position==Vector2(533,626),"front arch anchor")
 var originals={}
 for k in rig.face.objects:originals[k]=rig.face.objects[k].texture
 for s in [0.0,.00001,.01,.1,.25,.5,.75,.99,.99999,1.0]:
  for m in [0.0,.00001,.01,.1,.25,.5,.75,.99,.99999,1.0]:
   for o in [0.0,.00001,.01,.1,.25,.5,.75,.99,.99999,1.0]:
    check(rig.apply_controls({"mouth_spread":s,"mouth_smile":m,"mouth_open":o}),"cube accepted")
    check(is_equal_approx(rig.face.mouth_spread,s*m),"documented multiplicative smile coupling")
    check(rig.face.oral_objects.upper_teeth.position==Vector2(533,626),"front arch never moves")
    check(rig.head.position==Vector2(6,70) and rig.body.position==Vector2(6,70),"no head or body drift")
    for k in rig.face.objects:
     var n=rig.face.objects[k];var p=rig.face.homes[k].node
     check(n.scale==Vector2.ONE and p.scale==Vector2.ONE and n.modulate.a==1 and p.modulate.a==1,"unit scale opacity1 "+k)
     check(n.texture==originals[k],"no texture substitution "+k)
 for id in ["EXP-163","EXP-005"]:
  var duration=rig.registry.definition(id).duration
  for i in range(101):check(rig.sample_expression(id,duration*i/100.0).mouth_spread==0,"older profile zero spread")
 for mode in ["manual","active","release"]:
  rig.reset();rig.apply_controls({"mouth_spread":.7,"mouth_smile":.8,"mouth_open":.6})
  if mode!="manual":rig.play_expression("EXP-001");rig.advance(1.4)
  if mode=="release":rig.release();rig.advance(.1)
  for value in [-.000001,1.000001,NAN,INF,-INF,true,"1",null,{},[]]:
   var before=state_without_error();var parts=rig.face.snapshot()
   check(not rig.apply_controls({"mouth_spread":value,"reset":true,"mouth_open":.3}),"invalid spread rejected")
   check(state_without_error()==before and rig.face.snapshot()==parts,"invalid transaction fully atomic")
 for t in [0.0,.001,.3,.62,1.02,1.4,1.9,2.25,2.5,2.99]:
  for action in ["release","self","yawn","laugh","manual","reset"]:
   rig.reset();rig.play_expression("EXP-001");rig.advance(t);var before=rig.displayed_pose()
   if action=="release":
    rig.release();check(rig.displayed_pose()==before,"release C0");rig.advance(.5)
   elif action=="manual":
    rig.apply_controls({"mouth_spread":.31});check(rig.active_performance=="" and rig.pose_now().mouth_spread==.31,"manual takeover");rig.reset()
   elif action=="reset":rig.reset()
   else:
    var ids={"self":"EXP-001","yawn":"EXP-163","laugh":"EXP-005"}
    rig.play_expression(ids[action]);check(rig.displayed_pose()==before,"retrigger or handover C0");rig.advance(10)
   check(rig.displayed_pose()==rig.neutral_pose() and rig.face.mouth_spread==0,"complete neutral release")
 for id in ["EXP-163","EXP-005"]:
  rig.reset();rig.play_expression(id);rig.advance(1.5);var before=rig.displayed_pose();rig.play_expression("EXP-001");check(rig.displayed_pose()==before,"old to001 C0");rig.advance(10)
 for _n in range(3):
  rig.play_expression("EXP-001")
  for _i in range(181):rig.advance(1.0/60.0)
  check(rig.displayed_pose()==rig.neutral_pose(),"repeat ends neutral")
 print("SPREAD_RUNTIME checks=",checks," failures=",fails.size());quit(1 if fails.size() else 0)

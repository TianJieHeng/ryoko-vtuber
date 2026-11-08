extends SceneTree
var rig
var checks=0
var failures=[]
func _initialize():call_deferred("run")
func check(ok,label):
 checks+=1
 if not ok:failures.append(label);push_error(label)
func state():
 var s=rig.get_state();s.erase("last_error");return s
func signature(n):return [n.texture,n.transform,n.modulate,n.self_modulate,n.z_index,n.visible]
func core_state():
 var s={}
 for key in rig.face.objects:s[key]=[signature(rig.face.objects[key]),rig.face.homes[key].node.transform]
 for key in rig.face.oral_objects:s["ORAL_"+key]=signature(rig.face.oral_objects[key])
 return s
func run():
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 check(rig.rig_ready and rig.registry_ready,"readiness")
 if not rig.rig_ready or not rig.registry_ready:quit(2);return
 check(rig.Registry.CHANNEL_BOUNDS.blush_intensity==[0.0,1.0],"bounded effect registry")
 check(rig.face.effect_objects.size()==2,"separate source FX cheeks")
 var bridge=load("res://control_bridge.gd").new();bridge.rig=rig
 check(bridge.capabilities().controls.blush_intensity==[0.0,1.0],"bridge bounds");bridge.free()
 var effect_signatures={}
 for key in rig.face.effect_objects:
  var n=rig.face.effect_objects[key];effect_signatures[key]=[n.texture,n.transform,n.self_modulate,n.z_index]
  check(n.scale==Vector2.ONE and n.rotation==0 and n.z_index==29,"fixed registered placement below eyes and hair")
 for expression in rig.registry.list_expressions():
  for t in [0.0,.2,.7,1.0,1.36,1.54,2.04,expression.duration]:
   rig.reset();rig.play_expression(expression.id);rig.advance(t)
   if expression.id not in ["EXP-006","EXP-160"]:check(rig.pose_now().blush_intensity==0,"prior profile defaults zero")
   var before=core_state()
   for value in [0.0,.000001,.1,.35,.7,1.0,.7,.1,0.0]:
    check(rig.apply_controls({"blush_intensity":value}),"valid intensity")
    check(core_state()==before,"FX never changes facial source/opacity/geometry "+expression.id)
    check(rig.face.effect_owner=="manual" and rig.active_performance=="","manual FX ownership")
    for key in rig.face.effect_objects:
     var n=rig.face.effect_objects[key]
     check([n.texture,n.transform,n.self_modulate,n.z_index]==effect_signatures[key],"fixed effect texture and transform")
     check(is_equal_approx(n.modulate.a,value) and n.modulate.r==1 and n.modulate.g==1 and n.modulate.b==1,"only effect alpha intensity")
     check(n.visible==(value>0),"zero effect invisible")
 for mode in ["manual","active","release"]:
  rig.reset();rig.apply_controls({"blush_intensity":.7})
  if mode!="manual":rig.play_expression("EXP-006");rig.advance(1)
  if mode=="release":rig.release();rig.advance(.1)
  for bad in [-.000001,1.000001,NAN,INF,-INF,true,false,"0.5",null,{},[]]:
   var before=state();var face=rig.face.snapshot()
   check(not rig.apply_controls({"reset":true,"blush_intensity":bad,"mouth_open":.3}),"invalid effect transaction")
   check(state()==before and rig.face.snapshot()==face,"invalid effect transaction atomic")
 for t in [0.0,.000001,.2,.3,.7,1.0,1.18,1.36,1.54,2.04,2.7]:
  for action in ["release","retrigger","reset","manual","handover"]:
   rig.reset();rig.play_expression("EXP-006");rig.advance(t)
   var before=rig.displayed_pose()
   if action=="release":
    rig.release();check(before==rig.displayed_pose(),"effect release C0");check(rig.face.effect_owner=="release","release owns effects");rig.advance(.45)
   elif action=="retrigger":
    rig.play_expression("EXP-006");check(before==rig.displayed_pose(),"effect retrigger C0");rig.advance(10)
   elif action=="reset":rig.reset()
   elif action=="manual":
    rig.apply_controls({"blush_intensity":.4});check(rig.active_performance=="" and rig.face.effect_owner=="manual" and rig.pose_now().blush_intensity==.4,"manual takeover");rig.reset()
   else:
    for id in ["EXP-001","EXP-005","EXP-163","EXP-006"]:
     var current=rig.displayed_pose();rig.play_expression(id);check(current==rig.displayed_pose(),"cross-expression C0");check(rig.face.effect_owner==id,"active effect ownership");rig.advance(.05)
    rig.advance(10)
   check(rig.displayed_pose()==rig.neutral_pose() and rig.face.blush_intensity==0,"effect settles exact neutral")
   for n in rig.face.effect_objects.values():check(not n.visible and n.modulate.a==0,"effect clears")
 print("BLUSH_CONTROLS checks=",checks," failures=",failures.size());quit(1 if failures.size() else 0)

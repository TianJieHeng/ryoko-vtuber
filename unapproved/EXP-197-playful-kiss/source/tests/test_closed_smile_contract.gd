extends SceneTree
var rig
var checks=0
var failures=[]
func _initialize():call_deferred("run")
func check(ok:bool,label:String):
 checks+=1
 if not ok:
  if failures.size()<30:push_error(label)
  failures.append(label)
func state():
 var s=rig.get_state();s.erase("last_error");return s
func signature(n):
 var s=[n.texture,n.scale,n.modulate,n.self_modulate,n.offset,n.flip_h,n.flip_v,n.region_enabled,n.region_rect]
 if n.texture is AtlasTexture:s.append_array([n.texture.atlas,n.texture.region,n.texture.margin])
 return s
func transforms():
 var result={}
 for k in rig.face.objects:
  var n=rig.face.objects[k];result[k]=[n.transform,n.get_parent().transform]
 for k in rig.face.oral_objects:result["oral_"+k]=rig.face.oral_objects[k].transform
 return result
func run():
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 check(rig.rig_ready and rig.registry_ready,"import readiness")
 if not rig.rig_ready or not rig.registry_ready:quit(2);return
 var bridge=load("res://control_bridge.gd").new();bridge.rig=rig
 var caps=bridge.capabilities()
 for axis in ["mouth_lip_press","mouth_corner_lift"]:
  check(rig.Registry.CHANNEL_BOUNDS[axis]==[0.0,1.0],"registry bounds "+axis)
  check(caps.controls[axis]==[0.0,1.0],"bridge bounds "+axis)
  check(rig.pose_now()[axis]==0.0 and rig.neutral_pose()[axis]==0.0,"zero defaults "+axis)
 check(caps.closed_smile.maximum_inner_lip_depth_source_px==4.0,"bridge 4px depth")
 bridge.free()
 check(rig.face.pressed_lip_owners.size()==14,"fourteen rigid inner lip owners")
 var oral_signatures={}
 for k in rig.face.oral_objects:oral_signatures[k]=signature(rig.face.oral_objects[k])
 check(is_equal_approx(56.0*rig.face.MAX_MOUTH_APERTURE,30.8),"physical aperture maximum")
 var signatures={}
 for k in rig.face.objects:signatures[k]=signature(rig.face.objects[k])
 for c in [0.0,.000001,.25,.5,.75,.999999,1.0]:
  for s in [0.0,.5,1.0]:
   for m in [0.0,.5,1.0]:
    for o in [0.0,.000001,.5,1.0]:
     check(rig.apply_controls({"reset":true,"mouth_corner_lift":c,"mouth_spread":s,"mouth_smile":m,"mouth_open":o,"mouth_lip_press":0.0}),"base combination accepted")
     var base=transforms()
     for p in [0.0,.000001,.25,.5,.75,.999999,1.0]:
      check(rig.apply_controls({"mouth_lip_press":p}),"pressure accepted")
      check(transforms()==base,"pressure never translates/rotates original or inner owners")
      check(is_equal_approx(rig.face.mouth_lip_press,p) and is_equal_approx(rig.face.mouth_corner_lift,c),"independent axes")
      check(is_equal_approx(rig.face.mouth_spread,s*m),"existing spread coupling")
      check(rig.face.oral_objects.upper_teeth.position==Vector2(533,626),"central enamel anchor")
      for k in rig.face.objects:
       var n=rig.face.objects[k];var owner=rig.face.homes[k].node
       check(signature(n)==signatures[k],"immutable pigment/atlas/opacity "+k)
       check(n.scale==Vector2.ONE and owner.scale==Vector2.ONE and n.modulate.a==1 and owner.modulate.a==1,"rigid unit owner "+k)
      for k in rig.face.oral_objects:check(signature(rig.face.oral_objects[k])==oral_signatures[k],"immutable oral pigment/scale/opacity "+k)
      for e in rig.face.pressed_lip_owners:
       check(e.node.get_parent()==rig.face.homes[e.parent].node,"shared upper pivot")
       check(e.node.visible==(p>0),"pressure support visibility")
       check(is_equal_approx(e.node.material.get_shader_parameter("lip_press"),p),"pressure depth uniform")
     for x in range(81):
      var aperture=rig.face._smile_lip_offset(x,false,false)-rig.face._smile_lip_offset(x,true,false)
      check(aperture>=-.000001 and aperture<=30.800001,"bounded 30.8px aperture")
 for expression in rig.registry.list_expressions():
  for mode in ["manual","active","release"]:
   rig.reset();rig.apply_controls({"mouth_corner_lift":.77,"mouth_lip_press":.63,"mouth_open":.4})
   if mode!="manual":rig.play_expression(expression.id);rig.advance(.3)
   if mode=="release":rig.release();rig.advance(.1)
   for axis in ["mouth_corner_lift","mouth_lip_press"]:
    for invalid in [-.000001,1.000001,NAN,INF,-INF,true,false,"1",null,{},[]]:
     var before=state();var geometry=transforms();var face=rig.face.snapshot()
     var tx={"reset":true,"mouth_open":.3,"mouth_smile":.9,"mouth_corner_lift":.2,"mouth_lip_press":.8};tx[axis]=invalid
     check(not rig.apply_controls(tx),"invalid transaction rejected "+axis)
     check(state()==before and transforms()==geometry and rig.face.snapshot()==face,"full transaction atomicity "+expression.id+mode+axis)
  for t in [0.0,.000001,.3,expression.duration*.45,expression.duration-.001]:
   for action in ["release","manual","reset","handover","retrigger"]:
    rig.reset();rig.apply_controls({"mouth_corner_lift":.8,"mouth_lip_press":.9,"mouth_open":.2,"mouth_smile":.6})
    var start=rig.displayed_pose();check(rig.play_expression(expression.id),"profile play");check(rig.displayed_pose()==start,"incoming C0")
    rig.advance(t);var before=rig.displayed_pose()
    if action=="release":
     rig.release();check(rig.displayed_pose()==before,"release C0");rig.advance(10)
    elif action=="manual":
     check(rig.apply_controls({"mouth_corner_lift":.31,"mouth_lip_press":.43}),"manual takeover")
     check(rig.active_performance=="" and rig.pose_now().mouth_corner_lift==.31 and rig.pose_now().mouth_lip_press==.43,"manual axes retained");rig.reset()
    elif action=="reset":rig.reset()
    elif action=="retrigger":
     rig.play_expression(expression.id);check(rig.displayed_pose()==before,"retrigger C0");rig.advance(10)
    else:
     for destination in rig.registry.list_expressions():
      var a=rig.displayed_pose();rig.play_expression(destination.id);check(rig.displayed_pose()==a,"cross-profile C0");rig.advance(.05)
     rig.advance(10)
    check(rig.displayed_pose()==rig.neutral_pose() and rig.face.mouth_lip_press==0 and rig.face.mouth_corner_lift==0,"exact neutral completion")
 print("CLOSED_SMILE_CONTRACT checks=",checks," failures=",failures.size()," (structural/runtime only; no visual likeness verdict)")
 quit(1 if failures.size() else 0)

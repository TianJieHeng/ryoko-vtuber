extends SceneTree
var rig
var checks=0
var failures=[]
func _initialize():call_deferred("run")
func check(ok:bool,label:String):
    checks+=1
    if not ok:failures.append(label);push_error(label)
func state_without_error():
    var state=rig.get_state();state.erase("last_error");return state
func texture_signature(node):
    var value=[node.texture,node.scale,node.modulate]
    if node.texture is AtlasTexture:value.append(node.texture.atlas);value.append(node.texture.region);value.append(node.texture.margin)
    return value
func run():
    rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
    check(rig.rig_ready and rig.registry_ready,"required imported assets ready")
    if not rig.rig_ready or not rig.registry_ready:quit(2);return
    check(rig.Registry.CHANNEL_BOUNDS.mouth_corner_lift==[0.0,1.0],"corner registry bounds")
    var textures={}
    for key in rig.face.objects:textures[key]=texture_signature(rig.face.objects[key])
    for c in [0.0,.000001,.01,.25,.5,.75,.999999,1.0]:
      for s in [0.0,.000001,.5,1.0]:
       for m in [0.0,.000001,.5,1.0]:
        for o in [0.0,.000001,.5,1.0]:
            check(rig.apply_controls({"reset":true,"mouth_corner_lift":c,"mouth_spread":s,"mouth_smile":m,"mouth_open":o}),"accepted mouth cube")
            check(absf(rig.face.mouth_corner_lift-c)<.000001,"independent corner control")
            check(is_equal_approx(rig.face.mouth_spread,s*m),"unchanged spread coupling")
            check(rig.face.oral_objects.upper_teeth.position==Vector2(533,626),"fixed central enamel")
            check(rig.head.position==Vector2(6,70) and rig.body.position==Vector2(6,70),"stationary head/body")
            for key in rig.face.objects:
                var n=rig.face.objects[key];var p=rig.face.homes[key].node
                check(texture_signature(n)==textures[key],"fixed source/region/alpha "+key)
                check(n.scale==Vector2.ONE and p.scale==Vector2.ONE and n.modulate.a==1 and p.modulate.a==1,"rigid unit owners "+key)
            for x in range(81):
                var old=rig.face.mouth_corner_lift
                var upper=rig.face._smile_lip_offset(x,true,false)
                var lower=rig.face._smile_lip_offset(x,false,false)
                check(lower-upper>=-.000001 and lower-upper<=29.700001,"bounded rigid lip separation")
    for mode in ["manual","active","release"]:
        rig.reset();rig.apply_controls({"mouth_corner_lift":.77,"mouth_spread":.6,"mouth_smile":.8,"mouth_open":.4})
        if mode!="manual":rig.play_expression("EXP-006");rig.advance(1.0)
        if mode=="release":rig.release();rig.advance(.1)
        for value in [-.000001,1.000001,NAN,INF,-INF,true,"1",null,{},[]]:
            var before=state_without_error();var face=rig.face.snapshot()
            check(not rig.apply_controls({"mouth_corner_lift":value,"reset":true,"mouth_open":.3}),"invalid corner rejected")
            check(state_without_error()==before and rig.face.snapshot()==face,"atomic invalid input")
    for e in rig.registry.list_expressions():
      for t in [0.0,.000001,.3,e.duration*.45,e.duration-.001]:
       for action in ["release","manual","reset","handover"]:
        rig.reset();rig.apply_controls({"mouth_corner_lift":.8,"mouth_open":.2,"mouth_smile":.6})
        var start=rig.displayed_pose();rig.play_expression(e.id)
        check(rig.displayed_pose()==start,"incoming corner handover C0")
        rig.advance(t);var before=rig.displayed_pose()
        if action=="release":
            rig.release();check(rig.displayed_pose()==before,"release C0");rig.advance(.5)
        elif action=="manual":
            rig.apply_controls({"mouth_corner_lift":.31});check(rig.active_performance=="" and rig.pose_now().mouth_corner_lift==.31,"manual corner takeover");rig.reset()
        elif action=="reset":rig.reset()
        else:
            for destination in rig.registry.list_expressions():
                var a=rig.displayed_pose();rig.play_expression(destination.id);check(rig.displayed_pose()==a,"cross-profile handover C0 "+destination.id);rig.advance(.05)
            rig.advance(10)
        check(rig.displayed_pose()==rig.neutral_pose() and rig.face.mouth_corner_lift==0,"neutral reset/release/completion")
    for _cycle in range(3):
        rig.play_expression("EXP-006")
        for _i in range(181):check(rig.advance(1.0/60.0),"repeat advance")
        check(rig.displayed_pose()==rig.neutral_pose(),"repeat exact neutral")
    print("CORNER_LIFT_RUNTIME checks=",checks," failures=",failures.size())
    quit(1 if failures.size() else 0)

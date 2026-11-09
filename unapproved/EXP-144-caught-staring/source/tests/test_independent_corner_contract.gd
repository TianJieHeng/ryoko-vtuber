extends SceneTree
const AXES=["mouth_corner_lift_screen_left","mouth_corner_lift_screen_right"]
const SHADERS=["object_mouth_clip.gdshader","smile_lip_segment.gdshader","smile_lip_join.gdshader","pressed_lip_clip.gdshader","spread_teeth_clip.gdshader"]
var rig
var checks=0
var failures=[]
func _initialize():call_deferred("run")
func check(ok,label):
 checks+=1
 if not ok:
  if failures.size()<30:push_error(label)
  failures.append(label)
func state():
 var s=rig.get_state();s.erase("last_error");return s
func fingerprint(n):return [n.texture,n.scale,n.modulate,n.self_modulate,n.offset,n.flip_h,n.flip_v,n.region_enabled,n.region_rect]
func run():
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 check(rig.rig_ready and rig.registry_ready,"ready")
 if not rig.rig_ready or not rig.registry_ready:quit(2);return
 check(rig.list_expressions().size()==18 and rig.registry.resolve("EXP-181")=="EXP-181","eighteen approved profiles including EXP-181")
 for axis in AXES:check(rig.neutral_pose()[axis]==0 and rig.pose_now()[axis]==0 and rig.Registry.CHANNEL_BOUNDS[axis]==[0.0,1.0],"default schema "+axis)
 var bridge=load("res://control_bridge.gd").new();bridge.rig=rig;var cap=bridge.capabilities()
 for axis in AXES:check(cap.controls[axis]==[0.0,1.0],"bridge bounds")
 check(cap.independent_corners.maximum_total_cubic_lift_source_px==12.0,"bounded combined budget")
 bridge.session=1;bridge.external_enabled=true
 bridge.dispatch(JSON.stringify({"protocol":1,"id":1,"verb":"capabilities"}).to_utf8_buffer());bridge.outgoing.clear()
 bridge.dispatch(JSON.stringify({"protocol":1,"id":2,"session":1,"verb":"apply_controls","args":{AXES[0]:.7,AXES[1]:.3}}).to_utf8_buffer())
 var response=JSON.parse_string(bridge.outgoing.get_string_from_utf8());bridge.outgoing.clear()
 check(response.ok and is_equal_approx(response.result.rig.controls[AXES[0]],.7) and is_equal_approx(response.result.rig.controls[AXES[1]],.3),"shared bridge coordinates")
 check(not bridge.enabled and not bridge.server.is_listening(),"no socket test claimed");bridge.free()
 var pigment={}
 for k in rig.face.objects:pigment[k]=fingerprint(rig.face.objects[k])
 var combinations=[{}, {"mouth_open":1.0}, {"mouth_smile":1.0}, {"mouth_smile":1.0,"mouth_spread":1.0}, {"mouth_purse":1.0}, {"mouth_purse":1.0,"mouth_open":1.0}, {"mouth_smile":1.0,"mouth_spread":1.0,"mouth_open":1.0,"mouth_purse":1.0,"mouth_lip_press":1.0,"mouth_oral_lift":1.0}, {"mouth_smile":.3,"mouth_spread":.7,"mouth_open":.08,"mouth_purse":.4,"mouth_lip_press":.5,"mouth_oral_lift":.7}]
 var count=0
 for bilateral in [0.0,.5,1.0]:
  for sides in [Vector2.ZERO,Vector2(.000001,0),Vector2(0,.000001),Vector2(1,0),Vector2(0,1),Vector2.ONE,Vector2(.3,.7)]:
   for combination in combinations:
    var controls=combination.duplicate();controls.merge({"reset":true,"mouth_corner_lift":bilateral,AXES[0]:sides.x,AXES[1]:sides.y})
    check(rig.apply_controls(controls),"combined pose accepted");count+=1
    check(rig.face.mouth_corner_sides.is_equal_approx(sides),"side coordinate propagation")
    for x in [4.0,12.0,26.0,39.4999,39.5,39.5001,53.0,67.0,75.0]:
     var radius=clampf(abs((x-39.5)/35.5),0,1);var side=sides.x if x<39.5 else sides.y
     var expected=-12.0*(bilateral+(1.0-bilateral)*side)*radius*radius*radius
     check(absf(rig.face._corner_curve(x)-expected)<.000002,"bounded piecewise cubic")
     var gap=rig.face._smile_lip_offset(x,false,false)-rig.face._smile_lip_offset(x,true,false)
     check(gap>=-.000001 and gap<=29.700001,"nonnegative bounded lip separation")
    check(rig.face._corner_curve(39.5)==0.0,"center unchanged")
    check(rig.face.oral_objects.upper_teeth.position==Vector2(533,626),"fixed upper enamel")
    for k in rig.face.objects:
     var n=rig.face.objects[k];var owner=rig.face.homes[k].node
     check(fingerprint(n)==pigment[k] and owner.scale==Vector2.ONE and owner.modulate.a==1 and is_finite(owner.rotation) and owner.position.is_finite(),"rigid fixed pigment "+k)
     if n.material and n.material.shader and n.material.shader.resource_path.get_file() in SHADERS:
      check(n.material.get_shader_parameter("corner_lift_sides").is_equal_approx(sides),"complete shader propagation "+k)
    check(rig.head.position==Vector2(6,70) and rig.body.position==Vector2(6,70),"fixed head/body")
 var fixture={"id":"TEST-CORNERS","title":"Detached test only","duration":1.0,"keyframes":[{"time":0.0,"phase":"neutral","values":{}},{"time":.5,"phase":"corners","values":{AXES[0]:1.0,AXES[1]:.5}},{"time":1.0,"phase":"neutral","values":{}}]}
 check(rig.registry.validate_definition(fixture,fixture.id),"timeline channels valid")
 check(rig._sample(fixture,.25)[AXES[0]]==.5 and rig._sample(fixture,.25)[AXES[1]]==.25,"shared timeline sampler")
 var omitted=rig.neutral_pose()
 for axis in AXES:omitted.erase(axis)
 rig.apply_controls({AXES[0]:1.0,AXES[1]:1.0});rig._apply_performance_pose(omitted)
 for axis in AXES:check(rig.pose_now()[axis]==0 and rig.current_pose[axis]==0,"omitted internal values zero")
 for e in rig.list_expressions():
  for key in rig.registry.definition(e.id).keyframes:
   var p=rig.sample_expression(e.id,key.time)
   for axis in AXES:check(is_equal_approx(p[axis],key.values.get(axis,0.0)),"profile authored side or omitted zero "+e.id)
   if e.id in ["EXP-163","EXP-005","EXP-001","EXP-006","EXP-107","EXP-007","EXP-002","EXP-152","EXP-160","EXP-177","EXP-164","EXP-021"]:
    for axis in AXES:check(p[axis]==0 and key.values.get(axis,0.0)==0,"original twelve side default remains zero "+e.id)
  for mode in ["manual","active","release"]:
   rig.reset();rig.apply_controls({AXES[0]:.8,AXES[1]:.3,"auto_blink":true})
   if mode!="manual":rig.play_expression(e.id);rig.advance(.1)
   if mode=="release":rig.release();rig.advance(.1)
   for axis in AXES:
    for invalid in [-.000001,1.000001,NAN,INF,-INF,true,false,"1",null,{},[]]:
     var before=state();var face=rig.face.snapshot()
     check(not rig.apply_controls({"reset":true,"mouth_open":.6,axis:invalid}),"invalid side rejected")
     check(state()==before and rig.face.snapshot()==face,"invalid input atomic")
  for action in ["release","manual","reset","retrigger","handover"]:
   rig.reset();rig.apply_controls({AXES[0]:.7,AXES[1]:.2,"auto_blink":true})
   var start=rig.displayed_pose();rig.play_expression(e.id);check(rig.displayed_pose()==start,"entry C0")
   rig.advance(.1);var before=rig.displayed_pose()
   if action=="release":rig.release();check(rig.displayed_pose()==before,"release C0");rig.advance(1)
   elif action=="manual":
    rig.apply_controls({AXES[0]:.4});check(rig.active_performance=="" and not rig.auto_blink_pending_restore,"manual takeover")
    rig.advance(.8);check(is_equal_approx(rig.pose_now()[AXES[0]],.4),"manual persists");rig.reset()
   elif action=="reset":rig.reset()
   else:
    rig.play_expression(e.id if action=="retrigger" else "EXP-005");check(rig.displayed_pose()==before,"handover/retrigger C0");rig.advance(10)
   check(rig.pose_now()==rig.neutral_pose() and rig.face.mouth_corner_sides==Vector2.ZERO,"exact neutral recovery")
   check(rig.auto_blink==(action not in ["manual","reset"]),"auto-blink lifecycle preserved")
 rig.reset();rig.apply_controls({AXES[0]:.6,AXES[1]:.3})
 check(rig.apply_controls({"mouth_open":.4}) and is_equal_approx(rig.pose_now()[AXES[0]],.6),"omitted manual side retained")
 check(rig.apply_controls({"reset":true,AXES[0]:.2}) and is_equal_approx(rig.pose_now()[AXES[0]],.2) and rig.pose_now()[AXES[1]]==0,"reset then explicit value")
 print("INDEPENDENT_CORNER_CONTRACT checks=",checks," poses=",count," failures=",failures.size())
 quit(0 if failures.is_empty() else 1)

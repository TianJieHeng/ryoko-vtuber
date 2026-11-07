extends SceneTree
## Numeric/ownership contract only. Visual support is separately reviewed.
const AXES=["brow_inner_lift_screen_left","brow_inner_lift_screen_right"]
const IDS=["EXP-163","EXP-005","EXP-001","EXP-006","EXP-107","EXP-007","EXP-002","EXP-152","EXP-160","EXP-177"]
var rig
var checks=0
var failures=[]
var poses=0
func _initialize():call_deferred("run")
func check(ok,label):
 checks+=1
 if not ok:
  if failures.size()<20:push_error(label)
  failures.append(label)
func state():
 var s=rig.get_state();s.erase("last_error");return s
func other_geometry():
 var s=rig.face.snapshot();s.objects.erase("brow_screen_left");s.objects.erase("brow_screen_right");return s
func fingerprint(n):return [n.texture,n.scale,n.modulate,n.self_modulate,n.offset,n.flip_h,n.flip_v,n.region_enabled,n.region_rect,n.material]
func verify_pose(left,right,tilt_left,tilt_right,up_left,up_right):
 for i in [0,1]:
  var side="screen_left" if i==0 else "screen_right";var k="brow_"+side
  var p=rig.face.homes[k].node;var v=left if i==0 else right;var tilt=tilt_left if i==0 else tilt_right;var up=up_left if i==0 else up_right
  var expected=deg_to_rad(8)*tilt+(-1.0 if i==0 else 1.0)*deg_to_rad(rig.Limits.BROW_INNER_LIFT_DEGREES)*v
  check(absf(p.rotation-expected)<.000001,"signed additive pivot rotation "+side)
  check(p.scale==Vector2.ONE and rig.face.objects[k].scale==Vector2.ONE,"unit scale "+side)
  var home=rig.face.homes[k].pivot
  var a=rig.Limits.BROW_OUTER_ANCHORS[side]-home
  var old_angle=(Vector2(tilt_left,tilt_right)*deg_to_rad(8))[i]
  var target=home+Vector2(0,-10*up)+a.rotated(old_angle)
  check((p.position+a.rotated(p.rotation)).distance_to(target)<.00015,"fixed legacy-transformed outer anchor "+side)
  if v==0:
   check(p.position==home+Vector2(0,-10*up) and p.rotation==old_angle,"exact default-zero published transform "+side)
  check(is_equal_approx(rig.pose_now()[AXES[i]],v) and is_equal_approx(rig.displayed_pose()[AXES[i]],v),"state coordinate "+side)
 poses+=1
func run():
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 check(rig.rig_ready and rig.registry_ready,"ready")
 if not rig.rig_ready or not rig.registry_ready:quit(2);return
 var ids=[]
 for e in rig.list_expressions():ids.append(e.id)
 check(ids==IDS,"only nine approved profiles")
 for axis in AXES:check(rig.neutral_pose()[axis]==0 and rig.pose_now()[axis]==0 and rig.Registry.CHANNEL_BOUNDS[axis]==[0.0,1.0],"default and schema "+axis)
 var bridge=load("res://control_bridge.gd").new();bridge.rig=rig;var cap=bridge.capabilities()
 for axis in AXES:check(cap.controls[axis]==[0.0,1.0],"bridge normalized range")
 check(cap.brow_inner_lift.additional_rotation_degrees==26 and cap.brow_inner_lift.default==0,"bounded preparation capabilities")
 check(cap.brow_inner_lift.zero_lift_legacy_transform_exact and not cap.brow_inner_lift.nonzero_v0_compatible,"honest mapping revision semantics")
 check(cap.brow_inner_lift.outer_anchor_canonical.screen_left==[466.550,452.350] and cap.brow_inner_lift.outer_anchor_canonical.screen_right==[646.227,453.773],"capabilities identify native anchors")
 check(not cap.ai_model_connected and not cap.tts_connected,"no provider service")
 # Callable parser/dispatch preparation; do not start a server.
 bridge.session=1;bridge.external_enabled=true
 bridge.dispatch(JSON.stringify({"protocol":1,"id":1,"verb":"capabilities"}).to_utf8_buffer())
 var response=JSON.parse_string(bridge.outgoing.get_string_from_utf8());bridge.outgoing.clear()
 check(response.ok and JSON.stringify(response).to_utf8_buffer().size()<bridge.MAX_RESPONSE_BYTES,"bounded serialized capabilities")
 bridge.dispatch(JSON.stringify({"protocol":1,"id":2,"session":1,"verb":"apply_controls","args":{AXES[0]:.5,AXES[1]:.25}}).to_utf8_buffer())
 response=JSON.parse_string(bridge.outgoing.get_string_from_utf8());bridge.outgoing.clear()
 check(response.ok and response.result.rig.controls[AXES[0]]==.5 and response.result.rig.controls[AXES[1]]==.25,"callable bridge sends shared coordinates")
 var unchanged=state()
 bridge.dispatch(JSON.stringify({"protocol":1,"id":3,"session":1,"verb":"apply_controls","args":{AXES[0]:-.1,"reset":true}}).to_utf8_buffer())
 response=JSON.parse_string(bridge.outgoing.get_string_from_utf8());bridge.outgoing.clear()
 check(not response.ok and state()==unchanged,"bridge invalid transaction atomic")
 check(not bridge.enabled and not bridge.server.is_listening(),"no real socket test")
 bridge.free();rig.reset()
 var omitted=rig.neutral_pose()
 for axis in AXES:omitted.erase(axis)
 rig.apply_controls({AXES[0]:1.0,AXES[1]:1.0});rig._apply_performance_pose(omitted)
 for axis in AXES:check(rig.pose_now()[axis]==0 and rig.current_pose[axis]==0,"omitted internal timeline pose defaults zero")
 var pigment={}
 for k in rig.face.objects:pigment[k]=fingerprint(rig.face.objects[k])
 # All independent-side extrema with old tilt and vertical extrema and eye/hair corners.
 for tl in [-1.0,1.0]:
  for tr in [-1.0,1.0]:
   for ul in [-1.0,1.0]:
    for ur in [-1.0,1.0]:
     for lid in [0.0,.5,1.0]:
      for gx in [-1.0,1.0]:
       for gy in [-1.0,1.0]:
        for hair in [-.07,.07]:
         rig.apply_controls({"reset":true,"brow_tilt_screen_left":tl,"brow_tilt_screen_right":tr,"brow_screen_left":ul,"brow_screen_right":ur,"blink_R":lid,"blink_L":1-lid,"gaze_x":gx,"gaze_y":gy,"hair_sway":hair})
         var prior=other_geometry()
         for l in [0.0,.5,1.0]:
          for r in [0.0,.5,1.0]:
           check(rig.apply_controls({AXES[0]:l,AXES[1]:r}),"combined values accepted")
           verify_pose(l,r,tl,tr,ul,ur)
           check(other_geometry()==prior,"no other owner's transform/visibility/state changes")
           for k in ["brow_screen_left","brow_screen_right"]:check(fingerprint(rig.face.objects[k])==pigment[k],"fixed brow pigment UV alpha "+k)
 # Smooth fractional sweep, each independent direction and opposed asymmetric paths.
 for mode in [0,1,2]:
  rig.reset();rig.apply_controls({"brow_tilt_screen_left":-1.0,"brow_tilt_screen_right":1.0})
  var previous=Vector2(99,-99)
  for j in range(1001):
   var l=j/1000.0 if mode!=1 else 0.0;var r=j/1000.0 if mode!=0 else 0.0
   check(rig.apply_controls({AXES[0]:l,AXES[1]:r}),"fractional input")
   verify_pose(l,r,-1,1,0,0)
   var now=Vector2(rig.face.homes.brow_screen_left.node.rotation,rig.face.homes.brow_screen_right.node.rotation)
   check(now.x<=previous.x and now.y>=previous.y,"monotone independent rotation")
   if j>0:check((now-previous).length()<=deg_to_rad(rig.Limits.BROW_INNER_LIFT_DEGREES*sqrt(2.0)/1000.0+.00001),"bounded small fractional step")
   previous=now
 # Old definitions never implicitly acquire lift. Every old trajectory at30/60Hz.
 for e in rig.list_expressions():
  for hz in ([30,60] if e.id!="EXP-160" else []):
   rig.reset();rig.play_expression(e.id)
   for i in range(int(ceil(e.duration*hz))+1):
    var sample=rig.sample_expression(e.id,minf(float(i)/hz,e.duration))
    for axis in AXES:check(sample[axis]==0 and rig.pose_now()[axis]==0,"old timeline remains zero "+e.id)
    rig.advance(1.0/hz)
  for mode in ["manual","active","release"]:
   rig.reset();rig.apply_controls({AXES[0]:.71,AXES[1]:.39,"auto_blink":true})
   if mode!="manual":rig.play_expression(e.id);rig.advance(.1)
   if mode=="release":rig.release();rig.advance(.1)
   for axis in AXES:
    for invalid in [-.000001,1.000001,NAN,INF,-INF,true,false,"1",null,{},[]]:
     var before=state();var face=rig.face.snapshot()
     check(not rig.apply_controls({"reset":true,"mouth_open":.8,axis:invalid}),"invalid rejected "+axis)
     check(state()==before and rig.face.snapshot()==face,"invalid transaction atomic "+mode)
  for t in [0.0,.000001,.05,.299999,.3,e.duration*.5,e.duration-.001]:
   for action in ["manual","release","reset","retrigger","handover"]:
    rig.reset();rig.apply_controls({AXES[0]:.82,AXES[1]:.47,"auto_blink":true})
    var start=rig.displayed_pose();rig.play_expression(e.id);check(rig.displayed_pose()==start,"entry C0")
    rig.advance(t);var before=rig.displayed_pose()
    if action=="manual":
     rig.apply_controls({AXES[0]:.35});check(rig.active_performance=="" and rig.release_time<0 and not rig.auto_blink_pending_restore,"manual takeover cancels saved blink intent")
     rig.advance(.75);check(is_equal_approx(rig.pose_now()[AXES[0]],.35),"manual channel persists without stale resume");rig.reset()
    elif action=="release":
     rig.release();check(rig.displayed_pose()==before,"release C0");rig.advance(.12)
     before=rig.displayed_pose();rig.play_expression(e.id);check(rig.displayed_pose()==before,"release interruption C0");rig.advance(10)
    elif action=="reset":rig.reset()
    elif action=="retrigger":
     rig.play_expression(e.id);check(rig.displayed_pose()==before,"retrigger C0");rig.advance(.02)
     before=rig.displayed_pose();rig.play_expression(e.id);check(rig.displayed_pose()==before,"repeat retrigger C0");rig.advance(10)
    else:
     for d in rig.list_expressions():
      before=rig.displayed_pose();rig.play_expression(d.id);check(rig.displayed_pose()==before,"cross-expression C0");rig.advance(.04)
     rig.advance(10)
    check(rig.pose_now()==rig.neutral_pose(),"exact neutral recovery")
    check(rig.auto_blink==(action not in ["manual","reset"]),"auto-blink intent restoration")
 # Detached test-only schema fixture, never a playable expression.
 var fixture={"id":"TEST-BROW","title":"Test fixture","duration":1.0,"keyframes":[{"time":0.0,"phase":"neutral","values":{}},{"time":.5,"phase":"lift","values":{AXES[0]:1.0,AXES[1]:.5}},{"time":1.0,"phase":"neutral","values":{}}]}
 check(rig.registry.validate_definition(fixture,fixture.id),"bounded test timeline")
 check(rig._sample(fixture,.25)[AXES[0]]==.5 and rig._sample(fixture,.25)[AXES[1]]==.25,"shared smoothstep sampler")
 var catalog={"schema_version":1,"entries":[{"id":fixture.id,"path":"res://test-only-brow.json"}]};var isolated=rig.Registry.new()
 check(isolated.load_catalogue(catalog,{"res://test-only-brow.json":fixture}),"isolated valid load")
 var held=isolated.definition(fixture.id)
 for axis in AXES:
  for invalid in [-.001,1.001,NAN,INF,true,"1",null]:
   var bad=fixture.duplicate(true);bad.keyframes[1].values[axis]=invalid
   check(not isolated.load_catalogue(catalog,{"res://test-only-brow.json":bad}),"invalid timeline range")
   check(isolated.definition(fixture.id)==held,"failed registry reload atomic")
 rig.reset();rig.apply_controls({AXES[0]:.6,AXES[1]:.3})
 var before=state();check(not rig.apply_controls({AXES[0]:.1,"blink":true}),"invalid old field rejects extension transaction");check(state()==before,"old validation atomic")
 check(rig.apply_controls({"mouth_open":.4}) and is_equal_approx(rig.pose_now()[AXES[0]],.6) and is_equal_approx(rig.pose_now()[AXES[1]],.3),"omitted manual fields retain value")
 check(rig.apply_controls({"reset":true,AXES[0]:.2}) and is_equal_approx(rig.pose_now()[AXES[0]],.2) and rig.pose_now()[AXES[1]]==0,"reset then explicit values")
 check(rig.list_expressions().size()==10 and rig.registry.resolve("TEST-BROW")=="","fixture not registered")
 print("BROW_INNER_LIFT_CONTRACT checks=",checks," poses=",poses," failures=",failures.size())
 quit(0 if failures.is_empty() else 1)

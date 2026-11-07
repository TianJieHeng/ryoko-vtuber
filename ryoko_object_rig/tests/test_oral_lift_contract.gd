extends SceneTree
var rig
var checks=0
var failures=[]
const AXIS="mouth_oral_lift"
const IDS=["EXP-163","EXP-005","EXP-001","EXP-006","EXP-107","EXP-007"]
func _initialize():call_deferred("run")
func check(ok:bool,label:String):
 checks+=1
 if not ok:
  if failures.size()<20:push_error(label)
  failures.append(label)
func state():
 var s=rig.get_state();s.erase("last_error");return s
func nodes(n,result:Array):
 result.append(n)
 for c in n.get_children():nodes(c,result)
func signature(n):
 if n is Sprite2D:return [n.texture,n.scale,n.modulate,n.self_modulate,n.offset,n.flip_h,n.flip_v,n.region_enabled,n.region_rect]
 if n is Node2D:return [n.scale,n.modulate,n.self_modulate]
 return []
func geometry():
 var ns=[];nodes(rig.face,ns);var result={}
 for n in ns:
  if n is Node2D and n!=rig.face.spread_tongue:result[str(n.get_path())]=[n.transform,n.visible,signature(n)]
 return result
func close(a,b):return absf(a-b)<.000065
func run():
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 check(rig.rig_ready and rig.registry_ready,"rig ready")
 if not rig.rig_ready or not rig.registry_ready:quit(2);return
 var ids=[]
 for e in rig.list_expressions():ids.append(e.id)
 check(ids==IDS+["EXP-002","EXP-152","EXP-160","EXP-177","EXP-164"],"ten approved profiles plus scoped164")
 check(rig.pose_now()[AXIS]==0.0 and rig.neutral_pose()[AXIS]==0.0 and rig.face.mouth_oral_lift==0.0,"zero defaults")
 var bridge=load("res://control_bridge.gd").new();bridge.rig=rig
 var cap=bridge.capabilities()
 check(cap.controls[AXIS]==[0.0,1.0],"bridge range")
 check(cap.oral_surface.maximum_total_rise_source_px==40 and not cap.ai_model_connected and not cap.tts_connected,"bounded preparation-only bridge")
 bridge.free()
 check(rig.Registry.CHANNEL_BOUNDS[AXIS]==[0.0,1.0],"registry range")
 var tongue=rig.face.spread_tongue;var pigment=signature(tongue);var frame_count=0
 # Combined envelope corners and interiors, with focused near-zero and saturation values.
 for smile in [0.0,.75,1.0]:
  for spread in [0.0,.8,1.0]:
   for opening in [0.0,.000001,.6,1.0]:
    for corner in [0.0,.4,1.0]:
     for pressure in [0.0,1.0]:
      check(rig.apply_controls({"reset":true,"mouth_smile":smile,"mouth_spread":spread,"mouth_open":opening,"mouth_corner_lift":corner,"mouth_lip_press":pressure}),"combination accepted")
      var base=geometry();var home=tongue.position;var prior=home.y
      for lift in [0.0,.000001,.25,.5,.75,.999999,1.0]:
       check(rig.apply_controls({AXIS:lift}),"lift accepted")
       check(geometry()==base,"all other owners, textures, transforms and visibility unchanged")
       check(signature(tongue)==pigment and tongue.rotation==0 and tongue.scale==Vector2.ONE,"fixed oral pigment, unit scale and rotation")
       var effective=smile*spread;var expected=667.0-40.0*effective+2.75*opening-40.0*(1.0-effective)*lift
       check(close(tongue.position.x,510) and close(tongue.position.y,expected),"continuous bounded translation")
       check(tongue.position.y>=627.0+2.75*opening-.000065 and tongue.position.y<=home.y+.000065,"never expands existing vertical envelope")
       check(tongue.position.y<=prior+.000065,"monotonic lift")
       if effective==1.0:check(tongue.position==home,"full spread gains no extra range")
       if lift==0.0:check(tongue.position==home,"exact zero position")
       var offset=tongue.material.get_shader_parameter("rigid_offset")
       check((offset+Vector2(510,667)).is_equal_approx(tongue.position),"spatial clip follows rigid owner")
       check(rig.face.oral_objects.upper_teeth.position==Vector2(533,626),"fixed white arch")
       check(rig.pose_now()[AXIS]==lift and rig.displayed_pose()[AXIS]==lift and rig.face.mouth_oral_lift==lift,"state/display coordinate")
       prior=tongue.position.y;frame_count+=1
 # Exact default channel throughout every registered source trajectory at both rates.
 for e in rig.list_expressions():
  for hz in ([30,60] if e.id not in ["EXP-107","EXP-007","EXP-160"] else []):
   rig.reset();rig.play_expression(e.id)
   for i in range(int(ceil(e.duration*hz))+1):
    var t=minf(float(i)/hz,e.duration);var sample=rig.sample_expression(e.id,t)
    check(sample[AXIS]==0.0,"old data samples exact zero "+e.id)
    check(rig.pose_now()[AXIS]==0.0 and rig.face.mouth_oral_lift==0.0,"old playback exact zero "+e.id)
    rig.advance(1.0/hz)
  for mode in ["manual","active","release"]:
   rig.reset();rig.apply_controls({AXIS:.63,"mouth_open":.5,"mouth_smile":.75,"mouth_spread":.8})
   if mode!="manual":rig.play_expression(e.id);rig.advance(.1)
   if mode=="release":rig.release();rig.advance(.1)
   for invalid in [-.000001,1.000001,NAN,INF,-INF,true,false,"1",null,{},[]]:
    var before=state();var geo=geometry();var pos=tongue.position
    check(not rig.apply_controls({"reset":true,"mouth_open":.7,"mouth_smile":.9,AXIS:invalid}),"invalid atomically rejected")
    check(state()==before and geometry()==geo and tongue.position==pos,"invalid retains full pose clock ownership "+e.id+mode)
  for t in [0.0,.000001,.05,.299999,.3,e.duration*.45,e.duration-.001]:
   for action in ["manual","release","reset","retrigger","handover"]:
    rig.reset();rig.apply_controls({AXIS:.82,"mouth_open":.6,"mouth_smile":.75,"mouth_spread":.8,"mouth_lip_press":1.0})
    var start=rig.displayed_pose();check(rig.play_expression(e.id),"play");check(rig.displayed_pose()==start,"incoming C0")
    rig.advance(t);var before=rig.displayed_pose()
    if action=="manual":
     rig.apply_controls({AXIS:.35});check(rig.active_performance=="" and rig.release_time<0 and rig.face.owners.mouth=="manual","manual ownership")
     rig.advance(.75);check(rig.pose_now()[AXIS]==.35,"no stale resume")
     rig.reset()
    elif action=="release":
     rig.release();check(rig.displayed_pose()==before,"release C0");rig.advance(.12)
     var mid=rig.displayed_pose();rig.play_expression(e.id);check(rig.displayed_pose()==mid,"interrupted release C0");rig.advance(10)
    elif action=="reset":rig.reset()
    elif action=="retrigger":
     rig.play_expression(e.id);check(rig.displayed_pose()==before,"retrigger C0");rig.advance(.02)
     before=rig.displayed_pose();rig.play_expression(e.id);check(rig.displayed_pose()==before,"repeated retrigger C0");rig.advance(10)
    else:
     for destination in rig.list_expressions():
      var a=rig.displayed_pose();rig.play_expression(destination.id);check(rig.displayed_pose()==a,"cross-expression handover C0")
      rig.advance(.04);a=rig.displayed_pose();rig.play_expression(e.id);check(rig.displayed_pose()==a,"interrupted handover C0");rig.advance(.03)
     rig.advance(10)
    check(rig.displayed_pose()==rig.neutral_pose() and rig.face.mouth_oral_lift==0.0,"exact neutral completion")
 # Test-only in-memory definition; it is never added to the shipping registry.
 var fixture={"id":"TEST-ORAL-LIFT","title":"Test fixture","duration":1.0,"keyframes":[{"time":0.0,"phase":"neutral","values":{}},{"time":.5,"phase":"lift","values":{AXIS:1.0}},{"time":1.0,"phase":"neutral","values":{}}]}
 check(rig.registry.validate_definition(fixture,fixture.id),"timeline accepts bounded lift")
 check(rig._sample(fixture,.25)[AXIS]==.5 and rig._sample(fixture,.5)[AXIS]==1.0,"shared interpolation")
 for v in [-.1,1.1,true,"1",NAN]:
  fixture.keyframes[1].values[AXIS]=v
  check(not rig.registry.validate_definition(fixture,fixture.id),"timeline rejects invalid lift")
 var isolated_registry=rig.Registry.new()
 var catalog={"schema_version":1,"entries":[{"id":fixture.id,"path":"res://test-only-oral-lift.json"}]}
 fixture.keyframes[1].values[AXIS]=.8
 check(isolated_registry.load_catalogue(catalog,{"res://test-only-oral-lift.json":fixture}),"isolated valid timeline loads")
 var held=isolated_registry.definition(fixture.id)
 for invalid in [-.000001,1.000001,NAN,INF,true,"1",null]:
  var bad=fixture.duplicate(true);bad.keyframes[1].values[AXIS]=invalid
  check(not isolated_registry.load_catalogue(catalog,{"res://test-only-oral-lift.json":bad}),"invalid registry channel rejected")
  check(isolated_registry.definition(fixture.id)==held,"registry load failure is atomic")
 var before=state()
 check(not rig.apply_controls({AXIS:.7,"blink":true}),"valid oral lift plus invalid old field rejected")
 check(state()==before,"old-field failure preserves oral lift atomically")
 check(not rig.apply_controls({"tongue_lift":.5}),"unguessed alias rejected")
 check(rig.list_expressions().size()==11 and rig.registry.resolve("TEST-ORAL-LIFT")=="","fixture never published")
 print("ORAL_LIFT_CONTRACT checks=",checks," poses=",frame_count," failures=",failures.size())
 quit(1 if failures.size() else 0)

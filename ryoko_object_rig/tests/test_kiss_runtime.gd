extends SceneTree
var rig
var failures=[]
var checks=0
var results_path="user://kiss_runtime_checks.json"
func _initialize():call_deferred("run")
func check(ok,label):
 checks+=1
 if not ok:failures.append(label);push_error(label)
func opacity():
 var result={}
 for k in rig.face.objects:result[k]=rig.face.objects[k].self_modulate
 return result
func run():
 for arg in OS.get_cmdline_user_args():
  if arg.begins_with("--results="):results_path=arg.trim_prefix("--results=")
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 check(rig.rig_ready and rig.registry_ready,"ready")
 if not rig.rig_ready or not rig.registry_ready:quit(2);return
 rig.reset();var neutral=rig.face.snapshot();var alpha=opacity();var head=rig.head.transform;var body=rig.body.transform
 var source={}
 for k in rig.face.objects:
  var n=rig.face.objects[k];source[k]=[n.texture,n.scale,n.region_rect,n.region_enabled]
 check(rig.list_expressions().size()==21,"twenty prior profiles plus unapproved EXP-197")
 for weight in [0.0,.25,.5,.75,1.0]:
  check(rig.apply_controls({"mouth_kiss":weight}),"weight accepted")
  check(rig.face.mouth_kiss==weight and rig.face.spread_tongue.visible,"kiss never takes native visibility ownership")
  for key in rig.face.kiss_native_owners:check(absf(rig.face.objects[key].self_modulate.a-rig.face.kiss_native_opacity[key].a*(1.0-weight))<.000001,"native opacity follows blend")
  for key in rig.face.kiss_native_owners:
   var mat=rig.face.objects[key].material
   if mat is ShaderMaterial:check(absf(mat.get_shader_parameter("native_part_weight")-(1.0-weight))<.000001,"native shader follows blend")
 rig.reset();check(rig.face.snapshot()==neutral and opacity()==alpha,"direct reset exact")
 rig.apply_controls({"mouth_kiss":.8});var held=rig.get_state();var held_face=rig.face.snapshot()
 for bad in [-.1,1.1,NAN,INF,true,"1",null]:
  check(not rig.apply_controls({"mouth_kiss":bad}),"invalid weight rejected")
  check(rig.face.snapshot()==held_face,"invalid weight atomic")
 check(not rig.apply_controls({"mouth_open":.3}),"retained kiss rejects opening")
 rig.reset();rig.apply_controls({"mouth_open":.3})
 check(not rig.apply_controls({"mouth_kiss":.7}),"retained opening rejects kiss")
 check(rig.apply_controls({"mouth_open":0.0,"mouth_kiss":.7}),"atomic domain handover accepted")
 rig.reset();check(rig.play_expression("EXP-197"),"play")
 for i in range(217):
  if i>0:rig.advance(1.0/30.0)
  var p=rig.pose_now()
  check(rig.Registry.sealed_mouth_valid(p),"valid sampled mouth domain")
  check(rig.head.transform==head and rig.body.transform==body,"fixed head/body")
  for k in source:
   var n=rig.face.objects[k];check([n.texture,n.scale,n.region_rect,n.region_enabled]==source[k],"fixed source texture/scale/region")
 rig.advance(.01)
 check(rig.pose_now()==rig.neutral_pose() and rig.face.snapshot()==neutral and opacity()==alpha,"full cycle restores exact state")
 for t in [1.9,3.2,4.5]:
  rig.reset();rig.play_expression("EXP-197");rig.advance(t);var p=rig.displayed_pose()
  check(rig.play_expression("EXP-197") and rig.displayed_pose()==p,"retrigger C0")
  rig.advance(.1);p=rig.displayed_pose();check(rig.release() and rig.displayed_pose()==p,"release C0")
  rig.advance(.45);check(rig.face.snapshot()==neutral and opacity()==alpha,"release exact reset")
 # Legacy behavior samples and both directions of open/kiss handover.
 for entry in rig.list_expressions():
  if entry.id=="EXP-197":continue
  rig.reset();rig.play_expression(entry.id);rig.advance(entry.duration*.5)
  check(rig.pose_now().mouth_kiss==0 and opacity()==alpha,"legacy profile leaves mouth part absent")
  check(rig.play_expression("EXP-197"),"legacy-to-kiss handover")
  for i in range(12):rig.advance(.03);check(rig.Registry.sealed_mouth_valid(rig.pose_now()),"handover remains in valid domain")
  rig.advance(2.8);check(rig.play_expression(entry.id),"kiss-to-legacy handover")
  for i in range(12):rig.advance(.03);check(rig.Registry.sealed_mouth_valid(rig.pose_now()),"return handover remains in valid domain")
 rig.reset();check(rig.face.snapshot()==neutral and opacity()==alpha,"final reset exact")
 var f=FileAccess.open(results_path,FileAccess.WRITE)
 f.store_string(JSON.stringify({"checks":checks,"failures":failures,"status":"PASS" if failures.is_empty() else "FAIL","neutral_state_exact":rig.face.snapshot()==neutral,"native_opacity_exact":opacity()==alpha},"  "));f.close()
 print("KISS_RUNTIME checks=",checks," failures=",failures.size());quit(0 if failures.is_empty() else 1)

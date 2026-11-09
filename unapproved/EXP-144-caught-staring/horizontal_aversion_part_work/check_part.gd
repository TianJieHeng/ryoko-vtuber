extends SceneTree
var checks=0
var failures=[]
func check(ok,label):
 checks+=1
 if not ok:failures.append(label)
func _initialize():call_deferred("run")
func shaders(face):
 var a=[]
 for side in ["screen_left","screen_right"]:
  for prefix in ["iris_","sclera_"]:a.append(face.objects[prefix+side].material.get_shader_parameter("rigid_gaze"))
 return a
func run():
 var rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false);rig.auto_blink=false;rig.reset()
 var part=load("/workspace/scratch/42f2baf55663/horizontal_aversion_part_work/horizontal_aversion_part.gd").new()
 var baseline=rig.face.snapshot();var zero=shaders(rig.face)
 check(not part.apply(rig.face,12),"rejects open lids")
 var p=rig.neutral_pose();p.blink_L=.18;p.blink_R=.18;rig._apply_performance_pose(p)
 var closed=rig.face.snapshot()
 check(part.apply(rig.face,12),"accepts bounded twelve")
 var moved=rig.face.snapshot();var moved_shader=shaders(rig.face)
 for bad in [-1.0,12.01,INF,NAN]:
  check(not part.apply(rig.face,bad),"rejects invalid")
  check(rig.face.snapshot()==moved and shaders(rig.face)==moved_shader,"invalid is atomic")
 for x in [0.0,3.25,7.5,12.0,0.0]:
  check(part.apply(rig.face,x),"accepts in-range")
  for side in ["screen_left","screen_right"]:
   var h=rig.face.homes["iris_"+side]
   check(h.node.position==h.pivot+Vector2(x,0),"rigid pivot exact")
 check(rig.face.snapshot()==closed,"zero restores closed pose")
 rig.reset();part.restore(rig.face)
 check(rig.face.snapshot()==baseline and shaders(rig.face)==zero,"neutral reset exact")
 p=rig.neutral_pose();p.blink_L=.18;p.blink_R=.18;p.gaze_x=.5;rig._apply_performance_pose(p)
 var ordinary=rig.face.snapshot();var ordinary_shader=shaders(rig.face)
 check(not part.apply(rig.face,12),"rejects gaze composition")
 check(rig.face.snapshot()==ordinary and shaders(rig.face)==ordinary_shader,"gaze rejection atomic")
 part.restore(rig.face)
 check(rig.face.snapshot()==ordinary and shaders(rig.face)==ordinary_shader,"restores ordinary gaze")
 rig.reset();var f=FileAccess.open("/workspace/scratch/42f2baf55663/horizontal_aversion_part_work/part_checks.json",FileAccess.WRITE)
 f.store_string(JSON.stringify({"checks":checks,"failures":failures,"status":"PASS" if failures.is_empty() else "FAIL"},"  "));f.close();quit(0 if failures.is_empty() else 2)

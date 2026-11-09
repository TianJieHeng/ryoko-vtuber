extends SceneTree
func _initialize():call_deferred("run")
func run():
 var rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false);rig.auto_blink=false;rig.reset()
 var c=load("/workspace/scratch/42f2baf55663/caught_staring_performance_work/review_controller.gd").new();c.setup(rig);var baseline=rig.face.snapshot();var bad=[]
 for t in [0,.65,1.0,1.25,1.45,1.65,1.95,2.3,2.8,3.2,3.55,3.85,4.5,4.9,5.2]:
  if not c.apply(t):bad.append(t)
  c.reset()
  if rig.face.snapshot()!=baseline:bad.append("reset "+str(t))
  await process_frame
 var f=FileAccess.open("/workspace/scratch/42f2baf55663/caught_staring_performance_work/review_checks.json",FileAccess.WRITE);f.store_string(JSON.stringify({"keyframes_checked":15,"failures":bad,"status":"PASS" if bad.is_empty() else "FAIL"}));f.close();quit(0 if bad.is_empty() else 2)

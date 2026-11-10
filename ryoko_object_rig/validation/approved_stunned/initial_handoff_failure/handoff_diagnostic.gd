extends SceneTree
func _initialize():call_deferred("run")
func run():
 var rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false);rig.auto_blink=false
 var records=[]
 for pair in [["EXP-063","EXP-186"],["EXP-186","EXP-063"]]:
  rig.reset();rig.play_expression(pair[0]);rig.advance(rig.performance.duration*.5)
  var source=rig.displayed_pose();rig.play_expression(pair[1])
  for i in range(11):
   rig.advance(.03)
   var pose=rig.pose_now()
   records.append({"pair":pair,"step":i+1,"time":rig.performance_time,"source":source,"pose":pose,"target":rig.sample_expression(pair[1],rig.performance_time),"mouth_bridge":rig.mouth_transition_state(),"scoped_valid":rig.Registry.scoped_valid(pose),"sealed_mouth_valid":rig.Registry.sealed_mouth_valid(pose)})
 var f=FileAccess.open("/tmp/stunned_handoff_diagnostic.json",FileAccess.WRITE);f.store_string(JSON.stringify({"records":records},"  "));f.close()
 for row in records:
  if not row.sealed_mouth_valid:print(JSON.stringify(row))
 quit()

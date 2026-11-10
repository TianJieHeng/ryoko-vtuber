extends SceneTree
func _initialize():call_deferred("run")
func run():
 var rig=load("res://expression_rig.tscn").instantiate()
 rig.set_script(load("res://historical_capture_metadata/approved27_before_batch36/expression_rig.gd"))
 root.add_child(rig);rig.set_process(false)
 print("PRIOR27_SCENE_READY ",rig.rig_ready)
 rig.play_expression("EXP-144")
 print("PRIOR27_BEFORE_OPENING")
 rig.advance(1.05)
 print("PRIOR27_AFTER_OPENING")
 quit()

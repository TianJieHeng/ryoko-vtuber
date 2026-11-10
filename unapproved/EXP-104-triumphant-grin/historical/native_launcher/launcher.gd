extends Node
func _ready():
 var w="/workspace/scratch/42f2baf55663/triumphant_grin_work"
 if DirAccess.dir_exists_absolute(w+"/capture") or DirAccess.dir_exists_absolute(w+"/motion"):
  push_error("Existing capture must be preserved; refusing overwrite")
  return
 var static_probe=load("res://static.gd").new()
 add_child(static_probe)
 await static_probe.tree_exited
 var receipt=JSON.parse_string(FileAccess.get_file_as_string(w+"/capture/checks.json"))
 if receipt==null or receipt.get("status")!="PASS":
  push_error("Static capture failed; motion not started")
  return
 await get_tree().process_frame
 var motion_probe=load("res://motion.gd").new()
 add_child(motion_probe)
 await motion_probe.tree_exited
 print("Native capture finished. Inspect receipts before encoding or approval.")

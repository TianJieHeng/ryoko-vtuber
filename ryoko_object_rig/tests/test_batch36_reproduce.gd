extends SceneTree
class Current:
 extends "res://expression_rig.gd"
 func _ready():registry_ready=registry.load_file();rig_ready=true;current_pose=neutral_pose()
 func _apply_performance_pose(p:Dictionary):current_pose=p.duplicate(true)
 func pose_now()->Dictionary:return current_pose.duplicate(true)
 func displayed_pose()->Dictionary:return pose_now()
 func _write_pose():pass
 func _suspend_auto_blink():pass
 func _restore_auto_blink():pass
func _initialize():call_deferred("run")
func run():
 var rig=Current.new();root.add_child(rig);var records=[]
 for source_id in ["EXP-163","EXP-197","EXP-064","EXP-004"]:
  for target in ["EXP-064","EXP-004"]:
   var source=rig.sample_expression(source_id,.615 if source_id=="EXP-163" else 1.05)
   rig.current_pose=source.duplicate(true);rig.active_performance="";rig.release_time=-1;rig.performance_time=0;rig._clear_mouth_bridge();rig.play_expression(target);rig.advance(.24)
   var p=rig.pose_now()
   if not rig.Registry.scoped_valid(p):records.append({"source_id":source_id,"source":source,"target_id":target,"time":.24,"result":p})
 var out={"invalid_examples":records,"count":records.size()};var f=FileAccess.open("res://validation/approved_batch36/initial_failure/minimal_reproduction.json",FileAccess.WRITE);f.store_string(JSON.stringify(out,"  "));f.close();print(JSON.stringify(out));quit()

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
var checks=0
var failures=[]
var cases=0
func _initialize():call_deferred("run")
func check(ok,label):
 checks+=1
 if not ok and failures.size()<30:failures.append(label)
func seed_pose(rig,p):
 rig.current_pose=p.duplicate(true);rig.active_performance="";rig.release_time=-1;rig.performance_time=0;rig._clear_mouth_bridge()
func valid(rig,label):
 check(rig.Registry.scoped_valid(rig.pose_now()),label+" scope")
 check(rig.Registry.sealed_mouth_valid(rig.pose_now()),label+" mouth")
func run():
 var rig=Current.new();root.add_child(rig)
 for entry in rig.list_expressions():
  var d=rig.registry.definition(entry.id)
  for key in d.keyframes:
   for target in ["EXP-064","EXP-004"]:
    for t in [.0,.05,.099999999,.1,.100000001,.15,.199999999,.2,.200000001,.25,.299999999,.3,.300000001]:
     for action in ["release","restart"]:
      seed_pose(rig,rig.sample_expression(entry.id,key.time));rig.play_expression(target);rig.advance(t);valid(rig,"before "+action)
      var before=rig.pose_now()
      if action=="release":check(rig.release(),"release success");check(not rig.opening_bridge_active,"release clears bridge")
      else:check(rig.play_expression(target),"restart success")
      check(before==rig.pose_now(),action+" C0")
      var last=0.0
      for delta in [.0,.05,.1,.15,.2,.25,.3,.45,.4500001]:
       rig.advance(delta-last);last=delta;valid(rig,action+" sample")
      rig.advance(10);valid(rig,"completion");check(rig.pose_now()==rig.neutral_pose(),"exact complete neutral");check(not rig.opening_bridge_active,"completion clears bridge")
      cases+=1
 var out={"status":"PASS" if failures.is_empty() else "FAIL","checks":checks,"cases":cases,"failures":failures,"scope":"Production control code with face setters stubbed. All36 source keys into two early-opening targets; restart/release at both sides of all three stage boundaries, C0, scoped/mouth domains and lifecycle flag clearing."}
 var f=FileAccess.open("res://validation/approved_batch36/bridge_lifecycle_checks.json",FileAccess.WRITE);f.store_string(JSON.stringify(out,"  "));f.close();print(JSON.stringify(out));quit(0 if failures.is_empty() else 1)

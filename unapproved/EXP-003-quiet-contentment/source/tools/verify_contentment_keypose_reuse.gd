extends SceneTree
var rig
func _initialize():call_deferred("run")
func run():
 var input="";var output=""
 for arg in OS.get_cmdline_user_args():
  if arg.begins_with("--input="):input=arg.trim_prefix("--input=")
  if arg.begins_with("--output="):output=arg.trim_prefix("--output=")
 var records=JSON.parse_string(FileAccess.get_file_as_string(input));var checks=0;var failures=[]
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 if not rig.rig_ready or not rig.registry_ready:quit(2);return
 rig.head.position=Vector2.ZERO;rig.body.position=Vector2.ZERO;rig.head.scale=Vector2.ONE;rig.body.scale=Vector2.ONE
 for i in range(records.size()):
  var row=records[i];var expected=row.state;var t=rig.registry.definition("EXP-003").keyframes[i].time
  rig.reset();rig.play_expression("EXP-003");rig.advance(t);rig._write_pose()
  # Normalize through the same JSON encoder as the original saved evidence.
  var actual=JSON.parse_string(JSON.stringify(rig.face.snapshot()))
  checks+=1
  if actual!=expected.face:failures.append(row.destination+" face")
  checks+=1
  if JSON.parse_string(JSON.stringify(rig.pose_now()))!=expected.state.controls:failures.append(row.destination+" controls")
 var f=FileAccess.open(output,FileAccess.WRITE);f.store_string(JSON.stringify({"checks":checks,"failures":failures,"status":"PASS" if failures.is_empty() else "FAIL","purpose":"Prove the reused actual key-pose PNGs have exact current control and facial owner state equivalence. This does not claim new renders or normal-speed playback."},"  "));f.close()
 print("CONTENTMENT_KEYPOSE_REUSE_", "PASS" if failures.is_empty() else "FAIL", " ",failures);quit(0 if failures.is_empty() else 1)

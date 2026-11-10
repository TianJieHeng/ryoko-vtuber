extends SceneTree
var w = get_script().resource_path.get_base_dir()
var checks = 0
var failures = []
var frame_count = 0
var channel_count = 0
var max_error = 0.0
func _initialize(): call_deferred("run")
func check(ok, label):
 checks += 1
 if not ok: failures.append(label)
func run():
 var rig = load("res://expression_rig.tscn").instantiate()
 root.add_child(rig)
 rig.set_process(false)
 rig.auto_blink = false
 check(rig.rig_ready and rig.registry_ready, "ready")
 check(rig.list_expressions().size() == 36, "registry36")
 var inputs = JSON.parse_string(FileAccess.get_file_as_string(w + "/expected_states.json"))
 for item in inputs:
  rig.reset()
  check(rig.play_expression(item.id), "play " + item.id)
  for rec in item.records:
   if rec.frame > 0:
    check(rig.advance(maxf(0.0, float(rec.frame) / float(item.fps) - rig.performance_time)), "advance " + item.id)
   var pose = rig.pose_now()
   frame_count += 1
   check(pose.size() == rec.pose.size(), "channel count " + item.id)
   for key in rec.pose:
    channel_count += 1
    var error = absf(float(pose[key]) - float(rec.pose[key]))
    max_error = maxf(max_error, error)
    check(error < 0.000000001, "%s frame %d channel %s" % [item.id, int(rec.frame), key])
 var result = {"status":"PASS" if failures.is_empty() else "FAIL","checks":checks,"failures":failures,"frames":frame_count,"channel_comparisons":channel_count,"maximum_absolute_error":max_error,"tolerance":0.000000001,"scope":"Headless production numeric pose matching against every 30fps original native-record pose. Not fresh native pixel rendering or live pacing.","display":DisplayServer.get_name()}
 var f = FileAccess.open(w + "/numeric_source_parity.json", FileAccess.WRITE)
 f.store_string(JSON.stringify(result, "  "))
 f.close()
 print(JSON.stringify(result))
 quit(0 if failures.is_empty() else 1)

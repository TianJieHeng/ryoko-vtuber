extends Node
var root

var rig
var w = "/workspace/scratch/42f2baf55663/approved36_native_parity_work"
var failures = []
var checks = 0
var records = []
var comparisons = 0
var matches = 0
func _ready():
 root = get_tree().root
 call_deferred("run")
func check(ok, label):
 checks += 1
 if not ok: failures.append(label)
func snap(path, detail):
 root.size = Vector2i(568, 800)
 root.canvas_transform = Transform2D.IDENTITY
 if detail:
  root.size = Vector2i(400, 360)
  var camera = Transform2D.IDENTITY.scaled(Vector2.ONE / .49)
  camera.origin = -Vector2(6, 70) / .49 - Vector2(380, 380)
  root.canvas_transform = camera
 await get_tree().process_frame
 await get_tree().process_frame
 await RenderingServer.frame_post_draw
 var im = root.get_texture().get_image()
 var wanted = Vector2i(400,360) if detail else Vector2i(568,800)
 check(im.get_size() == wanted, "exact viewport dimensions " + path)
 if im.get_size() != wanted:
  var f = FileAccess.open(w + "/SIZE_FAILURE.json", FileAccess.WRITE)
  f.store_string(JSON.stringify({"actual":[im.get_width(),im.get_height()],"expected":[wanted.x,wanted.y],"path":path}))
  f.close()
  get_tree().quit(2)
  return "INVALID_SIZE"
 check(im.save_png(path) == OK, "save " + path)
 var ctx = HashingContext.new()
 ctx.start(HashingContext.HASH_SHA256)
 ctx.update(im.get_data())
 return ctx.finish().hex_encode()
func run():
 if DisplayServer.get_name() == "headless":
  push_error("Native X11/OpenGL display required; headless dummy rendering cannot prove pixel parity.")
  get_tree().quit(2)
  return
 rig = load("res://expression_rig.tscn").instantiate()
 root.add_child(rig)
 rig.set_process(false)
 rig.auto_blink = false
 check(rig.rig_ready and rig.registry_ready, "ready")
 check(rig.list_expressions().size() == 36, "production registry36")
 if not failures.is_empty():
  get_tree().quit(1)
  return
 rig.hud.hide()
 rig.hint.hide()
 rig.pose_status.hide()
 rig.reset()
 var baseline = rig.face.snapshot()
 var inputs = JSON.parse_string(FileAccess.get_file_as_string(w + "/expected_checkpoints.json"))
 for item in inputs:
  DirAccess.make_dir_recursive_absolute(w + "/captures/" + item.id)
  for checkpoint in item.checkpoints:
   rig.reset()
   check(rig.play_expression(item.id), "registered play " + item.id)
   check(rig.advance(float(checkpoint.frame) / float(item.fps)), "registered advance " + item.id)
   var path = w + "/captures/" + item.id + "/%04d" % int(checkpoint.frame)
   var hashes = [await snap(path + "_full.png", false), await snap(path + "_detail.png", true)]
   for view in range(2):
    comparisons += 1
    var same = hashes[view] == checkpoint.hashes[view]
    if same: matches += 1
    check(same, "exact approved pixels %s frame %d view %d" % [item.id, int(checkpoint.frame), view])
   records.append({"id":item.id,"frame":checkpoint.frame,"hashes":hashes,"expected_hashes":checkpoint.hashes})
  rig.reset()
  check(rig.face.snapshot() == baseline, "neutral reset " + item.id)
 var result = {"status":"PASS" if failures.is_empty() else "FAIL","checks":checks,"failures":failures,"profiles":inputs.size(),"captured_checkpoints":records.size(),"image_comparisons_run":comparisons,"pixel_matches":matches,"normal_speed_observed":false,"scope":"Ten production checkpoints per newly approved profile, full/detail exact approved RGBA parity. Not prior27 native parity or live pacing.","renderer":RenderingServer.get_video_adapter_name(),"display":DisplayServer.get_name(),"records":records}
 var f = FileAccess.open(w + "/RESULT.json", FileAccess.WRITE)
 f.store_string(JSON.stringify(result, "  "))
 f.close()
 print(JSON.stringify(result))
 get_tree().quit(0 if failures.is_empty() else 1)

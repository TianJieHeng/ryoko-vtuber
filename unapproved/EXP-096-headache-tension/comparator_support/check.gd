extends SceneTree
var rig
var w=get_script().resource_path.get_base_dir()
var failures=[]
var checks=0
var records=[]
var visual=false
func _initialize():
 visual="--capture" in OS.get_cmdline_user_args()
 call_deferred("run")
func check(ok,label):
 checks+=1
 if not ok:failures.append(label)
func snap(path,detail):
 root.size=Vector2i(568,800);root.canvas_transform=Transform2D.IDENTITY
 if detail:
  root.size=Vector2i(400,360)
  var camera=Transform2D.IDENTITY.scaled(Vector2.ONE/.49);camera.origin=-Vector2(6,70)/.49-Vector2(380,380);root.canvas_transform=camera
 await process_frame;await process_frame;await RenderingServer.frame_post_draw
 var im=root.get_texture().get_image()
 check(im.save_png(path)==OK,"saved "+path)
 var ctx=HashingContext.new();ctx.start(HashingContext.HASH_SHA256);ctx.update(im.get_data());return ctx.finish().hex_encode()
func run():
 var patched="--patched" in OS.get_cmdline_user_args()
 var mode="patched" if patched else "baseline"
 DirAccess.make_dir_recursive_absolute(w+"/"+mode)
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false);rig.auto_blink=false
 check(rig.rig_ready and rig.registry_ready,"ready")
 check(rig.list_expressions().size()==(25 if patched else 24),"registry count")
 rig.hud.hide();rig.hint.hide();rig.pose_status.hide();rig.reset()
 var samples=JSON.parse_string(FileAccess.get_file_as_string(w+"/samples.json"))
 var old={}
 if patched:old=JSON.parse_string(FileAccess.get_file_as_string(w+"/baseline.json"))
 for sample in samples:
  rig.reset();check(rig.play_expression(sample.id),"play "+sample.id);check(rig.advance(sample.time),"advance "+sample.id)
  var hashes=[]
  hashes.append(await snap(w+"/"+mode+"/"+sample.id+"_full.png",false));hashes.append(await snap(w+"/"+mode+"/"+sample.id+"_detail.png",true))
  if patched:check(hashes==old.records[records.size()].hashes,"exact prior approved pixels "+sample.id)
  records.append({"id":sample.id,"time":sample.time,"hashes":hashes})
 rig.reset()
 var result={"status":"PASS" if failures.is_empty() else "FAIL","checks":checks,"failures":failures,"scope":"All prior24 profiles one maximum-control key each, full and detail native RGBA. Not all-frame or interactive parity.","records":records}
 var f=FileAccess.open(w+"/"+mode+".json",FileAccess.WRITE);f.store_string(JSON.stringify(result,"  "));f.close();print(JSON.stringify(result));quit(0 if failures.is_empty() else 1)

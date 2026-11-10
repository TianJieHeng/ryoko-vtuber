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
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false);rig.auto_blink=false
 check(rig.rig_ready and rig.registry_ready,"ready");check(rig.list_expressions().size()==27,"production registry27")
 if not failures.is_empty():quit(1);return
 rig.hud.hide();rig.hint.hide();rig.pose_status.hide();rig.reset()
 var baseline=rig.face.snapshot()
 var old=JSON.parse_string(FileAccess.get_file_as_string(w+"/../motion_checks.json"))
 for idx in [0,7,16,28,42,61,81,103,113,120]:
  rig.reset();check(rig.play_expression("EXP-153"),"registered play");check(rig.advance(float(idx)/30.0),"registered advance")
  var hashes=[]
  hashes.append(await snap(w+"/%04d_full.png"%idx,false));hashes.append(await snap(w+"/%04d_detail.png"%idx,true))
  check(hashes==old.records[idx].hashes,"exact approved pixels "+str(idx));records.append({"frame":idx,"hashes":hashes})
 rig.reset();check(rig.face.snapshot()==baseline,"neutral reset")
 var result={"status":"PASS" if failures.is_empty() else "FAIL","checks":checks,"failures":failures,"scope":"Ten production EXP-153 checkpoints, both views, exact approved review RGBA parity. Not prior26 native parity or live pacing.","renderer":RenderingServer.get_video_adapter_name(),"display":DisplayServer.get_name(),"records":records}
 var f=FileAccess.open(w+"/RESULT.json",FileAccess.WRITE);f.store_string(JSON.stringify(result,"  "));f.close();print(JSON.stringify(result));quit(0 if failures.is_empty() else 1)

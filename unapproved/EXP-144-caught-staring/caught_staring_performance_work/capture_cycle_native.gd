extends SceneTree
var rig
var control
var output=""
var port=0
var view_mode="full"
var peer=StreamPeerTCP.new()
var failures=[]
var records=[]
func _initialize():call_deferred("run")
func check(ok,label):
 if not ok:failures.append(label);push_error(label)
func digest(im):
 var h=HashingContext.new();h.start(HashingContext.HASH_SHA256);h.update(im.get_data());return h.finish().hex_encode()
func run():
 for a in OS.get_cmdline_user_args():
  if a.begins_with("--output="):output=a.trim_prefix("--output=")
  if a.begins_with("--port="):port=int(a.trim_prefix("--port="))
  if a.begins_with("--view="):view_mode=a.trim_prefix("--view=")
 if output.is_empty() or port<=0:quit(2);return
 root.size=Vector2i(568,800);root.canvas_transform=Transform2D.IDENTITY
 if view_mode=="detail":
  root.size=Vector2i(400,360)
  var camera=Transform2D.IDENTITY.scaled(Vector2.ONE/.49);camera.origin=-Vector2(6,70)/.49-Vector2(380,380);root.canvas_transform=camera
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false);rig.auto_blink=false
 check(rig.rig_ready and rig.registry_ready,"ready")
 if not failures.is_empty():quit(2);return
 rig.hud.hide();rig.hint.hide();rig.pose_status.hide();rig.reset()
 var baseline=rig.face.snapshot();var head=rig.head.transform;var body=rig.body.transform
 control=load("/workspace/scratch/42f2baf55663/caught_staring_performance_work/review_controller.gd").new();control.setup(rig)
 peer.big_endian=true;check(peer.connect_to_host("127.0.0.1",port)==OK,"connect encoder")
 var start=Time.get_ticks_msec()
 while peer.get_status()!=StreamPeerTCP.STATUS_CONNECTED and Time.get_ticks_msec()-start<5000:peer.poll();await process_frame
 check(peer.get_status()==StreamPeerTCP.STATUS_CONNECTED,"encoder connected")
 if not failures.is_empty():quit(2);return
 var neutral_hash=""
 for index in range(157):
  var t=float(index)/30.0;check(control.apply(t),"bounded composition "+str(index))
  check(rig.head.transform==head and rig.body.transform==body,"fixed head/body")
  check(not rig.face.kiss_sprite.visible and rig.face.mouth_kiss==0,"kiss part never used")
  check(rig.face.spread_tongue.visible,"native oral visibility preserved")
  await process_frame;await RenderingServer.frame_post_draw
  var im=root.get_texture().get_image();var hash=digest(im)
  if index==0:neutral_hash=hash
  if index==156:check(hash==neutral_hash and rig.face.snapshot()==baseline,"exact neutral return")
  var bytes=im.save_png_to_buffer();peer.put_u32(bytes.size());check(peer.put_data(bytes)==OK,"stream frame")
  records.append({"frame":index,"time":t,"pixel_sha256":hash,"values":control.sample(t)})
  if not failures.is_empty():break
 peer.disconnect_from_host()
 for t in [1.1,2.4,3.9]:
  check(control.apply(t),"interrupt entry");control.reset();check(rig.face.snapshot()==baseline,"interrupted exact reset")
  check(control.apply(t),"retrigger entry");check(control.apply(0),"restart at neutral");check(rig.face.snapshot()==baseline,"restart exact reset")
 var f=FileAccess.open(output+"/capture_result.json",FileAccess.WRITE)
 f.store_string(JSON.stringify({"status":"PASS" if failures.is_empty() else "FAIL","failures":failures,"frames":records,"neutral_return":true,"live_pacing_measured":false,"player":"separate local review controller on shared rig; not installed in approved registry"},"  "));f.close()
 print("EXP144_COMPLETE_REVIEW_CYCLE ","PASS" if failures.is_empty() else "FAIL"," frames=",records.size()," ",failures);quit(0 if failures.is_empty() else 1)

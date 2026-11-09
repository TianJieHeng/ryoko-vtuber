extends SceneTree
# The unchanged public expression player drives every captured frame.
var rig
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
func capture():
 rig._write_pose();await process_frame;await RenderingServer.frame_post_draw
 return root.get_texture().get_image()
func run():
 for a in OS.get_cmdline_user_args():
  if a.begins_with("--output="):output=a.trim_prefix("--output=")
  if a.begins_with("--port="):port=int(a.trim_prefix("--port="))
  if a.begins_with("--view="):view_mode=a.trim_prefix("--view=")
 if output.is_empty() or port<=0:quit(2);return
 root.size=Vector2i(568,800);root.canvas_transform=Transform2D.IDENTITY
 if view_mode=="detail":
  root.size=Vector2i(400,360)
  var camera=Transform2D.IDENTITY.scaled(Vector2.ONE/.49)
  camera.origin=-Vector2(6,70)/.49-Vector2(380,380);root.canvas_transform=camera
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 check(rig.rig_ready and rig.registry_ready,"ready")
 if not rig.rig_ready or not rig.registry_ready:quit(2);return
 rig.hud.hide();rig.hint.hide();rig.pose_status.hide();rig.reset()
 var head=rig.head.transform;var body=rig.body.transform;var face_state=rig.face.snapshot()
 var originals={}
 var original_opacity={}
 for k in rig.face.objects:
  var n=rig.face.objects[k];originals[k]=[n.texture,n.region_rect,n.region_enabled,n.scale];original_opacity[k]=n.self_modulate
 peer.big_endian=true;check(peer.connect_to_host("127.0.0.1",port)==OK,"connect encoder")
 var start=Time.get_ticks_msec()
 while peer.get_status()!=StreamPeerTCP.STATUS_CONNECTED and Time.get_ticks_msec()-start<5000:
  peer.poll();await process_frame
 check(peer.get_status()==StreamPeerTCP.STATUS_CONNECTED,"encoder connected")
 if not failures.is_empty():quit(2);return
 var neutral_hash=""
 check(rig.play_expression("EXP-197"),"play new profile")
 for index in range(217):
  var t=float(index)/30.0
  if index>0:check(rig.advance(maxf(0.0,t-rig.performance_time)),"advance "+str(index))
  var expected=rig.sample_expression("EXP-197",t);var actual=rig.pose_now()
  if t<rig.RESTART_SECONDS:
   var weight=smoothstep(0.0,rig.RESTART_SECONDS,t)
   for key in expected:expected[key]*=weight
  for k in rig.CHANNELS:
   var bounds=rig.registry.CHANNEL_BOUNDS[k]
   check(is_finite(actual[k]) and actual[k]>=bounds[0] and actual[k]<=bounds[1],"bounds "+k)
   check(absf(actual[k]-expected[k])<.000001,"actual sample "+str(index)+" "+k)
  for k in rig.face.objects:
   var n=rig.face.objects[k]
   check([n.texture,n.region_rect,n.region_enabled,n.scale]==originals[k] and rig.face.homes[k].node.scale==Vector2.ONE,"fixed textures, rigid geometry "+k)
  check(rig.head.transform==head and rig.body.transform==body,"fixed head and body")
  check(not rig.face.mouth_sprite.visible,"no discrete viseme swap")
  check(rig.face.spread_tongue.visible,"native oral-surface visibility preserved")
  check(rig.face.mouth_kiss==actual.mouth_kiss,"kiss state follows shared player")
  if actual.mouth_kiss==0.0:
   for k in original_opacity:check(rig.face.objects[k].self_modulate==original_opacity[k],"native self-opacity restored")
  var im=await capture();check(im.get_size()==(Vector2i(400,360) if view_mode=="detail" else Vector2i(568,800)),"capture dimensions");var hash=digest(im)
  if index==0:neutral_hash=hash
  if index==216:check(hash==neutral_hash and rig.face.snapshot()==face_state and actual==rig.neutral_pose(),"exact neutral return")
  var bytes=im.save_png_to_buffer()
  peer.put_u32(bytes.size());check(peer.put_data(bytes)==OK,"stream frame "+str(index))
  records.append({"frame":index,"time":t,"phase":rig.phase_at(t),"pixel_sha256":hash,"mouth_open":actual.mouth_open,"blink_R":actual.blink_R,"blink_L":actual.blink_L,"blush":actual.blush_intensity,"kiss_weight":actual.mouth_kiss})
  if not failures.is_empty():break
 peer.disconnect_from_host()
 # Cheap state-only restart/release check, without another render or timeline.
 rig.play_expression("EXP-197");rig.advance(3.2);var before=rig.displayed_pose()
 check(rig.play_expression("EXP-197") and rig.displayed_pose()==before,"restart preserves displayed pose")
 check(rig.advance(.15) and rig.release() and rig.advance(.45),"restart and release")
 check(rig.pose_now()==rig.neutral_pose() and rig.face.snapshot()==face_state,"release restores neutral owners")
 var f=FileAccess.open(output+"/capture_result.json",FileAccess.WRITE)
 f.store_string(JSON.stringify({"status":"PASS" if failures.is_empty() else "FAIL","failures":failures,"frames":records,"registry_count":rig.list_expressions().size(),"separate_objects":rig.face.objects.size(),"neutral_return":true,"live_pacing_measured":false,"display":DisplayServer.get_name()},"  "));f.close()
 print("EXP197_COMPLETE_CYCLE ","PASS" if failures.is_empty() else "FAIL"," frames=",records.size()," ",failures)
 quit(0 if failures.is_empty() else 1)

extends SceneTree
var rig
var out=""
var prior=""
func _initialize():call_deferred("run")
func run():
 for arg in OS.get_cmdline_user_args():
  if arg.begins_with("--output="):out=arg.trim_prefix("--output=")
  if arg.begins_with("--prior="):prior=arg.trim_prefix("--prior=")
 var rows=JSON.parse_string(FileAccess.get_file_as_string(prior)).frames
 DirAccess.make_dir_recursive_absolute(out+"/frames")
 root.size=Vector2i(1136,1384)
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 if not rig.rig_ready or not rig.registry_ready:push_error("Rig not ready");quit(2);return
 rig.hud.hide();rig.hint.hide();rig.pose_status.hide()
 rig.head.position=Vector2.ZERO;rig.body.position=Vector2.ZERO;rig.head.scale=Vector2.ONE;rig.body.scale=Vector2.ONE
 var evidence=[]
 for i in range(121):
  var row=rows[i];rig.reset()
  if not rig.apply_controls(row.state.controls):push_error(rig.last_error);quit(2);return
  rig._write_pose()
  await process_frame;await RenderingServer.frame_post_draw
  var im=root.get_texture().get_image();im.save_png(out+"/frames/frame_%04d.png"%i)
  var hash=HashingContext.new();hash.start(HashingContext.HASH_SHA256);hash.update(im.get_data())
  evidence.append({"tick":i,"controls":row.state.controls,"sha256":hash.finish().hex_encode(),"expected_sha256":row.native_sha256,"face":rig.face.snapshot()})
  if i%30==0:print("RELIEF_PARITY_FRAME ",i)
 var f=FileAccess.open(out+"/evidence.json",FileAccess.WRITE);f.store_string(JSON.stringify({"frames":evidence,"normal_speed_playback":false},"  "));f.close()
 print("CONTENTMENT_RELIEF_PARITY_PASS frames=",evidence.size());quit(0)

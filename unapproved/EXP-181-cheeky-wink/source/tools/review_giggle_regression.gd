extends SceneTree
var rig
var out=""
var plans=""
func _initialize():call_deferred("run")
func run():
 for arg in OS.get_cmdline_user_args():
  if arg.begins_with("--output="):out=arg.trim_prefix("--output=")
  if arg.begins_with("--cases="):plans=arg.trim_prefix("--cases=")
 var cases=JSON.parse_string(FileAccess.get_file_as_string(plans))
 DirAccess.make_dir_recursive_absolute(out+"/frames")
 root.size=Vector2i(1136,1454)
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 if not rig.rig_ready or not rig.registry_ready:push_error("Rig not ready");quit(2);return
 rig.head.position=Vector2(0,70);rig.head.scale=Vector2.ONE;rig.body.position=Vector2(0,70);rig.body.scale=Vector2.ONE
 rig.hud.hide();rig.hint.hide();rig.pose_status.hide()
 var evidence=[]
 for i in range(cases.size()):
  var c=cases[i];rig.reset()
  if not rig.apply_controls(c.controls):push_error(rig.last_error);quit(2);return
  await process_frame;await RenderingServer.frame_post_draw
  var im=root.get_texture().get_image();im.save_png(out+"/frames/frame_%04d.png"%i)
  var hash=HashingContext.new();hash.start(HashingContext.HASH_SHA256);hash.update(im.get_data())
  evidence.append({"case":c,"sha256":hash.finish().hex_encode(),"state":rig.get_state(),"face":rig.face.snapshot()})
  if i%100==0:print("REGRESSION_FRAME ",i)
 var f=FileAccess.open(out+"/render_evidence.json",FileAccess.WRITE);f.store_string(JSON.stringify({"frames":evidence,"normal_speed_playback":false},"  "));f.close()
 print("REGRESSION_PASS frames=",evidence.size());quit(0)

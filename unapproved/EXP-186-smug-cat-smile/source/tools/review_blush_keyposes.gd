extends SceneTree
var rig
var out=""
var evidence=[]
func _initialize():call_deferred("run")
func capture(name):
 rig._write_pose()
 await process_frame;await RenderingServer.frame_post_draw
 var im=root.get_texture().get_image();im.save_png(out+"/"+name+".png")
 var h=HashingContext.new();h.start(HashingContext.HASH_SHA256);h.update(im.get_data())
 evidence.append({"name":name,"sha256":h.finish().hex_encode(),"state":rig.get_state(),"face":rig.face.snapshot()})
func run():
 for arg in OS.get_cmdline_user_args():
  if arg.begins_with("--output="):out=arg.trim_prefix("--output=")
 if out.is_empty():quit(2);return
 DirAccess.make_dir_recursive_absolute(out)
 root.size=Vector2i(1136,1384)
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 if not rig.rig_ready or not rig.registry_ready:push_error("readiness");quit(2);return
 rig.hud.hide();rig.hint.hide();rig.pose_status.hide()
 for scale in [1.0,.49]:
  root.size=Vector2i(1136,1384) if scale==1.0 else Vector2i(568,800)
  rig.head.scale=Vector2.ONE*scale;rig.body.scale=Vector2.ONE*scale
  rig.head.position=Vector2.ZERO if scale==1.0 else Vector2(6,70);rig.body.position=rig.head.position
  var prefix="native" if scale==1.0 else "full"
  for t in [0.0,.7,1.0,1.18,1.36,1.54,2.04,2.8]:
   rig.reset();rig.play_expression("EXP-006");rig.advance(t)
   await capture(prefix+"_%04d"%int(round(t*100)))
  for intensity in [0.0,.25,.5,.75,1.0]:
   rig.reset();rig.apply_controls({"blush_intensity":intensity})
   await capture(prefix+"_intensity_%03d"%int(round(intensity*100)))
 var f=FileAccess.open(out+"/evidence.json",FileAccess.WRITE);f.store_string(JSON.stringify({"frames":evidence,"normal_speed_playback_performed":false},"  "));f.close()
 print("BLUSH_KEYPOSES_PASS frames=",evidence.size());quit(0)

extends SceneTree
## Same harness against exact parent and candidate. No new controls or sockets.
const AXES=["brow_inner_lift_screen_left","brow_inner_lift_screen_right"]
var rig
var out=""
var full_transform
var body_transform
var records=[]
var dense=[]
var checks=0
var failures=[]
func _initialize():call_deferred("run")
func check(ok,label):
 checks+=1
 if not ok:failures.append(label)
func hash_bytes(bytes):
 var h=HashingContext.new();h.start(HashingContext.HASH_SHA256);h.update(bytes);return h.finish().hex_encode()
func strip_new(value):
 if value is Dictionary:
  var d={}
  for key in value:
   if key not in AXES:d[key]=strip_new(value[key])
  return d
 if value is Array:
  var a=[]
  for x in value:a.append(strip_new(x))
  return a
 return value
func state_hash():
 var s=rig.get_state();s.face=rig.face.snapshot();s.elapsed=rig.elapsed;s.current=rig.current_pose;s.restart=rig.restart_pose;s.release=rig.release_pose;s.performance=rig.performance
 for key in AXES:
  if s.controls.has(key):check(s.controls[key]==0,"old calls leave new channel zero")
 return hash_bytes(JSON.stringify(strip_new(s),"",true,true).to_utf8_buffer())
func image_hash(label,view,save):
 rig._write_pose();await process_frame;await RenderingServer.frame_post_draw
 var im=root.get_texture().get_image()
 if save:check(im.save_png(out+"/"+view+"/"+label+".png")==OK,"save "+label+view)
 return hash_bytes(im.get_data())
func capture(label,save=false):
 var state=state_hash()
 root.size=Vector2i(568,800);rig.head.transform=full_transform;rig.body.transform=body_transform
 var full=await image_hash(label,"full",save)
 root.size=Vector2i(1136,1384);rig.head.position=Vector2.ZERO;rig.body.position=Vector2.ZERO;rig.head.scale=Vector2.ONE;rig.body.scale=Vector2.ONE
 var native=await image_hash(label,"native",save)
 records.append({"label":label,"state_sha256":state,"full_rgba_sha256":full,"native_rgba_sha256":native})
func run():
 for arg in OS.get_cmdline_user_args():
  if arg.begins_with("--output="):out=arg.trim_prefix("--output=")
 if out.is_empty():quit(2);return
 DirAccess.make_dir_recursive_absolute(out+"/full");DirAccess.make_dir_recursive_absolute(out+"/native")
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 check(rig.rig_ready and rig.registry_ready,"ready")
 if not rig.rig_ready or not rig.registry_ready:quit(2);return
 full_transform=rig.head.transform;body_transform=rig.body.transform
 rig.hud.hide();rig.hint.hide();rig.pose_status.hide()
 await capture("neutral",true)
 for e in rig.list_expressions():
  # Two full30/60Hz state trajectories, separately from actual raster coverage.
  for hz in [30,60]:
   for cycle in range(2):
    rig.reset();rig.play_expression(e.id)
    for i in range(int(ceil(e.duration*hz))+2):
     dense.append({"id":e.id,"hz":hz,"cycle":cycle,"tick":i,"sha256":state_hash()});rig.advance(1.0/hz)
  # One complete30Hz raster trajectory, both fixed presentations.
  rig.reset();rig.play_expression(e.id)
  var ticks=int(ceil(e.duration*30))+2
  for i in range(ticks):
   await capture(e.id+"_t%03d"%i,i in [0,9,18,int(ticks/2),ticks-1]);rig.advance(1.0/30)
  # Authored/manual/release/retrigger and idle auto-blink must preserve old pixels.
  rig.reset();rig.apply_controls({"auto_blink":true});rig.advance(4.03)
  await capture(e.id+"_blink_in",true)
  rig.play_expression(e.id);await capture(e.id+"_trigger",true);rig.advance(.12)
  await capture(e.id+"_entry");rig.play_expression(e.id);await capture(e.id+"_retrigger");rig.advance(.24)
  rig.release();await capture(e.id+"_release_start");rig.advance(.2);await capture(e.id+"_release_mid",true)
  rig.play_expression(e.id);await capture(e.id+"_release_interrupt");rig.advance(.4)
  rig.apply_controls({"brow_tilt_screen_left":-.7,"brow_tilt_screen_right":.7,"blink_R":.4});await capture(e.id+"_manual",true)
  rig.advance(.8);await capture(e.id+"_manual_hold");rig.reset();await capture(e.id+"_reset",true)
  print("BROW_PARITY_CAPTURED ",e.id)
 # Old independent brow extrema with gaze/lid/hair corners.
 var index=0
 for tl in [-1.0,1.0]:
  for tr in [-1.0,1.0]:
   for ul in [-1.0,1.0]:
    for ur in [-1.0,1.0]:
     for h in [-.07,.07]:
      rig.reset();rig.apply_controls({"brow_tilt_screen_left":tl,"brow_tilt_screen_right":tr,"brow_screen_left":ul,"brow_screen_right":ur,"hair_sway":h,"blink_R":.5 if index%2 else 1.0,"blink_L":0.0 if index%2 else .5,"gaze_x":tl,"gaze_y":tr})
      await capture("old_bound_%02d"%index,index in [0,7,16,31]);index+=1
 var f=FileAccess.open(out+"/evidence.json",FileAccess.WRITE);f.store_string(JSON.stringify({"checks":checks,"failures":failures,"frames":records,"dense_states":dense,"normal_speed_playback_performed":false,"socket_test_performed":false},"  ",true,true));f.close()
 print("BROW_PARITY_CAPTURE_","PASS" if failures.is_empty() else "FAIL"," checks=",checks," raster_states=",records.size()," dense_states=",dense.size());quit(0 if failures.is_empty() else 1)

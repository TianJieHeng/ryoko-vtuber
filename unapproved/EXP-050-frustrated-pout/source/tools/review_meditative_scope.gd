extends SceneTree
## Real-render capture using the shipping shared player and fixed presentation transforms.
var rig

var out=""
var checks=0
var failures=[]
var evidence=[]
func _initialize():call_deferred("run")
func check(ok,label):
 checks+=1
 if not ok:failures.append(label)
func capture(path):
 rig._write_pose() # Refresh presentation-space shader uniforms after a fixed review placement.
 await process_frame;await RenderingServer.frame_post_draw
 var im=root.get_texture().get_image();im.save_png(path)
 var h=HashingContext.new();h.start(HashingContext.HASH_SHA256);h.update(im.get_data());return h.finish().hex_encode()
func run():
 for arg in OS.get_cmdline_user_args():
  if arg.begins_with("--output="):out=arg.trim_prefix("--output=")
 if out.is_empty():quit(2);return
 for directory in ["full","native","keyposes"]:DirAccess.make_dir_recursive_absolute(out+"/"+directory)
 root.size=Vector2i(568,800)
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 check(rig.rig_ready and rig.registry_ready,"ready")
 if not rig.rig_ready or not rig.registry_ready:quit(2);return
 rig.hud.hide();rig.hint.hide();rig.pose_status.hide()
 var sh=rig.head.transform;var sb=rig.body.transform
 var sources={}
 for key in rig.face.objects:
  var n=rig.face.objects[key];sources[key]={"texture":n.texture,"region":n.region_rect,"region_enabled":n.region_enabled}

 rig.reset();rig.apply_controls({"auto_blink":true})
 for tick in range(300):
  root.size=Vector2i(568,800);rig.head.transform=sh;rig.body.transform=sb
  if tick in [18,162]:
   var before=rig.displayed_pose();check(rig.play_expression("EXP-177"),"play");check(before==rig.displayed_pose(),"C0 play")
  if tick>0:check(rig.advance(1.0/30.0),"advance")
  var state=rig.get_state()
  var start=18 if tick<162 else 162
  var local_time=(tick-start+1)/30.0
  if tick>=start and local_time<3.9-0.000001:
   check(state.active_expression=="EXP-177" and is_equal_approx(state.time,local_time),"actual profile and time")
  if tick>=start and local_time>=1.2 and local_time<=2.35:
   check(state.controls.blink_R==1 and state.controls.blink_L==1,"actual sustained closure")
  for key in rig.CHANNELS:
   if key not in ["blink_R","blink_L"]:check(state.controls[key]==0,"no extra acting "+key)
  check(rig.head.transform==sh and rig.body.transform==sb,"fixed presentation")
  check(rig.face.oral_objects.upper_teeth.position==Vector2(533,626),"fixed enamel")
  for key in rig.face.objects:
   var n=rig.face.objects[key];var p=rig.face.homes[key].node
   check(n.scale==Vector2.ONE and p.scale==Vector2.ONE and n.modulate.a==1,"rigid owner")
   check(n.texture==sources[key].texture and n.region_rect==sources[key].region and n.region_enabled==sources[key].region_enabled,"fixed texture and UV region")
  for key in rig.face.effect_objects:
   var fx=rig.face.effect_objects[key]
   check(fx.scale==Vector2.ONE and fx.rotation==0 and fx.z_index==29,"fixed effect owner")
  var full_hash=await capture(out+"/full/frame_%04d.png"%tick)
  root.size=Vector2i(1136,1384);rig.head.position=Vector2.ZERO;rig.body.position=Vector2.ZERO;rig.head.scale=Vector2.ONE;rig.body.scale=Vector2.ONE
  var native_hash=await capture(out+"/native/frame_%04d.png"%tick)
  evidence.append({"tick":tick,"state":state,"full_sha256":full_hash,"native_sha256":native_hash})
  if tick%60==0:print("MEDITATIVE_FRAME ",tick)
 for t in [0.0,.4866515881418201,.6400595242051585,1.2,1.75,2.35,2.85,3.35,3.9]:
  rig.reset();rig.play_expression("EXP-177");rig.advance(t)
  root.size=Vector2i(1136,1384);rig.head.position=Vector2.ZERO;rig.body.position=Vector2.ZERO;rig.head.scale=Vector2.ONE;rig.body.scale=Vector2.ONE
  await capture(out+"/keyposes/native_%04d.png"%int(round(t*1000)))
  root.size=Vector2i(568,800);rig.head.transform=sh;rig.body.transform=sb
  await capture(out+"/keyposes/full_%04d.png"%int(round(t*1000)))
 var f=FileAccess.open(out+"/evidence.json",FileAccess.WRITE);f.store_string(JSON.stringify({"frames":evidence,"checks":checks,"failures":failures,"starts":[18,162],"fps":30,"duration":10.0,"normal_speed_playback_performed":false},"  "));f.close()
 print("MEDITATIVE_RENDER_", "PASS" if failures.is_empty() else "FAIL"," checks=",checks," failures=",failures);quit(0 if failures.is_empty() else 1)

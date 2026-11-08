extends SceneTree
## Actual bounded manual poses, not a claimed expression or watched playback.
var rig
var out=""
var plan=""
var records=[]
var checks=0
var failures=[]
func _initialize():call_deferred("run")
func check(ok,label):
 checks+=1
 if not ok:failures.append(label)
func capture(path):
 rig._write_pose()
 await process_frame;await RenderingServer.frame_post_draw
 var im=root.get_texture().get_image();check(im.save_png(path)==OK,"save "+path)
 var h=HashingContext.new();h.start(HashingContext.HASH_SHA256);h.update(im.get_data());return h.finish().hex_encode()
func run():
 for a in OS.get_cmdline_user_args():
  if a.begins_with("--output="):out=a.trim_prefix("--output=")
  if a.begins_with("--plan="):plan=a.trim_prefix("--plan=")
 if out.is_empty() or plan.is_empty():quit(2);return
 DirAccess.make_dir_recursive_absolute(out+"/full");DirAccess.make_dir_recursive_absolute(out+"/native")
 root.size=Vector2i(568,800)
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 check(rig.rig_ready and rig.registry_ready,"ready")
 if not rig.rig_ready or not rig.registry_ready:quit(2);return
 rig.hud.hide();rig.hint.hide();rig.pose_status.hide()
 var sh=rig.head.transform;var sb=rig.body.transform
 var original={}
 for key in rig.face.objects:
  var n=rig.face.objects[key];original[key]={"texture":n.texture,"region":n.region_rect,"region_enabled":n.region_enabled}
 var specs=JSON.parse_string(FileAccess.get_file_as_string(plan))
 for spec in specs.states:
  rig.reset();check(rig.apply_controls(spec.values),"apply "+spec.name)
  for key in spec.values:check(is_equal_approx(rig.get_state().controls[key],spec.values[key]),"actual control "+key)
  for key in rig.face.objects:
   var n=rig.face.objects[key];var parent=rig.face.homes[key].node
   check(n.scale==Vector2.ONE and parent.scale==Vector2.ONE and n.modulate.a==1,"rigid "+key)
   check(n.texture==original[key].texture and n.region_rect==original[key].region and n.region_enabled==original[key].region_enabled,"fixed UV "+key)
  for side in ["screen_left","screen_right"]:
   var home=rig.face.homes["brow_"+side];var n=home.node
   var a=rig.Limits.BROW_OUTER_ANCHORS[side]-home.pivot
   var idx=0 if side=="screen_left" else 1
   var expected=home.pivot+Vector2(0,-rig.face.brow[idx]*10)+a.rotated(rig.face.brow_tilt[idx])
   check((n.position+a.rotated(n.rotation)).distance_to(expected)<.00015,"actual transformed outer tail "+side)
  check(rig.face.oral_objects.upper_teeth.position==Vector2(533,626),"fixed enamel")
  root.size=Vector2i(568,800);rig.head.transform=sh;rig.body.transform=sb
  var full=await capture(out+"/full/"+spec.name+".png")
  root.size=Vector2i(1136,1384);rig.head.position=Vector2.ZERO;rig.body.position=Vector2.ZERO;rig.head.scale=Vector2.ONE;rig.body.scale=Vector2.ONE
  var native=await capture(out+"/native/"+spec.name+".png")
  records.append({"name":spec.name,"requested":spec.values,"state":rig.get_state(),"face":rig.face.snapshot(),"full_rgba_sha256":full,"native_rgba_sha256":native})
 var f=FileAccess.open(out+"/evidence.json",FileAccess.WRITE);f.store_string(JSON.stringify({"purpose":specs.purpose,"states":records,"checks":checks,"failures":failures,"normal_speed_playback_performed":false},"  "));f.close()
 print("BROW_EXTENSION_POSE_", "PASS" if failures.is_empty() else "FAIL"," checks=",checks," failures=",failures);quit(0 if failures.is_empty() else 1)

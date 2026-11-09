extends SceneTree
var rig
var out=""
var records=[]
var checks=0
var failures=[]
var fixed={}
var h
var b
func _initialize():call_deferred("run")
func check(ok,label):
 checks+=1
 if not ok:failures.append(label);push_error(label)
func accepted(ok,label):check(ok,label+" accepted: "+rig.last_error)
func invariant():
 check(rig.head.transform==h and rig.body.transform==b,"fixed presentation")
 check(rig.face.oral_objects.upper_teeth.position==Vector2(533,626),"fixed enamel")
 for key in fixed:
  var n=rig.face.objects[key];var owner=rig.face.homes[key].node
  check(n.scale==Vector2.ONE and owner.scale==Vector2.ONE and n.modulate==fixed[key].modulate and n.self_modulate==fixed[key].self_modulate,"rigid full-opacity owner "+key)
  check(n.texture==fixed[key].texture and n.region_rect==fixed[key].region and n.region_enabled==fixed[key].region_enabled,"fixed pigment/UV "+key)
 var p=rig.pose_now();var off=rig.Limits.gaze_pixels(Vector2(p.gaze_x,p.gaze_y),p.gaze_down_extra)
 for side in ["screen_left","screen_right"]:
  var key="iris_"+side
  check(rig.face.homes[key].node.position.is_equal_approx(rig.face.homes[key].pivot+off),"summed rigid iris")
  check(rig.face.objects[key].material.get_shader_parameter("rigid_gaze").is_equal_approx(off),"shader follows rigid iris")
func neutral():
 check(rig.pose_now()==rig.neutral_pose() and rig.displayed_pose()==rig.neutral_pose(),"exact full neutral")
 check(rig.active_performance=="" and rig.release_time<0 and not rig.auto_blink_pending_restore,"no stale owner")
func capture(label):
 rig._write_pose();invariant()
 await process_frame;await RenderingServer.frame_post_draw
 var im=root.get_texture().get_image();check(im.save_png(out+"/"+label+".png")==OK,"save "+label)
 var hash=HashingContext.new();hash.start(HashingContext.HASH_SHA256);hash.update(im.get_data())
 var digest=hash.finish().hex_encode()
 records.append({"label":label,"sha256":digest,"state":rig.get_state(),"face":rig.face.snapshot()})
 return digest
func run():
 for arg in OS.get_cmdline_user_args():
  if arg.begins_with("--output="):out=arg.trim_prefix("--output=")
 if out.is_empty():quit(2);return
 DirAccess.make_dir_recursive_absolute(out);root.size=Vector2i(1136,1384)
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 check(rig.rig_ready and rig.registry_ready,"ready")
 if not rig.rig_ready or not rig.registry_ready:quit(2);return
 rig.hud.hide();rig.hint.hide();rig.pose_status.hide()
 rig.head.position=Vector2.ZERO;rig.body.position=Vector2.ZERO;rig.head.scale=Vector2.ONE;rig.body.scale=Vector2.ONE
 h=rig.head.transform;b=rig.body.transform
 for key in rig.face.objects:
  var n=rig.face.objects[key];fixed[key]={"texture":n.texture,"region":n.region_rect,"region_enabled":n.region_enabled,"modulate":n.modulate,"self_modulate":n.self_modulate}
 accepted(rig.reset(),"reset");neutral();var zero=await capture("neutral")
 for source in ["EXP-152","EXP-005"]:
  for action in ["release","retrigger","handoff","manual","reset"]:
   var label=source+"_"+action
   accepted(rig.reset(),"reset");accepted(rig.play_expression(source),"source trigger");accepted(rig.advance(.75 if source=="EXP-152" else 1.5),"source advance")
   check(rig.active_performance==source,"source owns performance")
   var before=rig.displayed_pose();var before_hash=await capture(label+"_before")
   var target="EXP-005" if source=="EXP-152" else "EXP-152"
   if action=="release":accepted(rig.release(),"release");check(rig.active_performance=="" and rig.release_time==0,"release owns")
   elif action=="retrigger":accepted(rig.play_expression(source),"retrigger");check(rig.active_performance==source and rig.performance_time==0,"retrigger owns")
   elif action=="handoff":accepted(rig.play_expression(target),"handoff");check(rig.active_performance==target and rig.performance_time==0,"target owns")
   elif action=="manual":
    accepted(rig.apply_controls({"gaze_x":-.2,"gaze_y":.3,"gaze_down_extra":.25,"blink_R":.1,"blink_L":.15,"mouth_corner_lift":.1}),"manual")
    check(rig.active_performance=="" and rig.release_time<0 and not rig.auto_blink_pending_restore,"manual owns")
    check(is_equal_approx(rig.pose_now().gaze_down_extra,.25) and is_equal_approx(rig.pose_now().gaze_x,-.2),"actual manual controls")
   else:accepted(rig.reset(),"reset");neutral()
   if action in ["release","retrigger","handoff"]:check(rig.displayed_pose()==before,"C0 displayed controls")
   var after_hash=await capture(label+"_at");var held=rig.displayed_pose()
   if action in ["release","retrigger","handoff"]:check(before_hash==after_hash,"C0 pixels")
   for step in range(10):
    accepted(rig.advance(.05),"advance lifecycle")
    if action=="manual":check(rig.displayed_pose()==held and rig.face.owners.eyes=="manual","manual persists")
    await capture(label+"_%02d"%step)
   if action=="manual":accepted(rig.reset(),"manual reset")
   else:accepted(rig.advance(10),"complete")
   neutral();check(await capture(label+"_end")==zero,"exact final neutral pixels")
 var f=FileAccess.open(out+"/evidence.json",FileAccess.WRITE)
 check(f!=null,"open evidence")
 if f!=null:f.store_string(JSON.stringify({"frames":records,"checks":checks,"failures":failures,"normal_speed_playback":false},"  "));f.close()
 print("PRIVATE_PRIDE_LIFECYCLE_CAPTURE_","PASS" if failures.is_empty() else "FAIL"," frames=",records.size()," checks=",checks," failures=",failures.size());quit(0 if failures.is_empty() else 1)

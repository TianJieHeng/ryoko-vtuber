extends SceneTree
## Diagnostic and final captures use the existing shared player, never a second controller.
var rig
var out=""
var plan_path=""
var checks=0
var failures=[]
var records=[]
var sources={}
var validate_only=false
var graphical_lease=false
var full_head
var full_body
func _initialize():call_deferred("run")
func check(ok,label):
 checks+=1
 if not ok:
  failures.append(label)
  if failures.size()<20:push_error(label)
func digest(bytes):
 var h=HashingContext.new();h.start(HashingContext.HASH_SHA256);h.update(bytes);return h.finish().hex_encode()
func invariant(label):
 var p=rig.pose_now()
 check(p.has("mouth_width_screen_left") and p.has("mouth_width_screen_right"),label+" explicit width state")
 check(p.mouth_open==0 or (p.mouth_width_screen_left==0 and p.mouth_width_screen_right==0),label+" sealed domain")
 check(rig.face.mouth_width_sides==Vector2(p.mouth_width_screen_left,p.mouth_width_screen_right),label+" face width transport")
 for k in p:
  var bounds=rig.registry.CHANNEL_BOUNDS[k]
  check(is_finite(p[k]) and p[k]>=bounds[0]-.000001 and p[k]<=bounds[1]+.000001,label+" bounds "+k)
 for k in rig.face.objects:
  var n=rig.face.objects[k];var parent=rig.face.homes[k].node
  check(n.scale==Vector2.ONE and parent.scale==Vector2.ONE and n.modulate==Color.WHITE,label+" rigid "+k)
  check([n.texture,n.region_rect,n.region_enabled]==sources[k],label+" fixed UV "+k)
 check(rig.face.oral_objects.upper_teeth.position==Vector2(533,626),label+" fixed enamel")
 check(is_equal_approx(rig.face.MAX_MOUTH_APERTURE,.55),label+" aperture constant")
 for x in range(81):
  var gap=rig.face._smile_lip_offset(x,false,false)-rig.face._smile_lip_offset(x,true,false)
  check(gap>=-.000001 and gap<=30.800001,label+" aperture bound")
 for key in rig.face.effect_objects:
  var fx=rig.face.effect_objects[key]
  check(fx.scale==Vector2.ONE and fx.rotation==0 and fx.z_index==29,label+" fixed FX")
func expectations(spec,label):
 var state=rig.get_state()
 for k in ["auto_blink","auto_blink_pending_restore","active_expression"]:
  if spec.has(k):check(state[k]==spec[k],label+" expected "+k)
 if spec.has("mouth_transition_mode"):check(rig.mouth_transition_state().mode==spec.mouth_transition_mode,label+" fixed bridge mode")
 if spec.get("neutral",false):check(rig.pose_now()==rig.neutral_pose() and rig.active_performance=="" and rig.release_time<0,label+" exact idle neutral")
 if spec.has("minimum_closure"):check(rig.face.closure.x>=spec.minimum_closure and rig.face.closure.y>=spec.minimum_closure,label+" visible blink")
 if spec.has("maximum_closure"):check(rig.face.closure.x<=spec.maximum_closure and rig.face.closure.y<=spec.maximum_closure,label+" open eyes")
 for k in spec.get("controls",{}):check(is_equal_approx(rig.pose_now()[k],spec.controls[k]),label+" expected control "+k)
func image_hash(path):
 rig._write_pose()
 await process_frame;await RenderingServer.frame_post_draw
 var im=root.get_texture().get_image();check(im.save_png(path)==OK,"save "+path);return digest(im.get_data())
func capture(chapter,t,index):
 var label=chapter.name+"_%03d"%index
 invariant(label)
 if chapter.get("natural_cat_smile",false):
  var p=rig.pose_now();var performance_t=rig.performance_time
  for k in rig.CHANNELS:
   if k not in ["blink_R", "blink_L", "brow_screen_left", "brow_screen_right", "brow_tilt_screen_left", "brow_tilt_screen_right", "mouth_smile", "mouth_spread", "mouth_corner_lift_screen_left", "mouth_corner_lift_screen_right", "mouth_width_screen_left", "mouth_width_screen_right"]:check(p[k]==0,label+" unused natural field "+k)
  check(p.blink_R<=.360001 and p.blink_L<=.330001,label+" accepted watching eye bounds")
  check(p.mouth_open==0 and p.mouth_purse==0 and p.eye_smile_R==0 and p.eye_smile_L==0,label+" sealed ordinary-lid cat smile")
  for joint in rig.face.smile_lip_joints:
   if joint.upper:
    var peer=("mouth_corner_lower_" if joint.corner else "lower_lip_joint_")+str(joint.index)
    check(rig.face.homes[joint.key].node.transform==rig.face.homes[peer].node.transform,label+" matching sealed lip owners")
  if performance_t<=.1 or performance_t>=3.18:check(p==rig.neutral_pose(),label+" quiet neutral and exact finish interval")
 if validate_only:
  records.append({"label":label,"chapter":chapter.name,"chapter_elapsed":t,"idle_elapsed":rig.elapsed,"state":rig.get_state(),"mouth_bridge":bridge_record()});return
 root.size=Vector2i(568,800);rig.head.transform=full_head;rig.body.transform=full_body
 var state=rig.get_state();var face=rig.face.snapshot()
 check(rig.head.transform==full_head and rig.body.transform==full_body,"fixed full presentation")
 var full=await image_hash(out+"/full/"+label+".png")
 root.size=Vector2i(1136,1384);rig.head.position=Vector2.ZERO;rig.body.position=Vector2.ZERO;rig.head.scale=Vector2.ONE;rig.body.scale=Vector2.ONE
 var native=await image_hash(out+"/native/"+label+".png")
 check(rig.get_state()==state and rig.face.snapshot()==face,label+" capture does not change controls or objects")
 records.append({"label":label,"chapter":chapter.name,"checkpoint":index,"chapter_elapsed":t,"idle_elapsed":rig.elapsed,"state":state,"mouth_bridge":bridge_record(),"face":face,"full_rgba_sha256":full,"native_rgba_sha256":native})
func run():
 for a in OS.get_cmdline_user_args():
  if a=="--validate-only":validate_only=true
  if a=="--coordinator-display-lease-granted":graphical_lease=true
  if a.begins_with("--output="):out=a.trim_prefix("--output=")
  if a.begins_with("--plan="):plan_path=a.trim_prefix("--plan=")
 if out.is_empty() or plan_path.is_empty():quit(2);return
 if not validate_only and (not graphical_lease or DisplayServer.get_name()=="headless"):push_error("Graphical lease and real renderer required");quit(2);return
 var plan=JSON.parse_string(FileAccess.get_file_as_string(plan_path))
 DirAccess.make_dir_recursive_absolute(out+"/full");DirAccess.make_dir_recursive_absolute(out+"/native")
 root.size=Vector2i(568,800)
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 check(rig.rig_ready and rig.registry_ready,"ready")
 if not rig.rig_ready or not rig.registry_ready:quit(2);return
 rig.hud.hide();rig.hint.hide();rig.pose_status.hide();full_head=rig.head.transform;full_body=rig.body.transform
 for k in rig.face.objects:
  var n=rig.face.objects[k];sources[k]=[n.texture,n.region_rect,n.region_enabled]
 for chapter in plan.chapters:
  if chapter.get("reset",true):rig.reset()
  for command in chapter.setup:
   if command.has("advance"):check(rig.advance(command.advance),"setup advance")
   else:
    var before=rig.displayed_pose();check(rig.apply_controls(command),"setup command "+str(command))
    if command.has("perform_expression") or command.get("release_performance",false):check(rig.displayed_pose()==before,"C0 command "+chapter.name)
  var last=0.0
  for index in range(chapter.times.size()):
   var t=float(chapter.times[index]);check(t>=last,"ordered checkpoints")
   check(rig.advance(t-last),"advance "+chapter.name);last=t
   if chapter.has("expected_expression"):
    var expected=str(chapter.expected_expression)
    if expected!="" and t+float(chapter.get("origin",0))<rig.registry.definition(expected).duration-.000001:check(rig.active_performance==expected,"actual expression "+chapter.name)
   if chapter.get("mode","")=="release":
    check(rig.active_performance=="","release owns no expression")
    if t<.45-.000001:check(abs(rig.release_time-t)<.000001,"actual release time")
   if chapter.get("mode","")=="play":check(abs(rig.performance_time-minf(rig.registry.definition(chapter.expected_expression).duration,float(chapter.get("origin",0))+t))<.00001,"actual performance time")
   if chapter.get("assertions",{}).has(str(index)):expectations(chapter.assertions[str(index)],chapter.name+" checkpoint "+str(index))
   if chapter.has("expected_bridge_mode") and rig.active_performance!="":
    check(rig.mouth_transition_state().mode==chapter.expected_bridge_mode,"fixed expected bridge mode "+chapter.name)
    check(rig.mouth_transition_state().duration==.30,"expected bridge duration")
    if chapter.expected_bridge_mode=="staged" and t==.15:
     var p=rig.pose_now();check(p.mouth_open==0 and p.mouth_width_screen_left==0 and p.mouth_width_screen_right==0,"actual zero trio separator")
   await capture(chapter,t,index)
  expectations(chapter.get("final_expect",{}),chapter.name+" final")
  print("SMUG_CAT_SMILE_CAPTURED ",chapter.name," records=",records.size())
 var f=FileAccess.open(out+"/evidence.json",FileAccess.WRITE)
 f.store_string(JSON.stringify({"purpose":plan.purpose,"checks":checks,"failures":failures,"records":records,"plan_sha256":digest(FileAccess.get_file_as_bytes(plan_path)),"profile_sha256":digest(FileAccess.get_file_as_bytes("res://expressions/EXP-186.json")),"normal_speed_playback_observed":false,"socket_test_performed":false,"validate_only":validate_only,"display_server":DisplayServer.get_name(),"renderer":RenderingServer.get_video_adapter_name(),"source_manifest_sha256":digest(FileAccess.get_file_as_bytes("res://SMUG_CAT_SMILE_CAPTURE_FREEZE.json"))},"  "));f.close()
 print("SMUG_CAT_SMILE_TRAJECTORY_", "PASS" if failures.is_empty() else "FAIL"," checks=",checks," failures=",failures.size());quit(0 if failures.is_empty() else 1)

func bridge_record():
 var target={}
 if rig.active_performance!="":target=rig.sample_expression(rig.active_performance,rig.performance_time)
 return {"transition":rig.mouth_transition_state(),"source_pose":rig.restart_pose.duplicate(true),"sampled_target_pose":target,"release_source":rig.release_pose.duplicate(true)}

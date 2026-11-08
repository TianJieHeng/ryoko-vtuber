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
var lease=false
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
 if spec.get("neutral",false):check(rig.pose_now()==rig.neutral_pose() and rig.active_performance=="" and rig.release_time<0,label+" exact idle neutral")
 if spec.has("minimum_closure"):check(rig.face.closure.x>=spec.minimum_closure and rig.face.closure.y>=spec.minimum_closure,label+" visible blink")
 if spec.has("maximum_closure"):check(rig.face.closure.x<=spec.maximum_closure and rig.face.closure.y<=spec.maximum_closure,label+" open eyes")
 for k in spec.get("controls",{}):check(is_equal_approx(rig.pose_now()[k],spec.controls[k]),label+" expected control "+k)
func image_hash(path):
 rig._write_pose()
 await process_frame;await RenderingServer.frame_post_draw
 var im=root.get_texture().get_image();check(not im.is_empty(),"nonempty actual frame");check(im.save_png(path)==OK,"save "+path);return {"rgba_sha256":digest(im.get_data()),"png_sha256":digest(FileAccess.get_file_as_bytes(path)),"width":im.get_width(),"height":im.get_height(),"path":path}
func capture(chapter,t,index):
 var label=chapter.name+"_%03d"%index
 invariant(label)
 if validate_only:
  records.append({"label":label,"state":rig.get_state()});return
 root.size=Vector2i(568,800);rig.head.transform=full_head;rig.body.transform=full_body
 var state=rig.get_state();var face=rig.face.snapshot()
 check(rig.head.transform==full_head and rig.body.transform==full_body,"fixed full presentation")
 var full=await image_hash(out+"/full/"+label+".png")
 root.size=Vector2i(1136,1384);rig.head.position=Vector2.ZERO;rig.body.position=Vector2.ZERO;rig.head.scale=Vector2.ONE;rig.body.scale=Vector2.ONE
 var native=await image_hash(out+"/native/"+label+".png")
 check(rig.get_state()==state and rig.face.snapshot()==face,"capture retains real state "+label)
 root.size=Vector2i(568,800);rig.head.transform=full_head;rig.body.transform=full_body
 records.append({"label":label,"chapter":chapter.name,"checkpoint":index,"chapter_elapsed":t,"state":state,"face":face,"full_render":full,"native_render":native})
func run():
 for a in OS.get_cmdline_user_args():
  if a=="--validate-only":validate_only=true
  if a=="--coordinator-display-lease-granted":lease=true
  if a.begins_with("--output="):out=a.trim_prefix("--output=")
  if a.begins_with("--plan="):plan_path=a.trim_prefix("--plan=")
 if out.is_empty() or plan_path.is_empty():quit(2);return
 if not validate_only and (not lease or DisplayServer.get_name()=="headless"):
  push_error("Graphical capture requires the explicit coordinator lease and real display");quit(2);return
 var plan=JSON.parse_string(FileAccess.get_file_as_string(plan_path))
 check(digest(FileAccess.get_file_as_bytes("res://expressions/EXP-164.json"))==plan.profile_sha256,"pinned profile hash")
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
   var expected=rig.pose_now().duplicate()
   if chapter.get("mode","")=="play":
    expected=rig.sample_expression(chapter.expected_expression,rig.performance_time)
    if rig.performance_time<rig.RESTART_SECONDS:
     var weight=smoothstep(0.0,rig.RESTART_SECONDS,rig.performance_time)
     for k in rig.CHANNELS:expected[k]=lerpf(rig.restart_pose.get(k,0),expected[k],weight)
   elif chapter.get("mode","")=="release":
    var weight=smoothstep(0.0,rig.RELEASE_SECONDS,t)
    for k in rig.CHANNELS:expected[k]=lerpf(rig.release_pose[k],0,weight)
   for k in rig.CHANNELS:check(is_equal_approx(rig.pose_now()[k],expected[k]),"actual coordinate "+chapter.name+" "+k)
   if chapter.get("assertions",{}).has(str(index)):expectations(chapter.assertions[str(index)],chapter.name+" checkpoint "+str(index))
   await capture(chapter,t,index)
  expectations(chapter.get("final_expect",{}),chapter.name+" final")
  print("FIGHTING_SLEEP_CAPTURED ",chapter.name," records=",records.size())
 check(records.size()==plan.expected_records,"exact pinned record count")
 var f=FileAccess.open(out+"/evidence.json",FileAccess.WRITE)
 f.store_string(JSON.stringify({"purpose":plan.purpose,"checks":checks,"failures":failures,"records":records,"plan_sha256":digest(FileAccess.get_file_as_bytes(plan_path)),"profile_sha256":digest(FileAccess.get_file_as_bytes("res://expressions/EXP-164.json")),"normal_speed_playback_observed":false,"socket_test_performed":false,"validate_only":validate_only},"  "));f.close()
 print("FIGHTING_SLEEP_TRAJECTORY_", "PASS" if failures.is_empty() else "FAIL"," checks=",checks," failures=",failures.size());quit(0 if failures.is_empty() else 1)

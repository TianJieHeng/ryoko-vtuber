extends SceneTree
## Diagnostic and final captures use the existing shared player, never a second controller.
var rig
var out=""
var plan_path=""
var checks=0
var failures=[]
var record_index=[]
var plan={}
var sources={}
var validate_only=false
var graphical_lease=false
var full_head
var full_body
var full_rig
var parentage={}
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
 check(rig.head.transform==full_head and rig.body.transform==full_body and rig.transform==full_rig,label+" fixed canonical head/body/root")
 check(rig.head.transform==Transform2D(Vector2(.49,0),Vector2(0,.49),Vector2(6,70)) and rig.body.transform==rig.head.transform,label+" approved presentation defaults")
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
 if chapter.get("natural_secondhand_embarrassment",false):
  var p=rig.pose_now();var performance_t=rig.performance_time
  for k in rig.CHANNELS:
   if k not in ["blink_R", "blink_L", "brow_screen_left", "brow_screen_right", "brow_tilt_screen_left", "brow_tilt_screen_right", "brow_inner_lift_screen_left", "brow_inner_lift_screen_right", "eye_smile_L", "mouth_smile", "mouth_corner_lift_screen_left", "mouth_corner_lift_screen_right", "mouth_width_screen_left", "mouth_width_screen_right", "blush_intensity"]:check(p[k]==0,label+" unused natural field "+k)
  check(p.blink_R<=.520001 and p.eye_smile_R==0,label+" left never second full wink")
  check(p.mouth_open==0 and p.mouth_purse==0 and p.mouth_spread==0,label+" sealed embarrassed face")
  if performance_t>=1.66:check(p.eye_smile_L==0,label+" no later closed-contour pulse")
  for joint in rig.face.smile_lip_joints:
   if joint.upper:
    var peer=("mouth_corner_lower_" if joint.corner else "lower_lip_joint_")+str(joint.index)
    check(rig.face.homes[joint.key].node.transform==rig.face.homes[peer].node.transform,label+" matching sealed lip owners")
  if performance_t<=.12 or performance_t>=3.12:check(p==rig.neutral_pose(),label+" quiet neutral and exact finish interval")
 var state=rig.get_state();var face=rig.face.snapshot();var expected=expected_ownership(chapter,t)
 check(state.active_expression==expected.active and (state.release_time>=0)==expected.releasing,label+" planned active/release/manual state")
 var direct=direct_record();var ancestry={};var native_coordinates=native_coordinate_record(direct,ancestry)
 var ownership=validated_ownership(direct,expected.owner,label)
 var manual_comparison=native_coordinates.duplicate(true)
 for key in manual_comparison.face_snapshot.owners:manual_comparison.face_snapshot.owners[key]="manual"
 for side in manual_comparison.face_snapshot.effects:manual_comparison.face_snapshot.effects[side].owner="manual"
 var direct_hash=value_hash(direct);var coordinate_hash=value_hash(native_coordinates);var comparison_hash=value_hash(manual_comparison)
 var record={"label":label,"chapter":chapter.name,"checkpoint":index,"chapter_elapsed":t,"idle_elapsed":rig.elapsed,"state":state,"mouth_bridge":bridge_record(),"face":face,"expected_ownership":expected,"validated_ownership":ownership,"direct_sha256":direct_hash,"native_coordinate_sha256":coordinate_hash,"static_manual_comparison_sha256":comparison_hash,"direct_file":"direct/"+label+".json"}
 var object_paths={"objects":{},"effects":{}}
 for key in rig.face.objects:object_paths.objects[key]=str(rig.get_path_to(rig.face.objects[key]))
 for key in rig.face.effect_objects:object_paths.effects[key]=str(rig.get_path_to(rig.face.effect_objects[key]))
 var payload={"object_paths":object_paths,"raw_direct_json":JSON.stringify(normalize(direct),"",true,true),"native_coordinate_json":JSON.stringify(normalize(native_coordinates),"",true,true),"static_manual_comparison_json":JSON.stringify(normalize(manual_comparison),"",true,true),"ancestry":ancestry,"coordinate_contract":"Actual Node2D ancestry composed relative to unchanged canonical head; raw globals retained and individually checked against actual parent globals. No inverse of rounded global values."}
 var direct_bytes=(JSON.stringify(payload,"  ",true,true)+"\n").to_utf8_buffer()
 var f=FileAccess.open(out+"/"+record.direct_file,FileAccess.WRITE);check(f!=null,"open direct checkpoint "+label)
 if f==null:return
 f.store_buffer(direct_bytes);f.flush();var direct_ok=f.get_error()==OK;f.close();check(direct_ok,"flush direct checkpoint "+label)
 if not direct_ok:return
 check(digest(FileAccess.get_file_as_bytes(out+"/"+record.direct_file))==digest(direct_bytes),"exact written direct checkpoint "+label)
 record.direct_file_sha256=digest(direct_bytes);record.direct_file_bytes=direct_bytes.size()
 if validate_only:
  for view in ["full","native"]:
   set_view(view);check(direct_record()==direct,label+" headless camera-only raw identity "+view)
  root.canvas_transform=Transform2D.IDENTITY;root.size=Vector2i(568,800)
  write_record(record);return
 for view in ["full","native"]:
  set_view(view)
  record[view+"_rgba_sha256"]=await image_hash(out+"/"+view+"/"+label+".png")
  check(direct_record()==direct,label+" camera-only unchanged raw direct record "+view)
  check(rig.get_state()==state and rig.face.snapshot()==face,label+" capture unchanged control/owner state "+view)
  record[view+"_direct_sha256"]=value_hash(direct_record())
  record[view+"_camera"]={"canvas_transform":normalize(root.canvas_transform),"effective_head_transform":normalize(root.canvas_transform*rig.head.global_transform),"effective_body_transform":normalize(root.canvas_transform*rig.body.global_transform),"head_transform":normalize(rig.head.transform),"body_transform":normalize(rig.body.transform),"rig_transform":normalize(rig.transform)}
 root.canvas_transform=Transform2D.IDENTITY;root.size=Vector2i(568,800)
 write_record(record)
func set_view(view):
 root.size=Vector2i(568,800) if view=="full" else Vector2i(1136,1384)
 root.canvas_transform=Transform2D.IDENTITY if view=="full" else full_head.affine_inverse()
 check(rig.head.transform==full_head and rig.body.transform==full_body and rig.transform==full_rig,"camera-only canonical transforms "+view)
 var effective=full_head if view=="full" else Transform2D.IDENTITY
 check(root.canvas_transform*rig.head.global_transform==effective and root.canvas_transform*rig.body.global_transform==effective,"exact effective camera transform "+view)
func expected_ownership(chapter,t):
 if chapter.get("mode","")=="play":
  var id=str(chapter.expected_expression);var active=id if t+float(chapter.get("origin",0))<rig.registry.definition(id).duration else ""
  return {"active":active,"releasing":false,"owner":active if active!="" else "manual"}
 if chapter.get("mode","")=="release":return {"active":"","releasing":t<.45,"owner":"release" if t<.45 else "manual"}
 return {"active":"","releasing":false,"owner":"manual"}
func validated_ownership(direct,expected,label):
 var owners=direct.face_snapshot.owners;var effects=direct.face_snapshot.effects
 check(owners.size()==4 and effects.size()==2,label+" exact six ownership label schema")
 var labels={"owners":owners.duplicate(true),"effect_owners":{}}
 for key in ["eyes","brows","mouth","hair"]:check(owners.get(key)==expected and rig.get_state().owners.get(key)==expected,label+" expected owner "+key)
 for side in ["screen_left","screen_right"]:
  check(effects.has(side) and effects[side].owner==expected,label+" expected FX owner "+side);labels.effect_owners[side]=effects[side].owner
 return labels
func native_relative(node,ancestry):
 var chain=[];var current=node
 while current!=rig.head:
  check(current is Node2D and current!=rig,"face owner descends from canonical head")
  if not current is Node2D or current==rig:return Transform2D.IDENTITY
  var path=str(rig.get_path_to(current));var parent=current.get_parent()
  check(parent is Node2D,"actual Node2D ancestry parent")
  check(parentage.get(path)==str(rig.get_path_to(parent)),"unchanged parentage "+path)
  check(current.global_transform==parent.global_transform*current.transform,"exact actual parent/global composition "+path)
  ancestry[path]={"parent":str(rig.get_path_to(parent)),"local_transform":normalize(current.transform),"global_transform":normalize(current.global_transform),"parent_global_transform":normalize(parent.global_transform)}
  chain.push_front(current.transform);current=parent
 var relative=Transform2D.IDENTITY
 for transform in chain:relative=relative*transform
 return relative
func native_coordinate_record(raw,ancestry):
 var result=raw.duplicate(true)
 # These are named comparison coordinates, never writes to a live scene node.
 result.head_transform=normalize(Transform2D.IDENTITY);result.body_transform=normalize(Transform2D.IDENTITY)
 for key in rig.face.objects:result.objects[key].global_transform=normalize(native_relative(rig.face.objects[key],ancestry))
 for key in rig.face.effect_objects:result.effects[key].global_transform=normalize(native_relative(rig.face.effect_objects[key],ancestry))
 return result
func bind_parentage(node):
 for child in node.get_children():
  if child is Node2D:parentage[str(rig.get_path_to(child))]=str(rig.get_path_to(child.get_parent()))
  bind_parentage(child)

func run():
 for a in OS.get_cmdline_user_args():
  if a=="--validate-only":validate_only=true
  if a=="--coordinator-display-lease-granted":graphical_lease=true
  if a.begins_with("--output="):out=a.trim_prefix("--output=")
  if a.begins_with("--plan="):plan_path=a.trim_prefix("--plan=")
 if out.is_empty() or plan_path.is_empty():quit(2);return
 if not validate_only and (not graphical_lease or DisplayServer.get_name()=="headless"):push_error("Graphical lease and real renderer required");quit(2);return
 plan=JSON.parse_string(FileAccess.get_file_as_string(plan_path))
 DirAccess.make_dir_recursive_absolute(out+"/full");DirAccess.make_dir_recursive_absolute(out+"/native");DirAccess.make_dir_recursive_absolute(out+"/direct");DirAccess.make_dir_recursive_absolute(out+"/records")
 root.size=Vector2i(568,800)
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 check(rig.rig_ready and rig.registry_ready,"ready")
 if not rig.rig_ready or not rig.registry_ready:quit(2);return
 rig.hud.hide();rig.hint.hide();rig.pose_status.hide();full_head=rig.head.transform;full_body=rig.body.transform;full_rig=rig.transform
 check(full_rig==Transform2D.IDENTITY,"canonical rig root identity");bind_parentage(rig.head)
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
  print("SECONDHAND_EMBARRASSMENT_CAPTURED ",chapter.name," records=",record_index.size())
 if failures.is_empty():validate_record_files()
 var result={"status":"PASS" if failures.is_empty() else "FAIL","purpose":plan.purpose,"checks":checks,"failures":failures,"serialization_schema":"EXP097_RECORD_FILES_V1","serialization_complete":failures.is_empty(),"record_count":record_index.size(),"expected_record_count":int(plan.checkpoints),"record_files":record_index,"plan_sha256":digest(FileAccess.get_file_as_bytes(plan_path)),"profile_sha256":digest(FileAccess.get_file_as_bytes("res://expressions/EXP-097.json")),"harness_sha256":digest(FileAccess.get_file_as_bytes(get_script().resource_path)),"normal_speed_playback_observed":false,"socket_test_performed":false,"validate_only":validate_only,"display_server":DisplayServer.get_name(),"renderer":RenderingServer.get_video_adapter_name(),"source_manifest_sha256":digest(FileAccess.get_file_as_bytes("res://SECONDHAND_EMBARRASSMENT_CAPTURE_FREEZE.json"))}
 var f=FileAccess.open(out+"/evidence.json",FileAccess.WRITE);f.store_string(JSON.stringify(result,"  ",true,true));f.flush();var finish_ok=f.get_error()==OK;f.close()
 print("SECONDHAND_EMBARRASSMENT_TRAJECTORY_", "PASS" if failures.is_empty() and finish_ok else "FAIL"," checks=",checks," failures=",failures.size());quit(0 if failures.is_empty() and finish_ok else 1)

func write_record(row):
 # Retain only a small descriptor, never the complete traversal array.
 var ordinal=record_index.size();var relative="records/%04d.json"%ordinal;var path=out+"/"+relative
 check(not FileAccess.file_exists(path),"record destination is new "+relative)
 if FileAccess.file_exists(path):return
 var text=JSON.stringify(row,"  ",true,true);var bytes=text.to_utf8_buffer()
 var f=FileAccess.open(path,FileAccess.WRITE);check(f!=null,"open complete checkpoint "+relative)
 if f==null:return
 f.store_buffer(bytes);f.flush();var ok=f.get_error()==OK;f.close();check(ok,"flush complete checkpoint "+relative)
 if not ok:return
 check(digest(FileAccess.get_file_as_bytes(path))==digest(bytes),"written checkpoint hash "+relative)
 record_index.append({"ordinal":ordinal,"label":row.label,"chapter":row.chapter,"checkpoint":row.checkpoint,"chapter_elapsed":row.chapter_elapsed,"path":relative,"sha256":digest(bytes),"bytes":bytes.size()})
func validate_record_files():
 # Final PASS is impossible without the full plan order and exact flushed files.
 check(record_index.size()==int(plan.checkpoints),"complete manifest record count")
 var ordinal=0;var names=[]
 for chapter in plan.chapters:
  for checkpoint in range(chapter.times.size()):
   if ordinal>=record_index.size():check(false,"missing final record descriptor");return
   var entry=record_index[ordinal];var relative="records/%04d.json"%ordinal
   var label=chapter.name+"_%03d"%checkpoint
   check(entry.ordinal==ordinal and entry.path==relative and entry.label==label and entry.chapter==chapter.name and entry.checkpoint==checkpoint and entry.chapter_elapsed==chapter.times[checkpoint],"ordered final descriptor "+str(ordinal))
   var bytes=FileAccess.get_file_as_bytes(out+"/"+relative)
   check(bytes.size()==entry.bytes and digest(bytes)==entry.sha256,"final record bytes/hash "+relative)
   var row=JSON.parse_string(bytes.get_string_from_utf8());check(row is Dictionary,"complete JSON checkpoint "+relative)
   if row is Dictionary:check(row.label==label and row.chapter==chapter.name and row.checkpoint==checkpoint and row.chapter_elapsed==chapter.times[checkpoint],"final checkpoint identity "+relative)
   names.append(relative.get_file());ordinal+=1
 check(ordinal==int(plan.checkpoints),"all final expected records visited")
 var actual=[]
 for file in DirAccess.get_files_at(out+"/records"):actual.append(file)
 actual.sort();names.sort();check(actual==names,"no missing duplicate or extra checkpoint files")

func bridge_record():
 var target={}
 if rig.active_performance!="":target=rig.sample_expression(rig.active_performance,rig.performance_time)
 return {"transition":rig.mouth_transition_state(),"source_pose":rig.restart_pose.duplicate(true),"sampled_target_pose":target,"release_source":rig.release_pose.duplicate(true)}

func normalize(v):
 if v is Dictionary:
  var result={}
  for k in v:result[k]=normalize(v[k])
  return result
 if v is Array:
  var result=[]
  for item in v:result.append(normalize(item))
  return result
 if v is Vector2:return [v.x,v.y]
 if v is Vector2i:return [v.x,v.y]
 if v is Rect2:return [v.position.x,v.position.y,v.size.x,v.size.y]
 if v is Transform2D:return [v.x.x,v.x.y,v.y.x,v.y.y,v.origin.x,v.origin.y]
 if v is Color:return [v.r,v.g,v.b,v.a]
 if v is AtlasTexture:return {"atlas":normalize(v.atlas),"region":normalize(v.region),"margin":normalize(v.margin),"filter_clip":v.filter_clip}
 if v is Resource:return v.resource_path
 return v
func value_hash(value):return JSON.stringify(normalize(value),"",true,true).sha256_text()
func material_record(n):
 if not n.material is ShaderMaterial:return {}
 var uniforms={}
 for item in n.material.shader.get_shader_uniform_list():uniforms[item.name]=normalize(n.material.get_shader_parameter(item.name))
 return {"shader":n.material.shader.resource_path,"uniforms":uniforms}
func owner_record(key):
 var n=rig.face.objects[key];var p=rig.face.homes[key].node
 return {"pivot_transform":normalize(p.transform),"sprite_transform":normalize(n.transform),"global_transform":normalize(n.global_transform),"modulate":normalize(n.modulate),"self_modulate":normalize(n.self_modulate),"visible":n.visible,"z_index":n.z_index,"texture":normalize(n.texture),"region_enabled":n.region_enabled,"region_rect":normalize(n.region_rect),"material":material_record(n)}
func direct_record():
 var owners={};var effects={}
 for key in rig.face.objects:owners[key]=owner_record(key)
 for key in rig.face.effect_objects:
  var n=rig.face.effect_objects[key]
  effects[key]={"transform":normalize(n.transform),"global_transform":normalize(n.global_transform),"texture":normalize(n.texture),"visible":n.visible,"modulate":normalize(n.modulate),"self_modulate":normalize(n.self_modulate),"z_index":n.z_index,"material":material_record(n)}
 return {"objects":owners,"effects":effects,"head_transform":normalize(rig.head.transform),"body_transform":normalize(rig.body.transform),"body_texture":normalize(rig.body.texture),"rig_transform":normalize(rig.transform),"face_transform":normalize(rig.face.transform),"face_snapshot":rig.face.snapshot()}

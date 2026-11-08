extends SceneTree
## Actual unchanged shared player. Only root canvas/viewport change for the two presentations.
const ID="EXP-114"
const ALLOWED=["blink_R","blink_L","brow_screen_left","brow_screen_right","brow_tilt_screen_left","brow_tilt_screen_right","mouth_open","mouth_smile","mouth_spread","mouth_corner_lift_screen_left","mouth_corner_lift_screen_right"]
var rig
var output=""
var plan_path=""
var plan={}
var validate_only=false
var runtime_lease=false
var display_lease=false
var review_approved=false
var checks=0
var failures=[]
var records=[]
var textures={}
var fixed_owners={}
var neutral_snapshot={}
var neutral_face_state={}
var registry_before=[]
var imported_inspection={}
var full_head:Transform2D
var full_body:Transform2D
var full_rig:Transform2D
func _initialize():call_deferred("run")
func check(ok,label):
 checks+=1
 if not ok:
  failures.append(label)
  if failures.size()<20:push_error(label)
func digest(bytes):
 var h=HashingContext.new();h.start(HashingContext.HASH_SHA256);h.update(bytes);return h.finish().hex_encode()
func encoded(v):
 if v is Vector2 or v is Vector2i:return [v.x,v.y]
 if v is Transform2D:return [encoded(v.x),encoded(v.y),encoded(v.origin)]
 if v is Color:return [v.r,v.g,v.b,v.a]
 if v is Rect2:return [encoded(v.position),encoded(v.size)]
 if v is Resource:
  var result={"class":v.get_class(),"resource_path":v.resource_path,"instance_id":v.get_instance_id()}
  if v is Texture2D:result.size=[v.get_width(),v.get_height()]
  if v is AtlasTexture:
   result.atlas=encoded(v.atlas);result.region=encoded(v.region);result.margin=encoded(v.margin);result.filter_clip=v.filter_clip
  return result
 if v is Array:
  var a=[]
  for item in v:a.append(encoded(item))
  return a
 if v is Dictionary:
  var d={}
  for key in v:d[str(key)]=encoded(v[key])
  return d
 if v is StringName or v is NodePath:return str(v)
 return v
func uniforms(node):
 var result={}
 if node is CanvasItem and node.material is ShaderMaterial:
  for u in node.material.shader.get_shader_uniform_list():result[str(u.name)]=node.material.get_shader_parameter(u.name)
 return result
func snapshot_node(n):
 var d={"class":n.get_class(),"instance_id":n.get_instance_id(),"children":[]}
 for child in n.get_children():d.children.append(str(child.name))
 if n is CanvasItem:
  d.visible=n.visible;d.modulate=encoded(n.modulate);d.self_modulate=encoded(n.self_modulate);d.z_index=n.z_index;d.z_as_relative=n.z_as_relative
  d.material=encoded(n.material);d.use_parent_material=n.use_parent_material;d.texture_filter=n.texture_filter;d.texture_repeat=n.texture_repeat
  if n.material is ShaderMaterial:d.shader=encoded(n.material.shader);d.uniforms=encoded(uniforms(n))
 if n is Node2D:
  d.transform=encoded(n.transform);d.position=encoded(n.position);d.rotation=n.rotation;d.scale=encoded(n.scale);d.skew=n.skew
 if n is Sprite2D:
  d.texture=encoded(n.texture);d.centered=n.centered;d.offset=encoded(n.offset);d.region_enabled=n.region_enabled;d.region_rect=encoded(n.region_rect);d.region_filter_clip_enabled=n.region_filter_clip_enabled
  d.flip_h=n.flip_h;d.flip_v=n.flip_v;d.hframes=n.hframes;d.vframes=n.vframes;d.frame=n.frame
 return d
func walk_snapshot(n,d):
 d[str(rig.get_path_to(n))]=snapshot_node(n)
 for child in n.get_children():walk_snapshot(child,d)
func actual_snapshot():
 var d={};walk_snapshot(rig,d);return d
func fingerprint(n):
 return [n.texture,n.material,n.scale,n.modulate,n.self_modulate,n.offset,n.flip_h,n.flip_v,n.region_enabled,n.region_rect,n.centered,n.hframes,n.vframes,n.frame]
func owner_record(key):
 var n=rig.face.objects[key];var p=rig.face.homes[key].node
 return {"owner_path":str(rig.get_path_to(n)),"pivot_path":str(rig.get_path_to(p)),"home_pivot":encoded(rig.face.homes[key].pivot),"owner":snapshot_node(n),"pivot":snapshot_node(p)}
func direct_owners():
 var d={}
 for key in rig.face.objects:d[key]=owner_record(key)
 return d
func inspect_texture(tex):
 if tex==null:return
 if tex is AtlasTexture:inspect_texture(tex.atlas);return
 if not tex is Texture2D:return
 var path=tex.resource_path
 if path.is_empty() or imported_inspection.has(path):return
 check(path.begins_with("res://") and path.ends_with(".png"),"original PNG texture "+path)
 if not path.ends_with(".png"):return
 var loaded=tex.get_image();check(loaded!=null,"actual loaded image readable "+path)
 if loaded==null:return
 var raw=Image.load_from_file(path);check(raw!=null,"raw PNG readable "+path)
 if raw==null:return
 var original_format=loaded.get_format();var compressed=loaded.is_compressed()
 if compressed:check(loaded.decompress()==OK,"loaded decompress "+path)
 loaded.convert(Image.FORMAT_RGBA8);raw.convert(Image.FORMAT_RGBA8)
 check(loaded.get_size()==raw.get_size(),"raw/loaded dimensions "+path)
 var a=raw.get_data();var b=loaded.get_data();check(a.size()==b.size(),"raw/loaded bytes "+path)
 var file_name=path.trim_prefix("res://").replace("/","__")+".loaded.rgba"
 var f=FileAccess.open(output+"/imported_data/"+file_name,FileAccess.WRITE);f.store_buffer(b);f.close()
 imported_inspection[path]={"texture":encoded(tex),"original_format":original_format,"original_compressed":compressed,"rgba_size":encoded(loaded.get_size()),"raw_rgba_sha256":digest(a),"loaded_rgba_sha256":digest(b),"loaded_data_file":"imported_data/"+file_name,"source_png_sha256":digest(FileAccess.get_file_as_bytes(path))}
 # Full differences are independently calculated from actual emitted RGBA, without retouching.
func inspect_node_textures(n):
 if n is Sprite2D:inspect_texture(n.texture)
 if n is CanvasItem and n.material is ShaderMaterial:
  for value in uniforms(n).values():
   if value is Texture2D:inspect_texture(value)
 for child in n.get_children():inspect_node_textures(child)
func set_view(view):
 if view=="bust":root.size=Vector2i(568,800);root.canvas_transform=Transform2D.IDENTITY
 else:root.size=Vector2i(1136,1384);root.canvas_transform=full_head.affine_inverse()
 check(rig.transform==full_rig and rig.head.transform==full_head and rig.body.transform==full_body,"camera-only view "+view)
 var effective=root.canvas_transform*rig.head.transform
 if view=="native":check(effective.is_equal_approx(Transform2D.IDENTITY),"actual native one-to-one camera")
 else:check(effective==full_head,"actual .49 bust camera")
func capture_image(path):
 var before=actual_snapshot();var pose=rig.pose_now()
 await process_frame;await RenderingServer.frame_post_draw
 await process_frame;await RenderingServer.frame_post_draw
 check(actual_snapshot()==before and rig.pose_now()==pose,"renderer preserved direct owners "+path)
 var im=root.get_texture().get_image();check(im.save_png(path)==OK,"actual capture "+path)
 return {"rgba_sha256":digest(im.get_data()),"png_sha256":digest(FileAccess.get_file_as_bytes(path)),"size":encoded(im.get_size()),"canvas_transform":encoded(root.canvas_transform),"effective_head_transform":encoded(root.canvas_transform*full_head),"head_transform":encoded(rig.head.transform),"body_transform":encoded(rig.body.transform),"rig_transform":encoded(rig.transform)}

func stable(v):
 if v is Dictionary:
  var result={}
  for key in v:
   if key!="instance_id":result[key]=stable(v[key])
  return result
 if v is Array:
  var result=[]
  for item in v:result.append(stable(item))
  return result
 return v
func record_digest(v):return JSON.stringify(stable(encoded(v)),"",true,true).sha256_text()
func expected_owner():return rig.active_performance if rig.active_performance!="" else ("release" if rig.release_time>=0 else "manual")
func transport_pose(p):
 var result=p.duplicate()
 for key in ["blink_R","blink_L","brow_screen_left","brow_screen_right","brow_tilt_screen_left","brow_tilt_screen_right","brow_inner_lift_screen_left","brow_inner_lift_screen_right","gaze_x","gaze_y","eye_smile_R","eye_smile_L","mouth_corner_lift_screen_left","mouth_corner_lift_screen_right","mouth_width_screen_left","mouth_width_screen_right"]:result[key]=Vector2(p[key],0).x
 return result
func expected_player_pose():
 var p=rig.neutral_pose()
 if rig.active_performance!="":
  var definition=rig.registry.definition(rig.active_performance);var time=rig.performance_time
  if time>0 and time<definition.duration:
   for i in range(definition.keyframes.size()-1):
    var a=definition.keyframes[i];var b=definition.keyframes[i+1]
    if time>=a.time and time<=b.time:
     var u=clampf((time-a.time)/(b.time-a.time),0,1);u=u*u*(3-2*u)
     for key in rig.CHANNELS:p[key]=lerpf(float(a.values.get(key,0)),float(b.values.get(key,0)),u)
     break
  var raw=p.duplicate();var mode=rig.mouth_transition_state().mode
  if time<.30:
   var w=smoothstep(0.0,.30,time)
   for key in rig.CHANNELS:p[key]=lerpf(rig.restart_pose.get(key,0),p[key],w)
  if mode not in ["none","legacy"]:
   var duration=minf(.30,definition.duration);var u=clampf(time/duration,0,1)
   for key in ["mouth_open","mouth_width_screen_left","mouth_width_screen_right"]:
    if time>=duration:p[key]=raw[key]
    elif mode=="bounded_direct":p[key]=lerpf(float(rig.restart_pose.get(key,0)),float(raw[key]),smoothstep(0.0,1.0,u))
    elif u<=.5:p[key]=float(rig.restart_pose.get(key,0))*(1.0-smoothstep(0.0,.5,u))
    else:p[key]=float(raw[key])*smoothstep(.5,1.0,u)
 elif rig.release_time>=0:
  var u=smoothstep(0.0,.45,rig.release_time)
  for key in rig.CHANNELS:p[key]=lerpf(rig.release_pose[key],0,u)
 else:return {}
 return transport_pose(p)
func invariant(label,natural):
 var p=rig.pose_now();var face=rig.face
 var expected=expected_player_pose()
 if not expected.is_empty():check(p==expected,label+" exact modeled sampler/restart/bridge/release and float32 public transport")
 check(rig.list_expressions()==registry_before,label+" fixed nineteen registry entries")
 check(rig.transform==full_rig and rig.head.transform==full_head and rig.body.transform==full_body and face.transform==Transform2D.IDENTITY,label+" fixed root/head/neck/body/face")
 check(p.mouth_open==0 or (p.mouth_width_screen_left==0 and p.mouth_width_screen_right==0),label+" strict open/new-width exclusion")
 check(face.mouth_width_sides==Vector2(p.mouth_width_screen_left,p.mouth_width_screen_right),label+" actual width transport")
 var owner=expected_owner();var snapshot=face.snapshot()
 check(snapshot.owners=={"eyes":owner,"brows":owner,"mouth":owner,"hair":owner},label+" explicit active/release/manual ownership")
 for side in ["screen_left","screen_right"]:check(snapshot.effects[side].owner==owner,label+" explicit effect ownership "+side)
 for key in rig.CHANNELS:
  var bounds=rig.registry.CHANNEL_BOUNDS[key]
  check(is_finite(p[key]) and p[key]>=bounds[0] and p[key]<=bounds[1],label+" bounded public "+key)
  if natural and key not in ALLOWED:check(p[key]==0,label+" unused natural channel "+key)
 for key in face.objects:
  var n=face.objects[key];var pivot=face.homes[key].node
  check(fingerprint(n)==textures[key],label+" original texture/material/UV/opacity "+key)
  check(n.scale==Vector2.ONE and pivot.scale==Vector2.ONE and n.modulate==Color.WHITE and n.self_modulate==Color.WHITE and pivot.modulate==Color.WHITE,label+" rigid opaque anatomy "+key)
  check(pivot.position.is_finite() and is_finite(pivot.rotation),label+" finite owner "+key)
 # All chapters retain the source art; hair may move only in a prior expression stress chapter.
 if natural:
  for key in fixed_owners:check(owner_record(key)==fixed_owners[key],label+" fixed unrelated owner "+key)
  check(p.blink_R<=.280001 and p.blink_L<=.280001 and p.mouth_open<=.340001,label+" accepted ordinary eyes and shallow grin envelope")
  check(face.gaze==Vector2.ZERO and face.gaze_down_extra==0 and face.smile_eyes==Vector2.ZERO,label+" no invented gaze/blink-smile substitute")
  check(face.mouth_width_sides==Vector2.ZERO and face.mouth_purse==0 and face.mouth_lip_press==0 and face.mouth_oral_lift==0,label+" excluded mouth axes zero")
  for side in ["screen_left","screen_right"]:
   check(not face.effect_objects[side].visible and face.effect_objects[side].modulate.a==0,label+" no source-added blush")
   var b=face.homes["brow_"+side];var control=Vector2(p["brow_"+side],0).x
   # Vector2 addition performs the same float32 stages as production, not Python double math.
   check(b.node.position==b.pivot+Vector2(0,-control*10.0),label+" exact float32 brow height "+side)
  if p.mouth_open==0:
   for joint in face.smile_lip_joints:
    if joint.upper:
     var peer=("mouth_corner_lower_" if joint.corner else "lower_lip_joint_")+str(joint.index)
     check(face.homes[joint.key].node.transform==face.homes[peer].node.transform,label+" exact rigid sealed seam")
 check(face.oral_objects.upper_teeth.position==Vector2(533,626) and face.spread_enamel_roots.position==Vector2(533,629),label+" fixed upper enamel and roots")
 check(not face.mouth_sprite.visible,label+" no whole-mouth proxy")
 for x in range(81):
  var gap=face._smile_lip_offset(x,false,false)-face._smile_lip_offset(x,true,false)
  check(gap>=-.000001 and gap<=30.800001,label+" unchanged bounded aperture")
  if natural:check(gap<=10.10001,label+" bounded114 shallow aperture")
func expectations(spec,label):
 var state=rig.get_state()
 for key in ["auto_blink","auto_blink_pending_restore","active_expression"]:
  if spec.has(key):check(state[key]==spec[key],label+" expected "+key)
 if spec.get("neutral",false):check(rig.pose_now()==rig.neutral_pose() and rig.active_performance=="" and rig.release_time<0,label+" exact idle neutral")
 if spec.has("minimum_closure"):check(rig.face.closure.x>=spec.minimum_closure and rig.face.closure.y>=spec.minimum_closure,label+" expected visible blink")
 if spec.has("maximum_closure"):check(rig.face.closure.x<=spec.maximum_closure and rig.face.closure.y<=spec.maximum_closure,label+" expected open eyes")
 for key in spec.get("controls",{}):
  var wanted=spec.controls[key]
  if key in ["mouth_corner_lift_screen_left","mouth_corner_lift_screen_right"]:wanted=Vector2(wanted,0).x
  check(rig.pose_now()[key]==wanted,label+" exact expected control "+key)
func bridge_record():
 var target={}
 if rig.active_performance!="":target=rig.sample_expression(rig.active_performance,rig.performance_time)
 return {"transition":rig.mouth_transition_state(),"source_pose":rig.restart_pose.duplicate(true),"sampled_target_pose":target,"release_source":rig.release_pose.duplicate(true)}
func anchor_for(chapter,time):
 if not chapter.get("natural_daring",false):return {}
 for anchor in plan.static_checkpoints:
  if time==anchor.time:return anchor
 return {}
func capture(chapter,time,index):
 var label=chapter.name+"_%03d"%index
 invariant(label,chapter.get("natural_daring",false))
 var actual=actual_snapshot();var owners=direct_owners();var face=encoded(rig.face.snapshot())
 var row={"label":label,"chapter":chapter.name,"checkpoint":index,"chapter_elapsed":time,"idle_elapsed":rig.elapsed,"state":rig.get_state(),"public_controls":rig.pose_now(),"expected_player_pose":expected_player_pose(),"mouth_bridge":bridge_record(),"face_state":face,"actual_owners_sha256":record_digest(actual),"direct_owners_sha256":record_digest(owners),"owner_count":owners.size(),"tree_node_count":actual.size()}
 var anchor=anchor_for(chapter,time)
 if not anchor.is_empty():
  row.static_anchor=anchor;row.actual_owners=actual;row.direct_owners=owners
 if failures.is_empty() and not validate_only:
  for view in ["native","bust"]:
   set_view(view)
   row[view]=await capture_image(output+"/"+view+"/"+label+".png")
   if not failures.is_empty():break
  root.size=Vector2i(568,800);root.canvas_transform=Transform2D.IDENTITY
 records.append(row)
func finish():
 var result={"status":"PASS" if failures.is_empty() else "FAIL","checks":checks,"failures":failures,"records":records,"validate_only":validate_only,"actual_renderer_capture":not validate_only,"normal_speed_playback_observed":false,"display_server":DisplayServer.get_name(),"renderer":RenderingServer.get_video_adapter_name(),"plan_sha256":digest(FileAccess.get_file_as_bytes(plan_path)),"profile_sha256":digest(FileAccess.get_file_as_bytes("res://expressions/EXP-114.json")),"harness_sha256":digest(FileAccess.get_file_as_bytes(get_script().resource_path)),"neutral_snapshot":neutral_snapshot,"neutral_face_state":neutral_face_state,"imported_inspection":imported_inspection,"registry_before":registry_before,"registry_after":rig.list_expressions() if rig!=null else []}
 var f=FileAccess.open(output+"/evidence.json",FileAccess.WRITE);f.store_string(JSON.stringify(result,"  "));f.close()
 print("DARING_PROVOCATION_TRAJECTORY_",result.status," checks=",checks," records=",records.size()," failures=",failures.size());quit(0 if failures.is_empty() else 1)
func run():
 for a in OS.get_cmdline_user_args():
  if a=="--validate-only":validate_only=true
  if a=="--coordinator-godot-slot-granted":runtime_lease=true
  if a=="--coordinator-display-lease-granted":display_lease=true
  if a=="--independent-pre-render-review-approved":review_approved=true
  if a.begins_with("--output="):output=a.trim_prefix("--output=")
  if a.begins_with("--plan="):plan_path=a.trim_prefix("--plan=")
 if output.is_empty() or plan_path.is_empty() or not runtime_lease:quit(2);return
 if validate_only and DisplayServer.get_name()!="headless":push_error("Preflight must be headless");quit(2);return
 if not validate_only and (not display_lease or not review_approved or DisplayServer.get_name()=="headless"):push_error("Independent review and separate actual-renderer lease required");quit(2);return
 plan=JSON.parse_string(FileAccess.get_file_as_string(plan_path))
 DirAccess.make_dir_recursive_absolute(output);DirAccess.make_dir_recursive_absolute(output+"/imported_data")
 if not validate_only:
  for view in ["native","bust"]:DirAccess.make_dir_recursive_absolute(output+"/"+view)
 root.size=Vector2i(568,800);root.canvas_transform=Transform2D.IDENTITY
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 check(rig.rig_ready and rig.registry_ready,"ready")
 if not rig.rig_ready or not rig.registry_ready:finish();return
 rig.hud.hide();rig.hint.hide();rig.pose_status.hide();full_head=rig.head.transform;full_body=rig.body.transform;full_rig=rig.transform
 check(full_head==full_body and rig.head.position==Vector2(6,70) and rig.head.scale==Vector2(.49,.49),"canonical .49 bust presentation")
 rig.reset();registry_before=rig.list_expressions();check(registry_before.size()==19,"nineteen registered, eighteen approved")
 for key in rig.face.objects:
  textures[key]=fingerprint(rig.face.objects[key])
  if key.begins_with("hair_") or key in ["face_base","face_skin","nose","ear_screen_left","ear_screen_right"]:fixed_owners[key]=owner_record(key)
 neutral_snapshot=actual_snapshot();neutral_face_state=encoded(rig.face.snapshot());inspect_node_textures(rig)
 for chapter in plan.chapters:
  if not failures.is_empty():break
  if chapter.get("reset",true):check(rig.reset(),"chapter reset")
  for command in chapter.setup:
   if command.has("advance"):check(rig.advance(command.advance),"setup advance")
   else:
    var before=rig.displayed_pose();check(rig.apply_controls(command),"setup command "+str(command))
    if command.has("perform_expression") or command.get("release_performance",false):check(rig.displayed_pose()==before,"C0 trigger/release "+chapter.name)
  var last=0.0
  for index in range(chapter.times.size()):
   if not failures.is_empty():break
   var time=float(chapter.times[index]);check(time>=last,"ordered chapter clock")
   check(rig.advance(time-last),"advance "+chapter.name);last=time
   if chapter.has("expected_expression") and time<rig.registry.definition(chapter.expected_expression).duration:check(rig.active_performance==chapter.expected_expression,"actual requested expression "+chapter.name)
   if chapter.get("mode","")=="release":check(rig.active_performance=="","release has no active expression")
   if chapter.has("expected_bridge_mode") and rig.active_performance!="":
    check(rig.mouth_transition_state().mode==chapter.expected_bridge_mode,"fixed expected bridge mode "+chapter.name)
    check(rig.mouth_transition_state().duration==.30,"fixed bridge duration")
    if chapter.expected_bridge_mode=="staged" and time==.15:
     var p=rig.pose_now();check(p.mouth_open==0 and p.mouth_width_screen_left==0 and p.mouth_width_screen_right==0,"explicit zero trio separator")
   if chapter.get("assertions",{}).has(str(index)):expectations(chapter.assertions[str(index)],chapter.name+" checkpoint "+str(index))
   await capture(chapter,time,index)
  expectations(chapter.get("final_expect",{}),chapter.name+" final")
  print("DARING_CAPTURED ",chapter.name," records=",records.size())
 check(rig.reset(),"final public reset")
 check(actual_snapshot()==neutral_snapshot and encoded(rig.face.snapshot())==neutral_face_state,"exact owner/material/head/body canonical neutral restoration")
 if failures.is_empty():check(records.size()==int(plan.checkpoints),"all planned checkpoints")
 finish()

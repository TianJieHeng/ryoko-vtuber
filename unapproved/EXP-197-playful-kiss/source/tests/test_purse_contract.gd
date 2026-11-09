extends SceneTree
## Geometry/state contract only. Does not certify rendered silhouettes or connect services.
const AXIS="mouth_purse"
const IDS=["EXP-163","EXP-005","EXP-001","EXP-006","EXP-107","EXP-007"]
const PURSE_VALUES=[0.0,.000001,.3,.7,1.0]
const OPEN_VALUES=[0.0,.000001,.2,.6,1.0]
const MOUTH_SHADERS=["res://object_mouth_clip.gdshader","res://smile_lip_segment.gdshader","res://smile_lip_join.gdshader","res://pressed_lip_clip.gdshader","res://spread_teeth_clip.gdshader"]
const FIXED_UNIFORMS=["seam_texture","profile_texture","lower_profile_texture","aperture_texture","iris_texture","skin_texture","owner_texture","original_texture","hair_texture","previous_sleeve_texture","atlas_origin_px","previous_atlas_origin_px","source_x","source_center","left_edge","right_edge","corner","upper_lip","origin","joint_center","half_width","outer_extension","left_side","lip","underlip_shadow"]
const PIXEL_TOLERANCE=.0001
var rig
var checks=0
var failures=[]
var geometry_poses=0
var grid_poses=0
var context="startup"
var immutable={}
var fixed_transforms={}
var all_uniform_names={}
var mouth_nodes=[]
var head_transform:Transform2D
var body_transform:Transform2D
var face_transform:Transform2D
var root_transform:Transform2D
var result_path=""
var boundary_observations=[]
func _initialize():
    for argument in OS.get_cmdline_user_args():
        if argument.begins_with("--contract-results="):result_path=argument.trim_prefix("--contract-results=")
    call_deferred("run")
func check(ok:bool,label:String):
    checks+=1
    if not ok:
        var message=context+": "+label
        if failures.size()<20:push_error("PURSE_CONTRACT "+message)
        failures.append(message)
func close(a:float,b:float)->bool:return absf(a-b)<=PIXEL_TOLERANCE
func texture_signature(node:Sprite2D)->Array:
    var value=[node.texture,node.centered,node.offset,node.flip_h,node.flip_v,node.region_enabled,node.region_rect,node.hframes,node.vframes,node.frame_coords,node.texture_filter,node.texture_repeat]
    if node.texture is AtlasTexture:
        value.append_array([node.texture.atlas,node.texture.region,node.texture.margin,node.texture.filter_clip])
    return value
func source_signature(key:String)->Array:
    var node=rig.face.objects[key]
    var value=texture_signature(node)
    value.append(node.material)
    if node.material is ShaderMaterial:
        value.append(node.material.shader)
        for name in immutable.get(key,{}).get("fixed_uniform_names",[]):
            value.append(node.material.get_shader_parameter(name))
    return value
func remember_sources():
    root_transform=rig.transform;head_transform=rig.head.transform;body_transform=rig.body.transform;face_transform=rig.face.transform
    for key in rig.face.objects:
        var node=rig.face.objects[key];var fixed_names=[];var names=[]
        if node.material is ShaderMaterial and node.material.shader!=null:
            for uniform in node.material.shader.get_shader_uniform_list():
                names.append(uniform.name)
                if uniform.name in FIXED_UNIFORMS:fixed_names.append(uniform.name)
            if node.material.shader.resource_path in MOUTH_SHADERS:mouth_nodes.append(node)
        all_uniform_names[key]=names
        immutable[key]={"fixed_uniform_names":fixed_names,"sprite_color":node.modulate,"sprite_self_color":node.self_modulate,"pivot_color":rig.face.homes[key].node.modulate,"pivot_self_color":rig.face.homes[key].node.self_modulate}
        immutable[key].source=source_signature(key)
    for key in ["stationary_backing","neutral_lips","hair_front_fringe"]:
        fixed_transforms[key]=rig.face.homes[key].node.transform
func verify_shader_source_contract():
    var mutation=RegEx.new();mutation.compile("\\b(?:UV|VERTEX)\\s*(?:[+*/-]=|=(?!=))")
    var whitespace=RegEx.new();whitespace.compile("\\s+")
    for path in MOUTH_SHADERS:
        var source=FileAccess.get_file_as_string(path)
        var compact=whitespace.sub(source,"",true)
        check("texture(TEXTURE,UV)" in compact,"fixed native pigment sampling "+path)
        check(mutation.search(source)==null,"no source UV or vertex assignment "+path)
        check("voidvertex(" not in compact,"no shader vertex deformation "+path)
    check(rig.face.MAX_MOUTH_APERTURE==.55,"unchanged physical aperture multiplier")
    var segment=FileAccess.get_file_as_string("res://smile_lip_segment.gdshader")
    check("float boundary_intrusion" in segment and "length(direction)" in segment,"oriented finite-distance boundary clipping")
    check("max(.001,neighbor_left_bottom.y-neighbor_left_top.y)" not in segment,"no positive-only vertical denominator")
func assert_geometry():
    geometry_poses+=1
    var face=rig.face;var pose=rig.pose_now()
    check(rig.transform==root_transform and rig.head.transform==head_transform and rig.body.transform==body_transform and face.transform==face_transform,"fixed root/head/body/face registration")
    check(rig.body.modulate==Color.WHITE and rig.head.modulate==Color.WHITE and face.modulate==Color.WHITE,"opaque body/head/face")
    check(face.oral_objects.upper_teeth.position==Vector2(533,626) and face.oral_objects.upper_teeth.rotation==0.0,"fixed central enamel anchor")
    check(face.mouth_purse==pose[AXIS] and face.mouth_opening==pose.mouth_open,"bounded coordinates reach geometry")
    check(face.mouth_purse>=0.0 and face.mouth_purse<=1.0 and face.mouth_opening>=0.0 and face.mouth_opening<=1.0,"finite normalized controls")
    check(close(face.mouth_spread,pose.mouth_smile*pose.mouth_spread),"unchanged spread coupling")
    for key in face.objects:
        var node=face.objects[key];var pivot=face.homes[key].node;var saved=immutable[key]
        check(source_signature(key)==saved.source,"immutable texture/UV/Atlas/static uniforms "+key)
        check(node.scale==Vector2.ONE and pivot.scale==Vector2.ONE,"unit sprite/pivot scale "+key)
        check(node.modulate==saved.sprite_color and node.self_modulate==saved.sprite_self_color and pivot.modulate==saved.pivot_color and pivot.self_modulate==saved.pivot_self_color,"unchanged anatomical opacity/color "+key)
        check(node.modulate.a==1.0 and node.self_modulate.a==1.0 and pivot.modulate.a==1.0 and pivot.self_modulate.a==1.0,"fully opaque anatomical owners "+key)
        check(node.position.is_finite() and pivot.position.is_finite() and is_finite(node.rotation) and is_finite(pivot.rotation),"finite rigid transforms "+key)
        check(close(node.transform.determinant(),1.0) and close(pivot.transform.determinant(),1.0),"no transform stretch/shear "+key)
    var physical=pose.mouth_open*.55
    check(physical>=0.0 and physical<=.55 and 56.0*physical<=30.800001,"total physical aperture cap")
    for node in mouth_nodes:
        var opening=node.material.get_shader_parameter("opening")
        check(opening!=null and close(opening,physical),"shared bounded shader opening "+str(node.name))
        check(close(node.material.get_shader_parameter("purse"),pose[AXIS]),"shared shader purse coordinate "+str(node.name))
    for joint in face.smile_lip_joints:
        var pivot=face.homes[joint.key].node
        var baseline_x=face.homes[joint.key].pivot.x+20.0*face.mouth_spread*(joint.center-39.5)/35.5
        var inward=-14.0*pose[AXIS]*(joint.center-39.5)/35.5
        check(close(pivot.position.x,baseline_x+inward),"rigid inward lip pivot "+joint.key)
        check((pivot.position.x-baseline_x)*signf(joint.center-39.5)<=PIXEL_TOLERANCE,"purse never moves lip pivots outward "+joint.key)
    var half_width=lerpf(38.0-12.0*physical,35.5,face.smile_mouth)+20.0*face.mouth_spread-14.0*face.mouth_purse
    check(half_width>0.0 and is_finite(half_width),"positive finite cavity half-width")
    for x in range(81):
        var upper=face._smile_lip_offset(float(x),true,false)
        var lower=face._smile_lip_offset(float(x),false,false)
        var gap=lower-upper
        check(is_finite(upper) and is_finite(lower) and gap>=-.000001 and gap<=30.800001,"nonnegative bounded relative lip gap x="+str(x))
        check(gap<=54.0*physical+.000001,"relative lip gap respects opening-specific cap x="+str(x))
        var h=clampf(abs(float(x)-39.5)/half_width,0.0,1.0)
        var curve=lerpf(sqrt(maxf(0.0,1.0-pow(h,4.0))),pow(maxf(0.0,1.0-h*h),.72),face.smile_mouth)
        if face.mouth_purse>0.0:curve=lerpf(curve,sqrt(maxf(0.0,1.0-h*h)),face.mouth_purse)
        var aperture=56.0*physical*curve
        check(is_finite(aperture) and aperture>=0.0 and aperture<=30.800001,"spatial cavity aperture envelope x="+str(x))
func complete_snapshot()->Dictionary:
    var state=rig.get_state();state.erase("last_error")
    state.current=rig.current_pose.duplicate(true);state.restart=rig.restart_pose.duplicate(true)
    state.release=rig.release_pose.duplicate(true);state.performance=rig.performance.duplicate(true)
    state.elapsed=rig.elapsed;state.oral_mode=rig.oral_mode
    state.root=rig.transform;state.head=rig.head.transform;state.body=rig.body.transform;state.face=rig.face.snapshot()
    state.geometry={}
    for key in rig.face.objects:
        var node=rig.face.objects[key];var pivot=rig.face.homes[key].node;var uniforms=[]
        for name in all_uniform_names[key]:uniforms.append(node.material.get_shader_parameter(name))
        state.geometry[key]=[node.transform,pivot.transform,node.visible,pivot.visible,node.modulate,node.self_modulate,pivot.modulate,pivot.self_modulate,source_signature(key),uniforms]
    state.effects={}
    for key in rig.face.effect_objects:
        var node=rig.face.effect_objects[key]
        state.effects[key]=[node.transform,node.visible,node.modulate,node.self_modulate,texture_signature(node)]
    return state
func idle_neutral()->bool:
    return rig.active_performance=="" and rig.release_time<0.0 and rig.pose_now()==rig.neutral_pose()
func neutral(label:String,blink_enabled:bool=false):
    check(rig.pose_now()==rig.neutral_pose() and rig.displayed_pose()==rig.neutral_pose(),label+" exact neutral coordinates")
    check(rig.active_performance=="" and rig.release_time<0.0,label+" no stale performance/release")
    check(rig.auto_blink==blink_enabled,label+" expected auto-blink preference")
    assert_geometry()
func run_grid():
    for purse in PURSE_VALUES:
     for opening in OPEN_VALUES:
      for smile in [0.0,.3,1.0]:
       for spread in [0.0,.5,1.0]:
        for corner in [0.0,1.0]:
         for pressure in [0.0,1.0]:
          for oral_lift in [0.0,1.0]:
            context="grid p=%.6f o=%.6f s=%.6f w=%.6f c=%.6f press=%.6f oral=%.6f"%[purse,opening,smile,spread,corner,pressure,oral_lift]
            check(rig.apply_controls({"reset":true,AXIS:purse,"mouth_open":opening,"mouth_smile":smile,"mouth_spread":spread,"mouth_corner_lift":corner,"mouth_lip_press":pressure,"mouth_oral_lift":oral_lift}),"bounded grid accepted")
            assert_geometry();grid_poses+=1
            for key in fixed_transforms:check(rig.face.homes[key].node.transform==fixed_transforms[key],"mouth grid leaves non-mouth owner fixed "+key)
    context="grid totals";check(grid_poses==1800,"complete requested Cartesian grid")
    print("PURSE_CONTRACT_GRID poses=",grid_poses," checks=",checks," failures=",failures.size())
func run_atomicity():
    for id in IDS:
     for mode in ["manual","active","release"]:
        rig.reset();rig.apply_controls({AXIS:.7,"mouth_open":.6,"mouth_smile":.3,"mouth_spread":.5,"mouth_corner_lift":1.0,"mouth_lip_press":1.0,"mouth_oral_lift":1.0,"blush_intensity":.4})
        if mode!="manual":rig.play_expression(id);rig.advance(.12)
        if mode=="release":rig.release();rig.advance(.1)
        for invalid in [-.000001,1.000001,NAN,INF,-INF,true,false,"0.5",null,{},[]]:
            context="atomic "+id+" "+mode+" invalid="+str(invalid)
            var before=complete_snapshot()
            check(not rig.apply_controls({"reset":true,AXIS:invalid,"mouth_open":.2,"blink":.4}),"invalid purse rejected")
            check(complete_snapshot()==before,"invalid purse leaves all state/geometry/uniforms unchanged")
        context="mixed atomic "+id+" "+mode
        var before=complete_snapshot()
        check(not rig.apply_controls({AXIS:.3,"blink":true}),"valid purse plus invalid legacy field rejected")
        check(complete_snapshot()==before,"mixed invalid transaction preserves geometry")
        assert_geometry()
func run_lifecycle():
    for id in IDS:
     var duration=rig.registry.definition(id).duration
     for t in [0.0,.000001,.1,.299999,.3,duration*.45,duration-.000001]:
      for action in ["release","reset","retrigger","manual"]:
        context="lifecycle "+id+" "+action+" t="+str(t)
        rig.reset();rig.apply_controls({AXIS:.7,"mouth_open":.6,"mouth_smile":.3,"mouth_spread":.5,"mouth_corner_lift":1.0,"mouth_lip_press":1.0,"mouth_oral_lift":1.0})
        var before=rig.displayed_pose();rig.play_expression(id)
        check(rig.displayed_pose()==before,"incoming purse control C0")
        rig.advance(t);assert_geometry();before=rig.displayed_pose()
        if action=="release":
            rig.release();check(rig.displayed_pose()==before,"release C0")
            rig.advance(.15);assert_geometry();rig.advance(rig.RELEASE_SECONDS-rig.release_time)
        elif action=="reset":rig.reset()
        elif action=="retrigger":
            rig.play_expression(id);check(rig.displayed_pose()==before,"retrigger C0")
            rig.advance(.05);rig.release();rig.advance(.12);before=rig.displayed_pose()
            rig.play_expression(id);check(rig.displayed_pose()==before,"retrigger during release C0")
            rig.advance(.17);assert_geometry();rig.advance(duration)
        else:
            rig.apply_controls({AXIS:.3});check(rig.active_performance=="" and rig.release_time<0 and rig.face.owners.mouth=="manual","manual purse takeover")
            rig.advance(.7);check(rig.pose_now()[AXIS]==.3,"manual pose cannot resume stale playback");assert_geometry();rig.reset()
        neutral(action)
    # Every ordered pair exercises both incoming and outgoing six-profile handovers.
    for source in IDS:
     for destination in IDS:
        context="handover "+source+" to "+destination
        rig.reset();rig.apply_controls({AXIS:.7,"mouth_open":.6});rig.play_expression(source);rig.advance(.12)
        var before=rig.displayed_pose();rig.play_expression(destination)
        check(rig.displayed_pose()==before,"cross-profile C0")
        rig.advance(.15);assert_geometry();rig.advance(rig.registry.definition(destination).duration)
        neutral("cross-profile completion")
func run_prior_profiles():
    for id in IDS:
     var definition=rig.registry.definition(id)
     if id not in ["EXP-007","EXP-160"]:
        for frame in definition.keyframes:check(not frame.values.has(AXIS),"prior profile does not author purse "+id)
     for hz in [30,60]:
        context="profile "+id+" hz="+str(hz)
        rig.reset();rig.play_expression(id)
        for i in range(int(ceil(definition.duration*hz))+1):
            if id not in ["EXP-007","EXP-160"]:
                check(rig.sample_expression(id,minf(float(i)/hz,definition.duration))[AXIS]==0.0,"prior samples exact zero purse")
                check(rig.pose_now()[AXIS]==0.0 and rig.face.mouth_purse==0.0,"prior playback exact zero purse")
            # Keep full source/geometry checks at every tenth frame plus each end.
            if i%10==0 or i==int(ceil(definition.duration*hz)):assert_geometry()
            rig.advance(1.0/hz)
        neutral("profile completion")
func run_eye_restoration():
    # Explicit closed laughing-eye input is independent of a profile's timed key.
    for eye_values in [Vector2.ONE,Vector2(1,0),Vector2(0,1)]:
      context="closed laughing-eye incoming "+str(eye_values)
      rig.reset();rig.apply_controls({AXIS:.7,"mouth_open":.6,"eye_smile_R":eye_values.x,"eye_smile_L":eye_values.y})
      var visible_laugh=0
      for joint in rig.face.smile_eye_joints:
        if not joint.old and rig.face.objects[joint.key].visible:visible_laugh+=1
      check(visible_laugh>0,"incoming laughing-eye owners actually visible")
      var before=rig.displayed_pose();rig.play_expression("EXP-007")
      check(rig.displayed_pose()==before,"closed-eye incoming C0")
      for step in range(19):rig.advance(1.0/60.0);assert_geometry()
      check(rig.pose_now().eye_smile_R==0.0 and rig.pose_now().eye_smile_L==0.0,"relief clears laughing-eye coordinates after restart")
      for joint in rig.face.smile_eye_joints:check(not rig.face.objects[joint.key].visible,"ordinary eye ownership restored "+joint.key)
      for key in rig.face.manifest.objects:
        if rig.face.manifest.objects[key].get("eye_role",0)==4:check(rig.face.objects[key].visible,"ordinary closed-lash owner available "+key)
      rig.advance(3.2);neutral("closed-eye recovery")
func run_release_threshold():
    for id in IDS:
        context="release threshold "+id
        rig.reset();rig.play_expression(id);rig.advance(.6);rig.release()
        rig.advance(rig.RELEASE_SECONDS-.000001)
        check(rig.active_performance=="" and rig.release_time>=0.0 and rig.release_time<rig.RELEASE_SECONDS,"deliberately below threshold remains releasing")
        check(not idle_neutral(),"near-neutral coordinates alone do not permit restoration")
        assert_geometry()
        rig.advance(.000002);neutral("next small advance completes release")
        # Preserve the inherited double-precision boundary as an explicit
        # observation, rather than claiming .15+.30 has reached the threshold.
        rig.apply_controls({AXIS:.7,"mouth_open":.6});rig.release()
        rig.advance(.15);rig.advance(.30)
        var remaining=rig.RELEASE_SECONDS-rig.release_time
        check(remaining>0.0 and remaining<.000000000001,"split .15+.30 is one rounding step below threshold")
        check(rig.active_performance=="" and rig.release_time>=0.0 and not idle_neutral(),"rounded-neutral split release is not yet idle")
        boundary_observations.append({"expression":id,"split_release_time":rig.release_time,"threshold":rig.RELEASE_SECONDS,"remaining_seconds":remaining,"pose_coordinates_neutral":rig.pose_now()==rig.neutral_pose(),"idle":idle_neutral()})
        rig.advance(remaining);neutral("exact remaining interval completes release")
func run_blink_restoration():
    for id in IDS:
     for ending in ["complete","release"]:
        context="auto-blink "+id+" "+ending
        rig.reset();rig.apply_controls({"auto_blink":true});rig.advance(4.03)
        check(rig.face.closure.x>.99,"incoming manual blink is visibly closed")
        var before=rig.displayed_pose();rig.play_expression(id)
        check(rig.displayed_pose()==before and not rig.auto_blink,"trigger captures blink and intentionally disables auto-blink")
        if ending=="complete":rig.advance(rig.registry.definition(id).duration)
        else:rig.advance(.6);rig.release();rig.advance(.45)
        neutral("after automatic neutral recovery",true)
        check(idle_neutral(),"all three idle predicates required before restoration")
        if not idle_neutral():continue
        check(rig.apply_controls({"auto_blink":true}) and rig.auto_blink,"explicit auto-blink restoration needs no reset")
        check(rig.active_performance=="" and rig.release_time<0,"restored auto-blink remains manual idle")
        rig.advance(0.0);check(rig.face.closure==Vector2.ZERO,"restored auto-blink starts open without a stale-clock jump")
        rig.advance(4.03);check(rig.face.closure.x>.99,"restored auto-blink closes using the existing cycle")
    context="early blink is takeover"
    rig.reset();rig.play_expression("EXP-007");rig.advance(.6);rig.release();rig.advance(.1)
    var before=rig.pose_now()
    check(rig.apply_controls({"auto_blink":true}),"early auto-blink is valid manual action")
    check(rig.active_performance=="" and rig.release_time<0 and rig.pose_now()==before,"early blink cancels release instead of promising automatic recovery")
    rig.advance(.6);check(rig.pose_now()==before,"interrupted release does not silently continue")
    rig.reset();neutral("final reset")
func run_reversed_boundary_regression():
    var negative=0
    for smile in [0.0,.5]:
        var centers=[.702,.70225,.7025,.70275,.703,.75,1.0] if smile==0.0 else [.917,.91725,.9175,.91775,.918,.95,1.0]
        for center in centers:
            var previous={}
            for epsilon in [-.000001,0.0,.000001]:
                var purse=clampf(center+epsilon,0.0,1.0)
                context="reversed boundary smile="+str(smile)+" purse="+str(purse)
                rig.reset();check(rig.apply_controls({"mouth_open":1.0,"mouth_smile":smile,"mouth_purse":purse,"mouth_lip_press":1.0,"mouth_oral_lift":.8}),"valid public mixed-control pose")
                for key in ["mouth_corner_lower_0","lower_lip_joint_1"]:
                    var mat=rig.face.objects[key].material
                    for side in ["left","right"]:
                        var a:Vector2=mat.get_shader_parameter("neighbor_"+side+"_top")
                        var b:Vector2=mat.get_shader_parameter("neighbor_"+side+"_bottom")
                        var direction=b-a
                        check(absf(direction.length()-45.0)<.001,"fixed-length rigid clipping edge")
                        if direction.y<0.0:negative+=1
                        var edge:float=mat.get_shader_parameter(side+"_edge")
                        for y in [0.0,14.0,20.0,31.0,45.0]:
                            var query=Vector2(edge,y)-a
                            var sign_value=1.0 if side=="left" else -1.0
                            var intrusion=sign_value*(direction.x*query.y-direction.y*query.x)/maxf(.001,direction.length())
                            check(is_finite(intrusion),"finite oriented intrusion through horizontal/reversed edge")
                            var label=key+side+str(y)
                            if previous.has(label):check(absf(intrusion-previous[label])<.02,"continuous normal-distance intrusion for one-millionth purse step")
                            previous[label]=intrusion
    check(negative>0,"regression actually covers reversed boundaries")
    rig.reset()
func run():
    rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
    check(rig.rig_ready and rig.registry_ready,"required assets and registry ready")
    if not rig.rig_ready or not rig.registry_ready:quit(2);return
    var ids=[]
    for entry in rig.list_expressions():ids.append(entry.id)
    check(ids==["EXP-163","EXP-005","EXP-001","EXP-006","EXP-107","EXP-007","EXP-002","EXP-152","EXP-160","EXP-177","EXP-164","EXP-021","EXP-158","EXP-181","EXP-102","EXP-116","EXP-050","EXP-186"],"exact eighteen approved registry IDs")
    remember_sources();verify_shader_source_contract()
    run_grid();run_reversed_boundary_regression();run_atomicity();run_lifecycle();run_prior_profiles();run_eye_restoration();run_release_threshold();run_blink_restoration()
    var result={"status":"PASS" if failures.is_empty() else "FAIL","checks":checks,"grid_poses":grid_poses,"geometry_poses":geometry_poses,"failures":failures,"release_boundary_observations":boundary_observations,"scope":"geometry/state invariants; no rendered silhouette certification or external services"}
    if result_path!="":
        var file=FileAccess.open(result_path,FileAccess.WRITE)
        if file==null:push_error("Cannot write purse contract result: "+result_path);quit(2);return
        file.store_string(JSON.stringify(result,"  ")+"\n");file.close()
    print("PURSE_CONTRACT checks=",checks," grid_poses=",grid_poses," geometry_poses=",geometry_poses," failures=",failures.size())
    quit(1 if failures.size() else 0)

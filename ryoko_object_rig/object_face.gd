extends Node2D
## Reusable base assembly. Independent rigid objects; no emotion playback.
const GazeLimits=preload("res://control_limits.gd")
var gaze_manifest:Dictionary
var manifest:Dictionary
var objects:Dictionary={}
var homes:Dictionary={}
var closure=Vector2.ZERO
var gaze=Vector2.ZERO
var gaze_down_extra=0.0
var brow=Vector2.ZERO
var brow_tilt=Vector2.ZERO
var brow_inner_lift=Vector2.ZERO
var hair_sway=0.0
var mouth_variant="neutral_lips"
const MAX_MOUTH_APERTURE=0.55
var mouth_opening=0.0
var mouth_sprite:Sprite2D
var owners={"eyes":"base_control","brows":"base_control","mouth":"base_control","hair":"base_control"}
var oral_objects:Dictionary={}
var oral_homes:Dictionary={}
var oral_manifest:Dictionary

var smile_eyes=Vector2.ZERO
var smile_mouth=0.0
var mouth_spread=0.0
var mouth_corner_lift=0.0
var mouth_lip_press=0.0
var mouth_oral_lift=0.0
var mouth_purse=0.0
var pressed_lip_owners:Array=[]
var blush_intensity=0.0
var effect_owner="manual"
var effect_objects:Dictionary={}
var blush_manifest:Dictionary={}
var spread_cavity:Array=[]
var spread_teeth:Array=[]
var spread_joint_extensions:Dictionary={}
var spread_tongue:Sprite2D
var spread_enamel_roots:Sprite2D
var smile_manifest:Dictionary
var smile_lip_joints:Array=[]
var smile_eye_joints:Array=[]
var smile_lip_continuations:Array=[]
var neutral_residue_objects:Array=[]


var ready_for_controls=false
var asset_error=""
func _ready():
    if not _verify_required_textures():return
    manifest=JSON.parse_string(FileAccess.get_file_as_string("res://rig_assets/object_face/manifest.json"))
    gaze_manifest=JSON.parse_string(FileAccess.get_file_as_string("res://rig_assets/gaze_eyes/manifest.json"))
    for key in gaze_manifest.get("foreground_objects",{}):
        manifest.objects[key]=gaze_manifest.foreground_objects[key].duplicate(true)
    # Original object-face PNGs remain reproducible immutable inputs. Only the
    # four eye-interior sprites select the explicitly labelled gaze derivatives.
    for side in ["screen_left","screen_right"]:
        var ge=gaze_manifest.eyes[side]
        for kind in ["iris","sclera"]:
            var entry=manifest.objects[kind+"_"+side]
            entry.file="../gaze_eyes/"+kind+"_"+side+".png"
            entry.eye_role=7 if kind=="iris" else 6
            if kind=="iris":entry.xy=ge.iris_origin;entry.size=ge.iris_size
    for key in manifest.objects:
        var e=manifest.objects[key]
        if key.begins_with("closed_reference") or key.begins_with("viseme_"):continue
        var node=Sprite2D.new();node.name=key;node.texture=load("res://rig_assets/object_face/"+e.file);node.centered=false
        var pivot=Node2D.new();pivot.name=key+"_pivot";pivot.position=Vector2(e.pivot[0],e.pivot[1]);pivot.z_index=int(e.z)
        node.position=Vector2(e.xy[0],e.xy[1])-pivot.position;pivot.add_child(node);add_child(pivot)
        objects[key]=node;homes[key]={"xy":Vector2(e.xy[0],e.xy[1]),"pivot":pivot.position,"node":pivot}
        if e.has("eye_role"):
            var material=ShaderMaterial.new();material.shader=load("res://canonical_eye_alpha.gdshader")
            material.set_shader_parameter("profile_texture",load("res://rig_assets/object_face/"+e.eye_profile))
            material.set_shader_parameter("lower_profile_texture",load("res://rig_assets/object_face/"+e.eye_lower_profile))
            material.set_shader_parameter("role",int(e.eye_role))
            if int(e.eye_role) in [6,7]:
                var ge=gaze_manifest.eyes[e.eye_side]
                material.set_shader_parameter("eye_size",Vector2(ge.size[0],ge.size[1]))
                material.set_shader_parameter("iris_size",Vector2(ge.iris_size[0],ge.iris_size[1]))
                material.set_shader_parameter("iris_padding",Vector2(ge.iris_padding[0],ge.iris_padding[1]))
                material.set_shader_parameter("sprite_origin",Vector2(-ge.iris_padding[0],-ge.iris_padding[1]) if int(e.eye_role)==7 else Vector2.ZERO)
                material.set_shader_parameter("aperture_texture",load("res://rig_assets/gaze_eyes/aperture_"+e.eye_side+".png"))
                material.set_shader_parameter("iris_texture",load("res://rig_assets/gaze_eyes/iris_"+e.eye_side+".png"))
            node.material=material
    for side in ["screen_left","screen_right"]:
        objects["iris_"+side].visibility_changed.connect(_update_iris_visibility.bind(side))
    mouth_sprite=Sprite2D.new();mouth_sprite.name="active_viseme";mouth_sprite.centered=false;mouth_sprite.z_index=55;add_child(mouth_sprite)
    objects.active_viseme=mouth_sprite;homes.active_viseme={"xy":Vector2.ZERO,"pivot":Vector2.ZERO,"node":mouth_sprite}
    _build_oral_objects()
    _build_smile_objects()
    _build_spread_objects()
    if not _build_blush_objects():return
    ready_for_controls=true
    set_pose(Vector2.ZERO,Vector2.ZERO,Vector2.ZERO,Vector2.ZERO,"neutral",0.0)
func _update_iris_visibility(side:String):
    objects["sclera_"+side].material.set_shader_parameter("iris_present",objects["iris_"+side].visible)
func set_pose(lids:Vector2,eye_gaze:Vector2,brows:Vector2,brow_angles:Vector2,shape:String,hair_value:float,down_extra:float=0.0,inner_lift:Vector2=Vector2.ZERO):
    if not ready_for_controls:return
    closure=lids.clamp(Vector2.ZERO,Vector2.ONE);gaze=eye_gaze.clamp(Vector2(GazeLimits.GAZE_MIN,GazeLimits.GAZE_MIN),Vector2(GazeLimits.GAZE_MAX,GazeLimits.GAZE_MAX))
    gaze_down_extra=clampf(down_extra,0.0,1.0)
    var gaze_offset=GazeLimits.gaze_pixels(gaze,gaze_down_extra)
    brow=brows.clamp(-Vector2.ONE,Vector2.ONE);brow_tilt=brow_angles.clamp(-Vector2.ONE,Vector2.ONE)*deg_to_rad(8)
    brow_inner_lift=inner_lift.clamp(Vector2.ZERO,Vector2.ONE)
    for side in ["screen_left","screen_right"]:
        var index=0 if side=="screen_left" else 1
        for key in manifest.objects:
            var e=manifest.objects[key]
            if e.get("eye_side","")==side and e.has("eye_role"):
                objects[key].material.set_shader_parameter("closure",closure[index])
                if int(e.eye_role)==1:homes[key].node.position=homes[key].pivot+Vector2(0,36.0*closure[index])
                if int(e.eye_role) in [6,7]:
                    objects[key].material.set_shader_parameter("rigid_gaze",gaze_offset)
                    if int(e.eye_role)==7:homes[key].node.position=homes[key].pivot+gaze_offset
        var key="brow_"+side
        var legacy_angle=brow_tilt[index]
        var lift_angle=(-1.0 if index==0 else 1.0)*deg_to_rad(GazeLimits.BROW_INNER_LIFT_DEGREES)*brow_inner_lift[index]
        # Preserve every published default-zero transform exactly. The new rigid
        # rotation is about the tail after legacy tilt and vertical translation.
        homes[key].node.position=homes[key].pivot+Vector2(0,-brow[index]*10)
        homes[key].node.rotation=legacy_angle
        if brow_inner_lift[index]>0.0:
            var anchor_offset=GazeLimits.BROW_OUTER_ANCHORS[side]-homes[key].pivot
            homes[key].node.position+=(anchor_offset-anchor_offset.rotated(lift_angle)).rotated(legacy_angle)
            homes[key].node.rotation=legacy_angle+lift_angle
    _write_mouth(shape);set_hair_sway(hair_value)
func _write_mouth(shape:String):
    for key in oral_objects:oral_objects[key].visible=false
    mouth_variant="neutral_lips" if shape=="neutral" else "viseme_"+shape
    mouth_opening=0.0 if shape=="neutral" else 1.0
    objects.neutral_lips.visible=shape=="neutral";mouth_sprite.visible=shape!="neutral"
    if shape=="neutral":return
    var e=manifest.objects[mouth_variant]
    mouth_sprite.texture=load("res://rig_assets/object_face/"+e.file)
    mouth_sprite.position=Vector2(e.xy[0],e.xy[1])
func set_hair_sway(value:float):
    hair_sway=clamp(value,-1,1)
    for key in manifest.objects:
        var e=manifest.objects[key]
        if e.has("hair_angle"):
            homes[key].node.rotation=deg_to_rad(float(e.hair_angle))*hair_sway
func snapshot()->Dictionary:
    var transforms={}
    for key in objects:
        var p=homes[key].node
        transforms[key]={"position":[p.position.x,p.position.y],"rotation":p.rotation,"scale":[p.scale.x,p.scale.y],"opacity":objects[key].modulate.a,"visible":objects[key].visible}
    return {"owners":owners.duplicate(),"closure":[closure.x,closure.y],"gaze":[gaze.x,gaze.y],"gaze_down_extra":gaze_down_extra,"mouth_variant":mouth_variant,"mouth_opening":mouth_opening,"eye_smile":[smile_eyes.x,smile_eyes.y],"mouth_smile":smile_mouth,"effective_mouth_spread":mouth_spread,"mouth_corner_lift":mouth_corner_lift,"mouth_lip_press":mouth_lip_press,"mouth_oral_lift":mouth_oral_lift,"mouth_purse":mouth_purse,"hair_sway":hair_sway,"objects":transforms,"blush_intensity":blush_intensity,"effects":_effect_snapshot()}

func _build_oral_objects():
    oral_manifest=JSON.parse_string(FileAccess.get_file_as_string("res://rig_assets/yawn_mouth/manifest.json"))
    for key in oral_manifest.objects:
        var e=oral_manifest.objects[key]
        var node=Sprite2D.new();node.name="oral_"+key;node.centered=false;node.z_index=int(e.z)
        node.texture=load("res://rig_assets/yawn_mouth/"+e.file);node.position=Vector2(e.xy[0],e.xy[1])
        add_child(node)
        oral_objects[key]=node;oral_homes[key]=node.position
        objects["oral_"+key]=node;homes["oral_"+key]={"xy":node.position,"pivot":node.position,"node":node}
        if true:
            var material=ShaderMaterial.new();material.shader=load("res://object_mouth_clip.gdshader")
            material.set_shader_parameter("origin",node.position)
            material.set_shader_parameter("seam_texture",load("res://rig_assets/yawn_mouth/neutral_seam.png"))
            material.set_shader_parameter("lip",key in ["upper_lip","lower_lip","underlip_shadow"])
            material.set_shader_parameter("upper_lip",key=="upper_lip")
            material.set_shader_parameter("underlip_shadow",key=="underlip_shadow")
            node.material=material
        node.visible=false
func set_mouth_open(value:float):
    mouth_opening=clamp(value,0.0,1.0);mouth_variant="continuous_neutral_split"
    # Control range stays normalized; every continuous path uses the same cap.
    var aperture=mouth_opening*MAX_MOUTH_APERTURE
    objects.neutral_lips.visible=false;mouth_sprite.visible=false
    for key in oral_objects:
        var node=oral_objects[key];node.visible=true
        var offset=Vector2.ZERO
        if key=="lower_lip":offset.y=aperture*54.0
        if key=="upper_lip":offset.y=0.0
        if key in ["lower_teeth","tongue"]:offset.y=aperture*5.0
        node.position=oral_homes[key]+offset
        if node.material:
            node.material.set_shader_parameter("rigid_offset",offset)
            node.material.set_shader_parameter("opening",aperture)
func _build_smile_objects():
    smile_manifest=JSON.parse_string(FileAccess.get_file_as_string("res://rig_assets/smile_support/manifest.json"))
    objects.stationary_backing.texture=load("res://rig_assets/smile_support/stationary_backing_eye_reassigned.png")
    for e in smile_manifest.residue_objects:
        var node=Sprite2D.new();node.name=e.name;node.centered=false;node.z_index=e.z
        node.position=Vector2(e.xy[0],e.xy[1]);node.texture=load("res://rig_assets/smile_support/"+e.name+"_original.png");add_child(node)
        var mat=ShaderMaterial.new();mat.shader=load("res://neutral_eye_residue.gdshader")
        mat.set_shader_parameter("skin_texture",load("res://rig_assets/smile_support/"+e.name+"_skin.png"))
        mat.set_shader_parameter("owner_texture",load("res://rig_assets/smile_support/"+e.name+"_ownership.png"))
        node.material=mat;objects[e.name]=node;homes[e.name]={"xy":node.position,"pivot":node.position,"node":node};neutral_residue_objects.append(node)
    objects.hair_front_fringe.texture=load("res://rig_assets/smile_support/hair_front_fringe_eye_reassigned.png")
    var f=smile_manifest.fringe_reassignment
    for key in ["hidden_fringe_continuation","neutral_fringe_eye_pigment"]:
        var pivot=Node2D.new();pivot.position=Vector2(f.pivot[0],f.pivot[1]);pivot.z_index=68 if key=="hidden_fringe_continuation" else 69;add_child(pivot)
        var node=Sprite2D.new();node.name=key;node.centered=false;node.position=Vector2(f.xy[0],f.xy[1])-pivot.position
        node.texture=load("res://rig_assets/smile_support/"+key+".png");pivot.add_child(node)
        objects[key]=node;homes[key]={"xy":Vector2(f.xy[0],f.xy[1]),"pivot":pivot.position,"node":pivot}
        manifest.objects[key]={"hair_angle":.6}
        var mat=ShaderMaterial.new();mat.shader=load("res://neutral_eye_pigment_clip.gdshader")
        mat.set_shader_parameter("original_texture",load("res://rig_assets/smile_support/neutral_fringe_eye_pigment.png"))
        mat.set_shader_parameter("hair_texture",load("res://rig_assets/smile_support/fringe_reassigned_alpha.png"))
        mat.set_shader_parameter("continuation",key=="hidden_fringe_continuation")
        node.material=mat;neutral_residue_objects.append(node)
    for side in ["screen_left","screen_right"]:
        var e=smile_manifest.eye_joints[side]
        var edges=e.edges
        for i in range(edges.size()-1):
            var center=(float(edges[i])+float(edges[i+1]))*.5
            var col=clampi(roundi(center),0,e.size[0]-1)
            for kind in ["ordinary_closed","laugh_lash","laugh_lower_contour","laugh_hidden_continuation"]:
                var old=kind=="ordinary_closed"
                var key=kind+"_"+side+"_joint_"+str(i)
                var pivot=Node2D.new();pivot.name=key+"_pivot";pivot.position=Vector2(e.origin[0]+center,e.origin[1]+(e.old_centers[col] if old else e.new_centers[col]));pivot.z_index=35 if old else (38 if kind=="laugh_lash" else 37)
                var node=Sprite2D.new();node.name=key;node.centered=false;node.position=Vector2(e.origin[0],e.origin[1])-pivot.position;pivot.add_child(node);add_child(pivot)
                node.texture=load("res://rig_assets/object_face/closed_lash_"+side+".png") if old else load("res://rig_assets/smile_support/"+kind+"_"+side+".png")
                var mat=ShaderMaterial.new();mat.shader=load("res://smile_eye_segment.gdshader")
                mat.set_shader_parameter("left_edge",float(edges[i]));mat.set_shader_parameter("right_edge",float(edges[i+1]))
                mat.set_shader_parameter("outgoing",old)
                mat.set_shader_parameter("source_center",float(e.old_centers[col] if old else e.new_centers[col]))
                node.material=mat;node.visible=false
                objects[key]=node;homes[key]={"xy":pivot.position,"pivot":pivot.position,"node":pivot}
                smile_eye_joints.append({"key":key,"side":side,"old":old,"old_center":e.old_centers[col],"new_center":e.new_centers[col],"slope_delta":(e.new_centers[min(col+2,e.size[0]-1)]-e.new_centers[max(col-2,0)]-e.old_centers[min(col+2,e.size[0]-1)]+e.old_centers[max(col-2,0)])/4.0})
    var edges=smile_manifest.lips.segment_edges
    for i in range(edges.size()-1):
        var corner=i==0 or i==edges.size()-2
        for upper in [false,true]:
            var pivot=Node2D.new();var center=(float(edges[i])+float(edges[i+1]))*.5
            pivot.position=Vector2(525+center,634);pivot.z_index=58
            pivot.name=(("mouth_corner_upper_" if upper else "mouth_corner_lower_") if corner else ("upper_lip_joint_" if upper else "lower_lip_joint_"))+str(i)
            add_child(pivot)
            var node=Sprite2D.new();node.centered=false;node.name=pivot.name+"_pigment"
            node.texture=load("res://rig_assets/yawn_mouth/upper_lip.png");node.position=Vector2(525,620)-pivot.position;pivot.add_child(node)
            var mat=ShaderMaterial.new();mat.shader=load("res://smile_lip_segment.gdshader")
            mat.set_shader_parameter("seam_texture",load("res://rig_assets/yawn_mouth/neutral_seam.png"))
            mat.set_shader_parameter("left_edge",float(edges[i]));mat.set_shader_parameter("right_edge",float(edges[i+1]))
            mat.set_shader_parameter("corner",corner);mat.set_shader_parameter("upper_lip",upper);node.material=mat;node.visible=false
            var key=pivot.name;objects[key]=node;homes[key]={"xy":Vector2(525,620),"pivot":pivot.position,"node":pivot}
            smile_lip_joints.append({"key":key,"center":center,"upper":upper,"corner":corner,"index":i,"left":float(edges[i]),"right":float(edges[i+1])})

    for e in smile_manifest.lip_continuations:
        var node=Sprite2D.new();node.name=e.name;node.centered=false;node.z_index=57
        var atlas=AtlasTexture.new();atlas.atlas=load("res://rig_assets/smile_support/"+e.file)
        atlas.region=Rect2(e.atlas_rect[0]-4,e.atlas_rect[1],e.atlas_rect[2]+8,e.atlas_rect[3]);node.texture=atlas;node.position=Vector2(-10,-14)
        var pivot=Node2D.new();pivot.name=e.name+"_pivot";pivot.position=Vector2(525+e.edge,634);pivot.z_index=57;pivot.add_child(node);add_child(pivot);node.z_index=0
        var mat=ShaderMaterial.new();mat.shader=load("res://smile_lip_join.gdshader")
        mat.set_shader_parameter("atlas_origin_px",Vector2(e.atlas_rect[0],e.atlas_rect[1]));mat.set_shader_parameter("source_x",float(e.edge));mat.set_shader_parameter("upper_lip",e.upper);mat.set_shader_parameter("seam_texture",load("res://rig_assets/yawn_mouth/neutral_seam.png"));node.material=mat;node.visible=false
        objects[e.name]=node;homes[e.name]={"xy":Vector2(525+e.edge,634),"pivot":pivot.position,"node":pivot}
        smile_lip_continuations.append(e)

    for joint in smile_lip_joints:
        if not joint.upper:continue
        var node=Sprite2D.new();node.centered=false;node.name="inner_"+joint.key
        node.texture=load("res://rig_assets/pressed_lip_support/inner_upper_lip.png")
        node.position=Vector2(525,620)-homes[joint.key].pivot
        node.z_index=-1;homes[joint.key].node.add_child(node)
        var mat=ShaderMaterial.new();mat.shader=load("res://pressed_lip_clip.gdshader")
        mat.set_shader_parameter("left_edge",joint.left);mat.set_shader_parameter("right_edge",joint.right)
        mat.set_shader_parameter("joint_center",joint.center)
        mat.set_shader_parameter("seam_texture",load("res://rig_assets/yawn_mouth/neutral_seam.png"));node.material=mat
        node.visible=false;objects[node.name]=node;homes[node.name]=homes[joint.key]
        pressed_lip_owners.append({"node":node,"parent":joint.key})

func _smile_lip_offset(x:float,upper:bool,corner:bool)->float:
    return _smile_lip_offset_for_spread(x,upper,corner,mouth_spread)

func _smile_lip_offset_for_spread(x:float,upper:bool,corner:bool,spread_value:float)->float:
    var radius=clampf(abs((x-39.5)/35.5),0.0,1.0)
    var lift=-4.0*spread_value-(4.0+5.0*spread_value)*smile_mouth*pow(radius,1.5)+_corner_curve(x)
    # Purse is rigid contour articulation. Zero retains predecessor arithmetic.
    if mouth_purse>0.0:lift+=mouth_purse*(4.0+8.0*radius*radius)
    if upper:return lift
    var curve=pow(maxf(0.0,1.0-radius*radius),.72)
    var aperture_curve=lerpf(1.0,curve,smile_mouth)
    if mouth_purse>0.0:
        var signed_width=1.0+20.0*spread_value/35.5-14.0*mouth_purse/35.5
        var cavity_width=lerpf(38.0-12.0*mouth_opening*MAX_MOUTH_APERTURE,35.5,smile_mouth)+20.0*spread_value-14.0*mouth_purse
        var h=clampf(abs((x-39.5)*signed_width)/cavity_width,0.0,1.0)
        aperture_curve=lerpf(aperture_curve,sqrt(maxf(0.0,1.0-h*h)),mouth_purse)
    var gap=mouth_opening*MAX_MOUTH_APERTURE*54.0*aperture_curve
    if mouth_purse>0.0:gap=maxf(0.0,gap-1.5*mouth_purse*minf(mouth_opening*4.0,1.0))
    return lift+gap

func _purse_zero_lip_offset(x:float,upper:bool)->float:
    var radius=clampf(abs((x-39.5)/35.5),0.0,1.0)
    var lift=-4.0*mouth_spread-(4.0+5.0*mouth_spread)*smile_mouth*pow(radius,1.5)+_corner_curve(x)
    if upper:return lift
    var curve=pow(maxf(0.0,1.0-radius*radius),.72)
    return lift+mouth_opening*MAX_MOUTH_APERTURE*54.0*lerpf(1.0,curve,smile_mouth)

func _corner_curve(x:float)->float:
    var radius=clampf(abs((x-39.5)/35.5),0.0,1.0)
    return -12.0*mouth_corner_lift*radius*radius*radius

func _corner_secant_offset(joint:Dictionary)->float:
    return (_corner_curve(joint.left)+_corner_curve(joint.right))*.5-_corner_curve(joint.center)

func _corner_secant_slope(joint:Dictionary)->float:
    return (_corner_curve(joint.right)-_corner_curve(joint.left))/(joint.right-joint.left)-(_corner_curve(joint.center+.5)-_corner_curve(joint.center-.5))

func set_smile_controls(eyes:Vector2,mouth:float,spread:float=0.0,corner_lift:float=0.0,lip_press:float=0.0,oral_lift:float=0.0,purse:float=0.0):
    mouth_purse=clampf(purse,0.0,1.0)
    mouth_oral_lift=clampf(oral_lift,0.0,1.0)
    mouth_lip_press=clampf(lip_press,0.0,1.0)
    mouth_corner_lift=clampf(corner_lift,0.0,1.0)
    mouth_spread=clampf(spread,0.0,1.0)*clampf(mouth,0.0,1.0)
    smile_eyes=eyes.clamp(Vector2.ZERO,Vector2.ONE);smile_mouth=clampf(mouth,0.0,1.0)
    for side in ["screen_left","screen_right"]:
        var index=0 if side=="screen_left" else 1
        var amount=smile_eyes[index]
        var close_amount=maxf(closure[index],minf(amount*2.0,1.0))
        var shape=clampf((amount-.5)*2.0,0.0,1.0)
        for key in manifest.objects:
            var e=manifest.objects[key]
            if e.get("eye_side","")==side and e.has("eye_role"):
                objects[key].material.set_shader_parameter("closure",close_amount)
                if int(e.eye_role)==1:homes[key].node.position=homes[key].pivot+Vector2(0,36.0*close_amount)
                if int(e.eye_role)==4:objects[key].visible=shape==0.0
        for joint in smile_eye_joints:
            if joint.side!=side:continue
            var node=objects[joint.key];node.visible=shape>0.0
            var common=lerpf(joint.old_center,joint.new_center,shape)
            var offset=common-(joint.old_center if joint.old else joint.new_center)
            homes[joint.key].node.position=homes[joint.key].pivot+Vector2(0,offset)
            homes[joint.key].node.rotation=atan(joint.slope_delta*(shape if joint.old else shape-1.0))
            node.material.set_shader_parameter("shape",shape)
    for node in neutral_residue_objects:node.material.set_shader_parameter("smile",smile_eyes.y)
    var baseline_lip_transforms={}
    var purse_zero_transforms={}
    for joint in smile_lip_joints:
        var key=joint.key;var home=homes[key];objects[key].visible=smile_mouth>0.0 or mouth_spread>0.0 or mouth_corner_lift>0.0 or mouth_lip_press>0.0 or mouth_purse>0.0
        objects[key].material.set_shader_parameter("opening",mouth_opening*MAX_MOUTH_APERTURE)
        objects[key].material.set_shader_parameter("smile",smile_mouth)
        var baseline_offset=_smile_lip_offset_for_spread(joint.center,joint.upper,joint.corner,0.0)+_corner_secant_offset(joint)
        var baseline_slope=_smile_lip_offset_for_spread(joint.center+.5,joint.upper,joint.corner,0.0)-_smile_lip_offset_for_spread(joint.center-.5,joint.upper,joint.corner,0.0)+_corner_secant_slope(joint)
        baseline_lip_transforms[key]=Transform2D(atan(baseline_slope),home.pivot+Vector2(0,baseline_offset))
        var offset=_smile_lip_offset(joint.center,joint.upper,joint.corner)+_corner_secant_offset(joint)
        home.node.position=home.pivot+Vector2(_spread_x(joint.center),offset)
        var slope=(_smile_lip_offset(joint.center+.5,joint.upper,joint.corner)-_smile_lip_offset(joint.center-.5,joint.upper,joint.corner))+_corner_secant_slope(joint)
        home.node.rotation=atan(slope/(1.0+20.0*mouth_spread/35.5-14.0*mouth_purse/35.5))
        objects[key].material.set_shader_parameter("spread",mouth_spread)
        objects[key].material.set_shader_parameter("corner_lift",mouth_corner_lift)
        objects[key].material.set_shader_parameter("offset_x",_spread_x(joint.center))
        objects[key].material.set_shader_parameter("joint_center",joint.center)
        objects[key].material.set_shader_parameter("offset_y",offset)
        objects[key].material.set_shader_parameter("angle",home.node.rotation)
        var zero_offset=_purse_zero_lip_offset(joint.center,joint.upper)+_corner_secant_offset(joint)
        var zero_slope=_purse_zero_lip_offset(joint.center+.5,joint.upper)-_purse_zero_lip_offset(joint.center-.5,joint.upper)+_corner_secant_slope(joint)
        var zero_angle=atan(zero_slope/(1.0+20.0*mouth_spread/35.5))
        var zero_origin=home.pivot+Vector2(20.0*mouth_spread*(joint.center-39.5)/35.5,zero_offset)
        purse_zero_transforms[key]=Transform2D(zero_angle,zero_origin)*objects[key].transform
    # Trim only newly created rigid-strip overlap. Baseline overlap remains exact.
    for joint in smile_lip_joints:
        var node=objects[joint.key];var actual=homes[joint.key].node.transform*node.transform
        var baseline=purse_zero_transforms[joint.key]
        for side in ["left","right"]:
            var edge=joint.left if side=="left" else joint.right
            var index=joint.index+(-1 if side=="left" else 1)
            var top=Vector2(edge,0);var bottom=Vector2(edge,45)
            var old_top=top;var old_bottom=bottom
            for other in smile_lip_joints:
                if other.upper!=joint.upper or other.index!=index:continue
                var target=homes[other.key].node.transform*objects[other.key].transform
                var old_target=purse_zero_transforms[other.key]
                top=actual.affine_inverse()*(target*Vector2(edge,0))
                bottom=actual.affine_inverse()*(target*Vector2(edge,45))
                old_top=baseline.affine_inverse()*(old_target*Vector2(edge,0))
                old_bottom=baseline.affine_inverse()*(old_target*Vector2(edge,45))
                break
            node.material.set_shader_parameter("neighbor_"+side+"_top",top)
            node.material.set_shader_parameter("neighbor_"+side+"_bottom",bottom)
            node.material.set_shader_parameter("baseline_"+side+"_top",old_top)
            node.material.set_shader_parameter("baseline_"+side+"_bottom",old_bottom)
    for joint in smile_lip_joints:
        if not joint.upper:continue
        var lower_key=("mouth_corner_lower_" if joint.corner else "lower_lip_joint_")+str(joint.index)
        var upper_transform=homes[joint.key].node.transform*objects[joint.key].transform
        var lower_transform=homes[lower_key].node.transform*objects[lower_key].transform
        var peer_transform=lower_transform.affine_inverse()*upper_transform
        var material=objects[joint.key].material
        material.set_shader_parameter("lower_peer_x",peer_transform.x)
        material.set_shader_parameter("lower_peer_y",peer_transform.y)
        material.set_shader_parameter("lower_peer_origin",peer_transform.origin)
        material.set_shader_parameter("lower_peer_angle",homes[lower_key].node.rotation)
        material.set_shader_parameter("lower_peer_offset",homes[lower_key].node.position-homes[lower_key].pivot)
    for continuation in smile_lip_continuations:
        var edge_index=smile_manifest.lips.segment_edges.find(continuation.edge)
        var left_key="";var right_key=""
        for joint in smile_lip_joints:
            if joint.upper!=continuation.upper:continue
            if joint.index==edge_index-1:left_key=joint.key
            if joint.index==edge_index:right_key=joint.key
        var point=Vector2(525+continuation.edge,634)
        var a=homes[left_key].node.transform*(point-homes[left_key].pivot)
        var b=homes[right_key].node.transform*(point-homes[right_key].pivot)
        var delta=b-a
        var key=continuation.name;var node=objects[key];var pivot=homes[key].node
        pivot.position=(a+b)*.5;pivot.rotation=(homes[left_key].node.rotation+homes[right_key].node.rotation)*.5
        var inv=pivot.transform.affine_inverse()
        var left_top=inv*(homes[left_key].node.transform*(point+Vector2(0,-14)-homes[left_key].pivot))
        var left_bottom=inv*(homes[left_key].node.transform*(point+Vector2(0,31)-homes[left_key].pivot))
        var right_top=inv*(homes[right_key].node.transform*(point+Vector2(0,-14)-homes[right_key].pivot))
        var right_bottom=inv*(homes[right_key].node.transform*(point+Vector2(0,31)-homes[right_key].pivot))
        node.visible=smile_mouth>0.0 or mouth_spread>0.0 or mouth_corner_lift>0.0 or mouth_lip_press>0.0 or mouth_purse>0.0
        node.material.set_shader_parameter("spread",mouth_spread)
        node.material.set_shader_parameter("corner_lift",mouth_corner_lift)
        if spread_joint_extensions.has(key):
            var lt:Transform2D=baseline_lip_transforms[left_key];var rt:Transform2D=baseline_lip_transforms[right_key]
            var ba=lt*(point-homes[left_key].pivot);var bb=rt*(point-homes[right_key].pivot)
            var baseline_pivot=Transform2D((lt.get_rotation()+rt.get_rotation())*.5,(ba+bb)*.5)
            var binv=baseline_pivot.affine_inverse();var extra=spread_joint_extensions[key]
            extra.material.set_shader_parameter("baseline_left_top",binv*(lt*(point+Vector2(0,-14)-homes[left_key].pivot)))
            extra.material.set_shader_parameter("baseline_left_bottom",binv*(lt*(point+Vector2(0,31)-homes[left_key].pivot)))
            extra.material.set_shader_parameter("baseline_right_top",binv*(rt*(point+Vector2(0,-14)-homes[right_key].pivot)))
            extra.material.set_shader_parameter("baseline_right_bottom",binv*(rt*(point+Vector2(0,31)-homes[right_key].pivot)))
        node.material.set_shader_parameter("joint_origin",pivot.position)
        node.material.set_shader_parameter("angle",pivot.rotation)
        node.material.set_shader_parameter("left_top",left_top)
        node.material.set_shader_parameter("left_bottom",left_bottom)
        node.material.set_shader_parameter("right_top",right_top)
        node.material.set_shader_parameter("right_bottom",right_bottom)
        node.material.set_shader_parameter("opening",mouth_opening*MAX_MOUTH_APERTURE)
        node.material.set_shader_parameter("smile",smile_mouth)
    for original_name in spread_joint_extensions:
        var extension=spread_joint_extensions[original_name]
        var original=objects[original_name]
        extension.visible=mouth_spread>0.0
        for parameter in ["joint_origin","angle","left_top","left_bottom","right_top","right_bottom","opening","smile","spread","corner_lift"]:
            extension.material.set_shader_parameter(parameter,original.material.get_shader_parameter(parameter))
    if smile_mouth>0.0 or mouth_spread>0.0 or mouth_corner_lift>0.0 or mouth_lip_press>0.0 or mouth_purse>0.0:
        oral_objects.upper_lip.visible=false;oral_objects.lower_lip.visible=false
    for key in oral_objects:
        oral_objects[key].material.set_shader_parameter("smile",smile_mouth)
        oral_objects[key].material.set_shader_parameter("spread",mouth_spread)
        oral_objects[key].material.set_shader_parameter("corner_lift",mouth_corner_lift)
    for node in spread_cavity:
        node.visible=mouth_spread>0.0
        node.material.set_shader_parameter("opening",mouth_opening*MAX_MOUTH_APERTURE)
        node.material.set_shader_parameter("smile",smile_mouth)
        node.material.set_shader_parameter("spread",mouth_spread)
        node.material.set_shader_parameter("corner_lift",mouth_corner_lift)

    for node in spread_teeth:
        var left=node.name.ends_with("left")
        var anchor=Vector2(553 if left else 577,619)
        var origin=Vector2(532 if left else 553,605)
        var angle=(1.0 if left else -1.0)*.12*mouth_spread
        var offset=Vector2((-20.0 if left else 20.0)*mouth_spread,9.0*mouth_spread)
        node.position=anchor+(origin-anchor).rotated(angle)+offset;node.rotation=angle
        node.material.set_shader_parameter("rigid_offset",offset)
        node.material.set_shader_parameter("angle",angle)
        node.material.set_shader_parameter("anchor",anchor)
        node.visible=mouth_spread>0.0
        node.material.set_shader_parameter("opening",mouth_opening*MAX_MOUTH_APERTURE)
        node.material.set_shader_parameter("smile",smile_mouth)
        node.material.set_shader_parameter("spread",mouth_spread)
        node.material.set_shader_parameter("corner_lift",mouth_corner_lift)
    spread_enamel_roots.visible=mouth_spread>0.0
    for parameter in ["opening","smile","spread","corner_lift"]:
        spread_enamel_roots.material.set_shader_parameter(parameter,oral_objects.cavity.material.get_shader_parameter(parameter))
    var tongue_offset=Vector2(0,-40.0*mouth_spread+mouth_opening*MAX_MOUTH_APERTURE*5.0)
    # Preserve the old arithmetic exactly at zero. Total rise stays inside the existing 40px envelope.
    var additional_oral_rise=40.0*(1.0-mouth_spread)*mouth_oral_lift
    if mouth_oral_lift>0.0:tongue_offset.y-=additional_oral_rise
    spread_tongue.position=Vector2(510,667)+tongue_offset
    spread_tongue.material.set_shader_parameter("rigid_offset",tongue_offset)
    spread_tongue.material.set_shader_parameter("opening",mouth_opening*MAX_MOUTH_APERTURE)
    spread_tongue.material.set_shader_parameter("smile",smile_mouth)
    spread_tongue.material.set_shader_parameter("spread",mouth_spread)
    spread_tongue.material.set_shader_parameter("corner_lift",mouth_corner_lift)

    for entry in pressed_lip_owners:
        var node=entry.node;var parent=homes[entry.parent].node
        node.visible=mouth_lip_press>0.0
        node.material.set_shader_parameter("joint_origin",parent.position)
        node.material.set_shader_parameter("angle",parent.rotation)
        node.material.set_shader_parameter("opening",mouth_opening*MAX_MOUTH_APERTURE)
        node.material.set_shader_parameter("smile",smile_mouth)
        node.material.set_shader_parameter("spread",mouth_spread)
        node.material.set_shader_parameter("corner_lift",mouth_corner_lift)
        node.material.set_shader_parameter("lip_press",mouth_lip_press)
    for node in objects.values():
        if node.material and node.material.shader and node.material.shader.resource_path in ["res://object_mouth_clip.gdshader","res://smile_lip_segment.gdshader","res://smile_lip_join.gdshader","res://pressed_lip_clip.gdshader","res://spread_teeth_clip.gdshader"]:
            node.material.set_shader_parameter("purse",mouth_purse)


func _spread_x(source_x:float)->float:
    var offset=20.0*mouth_spread*(source_x-39.5)/35.5
    if mouth_purse>0.0:offset-=14.0*mouth_purse*(source_x-39.5)/35.5
    return offset

func _build_spread_objects():
    for side in ["left","right","top"]:
        var node=Sprite2D.new();node.name="spread_cavity_"+side;node.centered=false;node.z_index=54
        node.texture=load("res://rig_assets/spread_support/cavity_"+side+".png")
        node.position=Vector2(501,620) if side=="left" else (Vector2(605,620) if side=="right" else Vector2(525,619));add_child(node)
        var mat=ShaderMaterial.new();mat.shader=load("res://object_mouth_clip.gdshader")
        mat.set_shader_parameter("origin",node.position)
        mat.set_shader_parameter("seam_texture",load("res://rig_assets/yawn_mouth/neutral_seam.png"))
        node.material=mat;node.visible=false;spread_cavity.append(node);_register_spread_owner(node)


    for side in ["left","right"]:
        var node=Sprite2D.new();node.name="spread_posterior_teeth_"+side;node.centered=false;node.z_index=54
        node.texture=load("res://rig_assets/spread_support/teeth_"+side+".png")
        node.position=Vector2(532 if side=="left" else 553,605);add_child(node)
        var mat=ShaderMaterial.new();mat.shader=load("res://spread_teeth_clip.gdshader")
        mat.set_shader_parameter("origin",node.position)
        mat.set_shader_parameter("seam_texture",load("res://rig_assets/yawn_mouth/neutral_seam.png"))
        mat.set_shader_parameter("left_side",side=="left")
        node.material=mat;node.visible=false;spread_teeth.append(node);_register_spread_owner(node)
    spread_tongue=Sprite2D.new();spread_tongue.name="spread_lower_oral_surface";spread_tongue.centered=false;spread_tongue.z_index=54
    spread_tongue.texture=load("res://rig_assets/spread_support/tongue_surface.png");spread_tongue.position=Vector2(510,667);add_child(spread_tongue)
    # Cavity < tongue < posterior/root enamel < unchanged original front arch.
    move_child(spread_tongue,spread_teeth[0].get_index())
    var mat=ShaderMaterial.new();mat.shader=load("res://object_mouth_clip.gdshader")
    mat.set_shader_parameter("origin",spread_tongue.position)
    mat.set_shader_parameter("seam_texture",load("res://rig_assets/yawn_mouth/neutral_seam.png"));spread_tongue.material=mat;_register_spread_owner(spread_tongue)
    spread_enamel_roots=Sprite2D.new();spread_enamel_roots.name="spread_upper_enamel_roots";spread_enamel_roots.centered=false;spread_enamel_roots.z_index=54
    spread_enamel_roots.texture=load("res://rig_assets/spread_support/upper_enamel_roots.png");spread_enamel_roots.position=Vector2(533,629);add_child(spread_enamel_roots)
    var root_material=ShaderMaterial.new();root_material.shader=load("res://object_mouth_clip.gdshader")
    root_material.set_shader_parameter("origin",spread_enamel_roots.position)
    root_material.set_shader_parameter("seam_texture",load("res://rig_assets/yawn_mouth/neutral_seam.png"));spread_enamel_roots.material=root_material;spread_enamel_roots.visible=false;_register_spread_owner(spread_enamel_roots)
    var support=JSON.parse_string(FileAccess.get_file_as_string("res://rig_assets/spread_support/manifest.json"))
    for e in support.joint_extensions:
        var node=Sprite2D.new();node.name=e.name;node.centered=false;node.position=Vector2(-10,-14);node.z_index=-1
        var atlas=AtlasTexture.new();atlas.atlas=load("res://rig_assets/spread_support/"+e.file)
        atlas.region=Rect2(e.atlas_rect[0],e.atlas_rect[1],20,45);node.texture=atlas
        homes[e.parent].node.add_child(node)
        var material=ShaderMaterial.new();material.shader=load("res://smile_lip_join.gdshader")
        material.set_shader_parameter("atlas_origin_px",Vector2(e.atlas_rect[0],e.atlas_rect[1]))
        material.set_shader_parameter("source_x",float(e.edge));material.set_shader_parameter("upper_lip",e.upper)
        material.set_shader_parameter("seam_texture",load("res://rig_assets/yawn_mouth/neutral_seam.png"))
        material.set_shader_parameter("half_width",10.0);material.set_shader_parameter("outer_extension",true)
        material.set_shader_parameter("previous_sleeve_texture",load("res://rig_assets/smile_support/lip_continuations_atlas.png"))
        for previous in smile_manifest.lip_continuations:
            if previous.name==e.parent:material.set_shader_parameter("previous_atlas_origin_px",Vector2(previous.atlas_rect[0],previous.atlas_rect[1]))
        node.material=material;node.visible=false;spread_joint_extensions[e.parent]=node
        objects[e.name]=node;homes[e.name]=homes[e.parent]

func _register_spread_owner(node:Sprite2D):
    objects[node.name]=node
    homes[node.name]={"xy":node.position,"pivot":node.position,"node":node}

func _verify_required_textures()->bool:
    var file="res://rig_assets/spread_support/required_textures.json"
    if not FileAccess.file_exists(file):
        asset_error="Missing required-texture manifest";push_error(asset_error);return false
    var paths=JSON.parse_string(FileAccess.get_file_as_string(file))
    if not paths is Array or paths.is_empty():
        asset_error="Invalid required-texture manifest";push_error(asset_error);return false
    for path in paths:
        if not path is String or not ResourceLoader.exists(path):
            asset_error="REQUIRED_TEXTURE_IMPORT_MISSING: "+str(path);push_error(asset_error);return false
        var texture=load(path)
        if not texture is Texture2D or texture.get_width()<=0 or texture.get_height()<=0:
            asset_error="REQUIRED_TEXTURE_INVALID: "+str(path);push_error(asset_error);return false
    return true


# Separate source FX, not facial-anatomy owners. Fixed registered pigment and
# unit transforms; only effect intensity changes. Hair remains in front.
func _build_blush_objects()->bool:
    var path="res://rig_assets/blush_support/manifest.json"
    if not FileAccess.file_exists(path):
        asset_error="BLUSH_MANIFEST_MISSING";push_error(asset_error);return false
    var parsed=JSON.parse_string(FileAccess.get_file_as_string(path))
    if not parsed is Dictionary or not parsed.get("objects") is Dictionary or parsed.objects.size()!=2:
        asset_error="BLUSH_MANIFEST_INVALID";push_error(asset_error);return false
    blush_manifest=parsed
    for key in blush_manifest.objects:
        var entry=blush_manifest.objects[key]
        if not entry is Dictionary or not entry.get("file") is String or not entry.get("xy") is Array or entry.xy.size()!=2:
            asset_error="BLUSH_ENTRY_INVALID";push_error(asset_error);return false
    for key in blush_manifest.objects:
        var entry=blush_manifest.objects[key]
        var node=Sprite2D.new();node.name=key;node.centered=false
        node.texture=load("res://rig_assets/blush_support/"+entry.file)
        node.position=Vector2(entry.xy[0],entry.xy[1]);node.z_index=29
        node.modulate=Color(1,1,1,0);node.visible=false
        add_child(node);effect_objects[key]=node
    return true
func set_blush_intensity(value:float):
    blush_intensity=clampf(value,0.0,1.0)
    for node in effect_objects.values():
        node.modulate=Color(1,1,1,blush_intensity);node.visible=blush_intensity>0.0
func _effect_snapshot()->Dictionary:
    var result={}
    for key in effect_objects:
        var node=effect_objects[key]
        result[key]={"position":[node.position.x,node.position.y],"rotation":node.rotation,"scale":[node.scale.x,node.scale.y],"intensity":node.modulate.a,"visible":node.visible,"z_index":node.z_index,"owner":effect_owner}
    return result

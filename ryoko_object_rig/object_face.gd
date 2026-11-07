extends Node2D
## Reusable base assembly. Independent rigid objects; no emotion playback.
const GazeLimits=preload("res://control_limits.gd")
var gaze_manifest:Dictionary
var manifest:Dictionary
var objects:Dictionary={}
var homes:Dictionary={}
var closure=Vector2.ZERO
var gaze=Vector2.ZERO
var brow=Vector2.ZERO
var brow_tilt=Vector2.ZERO
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
var smile_manifest:Dictionary
var smile_lip_joints:Array=[]
var smile_eye_joints:Array=[]
var smile_lip_continuations:Array=[]
var neutral_residue_objects:Array=[]

var ready_for_controls=false
func _ready():
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
    ready_for_controls=true
    set_pose(Vector2.ZERO,Vector2.ZERO,Vector2.ZERO,Vector2.ZERO,"neutral",0.0)
func _update_iris_visibility(side:String):
    objects["sclera_"+side].material.set_shader_parameter("iris_present",objects["iris_"+side].visible)
func set_pose(lids:Vector2,eye_gaze:Vector2,brows:Vector2,brow_angles:Vector2,shape:String,hair_value:float):
    if not ready_for_controls:return
    closure=lids.clamp(Vector2.ZERO,Vector2.ONE);gaze=eye_gaze.clamp(Vector2(GazeLimits.GAZE_MIN,GazeLimits.GAZE_MIN),Vector2(GazeLimits.GAZE_MAX,GazeLimits.GAZE_MAX))
    var gaze_offset=GazeLimits.gaze_pixels(gaze)
    brow=brows.clamp(-Vector2.ONE,Vector2.ONE);brow_tilt=brow_angles.clamp(-Vector2.ONE,Vector2.ONE)*deg_to_rad(8)
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
        var key="brow_"+side;homes[key].node.position=homes[key].pivot+Vector2(0,-brow[index]*10);homes[key].node.rotation=brow_tilt[index]
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
    return {"owners":owners.duplicate(),"closure":[closure.x,closure.y],"gaze":[gaze.x,gaze.y],"mouth_variant":mouth_variant,"mouth_opening":mouth_opening,"eye_smile":[smile_eyes.x,smile_eyes.y],"mouth_smile":smile_mouth,"hair_sway":hair_sway,"objects":transforms}

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
            smile_lip_joints.append({"key":key,"center":center,"upper":upper,"corner":corner,"index":i})

    for e in smile_manifest.lip_continuations:
        var node=Sprite2D.new();node.name=e.name;node.centered=false;node.z_index=57
        var atlas=AtlasTexture.new();atlas.atlas=load("res://rig_assets/smile_support/"+e.file)
        atlas.region=Rect2(e.atlas_rect[0],e.atlas_rect[1],e.atlas_rect[2],e.atlas_rect[3]);node.texture=atlas;node.position=Vector2(-6,-14)
        var pivot=Node2D.new();pivot.name=e.name+"_pivot";pivot.position=Vector2(525+e.edge,634);pivot.z_index=57;pivot.add_child(node);add_child(pivot);node.z_index=0
        var mat=ShaderMaterial.new();mat.shader=load("res://smile_lip_join.gdshader")
        mat.set_shader_parameter("atlas_origin_px",Vector2(e.atlas_rect[0],e.atlas_rect[1]));mat.set_shader_parameter("source_x",float(e.edge));mat.set_shader_parameter("upper_lip",e.upper);mat.set_shader_parameter("seam_texture",load("res://rig_assets/yawn_mouth/neutral_seam.png"));node.material=mat;node.visible=false
        objects[e.name]=node;homes[e.name]={"xy":Vector2(525+e.edge,634),"pivot":pivot.position,"node":pivot}
        smile_lip_continuations.append(e)

func _smile_lip_offset(x:float,upper:bool,corner:bool)->float:
    var radius=clampf(abs((x-39.5)/35.5),0.0,1.0)
    var lift=-4.0*smile_mouth*pow(radius,1.5)
    if upper:return lift
    var curve=pow(maxf(0.0,1.0-radius*radius),.72)
    return lift+mouth_opening*MAX_MOUTH_APERTURE*54.0*lerpf(1.0,curve,smile_mouth)

func set_smile_controls(eyes:Vector2,mouth:float):
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
    for joint in smile_lip_joints:
        var key=joint.key;var home=homes[key];objects[key].visible=smile_mouth>0.0
        objects[key].material.set_shader_parameter("opening",mouth_opening*MAX_MOUTH_APERTURE)
        objects[key].material.set_shader_parameter("smile",smile_mouth)
        var offset=_smile_lip_offset(joint.center,joint.upper,joint.corner)
        home.node.position=home.pivot+Vector2(0,offset)
        var slope=(_smile_lip_offset(joint.center+.5,joint.upper,joint.corner)-_smile_lip_offset(joint.center-.5,joint.upper,joint.corner))
        home.node.rotation=atan(slope)
        objects[key].material.set_shader_parameter("joint_center",joint.center)
        objects[key].material.set_shader_parameter("offset_y",offset)
        objects[key].material.set_shader_parameter("angle",home.node.rotation)
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
        node.visible=smile_mouth>0.0
        node.material.set_shader_parameter("joint_origin",pivot.position)
        node.material.set_shader_parameter("angle",pivot.rotation)
        node.material.set_shader_parameter("left_top",left_top)
        node.material.set_shader_parameter("left_bottom",left_bottom)
        node.material.set_shader_parameter("right_top",right_top)
        node.material.set_shader_parameter("right_bottom",right_bottom)
        node.material.set_shader_parameter("opening",mouth_opening*MAX_MOUTH_APERTURE)
        node.material.set_shader_parameter("smile",smile_mouth)
    if smile_mouth>0.0:
        oral_objects.upper_lip.visible=false;oral_objects.lower_lip.visible=false
    for key in oral_objects:oral_objects[key].material.set_shader_parameter("smile",smile_mouth)

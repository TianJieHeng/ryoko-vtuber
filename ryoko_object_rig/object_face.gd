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
    return {"owners":owners.duplicate(),"closure":[closure.x,closure.y],"gaze":[gaze.x,gaze.y],"mouth_variant":mouth_variant,"mouth_opening":mouth_opening,"hair_sway":hair_sway,"objects":transforms}

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

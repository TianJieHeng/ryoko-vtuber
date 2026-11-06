extends Node2D
## Reusable base assembly. Independent rigid objects; no emotion playback.
var manifest:Dictionary
var objects:Dictionary={}
var homes:Dictionary={}
var closure=Vector2.ZERO
var gaze=Vector2.ZERO
var brow=Vector2.ZERO
var brow_tilt=Vector2.ZERO
var hair_sway=0.0
var mouth_variant="neutral_lips"
var mouth_opening=0.0
var mouth_sprite:Sprite2D
var owners={"eyes":"base_control","brows":"base_control","mouth":"base_control","hair":"base_control"}
var ready_for_controls=false
func _ready():
    manifest=JSON.parse_string(FileAccess.get_file_as_string("res://rig_assets/object_face/manifest.json"))
    for key in manifest.objects:
        var e=manifest.objects[key]
        if key.begins_with("closed_reference") or key.begins_with("viseme_"):continue
        var node=Sprite2D.new();node.name=key;node.texture=load("res://rig_assets/object_face/"+e.file);node.centered=false
        var pivot=Node2D.new();pivot.name=key+"_pivot";pivot.position=Vector2(e.pivot[0],e.pivot[1]);pivot.z_index=int(e.z)
        node.position=Vector2(e.xy[0],e.xy[1])-pivot.position;pivot.add_child(node);add_child(pivot)
        objects[key]=node;homes[key]={"xy":Vector2(e.xy[0],e.xy[1]),"pivot":pivot.position,"node":pivot}
        if key.begins_with("sclera_") or key.begins_with("iris_"):
            var material=ShaderMaterial.new();material.shader=load("res://object_eye_clip.gdshader")
            material.set_shader_parameter("origin",Vector2(e.xy[0],e.xy[1]))
            material.set_shader_parameter("eye_center",Vector2(475,500) if "screen_left" in key else Vector2(651,500))
            node.material=material
    mouth_sprite=Sprite2D.new();mouth_sprite.name="active_viseme";mouth_sprite.centered=false;mouth_sprite.z_index=55;add_child(mouth_sprite)
    objects.active_viseme=mouth_sprite;homes.active_viseme={"xy":Vector2.ZERO,"pivot":Vector2.ZERO,"node":mouth_sprite}
    ready_for_controls=true
    set_pose(Vector2.ZERO,Vector2.ZERO,Vector2.ZERO,Vector2.ZERO,"neutral",0.0)
func set_pose(lids:Vector2,eye_gaze:Vector2,brows:Vector2,brow_angles:Vector2,shape:String,hair_value:float):
    if not ready_for_controls:return
    closure=lids.clamp(Vector2.ZERO,Vector2.ONE);gaze=eye_gaze.clamp(-Vector2.ONE,Vector2.ONE)
    brow=brows.clamp(-Vector2.ONE,Vector2.ONE);brow_tilt=brow_angles.clamp(-Vector2.ONE,Vector2.ONE)*deg_to_rad(8)
    for side in ["screen_left","screen_right"]:
        var index=0 if side=="screen_left" else 1
        for prefix in ["sclera_","iris_"]:
            var key=prefix+side;var node=objects[key]
            var offset=Vector2(gaze.x*6,gaze.y*2) if prefix=="iris_" else Vector2.ZERO
            homes[key].node.position=homes[key].pivot+offset
            node.material.set_shader_parameter("rigid_offset",offset);node.material.set_shader_parameter("closure",closure[index])
        var lash="lash_"+side;homes[lash].node.position=homes[lash].pivot+Vector2(0,closure[index]*23)
        var key="brow_"+side;homes[key].node.position=homes[key].pivot+Vector2(0,-brow[index]*10);homes[key].node.rotation=brow_tilt[index]
    _write_mouth(shape);set_hair_sway(hair_value)
func _write_mouth(shape:String):
    mouth_variant="neutral_lips" if shape=="neutral" else "viseme_"+shape
    mouth_opening=0.0 if shape=="neutral" else 1.0
    objects.neutral_lips.visible=shape=="neutral";mouth_sprite.visible=shape!="neutral"
    if shape=="neutral":return
    var e=manifest.objects[mouth_variant]
    mouth_sprite.texture=load("res://rig_assets/object_face/"+e.file)
    mouth_sprite.position=Vector2(e.xy[0],e.xy[1])
func set_hair_sway(value:float):
    hair_sway=clamp(value,-1,1)
    var angles={"hair_front_fringe":0.6,"hair_temple_screen_left":1.6,"hair_temple_screen_right":1.6,"hair_short_tail":2.0,"hair_bun":0.4,"hair_rear_scalp":0.25}
    for key in angles:homes[key].node.rotation=deg_to_rad(angles[key])*hair_sway
func snapshot()->Dictionary:
    var transforms={}
    for key in objects:
        var p=homes[key].node
        transforms[key]={"position":[p.position.x,p.position.y],"rotation":p.rotation,"scale":[p.scale.x,p.scale.y],"opacity":objects[key].modulate.a,"visible":objects[key].visible}
    return {"owners":owners.duplicate(),"closure":[closure.x,closure.y],"gaze":[gaze.x,gaze.y],"mouth_variant":mouth_variant,"mouth_opening":mouth_opening,"hair_sway":hair_sway,"objects":transforms}

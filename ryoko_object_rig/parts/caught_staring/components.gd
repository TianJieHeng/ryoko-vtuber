extends RefCounted
# Shared bounded component assembly. No expression-specific timeline player.
var rig
var eye
var aversion
var mouth
func setup(r):
    rig=r
    eye=load("res://parts/caught_staring/upper_opening_part.gd").new();eye.rig=rig;eye.work="res://parts/caught_staring"
    aversion=load("res://parts/caught_staring/horizontal_aversion_part.gd").new()
    for side in ["screen_left","screen_right"]:eye.repaired_textures[side]=rig.face.objects["iris_"+side].texture
    mouth=Sprite2D.new();mouth.name="uneasy_visible_part";mouth.centered=false;mouth.z_index=58;mouth.position=Vector2(537,628)
    mouth.texture=ImageTexture.create_from_image(Image.load_from_file("res://parts/caught_staring/uneasy_clear_parting.png"));mouth.modulate.a=0;rig.face.add_child(mouth)
func restore_eye():eye.restore()
func apply(v):
    eye.install_opening(v.opening_px)
    var valid=aversion.apply(rig.face,v.aversion_px)
    assert(valid,"Invalid aversion composition")
    var weight=float(v.uneasy_weight)
    # Kiss owns the default native opacity. Override only while this part owns it.
    if weight>0:
        for key in rig.face.kiss_native_owners:
            var n=rig.face.objects[key];var c=rig.face.kiss_native_opacity[key];c.a*=1.0-weight;n.self_modulate=c
            if n.material is ShaderMaterial:n.material.set_shader_parameter("native_part_weight",1.0-weight)
    mouth.modulate.a=weight

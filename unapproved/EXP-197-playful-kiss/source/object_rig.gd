extends Node2D
## Reusable independent-object BASE. No expression timelines or fallback renderer.
var face
var head:Node2D
var body:Sprite2D
var manual_lids=Vector2.ZERO
var manual_gaze=Vector2.ZERO
var manual_gaze_down_extra=0.0
var manual_brow=Vector2.ZERO
var manual_brow_tilt=Vector2.ZERO
var manual_brow_inner_lift=Vector2.ZERO
var mouth_shape="neutral"
var manual_hair=0.0
var auto_blink=false
var elapsed=0.0
var rig_ready=false
var hud:Label
var hint:Label
var pose_status:Label
var last_error=""
const Limits=preload("res://control_limits.gd")
const MAX_HAIR_SWAY=0.07
const NUMBERS=["blink","blink_L","blink_R","gaze_x","gaze_y","gaze_down_extra","brow_raise","brow_screen_left","brow_screen_right","brow_tilt_screen_left","brow_tilt_screen_right","brow_inner_lift_screen_left","brow_inner_lift_screen_right","hair_sway"]
static func number(value)->bool:return (value is float or value is int) and is_finite(float(value))
func _ready():
    body=Sprite2D.new();body.name="FixedNeckTorso";body.texture=load("res://rig_assets/object_face/fixed_neck_torso.png");body.centered=false
    body.position=Vector2(6,70);body.scale=Vector2(.49,.49);body.z_index=10;add_child(body)
    head=Node2D.new();head.name="RigidHead";head.position=Vector2(6,70);head.scale=Vector2(.49,.49);add_child(head)
    face=load("res://object_face.gd").new();face.name="SeparateFaceObjects";head.add_child(face)
    hud=Label.new();hud.position=Vector2(18,10);hud.add_theme_font_size_override("font_size",20);add_child(hud)
    hint=Label.new();hint.position=Vector2(18,39);hint.add_theme_font_size_override("font_size",13);add_child(hint)
    pose_status=Label.new();pose_status.position=Vector2(18,59);pose_status.add_theme_font_size_override("font_size",12);add_child(pose_status)
    if not face.ready_for_controls:
        last_error=face.asset_error;push_error(last_error);return
    rig_ready=true;_write_pose();print("OBJECT_BASE_READY independent_sprites=",face.objects.size()," expression_timelines=0")
func apply_controls(data:Dictionary)->bool:
    # Validate shared gaze bounds before any pose or ownership mutation.
    for gaze_key in ["gaze_x","gaze_y"]:
        if data.has(gaze_key) and not Limits.valid_gaze(data[gaze_key]):
            last_error="Gaze must be finite and within the advertised normalized bounds";return false
    if data.has("gaze_down_extra") and not Limits.valid_gaze_down_extra(data.gaze_down_extra):
        last_error="gaze_down_extra must be finite and in [0,1]";return false
    # The flattened canonical hair has only a verified small reveal margin.
    if data.has("hair_sway") and (not number(data.hair_sway) or abs(float(data.hair_sway))>MAX_HAIR_SWAY):
        last_error="Canonical hair_sway supports only [-0.07,0.07]";return false
    # Atomic validation: unsupported legacy/emotion commands never mutate the base.
    for key in data:
        if key not in NUMBERS and key not in ["reset","auto_blink","mouth","viseme"]:last_error="Not a base-assembly control: "+str(key);return false
    for key in NUMBERS:
        if data.has(key) and (not number(data[key]) or abs(float(data[key]))>1 or (key in ["blink","blink_L","blink_R","brow_inner_lift_screen_left","brow_inner_lift_screen_right"] and data[key]<0)):
            last_error="Invalid numeric base control: "+key;return false
    for key in ["reset","auto_blink"]:
        if data.has(key) and not data[key] is bool:last_error="Expected boolean: "+key;return false
    for key in ["mouth","viseme"]:
        if data.has(key) and (not data[key] is String or data[key].to_upper() not in ["A","E","I","O","U","REST","RELEASE","NEUTRAL"]):last_error="Invalid mouth shape";return false
    if data.get("reset",false):
        manual_lids=Vector2.ZERO;manual_gaze=Vector2.ZERO;manual_gaze_down_extra=0.0;manual_brow=Vector2.ZERO;manual_brow_tilt=Vector2.ZERO;manual_brow_inner_lift=Vector2.ZERO;mouth_shape="neutral";manual_hair=0;auto_blink=false;elapsed=0
    if data.has("auto_blink"):auto_blink=data.auto_blink
    if data.has("blink"):manual_lids=Vector2.ONE*float(data.blink)
    # Compatibility: anatomical L is screen-right.
    if data.has("blink_L"):manual_lids.y=data.blink_L
    if data.has("blink_R"):manual_lids.x=data.blink_R
    if data.has("gaze_x"):manual_gaze.x=data.gaze_x
    if data.has("gaze_y"):manual_gaze.y=data.gaze_y
    if data.has("gaze_down_extra"):manual_gaze_down_extra=float(data.gaze_down_extra)
    if data.has("brow_raise"):manual_brow=Vector2.ONE*float(data.brow_raise)
    if data.has("brow_screen_left"):manual_brow.x=data.brow_screen_left
    if data.has("brow_screen_right"):manual_brow.y=data.brow_screen_right
    if data.has("brow_tilt_screen_left"):manual_brow_tilt.x=data.brow_tilt_screen_left
    if data.has("brow_tilt_screen_right"):manual_brow_tilt.y=data.brow_tilt_screen_right
    if data.has("brow_inner_lift_screen_left"):manual_brow_inner_lift.x=data.brow_inner_lift_screen_left
    if data.has("brow_inner_lift_screen_right"):manual_brow_inner_lift.y=data.brow_inner_lift_screen_right
    for key in ["mouth","viseme"]:
        if data.has(key):
            var shape=data[key].to_upper()
            if shape in ["REST","RELEASE","NEUTRAL"]:mouth_shape="neutral"
            else:mouth_shape=shape
    if data.has("hair_sway"):manual_hair=data.hair_sway
    _write_pose();return true
func _write_pose():
    var lids=manual_lids
    if auto_blink:
        var phase=fmod(elapsed,4.2)
        if phase>3.86:lids=lids.max(Vector2.ONE*sin((phase-3.86)/.34*PI))
    face.set_pose(lids,manual_gaze,manual_brow,manual_brow_tilt,mouth_shape,manual_hair,manual_gaze_down_extra,manual_brow_inner_lift)
    hud.text="Ryoko / separate-part base assembly"
    hint.text="B lids · O brows · M source viseme · H hair · 0 reset"
    pose_status.text="Canonical native artwork / "+("bounded gaze" if Limits.GAZE_ENABLED else "gaze centered pending coverage QA")
func _process(delta):
    if not rig_ready:return
    elapsed+=delta;_write_pose()
func _unhandled_key_input(event):
    if not event is InputEventKey or not event.pressed or event.echo:return
    match event.keycode:
        KEY_B:apply_controls({"blink":0.0 if manual_lids.x>0 else 1.0})
        KEY_O:apply_controls({"brow_raise":0.0 if manual_brow.x>0 else 1.0})
        KEY_M:apply_controls({"mouth":"REST" if mouth_shape!="neutral" else "A"})
        KEY_H:apply_controls({"hair_sway":0.0 if manual_hair>0 else MAX_HAIR_SWAY})
        KEY_LEFT:apply_controls({"gaze_x":Limits.GAZE_MIN})
        KEY_RIGHT:apply_controls({"gaze_x":Limits.GAZE_MAX})
        KEY_0:apply_controls({"reset":true})

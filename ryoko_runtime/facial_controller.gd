extends Node2D
# Isolated 2D facial expression checkpoint. No audio analysis, body motion or network listener.
var optional_effects
var base_sprite: Sprite2D
var mouths = {}
var blinks = {}
var emotion_eyes = {}
var emotion_blinks = {}
var emotion_mouths = {}
var emotion_effects = {}
var expression = "neutral"
# -1 preserves the legacy discrete rendering exactly.
var performance_amount = -1.0
var articulated_mouths={}
var active_articulated_mouth=""
var performance_effect_strength = 1.0
var speech_override = ""
var mouth_state = "neutral"
var blink_left = false
var blink_right = false
var time = 0.0
var demo = false
var demo_states = ["neutral", "A", "E", "I", "O", "U"]

func _ready():
    var manifest = JSON.parse_string(FileAccess.get_file_as_string("res://registration.json"))
    base_sprite = Sprite2D.new()
    base_sprite.name = "OriginalBustBase"
    base_sprite.texture = load("res://artwork/bust_base.png")
    base_sprite.centered = false
    add_child(base_sprite)
    for state in manifest["mouths"]: mouths[state] = _make_sprite(manifest["mouths"][state])
    for side in manifest["blinks"]: blinks[side] = _make_sprite(manifest["blinks"][side])
    for id in manifest["expressions"]:
        var e = manifest["expressions"][id]
        emotion_effects[id] = []
        for fx in e.get("effects", []):
            var effect_sprite = _make_sprite(fx)
            effect_sprite.set_meta("rest_only", fx.get("rest_only", false))
            emotion_effects[id].append(effect_sprite)
        emotion_eyes[id] = {}
        emotion_blinks[id] = {}
        for side in ["L", "R"]:
            emotion_eyes[id][side] = _make_sprite(e["eyes"][side])
            emotion_blinks[id][side] = _make_sprite(e["blinks"][side])
        emotion_mouths[id] = _make_sprite(e["mouth"])
    _setup_articulated_mouths()
    optional_effects = preload("res://optional_effects.gd").new()
    optional_effects.name = "OptionalEffects"
    add_child(optional_effects)
    reset_neutral()
    demo = "--demo" in OS.get_cmdline_user_args()

func _setup_articulated_mouths():
    var path="res://rig_assets/expression_mouths/manifest.json"
    if not FileAccess.file_exists(path):return
    var manifest=JSON.parse_string(FileAccess.get_file_as_string(path))
    for id in manifest.profiles:
        if not emotion_mouths.has(id):continue
        var p=manifest.profiles[id]
        var base=emotion_mouths[id]
        var material=ShaderMaterial.new()
        material.shader=load("res://isolated_mouth.gdshader")
        material.set_shader_parameter("cleared_mouth",load("res://rig_assets/expression_mouths/"+p.cleared))
        material.set_shader_parameter("oral_feature",load("res://rig_assets/expression_mouths/"+p.feature))
        material.set_shader_parameter("oral_size",Vector2(p.size[0],p.size[1]))
        material.set_shader_parameter("oral_pivot",Vector2(p.pivot[0],p.pivot[1]))
        articulated_mouths[id]={"base":base,"original":base.texture,"material":material}

func set_mouth_articulation(id:String,opening:float,width:float,curve:float=0.0,shift:Vector2=Vector2.ZERO):
    if id!=active_articulated_mouth:clear_mouth_articulation()
    if not articulated_mouths.has(id):return false
    var entry=articulated_mouths[id]
    entry.base.material=entry.material
    var yscale=1.0+clamp(opening,-1.0,1.0)*(0.12 if opening>=0 else 0.9)
    entry.material.set_shader_parameter("oral_scale",Vector2(clamp(1.0+clamp(width,-1.0,1.0)*0.18,0.82,1.16),min(yscale,1.0)))
    entry.material.set_shader_parameter("oral_curve",clamp(curve,-1.0,1.0))
    entry.material.set_shader_parameter("oral_shift",Vector2(clamp(shift.x,-1.0,1.0)*5.0,clamp(shift.y,-1.0,1.0)*4.0))
    active_articulated_mouth=id
    return true

func clear_mouth_articulation():
    if articulated_mouths.has(active_articulated_mouth):
        var entry=articulated_mouths[active_articulated_mouth]
        entry.base.material=null;entry.base.texture=entry.original
    active_articulated_mouth=""

func _make_sprite(entry):
    var sprite = Sprite2D.new()
    sprite.texture = load("res://artwork/" + entry["file"])
    sprite.centered = false
    sprite.position = Vector2(entry["xy"][0], entry["xy"][1])
    add_child(sprite)
    return sprite

func set_expression(id):
    if id != "neutral" and not emotion_eyes.has(id): return false
    expression = id
    _refresh()
    return true

func set_mouth(state):
    var normalized = String(state).to_upper()
    if normalized in ["REST", "RELEASE"]:
        release_speech()
        return true
    if normalized == "NEUTRAL": normalized = "neutral"
    if not mouths.has(normalized): return false
    speech_override = normalized
    _refresh()
    return true

func release_speech():
    speech_override = ""
    _refresh()

func set_blink(left, right):
    blink_left = float(left) >= 0.5
    blink_right = float(right) >= 0.5
    _refresh()

func set_performance_mix(amount:float,effect_strength:float=1.0):
    performance_amount=clamp(amount,0.0,1.0) if amount>=0 else -1.0
    performance_effect_strength=clamp(effect_strength,0.0,1.0)
    _refresh()

func _refresh():
    for node in get_children():
        if node is Sprite2D:node.modulate.a=1.0
    mouth_state = speech_override if speech_override != "" else ("neutral" if expression == "neutral" else expression + "_rest")
    for key in mouths: mouths[key].visible = key == mouth_state
    for side in blinks:
        blinks[side].visible = expression == "neutral" and (blink_left if side == "L" else blink_right)
    for id in emotion_eyes:
        emotion_mouths[id].visible = expression == id and speech_override == ""
        for fx in emotion_effects[id]: fx.visible = expression == id and (speech_override == "" or not fx.get_meta("rest_only", false))
        for side in ["L", "R"]:
            var closed = blink_left if side == "L" else blink_right
            emotion_eyes[id][side].visible = expression == id and not closed
            emotion_blinks[id][side].visible = expression == id and closed

    if performance_amount>=0.0 and expression!="neutral":
        var weight=performance_amount
        for side in ["L","R"]:
            emotion_eyes[expression][side].modulate.a=weight
            emotion_blinks[expression][side].modulate.a=weight
        emotion_mouths[expression].modulate.a=weight
        for fx in emotion_effects[expression]:fx.modulate.a=weight*(performance_effect_strength if not "clean" in fx.texture.resource_path else 1.0)
        if speech_override=="":
            mouths.neutral.visible=true
            mouths.neutral.modulate.a=1.0
        # Neutral base already includes eyes; closing during blending needs
        # the neutral lids behind the incoming expression-specific lids.
        for side in blinks:
            blinks[side].visible=(blink_left if side=="L" else blink_right) and weight<1.0
            blinks[side].modulate.a=1.0
    else:
        for node in get_children():
            if node is Sprite2D:node.modulate.a=1.0

func reset_neutral():
    clear_mouth_articulation()
    performance_amount=-1.0
    performance_effect_strength=1.0
    if optional_effects != null:optional_effects.reset()
    expression = "neutral"
    speech_override = ""
    blink_left = false
    blink_right = false
    _refresh()

func _handle_command(data):
    if data.get("reset", false): reset_neutral()
    if data.has("expression"): set_expression(String(data["expression"]))
    if data.has("mouth"): set_mouth(data["mouth"])
    if data.has("viseme"): set_mouth(data["viseme"])
    if data.has("blink"): set_blink(data["blink"], data["blink"])
    if data.has("blink_L"): blink_left = float(data["blink_L"]) >= 0.5
    if data.has("blink_R"): blink_right = float(data["blink_R"]) >= 0.5
    if data.has("lip_sync"):
        var amplitude = clamp(float(data["lip_sync"]), 0.0, 1.0)
        if amplitude < 0.08: release_speech()
        else: set_mouth("E" if amplitude < 0.35 else "A")
    if data.has("speech_active") and not data["speech_active"]: release_speech()
    _refresh()

func _process(delta):
    if not demo: return
    time += delta
    var ids = emotion_eyes.keys()
    ids.sort()
    set_expression(ids[int(time / 6.0) % ids.size()])
    var phase = fmod(time, 6.0)
    if phase < 2.0: release_speech()
    else: set_mouth(demo_states[int(time * 2.0) % demo_states.size()])
    set_blink(1.0 if fmod(time, 3.0) > 2.85 else 0.0, 1.0 if fmod(time, 3.0) > 2.85 else 0.0)

extends Node2D
# Isolated 2D facial expression checkpoint. No audio analysis, body motion or network listener.
var mouths = {}
var blinks = {}
var emotion_eyes = {}
var emotion_blinks = {}
var emotion_mouths = {}
var emotion_effects = {}
var expression = "neutral"
var speech_override = ""
var mouth_state = "neutral"
var blink_left = false
var blink_right = false
var time = 0.0
var demo = false
var demo_states = ["neutral", "A", "E", "I", "O", "U"]

func _ready():
    var manifest = JSON.parse_string(FileAccess.get_file_as_string("res://registration.json"))
    var base = Sprite2D.new()
    base.texture = load("res://artwork/bust_base.png")
    base.centered = false
    add_child(base)
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
    reset_neutral()
    demo = "--demo" in OS.get_cmdline_user_args()

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

func _refresh():
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

func reset_neutral():
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
    var ids = ["EXP-002", "EXP-041", "EXP-061", "EXP-021", "EXP-102", "EXP-181", "EXP-123", "EXP-142", "EXP-163", "EXP-023", "EXP-081", "EXP-192", "EXP-005", "EXP-161", "EXP-197", "EXP-070", "EXP-094", "EXP-185", "EXP-045", "EXP-104", "EXP-022", "EXP-052", "EXP-096", "EXP-083", "EXP-124", "EXP-184", "EXP-191", "EXP-033", "EXP-087", "EXP-187"]
    set_expression(ids[int(time / 6.0) % ids.size()])
    var phase = fmod(time, 6.0)
    if phase < 2.0: release_speech()
    else: set_mouth(demo_states[int(time * 2.0) % demo_states.size()])
    set_blink(1.0 if fmod(time, 3.0) > 2.85 else 0.0, 1.0 if fmod(time, 3.0) > 2.85 else 0.0)

extends Node2D
# Isolated 2D facial checkpoint. No UDP, body motion, gaze or physics enabled.
var mouths = {}
var blinks = {}
var mouth_state = "neutral"
var time = 0.0
var demo = false
var demo_states = ["neutral", "A", "E", "I", "O", "U"]

func _ready():
    var manifest = JSON.parse_string(FileAccess.get_file_as_string("res://registration.json"))
    var base = Sprite2D.new()
    base.texture = load("res://artwork/bust_base.png")
    base.centered = false
    add_child(base)
    for state in manifest["mouths"]:
        mouths[state] = _make_sprite(manifest["mouths"][state])
    for side in manifest["blinks"]:
        blinks[side] = _make_sprite(manifest["blinks"][side])
    reset_neutral()
    demo = "--demo" in OS.get_cmdline_user_args()

func _make_sprite(entry):
    var sprite = Sprite2D.new()
    sprite.texture = load("res://artwork/" + entry["file"])
    sprite.centered = false
    sprite.position = Vector2(entry["xy"][0], entry["xy"][1])
    add_child(sprite)
    return sprite

func set_mouth(state):
    var normalized = String(state).to_upper()
    if normalized == "NEUTRAL": normalized = "neutral"
    if not mouths.has(normalized): return false
    mouth_state = normalized
    for key in mouths: mouths[key].visible = key == normalized
    return true

func set_blink(left, right):
    # Binary eyelid swaps, not continuous lid deformation.
    blinks["L"].visible = float(left) >= 0.5
    blinks["R"].visible = float(right) >= 0.5

func reset_neutral():
    set_mouth("neutral")
    set_blink(0.0, 0.0)

func _handle_command(data):
    if data.get("reset", false): reset_neutral()
    if data.has("mouth"): set_mouth(data["mouth"])
    if data.has("viseme"): set_mouth(data["viseme"])
    if data.has("blink"): set_blink(data["blink"], data["blink"])
    if data.has("blink_L"): blinks["L"].visible = float(data["blink_L"]) >= 0.5
    if data.has("blink_R"): blinks["R"].visible = float(data["blink_R"]) >= 0.5
    if data.has("lip_sync"):
        # Amplitude fallback only. Phoneme analysis belongs to the external app.
        var amplitude = clamp(float(data["lip_sync"]), 0.0, 1.0)
        set_mouth("neutral" if amplitude < 0.08 else ("E" if amplitude < 0.35 else "A"))

func _process(delta):
    if not demo: return
    time += delta
    set_mouth(demo_states[int(time * 2.0) % demo_states.size()])
    var phase = fmod(time, 3.0)
    set_blink(1.0 if phase > 2.85 else 0.0, 1.0 if phase > 2.85 else 0.0)

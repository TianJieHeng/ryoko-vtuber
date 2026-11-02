extends Node2D
# Registered 2D cutout rig. No volumetric assets, meshes, VRM, or 3D pipeline.
var entries = {}
var sprites = {}
var layer_nodes = {}
var nodes = {}
var global_pivots = {"root": Vector2.ZERO}
var base_positions = {}
var expression_map = {}
var action_map = {}
var gesture_hide = []
var iris_materials = {}
var udp
var peers = []
var time = 0.0
var auto_blink = true
var next_blink = 2.4
var blink_start = -1.0
var blink_left = 0.0
var blink_right = 0.0
var live_gaze = Vector2.ZERO
var expression_gaze = Vector2.ZERO
var live_head_tilt = 0.0
var live_head_turn = 0.0
var expression_head_tilt = 0.0
var expression_brow_raise = 0.0
var expression_brow_lower = 0.0
var action_controls = {"head_tilt":0.0,"brow_raise":0.0,"brow_lower":0.0,"sway":0.25,"arm_proxy":0.0}
var mouth_expression = "neutral"
var live_mouth = ""
var mouth_applied = ""
var lip_sync = 0.0
var expression_effects = []
var live_effects = []
var current_gesture = ""
var gesture_head_offset = Vector2.ZERO
var proof = false
var proof_time = 0.0
var proof_stage = -1
var status_label
var background
var torso
var head
var rig_root

func load_json(path):
    return JSON.parse_string(FileAccess.get_file_as_string(path))

func _ready():
    _build_rig()
    _load_performances()
    _setup_udp()
    var args = OS.get_cmdline_user_args()
    if "--proof" in args:
        proof = true
        auto_blink = false
    if "--live-capture" in args:
        auto_blink = false
    reset_neutral()
    print("RYOKO_RIG_READY layers=%d expressions=%d actions=%d udp=9122" % [entries.size(), expression_map.size(), action_map.size()])

func _group(name, parent, pivot):
    var node = Node2D.new()
    node.name = name
    nodes[parent].add_child(node)
    nodes[name] = node
    global_pivots[name] = pivot
    node.position = pivot - global_pivots[parent]
    base_positions[name] = node.position
    return node

func _build_rig():
    background = ColorRect.new()
    background.size = Vector2(1024,1536)
    background.color = Color(0.094,0.114,0.133,1)
    background.z_index = -1000
    background.mouse_filter = Control.MOUSE_FILTER_IGNORE
    add_child(background)
    rig_root = Node2D.new()
    rig_root.name = "root"
    rig_root.scale = Vector2(0.5,0.5)
    add_child(rig_root)
    nodes["root"] = rig_root
    torso = _group("torso", "root", Vector2(1024,560))
    # Rotate the whole head about the neck base, as in the nostalgic-fondness reference.
    head = _group("head", "torso", Vector2(1024,500))
    _group("pelvis", "torso", Vector2(1024,1300))
    var placement = load_json("res://manifest/placement_manifest.json")
    var gestures = load_json("res://manifest/gesture_layers.json")
    gesture_hide = gestures["gesture_hide"]
    var all_entries = placement["layers"] + gestures["layers"]
    # First create every pivot, then attach parents whose own pivots may appear later in z order.
    for e in all_entries:
        var node = Node2D.new()
        node.name = String(e["name"]) + "_pivot"
        nodes[e["name"]] = node
        layer_nodes[e["name"]] = node
        entries[e["name"]] = e
        global_pivots[e["name"]] = Vector2(e["pivot_master"][0],e["pivot_master"][1])
    for e in all_entries:
        var name = e["name"]
        var parent = e["parent"]
        if not nodes.has(parent): parent = "root"
        var node = layer_nodes[name]
        nodes[parent].add_child(node)
        node.position = global_pivots[name] - global_pivots[parent]
        base_positions[name] = node.position
        var sprite = Sprite2D.new()
        sprite.name = name
        sprite.texture = load("res://" + e["registered_png"])
        sprite.centered = true
        sprite.position = Vector2(e["master_xy"][0] + e["master_size"][0]/2.0, e["master_xy"][1] + e["master_size"][1]/2.0) - global_pivots[name]
        sprite.z_index = int(round(e["z"] * 10.0))
        sprite.z_as_relative = false
        sprite.visible = e.get("enabled_neutral",false)
        node.add_child(sprite)
        sprites[name] = sprite
        if name == "iris_R" or name == "iris_L":
            var mat = ShaderMaterial.new()
            mat.shader = load("res://shaders/iris_clip.gdshader")
            if name == "iris_R":
                mat.set_shader_parameter("clip_center",Vector2(0.604,0.483))
            else:
                mat.set_shader_parameter("clip_center",Vector2(0.356,0.483))
            mat.set_shader_parameter("clip_radius",Vector2(0.235,0.32))
            sprite.material = mat
            iris_materials[name] = mat
    status_label = Label.new()
    status_label.position = Vector2(22,18)
    status_label.add_theme_font_size_override("font_size",25)
    status_label.add_theme_color_override("font_color",Color(0.86,0.92,0.89))
    status_label.z_index = 1200
    add_child(status_label)

func _load_performances():
    for e in load_json("res://manifest/expression_map.json")["expressions"]:
        expression_map[e["id"]] = e
    for a in load_json("res://manifest/body_action_map.json")["actions"]:
        action_map[a["id"]] = a

func _setup_udp():
    udp = UDPServer.new()
    var err = udp.listen(9122)
    if err != OK:
        print("RYOKO_UDP_ERROR code=%d" % err)
    else:
        print("RYOKO_UDP_LISTENING port=9122")

func _poll_udp():
    if udp == null: return
    udp.poll()
    while udp.is_connection_available():
        peers.append(udp.take_connection())
    for peer in peers:
        while peer.get_available_packet_count() > 0:
            var data = JSON.parse_string(peer.get_packet().get_string_from_utf8())
            if typeof(data) == TYPE_DICTIONARY:
                _handle_command(data)

func _handle_command(data):
    print("RYOKO_LIVE_CONTROL " + JSON.stringify(data))
    if data.get("reset",false):
        reset_neutral()
    if data.has("blink"):
        blink_left = clamp(float(data["blink"]),0.0,1.0)
        blink_right = blink_left
    if data.has("blink_L"): blink_left = clamp(float(data["blink_L"]),0.0,1.0)
    if data.has("blink_R"): blink_right = clamp(float(data["blink_R"]),0.0,1.0)
    if data.has("gaze_x"): live_gaze.x = clamp(float(data["gaze_x"]),-1.0,1.0)
    if data.has("gaze_y"): live_gaze.y = clamp(float(data["gaze_y"]),-1.0,1.0)
    if data.has("head_tilt"): live_head_tilt = clamp(float(data["head_tilt"]),-1.0,1.0)
    if data.has("head_turn"): live_head_turn = clamp(float(data["head_turn"]),-1.0,1.0)
    if data.has("brow_raise"): expression_brow_raise = clamp(float(data["brow_raise"]),0.0,1.0)
    if data.has("brow_lower"): expression_brow_lower = clamp(float(data["brow_lower"]),0.0,1.0)
    if data.has("mouth"):
        live_mouth = String(data["mouth"]).to_upper()
        if live_mouth == "NEUTRAL": live_mouth = "neutral"
    if data.has("viseme"):
        live_mouth = String(data["viseme"]).to_upper()
    if data.has("lip_sync"): lip_sync = clamp(float(data["lip_sync"]),0.0,1.0)
    if data.has("expression"): set_expression(String(data["expression"]))
    if data.has("action"): set_action(String(data["action"]))
    if data.has("gesture"): set_gesture(String(data["gesture"]))
    if data.has("effects") and typeof(data["effects"]) == TYPE_DICTIONARY:
        live_effects = []
        for key in data["effects"]:
            if bool(data["effects"][key]): live_effects.append(key)
    if data.has("background"):
        background.color = Color(0.949,0.937,0.910) if data["background"] == "light" else Color(0.094,0.114,0.133)
    if data.has("capture"):
        _capture_later(String(data["capture"]))

func set_expression(id):
    if id == "" or id == "neutral":
        expression_gaze = Vector2.ZERO
        expression_head_tilt = 0.0
        expression_brow_raise = 0.0
        expression_brow_lower = 0.0
        expression_effects = []
        mouth_expression = "neutral"
        return
    if not expression_map.has(id):
        print("RYOKO_UNKNOWN_EXPRESSION " + id)
        return
    var c = expression_map[id]["controls"]
    expression_gaze = Vector2(c.get("gaze_x",0.0),c.get("gaze_y",0.0))
    expression_head_tilt = c.get("head_tilt",0.0)
    expression_brow_raise = c.get("brow_raise",0.0)
    expression_brow_lower = c.get("brow_lower",0.0)
    expression_effects = c.get("effects",[])
    mouth_expression = c.get("mouth","neutral")
    status_label.text = id + " / " + expression_map[id]["slug"]

func set_action(id):
    if id == "" or id == "neutral":
        action_controls = {"head_tilt":0.0,"brow_raise":0.0,"brow_lower":0.0,"sway":0.25,"arm_proxy":0.0}
        set_gesture("")
        return
    if not action_map.has(id):
        print("RYOKO_UNKNOWN_ACTION " + id)
        return
    var a = action_map[id]
    action_controls = a["controls"]
    set_gesture(a.get("gesture",""))
    status_label.text = id + " / " + a["slug"]

func set_gesture(name):
    current_gesture = name
    # Match the approved head and narrow neck join to each registered original torso.
    gesture_head_offset = Vector2.ZERO
    # The registered torso moves to the approved head; the head itself never shifts.
    for layer_name in gesture_hide:
        if sprites.has(layer_name):
            sprites[layer_name].visible = name == "" and entries[layer_name].get("enabled_neutral",false)
    for gesture_name in ["gesture_finger_wag","gesture_crossed_arms","gesture_wave"]:
        if sprites.has(gesture_name): sprites[gesture_name].visible = name == gesture_name
    if sprites.has("gesture_neck_bridge"):
        sprites["gesture_neck_bridge"].visible = name != ""
        layer_nodes["gesture_neck_bridge"].position = base_positions["gesture_neck_bridge"] + gesture_head_offset

func reset_neutral():
    set_expression("")
    set_action("")
    live_gaze = Vector2.ZERO
    live_head_tilt = 0.0
    live_head_turn = 0.0
    blink_left = 0.0
    blink_right = 0.0
    live_mouth = ""
    lip_sync = 0.0
    live_effects = []
    status_label.text = "NEUTRAL"

func _apply_eye(side, value):
    var open = value < 0.55
    for part in ["sclera_","iris_","lash_"]:
        var key = part + side
        if sprites.has(key): sprites[key].visible = open
    var closed = "closed_" + side
    if sprites.has(closed): sprites[closed].visible = not open

func _apply_effects():
    for name in ["blush_R","blush_L","tear_R","tear_L","sweat","anger","sparkle"]:
        if sprites.has(name): sprites[name].visible = name in expression_effects or name in live_effects

func _apply_mouth():
    var selected = mouth_expression
    if lip_sync > 0.04:
        var shapes = ["A","E","I","O","U"]
        selected = shapes[int(time * 11.0) % shapes.size()]
    if live_mouth != "": selected = live_mouth
    if selected == mouth_applied: return
    mouth_applied = selected
    for name in ["mouth_neutral","mouth_A","mouth_E","mouth_I","mouth_O","mouth_U"]:
        if sprites.has(name): sprites[name].visible = name == "mouth_" + selected

func _apply_motion(delta):
    var breath = sin(time * 1.65)
    var sway_amount = action_controls.get("sway",0.25)
    torso.position = base_positions["torso"] + Vector2(sin(time*.72)*3.0*sway_amount,breath*2.0)
    torso.scale = Vector2(1.0+breath*.0015,1.0+breath*.0025)
    rig_root.rotation = sin(time*.58)*.0025*sway_amount
    var tilt = clamp(live_head_tilt + expression_head_tilt + action_controls.get("head_tilt",0.0),-1.0,1.0)
    head.rotation = deg_to_rad(tilt*5.0 + sin(time*.9)*.20)
    head.scale = Vector2(1.0-abs(live_head_turn)*.035,1.0)
    head.position = base_positions["head"] + Vector2(live_head_turn*9.0,0) + gesture_head_offset
    var raise = max(expression_brow_raise,action_controls.get("brow_raise",0.0))
    var lower = max(expression_brow_lower,action_controls.get("brow_lower",0.0))
    for side in ["R","L"]:
        var key = "brow_" + side
        layer_nodes[key].position = base_positions[key] + Vector2(0,(lower-raise)*7.0)
        layer_nodes[key].rotation = deg_to_rad((-1 if side == "R" else 1)*lower*2.0)
    for name in ["temple_R","temple_L","short_tail"]:
        layer_nodes[name].rotation = sin(time*1.35 + (1.0 if name == "temple_L" else 0.0))*.018
    for name in ["earring_R","earring_L","hair_dangler"]:
        layer_nodes[name].rotation = sin(time*1.7 + (1.2 if name.ends_with("L") else 0.0))*.045
    layer_nodes["green_pendant"].rotation = sin(time*1.45)*.035
    # Registered gesture drawings stay locked to the neck and pelvis. Rotating the
    # whole upper-body swap detached it from the approved head in the rejected proof.
    for gesture_name in ["gesture_finger_wag","gesture_crossed_arms","gesture_wave"]:
        if layer_nodes.has(gesture_name): layer_nodes[gesture_name].rotation = 0.0
    var gaze = (live_gaze + expression_gaze).limit_length(1.0)
    for name in iris_materials:
        iris_materials[name].set_shader_parameter("gaze_uv",Vector2(gaze.x*.055,gaze.y*.075))
    var automatic = 0.0
    if auto_blink:
        if time >= next_blink:
            blink_start = time
            next_blink = time + 3.1 + fmod(time*1.73,1.6)
        if blink_start >= 0.0:
            var phase = (time-blink_start)/.18
            if phase <= 1.0: automatic = sin(phase*PI)
            else: blink_start = -1.0
    _apply_eye("L",max(blink_left,automatic))
    _apply_eye("R",max(blink_right,automatic))
    _apply_mouth()
    _apply_effects()

func _proof_update(delta):
    proof_time += delta
    var stages = [0.0,1.15,1.75,3.0,4.25,6.15,7.15,8.0]
    var labels = ["neutral","blink","mouth","head_tilt","finger_wag","crossed_arms","wave","neutral_return"]
    var index = 0
    for i in range(stages.size()):
        if proof_time >= stages[i]: index = i
    if index != proof_stage:
        proof_stage = index
        if index == 0:
            reset_neutral()
        elif index == 1:
            blink_left = 1.0; blink_right = 1.0; status_label.text = "BLINK"
        elif index == 2:
            blink_left = 0.0; blink_right = 0.0; lip_sync = 1.0; status_label.text = "MOUTH / LIP SYNC"
        elif index == 3:
            lip_sync = 0.0; live_head_tilt = .85; live_head_turn = 0.0; expression_brow_raise = 0.0; status_label.text = "HEAD TILT"
        elif index == 4:
            live_head_tilt = 0.0; expression_brow_raise = 0.0; expression_brow_lower = .75; set_gesture("gesture_finger_wag"); status_label.text = "FINGER WAG / SCOLDING"
        elif index == 5:
            set_gesture("gesture_crossed_arms"); status_label.text = "CROSSED ARMS / STERN"
        elif index == 6:
            set_gesture("gesture_wave"); expression_brow_lower = 0.0; expression_brow_raise = .35; status_label.text = "WAVE"
        elif index == 7:
            reset_neutral(); status_label.text = "NEUTRAL RETURN"
        _capture_later(labels[index])
    if proof_time > 8.65:
        get_tree().quit()

func _process(delta):
    time += delta
    _poll_udp()
    if proof: _proof_update(delta)
    _apply_motion(delta)

func _capture_later(label):
    await get_tree().create_timer(.22).timeout
    await RenderingServer.frame_post_draw
    var image = get_viewport().get_texture().get_image()
    var path = "res://previews/proof_" + label + ".png"
    image.save_png(path)
    print("RYOKO_CAPTURE label=" + label + " path=" + path)

func _unhandled_input(event):
    if event is InputEventKey and event.pressed and not event.echo:
        match event.keycode:
            KEY_SPACE:
                blink_left = 1.0; blink_right = 1.0
            KEY_0: reset_neutral()
            KEY_1: live_mouth = "A"
            KEY_2: live_mouth = "E"
            KEY_3: live_mouth = "I"
            KEY_4: live_mouth = "O"
            KEY_5: live_mouth = "U"
            KEY_6: set_action("BOD-002")
            KEY_7: set_action("BOD-001")
            KEY_8: set_action("BOD-011")
            KEY_LEFT: live_head_tilt = -1.0
            KEY_RIGHT: live_head_tilt = 1.0
            KEY_UP: live_head_tilt = 0.0

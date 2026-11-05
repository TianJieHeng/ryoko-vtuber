extends SceneTree
# Existing-expression rigging only. This does not add expressions or clip fields.
# Texture/driver checks run headlessly; visual quality still needs rendered review.
var checks = 0
var failures = 0
const SUPPORTED = ["EXP-064", "EXP-189"]
const SIDES = ["screen_left", "screen_right"]
const LAYERS = ["iris", "sclera", "aperture"]
const EXPECTED_IDS = [
    "EXP-001", "EXP-002", "EXP-003", "EXP-004", "EXP-005", "EXP-006", "EXP-007", "EXP-014",
    "EXP-021", "EXP-022", "EXP-023", "EXP-029", "EXP-031", "EXP-033", "EXP-035", "EXP-040",
    "EXP-041", "EXP-042", "EXP-043", "EXP-045", "EXP-046", "EXP-047", "EXP-050", "EXP-052",
    "EXP-056", "EXP-061", "EXP-063", "EXP-064", "EXP-067", "EXP-069", "EXP-070", "EXP-075",
    "EXP-076", "EXP-078", "EXP-081", "EXP-082", "EXP-083", "EXP-084", "EXP-087", "EXP-088",
    "EXP-089", "EXP-090", "EXP-091", "EXP-092", "EXP-093", "EXP-094", "EXP-095", "EXP-096",
    "EXP-097", "EXP-099", "EXP-102", "EXP-104", "EXP-107", "EXP-114", "EXP-116", "EXP-123",
    "EXP-124", "EXP-125", "EXP-128", "EXP-129", "EXP-130", "EXP-132", "EXP-134", "EXP-137",
    "EXP-139", "EXP-142", "EXP-144", "EXP-148", "EXP-152", "EXP-153", "EXP-158", "EXP-160",
    "EXP-161", "EXP-163", "EXP-164", "EXP-170", "EXP-171", "EXP-174", "EXP-177", "EXP-178",
    "EXP-181", "EXP-184", "EXP-185", "EXP-186", "EXP-187", "EXP-189", "EXP-191", "EXP-192",
    "EXP-193", "EXP-194", "EXP-196", "EXP-197", "EXP-198"
]

func verify(value, label):
    checks += 1
    if not value:
        failures += 1
        push_error("EXPRESSION_GAZE: " + label)

func clean(rig):
    rig.apply_controls({"reset": true})
    rig.apply_controls({"auto_blink": false, "body_follow": false})
    rig._process(0.0)

func select(rig, id):
    verify(rig.apply_controls({"expression": id}), "select " + id)
    rig._process(0.0)

func check_binding(rig, id, open_eyes = Vector2.ONE):
    var supported = id == "neutral" or id in SUPPORTED
    var selected = id if supported else "neutral"
    verify(rig.face.expression == id, "selected expression remains " + id)
    verify(rig.gaze_profile_name == selected, "active texture profile for " + id)
    verify(rig.skin_material.get_shader_parameter("gaze_open") == (open_eyes if supported else Vector2.ZERO), "independent gaze gate for " + id)
    verify(rig.skin_material.get_shader_parameter("brow_enabled") == (id == "neutral"), "brows remain neutral-only for " + id)
    for side in SIDES:
        for layer in LAYERS:
            var key = layer + "_" + side
            verify(rig.skin_material.get_shader_parameter(key) == rig.gaze_profiles[selected][key], "matching cached sampler " + id + "/" + key)

func check_face_art(rig, id, left_closed = false, right_closed = false):
    # Existing facial L is screen-right, and facial R is screen-left.
    verify(rig.face.blink_right == left_closed and rig.face.blink_left == right_closed, "screen-side blink mapping " + id)
    for side in ["L", "R"]:
        var closed = right_closed if side == "L" else left_closed
        verify(rig.face.emotion_eyes[id][side].visible == not closed, "authored eye visibility " + id + "/" + side)
        verify(rig.face.emotion_blinks[id][side].visible == closed, "authored blink visibility " + id + "/" + side)
    verify(not rig.face.blinks.L.visible and not rig.face.blinks.R.visible, "neutral blinks never cover expression " + id)

func check_manifest_and_pixels(rig, manifest):
    var keys = manifest.profiles.keys()
    keys.sort()
    verify(keys == SUPPORTED, "manifest enables exactly the two existing expressions")
    keys = rig.gaze_profiles.keys()
    keys.sort()
    verify(keys == ["EXP-064", "EXP-189", "neutral"], "three cached profiles including unchanged neutral")
    var paths = {}
    var iris_pixels = {}
    for id in ["neutral"] + SUPPORTED:
        verify(rig.gaze_profiles[id].size() == 6, "exactly six samplers " + id)
        for side in SIDES:
            for layer in LAYERS:
                var key = layer + "_" + side
                var path = "res://rig_assets/" + key + ".png" if id == "neutral" else "res://" + manifest.profiles[id][side][layer]
                var texture = rig.gaze_profiles[id][key]
                verify(texture is Texture2D, "loaded texture " + id + "/" + key)
                if not texture is Texture2D:
                    continue
                verify(texture.resource_path == path, "exact source binding " + id + "/" + key)
                verify(texture.get_size() == Vector2(1136, 1384), "full registered canvas " + id + "/" + key)
                if id != "neutral":
                    verify(path.begins_with("res://rig_assets/expression_gaze/"), "derivative lives outside authored artwork " + path)
                    verify(not paths.has(path), "no accidental shared derivative " + path)
                    paths[path] = true
                # Decode source PNGs directly. No GPU readback or renderer needed.
                var pixels = Image.new()
                var decoded = pixels.load_png_from_buffer(FileAccess.get_file_as_bytes(path)) == OK
                verify(decoded and not pixels.is_empty(), "CPU image decode " + path)
                if not decoded or pixels.is_empty():
                    continue
                verify(pixels.get_size() == Vector2i(1136, 1384), "CPU registered dimensions " + path)
                if layer == "iris":
                    verify(pixels.get_used_rect().has_area(), "nonempty separated iris " + id + "/" + side)
                    iris_pixels[id + "/" + side] = pixels.get_data()
                elif layer == "aperture":
                    # Shader uses the red channel, not the PNG's alpha channel.
                    var active = 0
                    var other = 0
                    for y in range(440, 560, 2):
                        for x in range(390, 740, 2):
                            if pixels.get_pixel(x, y).r > 0.5:
                                if (x < 568) == (side == "screen_left"):
                                    active += 1
                                else:
                                    other += 1
                    verify(active > 10 and other == 0, "aperture covers only its screen-side eye " + id + "/" + side)
                    verify(pixels.get_pixel(0, 0).r == 0 and pixels.get_pixel(568, 900).r == 0, "aperture does not repaint background or torso " + id + "/" + side)
    verify(paths.size() == 12, "twelve expression-only derivative PNGs")
    for side in SIDES:
        for pair in [["neutral", "EXP-064"], ["neutral", "EXP-189"], ["EXP-064", "EXP-189"]]:
            var a = pair[0] + "/" + side
            var b = pair[1] + "/" + side
            verify(iris_pixels.has(a) and iris_pixels.has(b) and iris_pixels[a] != iris_pixels[b], "expression-specific iris pixels " + a + " versus " + b)

func test_transitions_and_fallbacks(rig, registration):
    clean(rig)
    var ids = registration.expressions.keys()
    ids.sort()
    verify(ids == EXPECTED_IDS and rig.expression_ids == EXPECTED_IDS, "all 93 existing expression IDs unchanged")
    var face_ids = rig.face.emotion_eyes.keys()
    face_ids.sort()
    verify(face_ids == EXPECTED_IDS, "facial controller retains all 93 profiles")
    rig.apply_controls({"gaze_x": 0.6, "gaze_y": -0.4, "brow_raise": 0.8})
    for i in range(60):
        rig._process(1.0 / 60)
    var direction = rig.gaze.current
    var original_textures = {}
    for id in EXPECTED_IDS:
        original_textures[id] = {}
        for side in ["L", "R"]:
            original_textures[id][side] = rig.face.emotion_eyes[id][side].texture
    for repeat in range(4):
        for id in ["neutral", "EXP-064", "EXP-189", "EXP-001", "neutral"]:
            select(rig, id)
            check_binding(rig, id)
            verify(rig.gaze.current == direction and rig.gaze.target.is_equal_approx(Vector2(0.6, -0.4)), "profile selection does not change gaze values")
    var fallback_count = 0
    for id in EXPECTED_IDS:
        # Each unsupported profile follows real supported rendering, not just
        # another already-disabled fallback, to catch stale sampler/gate state.
        if id not in SUPPORTED:
            select(rig, SUPPORTED[fallback_count % 2])
            fallback_count += 1
        select(rig, id)
        check_binding(rig, id)
        check_face_art(rig, id)
        for side in ["L", "R"]:
            var sprite = rig.face.emotion_eyes[id][side]
            var entry = registration.expressions[id].eyes[side]
            verify(sprite.texture == original_textures[id][side], "authored eye texture retained " + id + "/" + side)
            verify(sprite.texture.resource_path == "res://artwork/" + entry.file, "authored source retained " + id + "/" + side)
            verify(sprite.position == Vector2(entry.xy[0], entry.xy[1]), "eye registration retained " + id + "/" + side)
        rig.apply_controls({"blink": 1})
        rig._process(0.0)
        check_binding(rig, id, Vector2.ZERO)
        check_face_art(rig, id, true, true)
        rig.apply_controls({"blink": 0})
        rig._process(0.0)
    verify(fallback_count == 91, "all 91 unsupported expressions preserve authored-eye fallback")
    select(rig, "EXP-064")
    verify(not rig.apply_controls({"expression": "EXP-999"}), "unknown expression is rejected")
    rig._process(0.0)
    check_binding(rig, "EXP-064")

func test_blinks_and_speech(rig):
    for id in SUPPORTED:
        clean(rig)
        select(rig, id)
        rig.apply_controls({"gaze_x": -0.8, "gaze_y": 0.5, "brow_raise": 0.9})
        for left in [0, 1]:
            for right in [0, 1]:
                rig.apply_controls({"eye_screen_left": left, "eye_screen_right": right})
                rig._process(0.1)
                check_binding(rig, id, Vector2(1 - left, 1 - right))
                check_face_art(rig, id, bool(left), bool(right))
                for mouth in ["neutral", "A", "E", "I", "O", "U"]:
                    rig.apply_controls({"mouth": mouth})
                    rig._process(0.01)
                    verify(rig.face.mouth_state == mouth and rig.face.mouths[mouth].visible, "speech coexists " + id + "/" + mouth)
                    verify(not rig.face.emotion_mouths[id].visible, "speech hides authored rest mouth " + id)
                    check_binding(rig, id, Vector2(1 - left, 1 - right))
                    rig.apply_controls({"speech_active": false})
                    rig._process(0.0)
                    verify(rig.face.mouth_state == id + "_rest" and rig.face.emotion_mouths[id].visible, "speech release restores expression mouth " + id)
        rig.apply_controls({"release_eye_controls": true})
        rig._process(0.0)
        for side in ["screen_left", "screen_right", "both"]:
            rig.apply_controls({"wink": side, "wink_duration": 0.2, "mouth": "E"})
            rig._process(0.05)
            var closed_left = side in ["screen_left", "both"]
            var closed_right = side in ["screen_right", "both"]
            check_binding(rig, id, Vector2(0 if closed_left else 1, 0 if closed_right else 1))
            check_face_art(rig, id, closed_left, closed_right)
            verify(rig.face.mouth_state == "E", "wink preserves speech " + id + "/" + side)
            rig._process(0.2)
            check_binding(rig, id)
            check_face_art(rig, id)
        rig.apply_controls({"mouth": "RELEASE"})
        rig._process(0.0)
        verify(rig.face.speech_override == "" and rig.face.emotion_mouths[id].visible, "mouth release command restores own rest")
        rig.apply_controls({"audio_level": 0.8})
        for i in range(12):
            rig._process(1.0 / 60)
        verify(rig.face.speech_override != "", "audio mouth coexists with " + id)
        check_binding(rig, id)
        rig.apply_controls({"audio_stop": true})
        rig._process(0.0)
        verify(rig.face.speech_override == "" and rig.face.emotion_mouths[id].visible, "audio stop restores " + id)

func test_rigid_motion_and_attention(rig):
    var reference = load("res://gaze_driver.gd").new()
    for id in ["neutral"] + SUPPORTED:
        clean(rig)
        select(rig, id)
        reference.reset()
        for target in [Vector2(-1, -1), Vector2(1, 1), Vector2(-1, 1), Vector2(1, -1), Vector2.ZERO]:
            rig.apply_controls({"gaze_x": target.x, "gaze_y": target.y})
            reference.set_target(target.x, target.y)
            for i in range(20):
                var delta = 1.0 / 60
                reference.step(delta)
                rig._process(delta)
                verify(rig.gaze.current.is_equal_approx(reference.current), "unchanged easing " + id)
                verify(rig.skin_material.get_shader_parameter("gaze_direction").is_equal_approx(reference.current), "unchanged shader direction " + id)
            for p in [Vector2(440, 480), Vector2(470, 510), Vector2(650, 490), Vector2(680, 520)]:
                var q = p + Vector2(13, 7)
                verify((rig.gaze.sample_pixel(p, target) - p).is_equal_approx(-target * Vector2(7, 2)), "same seven/two pixel translation " + id)
                verify((rig.gaze.sample_pixel(q, target) - rig.gaze.sample_pixel(p, target)).is_equal_approx(q - p), "rigid iris shape " + id)
        if id == "neutral":
            continue
        rig.apply_controls({"look_x": 0.9, "look_y": -0.4})
        for i in range(180):
            rig._process(1.0 / 60)
            verify(rig.body_target == Vector3.ZERO and rig.body_current == Vector3.ZERO, "look-at does not drive torso " + id)
        check_binding(rig, id)
        verify(rig.current.y > 0.49 and rig.skin_material.get_shader_parameter("gaze_direction").x > 0.5, "eyes-first look-at integrates " + id)
        rig.apply_controls({"gaze_x": 1, "gaze_y": -1})
        for i in range(60):
            rig._process(1.0 / 60)
        verify(rig.skin_material.get_shader_parameter("gaze_direction") == Vector2(1, -1), "combined look/manual gaze clamps at original limits " + id)
        rig.apply_controls({"gaze_x": 0, "gaze_y": 0, "look_release": true})
        for i in range(600):
            rig._process(1.0 / 60)
        verify(rig.current.length() < 0.0001 and rig.skin_material.get_shader_parameter("gaze_direction").length() < 0.0001, "look/gaze release settles " + id)
        check_binding(rig, id)

func start_memory_clip(rig, data):
    # Use the existing in-memory player API; do not create extra fixture files.
    rig.stop_clip()
    verify(rig.clip.load_data(data) and rig.clip.play(), "existing clip schema accepts gaze cues")
    rig.apply_controls({"auto_blink": false})

func frozen_state(rig):
    return [rig.clock_time, rig.clip.elapsed, rig.current, rig.body_current,
        rig.gaze.current, rig.attention.eye, rig.attention.head, rig.brows.current,
        rig.breathing.amount, rig.skin_material.get_shader_parameter("gaze_direction")]

func test_clips_pause_and_reset(rig):
    var data = {"version": 1, "duration": 1.0, "cues": [
        {"time": 0.0, "controls": {"gaze_x": -0.8, "gaze_y": 0.2, "mouth": "A"}},
        {"time": 0.4, "controls": {"gaze_x": 0.7, "gaze_y": -0.5, "wink": "screen_right", "wink_duration": 0.3}},
        {"time": 0.8, "controls": {"gaze_x": 0.0, "gaze_y": 0.0, "speech_active": false}},
        {"time": 1.0, "controls": {"release_eye_controls": true}}
    ]}
    var validator = load("res://clip_player.gd").new()
    var invalid = data.duplicate(true)
    invalid.cues[0].controls.expression = "EXP-064"
    verify(not validator.load_data(invalid), "expression cues remain unsupported")
    for id in SUPPORTED:
        clean(rig)
        select(rig, id)
        start_memory_clip(rig, data)
        rig._process(0.1)
        check_binding(rig, id)
        verify(rig.gaze.target.is_equal_approx(Vector2(-0.8, 0.2)) and rig.face.mouth_state == "A", "initial gaze/mouth cue on preselected " + id)
        rig.pause_clip(true)
        var state = frozen_state(rig)
        for repeat in range(3):
            for next in ["neutral", "EXP-064", "EXP-189", "EXP-001", id]:
                select(rig, next)
                rig._process(0.25)
                check_binding(rig, next)
                verify(frozen_state(rig) == state, "paused profile swap never advances simulation " + next)
                rig.apply_controls({"blink": 1})
                rig._process(0.25)
                check_binding(rig, next, Vector2.ZERO)
                verify(frozen_state(rig) == state, "paused direct blink updates render gate only")
                rig.apply_controls({"blink": 0})
                rig._process(0.0)
        verify(rig.face.mouth_state == "A", "paused expression changes retain speech")
        rig.pause_clip(false)
        rig._process(0.35)
        verify(rig.clip.elapsed > state[1] and rig.gaze.target.is_equal_approx(Vector2(0.7, -0.5)), "resume dispatches next cue " + id)
        # The 0.35 s test step consumes the 0.3 s wink; schedule an ordinary
        # short step on replay below to verify the cue's actual closed state.
        check_binding(rig, id)
        rig._process(0.4)
        verify(rig.gaze.target == Vector2.ZERO and rig.face.speech_override == "", "explicit timed releases " + id)
        rig._process(0.3)
        verify(not rig.clip.active and rig.face.expression == id, "completion preserves preselected expression " + id)
        start_memory_clip(rig, data)
        rig._process(0.39)
        rig._process(0.02)
        check_binding(rig, id, Vector2(1, 0))
        check_face_art(rig, id, false, true)
        rig.pause_clip(true)
        rig.stop_clip()
        rig._process(0.0)
        verify(not rig.clip.active and not rig.clip.paused and rig.gaze.target == Vector2.ZERO, "paused cancellation releases owned gaze " + id)
        check_binding(rig, id)
        start_memory_clip(rig, data)
        rig._process(0.1)
        rig.pause_clip(true)
        rig.apply_controls({"reset": true})
        rig.apply_controls({"auto_blink": false})
        rig._process(0.0)
        verify(not rig.clip.active and not rig.clip.paused and rig.gaze.current == Vector2.ZERO and rig.gaze.target == Vector2.ZERO, "reset cancels paused clip and clears gaze")
        check_binding(rig, "neutral")

func test_udp(rig):
    clean(rig)
    var adapter = load("res://live_input.gd").new()
    var bound = adapter.start(0) == OK
    verify(bound, "actual UDP loopback bind on ephemeral port")
    if not bound:
        return
    var sender = PacketPeerUDP.new()
    verify(sender.set_dest_address("127.0.0.1", adapter.socket.get_local_port()) == OK, "UDP sender destination")
    select(rig, "EXP-189")
    start_memory_clip(rig, {"version": 1, "duration": 3.0, "cues": [
        {"time": 0.0, "controls": {"gaze_x": 0.8, "gaze_y": -0.8}}
    ]})
    rig._process(0.1)
    rig.pause_clip(true)
    var sequence = 0
    for id in ["EXP-064", "EXP-189", "EXP-001", "neutral", "EXP-189"]:
        sequence += 1
        var controls = {"expression": id, "gaze_x": -0.7, "gaze_y": 0.4, "auto_blink": false, "mouth": "E"}
        verify(sender.put_packet(JSON.stringify({"seq": sequence, "controls": controls}).to_utf8_buffer()) == OK, "send expression+gaze packet " + id)
        await create_timer(0.04).timeout
        adapter.poll(0.01, rig)
        rig._process(0.05)
        verify(adapter.accepted == sequence and adapter.rejected == 0, "actual UDP expression+gaze accepted " + id)
        verify(not rig.clip.active and not rig.clip.paused, "live packet takes over paused clip " + id)
        verify(rig.gaze.target.is_equal_approx(Vector2(-0.7, 0.4)) and rig.face.mouth_state == "E", "actual UDP targets and speech " + id)
        check_binding(rig, id)
    adapter.poll(2.1, rig)
    rig.apply_controls({"auto_blink": false})
    rig._process(0.0)
    verify(not adapter.leased and rig.gaze.target == Vector2.ZERO and rig.gaze.current == Vector2.ZERO and rig.face.speech_override == "", "UDP timeout clears gaze and speech")
    check_binding(rig, "neutral")
    adapter.stop()
    sender.close()

func _initialize():
    call_deferred("run")

func run():
    var manifest = JSON.parse_string(FileAccess.get_file_as_string("res://rig_assets/expression_gaze/profiles.json"))
    verify(manifest is Dictionary and manifest.get("profiles") is Dictionary, "expression-gaze manifest is ready")
    if not manifest is Dictionary or not manifest.get("profiles") is Dictionary:
        quit(1)
        return
    var registration = JSON.parse_string(FileAccess.get_file_as_string("res://registration.json"))
    var rig = load("res://motion_rig.tscn").instantiate()
    root.add_child(rig)
    await process_frame
    rig.set_process(false)
    check_manifest_and_pixels(rig, manifest)
    test_transitions_and_fallbacks(rig, registration)
    test_blinks_and_speech(rig)
    test_rigid_motion_and_attention(rig)
    test_clips_pause_and_reset(rig)
    await test_udp(rig)
    clean(rig)
    rig.queue_free()
    await process_frame
    print("EXPRESSION_GAZE_CHECKS_", "PASS" if failures == 0 else "FAIL", " count=", checks, " failures=", failures)
    quit(1 if failures else 0)

extends SceneTree
# Timed selection of existing registered art, not new expressions or gaze support.
var checks = 0
var failures = 0
var serial = 0
const SUPPORTED = ["EXP-064", "EXP-189"]
const BAD_EXPRESSIONS = ["", "EXP-999", "EXP-008", "exp-064", "EXP-064 ", " neutral", "NEUTRAL", "../artwork/eye.png", "res://artwork/bust_base.png", "user://pose.json", "/tmp/face.png", "https://example.com/face.png", 0, 64, 1.5, true, false, null, [], {}, NAN, INF, -INF]

func verify(value, label):
    checks += 1
    if not value:
        failures += 1
        push_error("EXPRESSION_CUES: " + label)

func data(controls, duration = 3.0):
    return {"version": 1, "duration": duration, "cues": [{"time": 0.0, "controls": controls}]}

func fixture(value):
    serial += 1
    var path = "user://expression_cues_test_%d.json" % serial
    var file = FileAccess.open(path, FileAccess.WRITE)
    file.store_string(JSON.stringify(value))
    file.close()
    return path

func play(rig, value):
    var path = fixture(value)
    var accepted = rig.play_clip(path)
    DirAccess.remove_absolute(path)
    verify(accepted, "runtime fixture loads %d" % serial)
    return accepted

func clean(rig):
    rig.apply_controls({"reset": true})
    rig.apply_controls({"auto_blink": false, "body_follow": false})
    rig._process(0.0)

func key(rig, code, pressed = true, echo = false):
    var event = InputEventKey.new()
    event.keycode = code
    event.pressed = pressed
    event.echo = echo
    rig._unhandled_key_input(event)

func player_state(player):
    return [player.cues.duplicate(true), player.duration, player.elapsed, player.index, player.active, player.paused, player.dispatch_id]

func rig_state(rig):
    return [player_state(rig.clip), rig.face.expression, rig.expression_index, rig.face.speech_override,
        rig.face.blink_left, rig.face.blink_right, rig.target, rig.current, rig.body_target, rig.body_current,
        rig.gaze.target, rig.gaze.current, rig.brows.target, rig.brows.current,
        rig.breathing.manual, rig.breathing.amount, rig.attention.target, rig.attention.active,
        rig.clip_channels.duplicate(true), rig.external_controls, rig.audio_mouth.active,
        rig.audio_mouth.player.stream_paused, rig.gaze_profile_name, rig.clock_time,
        rig.skin_material.get_shader_parameter("gaze_open"), rig.skin_material.get_shader_parameter("gaze_direction")]

func frozen_state(rig):
    return [rig.clip.elapsed, rig.clip.index, rig.clock_time, rig.current, rig.body_current,
        rig.gaze.current, rig.brows.current, rig.attention.eye, rig.attention.head, rig.breathing.amount,
        rig.skin_material.get_shader_parameter("gaze_direction"), rig.audio_mouth.elapsed]

func check_binding(rig, id, open_eyes = Vector2.ONE):
    var supported = id == "neutral" or id in SUPPORTED
    var profile = id if supported else "neutral"
    verify(rig.face.expression == id, "selected " + id)
    verify(rig.expression_index == rig.expression_ids.find(id), "cycle index follows " + id)
    verify(rig.gaze_profile_name == profile, "texture profile follows " + id)
    verify(rig.skin_material.get_shader_parameter("gaze_open") == (open_eyes if supported else Vector2.ZERO), "gaze gate follows " + id)
    verify(rig.skin_material.get_shader_parameter("brow_enabled") == (id == "neutral"), "neutral-only brow gate " + id)
    for side in ["screen_left", "screen_right"]:
        for layer in ["iris", "sclera", "aperture"]:
            var field = layer + "_" + side
            verify(rig.skin_material.get_shader_parameter(field) == rig.gaze_profiles[profile][field], "correct sampler " + id + "/" + field)
    if id != "neutral":
        for side in ["L", "R"]:
            var closed = rig.face.blink_left if side == "L" else rig.face.blink_right
            verify(rig.face.emotion_eyes[id][side].visible == not closed, "authored eye visibility " + id + "/" + side)
            verify(rig.face.emotion_blinks[id][side].visible == closed, "authored blink visibility " + id + "/" + side)

func test_validation(ids):
    var player = load("res://clip_player.gd").new()
    verify(ids.size() == 93, "registry has all existing 93 IDs")
    verify(player.load_data(data({"head_tilt": 0.4})), "legacy standalone load needs no registry")
    verify(player.load_data(data({"expression": "neutral"})), "neutral requires no registry")
    verify(not player.load_data(data({"expression": "EXP-064"})), "unconfigured standalone player fails closed for registered IDs")
    for id in ["neutral"] + ids:
        verify(player.load_data(data({"expression": id}), ids), "load accepts registered " + id)
        verify(player.play() and player.step(0.0) == [{"expression": id}], "dispatch exact registered string " + id)
    for value in BAD_EXPRESSIONS:
        verify(not player.load_data(data({"expression": value}), ids), "reject invalid name/type " + str(value))
    for controls in [{"expression_path": "EXP-064"}, {"pose_save": 1}, {"clip_play": true}, {"clip_stop": true}, {"clip_paused": true}, {"file": "res://demo_clip.json"}]:
        verify(not player.load_data(data(controls), ids), "no generalized/file control expansion " + str(controls))
    var original = {"version": 1, "duration": 3.0, "cues": [
        {"time": 0.0, "controls": {"expression": "EXP-064", "head_tilt": 0.4}},
        {"time": 1.0, "controls": {"expression": "EXP-189"}}
    ]}
    for paused in [false, true]:
        verify(player.load_data(original, ids) and player.play(), "atomicity baseline")
        player.step(0.25)
        player.paused = paused
        for value in BAD_EXPRESSIONS:
            var prior = player_state(player)
            var invalid = original.duplicate(true)
            invalid.duration = 9.0
            invalid.cues.append({"time": 2.0, "controls": {"head_tilt": -1, "reset": true, "expression": value}})
            verify(not player.load_data(invalid, ids), "reject late invalid cue while paused=" + str(paused))
            verify(player_state(player) == prior, "invalid replacement preserves all player state " + str(value))
    var source = data({"expression": "EXP-064"})
    verify(player.load_data(source, ids) and player.play(), "copy validation baseline")
    source.cues[0].controls.expression = "EXP-189"
    var due = player.step(0.0)
    verify(due[0].expression == "EXP-064", "caller cannot mutate validated cue")
    due[0].expression = "EXP-999"
    verify(player.cues[0].controls.expression == "EXP-064", "emitted controls do not mutate stored cue")
    var ordered = {"version": 1, "duration": 2.0, "cues": [
        {"time": 0.0, "controls": {"expression": "EXP-064"}},
        {"time": 0.2, "controls": {"expression": "EXP-189"}},
        {"time": 0.2, "controls": {"expression": "EXP-001"}},
        {"time": 2.0, "controls": {"expression": "neutral"}}
    ]}
    verify(player.load_data(ordered, ids) and player.play(), "ordered load")
    verify(player.step(0.0) == [{"expression": "EXP-064"}], "time-zero expression")
    player.paused = true
    verify(player.step(20.0).is_empty() and player.elapsed == 0.0, "paused expression clock freezes")
    player.paused = false
    verify(player.step(20.0) == [{"expression": "EXP-189"}, {"expression": "EXP-001"}, {"expression": "neutral"}], "same-time and skipped-frame order")
    verify(not player.active and player.step(1.0).is_empty(), "natural completion dispatches once")
    verify(player.play() and player.step(0.0) == [{"expression": "EXP-064"}], "replay starts from first expression")
    player.stop()
    verify(player.step(20.0).is_empty(), "cancel stops future expression cues")

func test_all_runtime_ids(rig):
    clean(rig)
    var timeline = {"version": 1, "duration": 95.0, "cues": []}
    var ids = ["neutral"] + rig.expression_ids
    for i in range(ids.size()):
        timeline.cues.append({"time": float(i), "controls": {"expression": ids[i], "gaze_x": 0.6, "gaze_y": -0.3, "brow_raise": 0.5}})
    play(rig, timeline)
    for i in range(ids.size()):
        rig._process(0.0 if i == 0 else 1.0)
        check_binding(rig, ids[i])
        verify(rig.face.speech_override == "" and rig.face.mouth_state == ("neutral" if ids[i] == "neutral" else ids[i] + "_rest"), "timed selection uses own resting mouth " + ids[i])
    rig.stop_clip()

func test_runtime_atomicity(rig):
    var original = {"version": 1, "duration": 3.0, "cues": [
        {"time": 0.0, "controls": {"expression": "EXP-064", "head_tilt": 0.4, "gaze_x": 0.6, "brow_raise": 0.5, "breath_level": 0.4, "look_y": 0.3, "mouth": "A"}},
        {"time": 1.0, "controls": {"expression": "EXP-189"}}
    ]}
    for paused in [false, true]:
        clean(rig)
        play(rig, original)
        rig._process(0.25)
        rig.pause_clip(paused)
        # Non-finite numbers cannot be faithfully represented in JSON; the
        # in-memory validator above covers them without serializer coercion.
        for value in BAD_EXPRESSIONS.slice(0, 20):
            var prior = rig_state(rig)
            var invalid = original.duplicate(true)
            invalid.cues.append({"time": 2.0, "controls": {"expression": value, "head_tilt": -1, "mouth": "E", "reset": true}})
            var path = fixture(invalid)
            verify(not rig.play_clip(path), "runtime rejects invalid replacement " + str(value))
            DirAccess.remove_absolute(path)
            verify(rig_state(rig) == prior, "active/paused replacement leaves rig untouched " + str(value))
        var before = rig_state(rig)
        verify(not rig.apply_controls({"head_tilt": -1, "gaze_x": -1, "reset": true, "expression": "EXP-999"}, "clip"), "defensive dispatch rejects invalid expression")
        verify(rig_state(rig) == before, "invalid expression cannot partially apply same-cue controls")
        rig.pause_clip(false)
        rig._process(1.0)
        check_binding(rig, "EXP-189")
    clean(rig)
    play(rig, original)
    rig._process(0.25)
    rig.pause_clip(true)
    play(rig, data({"head_tilt": -0.4}))
    verify(not rig.clip.paused and rig.clip.elapsed == 0 and rig.face.expression == "EXP-064", "valid replacement unpauses but retains expression until a new cue")
    verify(rig.gaze.target == Vector2.ZERO and rig.brows.target == Vector2.ZERO and rig.breathing.manual == 0 and not rig.attention.active, "replacement preserves existing owned-channel release policy")
    rig._process(0.1)
    check_binding(rig, "EXP-064")

func test_order_completion_reset(rig):
    clean(rig)
    var ordered = {"version": 1, "duration": 2.0, "cues": [
        {"time": 0.0, "controls": {"expression": "EXP-064", "gaze_x": 0.8}},
        {"time": 0.2, "controls": {"expression": "EXP-189", "gaze_y": 0.5}},
        {"time": 0.2, "controls": {"expression": "EXP-001", "gaze_x": -0.4}},
        {"time": 1.0, "controls": {"expression": "EXP-064", "mouth": "E"}}
    ]}
    play(rig, ordered)
    rig._process(0.0)
    check_binding(rig, "EXP-064")
    rig._process(0.2)
    check_binding(rig, "EXP-001")
    verify(rig.gaze.target.is_equal_approx(Vector2(-0.4, 0.5)), "same-time controls retain source order")
    rig._process(10.0)
    check_binding(rig, "EXP-064")
    verify(not rig.clip.active and rig.face.mouth_state == "E", "natural completion holds final expression and speech")
    rig.stop_clip()
    verify(rig.face.expression == "EXP-064" and rig.face.mouth_state == "E", "inactive stop preserves completed expression and existing speech policy")
    rig.apply_controls({"expression": "EXP-189"})
    rig._process(4.0)
    check_binding(rig, "EXP-189")
    play(rig, ordered)
    rig._process(0.0)
    check_binding(rig, "EXP-064")
    var reset_clip = {"version": 1, "duration": 1.0, "cues": [
        {"time": 0.0, "controls": {"expression": "EXP-189", "gaze_x": 1}},
        {"time": 0.2, "controls": {"reset": true}},
        {"time": 0.2, "controls": {"expression": "EXP-064", "gaze_x": -1, "mouth": "A"}},
        {"time": 1.0, "controls": {"expression": "EXP-001"}}
    ]}
    play(rig, reset_clip)
    rig._process(5.0)
    verify(not rig.clip.active and rig.clip_channels.is_empty(), "reset cancels collected same-frame cues")
    verify(rig.face.expression == "neutral" and rig.expression_index == -1 and rig.gaze.target == Vector2.ZERO and rig.face.speech_override == "", "reset keeps neutral despite stale same-time expression cues")
    rig.apply_controls({"auto_blink": false})
    rig._process(0.0)
    check_binding(rig, "neutral")

func test_pause_and_takeover(rig):
    var timeline = {"version": 1, "duration": 3.0, "cues": [
        {"time": 0.0, "controls": {"expression": "EXP-064", "gaze_x": 0.6, "head_tilt": 0.3, "mouth": "A"}},
        {"time": 1.0, "controls": {"expression": "EXP-189"}},
        {"time": 2.0, "controls": {"expression": "neutral"}}
    ]}
    clean(rig)
    play(rig, timeline)
    rig._process(0.2)
    rig.pause_clip(true)
    var frozen = frozen_state(rig)
    for id in ["EXP-189", "EXP-001", "neutral", "EXP-064"]:
        verify(rig.apply_controls({"expression": id}), "paused API expression change")
        rig._process(10.0)
        check_binding(rig, id)
        verify(rig.clip.active and rig.clip.paused and frozen_state(rig) == frozen, "paused API selection refreshes texture without advancing")
        verify(rig.face.mouth_state == "A", "paused selection preserves speech")
    rig.face.set_expression("EXP-189")
    rig._process(1.0)
    check_binding(rig, "EXP-189")
    verify(frozen_state(rig) == frozen, "direct facial API also refreshes paused samplers/index")
    rig.pause_clip(false)
    rig._process(0.8)
    check_binding(rig, "EXP-189")
    rig._process(1.0)
    check_binding(rig, "neutral")
    for paused in [false, true]:
        for code in [KEY_COMMA, KEY_PERIOD]:
            clean(rig)
            play(rig, timeline)
            rig._process(1.1)
            var start = rig.expression_ids.find("EXP-189")
            verify(rig.expression_index == start, "cycle index tracks latest clip selection")
            rig.pause_clip(paused)
            key(rig, code, false)
            key(rig, code, true, true)
            verify(rig.clip.active and rig.clip.paused == paused and rig.face.expression == "EXP-189", "release/repeat events do not claim clip")
            key(rig, code)
            var next = rig.expression_ids[posmod(start + (-1 if code == KEY_COMMA else 1), rig.expression_ids.size())]
            verify(not rig.clip.active and not rig.clip.paused, "expression key takes over active/paused clip")
            rig._process(10.0)
            check_binding(rig, next)
            verify(rig.gaze.target == Vector2.ZERO and rig.face.speech_override == "", "manual takeover keeps existing transient cleanup")
    # Cycle from a direct facial call even before a process tick can synchronize.
    rig.face.set_expression("EXP-064")
    key(rig, KEY_PERIOD)
    verify(rig.face.expression == rig.expression_ids[rig.expression_ids.find("EXP-064") + 1], "cycle reads actual face rather than stale index")
    for code in [KEY_PERIOD, KEY_COMMA]:
        clean(rig)
        key(rig, code)
        var next = rig.expression_ids[posmod(-1 + (1 if code == KEY_PERIOD else -1), rig.expression_ids.size())]
        verify(rig.face.expression == next, "legacy neutral cycle ordering preserved")
    for paused in [false, true]:
        clean(rig)
        play(rig, timeline)
        rig._process(0.2)
        rig.pause_clip(paused)
        key(rig, KEY_ESCAPE)
        rig._process(10.0)
        check_binding(rig, "EXP-064")
        verify(not rig.clip.active and not rig.clip.paused, "Escape keeps expression and cancels future cues")
        rig.apply_controls({"expression": "EXP-189", "mouth": "E"})
        rig.stop_clip()
        verify(rig.face.expression == "EXP-189" and rig.face.mouth_state == "E", "repeated inactive cancellation preserves fresh state")
        play(rig, timeline)
        rig._process(0.2)
        rig.pause_clip(paused)
        key(rig, KEY_R)
        rig.apply_controls({"auto_blink": false})
        rig._process(10.0)
        check_binding(rig, "neutral")
        verify(not rig.clip.active and not rig.clip.paused, "manual reset cancels future expressions")

func test_blink_speech_independence(rig):
    for id in ["EXP-064", "EXP-189", "EXP-001"]:
        for left in [0, 1]:
            for right in [0, 1]:
                for mouth in ["neutral", "A", "E", "I", "O", "U"]:
                    clean(rig)
                    rig.apply_controls({"expression": "EXP-189", "eye_screen_left": left, "eye_screen_right": right, "mouth": mouth})
                    play(rig, data({"expression": id, "gaze_x": -0.7, "gaze_y": 0.4}))
                    rig._process(0.1)
                    check_binding(rig, id, Vector2(1 - left, 1 - right))
                    verify(rig.face.mouth_state == mouth and not rig.face.emotion_mouths[id].visible, "expression cue preserves viseme " + id + "/" + mouth)
                    verify(rig.face.blink_right == bool(left) and rig.face.blink_left == bool(right), "expression cue preserves independent eyelids")
                    rig.apply_controls({"speech_active": false})
                    verify(rig.face.mouth_state == id + "_rest" and rig.face.emotion_mouths[id].visible, "speech release returns selected expression mouth")
        clean(rig)
        var performance = {"version": 1, "duration": 1.0, "cues": [
            {"time": 0.0, "controls": {"expression": id, "gaze_x": 0.8, "wink": "screen_left", "wink_duration": 0.3, "mouth": "E"}},
            {"time": 0.2, "controls": {"expression": "EXP-064", "audio_level": 0.8}},
            {"time": 0.8, "controls": {"expression": id, "release_eye_controls": true, "audio_stop": true}}
        ]}
        play(rig, performance)
        rig._process(0.05)
        check_binding(rig, id, Vector2(0, 1))
        verify(rig.face.mouth_state == "E", "same-cue wink/speech/expression compose")
        rig._process(0.16)
        check_binding(rig, "EXP-064", Vector2(0, 1))
        verify(rig.audio_mouth.active and rig.face.speech_override != "", "expression transition preserves wink and amplitude mouth")
        rig._process(0.6)
        check_binding(rig, id)
        verify(not rig.audio_mouth.active and rig.face.mouth_state == id + "_rest", "timed releases restore selected authored face")

func test_udp(rig):
    clean(rig)
    var adapter = load("res://live_input.gd").new()
    var bound = adapter.start(0) == OK
    verify(bound, "real loopback UDP binds ephemeral port")
    if not bound:
        return
    var sender = PacketPeerUDP.new()
    verify(sender.set_dest_address("127.0.0.1", adapter.socket.get_local_port()) == OK, "real UDP destination")
    var seq = 0
    for paused in [false, true]:
        for supplied_expression in [false, true]:
            clean(rig)
            play(rig, {"version": 1, "duration": 3.0, "cues": [
                {"time": 0.0, "controls": {"expression": "EXP-064", "gaze_x": 0.6}},
                {"time": 1.0, "controls": {"expression": "EXP-001"}}
            ]})
            rig._process(0.2)
            rig.pause_clip(paused)
            var before = rig_state(rig)
            seq += 1
            verify(sender.put_packet(JSON.stringify({"seq": seq, "controls": {"expression": "EXP-999", "head_tilt": -1}}).to_utf8_buffer()) == OK, "send invalid UDP expression")
            await create_timer(0.04).timeout
            adapter.poll(0.01, rig)
            verify(rig_state(rig) == before, "invalid UDP packet cannot cancel or partially change expression clip")
            var controls = {"gaze_x": -0.7, "gaze_y": 0.4, "auto_blink": false, "mouth": "E"}
            if supplied_expression:
                controls.expression = "EXP-189"
            # Reuse the rejected sequence: invalid input must not claim it.
            verify(sender.put_packet(JSON.stringify({"seq": seq, "controls": controls}).to_utf8_buffer()) == OK, "send valid UDP takeover")
            await create_timer(0.04).timeout
            adapter.poll(0.01, rig)
            rig._process(1.5)
            verify(adapter.accepted == seq and adapter.rejected == seq, "real UDP validates then accepts replacement packet")
            verify(not rig.clip.active and not rig.clip.paused, "live controls take over active/paused expression clip")
            check_binding(rig, "EXP-189" if supplied_expression else "EXP-064")
            verify(rig.gaze.target.is_equal_approx(Vector2(-0.7, 0.4)) and rig.face.mouth_state == "E", "UDP controls survive cleanup and future cues cannot overwrite them")
    adapter.poll(2.1, rig)
    rig.apply_controls({"auto_blink": false})
    rig._process(0.0)
    check_binding(rig, "neutral")
    verify(not adapter.leased and not rig.clip.active and rig.gaze.target == Vector2.ZERO and rig.face.speech_override == "", "UDP timeout retains existing neutral reset policy")
    seq += 1
    sender.put_packet(JSON.stringify({"seq": seq, "controls": {"expression": "EXP-064", "auto_blink": false}}).to_utf8_buffer())
    await create_timer(0.04).timeout
    adapter.poll(0.01, rig)
    rig._process(0.0)
    check_binding(rig, "EXP-064")
    verify(adapter.leased and adapter.accepted == seq, "new UDP sequence resumes after timeout")
    adapter.stop()
    sender.close()

func test_legacy_demos(rig):
    for path in ["res://demo_clip.json", "res://demo_bust_clip.json"]:
        clean(rig)
        rig.apply_controls({"expression": "EXP-064"})
        verify(rig.play_clip(path), "legacy demo still loads " + path)
        for i in range(600):
            rig._process(1.0 / 30)
        verify(not rig.clip.active and rig.face.expression == "EXP-064", "legacy demo still uses preselected expression " + path)
        verify(rig.target == Vector3.ZERO and rig.body_target == Vector3.ZERO, "legacy demo keeps neutral pose ending " + path)

func _initialize():
    call_deferred("run")

func run():
    var registration = JSON.parse_string(FileAccess.get_file_as_string("res://registration.json"))
    var ids = registration.expressions.keys()
    ids.sort()
    test_validation(ids)
    var rig = load("res://motion_rig.tscn").instantiate()
    root.add_child(rig)
    await process_frame
    rig.set_process(false)
    verify(rig.expression_ids == ids, "runtime registry exactly matches registration")
    test_all_runtime_ids(rig)
    test_runtime_atomicity(rig)
    test_order_completion_reset(rig)
    test_pause_and_takeover(rig)
    test_blink_speech_independence(rig)
    await test_udp(rig)
    test_legacy_demos(rig)
    clean(rig)
    rig.queue_free()
    await process_frame
    print("EXPRESSION_CUES_CHECKS_", "PASS" if failures == 0 else "FAIL", " count=", checks, " failures=", failures)
    quit(1 if failures else 0)

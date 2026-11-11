extends SceneTree
## PREPARATION ONLY. Never executed or parser-checked in this task.
## Existing access denial must be resolved externally before a later native task.
var w = get_script().resource_path.get_base_dir()
var rig
var failures = []
var checks = 0
var records = {}
var out = ""
const IDS = ["EXP-092", "EXP-096", "EXP-091"]
const ACTING = ["blink_L", "blink_R", "brow_screen_left", "brow_screen_right", "brow_tilt_screen_left", "brow_tilt_screen_right", "mouth_lip_press", "mouth_purse"]

func read_json(path):
    return JSON.parse_string(FileAccess.get_file_as_string(path))

func check(ok, label):
    checks += 1
    if not ok:
        failures.append(label)

func _initialize():
    var gate = read_json(w + "/NATIVE_GATE.json")
    if not gate is Dictionary or gate.get("allowed", false) != true:
        push_error("Native launch remains blocked. This prepared script is not execution authorization.")
        quit(3)
        return
    if DisplayServer.get_name() == "headless":
        push_error("Native capture requires an authorized non-headless renderer, not a state-only substitute.")
        quit(3)
        return
    out = w + "/native_capture"
    if DirAccess.dir_exists_absolute(out):
        push_error("Preserving existing capture output; refusing overwrite.")
        quit(3)
        return
    call_deferred("run")

func snap(path, detail):
    root.size = Vector2i(568, 800)
    root.canvas_transform = Transform2D.IDENTITY
    if detail:
        root.size = Vector2i(400, 360)
        var camera = Transform2D.IDENTITY.scaled(Vector2.ONE / .49)
        camera.origin = -Vector2(6, 70) / .49 - Vector2(380, 380)
        root.canvas_transform = camera
    await process_frame
    await process_frame
    await RenderingServer.frame_post_draw
    var im = root.get_texture().get_image()
    im.convert(Image.FORMAT_RGBA8)
    check(im.get_size() == (Vector2i(400, 360) if detail else Vector2i(568, 800)), "native dimensions " + path)
    check(im.save_png(path) == OK, "save " + path)
    var ctx = HashingContext.new()
    ctx.start(HashingContext.HASH_SHA256)
    ctx.update(im.get_data())
    return ctx.finish().hex_encode()

func sour_objects(p, frame, brow_home, lash_home):
    for key in p:
        if key not in ACTING:
            check(p[key] == 0, "excluded " + key + " " + str(frame))
    check(p.blink_L == p.blink_R, "ordinary bilateral lids " + str(frame))
    check(p.mouth_open == 0 and p.mouth_kiss == 0 and p.mouth_purse <= .900001, "sealed non-kiss purse " + str(frame))
    for side in ["screen_left", "screen_right"]:
        var node = rig.face.homes["brow_" + side].node
        check((node.position - brow_home[side]).distance_to(Vector2(0, -10 * p["brow_" + side])) < .0001, "actual brow height " + side)
        check(is_equal_approx(node.rotation, deg_to_rad(8 * p["brow_tilt_" + side])), "actual brow rotation " + side)
        var closure = p.blink_R if side == "screen_left" else p.blink_L
        var delta = rig.face.homes["upper_lash_" + side].node.position - lash_home[side]
        check(delta.distance_to(Vector2(0, 36 * closure)) < .0001, "ordinary lash travel " + side)
        check(is_equal_approx(rig.face.objects["iris_" + side].material.get_shader_parameter("closure"), closure), "actual iris closure " + side)
    for entry in rig.face.pressed_lip_owners:
        check(is_equal_approx(entry.node.material.get_shader_parameter("lip_press"), p.mouth_lip_press), "actual pressure shader")
        check(entry.node.visible == (p.mouth_lip_press > 0), "actual pressure visibility")
    check(not rig.face.pressed_lip_owners.is_empty(), "pressure owners present")
    check(is_equal_approx(rig.face._spread_x(4), 14 * p.mouth_purse), "actual left purse displacement")
    check(is_equal_approx(rig.face._spread_x(75), -14 * p.mouth_purse), "actual right purse displacement")
    for x in [4.0, 39.5, 75.0]:
        var expected = p.mouth_purse * (4 + 8 * pow(absf((x - 39.5) / 35.5), 2))
        check(is_equal_approx(rig.face._smile_lip_offset(x, true, false), expected), "actual sealed upper contour")
        check(is_equal_approx(rig.face._smile_lip_offset(x, false, false), expected), "actual sealed lower contour")

func run():
    var freeze = read_json(w + "/INPUT_FREEZE.json")
    if not freeze is Dictionary:
        push_error("Input freeze missing")
        quit(2)
        return
    for name in freeze.files_sha256:
        check(FileAccess.get_sha256(w + "/" + name) == freeze.files_sha256[name], "frozen input " + name)
    var baseline = read_json(w + "/BASELINE_FREEZE.json")
    check(baseline.baseline_profile_count == 39, "approved39 baseline")
    if not failures.is_empty():
        quit(2)
        return
    rig = load("res://expression_rig.tscn").instantiate()
    root.add_child(rig)
    rig.set_process(false)
    rig.auto_blink = false
    check(rig.rig_ready and rig.registry_ready, "rig ready")
    check(rig.list_expressions().size() == 39, "production registry count")
    if not failures.is_empty():
        quit(2)
        return
    rig.hud.hide()
    rig.hint.hide()
    rig.pose_status.hide()
    rig.reset()
    var neutral_objects = rig.face.snapshot()
    var head = rig.head.transform
    var body = rig.body.transform
    var brow_home = {}
    var lash_home = {}
    for side in ["screen_left", "screen_right"]:
        brow_home[side] = rig.face.homes["brow_" + side].node.position
        lash_home[side] = rig.face.homes["upper_lash_" + side].node.position
    var registry_text = FileAccess.get_file_as_string("res://expressions/registry.json")
    var cat = JSON.parse_string(registry_text)
    var defs = {}
    for entry in cat.entries:
        defs[entry.path] = read_json(entry.path)
    var profile_hashes = {}
    for id in IDS:
        var path = w + ("/EXP-092.json" if id == "EXP-092" else "/comparators/" + id + ".json")
        defs["res://candidate-" + id + ".json"] = read_json(path)
        cat.entries.append({"id":id, "path":"res://candidate-" + id + ".json", "aliases":[], "trigger_phase":"neutral"})
        profile_hashes[id] = FileAccess.get_sha256(path)
    check(rig.registry.load_catalogue(cat, defs), "in-memory candidates " + rig.registry.last_error)
    if not failures.is_empty():
        quit(2)
        return
    var predicted = read_json(w + "/NUMERIC_TRAJECTORY.json")
    for id in IDS:
        for view in ["full", "detail"]:
            DirAccess.make_dir_recursive_absolute(out + "/" + id + "/" + view)
        rig.reset()
        check(rig.play_expression(id), "play " + id)
        records[id] = []
        for i in range(121):
            if i > 0:
                check(rig.advance(maxf(0, float(i) / 30 - rig.performance_time)), "advance " + id)
            var p = rig.pose_now()
            check(rig.Registry.scoped_valid(p) and rig.Registry.sealed_mouth_valid(p), "composition " + id)
            check(rig.head.transform == head and rig.body.transform == body, "fixed head/body")
            if id == "EXP-092":
                sour_objects(p, i, brow_home, lash_home)
                for key in p:
                    check(absf(p[key] - predicted.records[i].pose[key]) < .00001, "numeric/native pose parity " + str(i) + " " + key)
            var hashes = []
            hashes.append(await snap(out + "/" + id + "/full/%04d.png" % i, false))
            hashes.append(await snap(out + "/" + id + "/detail/%04d.png" % i, true))
            records[id].append({"frame":i, "time":float(i) / 30, "pose":p, "hashes":hashes})
        check(rig.face.snapshot() == neutral_objects, "exact object neutral " + id)
        check(records[id][0].hashes == records[id][120].hashes, "exact pixel neutral " + id)
    for t in [.35, .6, 1.0, 1.3, 1.6, 2.0, 2.4, 2.8, 3.2, 3.7]:
        for event in ["retrigger", "release", "reset"]:
            rig.reset()
            rig.play_expression("EXP-092")
            rig.advance(t)
            var before = rig.displayed_pose()
            if event == "retrigger":
                rig.play_expression("EXP-092")
                check(rig.displayed_pose() == before, "retrigger continuity")
            elif event == "release":
                rig.release()
                check(rig.displayed_pose() == before, "release continuity")
            else:
                rig.reset()
            for j in range(16):
                check(rig.advance(1.0 / 30), "lifecycle advance")
                check(rig.Registry.scoped_valid(rig.pose_now()), "lifecycle composition")
            rig.advance(4)
            check(rig.face.snapshot() == neutral_objects, "lifecycle exact neutral")
    check(FileAccess.get_file_as_string("res://expressions/registry.json") == registry_text, "unchanged disk registry")
    var result = {"status":"PASS" if failures.is_empty() else "FAIL", "failures":failures,
        "checks":checks, "approval":"UNAPPROVED", "visual_capture":true,
        "display":DisplayServer.get_name(), "renderer":RenderingServer.get_video_adapter_name(),
        "profile_hashes":profile_hashes, "input_freeze_sha256":FileAccess.get_sha256(w + "/INPUT_FREEZE.json"),
        "baseline_freeze_sha256":FileAccess.get_sha256(w + "/BASELINE_FREEZE.json"),
        "frames_per_profile":121, "fps":30, "duration":4.0, "records":records,
        "normal_speed_observed":false, "visual_distinctness":"PENDING independent source/native review"}
    var file = FileAccess.open(out + "/motion_checks.json", FileAccess.WRITE)
    file.store_string(JSON.stringify(result, "  "))
    file.close()
    quit(0 if failures.is_empty() else 1)

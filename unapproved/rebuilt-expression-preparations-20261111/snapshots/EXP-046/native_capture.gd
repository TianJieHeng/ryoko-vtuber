extends SceneTree
# PREPARATION ONLY. Never executed in this task. No launcher is supplied.
# Parent must resolve the exact outstanding project-launch denial first.
var w = get_script().resource_path.get_base_dir()
var rig
var failures = []
var checks = 0
var frozen = {}
var baseline_freeze = {}
var expected = {}
func _initialize():
    call_deferred("run")
func read_json(path):
    return JSON.parse_string(FileAccess.get_file_as_string(path))
func check(ok, label):
    checks += 1
    if not ok: failures.append(label)
func fail_early(label):
    push_error(label)
    quit(1)
func verify_inputs():
    frozen = read_json(w + "/CANDIDATE_FREEZE.json")
    baseline_freeze = read_json(w + "/BASELINE_FREEZE.json")
    if frozen == null or baseline_freeze == null: return false
    for path in frozen.files_sha256:
        check(FileAccess.get_sha256(w + "/" + path) == frozen.files_sha256[path], "candidate input " + path)
    for path in baseline_freeze.baseline_files_sha256:
        check(FileAccess.get_sha256("res://" + path) == baseline_freeze.baseline_files_sha256[path], "baseline input " + path)
    for path in baseline_freeze.reference_files_sha256:
        check(FileAccess.get_sha256(w + "/reference/" + path) == baseline_freeze.reference_files_sha256[path], "reference input " + path)
    return failures.is_empty()
func pose_check(p, label):
    check(rig.Registry.scoped_valid(p), label + " scoped")
    check(rig.Registry.sealed_mouth_valid(p), label + " mouth domain")
    for key in p:
        var bounds = rig.Registry.CHANNEL_BOUNDS[key]
        check(p[key] >= bounds[0] and p[key] <= bounds[1], label + " bounds " + key)
func near_pose(actual, wanted, label):
    for key in rig.CHANNELS:
        check(absf(float(actual[key]) - float(wanted.get(key, 0.0))) < 0.00001, label + " " + key)
func geometry_check(p, wanted, label):
    var gaze = Vector2(wanted.gaze_source_px[0], wanted.gaze_source_px[1])
    for side in ["screen_left", "screen_right"]:
        var iris = rig.face.homes["iris_" + side]
        check((iris.node.position - iris.pivot).distance_to(gaze) < 0.0001, label + " iris position " + side)
        var shader_gaze = rig.face.objects["iris_" + side].material.get_shader_parameter("rigid_gaze")
        check(shader_gaze.distance_to(gaze) < 0.0001, label + " iris shader " + side)
        var sclera_gaze = rig.face.objects["sclera_" + side].material.get_shader_parameter("rigid_gaze")
        check(sclera_gaze.distance_to(gaze) < 0.0001, label + " sclera shader " + side)
        var brow = rig.face.homes["brow_" + side]
        var b = wanted.brows[side]
        check((brow.node.position - brow.pivot).distance_to(Vector2(b.pivot_delta_source_px[0], b.pivot_delta_source_px[1])) < 0.0001, label + " brow position " + side)
        check(absf(rad_to_deg(brow.node.rotation) - b.angle_degrees) < 0.0001, label + " brow rotation " + side)
        var lash = rig.face.homes["upper_lash_" + side]
        check((lash.node.position - lash.pivot).distance_to(Vector2(0, wanted.lash_source_px[side])) < 0.0001, label + " ordinary lash " + side)
    var gap = rig.face._smile_lip_offset(39.5, false, false) - rig.face._smile_lip_offset(39.5, true, false)
    check(absf(gap - wanted.central_gap_source_px) < 0.0001, label + " central gap")
    pose_check(p, label)
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
    var size = Vector2i(400, 360) if detail else Vector2i(568, 800)
    check(im.get_size() == size, "native dimensions " + path)
    if im.get_size() != size: return ""
    check(im.save_png(path) == OK, "save " + path)
    var ctx = HashingContext.new()
    ctx.start(HashingContext.HASH_SHA256)
    ctx.update(im.get_data())
    return ctx.finish().hex_encode()
func run():
    var clearance = read_json(w + "/LAUNCH_CLEARANCE.json")
    if clearance == null or clearance.get("cleared", false) != true or clearance.get("state", "") != "CLEARED_FOR_THIS_NATIVE_CAPTURE":
        fail_early("Outstanding project-launch denial. Do not run or bypass it.")
        return
    if DisplayServer.get_name() == "headless" or RenderingServer.get_video_adapter_name().is_empty():
        fail_early("Headless/state-only execution is not native capture evidence.")
        return
    if DirAccess.dir_exists_absolute(w + "/native_capture"):
        fail_early("Preserving existing or partial capture. Use a separately frozen new attempt.")
        return
    if not verify_inputs():
        fail_early("Input identity failed before native capture: " + str(failures))
        return
    expected = read_json(w + "/EXPECTED_TRAJECTORY.json")
    rig = load("res://expression_rig.tscn").instantiate()
    root.add_child(rig)
    rig.set_process(false)
    rig.auto_blink = false
    check(rig.rig_ready and rig.registry_ready, "rig ready")
    check(rig.list_expressions().size() == 39, "baseline39 catalogue")
    if not failures.is_empty():
        fail_early(str(failures))
        return
    rig.hud.hide()
    rig.hint.hide()
    rig.pose_status.hide()
    rig.reset()
    var neutral_snapshot = rig.face.snapshot()
    var head = rig.head.transform
    var body = rig.body.transform
    var registry_text = FileAccess.get_file_as_string("res://expressions/registry.json")
    var cat = JSON.parse_string(registry_text)
    var defs = {}
    for entry in cat.entries: defs[entry.path] = read_json(entry.path)
    cat.entries.append({"id":"EXP-046", "path":"res://candidate-046.json", "aliases":[], "trigger_phase":"neutral"})
    defs["res://candidate-046.json"] = read_json(w + "/EXP-046.json")
    check(rig.registry.load_catalogue(cat, defs), "memory-only candidate validation " + rig.registry.last_error)
    check(rig.list_expressions().size() == 40, "baseline39 plus one memory-only candidate")
    if not failures.is_empty():
        fail_early(str(failures))
        return
    for directory in ["static", "full", "detail"]:
        DirAccess.make_dir_recursive_absolute(w + "/native_capture/" + directory)
    var static_records = []
    for row in read_json(w + "/plan.json"):
        rig.reset()
        check(rig.apply_controls(row.pose), "static controls " + row.name)
        near_pose(rig.pose_now(), row.pose, "static " + row.name)
        check(rig.head.transform == head and rig.body.transform == body, "static body fixed")
        var hashes = [await snap(w + "/native_capture/static/" + row.name + "_full.png", false), await snap(w + "/native_capture/static/" + row.name + "_detail.png", true)]
        static_records.append({"name":row.name, "pose":rig.pose_now(), "hashes":hashes})
    rig.reset()
    check(rig.play_expression("EXP-046"), "candidate trigger")
    var records = []
    for i in range(145):
        if i > 0: check(rig.advance(maxf(0.0, float(i) / 30.0 - rig.performance_time)), "advance " + str(i))
        var p = rig.pose_now()
        near_pose(p, expected.records[i].pose, "Python comparison " + str(i))
        geometry_check(p, expected.records[i].geometry_model, "geometry " + str(i))
        check(rig.head.transform == head and rig.body.transform == body, "fixed head/body " + str(i))
        check(not rig.auto_blink, "automatic blink off " + str(i))
        var hashes = [await snap(w + "/native_capture/full/%04d.png" % i, false), await snap(w + "/native_capture/detail/%04d.png" % i, true)]
        records.append({"frame":i, "time":float(i) / 30.0, "pose":p, "hashes":hashes})
    check(records[0].hashes == records[-1].hashes, "exact neutral pixels")
    check(rig.face.snapshot() == neutral_snapshot, "exact neutral object state")
    var lifecycle_records = []
    for t in [.35, .7, 1.15, 1.5, 1.85, 2.25, 2.7, 3.15, 3.7, 4.5]:
        rig.reset()
        rig.play_expression("EXP-046")
        rig.advance(t)
        var before = rig.displayed_pose()
        rig.play_expression("EXP-046")
        check(rig.displayed_pose() == before, "continuous retrigger " + str(t))
        for j in range(145):
            rig.advance(1.0 / 30.0)
            pose_check(rig.pose_now(), "retrigger " + str(t) + " " + str(j))
        check(rig.face.snapshot() == neutral_snapshot, "retrigger exact neutral " + str(t))
        rig.reset()
        rig.play_expression("EXP-046")
        rig.advance(t)
        before = rig.displayed_pose()
        rig.release()
        check(rig.displayed_pose() == before, "continuous release " + str(t))
        for j in range(16):
            rig.advance(1.0 / 30.0)
            pose_check(rig.pose_now(), "release " + str(t) + " " + str(j))
        check(rig.face.snapshot() == neutral_snapshot, "release exact neutral " + str(t))
        rig.play_expression("EXP-046")
        rig.advance(t)
        rig.reset()
        check(rig.face.snapshot() == neutral_snapshot, "reset exact neutral " + str(t))
        lifecycle_records.append({"interruption_time":t,"retrigger_steps":145,"release_steps":16,"reset_checked":true})
    check(FileAccess.get_file_as_string("res://expressions/registry.json") == registry_text, "disk registry unchanged")
    verify_inputs()
    var receipt = {"status":"PASS" if failures.is_empty() else "FAIL", "checks":checks, "failures":failures, "visual_capture":true, "profile_sha256":FileAccess.get_sha256(w + "/EXP-046.json"), "freeze_sha256":FileAccess.get_sha256(w + "/CANDIDATE_FREEZE.json"), "expected_sha256":FileAccess.get_sha256(w + "/EXPECTED_TRAJECTORY.json"), "baseline_profile_count":39, "frames":145, "fps":30, "duration":4.8, "display":DisplayServer.get_name(), "renderer":RenderingServer.get_video_adapter_name(), "static_records":static_records, "records":records, "lifecycle_records":lifecycle_records, "production_registry_unchanged":true, "normal_speed_observed":false, "approval":"UNAPPROVED"}
    var f = FileAccess.open(w + "/native_capture/checks.json", FileAccess.WRITE)
    f.store_string(JSON.stringify(receipt, "  "))
    f.close()
    print("EXP046_NATIVE_", receipt.status, " checks=", checks, " failures=", failures)
    quit(0 if failures.is_empty() else 1)

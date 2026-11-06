extends SceneTree
# Actual Godot render readback. Freeze everything except the selected oral
# channels and use the production material/compositor at source resolution.
var rig
var capture_view: SubViewport
var out_dir = ""
var records = []
var captured_curve = 0.0
var captured_shift = Vector2.ZERO
const ID = "EXP-005"

func _initialize(): call_deferred("run")

func freeze_body():
    rig.skin_material.set_shader_parameter("head_tilt", 0.0)
    rig.skin_material.set_shader_parameter("head_offset", Vector2.ZERO)
    rig.skin_material.set_shader_parameter("spine_tilt", 0.0)
    rig.skin_material.set_shader_parameter("torso_offset", Vector2.ZERO)
    rig.skin_material.set_shader_parameter("breath", 0.0)
    rig.skin_material.set_shader_parameter("controlled_breath", 0.0)
    rig.skin_material.set_shader_parameter("hair_offset", Vector2.ZERO)
    rig.skin_material.set_shader_parameter("chest_offset", Vector2.ZERO)
    rig.skin_material.set_shader_parameter("loose_hair_left", Vector2.ZERO)
    rig.skin_material.set_shader_parameter("loose_hair_right", Vector2.ZERO)
    rig.skin_material.set_shader_parameter("gaze_direction", Vector2.ZERO)

func save_frame(name, opening, width, time_value = -1.0, is_legacy = false):
    freeze_body()
    # Wait for both the facial source viewport and the production shader view.
    await process_frame
    await process_frame
    await RenderingServer.frame_post_draw
    var im = capture_view.get_texture().get_image()
    var path = out_dir.path_join(name + ".png")
    if im.is_empty() or im.save_png(path) != OK:
        push_error("Isolated mouth capture failed: " + path)
        quit(1)
        return
    records.append({"file": name + ".png", "expression": ID, "opening": opening, "width": width, "curve": captured_curve, "shift": [captured_shift.x, captured_shift.y], "time": time_value, "legacy": is_legacy, "pixels": [im.get_width(), im.get_height()]})
    print("ISOLATED_MOUTH_CAPTURE ", name)

func isolate(opening:float, width:float, curve:float = 0.0, shift:Vector2 = Vector2.ZERO):
    captured_curve = curve
    captured_shift = shift
    rig.expression_player.play({"perform_expression": ID})
    rig.expression_player.id = ID
    rig.expression_player.active = true
    rig.expression_player.paused = true
    rig.expression_player.recovering = false
    rig.expression_player.pending = {}
    rig.expression_player.values = preload("res://expression_performance.gd").zero()
    rig.expression_player.values.amount = 1.0
    rig.expression_player.values.mouth_open = opening
    rig.expression_player.values.mouth_wide = width
    rig.expression_player.values.mouth_curve = curve
    rig.expression_player.values.mouth_shift_x = shift.x
    rig.expression_player.values.mouth_shift_y = shift.y
    rig._process(0.0)

func run():
    var args = OS.get_cmdline_user_args()
    if args.is_empty(): push_error("Expected capture output directory"); quit(1); return
    out_dir = args[0]
    DirAccess.make_dir_recursive_absolute(out_dir)
    rig = load("res://motion_rig.tscn").instantiate()
    root.add_child(rig)
    await process_frame
    rig.set_process(false)
    rig.apply_controls({"reset": true, "expression": ID, "auto_blink": false, "body_follow": false, "ornament_secondary": false, "earring_secondary": false, "loose_hair_secondary": false, "pendant_secondary": false, "chest_secondary": false, "hair_secondary": false})
    rig._process(0.0)
    capture_view = SubViewport.new()
    capture_view.name = "IsolatedMouthPixelQA"
    capture_view.size = Vector2i(1136, 1384)
    capture_view.transparent_bg = true
    capture_view.render_target_update_mode = SubViewport.UPDATE_ALWAYS
    root.add_child(capture_view)
    var surface = MeshInstance2D.new()
    surface.mesh = rig.surface.mesh
    surface.texture = rig.surface.texture
    surface.material = rig.skin_material
    capture_view.add_child(surface)
    await save_frame("legacy_rest", 0.0, 0.0, -1.0, true)
    isolate(0.0, 0.0)
    await save_frame("articulated_rest", 0.0, 0.0)
    # Cover the authored envelope first. Extreme API values are recorded too,
    # but reported separately from acceptance of the current EXP-005 timeline.
    for opening in [-1.0, -0.85, -0.65, -0.34, -0.18, 0.0, 0.17, 0.24, 0.5, 1.0]:
        isolate(opening, 0.0)
        await save_frame("opening_%+.2f" % opening, opening, 0.0)
    for width in [-1.0, -0.1, 0.12, 0.18, 1.0]:
        isolate(0.0, width)
        await save_frame("width_%+.2f" % width, 0.0, width)
    for curve in [0.1, 0.18]:
        isolate(0.0, 0.0, curve)
        await save_frame("curve_%+.2f" % curve, 0.0, 0.0)
    var p = rig.expression_player.profiles[ID]
    var full_timeline = not "--quick" in args
    var count = int(ceil(float(p.duration) * 30.0)) + 1 if full_timeline else 0
    for i in range(count):
        var t = min(float(p.duration), i / 30.0)
        var sample = rig.expression_player.sample(p, t)
        isolate(sample.mouth_open, sample.mouth_wide, sample.mouth_curve, Vector2(sample.mouth_shift_x, sample.mouth_shift_y))
        await save_frame("timeline_%03d" % i, sample.mouth_open, sample.mouth_wide, t)
    var output = FileAccess.open(out_dir.path_join("captures.json"), FileAccess.WRITE)
    output.store_string(JSON.stringify({"expression": ID, "kind": "actual Godot source-resolution isolated mouth render", "full_timeline": full_timeline, "scope": "Production facial compositor and shader; all oral channels, all other motion frozen; full authored mouth timeline at 30 fps" if full_timeline else "Diagnostic oral sweeps, not full timeline acceptance", "frames": records}, "  "))
    output.close()
    print("ISOLATED_MOUTH_CAPTURE_COMPLETE frames=", records.size())
    quit(0)

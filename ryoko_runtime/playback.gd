extends Node2D
# Real Godot playback of registered cutout layers. No composited preview images.
var rig
var ids = []
var frames = 0
var playback_time = 0.0
var fps = 30
var seconds_per_expression = 3.6
var selected = -1
var header: Label
var status: Label
var pivot: Node2D
var batch = "highlights"
var log_file

func _ready():
    rig = load("res://preview.tscn").instantiate()
    pivot = Node2D.new()
    pivot.position = Vector2(284, 740)
    add_child(pivot)
    pivot.add_child(rig)
    rig.scale = Vector2(0.49, 0.49)
    rig.position = Vector2(-278.32, -678.16)
    ids = rig.emotion_eyes.keys()
    ids.sort()
    for arg in OS.get_cmdline_user_args():
        if arg.begins_with("--batch="): batch = arg.trim_prefix("--batch=")
    if batch == "highlights": ids = ["EXP-004", "EXP-042", "EXP-129", "EXP-002", "EXP-021", "EXP-061", "EXP-102", "EXP-181"]
    else:
        var start = (int(batch) - 1) * 31
        ids = ids.slice(start, start + 31)
    header = Label.new()
    header.position = Vector2(18, 10)
    header.add_theme_font_size_override("font_size", 23)
    add_child(header)
    status = Label.new()
    status.position = Vector2(18, 43)
    status.add_theme_font_size_override("font_size", 16)
    add_child(status)
    log_file = FileAccess.open("user://playback_" + batch + ".jsonl", FileAccess.WRITE)
    print("PLAYBACK_READY profiles=", rig.emotion_eyes.size(), " selected=", ids.size())

func _process(delta):
    var elapsed = float(frames) / fps if ("--write-movie" in OS.get_cmdline_args()) else playback_time
    playback_time += delta
    var index = int(elapsed / seconds_per_expression)
    if index >= ids.size():
        log_file.close()
        get_tree().quit()
        return
    var phase = fmod(elapsed, seconds_per_expression)
    if selected != index:
        selected = index
        rig.reset_neutral()
        assert(rig.set_expression(ids[index]))
        log_file.store_line(JSON.stringify({"expression":ids[index], "frame":frames, "time":elapsed}))
        print("PLAYBACK_EXPRESSION ", ids[index])
    var closed = (phase >= 0.8 and phase < 1.0) or (phase >= 2.45 and phase < 2.65)
    rig.set_blink(closed, closed)
    var speaking = phase >= 1.35 and phase < 3.0
    if speaking:
        var visemes = ["A", "E", "I", "O", "U", "neutral"]
        rig.set_mouth(visemes[int((phase - 1.35) * 7) % visemes.size()])
    else: rig.release_speech()
    # Small rigid cutout idle, not mesh deformation or head/body tracking.
    pivot.rotation = sin(elapsed * 1.8) * 0.008
    pivot.position.y = 740 + sin(elapsed * 2.4) * 1.4
    header.text = "RYOKO  /  " + ids[index] + "  /  %02d of %02d" % [index + 1, ids.size()]
    status.text = "GODOT LIVE  |  " + ("visemes" if speaking else "expression rest") + (" + blink" if closed else "")
    frames += 1

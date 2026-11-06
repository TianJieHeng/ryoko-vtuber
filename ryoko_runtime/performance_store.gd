extends RefCounted
# Explicit reusable control setups, separate from legacy head/body pose slots.
const AXES = ["head_tilt", "head_x", "head_y", "body_tilt", "body_x", "body_y", "gaze_x", "gaze_y", "brow_screen_left", "brow_screen_right"]
const KEYS = ["head_tilt", "head_x", "head_y", "body_tilt", "body_x", "body_y", "body_follow", "gaze_x", "gaze_y", "brow_screen_left", "brow_screen_right", "expression", "effects"]
const MAX_BYTES = 65536
var path = "user://rig_performances.json"
var slots = {}
var expressions: Array = []
var error_message = ""

static func valid_slot(slot) -> bool:
    return (slot is int or slot is float) and is_finite(float(slot)) and float(slot) == floor(float(slot)) and slot >= 1 and slot <= 3

func valid_snapshot(value) -> bool:
    if not value is Dictionary or value.size() != KEYS.size():return false
    for key in value:
        if key not in KEYS:return false
    if not value.body_follow is bool:return false
    for key in AXES:
        if not (value[key] is int or value[key] is float):return false
        if not is_finite(float(value[key])) or abs(float(value[key])) > 1.0:return false
    if not value.expression is String:return false
    if value.expression != "neutral" and not expressions.has(value.expression):return false
    if not preload("res://optional_effects.gd").valid(value.effects):return false
    return value.effects.size() == preload("res://optional_effects.gd").NAMES.size()

func load_disk() -> bool:
    error_message = ""
    if not FileAccess.file_exists(path):return true
    var file = FileAccess.open(path, FileAccess.READ)
    if file == null or file.get_length() > MAX_BYTES:
        error_message = "Cannot read performance file or file is too large."
        return false
    var parser = JSON.new()
    if parser.parse(file.get_as_text()) != OK:
        error_message = "Invalid performance JSON; existing file and slots left unchanged."
        return false
    var data = parser.data
    if not data is Dictionary or data.size() != 2 or not data.has("version") or not data.has("slots"):
        error_message = "Invalid performance file; existing file and slots left unchanged."
        return false
    if not (data.version is int or data.version is float) or data.version != 1 or not data.slots is Dictionary:
        error_message = "Invalid performance version or slots."
        return false
    for slot in data.slots:
        if slot not in ["1", "2", "3"] or not valid_snapshot(data.slots[slot]):
            error_message = "Invalid saved performance; existing file and slots left unchanged."
            return false
    slots = data.slots.duplicate(true)
    return true

func save_slot(slot, snapshot) -> bool:
    error_message = ""
    if not valid_slot(slot) or not valid_snapshot(snapshot):
        error_message = "Invalid performance or slot."
        return false
    var candidate = slots.duplicate(true)
    candidate[str(int(slot))] = snapshot.duplicate(true)
    var file = FileAccess.open(path + ".tmp", FileAccess.WRITE)
    if file == null:
        error_message = "Could not write performance file."
        return false
    file.store_string(JSON.stringify({"version": 1, "slots": candidate}, "  "))
    file.flush()
    var write_error = file.get_error()
    file.close()
    if write_error != OK:
        error_message = "Could not finish performance file; saved slots left unchanged."
        return false
    if DirAccess.rename_absolute(path + ".tmp", path) != OK:
        error_message = "Could not replace performance file; saved slots left unchanged."
        return false
    slots = candidate
    return true

func recall(slot) -> Dictionary:
    if not valid_slot(slot):return {}
    var snapshot = slots.get(str(int(slot)), {})
    # Validate again so edits or an outdated expression registry cannot partially
    # change the rig, release a clip, or disturb a paused performance.
    return snapshot.duplicate(true) if valid_snapshot(snapshot) else {}

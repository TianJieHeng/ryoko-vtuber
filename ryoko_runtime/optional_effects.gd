extends Node2D
# Additive overlays only: never modifies expression-authored pixels or visibility.
const NAMES = ["blush_L", "blush_R", "tear_L", "tear_R", "sweat", "anger", "sparkle"]
var state = {}
var sprites = {}

static func valid(value) -> bool:
    if not value is Dictionary:return false
    for key in value:
        if not key is String or key not in NAMES or not value[key] is bool:return false
    return true

func _ready():
    var manifest = JSON.parse_string(FileAccess.get_file_as_string("res://rig_assets/effects/manifest.json"))
    for key in NAMES:
        var entry = manifest.effects[key]
        var sprite = Sprite2D.new()
        sprite.name = key
        sprite.texture = load("res://rig_assets/effects/" + entry.file)
        sprite.centered = false
        sprite.region_enabled = true
        sprite.region_filter_clip_enabled = true
        var rect = entry.source_rect
        sprite.region_rect = Rect2(rect[0], rect[1], rect[2], rect[3])
        sprite.position = Vector2(entry.position[0], entry.position[1])
        sprite.scale = Vector2(entry.size[0] / float(rect[2]), entry.size[1] / float(rect[3]))
        sprite.visible = false
        add_child(sprite)
        sprites[key] = sprite
        state[key] = false

func apply(value) -> bool:
    if not valid(value):return false
    for key in value:
        state[key] = value[key]
        sprites[key].visible = value[key]
    return true

func reset():
    for key in NAMES:
        state[key] = false
        sprites[key].visible = false

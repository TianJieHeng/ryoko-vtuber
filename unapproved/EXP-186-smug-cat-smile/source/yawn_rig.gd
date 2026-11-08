extends "res://expression_rig.gd"
## Compatibility entry for existing review scripts/tests. All playback and validation is shared.
const DURATION=5.8
func sample_yawn(time)->Dictionary:return sample_expression("EXP-163",time)
func _ready():
    super._ready()
    _write_compatibility_labels()
func _write_pose():
    super._write_pose()
    _write_compatibility_labels()
func _write_compatibility_labels():
    hud.text="Ryoko / yawn · separate objects"
    hint.text="Y yawn · Space release · 0 reset"
    pose_status.text="EXP-163 / "+performance_phase
func _unhandled_key_input(event):
    if event is InputEventKey and event.pressed and not event.echo and event.keycode==KEY_Y:
        play_expression("EXP-163")
    else:super._unhandled_key_input(event)

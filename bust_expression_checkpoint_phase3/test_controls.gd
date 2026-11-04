extends SceneTree
var checks = 0
func check(value, message):
    checks += 1
    if not value:
        push_error(message)
        quit(1)
func _initialize():
    call_deferred("run_tests")
func run_tests():
    var rig = load("res://preview.tscn").instantiate()
    root.add_child(rig)
    await process_frame
    check(rig.mouths.size() == 6, "Six independently registered mouth sprites required")
    check(rig.blinks.size() == 2, "Two independent eyelid sprites required")
    for state in ["neutral", "A", "E", "I", "O", "U"]:
        check(rig.set_mouth(state), "Mouth setter failed")
        for key in rig.mouths:
            check(rig.mouths[key].visible == (key == state), "Exclusive mouth state broken")
            check(rig.mouths[key].texture != null, "Missing mouth texture")
    check(not rig.set_mouth("INVALID"), "Invalid state must be rejected")
    rig._handle_command({"blink_L": 1.0, "blink_R": 0.0, "viseme": "O"})
    check(rig.blinks["L"].visible and not rig.blinks["R"].visible, "Independent blink failed")
    check(rig.mouth_state == "O", "Blink must preserve mouth command")
    rig._handle_command({"blink": 1.0, "mouth": "E"})
    check(rig.blinks["L"].visible and rig.blinks["R"].visible, "Paired blink failed")
    check(rig.mouth_state == "E", "Mouth independent of paired blink")
    rig._handle_command({"lip_sync": 0.0})
    check(rig.mouth_state == "neutral", "Silent fallback failed")
    rig._handle_command({"lip_sync": 0.2})
    check(rig.mouth_state == "E", "Quiet fallback failed")
    rig._handle_command({"lip_sync": 0.7})
    check(rig.mouth_state == "A", "Loud fallback failed")
    rig.reset_neutral()
    check(rig.mouth_state == "neutral" and not rig.blinks["L"].visible and not rig.blinks["R"].visible, "Reset failed")
    print("FACIAL_CONTROL_CHECKS_PASS count=", checks)
    quit(0)

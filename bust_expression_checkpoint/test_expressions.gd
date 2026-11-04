extends SceneTree
var checks = 0
var failed = false
func check(value, message):
    checks += 1
    if not value:
        failed = true
        push_error(message)
func _initialize(): call_deferred("run_tests")
func run_tests():
    var rig = load("res://preview.tscn").instantiate()
    root.add_child(rig)
    await process_frame
    for id in ["EXP-002", "EXP-041", "EXP-061"]:
        rig.reset_neutral()
        check(rig.set_expression(id), "Expression must exist")
        check(rig.emotion_mouths[id].visible, "Emotion rest mouth visible")
        for state in ["neutral", "A", "E", "I", "O", "U"]:
            rig.set_mouth(state)
            check(rig.mouths[state].visible, "Speech mouth active")
            check(not rig.emotion_mouths[id].visible, "Rest mouth hidden during speech")
            check(rig.expression == id, "Speech must preserve emotion")
            for left in [0,1]:
                for right in [0,1]:
                    rig.set_blink(left,right)
                    check(rig.emotion_blinks[id]["L"].visible == bool(left), "Left blink")
                    check(rig.emotion_blinks[id]["R"].visible == bool(right), "Right blink")
                    check(rig.emotion_eyes[id]["L"].visible != bool(left), "No duplicate left eye")
                    check(rig.emotion_eyes[id]["R"].visible != bool(right), "No duplicate right eye")
                    check(rig.mouths[state].visible, "Blink preserves speech")
                    check(not rig.blinks["L"].visible and not rig.blinks["R"].visible, "Neutral blink must not overwrite emotion")
            rig.release_speech()
            check(rig.emotion_mouths[id].visible, "Restore emotion rest after speech")
            for key in rig.mouths: check(not rig.mouths[key].visible, "No double mouth after speech")
        rig._handle_command({"lip_sync":0.7})
        check(rig.mouths["A"].visible, "Amplitude speech")
        rig._handle_command({"lip_sync":0.0})
        check(rig.emotion_mouths[id].visible, "Silence restores emotion rest")
        rig._handle_command({"viseme":"O","speech_active":false})
        check(rig.emotion_mouths[id].visible, "Explicit speech release")
    rig.set_mouth("E")
    rig.set_expression("EXP-041")
    check(rig.mouths["E"].visible, "Changing emotion preserves active speech")
    check(not rig.set_expression("invalid"), "Invalid emotion rejected")
    rig.reset_neutral()
    check(rig.expression == "neutral" and rig.mouths["neutral"].visible, "Reset neutral")
    for id in rig.emotion_mouths: check(not rig.emotion_mouths[id].visible, "Hide all emotion rest mouths")
    print("EXPRESSION_CONTROL_CHECKS_", "FAIL" if failed else "PASS", " count=", checks)
    quit(1 if failed else 0)

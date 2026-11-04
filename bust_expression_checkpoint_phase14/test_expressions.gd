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
    for id in ["EXP-002", "EXP-041", "EXP-061", "EXP-021", "EXP-102", "EXP-181", "EXP-123", "EXP-142", "EXP-163", "EXP-023", "EXP-081", "EXP-192", "EXP-005", "EXP-161", "EXP-197", "EXP-070", "EXP-094", "EXP-185", "EXP-045", "EXP-104", "EXP-022", "EXP-052", "EXP-096", "EXP-083", "EXP-124", "EXP-184", "EXP-191", "EXP-033", "EXP-087", "EXP-187", "EXP-078", "EXP-148", "EXP-193", "EXP-047", "EXP-076", "EXP-177", "EXP-082", "EXP-088", "EXP-164", "EXP-006", "EXP-099", "EXP-089"]:
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
                    for fx in rig.emotion_effects["EXP-023"]: check(fx.visible == (id == "EXP-023"), "Sobbing cheek flush survives speech/blink")
                    for fx in rig.emotion_effects["EXP-081"]: check(fx.visible == (id == "EXP-081"), "Disgust nose survives speech/blink")
                    for fx in rig.emotion_effects["EXP-192"]: check(not fx.visible, "Puffed contour deflates during speech")
                    for fx in rig.emotion_effects["EXP-094"]: check(fx.visible == (id == "EXP-094"), "Pre-sneeze nose survives speech/blink")
                    for fx in rig.emotion_effects["EXP-185"]: check(fx.visible == (id == "EXP-185"), "Admiration blush survives speech/blink")
                    for fx in rig.emotion_effects["EXP-022"]: check(fx.visible == (id == "EXP-022"), "Holding-back-tears blush survives speech/blink")
                    for effect_id in ["EXP-052", "EXP-096", "EXP-083"]:
                        for fx in rig.emotion_effects[effect_id]: check(fx.visible == (id == effect_id), "New facial effects survive speech/blink")
                    for fx in rig.emotion_effects["EXP-197"]: check(fx.visible == (id == "EXP-197"), "Kiss cheek flush survives speech/blink")
                    for fx in rig.emotion_effects["EXP-142"]: check(fx.visible == (id == "EXP-142"), "Blush persists only during flustered expression")
                    check(not rig.blinks["L"].visible and not rig.blinks["R"].visible, "Neutral blink must not overwrite emotion")
            rig.release_speech()
            check(rig.emotion_mouths[id].visible, "Restore emotion rest after speech")
            for fx in rig.emotion_effects["EXP-192"]: check(fx.visible == (id == "EXP-192"), "Puffed contour restores with emotion rest")
            for key in rig.mouths: check(not rig.mouths[key].visible, "No double mouth after speech")
        rig._handle_command({"lip_sync":0.7})
        check(rig.mouths["A"].visible, "Amplitude speech")
        rig._handle_command({"lip_sync":0.0})
        check(rig.emotion_mouths[id].visible, "Silence restores emotion rest")
        rig._handle_command({"viseme":"O","speech_active":false})
        check(rig.emotion_mouths[id].visible, "Explicit speech release")
    for closed_id in ["EXP-005", "EXP-197", "EXP-094", "EXP-096", "EXP-177", "EXP-082"]:
        rig.set_expression(closed_id)
        rig.release_speech()
        rig.set_blink(1,1)
        rig.set_blink(0,0)
        for side in ["L", "R"]:
            check(rig.emotion_eyes[closed_id][side].texture.get_image().get_data() == rig.emotion_blinks[closed_id][side].texture.get_image().get_data(), "Laughter/kiss eyes remain closed on blink release")
    rig.set_expression("EXP-161")
    for side in ["L", "R"]:
        check(rig.emotion_eyes["EXP-161"][side].texture.get_image().get_data() != rig.emotion_blinks["EXP-161"][side].texture.get_image().get_data(), "Sleepy lids have distinct fully closed blink")
    for new_id in ["EXP-045", "EXP-104", "EXP-022", "EXP-124", "EXP-184", "EXP-191", "EXP-033", "EXP-087", "EXP-187", "EXP-078", "EXP-148", "EXP-193", "EXP-047", "EXP-076", "EXP-088", "EXP-164", "EXP-006", "EXP-099", "EXP-089"]:
        rig.set_expression(new_id)
        rig.release_speech()
        rig.set_blink(1,1)
        for side in ["L", "R"]:
            check(not rig.emotion_eyes[new_id][side].visible, "Blink hides open side-gaze/wet-eye layers")
            check(rig.emotion_eyes[new_id][side].texture.get_image().get_data() != rig.emotion_blinks[new_id][side].texture.get_image().get_data(), "Dedicated new blink differs from open eyes")
        rig.set_blink(0,0)
        for side in ["L", "R"]: check(rig.emotion_eyes[new_id][side].visible, "Blink release restores exact emotion eyes")
    rig.set_expression("EXP-083")
    rig.release_speech()
    rig.set_blink(1,1)
    rig.set_blink(0,0)
    check(rig.emotion_eyes["EXP-083"]["R"].texture.get_image().get_data() == rig.emotion_blinks["EXP-083"]["R"].texture.get_image().get_data(), "Bad taste viewer-left eye stays shut")
    check(rig.emotion_eyes["EXP-083"]["L"].texture.get_image().get_data() != rig.emotion_blinks["EXP-083"]["L"].texture.get_image().get_data(), "Bad taste viewer-right has full blink closure")
    rig.set_expression("EXP-023")
    rig.release_speech()
    for side in ["L", "R"]:
        check(rig.emotion_eyes["EXP-023"][side].texture.get_image().get_data() == rig.emotion_blinks["EXP-023"][side].texture.get_image().get_data(), "Sobbing eyes remain shut")
    rig.set_expression("EXP-163")
    rig.release_speech()
    for side in ["L", "R"]:
        check(rig.emotion_eyes["EXP-163"][side].texture.get_image().get_data() == rig.emotion_blinks["EXP-163"][side].texture.get_image().get_data(), "Yawn eyes remain shut through blink")
    rig.set_blink(1,1)
    rig.set_blink(0,0)
    check(rig.expression == "EXP-163" and rig.emotion_mouths["EXP-163"].visible, "Blink release restores yawn rest")
    rig.set_expression("EXP-181")
    rig.release_speech()
    rig.set_blink(0,0)
    var closed_at_rest = rig.emotion_eyes["EXP-181"]["L"].texture.get_image().get_data()
    var closed_on_blink = rig.emotion_blinks["EXP-181"]["L"].texture.get_image().get_data()
    check(closed_at_rest == closed_on_blink, "Wink viewer-right remains visually closed through blink")
    check(rig.emotion_eyes["EXP-181"]["L"].visible, "Wink resting layer visible after release")
    rig.set_blink(1,1)
    rig.set_blink(0,0)
    check(rig.emotion_eyes["EXP-181"]["L"].visible and rig.expression == "EXP-181", "Blink release restores wink rather than neutral open eyes")
    rig.set_mouth("E")
    rig.set_expression("EXP-041")
    check(rig.mouths["E"].visible, "Changing emotion preserves active speech")
    check(not rig.set_expression("invalid"), "Invalid emotion rejected")
    rig.reset_neutral()
    check(rig.expression == "neutral" and rig.mouths["neutral"].visible, "Reset neutral")
    for id in rig.emotion_mouths: check(not rig.emotion_mouths[id].visible, "Hide all emotion rest mouths")
    print("EXPRESSION_CONTROL_CHECKS_", "FAIL" if failed else "PASS", " count=", checks)
    quit(1 if failed else 0)

extends SceneTree
var rig
var elapsed=0.0
var stage=-1
var next_sample=0.0
func _initialize():call_deferred("setup")
func setup():
    rig=load("res://motion_rig.tscn").instantiate();root.add_child(rig)
    await process_frame;rig.set_process(false)
    rig.apply_controls({"reset":true,"auto_blink":false,"body_follow":false})
func _process(delta):
    if rig==null or not rig.rig_ready:return false
    elapsed+=delta
    var next=0 if elapsed<2 else (1 if elapsed<5 else (2 if elapsed<8 else (3 if elapsed<11 else (4 if elapsed<14 else (5 if elapsed<17 else (6 if elapsed<20 else (7 if elapsed<23 else (8 if elapsed<26 else 9))))))))
    var labels=["NEUTRAL / original hair at rest","HEAD LEFT / outer tips follow through","HEAD RIGHT / independent lower hair response","TORSO / roots follow the existing rig","HOLD / settles without idle oscillation","OFF / original rigid lower hair","ON / outer tips lag this reversal","EXISTING EXPRESSION / blink and mouth retained","COMBINED / gaze, brows, breath, ornaments","RESET / quiet neutral"]
    if next!=stage:
        stage=next
        match stage:
            0:rig.apply_controls({"head_tilt":0,"body_tilt":0,"loose_hair_secondary":true})
            1:rig.apply_controls({"head_tilt":-.95,"head_x":-.5})
            2:rig.apply_controls({"head_tilt":.95,"head_x":.5})
            3:rig.apply_controls({"head_tilt":-.55,"body_tilt":.9,"body_x":.4,"head_x":0})
            4:rig.apply_controls({"head_tilt":.6,"body_tilt":.3,"body_x":0})
            5:rig.apply_controls({"loose_hair_secondary":false,"head_tilt":-.95,"body_tilt":0,"head_x":-.5})
            6:rig.apply_controls({"loose_hair_secondary":true,"head_tilt":.95,"head_x":.5})
            7:rig.apply_controls({"expression":"EXP-041","mouth":"A","eye_screen_left":1,"head_tilt":-.7,"head_x":-.4,"body_tilt":.3})
            8:rig.apply_controls({"expression":"neutral","mouth":"REST","release_eye_controls":true,"head_tilt":.7,"head_x":0,"look_x":.7,"look_y":-.3,"brow_raise":.6,"breath_trigger":true})
            9:rig.apply_controls({"reset":true,"auto_blink":false,"body_follow":false})
        print("LOOSE_HAIR_STAGE ",JSON.stringify({"wall":elapsed,"stage":stage,"label":labels[stage]}))
    rig._process(delta)
    rig.hud.text="RYOKO / LOWER SIDE-LOCK MOTION"
    rig.hint.text=labels[stage]
    rig.pose_status.text="Original pixels · pinned roots · bounded outer-tip follow-through"
    if elapsed>=next_sample:
        var left=rig.loose_hair.screen_left.offset;var right=rig.loose_hair.screen_right.offset
        print("LOOSE_HAIR_SAMPLE ",JSON.stringify({"wall":elapsed,"stage":stage,"enabled":rig.loose_hair_enabled,"left":[left.x,left.y],"right":[right.x,right.y]}))
        next_sample+=.25
    if elapsed>=29:print("LOOSE_HAIR_REVIEW_COMPLETE");quit()
    return false

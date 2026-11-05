extends SceneTree
var rig
var wall=0.0
var ready=false
var stage=-1
var next_sample=0.0
func _initialize():call_deferred("setup")
func setup():
    rig=load("res://motion_rig.tscn").instantiate();root.add_child(rig)
    await process_frame;rig.set_process(false)
    rig.apply_controls({"reset":true,"auto_blink":false,"body_follow":false,"earring_secondary":false})
    ready=true
func _process(delta):
    if not ready:return false
    wall+=delta
    var next=0 if wall<2 else (1 if wall<4 else (2 if wall<7 else (3 if wall<10 else (4 if wall<13 else (5 if wall<16 else (6 if wall<18 else (7 if wall<20 else (8 if wall<23 else 9))))))))
    var labels=["OFF / original earrings", "ON / exact neutral source", "HEAD LEFT / pendants hang from ears", "HEAD RIGHT / independent follow-through", "TORSO / attachment follows head and body", "HOLD / quiet settle, no idle swing", "OFF / original tilted attachment", "ON / gravity follows the same held pose", "COMBINED / look, brows, breath, mouth", "RESET / quiet neutral"]
    if next!=stage:
        stage=next
        var actions=[
            {"earring_secondary":false},
            {"earring_secondary":true},
            {"head_tilt":-.8,"head_x":-.4},
            {"head_tilt":.8,"head_x":.4},
            {"head_tilt":-.3,"head_x":0,"body_tilt":.65,"body_x":.35},
            {"head_tilt":.7,"body_tilt":.3,"body_x":0},
            {"earring_secondary":false},
            {"earring_secondary":true},
            {"head_tilt":0,"body_tilt":0,"look_x":-.8,"look_y":-.2,"brow_raise":.65,"breath_trigger":true,"mouth":"A"},
            {"reset":true,"auto_blink":false,"body_follow":false}
        ]
        rig.apply_controls(actions[stage])
        print("EARRING_STAGE ",JSON.stringify({"stage":stage,"wall":wall,"label":labels[stage]}))
    rig._process(delta)
    rig.hud.text="RYOKO / INDEPENDENT EARRINGS"
    rig.hint.text=labels[stage]
    rig.pose_status.text="Fixed studs · rigid pendants · bounded gravity and sway"
    if wall>=next_sample:
        next_sample+=.25
        var left=rig.earrings.screen_left;var right=rig.earrings.screen_right
        print("EARRING_SAMPLE ",JSON.stringify({"wall":wall,"stage":stage,"enabled":rig.earrings_enabled,"left_angle":left.angle,"right_angle":right.angle,"left_swing":left.swing,"right_swing":right.swing,"left_pivot":[rig.earring_pivots.screen_left.position.x,rig.earring_pivots.screen_left.position.y],"right_pivot":[rig.earring_pivots.screen_right.position.x,rig.earring_pivots.screen_right.position.y]}))
    if wall>=26:print("EARRING_REVIEW_COMPLETE");quit()
    return false

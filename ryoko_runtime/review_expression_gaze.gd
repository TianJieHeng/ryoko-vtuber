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
    var next=0 if elapsed<2 else (1 if elapsed<4 else (2 if elapsed<6 else (3 if elapsed<8 else (4 if elapsed<9 else (5 if elapsed<10 else (6 if elapsed<12 else (7 if elapsed<14 else (8 if elapsed<16 else (9 if elapsed<18 else (10 if elapsed<20 else (11 if elapsed<22 else (12 if elapsed<24 else 13))))))))))))
    var labels=["NEUTRAL / approved gaze unchanged","EXISTING EXP-064 / original wide eye shape","EXP-064 / rigid iris glance left","EXP-064 / rigid iris glance right","EXP-064 / eyes up","EXP-064 / eyes down","EXP-064 / independent blink, mouth and head","EXISTING EXP-189 / its own iris artwork","EXP-189 / glance left","EXP-189 / glance right","EXP-189 / eyes-first attention","EXP-189 / blink and speech remain independent","OTHER EXPRESSIONS / authored eyes preserved","RESET / approved neutral rendering"]
    if next!=stage:
        stage=next
        match stage:
            0:pass
            1:rig.apply_controls({"expression":"EXP-064","gaze_x":0,"gaze_y":0})
            2:rig.apply_controls({"gaze_x":-1})
            3:rig.apply_controls({"gaze_x":1})
            4:rig.apply_controls({"gaze_x":0,"gaze_y":-1})
            5:rig.apply_controls({"gaze_y":1})
            6:rig.apply_controls({"gaze_x":.7,"gaze_y":0,"eye_screen_left":1,"mouth":"A","head_tilt":.5})
            7:rig.apply_controls({"expression":"EXP-189","gaze_x":0,"gaze_y":0,"release_eye_controls":true,"mouth":"REST","head_tilt":0})
            8:rig.apply_controls({"gaze_x":-1})
            9:rig.apply_controls({"gaze_x":1})
            10:rig.apply_controls({"gaze_x":0,"look_x":-.7,"look_y":.4,"brow_raise":.8})
            11:rig.apply_controls({"look_release":true,"gaze_x":.7,"eye_screen_right":1,"mouth":"A","head_tilt":-.4,"body_tilt":.2})
            12:rig.apply_controls({"expression":"EXP-041","gaze_x":-1,"release_eye_controls":true,"mouth":"REST"})
            13:rig.apply_controls({"reset":true,"auto_blink":false,"body_follow":false})
        print("EXPRESSION_GAZE_STAGE ",JSON.stringify({"wall":elapsed,"stage":stage,"label":labels[stage]}))
    rig._process(delta)
    rig.hud.text="RYOKO / GAZE ON EXISTING EXPRESSIONS"
    rig.hint.text=labels[stage]
    rig.pose_status.text="Only EXP-064 and EXP-189 added · no new expressions"
    if elapsed>=next_sample:
        var open=rig.skin_material.get_shader_parameter("gaze_open")
        print("EXPRESSION_GAZE_SAMPLE ",JSON.stringify({"wall":elapsed,"stage":stage,"expression":rig.face.expression,"profile":rig.gaze_profile_name,"gaze":[rig.gaze.current.x,rig.gaze.current.y],"open":[open.x,open.y],"brow_enabled":rig.skin_material.get_shader_parameter("brow_enabled")}))
        next_sample+=.25
    if elapsed>=28:print("EXPRESSION_GAZE_REVIEW_COMPLETE");quit()
    return false

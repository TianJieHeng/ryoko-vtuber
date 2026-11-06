extends SceneTree
var checks=0
var failed=0
func verify(ok,message):
    checks+=1
    if not ok:failed+=1;push_error("LAUGHTER: "+message)
func _initialize():call_deferred("run")
func run():
    var rig=load("res://motion_rig.tscn").instantiate();root.add_child(rig)
    await process_frame;rig.set_process(false)
    verify(rig.face.articulated_mouths.has("EXP-005"),"separate oral layers loaded")
    rig.apply_controls({"reset":true,"auto_blink":false})
    verify(rig.apply_controls({"perform_expression":"EXP-005"}),"AI command starts laughter")
    var widths={};var heights={};var peak_seen=false
    for i in range(190):
        rig._process(1.0/30.0)
        if rig.expression_player.active:
            var entry=rig.face.articulated_mouths["EXP-005"]
            var scale=entry.material.get_shader_parameter("oral_scale")
            verify(scale.x>=.82 and scale.x<=1.160001 and scale.y>=.099999 and scale.y<=1.000001,"bounded oral geometry")
            verify(rig.skin_material.get_shader_parameter("expression_mouth")==Vector3.ZERO,"no whole-face mouth warp")
            verify(rig.face.emotion_mouths["EXP-005"].material==entry.material,"isolated mouth actually rendered")
            widths[round(scale.x*10000)]=true;heights[round(scale.y*10000)]=true
            if scale.distance_to(Vector2.ONE)<.00001:peak_seen=true
    verify(widths.size()>10 and heights.size()>20,"genuine temporal oral movement")
    verify(peak_seen,"source-exact peak reached")
    verify(not rig.expression_player.active and rig.face.expression=="neutral","complete natural recovery")
    verify(rig.face.emotion_mouths["EXP-005"].material==null,"original material restored")
    rig.apply_controls({"perform_expression":"EXP-005"})
    for i in range(32):rig._process(1.0/30.0)
    rig.apply_controls({"expression_paused":true})
    var old=rig.expression_player.values.duplicate(true)
    for i in range(10):rig._process(1.0/30.0)
    verify(rig.expression_player.values==old,"pause holds authored state")
    rig.apply_controls({"expression_paused":false,"mouth":"E"})
    rig._process(1.0/30.0)
    verify(rig.face.mouths.E.visible and not rig.face.emotion_mouths["EXP-005"].visible,"live speech remains independent")
    rig.apply_controls({"mouth":"REST"});rig._process(1.0/30.0)
    verify(rig.face.emotion_mouths["EXP-005"].visible,"emotion mouth returns after speech")
    verify(not rig.apply_controls({"perform_expression":"EXP-invalid"}),"unknown request rejected")
    verify(rig.expression_player.active,"invalid request preserves laughter")
    rig.apply_controls({"expression_cancel":true})
    for i in range(15):rig._process(1.0/30.0)
    verify(not rig.expression_player.active and rig.face.active_articulated_mouth=="","cancel releases separate layer")
    rig.apply_controls({"perform_expression":"EXP-005"});rig._process(.3)
    rig.apply_controls({"expression":"EXP-005"})
    verify(not rig.expression_player.active and rig.face.emotion_mouths["EXP-005"].material==null,"legacy static selection takes over")
    rig.apply_controls({"perform_expression":"EXP-005"});rig._process(.3)
    rig.apply_controls({"reset":true})
    verify(rig.face.expression=="neutral" and rig.face.active_articulated_mouth=="","reset restores original neutral")
    print("HEARTY_LAUGHTER_CHECKS_", "PASS" if failed==0 else "FAIL", " count=",checks," failures=",failed)
    quit(1 if failed else 0)

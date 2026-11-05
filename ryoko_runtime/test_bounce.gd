extends SceneTree
func _initialize():call_deferred("run")
func run():
    var rig=load("res://motion_rig.tscn").instantiate();root.add_child(rig);await process_frame;rig.set_process(false)
    rig.apply_controls({"body_tilt":0});rig._process(.016)
    rig.apply_controls({"bounce":true})
    var peak_body=0.0;var peak_chest=0.0;var reverse=false
    for i in range(300):
        rig._process(1.0/60)
        peak_body=maxf(peak_body,abs(rig.bounce_position));peak_chest=maxf(peak_chest,abs(rig.chest_offset.y))
        if rig.chest_offset.y<-.1:reverse=true
        assert(rig.chest_offset.length()<=8.0001)
    assert(peak_body>10 and peak_body<25)
    assert(peak_chest>3 and peak_chest<=8)
    assert(reverse)
    assert(abs(rig.bounce_position)<.001 and rig.chest_offset.length()<.001)
    print("BOUNCE_CHECKS_PASS body_peak=",peak_body," chest_peak=",peak_chest," settled=true")
    quit()

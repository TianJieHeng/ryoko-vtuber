extends SceneTree
var checks=0
var failures=0
func verify(v,label):
    checks+=1
    if not v:push_error(label);failures+=1
func _initialize():call_deferred("run")
func run():
    var rig=load("res://motion_rig.tscn").instantiate();root.add_child(rig);await process_frame;rig.set_process(false)
    rig.apply_controls({"body_tilt":0,"body_y":0,"head_tilt":0})
    for i in range(120):rig._process(1.0/60)
    verify(rig.chest_offset==Vector2.ZERO,"stationary torso has no oscillation")
    rig.apply_controls({"head_tilt":1})
    for i in range(120):rig._process(1.0/60);verify(rig.chest_offset==Vector2.ZERO,"independent head cannot drive chest")
    rig.apply_controls({"body_tilt":1,"body_y":1})
    var peak=0.0
    for i in range(60):
        rig._process(1.0/60);peak=maxf(peak,rig.chest_offset.length());verify(rig.chest_offset.length()<=8.0001,"bounded motion")
    verify(peak>.2,"torso movement produces secondary lag")
    for i in range(240):rig._process(1.0/60)
    verify(rig.chest_offset.length()<.0001,"held torso settles")
    for point in [Vector2(300,920),Vector2(830,920),Vector2(568,900),Vector2(568,1384),Vector2(50,1100),Vector2(1080,1100)]:verify(rig.chest_weight(point)==0,"shoulders neck outer silhouette and base preserved")
    verify(rig.chest_weight(Vector2(568,1130))==1,"central chest region weighted")
    for point in [Vector2(350,1100),Vector2(786,1100),Vector2(300,1250),Vector2(836,1250),Vector2(568,1270)]:verify(rig.chest_weight(point)==1,"whole chest and shirt move together")
    verify(rig.chest_weight(Vector2(200,1150))>.5,"outer chest has broad feathering")
    rig.apply_controls({"body_tilt":-1})
    rig._process(.033)
    verify(rig.chest_offset.length()>.1,"reverse torso drives motion")
    rig.apply_controls({"chest_secondary":false});rig._process(.033)
    verify(rig.chest_offset==Vector2.ZERO,"disabled restores exact rigid torso")
    rig.apply_controls({"chest_secondary":true})
    for delta in [.008,.016,.033,.1,.8]:
        rig.apply_controls({"body_tilt":1})
        for i in range(20):rig._process(delta);verify(rig.chest_offset.is_finite() and rig.chest_offset.length()<=8.0001,"variable frame stability")
    if failures==0:print("CHEST_SECONDARY_CHECKS_PASS count=",checks," peak_source_pixels=",peak)
    quit(1 if failures else 0)

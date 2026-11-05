extends SceneTree
var count=0
var failures=0
func check(condition,label):
    count+=1
    if not condition:push_error(label);failures+=1
func _initialize():call_deferred("run")
func run():
    var driver=load("res://audio_mouth_driver.gd").new();root.add_child(driver)
    driver.deterministic=true
    check(driver.load_wav("res://audio_fixture.wav"),"fixture loads")
    check(abs(driver.duration-12.0)<0.01,"duration")
    check(driver.play(),"play")
    var seen={}
    for i in range(360):
        var shape=driver.step(1.0/30.0);seen[shape]=true
        check(driver.level>=0.0 and driver.level<=1.0,"bounds")
        if i in [82,172,262,345]:check(shape=="REST","silence returns to rest")
    check(seen.has("I") and seen.has("E") and seen.has("A"),"three opening sizes")
    driver.step(0.1);check(not driver.active,"EOF releases")
    driver.set_level(4.0);driver.step(.5);check(driver.raw_level==1.0,"high clamp")
    driver.set_level(-3.0);driver.step(1.0);check(driver.mouth=="REST","low clamp")
    driver.set_level(NAN);driver.step(1.0);check(is_finite(driver.level),"NaN safe")
    driver.stop();check(driver.level==0.0 and not driver.active,"stop resets")
    var rig=load("res://motion_rig.tscn").instantiate();root.add_child(rig);await process_frame
    rig.set_process(false)
    rig.apply_controls({"audio_level":.7,"head_tilt":.2});rig._process(.2)
    check(rig.face.mouth_state=="A","level API drives face")
    rig.apply_controls({"mouth":"O"});check(not rig.audio_mouth.active and rig.face.mouth_state=="O","manual mouth wins")
    rig.apply_controls({"audio_level":.7});rig.apply_controls({"reset":true});check(not rig.audio_mouth.active and rig.face.mouth_state=="neutral","rig reset stops audio")
    if failures==0:print("AUDIO_MOUTH_CHECKS_PASS count=",count)
    quit(1 if failures else 0)

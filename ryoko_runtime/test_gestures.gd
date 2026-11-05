extends SceneTree
var checks=0
var failures=0
func verify(value,label):
    checks+=1
    if not value:push_error(label);failures+=1
func _initialize():call_deferred("run")
func run():
    var driver=load("res://gesture_driver.gd").new()
    for id in ["acknowledge","greet"]:
        verify(driver.trigger(id),"valid trigger")
        var peak=0.0
        for i in range(120):
            driver.sample(1.0/30)
            peak=max(peak,driver.head.length())
            verify(driver.head.abs().max_axis_index()>=0 and driver.head.length()<1.1,"bounded offsets")
        verify(peak>.2,"gesture moved")
        verify(driver.active=="" and driver.head==Vector3.ZERO and driver.body==Vector3.ZERO,"one shot returns")
    driver.trigger("greet");driver.sample(.5);var active=driver.active
    verify(not driver.trigger("unknown") and driver.active==active,"invalid leaves current alone")
    driver.trigger("greet",NAN);driver.sample(.5);verify(driver.head==Vector3.ZERO,"finite strength")
    driver.trigger("greet",99);verify(driver.strength==1.0,"strength clamp")
    driver.cancel();verify(driver.active=="","cancel")
    var rig=load("res://motion_rig.tscn").instantiate();root.add_child(rig);await process_frame;rig.set_process(false)
    rig.apply_controls({"head_tilt":.2,"body_tilt":-.15,"gesture":"greet"})
    for i in range(180):rig._process(1.0/30)
    verify(is_equal_approx(rig.target.x,.2) and is_equal_approx(rig.body_target.x,-.15),"live targets unmodified")
    verify(rig.current.distance_to(rig.target)<.0001 and rig.body_current.distance_to(rig.body_target)<.0001,"returns to live pose")
    rig.apply_controls({"gesture":"greet"});rig._process(.4);var prior=rig.current
    rig.apply_controls({"gesture_cancel":true});rig._process(.001)
    verify(rig.current.distance_to(prior)<.02,"cancel eased not snap")
    rig.apply_controls({"gesture":"acknowledge","audio_level":.8});rig._process(.2)
    verify(rig.face.mouth_state=="A" and rig.gestures.active=="acknowledge","audio coexistence")
    rig.apply_controls({"reset":true});verify(rig.gestures.active=="","reset clears")
    rig.set_process(true)
    var key=InputEventKey.new();key.keycode=KEY_G;key.physical_keycode=KEY_G;key.pressed=true;Input.parse_input_event(key)
    await process_frame;await process_frame
    verify(rig.gestures.active=="greet","physical trigger")
    if failures==0:print("GESTURE_CHECKS_PASS count=",checks)
    quit(1 if failures else 0)

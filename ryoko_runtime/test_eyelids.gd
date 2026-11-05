extends SceneTree
var checks=0
var failures=0
func verify(value,label):
    checks+=1
    if not value:push_error(label);failures+=1
func _initialize():call_deferred("run")
func run():
    var d=load("res://eyelid_driver.gd").new()
    verify(d.resolve(0)==Vector2.ZERO,"rest")
    for side in ["screen_left","screen_right","both"]:
        d.reset();verify(d.trigger(side),"trigger")
        var expected=Vector2(1,0) if side=="screen_left" else (Vector2(0,1) if side=="screen_right" else Vector2.ONE)
        verify(d.resolve(0)==expected,"explicit screen mapping")
        for i in range(9):d.step(1.0/30)
        verify(not d.busy() and d.resolve(0)==Vector2.ZERO,"one shot release")
    verify(not d.trigger("left"),"ambiguous side rejected")
    d.set_hold("screen_left",1);d.set_hold("screen_right",0)
    for i in range(100):d.step(.1);verify(d.resolve(1)==Vector2(1,0),"hold overrides shared")
    d.reset();d.trigger("both",NAN);verify(d.wink_left==.28,"NaN duration")
    d.reset();d.trigger("both",99);verify(d.wink_left==.8,"duration clamp")
    var rig=load("res://motion_rig.tscn").instantiate();root.add_child(rig);await process_frame;rig.set_process(false)
    rig.next_blink=0;rig.apply_controls({"wink":"screen_left"});rig._process(.05)
    verify(rig.face.blink_right and not rig.face.blink_left,"viewer-left uses R artwork")
    verify(rig.face.blinks.R.visible and not rig.face.blinks.L.visible,"visible sprites match")
    verify(rig.next_blink>rig.clock_time,"auto blink deferred")
    rig.apply_controls({"release_eye_controls":true,"wink":"screen_right"});rig._process(.05)
    verify(rig.face.blink_left and not rig.face.blink_right,"viewer-right uses L artwork")
    rig.apply_controls({"release_eye_controls":true,"eye_screen_left":1,"eye_screen_right":0,"gesture":"greet","audio_level":.8});rig._process(.2)
    verify(rig.face.blink_right and not rig.face.blink_left and rig.face.mouth_state=="A" and rig.gestures.active=="greet","controls coexist")
    rig.apply_controls({"reset":true});verify(not rig.eyelids.busy(),"reset")
    rig.set_process(true)
    var key=InputEventKey.new();key.keycode=KEY_K;key.physical_keycode=KEY_K;key.pressed=true;Input.parse_input_event(key)
    await process_frame;await process_frame
    verify(rig.face.blink_left and not rig.face.blink_right,"keyboard screen-right")
    if failures==0:print("EYELID_CHECKS_PASS count=",checks)
    quit(1 if failures else 0)

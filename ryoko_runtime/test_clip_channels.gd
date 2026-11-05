extends SceneTree
# Headless integration coverage for opt-in extended timed clip channels.
var checks=0
var failures=0
var serial=0
const AXES=["gaze_x","gaze_y","brow_raise","brow_screen_left","brow_screen_right","look_x","look_y"]
const LEVELS=["breath_level","breath_strength"]
const FLAGS=["breath_trigger","breath_cancel","look_release","ornament_secondary"]
func verify(value,label):
    checks+=1
    if not value:
        failures+=1
        push_error("CLIP_CHANNELS: "+label)
func data(controls,duration=3.0):
    return {"version":1,"duration":duration,"cues":[{"time":0.0,"controls":controls}]}
func fixture(value):
    serial+=1
    var path="user://clip_channels_test_%d.json"%serial
    var file=FileAccess.open(path,FileAccess.WRITE)
    file.store_string(JSON.stringify(value));file.close()
    return path
func play(rig,value):
    var path=fixture(value)
    var ok=rig.play_clip(path)
    DirAccess.remove_absolute(path)
    verify(ok,"fixture loads %d"%serial)
func reset(rig):
    rig.apply_controls({"reset":true})
    rig.set_process(false)
func key(rig,code,shift=false):
    var event=InputEventKey.new()
    event.keycode=code;event.pressed=true;event.shift_pressed=shift
    rig._unhandled_key_input(event)
func _initialize():call_deferred("run")
func run():
    var c=load("res://clip_player.gd").new()
    for field in AXES+LEVELS:
        var low=-1.0 if field in AXES else 0.0
        for value in [low,0,0.5,1]:
            verify(c.load_data(data({field:value})),"accept boundary "+field+" "+str(value))
        for value in [low-0.0001,1.0001,NAN,INF,-INF,true,false,"0",null,[],{}]:
            verify(not c.load_data(data({field:value})),"reject type/range "+field+" "+str(value))
    for field in FLAGS:
        for value in [true,false]:verify(c.load_data(data({field:value})),"accept boolean "+field)
        for value in [0,1,0.0,1.0,NAN,INF,"true",null,[],{}]:
            verify(not c.load_data(data({field:value})),"reject nonboolean "+field+" "+str(value))
    for field in ["head_tilt","body_x","eye_screen_left","audio_level","blink","gesture_strength","wink_duration"]:
        for value in [-10.0,10.0]:verify(c.load_data(data({field:value})),"legacy finite permissive "+field)
        for value in [NAN,INF,true,"1"]:verify(not c.load_data(data({field:value})),"legacy type rejection "+field)
    for controls in [{"pose_save":1},{"hair_secondary":true},{"unknown":0}]:verify(not c.load_data(data(controls)),"unknown fields remain rejected")
    var source=data({"gaze_x":0.5})
    verify(c.load_data(source) and c.play(),"copy source load")
    source.cues[0].controls.gaze_x=-1;source.cues.append({"time":1,"controls":{}})
    verify(c.cues.size()==1 and c.cues[0].controls.gaze_x==0.5,"deep copy caller data")
    var due=c.step(0);due[0].gaze_x=-0.9
    verify(c.cues[0].controls.gaze_x==0.5,"deep copy emitted controls")
    var dispatch=c.dispatch_id
    verify(not c.load_data(data({"gaze_y":2})) and c.active and c.index==1 and c.dispatch_id==dispatch,"invalid replacement leaves timeline intact")
    c.stop();verify(c.dispatch_id==dispatch+1,"stop invalidates in-flight dispatch")
    c.play();verify(c.step(-1).size()==1 and c.elapsed==0,"negative delta cannot reverse time")
    c.paused=true;verify(c.step(100).is_empty() and c.elapsed==0,"paused player emits nothing")
    c.paused=false;c.step(100);verify(not c.active,"large skip completes player")
    c.play();verify(c.step(0).size()==1,"completed player replays from first cue")

    var rig=load("res://motion_rig.tscn").instantiate()
    root.add_child(rig);await process_frame;rig.set_process(false)
    reset(rig)
    var all={"gaze_x":0.8,"gaze_y":-0.6,"brow_raise":0.4,"brow_screen_left":-0.5,"brow_screen_right":0.9,"breath_level":0.7,"look_x":-0.7,"look_y":0.5,"ornament_secondary":false}
    play(rig,data(all));rig._process(0.25)
    verify(rig.gaze.target.is_equal_approx(Vector2(.8,-.6)),"actual gaze cue")
    verify(rig.brows.target.is_equal_approx(Vector2(-.5,.9)),"per-side brow cues override shared raise")
    verify(is_equal_approx(rig.breathing.manual,.7),"actual held breath")
    verify(rig.attention.active and rig.attention.target.is_equal_approx(Vector2(-.7,.5)),"actual attention cue")
    verify(not rig.ornament.enabled,"actual ornament toggle")
    verify(rig.clip_channels.size()==4,"only four transient groups tracked")
    var current=rig.gaze.current;var brow_current=rig.brows.current;var amount=rig.breathing.amount;var eye=rig.attention.eye
    rig.pause_clip(true)
    var elapsed=rig.clip.elapsed;var clock=rig.clock_time
    rig._process(20)
    verify(rig.clip.elapsed==elapsed and rig.clock_time==clock and rig.gaze.current==current and rig.breathing.amount==amount,"pause freezes timeline and new drivers")
    rig.pause_clip(false);rig._process(.01)
    verify(rig.clip.elapsed>elapsed,"resume advances timeline")
    current=rig.gaze.current;brow_current=rig.brows.current;amount=rig.breathing.amount;eye=rig.attention.eye
    rig.stop_clip()
    verify(rig.gaze.target==Vector2.ZERO and rig.brows.target==Vector2.ZERO and rig.breathing.manual==0 and not rig.attention.active,"cancel releases owned goals")
    verify(rig.gaze.current==current and rig.brows.current==brow_current and rig.breathing.amount==amount and rig.attention.eye==eye,"cancel preserves instantaneous state for smooth release")
    verify(not rig.ornament.enabled,"cancel preserves persistent ornament setting")
    for i in range(90):rig._process(1.0/30)
    verify(rig.gaze.current.length()<.0001 and rig.brows.current==Vector2.ZERO and rig.breathing.amount==0 and rig.attention.eye==Vector2.ZERO,"released drivers settle")
    rig.apply_controls({"gaze_x":.3,"brow_raise":.2,"breath_level":.4,"look_x":.6})
    rig.stop_clip();rig.stop_clip()
    verify(is_equal_approx(rig.gaze.target.x,.3) and is_equal_approx(rig.brows.target.x,.2) and is_equal_approx(rig.breathing.manual,.4) and rig.attention.active,"repeated inactive cancel preserves fresh controls")

    reset(rig)
    rig.apply_controls({"gaze_x":.3,"brow_raise":.2,"breath_level":.4,"look_x":.6})
    play(rig,data({"head_tilt":.1}));rig._process(.01);rig.stop_clip()
    verify(is_equal_approx(rig.gaze.target.x,.3) and is_equal_approx(rig.brows.target.x,.2) and is_equal_approx(rig.breathing.manual,.4) and rig.attention.active,"legacy clip cancel preserves untouched groups")
    reset(rig)
    var future=data({"head_tilt":0.0});future.cues.append({"time":2.0,"controls":all})
    play(rig,future);rig._process(.1)
    rig.apply_controls({"gaze_x":.3});rig.stop_clip()
    verify(is_equal_approx(rig.gaze.target.x,.3),"future unexecuted cue does not own gaze")

    reset(rig);play(rig,data(all));rig._process(.1)
    elapsed=rig.clip.elapsed;dispatch=rig.clip.dispatch_id
    var invalid=fixture(data({"breath_level":2}))
    verify(not rig.play_clip(invalid),"runtime invalid replacement fails")
    DirAccess.remove_absolute(invalid)
    verify(rig.clip.active and rig.clip.elapsed==elapsed and rig.clip.dispatch_id==dispatch and rig.gaze.target.x>.79,"runtime invalid replacement preserves ownership and commands")
    play(rig,data({"head_tilt":.1}))
    verify(rig.gaze.target==Vector2.ZERO and rig.brows.target==Vector2.ZERO and rig.breathing.manual==0 and not rig.attention.active,"valid active replacement releases old channels")
    verify(not rig.ornament.enabled and rig.clip_channels.is_empty(),"replacement preserves setting and starts clean ownership")

    reset(rig)
    var ordered={"version":1,"duration":1.0,"cues":[{"time":0,"controls":{"gaze_x":.8,"breath_trigger":true,"breath_strength":.25}},{"time":.2,"controls":{"gaze_y":.5,"brow_raise":.7}},{"time":.2,"controls":{"gaze_x":-.4,"brow_screen_left":-.3}},{"time":1,"controls":{"breath_cancel":true,"look_release":true}}]}
    play(rig,ordered);rig._process(.01)
    verify(rig.breathing.active and rig.breathing.strength==.25,"trigger uses cue strength")
    rig._process(5)
    verify(not rig.clip.active and rig.gaze.target.is_equal_approx(Vector2(-.4,.5)) and rig.brows.target.is_equal_approx(Vector2(-.3,.7)),"large skip applies same-time cues in source order and holds last commands")
    verify(not rig.breathing.active and not rig.attention.active,"final explicit release cues execute")
    rig._process(1);verify(rig.gaze.target.x<-.39,"natural completion does not re-dispatch or release")
    play(rig,ordered);rig._process(.01)
    verify(rig.gaze.target.x>.79 and rig.breathing.active,"runtime replay restarts commands")
    reset(rig)
    var reset_clip={"version":1,"duration":1.0,"cues":[{"time":0,"controls":all},{"time":.1,"controls":{"reset":true}},{"time":.1,"controls":{"gaze_x":1,"brow_raise":1,"breath_trigger":true,"look_x":1}},{"time":1,"controls":{"gaze_y":1}}]}
    play(rig,reset_clip);rig._process(5)
    verify(not rig.clip.active and rig.gaze.target==Vector2.ZERO and rig.brows.target==Vector2.ZERO and not rig.breathing.active and not rig.attention.active,"reset invalidates all remaining collected cues including same timestamp")
    verify(rig.clip_channels.is_empty(),"reset clears channel ownership")

    reset(rig)
    play(rig,data({"gaze_x":.6,"gaze_y":-.4,"look_x":-.5,"look_y":.7,"breath_level":.6,"brow_raise":.8},.1))
    rig._process(.2)
    verify(not rig.clip.active and rig.attention.active and is_equal_approx(rig.breathing.manual,.6) and is_equal_approx(rig.brows.target.x,.8),"natural completion holds all final continuous commands")
    rig.stop_clip()
    verify(rig.attention.active and is_equal_approx(rig.breathing.manual,.6),"inactive cancel after completion preserves held final commands")
    reset(rig)
    var releases={"version":1,"duration":3,"cues":[{"time":0,"controls":{"look_x":.5,"look_y":.6,"gaze_x":.7,"gaze_y":-.5,"breath_trigger":true}},{"time":1,"controls":{"look_y":-.2,"gaze_x":-.3,"breath_trigger":false,"breath_cancel":false,"look_release":false}},{"time":2,"controls":{"look_release":true,"breath_cancel":true}}]}
    play(rig,releases);rig._process(.1);rig._process(1)
    verify(rig.attention.target.is_equal_approx(Vector2(.5,-.2)) and rig.gaze.target.is_equal_approx(Vector2(-.3,-.5)),"partial axis cues preserve untouched coordinate")
    verify(rig.breathing.active and rig.attention.active,"false trigger/release flags do not cancel")
    rig._process(1)
    verify(not rig.attention.active and not rig.breathing.active,"explicit release cues end active look and breath")
    reset(rig);play(rig,data(all));rig._process(.1);rig.pause_clip(true);rig.stop_clip()
    verify(not rig.clip.paused and not rig.clip.active and rig.gaze.target==Vector2.ZERO and rig.brows.target==Vector2.ZERO and not rig.attention.active and rig.breathing.manual==0,"cancel paused clip releases ownership and clears pause")
    reset(rig)
    rig.apply_controls({"breath_level":.5,"look_x":.5,"gaze_x":.5,"brow_raise":.5})
    play(rig,data({"breath_strength":.2,"ornament_secondary":true}));rig._process(.1);rig.stop_clip()
    verify(rig.clip_channels.is_empty() and is_equal_approx(rig.breathing.manual,.5) and rig.attention.active and is_equal_approx(rig.gaze.target.x,.5) and is_equal_approx(rig.brows.target.x,.5),"strength-only and persistent cues claim no transient groups")
    for no_op in [{"breath_trigger":false},{"breath_cancel":false},{"look_release":false},{"breath_trigger":false,"breath_cancel":false,"look_release":false}]:
        reset(rig)
        rig.apply_controls({"breath_trigger":true,"breath_strength":.7,"look_x":.5,"look_y":-.3})
        play(rig,data(no_op));rig._process(.1)
        verify(rig.clip_channels.is_empty(),"false action flags claim no channels "+str(no_op))
        verify(rig.breathing.active and rig.attention.active,"false flags leave live sources active "+str(no_op))
        rig.stop_clip()
        verify(rig.breathing.active and is_equal_approx(rig.breathing.strength,.7),"cancel false-flag clip preserves unrelated breathing "+str(no_op))
        verify(rig.attention.active and rig.attention.target.is_equal_approx(Vector2(.5,-.3)),"cancel false-flag clip preserves unrelated attention "+str(no_op))
    for field in ["gaze_x","brow_raise","breath_level","look_x"]:
        reset(rig)
        rig.apply_controls({"breath_level":.5,"look_x":.5,"gaze_x":.5,"brow_raise":.5})
        play(rig,data({field:.8}));rig._process(.1)
        verify(rig.clip_channels.size()==1,"single field claims only its group "+field)
        rig.stop_clip()
        verify(is_equal_approx(rig.gaze.target.x,0 if field=="gaze_x" else .5),"selective gaze release "+field)
        verify(is_equal_approx(rig.brows.target.x,0 if field=="brow_raise" else .5),"selective brow release "+field)
        verify(is_equal_approx(rig.breathing.manual,0 if field=="breath_level" else .5),"selective breath release "+field)
        verify(rig.attention.active==(field!="look_x"),"selective attention release "+field)

    for code in [KEY_O,KEY_I,KEY_Y,KEY_V]:
        reset(rig);play(rig,data(all));rig._process(.01);key(rig,code)
        verify(not rig.clip.active,"manual key cancels clip "+str(code))
        if code==KEY_O:verify(rig.brows.target==Vector2.ONE,"manual brows survive cancel")
        if code==KEY_I:verify(rig.breathing.active and rig.breathing.strength==1,"manual breath survives cancel")
        if code==KEY_Y:verify(rig.attention.mouse_follow,"manual attention survives cancel")
        if code==KEY_V:verify(rig.gaze.mouse_follow,"manual gaze survives cancel")
    reset(rig);play(rig,data(all));rig._process(.01);key(rig,KEY_O,true)
    verify(not rig.clip.active and rig.ornament.enabled,"manual ornament toggle survives cancel")

    reset(rig);play(rig,data(all));rig._process(.01)
    var adapter=load("res://live_input.gd").new()
    var bound=adapter.start(0)==OK
    verify(bound,"UDP ephemeral loopback bind")
    if bound:
        var sender=PacketPeerUDP.new();sender.set_dest_address("127.0.0.1",adapter.socket.get_local_port())
        sender.put_packet(JSON.stringify({"seq":1,"controls":{"gaze_x":-.9,"brow_raise":.6,"breath_trigger":true,"look_x":.2}}).to_utf8_buffer())
        await create_timer(.05).timeout;adapter.poll(.01,rig)
        verify(adapter.accepted==1 and not rig.clip.active,"real UDP handover cancels clip")
        verify(is_equal_approx(rig.gaze.target.x,-.9) and is_equal_approx(rig.brows.target.x,.6) and rig.breathing.active and is_equal_approx(rig.attention.target.x,.2),"fresh UDP controls survive old ownership release")
        adapter.stop();sender.close()
    reset(rig)
    verify(rig.play_clip("res://demo_clip.json"),"original demo still loads")
    for i in range(450):rig._process(1.0/30)
    verify(not rig.clip.active and rig.target==Vector3.ZERO and rig.body_target==Vector3.ZERO,"original demo reaches neutral")
    key(rig,KEY_T,true)
    verify(rig.clip.active and rig.clip.duration==18.0 and rig.clip.cues[0].controls.has("gaze_x"),"Shift T starts new bust demo")
    key(rig,KEY_T)
    verify(rig.clip.active and rig.clip.duration==14.0 and not rig.clip.cues[0].controls.has("gaze_x"),"plain T retains original demo")
    rig.stop_clip()
    rig.queue_free();await process_frame
    print("CLIP_CHANNELS_CHECKS_", "PASS" if failures==0 else "FAIL", " count=",checks," failures=",failures)
    quit(1 if failures else 0)

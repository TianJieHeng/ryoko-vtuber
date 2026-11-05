extends SceneTree
var checks=0
var failures=0
func verify(v,label):
    checks+=1
    if not v:push_error(label);failures+=1
func _initialize():call_deferred("run")
func run():
    var c=load("res://clip_player.gd").new()
    var data={"version":1,"duration":2.0,"cues":[{"time":0.0,"controls":{"head_tilt":.2}},{"time":1.0,"controls":{"wink":"screen_left"}},{"time":2.0,"controls":{"head_tilt":0.0}}]}
    verify(c.load_data(data) and c.play(),"load play")
    verify(c.step(.1).size()==1,"initial cue")
    c.paused=true;var prior=c.elapsed;verify(c.step(10).is_empty() and c.elapsed==prior,"pause clock")
    c.paused=false;verify(c.step(3).size()==2 and not c.active,"all crossed cues dispatch once")
    verify(c.step(1).is_empty(),"no loop")
    var bad=data.duplicate(true);bad.cues[0].controls={"pose_save":1};verify(not c.load_data(bad),"no file-writing cues")
    bad=data.duplicate(true);bad.cues[1].time=-1;verify(not c.load_data(bad),"ordered timing")
    bad=data.duplicate(true);bad.cues[0].controls={"head_tilt":"bad"};verify(not c.load_data(bad),"numeric types")
    bad=data.duplicate(true);bad.duration=NAN;verify(not c.load_data(bad),"finite duration")
    var rig=load("res://motion_rig.tscn").instantiate();root.add_child(rig);await process_frame;rig.set_process(false)
    verify(rig.play_clip("res://demo_clip.json"),"real demo")
    for i in range(60):rig._process(1.0/30)
    rig.pause_clip(true);var clock=rig.clock_time;var pose=rig.current;var timeline=rig.clip.elapsed
    for i in range(30):rig._process(1.0/30);verify(rig.clock_time==clock and rig.current==pose and rig.clip.elapsed==timeline,"pause freezes rig and clip")
    rig.pause_clip(false);rig._process(.1);verify(rig.clip.elapsed>timeline,"resume")
    rig.apply_controls({"audio_level":.8,"gesture":"greet","wink":"screen_left"});rig.stop_clip()
    verify(not rig.clip.active and not rig.audio_mouth.active and not rig.eyelids.busy() and rig.gestures.active=="","stop releases transient controls")
    rig.apply_controls({"audio_level":.8});rig.stop_clip();verify(rig.audio_mouth.active,"inactive stop preserves unrelated audio")
    rig.play_clip("res://demo_clip.json")
    for i in range(450):rig._process(1.0/30)
    verify(not rig.clip.active and rig.target==Vector3.ZERO and rig.body_target==Vector3.ZERO,"demo completes neutral")
    rig.play_clip("res://demo_clip.json");rig.apply_controls({"reset":true});verify(not rig.clip.active,"reset cancels")
    if failures==0:print("CLIP_CHECKS_PASS count=",checks)
    quit(1 if failures else 0)

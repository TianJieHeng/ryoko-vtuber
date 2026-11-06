extends SceneTree
var checks=0
var failures=0
var rig
func verify(value,label):
    checks+=1
    if not value:push_error(label);failures+=1
func same(a,b):
    if a.keys()!=b.keys():return false
    for key in a:
        if a[key] is float or a[key] is int:
            if not is_equal_approx(float(a[key]),float(b[key])):return false
        elif a[key]!=b[key]:return false
    return true
func write_json(path,data):
    var file=FileAccess.open(path,FileAccess.WRITE);file.store_string(JSON.stringify(data));file.close()
func _initialize():call_deferred("run")
func run():
    var Store=load("res://performance_store.gd")
    var store=Store.new();store.expressions=["EXP-064"];store.path="user://test_performances.json"
    var effects={}
    for name in preload("res://optional_effects.gd").NAMES:effects[name]=false
    var saved={"head_tilt":.4,"head_x":-.2,"head_y":.1,"body_tilt":-.3,"body_x":.2,"body_y":-.1,"body_follow":false,"gaze_x":.5,"gaze_y":-.2,"brow_screen_left":.6,"brow_screen_right":-.5,"expression":"neutral","effects":effects}
    verify(store.save_slot(1,saved),"save complete snapshot")
    var fresh=Store.new();fresh.expressions=store.expressions;fresh.path=store.path
    verify(fresh.load_disk() and fresh.recall(1)==saved,"fresh load exact nested round trip")
    var copy=fresh.recall(1);copy.effects.sparkle=true;copy.head_x=1
    verify(fresh.recall(1)==saved,"deep copy on recall")
    var input=saved.duplicate(true);verify(fresh.save_slot(2,input),"second save")
    input.effects.anger=true;verify(fresh.recall(2)==saved,"deep copy on save")
    for value in [0,4,-1,1.5,true,false,"1",null,NAN,INF,{},[]]:
        verify(not fresh.save_slot(value,saved) and fresh.recall(value).is_empty(),"reject bad slot "+str(value))
    for axis in Store.AXES:
        for value in [NAN,INF,-INF,1.01,-1.01,true,"0",null,{}]:
            var bad=saved.duplicate(true);bad[axis]=value
            verify(not fresh.save_slot(3,bad) and fresh.recall(3).is_empty(),"reject axis "+axis+" "+str(value))
    for value in ["missing",true,1,null]:
        var bad=saved.duplicate(true);bad.expression=value
        verify(not fresh.save_slot(3,bad),"unknown or malformed expression")
    for value in [{},{"sparkle":true},{"unknown":true},true,[]]:
        var bad=saved.duplicate(true);bad.effects=value
        verify(not fresh.save_slot(3,bad),"complete effects required")
    var bad=saved.duplicate(true);bad.effects.sparkle=1
    verify(not fresh.save_slot(3,bad),"reject nonboolean effect")
    bad=saved.duplicate(true);bad.path="somewhere"
    verify(not fresh.save_slot(3,bad),"reject unexpected snapshot keys")
    bad=saved.duplicate(true);bad.erase("head_x")
    verify(not fresh.save_slot(3,bad),"reject missing field")
    var before=fresh.slots.duplicate(true)
    for malformed in [{"version":true,"slots":{}},{"version":2,"slots":{}},{"version":1,"slots":{"0":saved}},{"version":1,"slots":{"1":bad}},{"version":1,"slots":{},"extra":true},[]]:
        write_json(fresh.path,malformed)
        var bytes=FileAccess.get_file_as_bytes(fresh.path)
        verify(not fresh.load_disk() and fresh.slots==before,"invalid file preserves memory")
        verify(FileAccess.get_file_as_bytes(fresh.path)==bytes,"invalid file preserves disk")
    var file=FileAccess.open(fresh.path,FileAccess.WRITE);file.store_string("not JSON");file.close()
    verify(not fresh.load_disk() and fresh.slots==before,"corrupt JSON preserves slots")
    file=FileAccess.open(fresh.path,FileAccess.WRITE);file.store_string(" ".repeat(65537));file.close()
    verify(not fresh.load_disk() and fresh.slots==before,"oversize file bounded")
    fresh.path="user://nonexistent-directory/performances.json"
    verify(not fresh.save_slot(3,saved) and fresh.slots==before,"failed write preserves slots")
    rig=load("res://motion_rig.tscn").instantiate();root.add_child(rig)
    await process_frame;rig.set_process(false)
    rig.performance_store.path="user://test_rig_performances.json"
    rig.pose_store.path="user://test_legacy_pose_from_performance.json"
    rig.apply_controls({"reset":true,"auto_blink":false})
    rig.apply_controls(saved)
    verify(rig.save_performance(1),"rig saves snapshot")
    verify(same(rig.performance_store.recall(1),saved),"rig target snapshot exact")
    rig.apply_controls({"reset":true,"head_tilt":-.4,"expression":"EXP-064","gaze_x":-.7,"effects":{"sparkle":true}})
    verify(rig.save_performance(2),"existing expression snapshot")
    var second=rig.performance_store.recall(2)
    verify(second.body_follow and second.body_tilt==second.head_tilt,"body follows stored target")
    rig.apply_controls({"head_tilt":0,"body_tilt":0,"gaze_x":0,"brow_raise":0})
    for i in range(30):rig._process(1.0/30)
    var prior=rig.current
    rig.mouse_follow=true;rig.gaze.mouse_follow=true;rig.attention.mouse_follow=true;rig.attention.aim(.8,.8)
    rig._process(.1)
    verify(rig.recall_performance(1),"recall performance")
    verify(not rig.mouse_follow and not rig.gaze.mouse_follow and not rig.attention.active and not rig.attention.mouse_follow,"pointer and attention release")
    prior=rig.current;rig._process(.001)
    verify(rig.current.distance_to(prior)<.02,"recall preserves smooth easing")
    for i in range(180):
        rig._process(1.0/30)
        verify(same(rig.performance_snapshot(),saved),"targets persist through stepping")
    verify(rig.current.distance_to(rig.target)<.001 and rig.brows.current.distance_to(rig.brows.target)<.001,"settled pose and brows")
    verify(not true in rig.face.optional_effects.state.values(),"false effects clear previous on effects")
    rig.apply_controls({"audio_level":.8,"wink":"screen_left","gesture":"greet"})
    verify(rig.recall_performance(2),"second recall with live transients")
    rig._process(.1)
    verify(rig.audio_mouth.active and rig.face.mouth_state=="A" and rig.gestures.active=="greet" and rig.face.blink_right,"mouth wink gesture remain live")
    verify(rig.face.expression=="EXP-064" and rig.expression_index==rig.expression_ids.find("EXP-064"),"expression index follows recall")
    verify(rig.gaze_profile_name=="EXP-064","gaze profile follows existing expression")
    var clip_data={"version":1,"duration":4,"cues":[{"time":0,"controls":{"gaze_x":-.9,"brow_raise":-.9,"effects":{"anger":true}}},{"time":2,"controls":{"head_tilt":-1}}]}
    for paused in [false,true]:
        verify(rig.clip.load_data(clip_data,rig.expression_ids) and rig.clip.play(),"start clip")
        rig._process(.1);rig.pause_clip(paused)
        var elapsed=rig.clip.elapsed
        var ownership=rig.clip_channels.duplicate(true)
        var snapshot=rig.performance_snapshot()
        verify(not rig.recall_performance(3),"empty recall rejected")
        verify(rig.clip.active and rig.clip.paused==paused and rig.clip.elapsed==elapsed and rig.clip_channels==ownership and rig.performance_snapshot()==snapshot,"failed recall has no mutation")
        for value in [true,"1",1.5,4,NAN]:
            verify(not rig.apply_controls({"reset":true,"performance_load":value}) and rig.clip.active and rig.clip.paused==paused,"invalid direct load atomically rejects reset")
            verify(not rig.apply_controls({"reset":true,"performance_save":value}) and rig.clip.active and rig.clip.paused==paused,"invalid direct save atomically rejects reset")
        verify(rig.recall_performance(1),"valid active/paused recall")
        verify(not rig.clip.active and not rig.clip.paused and not rig.audio_mouth.player.stream_paused,"recall cancels and unpauses clip")
        verify(same(rig.performance_snapshot(),saved),"preset restores channels after clip release")
        for i in range(90):rig._process(1.0/30)
        verify(is_equal_approx(rig.target.x,saved.head_tilt),"future cancelled cue cannot overwrite recall")
    rig.performance_store.slots["3"]=saved.duplicate(true);rig.performance_store.slots["3"].expression="UNKNOWN"
    verify(not rig.recall_performance(3),"tampered slot revalidated")
    rig.performance_store.slots.erase("3")
    verify(rig.apply_controls({"performance_load":1,"head_x":.7,"effects":{"sparkle":true},"performance_save":3}),"load before override before save")
    verify(is_equal_approx(rig.performance_store.recall(3).head_x,.7) and rig.performance_store.recall(3).effects.sparkle,"combined control ordering")
    rig.apply_controls({"pendant_secondary":false,"earring_secondary":false,"loose_hair_secondary":false})
    rig.recall_performance(2)
    verify(not rig.pendant.enabled and not rig.earrings_enabled and not rig.loose_hair_enabled,"preserves secondary preferences")
    rig.apply_controls({"reset":true})
    verify(same(rig.performance_store.recall(1),saved) and rig.performance_store.recall(2)==second,"reset retains slots")
    verify(rig.face.expression=="neutral" and rig.gaze.target==Vector2.ZERO and not true in rig.face.optional_effects.state.values(),"reset keeps approved neutral")
    rig.apply_controls({"head_tilt":-.2,"pose_save":1})
    var legacy=rig.pose_store.recall(1)
    var key=InputEventKey.new();key.keycode=KEY_1;key.pressed=true;key.shift_pressed=true
    rig._unhandled_key_input(key)
    verify(same(rig.performance_snapshot(),saved),"Shift+1 recalls performance")
    key.shift_pressed=false;rig._unhandled_key_input(key)
    verify(is_equal_approx(rig.target.x,-.2) and rig.pose_store.recall(1)==legacy,"1 still recalls legacy pose")
    key.keycode=KEY_3;key.ctrl_pressed=true;key.shift_pressed=true;rig._unhandled_key_input(key)
    verify(rig.performance_store.recall(3)==rig.performance_snapshot(),"Ctrl+Shift+3 saves performance")
    for name in ["performance_load","performance_save"]:
        verify(rig.live_input.decode(JSON.stringify({"seq":1,"controls":{name:1}}).to_utf8_buffer(),rig.expression_ids).is_empty(),"UDP cannot access persistence")
        verify(not rig.clip.load_data({"version":1,"duration":1,"cues":[{"time":0,"controls":{name:1}}]},rig.expression_ids),"clips cannot access persistence")
    var sender=PacketPeerUDP.new()
    verify(rig.live_input.start(0)==OK,"real loopback listener")
    verify(sender.set_dest_address("127.0.0.1",rig.live_input.socket.get_local_port())==OK,"local destination")
    verify(sender.put_packet(JSON.stringify({"seq":1,"controls":{"head_tilt":-.8,"auto_blink":false}}).to_utf8_buffer())==OK,"send real live packet")
    await process_frame;rig.live_input.poll(.01,rig)
    verify(rig.live_input.accepted==1 and rig.live_input.leased and is_equal_approx(rig.target.x,-.8),"live input takes over preset")
    rig.recall_performance(1);rig.live_input.poll(2.1,rig)
    verify(not rig.live_input.leased and rig.target==Vector3.ZERO and rig.face.expression=="neutral","existing live timeout retained after local recall")
    verify(same(rig.performance_store.recall(1),saved),"timeout does not erase presets")
    sender.close();rig.live_input.stop()
    print("PERFORMANCE_PRESET_CHECKS_", "PASS" if failures==0 else "FAIL", " count=",checks," failures=",failures)
    quit(1 if failures else 0)

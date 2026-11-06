extends SceneTree
# Actual Godot renderer, explicit disk round trip, and real local UDP takeover.
var rig
var elapsed=0.0
var events={}
var next_sample=0.0
var sender=PacketPeerUDP.new()
var title="NEUTRAL / approved rig unchanged"
func _initialize():call_deferred("setup")
func setup():
    rig=load("res://motion_rig.tscn").instantiate();root.add_child(rig)
    await process_frame;rig.set_process(false)
    rig.performance_store.path="user://review_performances.json"
    rig.performance_store.slots.clear()
    rig.apply_controls({"reset":true,"auto_blink":false})
    if rig.live_input.start(0)!=OK:push_error("Local review UDP bind failed");quit(1);return
    sender.set_dest_address("127.0.0.1",rig.live_input.socket.get_local_port())
func once(name,time):
    if elapsed<time or events.has(name):return false
    events[name]=true;return true
func checked(ok,what):
    if not ok:push_error(what);quit(1)
func _process(delta):
    if rig==null or not rig.rig_ready:return false
    elapsed+=delta
    if once("setup1",1.5):
        rig.apply_controls({"head_tilt":-.45,"head_x":-.3,"body_tilt":.25,"gaze_x":.65,"gaze_y":-.15,"brow_screen_left":.8,"brow_screen_right":.2})
        title="SETUP 1 / neutral pose, gaze and independent brows"
    if once("save1",3.5):
        checked(rig.save_performance(1),"Save 1 failed")
        title="SAVED 1 / existing controls, no new artwork"
    if once("setup2",5.0):
        rig.apply_controls({"head_tilt":.45,"head_x":.25,"body_tilt":-.35,"expression":"EXP-064","gaze_x":-.6,"gaze_y":.15,"brow_raise":0,"effects":{"sparkle":true}})
        title="SETUP 2 / existing EXP-064, gaze and sparkle"
    if once("save2",6.5):
        checked(rig.save_performance(2),"Save 2 failed")
        title="SAVED 2 / separate from head-body pose slots"
    if once("roundtrip",8.0):
        rig.apply_controls({"reset":true,"auto_blink":false})
        rig.performance_store.slots.clear()
        checked(rig.performance_store.load_disk(),"Disk reload failed")
        checked(rig.performance_store.slots.size()==2,"Disk reload missing slots")
        print("PERFORMANCE_DISK_RELOAD_PASS")
        title="RESET / saved slots reloaded from disk"
    if once("recall1",10.0):
        checked(rig.recall_performance(1),"Recall 1 failed")
        title="RECALL 1 / eased pose, gaze and brows restored"
    if once("recall2",13.0):
        checked(rig.recall_performance(2),"Recall 2 failed")
        title="RECALL 2 / expression and effects restored"
    if once("live_face",14.5):
        rig.apply_controls({"audio_level":.55,"wink":"screen_left","gesture":"greet"})
        title="LIVE CONTROLS / mouth, wink and greeting still work"
    if once("mouth_release",16.0):rig.apply_controls({"audio_stop":true,"release_eye_controls":true})
    if once("clip_start",16.5):
        checked(rig.play_clip("res://demo_bust_clip.json"),"Clip failed")
        title="CLIP / existing timed controls"
    if once("pause",18.0):
        rig.pause_clip(true)
        title="PAUSED CLIP / complete rig held"
    if once("paused_recall",19.0):
        checked(rig.recall_performance(1),"Paused recall failed")
        title="RECALL 1 / takes over paused clip safely"
    if once("udp",21.5):
        var packet={"seq":1,"controls":{"head_tilt":.65,"body_tilt":-.45,"expression":"neutral","gaze_x":-.6,"mouth":"E","auto_blink":false}}
        checked(sender.put_packet(JSON.stringify(packet).to_utf8_buffer())==OK,"UDP send failed")
        title="REAL UDP / live input takes over recalled setup"
    rig._process(delta)
    if events.has("udp") and not rig.live_input.leased:title="TIMEOUT / approved neutral recovery; slots retained"
    rig.hud.text="RYOKO / REUSABLE PERFORMANCE PRESETS"
    rig.hud.add_theme_font_size_override("font_size",19)
    rig.hint.text=title
    rig.hint.add_theme_font_size_override("font_size",12)
    rig.pose_status.text="Ctrl+Shift+1/2/3 save | Shift+1/2/3 recall | legacy pose slots unchanged"
    rig.pose_status.add_theme_font_size_override("font_size",11)
    if elapsed>=next_sample:
        print("PERFORMANCE_SAMPLE ",JSON.stringify({"wall":elapsed,"label":title,"snapshot":rig.performance_snapshot(),"current":[rig.current.x,rig.current.y,rig.current.z],"clip_active":rig.clip.active,"clip_paused":rig.clip.paused,"mouth":rig.face.mouth_state,"wink":rig.face.blink_right,"udp_accepted":rig.live_input.accepted,"udp_leased":rig.live_input.leased,"saved_slots":rig.performance_store.slots.size()}))
        next_sample+=.25
    if elapsed>=26:
        checked(rig.live_input.accepted==1 and not rig.live_input.leased,"Live takeover/timeout missing")
        checked(rig.performance_store.slots.size()==2,"Saved slots lost")
        sender.close();rig.live_input.stop();print("PERFORMANCE_REVIEW_COMPLETE");quit()
    return false

extends SceneTree
# Actual Godot movie-writer proof. Source art is unchanged. Loopback takeover
# uses a real UDP packet, not a direct invocation of the rig's control API.
var rig
var sender=PacketPeerUDP.new()
var elapsed=0.0
var events={}
var next_sample=0.0
func _initialize():call_deferred("setup")
func setup():
    rig=load("res://motion_rig.tscn").instantiate();root.add_child(rig)
    await process_frame;rig.set_process(false)
    rig.apply_controls({"reset":true,"auto_blink":false,"body_follow":false})
    if rig.live_input.start(0)!=OK:
        push_error("Effects review could not bind loopback UDP");quit(1);return
    if sender.set_dest_address("127.0.0.1",rig.live_input.socket.get_local_port())!=OK:
        push_error("Effects review could not configure local sender");quit(1)
func once(name,time):
    if elapsed<time or events.has(name):return false
    events[name]=true;return true
func _process(delta):
    if rig==null or not rig.rig_ready:return false
    elapsed+=delta
    if once("start",1.0):
        if not rig.play_clip("res://demo_effects_clip.json"):push_error(rig.clip.error_message);quit(1);return false
    if once("pause",15.2):rig.pause_clip(true)
    if once("resume",16.2):rig.pause_clip(false)
    if once("replay",22.0):
        if not rig.play_clip("res://demo_effects_clip.json"):push_error(rig.clip.error_message);quit(1);return false
    if once("replay_pause",24.5):rig.pause_clip(true)
    if once("udp",25.0):
        var packet={"seq":1,"controls":{"effects":{"sparkle":true,"sweat":true},"mouth":"E","head_tilt":0.25,"auto_blink":false}}
        if sender.put_packet(JSON.stringify(packet).to_utf8_buffer())!=OK:push_error("Effects UDP send failed");quit(1);return false
        print("OPTIONAL_EFFECTS_UDP_PACKET_SENT")
    rig._process(delta)
    var t=rig.clip.elapsed
    var label="NEUTRAL / optional overlays off"
    if events.has("start"):
        label="COMPLETE / optional overlays off"
        if rig.clip.active:
            if t<1:label="NEUTRAL / optional overlays off"
            elif t<2.5:label="BLUSH / character-right only"
            elif t<4:label="BLUSH / independent sides together"
            elif t<5:label="BLUSH / character-left only"
            elif t<7:label="TEAR / character-right + mouth and wink"
            elif t<8.5:label="TEAR / character-left + head tilt"
            elif t<10:label="SWEAT / existing transparent source"
            elif t<11.5:label="ANGER / source mark follows head"
            elif t<13:label="SPARKLE / source cluster follows head"
            elif t<16:label="COMBINED / existing expression + overlays"
            elif t<17.5:label="OPTIONAL OFF / authored effects preserved"
            else:label="NEUTRAL / optional overlays off"
        if rig.clip.paused:label="PAUSED / pose and optional overlays held"
        if events.has("replay") and rig.clip.active and not rig.clip.paused:label="REPLAY / existing clip controls"
        if events.has("udp"):
            label="REAL UDP / paused clip taken over" if rig.live_input.leased else "UDP TIMEOUT / neutral and overlays released"
    var active=[]
    for key in rig.face.optional_effects.state:
        if rig.face.optional_effects.state[key]:active.append(key)
    rig.hud.text="RYOKO / INDEPENDENT OPTIONAL EFFECTS"
    rig.hint.text=label
    rig.pose_status.text="Optional: %s  |  Face: %s"%[", ".join(active) if not active.is_empty() else "off",rig.face.expression]
    rig.pose_status.add_theme_font_size_override("font_size",12)
    if elapsed>=next_sample:
        print("OPTIONAL_EFFECTS_SAMPLE ",JSON.stringify({"wall":elapsed,"clip":t,"active":rig.clip.active,"paused":rig.clip.paused,"expression":rig.face.expression,"effects":rig.face.optional_effects.state,"mouth":rig.face.mouth_state,"udp_accepted":rig.live_input.accepted,"udp_leased":rig.live_input.leased,"label":label,"head":[rig.current.x,rig.current.y,rig.current.z]}))
        next_sample+=0.25
    if elapsed>=30.0:
        sender.close();print("OPTIONAL_EFFECTS_REVIEW_COMPLETE");quit()
    return false

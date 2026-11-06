extends SceneTree
# Actual Godot movie-writer review. The live takeover uses a real UDP packet.
var rig
var sender=PacketPeerUDP.new()
var elapsed=0.0
var events={}
var next_sample=0.0
func _initialize():call_deferred("setup")
func setup():
    rig=load("res://motion_rig.tscn").instantiate();root.add_child(rig)
    await process_frame;rig.set_process(false)
    rig.apply_controls({"reset":true,"auto_blink":false,"body_follow":false,"pendant_secondary":false})
    if rig.live_input.start(0)!=OK:
        push_error("Pendant review could not bind loopback UDP");quit(1);return
    if sender.set_dest_address("127.0.0.1",rig.live_input.socket.get_local_port())!=OK:
        push_error("Pendant review could not configure local sender");quit(1)
func once(name,time):
    if elapsed<time or events.has(name):return false
    events[name]=true;return true
func _process(delta):
    if rig==null or not rig.rig_ready:return false
    elapsed+=delta
    if once("start",1.0):
        if not rig.play_clip("res://demo_pendant_clip.json"):push_error(rig.clip.error_message);quit(1);return false
    if once("pause",17.2):rig.pause_clip(true)
    if once("resume",18.2):rig.pause_clip(false)
    if once("live_pause",23.0):rig.pause_clip(true)
    if once("udp",23.5):
        var packet={"seq":1,"controls":{"pendant_secondary":true,"body_tilt":0.8,"body_x":0.6,"mouth":"E","auto_blink":false}}
        if sender.put_packet(JSON.stringify(packet).to_utf8_buffer())!=OK:push_error("Pendant UDP send failed");quit(1);return false
        print("PENDANT_UDP_PACKET_SENT")
    rig._process(delta)
    var t=rig.clip.elapsed
    var label="OFF / original pendant and chain"
    if rig.clip.active:
        if t<1:label="OFF / original pendant and chain"
        elif t<2:label="ON / exact neutral source"
        elif t<5:label="TORSO LEFT / restrained pendant follow-through"
        elif t<8:label="TORSO RIGHT / reversal and settling"
        elif t<11:label="HOLD / fixed chain, no invented idle swing"
        elif t<15:label="HEAD ONLY / torso and pendant settle independently"
        elif t<17:label="COMBINED / breath, expression, mouth and effects"
        elif t<18:label="OFF / original pendant at the same held pose"
        elif t<20:label="ON / small hinge, chain remains fixed"
        else:label="RETURN / neutral and quiet recovery"
    if rig.clip.paused:label="PAUSED / pendant and the complete rig held"
    if events.has("udp"):
        label="REAL UDP / paused clip taken over" if rig.live_input.leased else "UDP TIMEOUT / return to neutral"
    rig.hud.text="RYOKO / GREEN PENDANT HINGE"
    rig.hint.text=label
    rig.pose_status.text="Existing pixels | fixed chain | small skin fill behind pendant"
    rig.pose_status.add_theme_font_size_override("font_size",12)
    if elapsed>=next_sample:
        print("PENDANT_SAMPLE ",JSON.stringify({"wall":elapsed,"clip":t,"active":rig.clip.active,"paused":rig.clip.paused,"expression":rig.face.expression,"mouth":rig.face.mouth_state,"enabled":rig.pendant.enabled,"angle":rig.pendant.angle,"swing":rig.pendant.swing,"pivot":[rig.pendant_pivot.position.x,rig.pendant_pivot.position.y],"visible":rig.pendant_pivot.visible,"udp_accepted":rig.live_input.accepted,"udp_leased":rig.live_input.leased,"label":label}))
        next_sample+=0.25
    if elapsed>=29.0:
        sender.close();print("PENDANT_REVIEW_COMPLETE");quit()
    return false

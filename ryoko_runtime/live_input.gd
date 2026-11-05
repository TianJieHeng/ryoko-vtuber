extends RefCounted
# Opt-in, loopback-only UDP adapter. No paths, persistence or network configuration.
var socket=PacketPeerUDP.new()
var active=false
var last_sequence=-1
var accepted=0
var rejected=0
var age=0.0
var leased=false
var status="disabled"
const TIMEOUT=2.0
const NUMBERS=["look_x","look_y","brow_raise","brow_screen_left","brow_screen_right","breath_level","breath_strength","gaze_x","gaze_y","head_tilt","head_x","head_y","body_tilt","body_x","body_y","eye_screen_left","eye_screen_right","audio_level","blink","gesture_strength","wink_duration"]
const FLAGS=["ornament_secondary","look_release","breath_trigger","breath_cancel","reset","auto_blink","body_follow","release_eye_controls","gesture_cancel","audio_stop","speech_active"]
func start(port=9122):
    if active:return ERR_ALREADY_IN_USE
    var err=socket.bind(port,"127.0.0.1")
    active=err==OK;status="listening" if active else "bind failed: "+str(err)
    return err
func stop():
    socket.close();active=false;leased=false;status="disabled"
func decode(bytes,expressions):
    if bytes.size()>4096:return {}
    var parser=JSON.new()
    if parser.parse(bytes.get_string_from_utf8())!=OK:return {}
    var data=parser.data
    if not data is Dictionary or data.size()!=2 or not data.has("seq") or not data.has("controls"):return {}
    var seq=data.seq
    if not (seq is float or seq is int) or not is_finite(float(seq)) or float(seq)!=floor(float(seq)) or seq<0 or seq>2147483647 or seq<=last_sequence:return {}
    var c=data.controls
    if not c is Dictionary or c.is_empty() or c.size()>24:return {}
    for key in c:
        var v=c[key]
        if key in NUMBERS:
            if not (v is float or v is int) or not is_finite(float(v)):return {}
            var low=-1.0 if key in ["look_x","look_y","brow_raise","brow_screen_left","brow_screen_right","gaze_x","gaze_y","head_tilt","head_x","head_y","body_tilt","body_x","body_y"] else 0.0
            var high=2.0 if key=="wink_duration" else 1.0
            if v<low or v>high:return {}
        elif key in FLAGS:
            if not v is bool:return {}
        elif key=="expression":
            if not v is String or (v!="neutral" and not expressions.has(v)):return {}
        elif key=="mouth":
            if not v is String or not v in ["A","E","I","O","U","REST","RELEASE","neutral"]:return {}
        elif key=="gesture":
            if not v is String or not v in ["acknowledge","greet"]:return {}
        elif key=="wink":
            if not v is String or not v in ["screen_left","screen_right","both"]:return {}
        else:return {}
    return data
func poll(delta,rig):
    if not active:return
    age+=max(0.0,delta)
    for i in range(32):
        if socket.get_available_packet_count()==0:break
        var bytes=socket.get_packet()
        if socket.get_packet_ip()!="127.0.0.1":rejected+=1;continue
        var data=decode(bytes,rig.expression_ids)
        if data.is_empty():rejected+=1;continue
        rig.stop_clip() # A fresh live source takes priority over a recorded clip.
        if not rig.apply_controls(data.controls):rejected+=1;continue
        last_sequence=int(data.seq);accepted+=1;age=0.0;leased=true;status="receiving"
    if leased and age>=TIMEOUT:
        rig.apply_controls({"reset":true})
        leased=false;status="timed out / released"

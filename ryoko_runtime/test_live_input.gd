extends SceneTree
var checks=0
var failures=0
func verify(v,label):
    checks+=1
    if not v:push_error(label);failures+=1
func pack(c,seq=1):return JSON.stringify({"seq":seq,"controls":c}).to_utf8_buffer()
func _initialize():call_deferred("run")
func run():
    var adapter=load("res://live_input.gd").new()
    var ids=["test"]
    for c in [{"head_tilt":.5},{"body_tilt":-.5},{"mouth":"A"},{"wink":"both"},{"expression":"test"},{"reset":true}]:verify(not adapter.decode(pack(c),ids).is_empty(),"valid packet")
    for c in [{},{"head_tilt":"bad"},{"head_tilt":2},{"auto_blink":1},{"expression":"missing"},{"mouth":"bad"},{"gesture":"bad"},{"wink":"bad"},{"clip_play":true},{"pose_save":1},{"audio_file":"x"},{"head_x":true}]:verify(adapter.decode(pack(c),ids).is_empty(),"reject invalid atomically")
    for seq in [-1,1.5,2147483648]:verify(adapter.decode(pack({"head_tilt":0},seq),ids).is_empty(),"bad seq")
    for raw in ['[]','null','{"seq":1}','invalid','{"seq":1,"controls":{"reset":true},"extra":0}']:verify(adapter.decode(raw.to_utf8_buffer(),ids).is_empty(),"bad envelope")
    verify(adapter.decode((' '.repeat(4097)).to_utf8_buffer(),ids).is_empty(),"size limit")
    adapter.last_sequence=5
    for seq in [0,4,5]:verify(adapter.decode(pack({"head_tilt":0},seq),ids).is_empty(),"old or duplicate")
    var rig=load("res://motion_rig.tscn").instantiate();root.add_child(rig);await process_frame;rig.set_process(false)
    verify(not rig.live_input.active,"disabled by default")
    verify(adapter.start(19122)==OK,"bind loopback")
    var other=load("res://live_input.gd").new();verify(other.start(19122)!=OK,"bind failure not hidden")
    var sender=PacketPeerUDP.new();sender.set_dest_address("127.0.0.1",19122)
    sender.put_packet(pack({"head_tilt":.6,"body_tilt":-.2,"mouth":"A"},6))
    await create_timer(.03).timeout;adapter.poll(.01,rig)
    verify(adapter.accepted==1 and rig.target.x>.59 and rig.body_target.x<-.19,"actual UDP affects rig")
    verify(rig.face.mouth_state=="A","mouth real packet")
    sender.put_packet(pack({"head_tilt":-.8},6));await create_timer(.03).timeout;adapter.poll(.01,rig)
    verify(adapter.rejected==1 and rig.target.x>.59,"replay ignored")
    sender.put_packet(pack({"head_tilt":-.8,"expression":"missing"},7));await create_timer(.03).timeout;adapter.poll(.01,rig)
    verify(adapter.rejected==2 and rig.target.x>.59,"invalid batch no partial update")
    adapter.poll(2.1,rig)
    verify(not adapter.leased and rig.target==Vector3.ZERO and rig.face.speech_override=="","timeout releases")
    sender.put_packet(pack({"head_tilt":-.3},8));await create_timer(.03).timeout;adapter.poll(.01,rig)
    verify(adapter.leased and rig.target.x<-.29,"recovery")
    adapter.stop();sender.close();verify(not adapter.active,"stop")
    if failures==0:print("LIVE_INPUT_CHECKS_PASS count=",checks)
    quit(1 if failures else 0)

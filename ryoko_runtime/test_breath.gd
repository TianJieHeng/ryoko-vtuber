extends SceneTree
var checks=0
var failures=0
func verify(v,label):
    checks+=1
    if not v:push_error(label);failures+=1
func _initialize():call_deferred("run")
func run():
    var b=load("res://breath_driver.gd").new()
    for i in range(180):b.step(1.0/30);verify(b.amount==0,"no default loop")
    b.trigger();var peak=0.0
    for i in range(300):
        b.step(1.0/30);peak=max(peak,b.amount)
        verify(b.amount>=0 and b.amount<=1,"bounded profile")
    verify(peak>.97 and b.amount==0 and not b.active,"inhale settles")
    b.hold(.8)
    for i in range(60):b.step(1.0/30)
    verify(abs(b.amount-.8)<.001,"manual level")
    b.cancel()
    for i in range(90):b.step(1.0/30)
    verify(b.amount==0,"cancel settles")
    b.amount=1
    for x in range(0,1137,16):
        for y in range(0,1385,16):
            var p=Vector2(x,y);var d=b.offset(p)
            verify(d.is_finite() and d.length()<8,"bounded geometry")
            if y<=650 or y>=1384:verify(d==Vector2.ZERO,"face/base anchored")
            var mirror=b.offset(Vector2(1136-x,y))
            verify(abs(d.x+mirror.x)<.0001 and abs(d.y-mirror.y)<.0001,"symmetric expansion")
    verify(b.offset(Vector2(300,900)).y==b.offset(Vector2(500,1100)).y,"shoulder/chest shared lift")
    b.hold(NAN);verify(b.manual==0,"nonfinite neutral")
    b.trigger(99);verify(b.strength==1,"strength clamp")
    b.reset();verify(b.amount==0 and not b.active,"reset")
    var rig=load("res://motion_rig.tscn").instantiate();root.add_child(rig);await process_frame;rig.set_process(false)
    rig.apply_controls({"breath_trigger":true,"head_tilt":.3,"body_tilt":-.2})
    for i in range(70):rig._process(1.0/30)
    verify(rig.breathing.amount>.95,"runtime drives inhale")
    verify(rig.skin_material.get_shader_parameter("controlled_breath")>.95,"shader wired")
    verify(abs(rig.target.x-.3)<.0001,"head controls preserved")
    rig.apply_controls({"reset":true});verify(rig.breathing.amount==0,"rig reset")
    var adapter=load("res://live_input.gd").new();verify(adapter.start(19124)==OK,"loopback bind")
    var sender=PacketPeerUDP.new();sender.set_dest_address("127.0.0.1",19124)
    sender.put_packet('{"seq":1,"controls":{"breath_level":0.8}}'.to_utf8_buffer())
    await create_timer(.03).timeout;adapter.poll(.01,rig)
    verify(adapter.accepted==1 and rig.breathing.manual>.79,"actual UDP breath")
    adapter.poll(2.1,rig);verify(rig.breathing.manual==0,"timeout releases")
    adapter.stop();sender.close()
    if failures==0:print("BREATH_CHECKS_PASS count=",checks," peak=",peak)
    quit(1 if failures else 0)

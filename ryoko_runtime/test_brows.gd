extends SceneTree
var checks=0
var failures=0
func verify(v,label):
    checks+=1
    if not v:push_error(label);failures+=1
func _initialize():call_deferred("run")
func run():
    var b=load("res://brow_driver.gd").new()
    b.set_both(9);verify(b.target==Vector2.ONE,"clamp")
    b.set_side("screen_left",-1);verify(b.target==Vector2(-1,1),"independent sides")
    for i in range(90):b.step(1.0/30);verify(b.current.is_finite() and b.current.length()<=sqrt(2.0),"bounded easing")
    for amount in [-1.0,-.5,0.0,.5,1.0]:
        for x in range(430,700,3):
            for y in range(430,480,3):
                var p=Vector2(x,y);var q=p+Vector2(7,3)
                verify(b.sample_pixel(q,amount)-b.sample_pixel(p,amount)==q-p,"rigid brow shape")
    b.set_both(NAN);verify(b.target==Vector2.ZERO,"nonfinite")
    b.reset();verify(b.current==Vector2.ZERO,"reset")
    var rig=load("res://motion_rig.tscn").instantiate();root.add_child(rig);await process_frame;rig.set_process(false)
    rig.apply_controls({"brow_screen_left":1,"brow_screen_right":-.5,"mouth":"A","eye_screen_left":1})
    for i in range(30):rig._process(1.0/30)
    verify(rig.brows.current.x>.99 and rig.brows.current.y<-.49,"runtime independent")
    verify(rig.skin_material.get_shader_parameter("brow_enabled"),"neutral brow enabled")
    verify(rig.face.blink_right and rig.face.mouth_state=="A","blink/mouth coexist")
    rig.face.set_expression(rig.expression_ids[0]);rig._process(.1)
    verify(not rig.skin_material.get_shader_parameter("brow_enabled"),"authored expressions unchanged")
    rig.apply_controls({"reset":true});verify(rig.brows.current==Vector2.ZERO,"rig reset")
    var a=load("res://live_input.gd").new();verify(a.start(19125)==OK,"local bind")
    var sender=PacketPeerUDP.new();sender.set_dest_address("127.0.0.1",19125)
    sender.put_packet('{"seq":1,"controls":{"brow_screen_left":-0.7,"brow_screen_right":0.4}}'.to_utf8_buffer())
    await create_timer(.03).timeout;a.poll(.01,rig)
    verify(a.accepted==1 and rig.brows.target.x<-.69 and rig.brows.target.y>.39,"actual UDP")
    a.poll(2.1,rig);verify(rig.brows.target==Vector2.ZERO,"timeout release")
    a.stop();sender.close()
    if failures==0:print("BROW_CHECKS_PASS count=",checks)
    quit(1 if failures else 0)

extends SceneTree
var checks=0
var failures=0
func verify(v,label):
    checks+=1
    if not v:push_error(label);failures+=1
func _initialize():call_deferred("run")
func run():
    var g=load("res://gaze_driver.gd").new()
    g.set_target(99,-99);verify(g.target==Vector2(1,-1),"bounds")
    g.set_target(NAN,INF);verify(g.target==Vector2.ZERO,"finite")
    g.set_target(1,0)
    for i in range(90):g.step(1.0/30);verify(g.current.is_finite() and g.current.x<=1,"smooth stable")
    verify(g.current.x>.99,"target reached")
    g.reset();verify(g.current==Vector2.ZERO,"reset")
    for d in [Vector2(-1,-1),Vector2(1,1),Vector2(-1,1),Vector2(1,-1),Vector2.ZERO]:
        for y in range(470,530,2):
            for x in range(430,710,2):
                var p=Vector2(x,y);var q=p+Vector2(13,7)
                verify(g.sample_pixel(q,d)-g.sample_pixel(p,d)==q-p,"rigid distance and shape")
                verify(g.sample_pixel(p,d)-p==-d*Vector2(7,2),"uniform translation")
    var rig=load("res://motion_rig.tscn").instantiate();root.add_child(rig);await process_frame;rig.set_process(false)
    rig.apply_controls({"gaze_x":.7,"gaze_y":-.5,"head_tilt":.3,"mouth":"A"})
    rig._process(.1)
    verify(rig.gaze.current.x>0 and rig.face.mouth_state=="A","independent mouth + gaze")
    verify(rig.skin_material.get_shader_parameter("gaze_open")==Vector2.ONE,"neutral eyes enabled")
    rig.apply_controls({"eye_screen_left":1});rig._process(.1)
    verify(rig.skin_material.get_shader_parameter("gaze_open")==Vector2(0,1),"blink blocks correct screen eye")
    rig.face.set_expression(rig.expression_ids[0]);rig._process(.1)
    verify(rig.skin_material.get_shader_parameter("gaze_open")==Vector2.ZERO,"authored emotion preserved")
    var adapter=load("res://live_input.gd").new()
    verify(not adapter.decode('{"seq":1,"controls":{"gaze_x":-1,"gaze_y":1}}'.to_utf8_buffer(),[]).is_empty(),"live gaze accepted")
    rig.apply_controls({"reset":true});verify(rig.gaze.current==Vector2.ZERO,"rig reset")
    verify(adapter.start(19123)==OK,"gaze UDP bind")
    var sender=PacketPeerUDP.new();sender.set_dest_address("127.0.0.1",19123)
    sender.put_packet('{"seq":1,"controls":{"gaze_x":-.8,"gaze_y":.3}}'.replace('-.8','-0.8').replace(':.3',':0.3').to_utf8_buffer())
    await create_timer(.03).timeout;adapter.poll(.01,rig)
    verify(adapter.accepted==1 and rig.gaze.target.x<-.79 and rig.gaze.target.y>.29,"actual UDP gaze")
    adapter.poll(2.1,rig);verify(rig.gaze.target==Vector2.ZERO,"timeout centers eyes")
    adapter.stop();sender.close()
    if failures==0:print("GAZE_CHECKS_PASS count=",checks)
    quit(1 if failures else 0)

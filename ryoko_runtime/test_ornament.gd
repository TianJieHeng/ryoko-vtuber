extends SceneTree
var checks=0
var failures=0
func verify(v,label):
    checks+=1
    if not v:push_error(label);failures+=1
func _initialize():call_deferred("run")
func run():
    var o=load("res://ornament_driver.gd").new()
    for i in range(120):
        o.step(Vector2.ZERO,0,1.0/30)
        verify(o.angle==0 and o.swing==0,"no idle movement")
    var peak=0.0
    for i in range(90):
        o.step(Vector2(20,0),.1,1.0/30)
        peak=max(peak,abs(o.swing))
        verify(abs(o.angle)<=o.RELATIVE_LIMIT+.00001,"relative bound")
        verify(abs(o.swing)<=o.SWING_LIMIT+.00001,"swing bound")
    verify(peak>.01,"anchor translation creates swing")
    for i in range(300):o.step(Vector2(20,0),.1,1.0/30)
    verify(o.swing==0 and o.velocity==0,"held anchor settles exactly")
    verify(is_equal_approx(o.angle,-.1),"gravity cancels held head tilt")
    var previous=o.angle
    o.step(Vector2(NAN,0),0,.1);verify(o.angle==previous,"invalid anchor ignored")
    o.step(Vector2.ZERO,NAN,.1);verify(o.angle==previous,"invalid angle ignored")
    o.step(Vector2.ZERO,0,NAN);verify(o.angle==previous,"invalid delta ignored")
    o.step(Vector2.ZERO,0,0);verify(o.angle==previous,"zero delta does not advance")
    o.enabled=false;o.step(Vector2(100,0),.2,.1)
    verify(o.angle==0 and not o.initialized,"disabled exact baseline")
    o.enabled=true
    for dt in [.008,.016,.033,.1,.3]:
        for i in range(100):
            o.step(Vector2(200*(i%2),0),.25*(1 if i%2 else -1),dt)
            verify(is_finite(o.angle) and abs(o.angle)<=o.RELATIVE_LIMIT+.00001,"frame stall stability")
    o.reset();verify(o.angle==0 and o.velocity==0 and not o.initialized,"reset clears dynamics")
    var rig=load("res://motion_rig.tscn").instantiate();root.add_child(rig);await process_frame;rig.set_process(false)
    rig.apply_controls({"reset":true,"auto_blink":false,"body_follow":false})
    rig._process(1.0/30)
    verify(rig.ornament_pivot.visible,"ornament cutout visible")
    verify(rig.skin_material.get_shader_parameter("ornament_separate")==true,"source cutout removed")
    verify(rig.ornament_sprite.region_rect==Rect2(781,184,22,131),"source texture rectangle")
    rig.apply_controls({"head_tilt":.75,"head_x":.6})
    var live_peak=0.0
    for i in range(150):
        rig._process(1.0/30);live_peak=max(live_peak,abs(rig.ornament.swing))
    verify(live_peak>.001,"actual head motion drives accessory")
    verify(abs(rig.ornament_pivot.rotation)<.001,"held head angle leaves ornament hanging vertically")
    verify(rig.body_current==Vector3.ZERO,"head-only motion does not move torso")
    rig.apply_controls({"ornament_secondary":false});rig._process(.1)
    verify(not rig.ornament_pivot.visible,"off hides cutout")
    verify(not rig.skin_material.get_shader_parameter("ornament_separate"),"off restores exact source")
    rig.apply_controls({"ornament_secondary":true,"body_tilt":-.8,"bounce":true,"mouth":"A","eye_screen_left":1,"gaze_x":.5})
    for i in range(10):rig._process(1.0/30)
    verify(rig.face.mouth_state=="A" and rig.face.blink_right,"face controls compatible")
    verify(abs(rig.ornament.angle)<=o.RELATIVE_LIMIT,"body/bounce compatibility")
    rig.apply_controls({"reset":true});verify(rig.ornament.angle==0 and not rig.ornament.initialized,"rig reset clears accessory")
    var adapter=load("res://live_input.gd").new()
    verify(not adapter.decode('{"seq":1,"controls":{"ornament_secondary":false}}'.to_utf8_buffer(),[]).is_empty(),"UDP bool accepted")
    verify(adapter.decode('{"seq":1,"controls":{"ornament_secondary":1}}'.to_utf8_buffer(),[]).is_empty(),"UDP rejects non-bool")
    verify(adapter.start(19125)==OK,"UDP bind")
    var sender=PacketPeerUDP.new();sender.set_dest_address("127.0.0.1",19125)
    sender.put_packet('{"seq":1,"controls":{"ornament_secondary":false}}'.to_utf8_buffer())
    await create_timer(.03).timeout;adapter.poll(.01,rig);rig._process(.01)
    verify(adapter.accepted==1 and not rig.ornament.enabled and not rig.ornament_pivot.visible,"actual UDP switches rig")
    sender.put_packet('{"seq":2,"controls":{"ornament_secondary":true,"head_tilt":0.5}}'.to_utf8_buffer())
    await create_timer(.03).timeout;adapter.poll(.01,rig);rig._process(.01)
    verify(adapter.accepted==2 and rig.ornament.enabled,"actual UDP recovery")
    adapter.poll(2.1,rig);verify(not rig.ornament.initialized,"timeout resets accessory")
    adapter.stop();sender.close()
    if failures==0:print("ORNAMENT_CHECKS_PASS count=",checks," driver_peak=",peak," rig_peak=",live_peak)
    quit(1 if failures else 0)

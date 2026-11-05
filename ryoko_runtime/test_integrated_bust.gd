extends SceneTree
var failed=0
var checks=0
func ck(v,s):
    checks+=1
    if not v: push_error(s);failed+=1
func _initialize():call_deferred('run')
func run():
    var rig=load('res://motion_rig.tscn').instantiate();root.add_child(rig);await process_frame;rig.set_process(false)
    rig.apply_controls({'reset':true,'auto_blink':false,'body_follow':false,'look_x':.8,'look_y':-.3,'brow_screen_left':1,'brow_screen_right':-.5,'breath_level':1,'ornament_secondary':true})
    for i in range(120):rig._process(1.0/60)
    ck(rig.breathing.amount>.99 and rig.brows.current.x>.99 and rig.attention.head.y>.4,'combined states live')
    ck(rig.skin_material.get_shader_parameter('brow_enabled') and rig.skin_material.get_shader_parameter('ornament_separate'),'both fragment blocks enabled')
    rig.play_clip('res://demo_clip.json');rig.pause_clip(true)
    var state=[rig.breathing.amount,rig.brows.current,rig.attention.head,rig.ornament.angle,rig.clock_time]
    for i in range(60):rig._process(1.0/60)
    ck(state==[rig.breathing.amount,rig.brows.current,rig.attention.head,rig.ornament.angle,rig.clock_time],'pause freezes all')
    rig.pause_clip(false);rig._process(.1);ck(rig.clock_time>state[-1],'resume advances')
    rig.stop_clip()
    var ev=InputEventKey.new();ev.pressed=true;ev.keycode=KEY_O;ev.shift_pressed=true
    var b=rig.brows.target;rig._unhandled_key_input(ev)
    ck(not rig.ornament.enabled and rig.brows.target==b,'shift O only ornament')
    ev.shift_pressed=false;rig._unhandled_key_input(ev)
    ck(not rig.ornament.enabled and rig.brows.target==Vector2.ZERO,'plain O only brow')
    rig.apply_controls({'reset':true})
    ck(rig.breathing.amount==0 and rig.brows.current==Vector2.ZERO and rig.attention.head==Vector3.ZERO and not rig.ornament.initialized,'all reset')
    ck(not rig.ornament.enabled,'reset preserves ornament toggle')
    var a=load('res://live_input.gd').new();ck(a.start(19138)==OK,'bind')
    var sender=PacketPeerUDP.new();sender.set_dest_address('127.0.0.1',19138)
    sender.put_packet('{"seq":1,"controls":{"look_x":0.8,"brow_raise":1,"breath_level":1,"ornament_secondary":true}}'.to_utf8_buffer())
    await create_timer(.05).timeout;a.poll(.01,rig)
    for i in range(60):rig._process(1.0/60)
    ck(a.accepted==1 and rig.attention.active and rig.breathing.amount>.99 and rig.brows.current.x>.99 and rig.ornament.enabled,'joint UDP')
    a.poll(2.1,rig)
    ck(rig.breathing.amount==0 and rig.brows.current==Vector2.ZERO and not rig.attention.active and not rig.ornament.initialized,'joint timeout reset')
    a.stop();sender.close();rig.queue_free();await process_frame
    print('INTEGRATED_BUST_CHECKS_PASS count=',checks) if failed==0 else print('INTEGRATED_BUST_CHECKS_FAILED failures=',failed);quit(1 if failed else 0)

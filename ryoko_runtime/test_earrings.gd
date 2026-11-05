extends SceneTree
var checks=0
var failures=0
func check(value,label):
    checks+=1
    if not value:push_error("EARRINGS: "+label);failures+=1
func _initialize():call_deferred("run")
func run():
    var d=load("res://earring_driver.gd").new()
    for i in range(120):
        d.step(Vector2.ZERO,0,1.0/60)
        check(d.swing==0 and d.angle==0,"stationary anchor has no invented idle motion")
    var peak=0.0
    for i in range(200):
        d.step(Vector2(20,0),.1,1.0/60)
        peak=max(peak,abs(d.swing))
        check(abs(d.swing)<=d.SWING_LIMIT and abs(d.angle)<=d.RELATIVE_LIMIT,"bounded rigid angle")
    check(peak>.005,"anchor acceleration creates swing")
    for i in range(500):d.step(Vector2(20,0),.1,1.0/60)
    check(d.swing==0 and d.velocity==0 and is_equal_approx(d.angle,-.1),"gravity and settled pose")
    var before=d.angle
    for invalid in [[Vector2(NAN,0),0,.1],[Vector2.ZERO,INF,.1],[Vector2.ZERO,0,NAN],[Vector2.ZERO,0,0]]:
        d.step(invalid[0],invalid[1],invalid[2]);check(d.angle==before,"invalid input ignored")
    for dt in [.008,.016,.033,.1,.5]:
        for i in range(100):
            d.step(Vector2(100*(i%2),0),.15 if i%2 else -.15,dt)
            check(is_finite(d.angle) and abs(d.angle)<=d.RELATIVE_LIMIT,"stable frame stalls")
    d.enabled=false;d.step(Vector2.ZERO,0,.1)
    check(d.angle==0 and not d.initialized,"disabled driver resets")
    var rig=load("res://motion_rig.tscn").instantiate();root.add_child(rig)
    check(not rig.ornament_pivot.visible,"hairpin stays hidden until attachment initialized")
    for side in rig.earring_pivots:check(not rig.earring_pivots[side].visible,"earring stays hidden until attachment initialized")
    await process_frame;rig.set_process(false)
    rig.apply_controls({"reset":true,"auto_blink":false,"body_follow":false});rig._process(0)
    check(rig.earrings.size()==2,"two independent pendulums")
    check(rig.skin_material.get_shader_parameter("earring_separate")==Vector2.ZERO,"neutral preserves original pixels")
    for side in rig.earrings:
        var entry=rig.earring_metadata[side]
        var pivot=Vector2(entry.pivot[0],entry.pivot[1])
        check(pivot.y<650,"attachment above controlled-breath zone")
        check(not rig.earring_pivots[side].visible,"neutral original artwork")
    rig.apply_controls({"head_tilt":.8,"head_x":.6,"body_tilt":.4,"mouth":"A","gaze_x":.7,"brow_raise":.6,"breath_level":1})
    var split_peak=0.0
    for i in range(300):
        rig._process(1.0/60)
        split_peak=max(split_peak,abs(rig.earrings.screen_left.swing-rig.earrings.screen_right.swing))
        for side in rig.earrings:
            var entry=rig.earring_metadata[side];var pivot=Vector2(entry.pivot[0],entry.pivot[1])
            var expected=rig.deform_independent(pivot,rig.current,rig.body_current,sin(rig.clock_time*TAU/6.0))+Vector2(0,rig.bounce_position)
            check(rig.earring_pivots[side].position.distance_to(expected)<.0001,"ear attachment follows existing head transform")
            check(abs(rig.earrings[side].angle)<=d.RELATIVE_LIMIT,"runtime relative angle bounded")
    check(split_peak>.0001,"left and right respond independently to rotating anchors")
    for side in rig.earrings:
        check(rig.earring_pivots[side].visible,"tilt separates pendant")
        check(abs(rig.earring_pivots[side].rotation)<.002,"held tilt hangs close to vertical")
        check(rig.earring_pivots[side].scale==Vector2.ONE,"no pendant stretch or squash")
    check(rig.face.mouth_state=="A" and rig.breathing.amount>.99 and rig.brows.current.x>.59,"approved controls coexist")
    rig.play_clip("res://demo_clip.json");rig.pause_clip(true)
    var frozen=[rig.earrings.screen_left.angle,rig.earrings.screen_right.angle,rig.earring_pivots.screen_left.position,rig.clock_time]
    for i in range(50):rig._process(.033)
    check(frozen==[rig.earrings.screen_left.angle,rig.earrings.screen_right.angle,rig.earring_pivots.screen_left.position,rig.clock_time],"clip pause freezes pendulums")
    rig.stop_clip()
    rig.apply_controls({"earring_secondary":false});rig._process(.1)
    check(rig.skin_material.get_shader_parameter("earring_separate")==Vector2.ZERO,"off restores original source")
    for side in rig.earrings:check(not rig.earring_pivots[side].visible and not rig.earrings[side].initialized,"off hides and clears cutout")
    rig.apply_controls({"reset":true});check(not rig.earrings_enabled,"reset preserves disable setting")
    var e=InputEventKey.new();e.keycode=KEY_F;e.pressed=true;e.shift_pressed=true
    var hair_enabled=rig.hair.enabled;rig._unhandled_key_input(e)
    check(rig.earrings_enabled and rig.hair.enabled==hair_enabled,"Shift F controls only earrings")
    e.shift_pressed=false;rig._unhandled_key_input(e)
    check(rig.earrings_enabled and rig.hair.enabled!=hair_enabled,"plain F retains crown control")
    var adapter=load("res://live_input.gd").new()
    check(not adapter.decode('{"seq":1,"controls":{"earring_secondary":false}}'.to_utf8_buffer(),[]).is_empty(),"UDP boolean accepted")
    check(adapter.decode('{"seq":1,"controls":{"earring_secondary":1}}'.to_utf8_buffer(),[]).is_empty(),"UDP wrong type rejected")
    check(adapter.start(0)==OK,"local ephemeral UDP bind")
    var sender=PacketPeerUDP.new();sender.set_dest_address("127.0.0.1",adapter.socket.get_local_port())
    sender.put_packet('{"seq":1,"controls":{"earring_secondary":true,"head_tilt":-0.8}}'.to_utf8_buffer())
    await create_timer(.04).timeout;adapter.poll(.01,rig)
    for i in range(10):rig._process(1.0/30)
    check(adapter.accepted==1 and rig.earrings.screen_left.initialized,"actual UDP controls earrings")
    adapter.poll(2.1,rig)
    check(not rig.earrings.screen_left.initialized and not rig.earrings.screen_right.initialized,"timeout clears both dynamics")
    adapter.stop();sender.close()
    var c=load("res://clip_player.gd").new()
    check(c.load_data({"version":1,"duration":1,"cues":[{"time":0,"controls":{"earring_secondary":false}}]}),"clip boolean accepted")
    check(not c.load_data({"version":1,"duration":1,"cues":[{"time":0,"controls":{"earring_secondary":1}}]}),"clip wrong type rejected")
    var fixture="user://earring_clip_test.json"
    var file=FileAccess.open(fixture,FileAccess.WRITE)
    file.store_string(JSON.stringify({"version":1,"duration":2,"cues":[{"time":0,"controls":{"earring_secondary":false}},{"time":1,"controls":{"earring_secondary":true}}]}));file.close()
    check(rig.play_clip(fixture),"earring cue file loads")
    rig._process(.1);check(not rig.earrings_enabled,"actual clip cue disables earrings")
    rig.stop_clip();check(not rig.earrings_enabled,"cancellation preserves persistent toggle")
    rig.play_clip(fixture);rig._process(.1);rig.pause_clip(true);rig._process(2)
    check(not rig.earrings_enabled,"paused clip does not dispatch future earring cue")
    rig.pause_clip(false);rig._process(1)
    check(rig.earrings_enabled,"resume dispatches earring cue")
    rig.apply_controls({"earring_secondary":false})
    e.shift_pressed=true;rig._unhandled_key_input(e)
    check(not rig.clip.active and rig.earrings_enabled,"manual Shift F cancels clip before toggle")
    rig._process(2);check(rig.earrings_enabled,"cancelled future cues cannot overwrite manual toggle")
    DirAccess.remove_absolute(fixture)
    rig.queue_free();await process_frame
    print("EARRING_CHECKS_","PASS" if failures==0 else "FAIL"," count=",checks," failures=",failures," independent_peak=",split_peak)
    quit(1 if failures else 0)

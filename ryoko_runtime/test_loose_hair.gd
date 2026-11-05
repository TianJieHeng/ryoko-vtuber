extends SceneTree
# Local deterministic solver, control integration and actual loopback tests.
# Pixel/triangle interpolation safety is checked separately by rendered QA.
const Driver=preload("res://loose_hair_driver.gd")
const SIDES=["screen_left","screen_right"]
const DT=1.0/60.0
var checks=0
var failures=0
var driver_peak=0.0
var runtime_peak=0.0
var independent_peak=0.0

func check(value,label):
    checks+=1
    if not value:
        push_error("LOOSE_HAIR: "+label)
        failures+=1

func _initialize():call_deferred("run")

func driver_state(d):
    return [d.offset,d.velocity,d.previous_anchor,d.initialized,d.enabled]

func uniform_name(side):
    return "loose_hair_left" if side=="screen_left" else "loose_hair_right"

func loose_state(rig):
    return [driver_state(rig.loose_hair.screen_left),driver_state(rig.loose_hair.screen_right),rig.skin_material.get_shader_parameter("loose_hair_left"),rig.skin_material.get_shader_parameter("loose_hair_right"),rig.clock_time,rig.clip.elapsed]

func approved_state(rig):
    return [rig.target,rig.current,rig.body_target,rig.body_current,rig.body_follow,rig.clock_time,rig.hair.offset,rig.chest_offset,rig.bounce_position,rig.ornament.angle,rig.earrings.screen_left.angle,rig.earrings.screen_right.angle,rig.breathing.amount,rig.brows.current,rig.gaze.current,rig.attention.head,rig.attention.eye,rig.face.mouth_state,rig.face.blink_left,rig.face.blink_right,rig.face.expression]

func check_cleared(rig,label):
    for side in SIDES:
        var d=rig.loose_hair[side]
        check(d.offset==Vector2.ZERO and d.velocity==Vector2.ZERO and not d.initialized,label+" / "+side)

func test_weights():
    var d=Driver.new()
    for y in [0,120,330,570,588.2,600,795,795.8,830,920,1100,1384]:
        for x in [0,300,340,390.5,568,745.5,780,840,1136]:
            for side in SIDES:
                check(d.weight(Vector2(x,y),side)==0.0,"roots, protected upper row and lower body remain fixed")
    for y in range(0,1385,7):
        # These are the exact inner grid columns adjacent to the face/earrings.
        check(d.weight(Vector2(390.5,y),"screen_left")==0.0,"left protected inner grid column")
        check(d.weight(Vector2(745.5,y),"screen_right")==0.0,"right protected inner grid column")
        for x in [391,409,568,716,745]:
            for side in SIDES:
                check(d.weight(Vector2(x,y),side)==0.0,"face, fixed studs, earrings and collar have zero direct weight")
    for y in range(0,1385,13):
        for x in range(0,1137,17):
            var left=d.weight(Vector2(x,y),"screen_left")
            var right=d.weight(Vector2(x,y),"screen_right")
            check(left>=0 and left<=1 and right>=0 and right<=1,"weights bounded across source canvas")
            check(left*right==0.0,"outer tip domains never overlap")
    check(d.weight(Vector2(300,710),"screen_left")==1.0,"left free tip plateau")
    check(d.weight(Vector2(820,710),"screen_right")==1.0,"right free tip plateau")
    for point in [Vector2(360,710),Vector2(300,640),Vector2(300,770)]:
        check(d.weight(point,"screen_left")>0 and d.weight(point,"screen_left")<1,"left root, inner edge and bottom feather")
    for point in [Vector2(765,710),Vector2(820,640),Vector2(820,770)]:
        check(d.weight(point,"screen_right")>0 and d.weight(point,"screen_right")<1,"right root, inner edge and bottom feather")

func test_solver():
    var d=Driver.new()
    check(d.LIMIT==10.0,"source-pixel amplitude limit stays 10")
    for anchor in [Vector2.ZERO,Vector2(345,579),Vector2(-1000,2000)]:
        d.reset()
        for i in range(180):
            d.step(anchor,DT)
            check(d.offset==Vector2.ZERO and d.velocity==Vector2.ZERO,"initialization and stationary anchor have no invented idle motion")
    d.reset();d.step(Vector2.ZERO,DT);d.step(Vector2(8,0),DT)
    check(d.offset.x<0 and d.offset.y==0,"horizontal motion creates opposite inertial lag")
    var horizontal=d.offset.x
    d.reset();d.step(Vector2.ZERO,DT);d.step(Vector2(0,8),DT)
    check(d.offset.x==0 and d.offset.y<0 and is_equal_approx(d.offset.y,horizontal*.35),"vertical lag is deliberately reduced")
    for delta in [1.0/240,1.0/120,DT,1.0/30,.1,.5,5.0]:
        d.reset();d.step(Vector2.ZERO,delta)
        for i in range(180):
            var anchor=Vector2(1000 if i%2 else -1000,250 if i%3 else -250)
            d.step(anchor,delta)
            driver_peak=max(driver_peak,d.offset.length())
            check(d.offset.is_finite() and d.velocity.is_finite(),"alternating large impulses and stalls remain finite")
            check(d.offset.length()<=10.00001,"2D vector magnitude stays within ten source pixels")
        for i in range(900):d.step(d.previous_anchor,DT)
        check(d.offset==Vector2.ZERO and d.velocity==Vector2.ZERO,"held pose settles to exact zero at every tested frame rate")
    check(driver_peak>5,"test exercises visible dynamic range")
    d.reset();d.step(Vector2.ZERO,DT);d.step(Vector2(20,-5),DT)
    var before=driver_state(d)
    for invalid in [[Vector2(NAN,0),DT],[Vector2(0,NAN),DT],[Vector2(INF,0),DT],[Vector2(0,-INF),DT],[Vector2.ZERO,NAN],[Vector2.ZERO,INF],[Vector2.ZERO,-INF],[Vector2.ZERO,0.0],[Vector2.ZERO,-.1]]:
        d.step(invalid[0],invalid[1])
        check(driver_state(d)==before,"invalid samples leave all state unchanged")
    var a=Driver.new();var b=Driver.new()
    a.step(Vector2.ZERO,DT);b.step(Vector2.ZERO,DT)
    for i in range(40):
        var anchor=Vector2(i%2*40,i%3*10)
        a.step(anchor,.1);b.step(anchor,5.0)
        check(driver_state(a)==driver_state(b),"long stall integration is capped to .1 second")
    a.reset();b.reset();a.step(Vector2.ZERO,DT);b.step(Vector2.ZERO,DT)
    a.step(Vector2(20,3),DT);b.step(Vector2.ZERO,DT)
    check(a.offset!=Vector2.ZERO and b.offset==Vector2.ZERO,"driver instances do not share state")
    d.enabled=false;d.step(Vector2(999,-999),DT)
    check(d.offset==Vector2.ZERO and d.velocity==Vector2.ZERO and not d.initialized and d.previous_anchor==Vector2.ZERO,"disable clears complete solver state")
    d.enabled=true;d.step(Vector2(999,-999),DT)
    check(d.initialized and d.offset==Vector2.ZERO and d.previous_anchor==Vector2(999,-999),"reenable rebases at current anchor without a stale impulse")
    d.step(Vector2(-999,999),DT);d.reset()
    check(d.offset==Vector2.ZERO and d.velocity==Vector2.ZERO and d.previous_anchor==Vector2.ZERO and not d.initialized and d.enabled,"reset clears dynamics and preserves enabled setting")
    d.enabled=false;d.reset();check(not d.enabled,"reset also preserves disabled setting")

func run():
    test_weights()
    test_solver()
    var rig=load("res://motion_rig.tscn").instantiate()
    var reference=load("res://motion_rig.tscn").instantiate()
    root.add_child(rig);rig.set_process(false)
    root.add_child(reference);reference.set_process(false)
    await process_frame
    check(rig.loose_hair.size()==2 and rig.loose_hair.screen_left!=rig.loose_hair.screen_right,"runtime owns two independent tip drivers")
    check(not rig.live_input.active and not reference.live_input.active,"new motion does not open a live-input socket by default")
    var neutral={"reset":true,"auto_blink":false,"body_follow":false}
    rig.apply_controls(neutral);reference.apply_controls(neutral)
    reference.apply_controls({"loose_hair_secondary":false})
    for i in range(120):
        rig._process(DT);reference._process(DT)
        for side in SIDES:
            check(rig.loose_hair[side].offset==Vector2.ZERO,"runtime periodic breath does not create idle tip sway")
            check(rig.skin_material.get_shader_parameter(uniform_name(side))==Vector2.ZERO,"stationary runtime uploads exact zero")
    var combined={"head_tilt":.8,"head_x":.6,"head_y":-.2,"body_tilt":-.4,"body_x":.3,"body_y":.2,"mouth":"A","gaze_x":.7,"gaze_y":-.3,"brow_raise":.6,"breath_level":1,"eye_screen_left":.25,"eye_screen_right":.75}
    rig.apply_controls(combined);reference.apply_controls(combined)
    for i in range(300):
        if i==90:
            rig.apply_controls({"head_tilt":-.7,"body_tilt":.6});reference.apply_controls({"head_tilt":-.7,"body_tilt":.6})
        rig._process(DT);reference._process(DT)
        check(approved_state(rig)==approved_state(reference),"tip feature does not change approved body, face or accessory channels")
        var angle=rig.current.x*deg_to_rad(6.0)+rig.body_current.x*deg_to_rad(3.0)
        independent_peak=max(independent_peak,rig.loose_hair.screen_left.offset.distance_to(rig.loose_hair.screen_right.offset))
        for side in SIDES:
            var d=rig.loose_hair[side]
            runtime_peak=max(runtime_peak,d.offset.length())
            var root_position=Vector2(340,570) if side=="screen_left" else Vector2(780,570)
            var expected=rig.deform_independent(root_position,rig.current,rig.body_current,0)+Vector2(0,rig.bounce_position)
            check(d.previous_anchor.distance_to(expected)<.0001,"root follows approved head/body transform with periodic breath excluded")
            var uniform=rig.skin_material.get_shader_parameter(uniform_name(side))
            check(uniform.distance_to(d.offset.rotated(-angle))<.00001,"side-specific shader uniform receives local-frame lag")
            check(uniform.length()<=10.00001,"runtime shader offset magnitude bounded")
    check(runtime_peak>.1,"actual head and torso controls excite hair tips")
    check(independent_peak>.01,"rotating anchors produce independent left/right responses")
    check(rig.face.mouth_state=="A" and rig.breathing.amount>.99 and rig.brows.current.x>.59 and rig.gaze.current.x>.69,"combined approved controls still reach their targets")
    for i in range(900):rig._process(DT)
    for side in SIDES:
        check(rig.loose_hair[side].offset==Vector2.ZERO and rig.loose_hair[side].velocity==Vector2.ZERO,"held tilted runtime settles exactly without a periodic loop")
    rig.apply_controls({"loose_hair_secondary":false,"head_tilt":.8});rig._process(DT)
    check_cleared(rig,"disabled runtime clears both solvers")
    for side in SIDES:check(rig.skin_material.get_shader_parameter(uniform_name(side))==Vector2.ZERO,"off restores exact zero uniform")
    rig.apply_controls({"reset":true})
    check(not rig.loose_hair_enabled,"reset preserves persistent disable preference")
    check_cleared(rig,"reset clears both solvers immediately")
    rig.apply_controls({"loose_hair_secondary":true,"auto_blink":false,"body_follow":false})
    rig._process(DT)
    for side in SIDES:check(rig.loose_hair[side].offset==Vector2.ZERO,"group reenabling rebases both anchors")
    rig.apply_controls({"head_tilt":-.8});rig._process(DT)
    check(rig.loose_hair.screen_left.offset!=Vector2.ZERO,"reenabled group responds to fresh motion")
    rig.apply_controls({"reset":true})
    check(rig.loose_hair_enabled,"reset preserves persistent enable preference")
    check_cleared(rig,"active reset clears both dynamics")

    # Actual clip files exercise dispatch/ownership, not only the decoder.
    var c=load("res://clip_player.gd").new()
    for value in [false,true]:
        check(c.load_data({"version":1,"duration":3,"cues":[{"time":0,"controls":{"loose_hair_secondary":value}}]}),"typed clip accepts boolean tip toggle")
        check(c.play(),"validated toggle clip plays")
        check(c.step(.1)==[{"loose_hair_secondary":value}],"clip preserves exact boolean value")
    for value in [0,1,.5,"false",null,[],{}]:
        check(not c.load_data({"version":1,"duration":3,"cues":[{"time":0,"controls":{"loose_hair_secondary":value}}]}),"typed clip rejects every non-boolean toggle")
    var fixture="user://loose_hair_controls_test_%d.json"%OS.get_process_id()
    var file=FileAccess.open(fixture,FileAccess.WRITE)
    check(file!=null,"local clip fixture created")
    if file==null:
        rig.queue_free();reference.queue_free();await process_frame
        finish();return
    file.store_string(JSON.stringify({"version":1,"duration":3,"cues":[{"time":0,"controls":{"loose_hair_secondary":false}},{"time":1,"controls":{"loose_hair_secondary":true,"head_tilt":.8}},{"time":2,"controls":{"loose_hair_secondary":false}}]}));file.close()
    check(rig.play_clip(fixture),"actual tip-toggle clip loads")
    rig._process(.1)
    check(not rig.loose_hair_enabled,"actual time-zero cue disables tips")
    rig.stop_clip();check(not rig.loose_hair_enabled,"clip cancellation preserves disabled setting")
    check(rig.play_clip(fixture),"tip clip can replay")
    rig._process(.1);rig.pause_clip(true)
    var frozen=loose_state(rig)
    for i in range(40):rig._process(.1)
    check(loose_state(rig)==frozen and not rig.loose_hair_enabled,"paused clip freezes simulation clock and does not dispatch future toggle")
    rig.pause_clip(false);rig._process(1.0)
    check(rig.loose_hair_enabled,"resumed clip dispatches actual enable cue")
    rig._process(DT)
    check(rig.loose_hair.screen_left.offset.length()>0,"resumed clip motion excites tips")
    rig.pause_clip(true);frozen=loose_state(rig)
    for i in range(30):rig._process(.05)
    check(loose_state(rig)==frozen,"pause freezes nonzero offsets, velocities, anchors and uniforms exactly")
    rig.pause_clip(false);rig._process(DT)
    check(loose_state(rig)!=frozen,"resume advances dynamics again")
    rig.stop_clip();check(rig.loose_hair_enabled,"clip cancellation also preserves enabled setting")
    check(rig.play_clip(fixture),"clip restarts for keyboard takeover")
    rig._process(.1)
    var key=InputEventKey.new();key.keycode=KEY_X;key.pressed=true
    var existing_toggles=[rig.hair.enabled,rig.earrings_enabled,rig.ornament.enabled,rig.chest_enabled]
    key.echo=true;rig._unhandled_key_input(key)
    check(rig.clip.active and not rig.loose_hair_enabled,"key repeat neither toggles nor cancels clip")
    key.echo=false;key.pressed=false;rig._unhandled_key_input(key)
    check(rig.clip.active and not rig.loose_hair_enabled,"key release neither toggles nor cancels clip")
    key.pressed=true;rig._unhandled_key_input(key)
    check(not rig.clip.active and not rig.clip.paused and rig.loose_hair_enabled,"manual X cancels clip before toggling")
    rig._process(3)
    check(rig.loose_hair_enabled,"canceled future disable cue cannot overwrite X takeover")
    check(existing_toggles==[rig.hair.enabled,rig.earrings_enabled,rig.ornament.enabled,rig.chest_enabled],"X leaves all existing secondary toggles alone")
    rig._unhandled_key_input(key);rig._process(DT)
    check(not rig.loose_hair_enabled,"second fresh X reverses toggle")
    check_cleared(rig,"manual disable clears dynamics")
    rig.play_clip(fixture);rig._process(.1);rig.pause_clip(true);rig._unhandled_key_input(key)
    check(not rig.clip.active and not rig.clip.paused and rig.loose_hair_enabled,"manual X takes over from paused clip too")
    rig.play_clip(fixture);rig._process(.1);rig.apply_controls({"reset":true});rig._process(3)
    check(not rig.clip.active and not rig.loose_hair_enabled,"reset cancels future cues while preserving last toggle")

    # All packets use a kernel-assigned loopback port; no external server/CI.
    var adapter=load("res://live_input.gd").new()
    for value in [false,true]:
        var payload={"seq":1,"controls":{"loose_hair_secondary":value}}
        check(not adapter.decode(JSON.stringify(payload).to_utf8_buffer(),[]).is_empty(),"UDP decoder accepts boolean tip toggle")
    for value in [0,1,.5,"false",null,[],{}]:
        var payload={"seq":1,"controls":{"loose_hair_secondary":value}}
        check(adapter.decode(JSON.stringify(payload).to_utf8_buffer(),[]).is_empty(),"UDP decoder rejects non-boolean tip toggle")
    var bind_result=adapter.start(0)
    check(bind_result==OK,"actual ephemeral loopback UDP bind")
    if bind_result==OK:
        check(adapter.socket.get_local_port()>0,"kernel assigns nonzero ephemeral port")
        var sender=PacketPeerUDP.new()
        check(sender.set_dest_address("127.0.0.1",adapter.socket.get_local_port())==OK,"UDP sender addresses verified local port")
        rig.play_clip(fixture);rig._process(.1);rig.pause_clip(true)
        check(sender.put_packet('{"seq":1,"controls":{"loose_hair_secondary":true,"head_tilt":-0.8,"body_tilt":0.2}}'.to_utf8_buffer())==OK,"send actual enable packet")
        await create_timer(.04).timeout;adapter.poll(.01,rig)
        check(adapter.accepted==1 and rig.loose_hair_enabled and not rig.clip.active and not rig.clip.paused,"real UDP takes over paused clip and enables tips")
        for i in range(10):rig._process(DT)
        check(rig.loose_hair.screen_left.initialized and rig.loose_hair.screen_right.initialized,"real UDP initializes both runtime drivers")
        check(rig.loose_hair.screen_left.offset.length()>0,"real UDP head command drives tip motion")
        adapter.poll(adapter.TIMEOUT+.01,rig)
        check_cleared(rig,"UDP timeout clears both solver histories")
        check(rig.loose_hair_enabled and not adapter.leased,"UDP timeout preserves enabled preference and releases lease")
        check(sender.put_packet('{"seq":2,"controls":{"loose_hair_secondary":false}}'.to_utf8_buffer())==OK,"send actual disable packet")
        await create_timer(.04).timeout;adapter.poll(.01,rig);rig._process(DT)
        check(adapter.accepted==2 and not rig.loose_hair_enabled,"real UDP disables tips")
        check_cleared(rig,"real UDP disable clears both dynamics")
        for side in SIDES:check(rig.skin_material.get_shader_parameter(uniform_name(side))==Vector2.ZERO,"UDP disable zeros shader uniforms")
        check(sender.put_packet('{"seq":3,"controls":{"loose_hair_secondary":1}}'.to_utf8_buffer())==OK,"send actual invalid typed packet")
        check(sender.put_packet('{"seq":1,"controls":{"loose_hair_secondary":true}}'.to_utf8_buffer())==OK,"send actual stale packet")
        await create_timer(.04).timeout;adapter.poll(.01,rig)
        check(adapter.accepted==2 and adapter.rejected==2 and adapter.last_sequence==2 and not rig.loose_hair_enabled,"invalid and stale packets cannot change toggle or advance accepted sequence")
        adapter.poll(adapter.TIMEOUT+.01,rig)
        check(not rig.loose_hair_enabled and not adapter.leased,"UDP timeout also preserves disabled preference")
        check_cleared(rig,"disabled UDP timeout clears both dynamics")
        adapter.stop();sender.close()
        check(not adapter.active,"test closes loopback listener")
    check(DirAccess.remove_absolute(ProjectSettings.globalize_path(fixture))==OK,"temporary clip fixture removed")
    rig.queue_free();reference.queue_free();await process_frame
    finish()

func finish():
    print("LOOSE_HAIR_CHECKS_","PASS" if failures==0 else "FAIL"," count=",checks," failures=",failures," driver_peak=",driver_peak," runtime_peak=",runtime_peak," independent_peak=",independent_peak)
    quit(1 if failures else 0)

extends SceneTree
var checks=0
var failures=0
var serial=0
const BAD=[null,0,1,-1,0.5,"true","false",[],{},Vector2.ZERO,NAN,INF,-INF]
const FX=preload("res://optional_effects.gd")
func verify(value,label):
    checks+=1
    if not value:failures+=1;push_error("PENDANT: "+label)
func state(d):
    return [d.enabled,d.angle,d.swing,d.velocity,d.previous_anchor,d.previous_velocity,d.initialized]
func snapshot(rig):
    return [state(rig.pendant),rig.pendant_pivot.transform,rig.pendant_pivot.visible,rig.face.base_sprite.texture,
        rig.face.expression,rig.face.speech_override,rig.face.optional_effects.state.duplicate(),rig.target,rig.body_target,
        rig.current,rig.body_current,rig.chest_offset,rig.bounce_position,rig.clock_time,rig.external_controls,
        rig.clip.cues.duplicate(true),rig.clip.duration,rig.clip.elapsed,rig.clip.index,rig.clip.active,rig.clip.paused,
        rig.clip.dispatch_id,rig.clip_channels.duplicate(true),rig.gaze.target]
func controls_clip(controls):
    return {"version":1,"duration":2.0,"cues":[{"time":0.0,"controls":controls}]}
func play(rig,value):
    serial+=1
    var path="user://pendant_%d.json"%serial
    var file=FileAccess.open(path,FileAccess.WRITE)
    file.store_string(JSON.stringify(value));file.close()
    var result=rig.play_clip(path)
    DirAccess.remove_absolute(path)
    return result
func clean(rig):
    rig.apply_controls({"reset":true,"auto_blink":false,"body_follow":false,"pendant_secondary":true})
    # Inherited reset eases body/chest back; zero those only for a neutral fixture.
    rig.current=Vector3.ZERO;rig.body_current=Vector3.ZERO
    rig.chest_offset=Vector2.ZERO;rig.chest_velocity=Vector2.ZERO;rig.chest_initialized=false
    rig.bounce_position=0;rig.bounce_velocity=0
    rig._process(0)
func motion(rig):
    clean(rig)
    rig._process(1.0/60)
    rig.apply_controls({"body_tilt":0.8,"body_x":0.7,"breath_level":0.8})
    for i in range(20):rig._process(1.0/60)
    verify(rig.pendant_pivot.visible,"moving pendant separated")
func test_driver():
    var d=load("res://pendant_driver.gd").new()
    for i in range(180):
        d.step(Vector2.ZERO,0,1.0/60)
        verify(d.angle==0 and d.swing==0 and d.velocity==0,"stationary driver exactly neutral")
    var peak=0.0
    for i in range(180):
        d.step(Vector2(20,0),0.05,1.0/60)
        peak=max(peak,abs(d.swing))
        verify(abs(d.swing)<=d.SWING_LIMIT and abs(d.angle)<=d.RELATIVE_LIMIT,"transient bounded")
    verify(peak>.001,"horizontal acceleration creates short swing")
    for i in range(400):d.step(Vector2(20,0),0.05,1.0/60)
    verify(d.swing==0 and d.velocity==0 and is_equal_approx(d.angle,-0.05*d.VERTICAL_FOLLOW),"held frame settles toward vertical")
    d.reset()
    for i in range(300):d.step(Vector2(0,sin(i*.2)*20),0,1.0/60)
    verify(d.angle==0 and d.swing==0,"pure vertical translation cannot invent lateral swing")
    d.step(Vector2(12,0),.05,.016)
    var before=state(d)
    for bad in [[Vector2(NAN,0),0,.1],[Vector2(INF,0),0,.1],[Vector2(0,-INF),0,.1],
        [Vector2.ZERO,NAN,.1],[Vector2.ZERO,INF,.1],[Vector2.ZERO,-INF,.1],
        [Vector2.ZERO,0,NAN],[Vector2.ZERO,0,INF],[Vector2.ZERO,0,-INF],
        [Vector2.ZERO,0,0],[Vector2.ZERO,0,-1]]:
        d.step(bad[0],bad[1],bad[2]);verify(state(d)==before,"invalid and nonpositive dt are complete no-op")
    for dt in [1e-20,.001,.008,.016,.033,.1,.5,1000000.0]:
        for i in range(120):
            d.step(Vector2(1e30 if i%2 else -1e30,1e30 if i%3 else -1e30),1e30 if i%2 else -1e30,dt)
            verify(is_finite(d.angle) and is_finite(d.swing) and is_finite(d.velocity),"finite extreme caller inputs")
            verify(d.previous_anchor.is_finite() and d.previous_velocity.is_finite(),"bounded anchor state")
            verify(abs(d.angle)<=d.RELATIVE_LIMIT and abs(d.swing)<=d.SWING_LIMIT,"extreme inputs and stalls bounded")
    d.angle=NAN;d.step(Vector2.ZERO,0,.016)
    verify(is_finite(d.angle) and is_finite(d.velocity),"corrupted internal state recovers finite")
    d.enabled=false;d.reset()
    verify(not d.enabled and d.angle==0 and not d.initialized,"reset preserves disabled preference")
    d.step(Vector2(20,0),1,.1)
    verify(d.angle==0 and not d.initialized,"disabled driver clears dynamics")
    var a=load("res://pendant_driver.gd").new()
    var b=load("res://pendant_driver.gd").new()
    for i in range(400):
        var anchor=Vector2(sin(i*.07)*12,cos(i*.04)*4)
        a.step(anchor,sin(i*.02)*.05,1.0/60);b.step(anchor,sin(i*.02)*.05,1.0/60)
        verify(state(a)==state(b),"identical inputs deterministic")
    for i in range(600):a.step(Vector2.ZERO,0,1.0/60)
    verify(a.angle==0 and a.swing==0 and a.velocity==0,"quiet exact reset after settling")
func test_registration(rig):
    clean(rig)
    var md=rig.pendant_metadata
    verify(md.canvas==[1136.0,1384.0] and md.pivot==[563.5,933.0] and md.source_rect==[547.0,933.0,34.0,33.0],"verified source coordinates")
    verify(rig.pendant_pivot.position==Vector2(563.5,933),"source pivot fixed at lower original bail")
    verify(rig.pendant_pivot.get_parent()==rig.face and rig.face.get_parent() is SubViewport,"pendant inside original facial viewport")
    verify(rig.pendant_pivot.get_index()==rig.face.base_sprite.get_index()+1,"pendant follows base before face overlays")
    verify(rig.pendant_sprite.get_parent()==rig.pendant_pivot,"source cutout on pivot")
    verify(rig.pendant_sprite.region_rect==Rect2(547,933,34,33) and rig.pendant_sprite.region_enabled and not rig.pendant_sprite.centered,"tight source region")
    verify(rig.pendant_sprite.position==Vector2(547,933)-Vector2(563.5,933),"region registered to source pivot")
    verify(rig.pendant_sprite.region_filter_clip_enabled and rig.pendant_sprite.scale==Vector2.ONE and rig.pendant_pivot.scale==Vector2.ONE,"cutout clipped without local scale change")
    verify(rig.pendant_original_base==load("res://artwork/bust_base.png"),"preserved original texture resource")
    for texture in [rig.pendant_original_base,rig.pendant_cleared_base,rig.pendant_sprite.texture]:
        verify(texture.get_size()==Vector2(1136,1384),"full canvas texture registration")
    verify(rig.face.base_sprite.texture==rig.pendant_original_base and not rig.pendant_pivot.visible,"neutral uses exact original base")
    for angle in [-rig.pendant.RELATIVE_LIMIT,-.02,0,.02,rig.pendant.RELATIVE_LIMIT]:
        rig.pendant.angle=angle;rig._sync_pendant_render_state()
        verify(rig.pendant_pivot.position==Vector2(563.5,933),"rotation cannot move attachment")
        verify(rig.pendant_sprite.transform*Vector2(16.5,0)==Vector2.ZERO,"texture bail maps to pivot origin")
        verify(rig.pendant_pivot.visible==(angle!=0),"zero bypass and nonzero visibility")
        verify(rig.face.base_sprite.texture==(rig.pendant_original_base if angle==0 else rig.pendant_cleared_base),"base switches with cutout visibility")
    clean(rig)
    # Independently check one actual mesh triangle's affine interpolation.
    var cell=Vector2(1136.0/32,1384.0/40)
    var point=Vector2(563.5,933)
    rig.body_current=Vector3(.6,.3,-.4);rig.chest_offset=Vector2(3,-2);rig.bounce_position=-4;rig.breathing.amount=.8
    var grid=point/cell;var base=Vector2(floor(grid.x),floor(grid.y));var uv=grid-base
    var corners=[base*cell,(base+Vector2(1,0))*cell,(base+Vector2(0,1))*cell,(base+Vector2.ONE)*cell]
    var vertices=[]
    for p in corners:
        var torso=(p-Vector2(568,1340)).rotated(.6*deg_to_rad(3))+Vector2(568,1340)+Vector2(.3*8,-.4*5-4)
        var soft=smoothstep(920.0,1050.0,p.y)*(1-smoothstep(1280.0,1384.0,p.y))*(1-smoothstep(310.0,480.0,abs(p.x-568)))
        var ribs=smoothstep(850.0,1000.0,p.y)
        var inhale=Vector2((p.x-568)*.012*ribs,-4)*.8
        vertices.append(torso+Vector2(3,-2)*soft+inhale.rotated(.6*deg_to_rad(3)))
    var expected=vertices[0]+(vertices[1]-vertices[0])*uv.x+(vertices[2]-vertices[0])*uv.y if uv.x+uv.y<=1 else vertices[3]+(vertices[2]-vertices[3])*(1-uv.x)+(vertices[1]-vertices[3])*(1-uv.y)
    verify(rig._pendant_attachment_point(point).distance_to(expected)<.0002,"driver attachment matches actual shared mesh triangle")
    var anchor=rig._pendant_attachment_point(point)
    rig.current=Vector3.ONE;rig.clock_time=91
    verify(rig._pendant_attachment_point(point)==anchor,"head and baseline breath excluded from attachment driver")
func test_motion(rig):
    clean(rig)
    for i in range(360):
        rig.apply_controls({"head_tilt":sin(i*.05),"head_x":cos(i*.06),"head_y":sin(i*.07)})
        rig._process(1.0/60)
        verify(rig.pendant.angle==0 and rig.pendant.swing==0,"head-only and periodic baseline breath do not drive pendant")
        verify(rig.face.base_sprite.texture==rig.pendant_original_base and not rig.pendant_pivot.visible,"head-only preserves inherited pendant pixels")
    motion(rig)
    var anchor=rig.pendant.previous_anchor
    rig.apply_controls({"bounce":true,"body_tilt":-.8,"body_x":-.7,"breath_level":1})
    var peak=0.0
    for i in range(360):
        rig._process(1.0/60);peak=max(peak,abs(rig.pendant.swing))
        verify(abs(rig.pendant.angle)<=rig.pendant.RELATIVE_LIMIT and abs(rig.pendant.swing)<=rig.pendant.SWING_LIMIT,"combined body chest bounce breath bounded")
        verify(rig.pendant_pivot.position==Vector2(563.5,933),"source pivot invariant under body deformation")
        verify(rig.pendant.previous_anchor.distance_to(rig._pendant_attachment_point(Vector2(563.5,933)))<.0001,"driver follows current attachment")
    verify(peak>.001 and anchor!=rig.pendant.previous_anchor,"torso transition drives pendant")
    rig.apply_controls({"body_tilt":0,"body_x":0,"body_y":0,"head_tilt":0,"breath_level":0})
    for i in range(900):rig._process(1.0/60)
    verify(rig.pendant.angle==0 and rig.pendant.swing==0,"return to quiet exactly original")
    verify(not rig.pendant_pivot.visible and rig.face.base_sprite.texture==rig.pendant_original_base,"settle restores original source path")
    motion(rig)
    rig.apply_controls({"pendant_secondary":false})
    verify(not rig.pendant.enabled and not rig.pendant_pivot.visible and not rig.pendant.initialized and rig.pendant.angle==0,"direct off immediate, clears dynamics")
    verify(rig.face.base_sprite.texture==rig.pendant_original_base,"direct off texture immediate")
    rig.apply_controls({"reset":true})
    verify(not rig.pendant.enabled and not rig.pendant.initialized,"reset retains disabled preference")
    rig.apply_controls({"pendant_secondary":true});rig._process(.016)
    rig.apply_controls({"reset":true})
    verify(rig.pendant.enabled and rig.pendant.angle==0 and not rig.pendant.initialized and not rig.pendant_pivot.visible,"enabled reset immediately clears and preserves setting")
func test_validation_and_clips(rig):
    var player=load("res://clip_player.gd").new()
    var decoder=load("res://live_input.gd").new()
    for paused in [false,true]:
        motion(rig)
        verify(play(rig,controls_clip({"pendant_secondary":true,"effects":{"anger":true},"head_tilt":.2})),"baseline clip loads")
        rig._process(.2);rig.pause_clip(paused)
        for value in BAD:
            for source in ["external","clip","local"]:
                var before=snapshot(rig)
                verify(not rig.apply_controls({"reset":true,"head_tilt":-1,"effects":{"tear_L":true},"pendant_secondary":value},source),"malformed direct flag rejected before any mutation")
                verify(snapshot(rig)==before,"invalid direct patch atomic during active/paused clip")
            verify(not player.load_data(controls_clip({"pendant_secondary":value})),"typed clip boolean rejection")
            if not value is Vector2 and not (value is float and not is_finite(value)):
                verify(decoder.decode(JSON.stringify({"seq":1,"controls":{"reset":true,"pendant_secondary":value}}).to_utf8_buffer(),rig.expression_ids).is_empty(),"UDP decoder strict boolean")
                var before=snapshot(rig)
                var invalid=controls_clip({"pendant_secondary":false})
                invalid.cues.append({"time":1,"controls":{"reset":true,"pendant_secondary":value}})
                verify(not play(rig,invalid),"late invalid replacement rejected")
                verify(snapshot(rig)==before,"late invalid replacement atomic active/paused")
    motion(rig)
    play(rig,{"version":1,"duration":2,"cues":[{"time":1,"controls":{"pendant_secondary":false}}]})
    rig.pause_clip(true)
    var frozen=snapshot(rig)
    for i in range(60):rig._process(.1)
    verify(snapshot(rig)==frozen,"pause freezes full pendant state, texture, pivot, rig and clip clock")
    rig.apply_controls({"pendant_secondary":false})
    verify(rig.clip.paused and not rig.pendant_pivot.visible and not rig.pendant.initialized,"paused direct off immediate without advancing clip")
    verify(rig.face.base_sprite.texture==rig.pendant_original_base,"paused off uses original source")
    rig.apply_controls({"pendant_secondary":true})
    verify(rig.clip.paused and rig.pendant.enabled and not rig.pendant.initialized and not rig.pendant_pivot.visible,"paused direct on starts quiet without advancing")
    frozen=snapshot(rig);rig._process(1)
    verify(snapshot(rig)==frozen,"paused on remains held")
    rig.pause_clip(false);rig._process(.1)
    verify(rig.pendant.initialized and rig.pendant_pivot.visible,"resume updates attachment and renders held body tilt")
    rig._process(1)
    verify(not rig.pendant.enabled and not rig.pendant_pivot.visible,"resumed future cue disables pendant")
    rig.stop_clip()
    verify(not rig.pendant.enabled and not rig.pendant.initialized,"clip cancel preserves toggle and clears state")
    motion(rig);play(rig,controls_clip({"pendant_secondary":true}));rig._process(.1)
    rig.stop_clip()
    verify(rig.pendant.enabled and not rig.pendant.initialized and rig.pendant.angle==0,"enabled cancel clears dynamics")
    verify(not rig.pendant_pivot.visible and rig.face.base_sprite.texture==rig.pendant_original_base,"cancel switches immediately to original")
    rig._process(.1)
    var settled=state(rig.pendant);rig.stop_clip()
    verify(state(rig.pendant)==settled,"repeated inactive cancel does not erase later dynamics")
    play(rig,{"version":1,"duration":2,"cues":[{"time":0,"controls":{"pendant_secondary":true}},{"time":.2,"controls":{"reset":true}},{"time":.2,"controls":{"pendant_secondary":false}}]})
    rig._process(3)
    verify(rig.pendant.enabled and not rig.clip.active,"reset invalidates already-collected later pendant cue")
func test_expression_compatibility(rig):
    motion(rig)
    var state_all={}
    for key in FX.NAMES:state_all[key]=true
    verify(rig.expression_ids.size()==93,"all inherited expressions present")
    rig.apply_controls({"effects":state_all,"gaze_x":.8,"gaze_y":-.6,"brow_raise":.7,"breath_level":.5})
    for id in ["neutral"]+rig.expression_ids:
        verify(rig.apply_controls({"expression":id}),"existing expression accepted "+id)
        for blink in [0,1]:
            for mouth in ["A","E","I","O","U","neutral","RELEASE"]:
                verify(rig.apply_controls({"blink":blink,"mouth":mouth}),"mouth/blink coexist "+id)
                rig._process(0)
                verify(rig.face.expression==id and rig.face.blink_left==bool(blink) and rig.face.blink_right==bool(blink),"expression/blink preserved")
                verify(rig.pendant_pivot.visible and rig.face.base_sprite.texture==rig.pendant_cleared_base,"moving pendant survives expression/mouth/blink")
                verify(rig.face.mouth_state==(mouth if mouth!="RELEASE" else ("neutral" if id=="neutral" else id+"_rest")),"mouth state unchanged")
                for effect in FX.NAMES:verify(rig.face.optional_effects.state[effect] and rig.face.optional_effects.sprites[effect].visible,"optional effects coexist "+effect)
                if id!="neutral":
                    for fx in rig.face.emotion_effects[id]:verify(fx.visible==(mouth=="RELEASE" or not fx.get_meta("rest_only",false)),"authored effects unchanged")
    rig.apply_controls({"pendant_secondary":false})
    verify(rig.face.optional_effects.state==state_all and rig.face.expression==rig.expression_ids[-1],"pendant disable does not reset facial channels")
func test_udp(rig):
    var adapter=load("res://live_input.gd").new()
    verify(adapter.start(0)==OK,"actual loopback ephemeral bind")
    if not adapter.active:return
    var sender=PacketPeerUDP.new()
    verify(sender.set_dest_address("127.0.0.1",adapter.socket.get_local_port())==OK,"actual loopback destination")
    var seq=0
    for paused in [false,true]:
        for malformed in [null,0,1,"true",[],{}]:
            motion(rig);play(rig,controls_clip({"pendant_secondary":true}));rig._process(.1);rig.pause_clip(paused)
            var before=snapshot(rig);seq+=1
            sender.put_packet(JSON.stringify({"seq":seq,"controls":{"reset":true,"body_tilt":-1,"pendant_secondary":malformed}}).to_utf8_buffer())
            await create_timer(.012).timeout;adapter.poll(.01,rig)
            verify(snapshot(rig)==before,"invalid real UDP cannot cancel active/paused clip")
            verify(adapter.last_sequence==seq-1 if seq>1 else adapter.last_sequence==-1,"invalid UDP does not consume sequence")
            sender.put_packet(JSON.stringify({"seq":seq,"controls":{"pendant_secondary":false,"body_tilt":-.6}}).to_utf8_buffer())
            await create_timer(.012).timeout;adapter.poll(.01,rig)
            verify(not rig.clip.active and not rig.clip.paused and not rig.pendant.enabled,"valid real UDP takeover reuses rejected sequence")
            verify(not rig.pendant_pivot.visible and rig.face.base_sprite.texture==rig.pendant_original_base,"real UDP off immediate")
            verify(adapter.last_sequence==seq and is_equal_approx(rig.body_target.x,-.6),"real UDP applies accompanying body control")
    verify(adapter.accepted==seq and adapter.rejected==seq,"actual UDP acceptance/rejection counts")
    var before=snapshot(rig)
    sender.put_packet(JSON.stringify({"seq":seq,"controls":{"pendant_secondary":true}}).to_utf8_buffer())
    await create_timer(.012).timeout;adapter.poll(.01,rig)
    verify(snapshot(rig)==before and adapter.rejected==seq+1,"stale actual UDP rejected")
    adapter.poll(2.1,rig)
    verify(not rig.pendant.enabled and not rig.pendant.initialized and not rig.pendant_pivot.visible,"timeout preserves disabled preference and clears dynamics")
    seq+=1
    sender.put_packet(JSON.stringify({"seq":seq,"controls":{"pendant_secondary":true,"body_tilt":.8}}).to_utf8_buffer())
    await create_timer(.012).timeout;adapter.poll(.01,rig)
    for i in range(30):rig._process(.016)
    verify(rig.pendant.enabled and rig.pendant.initialized and rig.pendant_pivot.visible,"real UDP on and motion")
    adapter.poll(2.1,rig)
    verify(rig.pendant.enabled and not rig.pendant.initialized and rig.pendant.angle==0 and not rig.pendant_pivot.visible,"enabled timeout preserves preference and clears immediately")
    verify(rig.face.base_sprite.texture==rig.pendant_original_base,"timeout restores original source immediately")
    adapter.stop();sender.close()
func _initialize():call_deferred("run")
func run():
    test_driver()
    var rig=load("res://motion_rig.tscn").instantiate();root.add_child(rig)
    verify(not rig.pendant_pivot.visible and rig.face.base_sprite.texture==rig.pendant_original_base,"startup never renders uninitialized layer")
    await process_frame;rig.set_process(false)
    test_registration(rig)
    test_motion(rig)
    test_validation_and_clips(rig)
    test_expression_compatibility(rig)
    await test_udp(rig)
    clean(rig);rig.queue_free();await process_frame
    print("PENDANT_CHECKS_","PASS" if failures==0 else "FAIL"," count=",checks," failures=",failures)
    quit(1 if failures else 0)

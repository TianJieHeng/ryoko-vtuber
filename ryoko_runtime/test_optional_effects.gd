extends SceneTree
var checks=0
var failures=0
var serial=0
const FX=preload("res://optional_effects.gd")
const BAD=[null, false, true, 0, 1, "blush_L", [], {"blush":true}, {"blush_L":1}, {"tear_R":"false"}, {"sweat":null}, {"anger":[]}, {"sparkle":{}}, {"blush_L":true,"bad":false}]
func verify(value,label):
    checks+=1
    if not value:failures+=1;push_error("OPTIONAL_EFFECTS: "+label)
func controls_clip(controls):
    return {"version":1,"duration":2.0,"cues":[{"time":0.0,"controls":controls}]}
func fixture(value):
    serial+=1
    var path="user://optional_effects_%d.json"%serial
    var file=FileAccess.open(path,FileAccess.WRITE)
    file.store_string(JSON.stringify(value));file.close()
    return path
func play(rig,value):
    var path=fixture(value)
    var result=rig.play_clip(path)
    DirAccess.remove_absolute(path)
    return result
func snapshot(rig):
    return [rig.face.optional_effects.state.duplicate(),rig.face.expression,rig.target,rig.external_controls,
        rig.clip.cues.duplicate(true),rig.clip.duration,rig.clip.elapsed,rig.clip.index,rig.clip.active,rig.clip.paused,
        rig.clip.dispatch_id,rig.clip_channels.duplicate(true),rig.face.speech_override,rig.gaze.target]
func clean(rig):
    rig.apply_controls({"reset":true,"auto_blink":false})
func check_state(rig,state,label):
    verify(rig.face.optional_effects.state==state,label+" values")
    for key in FX.NAMES:verify(rig.face.optional_effects.sprites[key].visible==state[key],label+" visibility "+key)
func all_state(enabled):
    var value={}
    for key in FX.NAMES:value[key]=enabled
    return value
func test_defaults_and_combinations(rig):
    check_state(rig,all_state(false),"startup")
    var registration=JSON.parse_string(FileAccess.get_file_as_string("res://registration.json"))
    verify(rig.expression_ids.size()==93 and rig.face.emotion_eyes.size()==registration.expressions.size(),"original expression registry unchanged")
    for mask in range(128):
        var state={}
        for i in range(FX.NAMES.size()):state[FX.NAMES[i]]=bool(mask & (1<<i))
        verify(rig.apply_controls({"effects":state}),"accept combination "+str(mask))
        check_state(rig,state,"combination "+str(mask))
    for key in FX.NAMES:
        clean(rig)
        verify(rig.apply_controls({"effects":{key:true}}),"enable independent "+key)
        var state=all_state(false);state[key]=true
        check_state(rig,state,"independent "+key)
        verify(rig.apply_controls({"effects":{}}),"empty patch is no-op")
        check_state(rig,state,"empty patch")
        verify(rig.apply_controls({"expression":"neutral"}),"neutral expression selection")
        check_state(rig,state,"selection preserves optional state")
        rig.face.reset_neutral()
        check_state(rig,all_state(false),"direct neutral reset")
    rig.apply_controls({"effects":all_state(true)})
    clean(rig)
    check_state(rig,all_state(false),"rig neutral reset")
func test_validation(rig):
    var player=load("res://clip_player.gd").new()
    var decoder=load("res://live_input.gd").new()
    for value in BAD:
        for source in ["external","clip","local"]:
            var before=snapshot(rig)
            verify(not rig.apply_controls({"reset":true,"head_tilt":1,"effects":value},source),"reject malformed API "+str(value))
            verify(snapshot(rig)==before,"API all-or-nothing "+str(value))
        verify(not rig.face.optional_effects.apply(value),"direct overlay rejects malformed value")
        verify(not player.load_data(controls_clip({"effects":value})),"clip rejects malformed value")
        verify(decoder.decode(JSON.stringify({"seq":1,"controls":{"reset":true,"effects":value}}).to_utf8_buffer(),rig.expression_ids).is_empty(),"decoder rejects malformed value")
    verify(not FX.valid({1:true}) and not FX.valid({"anger":NAN}) and not FX.valid({"anger":INF}),"non-JSON key and values rejected")
    for paused in [false,true]:
        clean(rig)
        verify(play(rig,controls_clip({"effects":{"tear_L":true},"head_tilt":0.3})),"load baseline clip")
        rig._process(0.2);rig.pause_clip(paused)
        for value in BAD:
            var before=snapshot(rig)
            var invalid=controls_clip({"effects":{"anger":true}})
            invalid.cues.append({"time":1,"controls":{"reset":true,"head_tilt":-1,"effects":value}})
            verify(not play(rig,invalid),"invalid late replacement rejected")
            verify(snapshot(rig)==before,"invalid replacement atomic active/paused")
    var source=controls_clip({"effects":{"sparkle":true}})
    verify(player.load_data(source) and player.play(),"copy source")
    source.cues[0].controls.effects.sparkle=false
    var due=player.step(0)
    verify(due[0].effects.sparkle,"validated cue deep copy")
    due[0].effects.sparkle=false
    verify(player.cues[0].controls.effects.sparkle,"dispatch deep copy")
func test_clips(rig):
    clean(rig)
    rig.apply_controls({"effects":{"sweat":true,"blush_R":true}})
    var timeline={"version":1,"duration":2.0,"cues":[
        {"time":0,"controls":{"effects":{"anger":true}}},
        {"time":0.5,"controls":{"effects":{"anger":false,"tear_L":true}}},
        {"time":0.5,"controls":{"effects":{"sparkle":true}}},
        {"time":2,"controls":{"effects":{"tear_L":false}}}]}
    verify(play(rig,timeline),"clip loads")
    rig._process(0)
    verify(rig.face.optional_effects.state.anger,"time zero dispatch")
    rig.pause_clip(true)
    var before=snapshot(rig)
    rig._process(20)
    verify(snapshot(rig)==before,"pause freezes effects and clip")
    rig.pause_clip(false);rig._process(0.5)
    verify(not rig.face.optional_effects.state.anger and rig.face.optional_effects.state.tear_L and rig.face.optional_effects.state.sparkle,"same-time ordered cue dispatch")
    rig.stop_clip()
    var state=all_state(false);state.sweat=true;state.blush_R=true
    check_state(rig,state,"cancel clears only owned keys")
    rig.apply_controls({"effects":{"anger":true}});rig.stop_clip()
    verify(rig.face.optional_effects.state.anger,"inactive repeated cancellation preserves later controls")
    clean(rig);play(rig,timeline);rig._process(3)
    verify(not rig.clip.active and rig.face.optional_effects.state.sparkle and not rig.face.optional_effects.state.tear_L,"natural completion holds final state")
    rig.stop_clip()
    verify(rig.face.optional_effects.state.sparkle,"inactive completion stop preserves state")
    play(rig,timeline);rig._process(0)
    verify(rig.face.optional_effects.state.anger,"replay starts first cue")
    rig.pause_clip(true)
    verify(play(rig,controls_clip({"effects":{"sweat":true}})),"valid paused replacement")
    verify(not rig.clip.paused and not rig.face.optional_effects.state.anger and rig.face.optional_effects.state.sparkle,"replacement only releases this run's touched keys")
    rig._process(0)
    verify(rig.face.optional_effects.state.sweat,"replacement dispatch")
    var reset_clip={"version":1,"duration":2.0,"cues":[
        {"time":0,"controls":{"effects":{"anger":true}}},
        {"time":0.5,"controls":{"reset":true}},
        {"time":0.5,"controls":{"effects":{"sweat":true}}}]}
    play(rig,reset_clip);rig._process(3)
    check_state(rig,all_state(false),"reset invalidates collected same-frame cues")
    verify(not rig.clip.active and rig.clip_channels.is_empty(),"reset cancels ownership")
func test_expressions(rig):
    clean(rig)
    var state=all_state(true)
    rig.apply_controls({"effects":state})
    for id in ["neutral"]+rig.expression_ids:
        rig.apply_controls({"expression":id,"gaze_x":0.7,"gaze_y":-0.6})
        for blink in [0,1]:
            for mouth in ["A","E","I","O","U","neutral","RELEASE"]:
                rig.apply_controls({"blink":blink,"mouth":mouth})
                rig._process(0)
                check_state(rig,state,"independent expression/blink/mouth "+id)
                if id!="neutral":
                    for fx in rig.face.emotion_effects[id]:
                        verify(fx.visible==(rig.face.speech_override=="" or not fx.get_meta("rest_only",false)),"authored effects retain original visibility "+id)
        # Removing overlays must not hide the selected expression's own effects.
        rig.apply_controls({"effects":all_state(false),"mouth":"RELEASE"})
        if id!="neutral":
            for fx in rig.face.emotion_effects[id]:verify(fx.visible,"authored effect survives optional false "+id)
        rig.apply_controls({"effects":state})
func test_render_registration(rig):
    clean(rig);rig._process(0)
    verify(not rig.effects_surface.visible and rig.effects_viewport.render_target_update_mode==SubViewport.UPDATE_DISABLED,"unused effects pass hidden and disabled")
    verify(rig.effects_surface.mesh==rig.surface.mesh,"same grid resource")
    verify(rig.effects_viewport.size==Vector2i(1136,1384) and rig.effects_viewport.transparent_bg,"matching transparent coordinates")
    verify(rig.face.optional_effects.get_parent()==rig.effects_viewport,"effects separated from gaze replacement")
    verify(rig.effects_surface.get_index()>rig.surface.get_index(),"effects composite after authored face")
    var manifest=JSON.parse_string(FileAccess.get_file_as_string("res://rig_assets/effects/manifest.json"))
    for key in FX.NAMES:
        var entry=manifest.effects[key]
        var sprite=rig.face.optional_effects.sprites[key]
        verify(not sprite.centered and sprite.region_enabled,"registered region sprite "+key)
        verify(sprite.position==Vector2(entry.position[0],entry.position[1]),"registered position "+key)
        verify((sprite.region_rect.size*sprite.scale).is_equal_approx(Vector2(entry.size[0],entry.size[1])),"registered scale "+key)
    rig.apply_controls({"effects":all_state(true),"head_tilt":0.8,"head_x":0.7,"head_y":-0.4,
        "body_tilt":-0.6,"body_x":-0.5,"body_y":0.4,"breath_level":1.0,"bounce":true,
        "gaze_x":1,"gaze_y":-1,"brow_raise":1,"loose_hair_secondary":true})
    for i in range(60):
        rig._process(1.0/30)
        verify(rig.effects_surface.visible and rig.effects_viewport.render_target_update_mode==SubViewport.UPDATE_ALWAYS,"enabled overlay renders")
        verify(rig.effects_surface.transform==rig.surface.transform,"identical mesh registration under motion")
        verify(rig.effects_uniforms.size()==10,"all shared vertex uniforms discovered")
        for key in rig.effects_uniforms:
            verify(rig.effects_material.get_shader_parameter(key)==rig.skin_material.get_shader_parameter(key),"shared deformation "+str(key))
    play(rig,controls_clip({"effects":{"anger":true},"head_tilt":-1}))
    rig._process(0.2);rig.pause_clip(true)
    var frozen=[]
    for key in rig.effects_uniforms:frozen.append(rig.effects_material.get_shader_parameter(key))
    rig.apply_controls({"effects":{"anger":false}});rig._process(5)
    for i in range(rig.effects_uniforms.size()):
        verify(rig.effects_material.get_shader_parameter(rig.effects_uniforms[i])==frozen[i],"paused mesh deformation frozen")
    verify(not rig.face.optional_effects.sprites.anger.visible,"paused optional patch refreshes")
    clean(rig);rig._process(0)
    verify(not rig.effects_surface.visible,"reset hides effects pass")
    for key in rig.effects_uniforms:
        verify(rig.effects_material.get_shader_parameter(key)==rig.skin_material.get_shader_parameter(key),"reset deformation synchronized")

func test_udp(rig):
    var adapter=load("res://live_input.gd").new()
    verify(adapter.start(0)==OK,"loopback bind")
    if not adapter.active:return
    var sender=PacketPeerUDP.new()
    verify(sender.set_dest_address("127.0.0.1",adapter.socket.get_local_port())==OK,"loopback destination")
    var seq=0
    for paused in [false,true]:
        for malformed in BAD:
            clean(rig)
            rig.apply_controls({"effects":{"blush_R":true}})
            play(rig,controls_clip({"effects":{"tear_L":true}}));rig._process(0.2);rig.pause_clip(paused)
            var before=snapshot(rig)
            seq+=1
            sender.put_packet(JSON.stringify({"seq":seq,"controls":{"reset":true,"head_tilt":1,"effects":malformed}}).to_utf8_buffer())
            await create_timer(0.01).timeout
            adapter.poll(0.01,rig)
            verify(snapshot(rig)==before,"invalid UDP cannot take over active/paused clip")
            verify(adapter.last_sequence==(-1 if seq==1 else seq-1),"invalid UDP does not claim sequence")
            sender.put_packet(JSON.stringify({"seq":seq,"controls":{"effects":{"tear_R":true,"sweat":false}}}).to_utf8_buffer())
            await create_timer(0.01).timeout
            adapter.poll(0.01,rig)
            verify(not rig.clip.active and not rig.clip.paused,"valid UDP takeover")
            var state=all_state(false);state.blush_R=true;state.tear_R=true
            check_state(rig,state,"UDP retains untouched live effects and releases clip effects")
            verify(adapter.last_sequence==seq,"valid reuse of rejected sequence")
    verify(adapter.accepted==seq and adapter.rejected==seq,"all actual UDP messages accounted")
    adapter.poll(2.1,rig)
    check_state(rig,all_state(false),"live timeout resets overlays")
    adapter.stop();sender.close()
func _initialize():call_deferred("run")
func run():
    var rig=load("res://motion_rig.tscn").instantiate()
    root.add_child(rig);await process_frame;rig.set_process(false)
    test_defaults_and_combinations(rig)
    test_validation(rig)
    test_clips(rig)
    test_expressions(rig)
    test_render_registration(rig)
    await test_udp(rig)
    clean(rig);rig.queue_free();await process_frame
    print("OPTIONAL_EFFECTS_CHECKS_", "PASS" if failures==0 else "FAIL", " count=",checks," failures=",failures)
    quit(1 if failures else 0)

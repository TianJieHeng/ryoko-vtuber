extends SceneTree
var checks=0
var failures=0
func verify(ok,label):
    checks+=1
    if not ok:failures+=1;push_error("RELEASE_CONTROLS: "+label)
func packet(controls,seq=1):return JSON.stringify({"seq":seq,"controls":controls}).to_utf8_buffer()
func clip_data(controls):return {"version":1,"duration":10,"cues":[{"time":0,"controls":controls}]}
func key(rig,code,shift=false):
    var event=InputEventKey.new();event.keycode=code;event.pressed=true;event.shift_pressed=shift
    rig._unhandled_key_input(event)
func snapshot(rig):
    return [rig.clip.active,rig.clip.paused,rig.clip.elapsed,rig.clip.dispatch_id,rig.clip_channels.duplicate(true),rig.external_controls,rig.target,rig.face.expression,rig.expression_player.active,rig.expression_player.id,rig.expression_player.pending.duplicate(true),rig.expression_player.elapsed,rig.expression_player.recovering]
func _initialize():call_deferred("run")
func run():
    var rig=load("res://motion_rig.tscn").instantiate();root.add_child(rig)
    await process_frame;rig.set_process(false)
    var ids=rig.expression_ids
    var supported=rig.expression_player.profiles.keys()
    verify(ids.size()==93,"all 93 static expressions remain")
    verify(supported==["EXP-005"],"only approved performance ships")
    var adapter=load("res://live_input.gd").new()
    var clip=load("res://clip_player.gd").new()
    for id in ids:
        verify(not adapter.decode(packet({"expression":id}),ids,supported).is_empty(),"static live "+id)
        verify(clip.load_data(clip_data({"expression":id}),ids,supported),"static clip "+id)
        verify(rig.apply_controls({"expression":id}),"static rig "+id)
        verify(adapter.decode(packet({"perform_expression":id}),ids,supported).is_empty()==(id!="EXP-005"),"live performance allowlist "+id)
        verify(clip.load_data(clip_data({"perform_expression":id}),ids,supported)==(id=="EXP-005"),"clip performance allowlist "+id)
    verify(not adapter.decode(packet({"perform_expression":"EXP-001"}),ids).is_empty(),"legacy live default")
    verify(clip.load_data(clip_data({"perform_expression":"EXP-001"}),ids),"legacy clip default")
    verify(adapter.decode(packet({"perform_expression":"EXP-005"}),ids,[]).is_empty(),"explicit empty live allowlist")
    verify(not clip.load_data(clip_data({"perform_expression":"EXP-005"}),ids,[]),"explicit empty clip allowlist")
    rig.apply_controls({"reset":true,"auto_blink":false})
    verify(rig.clip.load_data(clip_data({"perform_expression":"EXP-005"}),ids,supported),"valid clip loaded")
    rig.clip.play()
    rig.apply_controls({"perform_expression":"EXP-005","head_tilt":.4},"clip")
    rig.clip.paused=true
    var before=snapshot(rig)
    var old_cues=rig.clip.cues.duplicate(true)
    var path="user://release_invalid_performance_clip.json"
    var file=FileAccess.open(path,FileAccess.WRITE)
    file.store_string(JSON.stringify(clip_data({"perform_expression":"EXP-001","reset":true})));file.close()
    for i in range(3):
        verify(not rig.apply_controls({"perform_expression":"EXP-001","reset":true,"head_tilt":-.8}),"invalid direct rejected")
        verify(snapshot(rig)==before,"direct rejection preserves owners")
        verify(not rig.apply_controls({"perform_expression":"EXP-001","reset":true},"clip"),"mutated clip cue rejected")
        verify(snapshot(rig)==before,"mutated cue preserves owners")
        verify(not rig.play_clip(path),"invalid clip file rejected")
        verify(snapshot(rig)==before and rig.clip.cues==old_cues,"failed replacement preserves clip")
    DirAccess.remove_absolute(path)
    verify(adapter.start(19125)==OK,"UDP binds")
    var sender=PacketPeerUDP.new();sender.set_dest_address("127.0.0.1",19125)
    for i in range(3):
        sender.put_packet(packet({"perform_expression":"EXP-001","reset":true,"head_tilt":-.8},i+1))
        await create_timer(.03).timeout;adapter.poll(.01,rig)
        verify(snapshot(rig)==before,"invalid live packet preserves paused clip and performance")
        verify(adapter.last_sequence==-1 and not adapter.leased and adapter.accepted==0,"invalid packet cannot claim lease")
    verify(adapter.rejected==3,"all invalid packets rejected")
    sender.put_packet(packet({"perform_expression":"EXP-005"},4))
    await create_timer(.03).timeout;adapter.poll(.01,rig)
    verify(adapter.accepted==1 and adapter.leased and adapter.last_sequence==4,"approved live performance accepted")
    verify(not rig.clip.active and not rig.clip.paused and rig.clip_channels.is_empty(),"valid live command takes clip ownership")
    adapter.stop();sender.close()
    for code in [KEY_COMMA,KEY_PERIOD]:
        for static_id in ["neutral","EXP-001","EXP-005","EXP-093"]:
            rig.apply_controls({"reset":true,"expression":static_id})
            key(rig,code,true)
            verify(rig.expression_player.active,"shift cycle starts approved performance from "+static_id)
            verify(rig.expression_player.pending.get("id",rig.expression_player.id)=="EXP-005","shift cycle selects only approved ID")
            key(rig,code,true)
            verify(rig.expression_player.pending.get("id",rig.expression_player.id)=="EXP-005","repeated shift cycle stays approved")
    for static_id in ["neutral","EXP-001","EXP-005","EXP-093"]:
        rig.apply_controls({"reset":true,"expression":static_id})
        key(rig,KEY_ENTER)
        verify(rig.expression_player.active,"Enter starts supported performance")
        verify(rig.expression_player.pending.get("id",rig.expression_player.id)=="EXP-005","Enter falls back to approved performance")
        key(rig,KEY_ENTER)
        verify(rig.expression_player.pending.get("id",rig.expression_player.id)=="EXP-005","Enter replays current or pending performance")
    rig.apply_controls({"reset":true,"expression":ids[0]})
    for i in range(93):
        key(rig,KEY_PERIOD)
        verify(rig.face.expression==ids[(i+1)%93] and not rig.expression_player.active,"plain forward static cycle")
    for i in range(93):
        key(rig,KEY_COMMA)
        verify(rig.face.expression==ids[posmod(-i-1,93)],"plain reverse static cycle")
    rig.expression_player.profiles={}
    rig.clip.load_data(clip_data({"expression":"EXP-001"}),ids,[]);rig.clip.play()
    before=snapshot(rig)
    key(rig,KEY_COMMA,true);key(rig,KEY_PERIOD,true);key(rig,KEY_ENTER)
    verify(snapshot(rig)==before,"empty supported registry leaves ownership untouched")
    print("RELEASE_PERFORMANCE_CONTROLS_", "PASS" if failures==0 else "FAIL", " count=",checks," failures=",failures)
    quit(1 if failures else 0)

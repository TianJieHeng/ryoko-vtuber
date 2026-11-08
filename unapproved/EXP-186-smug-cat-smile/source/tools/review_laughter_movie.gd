extends SceneTree
## Review only: one existing shared rig/player, two complete cycles plus lifecycle.
## Writes all evidence outside source. No alternate expression controller.
var rig
var out=""
var title:Label
var subtitle:Label
var phase_label:Label
var frames:Array=[]
var events:Array=[]
var native_head:Transform2D
var native_body:Transform2D
var checks=0
var failures:Array=[]
func _initialize():call_deferred("run")
func label(text_value:String,at:Vector2,size:int)->Label:
    var n=Label.new();n.text=text_value;n.position=at;n.add_theme_font_size_override("font_size",size);root.add_child(n);return n
func frame_image():
    await process_frame
    await RenderingServer.frame_post_draw
    return root.get_texture().get_image()
func command(tick:int,data:Dictionary,name:String):
    var before=rig.get_state();var before_image=await frame_image()
    var ok=rig.apply_controls(data)
    var after=rig.get_state();var after_image=await frame_image()
    var continuous=data.has("perform_expression") or data.has("release_performance")
    if continuous:
        before_image.save_png(out+"/transactions/%03d_before.png"%tick)
        after_image.save_png(out+"/transactions/%03d_after.png"%tick)
        checks+=1
        if before_image.get_data()!=after_image.get_data():failures.append("transaction render changed "+str(tick))
    events.append({"tick":tick,"time":tick/30.0,"name":name,"command":data,"accepted":ok,"before":before,"after":after,"continuous_transaction":continuous})
func run():
    for arg in OS.get_cmdline_user_args():
        if arg.begins_with("--output="):out=arg.trim_prefix("--output=")
    if out.is_empty():push_error("External --output directory required");quit(2);return
    DirAccess.make_dir_recursive_absolute(out+"/frames");DirAccess.make_dir_recursive_absolute(out+"/transactions")
    root.size=Vector2i(1136,1454)
    rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
    rig.head.position=Vector2(0,70);rig.head.scale=Vector2.ONE;rig.body.position=Vector2(0,70);rig.body.scale=Vector2.ONE
    rig.hud.hide();rig.hint.hide();rig.pose_status.hide()
    title=label("EXP-005 / HEARTY LAUGHTER",Vector2(26,15),28)
    subtitle=label("Complete performance",Vector2(26,53),19)
    phase_label=label("Neutral",Vector2(26,81),17)
    native_head=rig.head.transform;native_body=rig.body.transform
    rig.reset();await process_frame
    for tick in range(720):
        if tick in [24,240]:await command(tick,{"perform_expression":"EXP-005"},"complete_cycle")
        if tick==420:await command(tick,{"reset":true},"begin_lifecycle_review")
        if tick==435:await command(tick,{"perform_expression":"EXP-005"},"laugh")
        if tick==474:await command(tick,{"release_performance":true},"release_mid_laugh")
        if tick==487:await command(tick,{"perform_expression":"EXP-005"},"retrigger_during_release")
        if tick==526:await command(tick,{"perform_expression":"EXP-005"},"retrigger_mid_laugh")
        if tick==570:await command(tick,{"perform_expression":"EXP-163"},"handover_to_yawn")
        if tick==603:await command(tick,{"perform_expression":"EXP-005"},"handover_back_to_laugh")
        if tick==644:await command(tick,{"mouth_open":.20,"mouth_smile":.70,"eye_smile_R":.80,"eye_smile_L":.80},"manual_takeover")
        if tick==657:await command(tick,{"release_performance":true},"release_manual_pose")
        if tick==690:await command(tick,{"reset":true},"reset_and_hold")
        if tick>0:rig.advance(1.0/30.0)
        if tick<420:subtitle.text="Complete performance / cycle "+("2 of 2" if tick>=240 else "1 of 2")
        else:subtitle.text="Interruption, retrigger and shared-expression handover"
        var s=rig.get_state();phase_label.text=(s.active_expression+" / " if s.active_expression!="" else "")+s.phase.replace("_"," ")
        var max_scale_error=0.0;var max_opacity_error=0.0
        for key in rig.face.objects:
            var node=rig.face.objects[key];var pivot=rig.face.homes[key].node
            max_scale_error=maxf(max_scale_error,maxf((node.scale-Vector2.ONE).length(),(pivot.scale-Vector2.ONE).length()))
            max_opacity_error=maxf(max_opacity_error,absf(node.modulate.a-1.0))
        checks+=3
        if max_scale_error!=0 or max_opacity_error!=0:failures.append("owner scale/opacity "+str(tick))
        if rig.head.transform!=native_head or rig.body.transform!=native_body:failures.append("head/body drift "+str(tick))
        var im=await frame_image();im.save_png(out+"/frames/frame_%04d.png"%tick)
        var h=HashingContext.new();h.start(HashingContext.HASH_SHA256);h.update(im.get_data())
        frames.append({"frame":tick,"time":tick/30.0,"sha256":h.finish().hex_encode(),"state":s,"physical_mouth_aperture":rig.face.mouth_opening*.55,"max_scale_error":max_scale_error,"max_opacity_error":max_opacity_error})
        if tick%120==0:print("LAUGHTER_MOVIE_FRAME ",tick)
    var f=FileAccess.open(out+"/render_evidence.json",FileAccess.WRITE)
    f.store_string(JSON.stringify({"fps":30,"frames":frames,"events":events,"checks":checks,"failures":failures,"normal_speed_playback_performed":false,"render":"Actual Godot4.6.3 OpenGL shared rig, deterministic30Hz capture"},"  "));f.close()
    print("LAUGHTER_MOVIE_", "PASS" if failures.is_empty() else "FAIL", " frames=",frames.size()," checks=",checks," failures=",failures)
    quit(0 if failures.is_empty() else 1)

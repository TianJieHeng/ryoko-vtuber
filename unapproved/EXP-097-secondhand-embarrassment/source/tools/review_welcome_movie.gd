extends SceneTree
## Generic review capture: commands and chapters come from a data-only plan.
## Uses the one shipping rig/player. No expression dispatch or alternate controller.
## Writes all evidence outside source. No alternate expression controller.
var rig
var out=""
var plan_path=""
var plan:Dictionary={}
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
    checks+=1
    if not ok:push_error(rig.last_error);quit(2);return
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
        if arg.begins_with("--review-plan="):plan_path=arg.trim_prefix("--review-plan=")
    if out.is_empty() or plan_path.is_empty():push_error("External --output and --review-plan required");quit(2);return
    plan=JSON.parse_string(FileAccess.get_file_as_string(plan_path))
    if plan.get("fps")!=30 or not plan.get("commands") is Array:push_error("Invalid review plan");quit(2);return
    DirAccess.make_dir_recursive_absolute(out+"/frames");DirAccess.make_dir_recursive_absolute(out+"/transactions")
    root.size=Vector2i(1136,1454)
    rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
    if not rig.rig_ready or not rig.registry_ready:push_error("Rig not ready");quit(2);return
    rig.head.position=Vector2(0,70);rig.head.scale=Vector2.ONE;rig.body.position=Vector2(0,70);rig.body.scale=Vector2.ONE
    rig.hud.hide();rig.hint.hide();rig.pose_status.hide()
    title=label(plan.title,Vector2(26,15),28)
    subtitle=label("Complete performance",Vector2(26,53),19)
    phase_label=label("Neutral",Vector2(26,81),17)
    native_head=rig.head.transform;native_body=rig.body.transform
    rig.reset();await process_frame
    for tick in range(int(plan.total_frames)):
        for event in plan.commands:
            if tick==int(event.tick):await command(tick,event.command,event.name)
        if tick>0:rig.advance(1.0/30.0)
        for chapter in plan.chapters:
            if tick>=int(chapter.start):subtitle.text=chapter.text
        var s=rig.get_state()
        if tick>=24 and tick<113 or tick>=162 and tick<251:
            checks+=2
            var start=24 if tick<162 else 162
            if s.active_expression!="EXP-001" or abs(s.time-(tick-start+1)/30.0)>.00001:failures.append("actual EXP-001 identity/time "+str(tick))
            if s.controls.blink_R>.04 or s.controls.eye_smile_R!=0:failures.append("greeting eye state "+str(tick))
        if tick>=54 and tick<=79 or tick>=192 and tick<=217:
            checks+=1
            if abs(rig.face.mouth_opening-.80)>.00001 or rig.face.smile_mouth!=1:failures.append("actual greeting plateau "+str(tick))
        phase_label.text=(s.active_expression+" / " if s.active_expression!="" else "")+s.phase.replace("_"," ")
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
        if tick%120==0:print("PROFILE_MOVIE_FRAME ",tick)
    var f=FileAccess.open(out+"/render_evidence.json",FileAccess.WRITE)
    f.store_string(JSON.stringify({"plan":plan,"fps":30,"frames":frames,"events":events,"checks":checks,"failures":failures,"normal_speed_playback_performed":false,"render":"Actual Godot 4.6.3 OpenGL shared rig, deterministic 30 Hz capture"},"  "));f.close()
    print("PROFILE_MOVIE_", "PASS" if failures.is_empty() else "FAIL", " frames=",frames.size()," checks=",checks," failures=",failures)
    quit(0 if failures.is_empty() else 1)

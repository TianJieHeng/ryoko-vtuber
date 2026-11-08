extends SceneTree
## Finished actual-Godot review sequence. The primary uses only the public API.
## Closeups are mirrored render instances with fixed presentation transforms.
## Only the primary owns playback; they display its exact shared pose.
var primary
var views=[]
var out=""
var status:Label
var records=[]
func _initialize():call_deferred("run")
func require(ok:bool,message:String):
    if not ok:push_error(message);quit(2);assert(false,message)
func label_at(text:String,pos:Vector2,size:int)->Label:
    var label=Label.new();label.text=text;label.position=pos;label.z_index=101;label.add_theme_font_size_override("font_size",size);root.add_child(label);return label
func add_panel(size:Vector2i,pos:Vector2,origin:Vector2,zoom:float):
    var viewport=SubViewport.new();viewport.size=size;viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS;viewport.world_2d=World2D.new();root.add_child(viewport)
    var rig=load("res://expression_rig.tscn").instantiate();viewport.add_child(rig)
    rig.set_process(false);rig.set_process_unhandled_key_input(false);rig.hud.hide();rig.hint.hide();rig.pose_status.hide()
    rig.head.position=origin;rig.head.scale=Vector2.ONE*zoom;rig.body.position=origin;rig.body.scale=Vector2.ONE*zoom;views.append(rig)
    var screen=TextureRect.new();screen.position=pos;screen.size=Vector2(size);screen.texture=viewport.get_texture();root.add_child(screen)
func command(data:Dictionary):require(primary.apply_controls(data),"Movie command rejected: "+JSON.stringify(data)+" / "+primary.last_error)
func manual(gaze:Vector2,lids:Vector2=Vector2.ZERO,hair:float=0.0):
    command({"gaze_x":gaze.x,"gaze_y":gaze.y,"blink_R":lids.x,"blink_L":lids.y,"hair_sway":hair})
func sync_views():
    var pose=primary.displayed_pose()
    for rig in views:rig._apply_performance_pose(pose)
func run():
    for arg in OS.get_cmdline_user_args():
        if arg.begins_with("--output="):out=arg.trim_prefix("--output=")
    require(not out.is_empty(),"Provide an external output directory")
    DirAccess.make_dir_recursive_absolute(out+"/frames");root.size=Vector2i(1136,800)
    primary=load("res://expression_rig.tscn").instantiate();root.add_child(primary);primary.set_process(false);primary.set_process_unhandled_key_input(false)
    primary.hud.hide();primary.hint.hide();primary.pose_status.hide();primary.position=Vector2(0,18)
    label_at("Ryoko / separate eyes and bounded gaze",Vector2(22,15),24)
    label_at("One shared controller. Rigid iris motion, fixed eye opening.",Vector2(22,47),15)
    label_at("Eye close-up / fixed 1.6x source view",Vector2(590,98),19)
    add_panel(Vector2i(536,200),Vector2(585,132),Vector2(-644,-730),1.6)
    label_at("Mouth close-up / approved 0.55 physical cap",Vector2(590,380),19)
    add_panel(Vector2i(536,260),Vector2(585,416),Vector2(-750,-1040),1.8)
    label_at("Gaze: left/right 4 px, up 2 px, down 1 px",Vector2(590,702),15)
    label_at("Foreground hair, brows, eyes and mouth stay separate.",Vector2(590,726),14)
    var footer=ColorRect.new();footer.position=Vector2(0,760);footer.size=Vector2(1136,40);footer.color=Color(.12,.13,.14);footer.z_index=100;root.add_child(footer)
    status=label_at("Neutral",Vector2(22,769),17)
    await process_frame;command({"reset":true})
    for tick in range(1020):
        var t=tick/30.0
        if t<1:
            status.text="Neutral / original registration"
        elif t<5:
            var u=(t-1)/4.0
            manual(Vector2(sin(u*TAU),0));status.text="Horizontal sweep / rigid iris objects"
        elif t<9:
            var u=(t-5)/4.0
            manual(Vector2(0,-sin(u*TAU)));status.text="Vertical sweep / stationary upper and lower aperture"
        elif t<14:
            var u=(t-9)/5.0;var phase=u*TAU*2
            var lid=(1-cos(u*TAU*2))*.5
            manual(Vector2(sin(phase),cos(phase)),Vector2.ONE*lid,sin(phase)*.07)
            status.text="Synthetic coverage / gaze, full blink and bounded hair motion"
        elif t<18:
            var u=(t-14)/4.0;var phase=u*TAU*2
            var lids=Vector2(maxf(0,sin(phase)),maxf(0,-sin(phase)))
            manual(Vector2(cos(phase),sin(phase)),lids);status.text="Independent left and right eyelids"
        elif t<20:
            var u=(t-18)/2.0
            manual(Vector2(sin(u*TAU*2),sin(u*TAU)),Vector2.ONE*((1-cos(u*TAU))*.25));status.text="Fractional sweep and reversal"
        elif tick==600:
            command({"reset":true});status.text="Neutral return before approved yawn"
        elif tick==615:
            command({"perform_expression":"EXP-163"});require(primary.active_performance=="EXP-163","Yawn trigger inactive")
        elif tick>615 and tick<=789:
            require(primary.advance(1.0/30.0),"Yawn advance rejected")
            if tick<789:require(primary.active_performance=="EXP-163","Yawn ownership lost")
            if tick==675:require(primary.pose_now().mouth_open>.5,"Yawn never opened mouth")
            if tick==789:
                require(primary.advance(.000001),"Yawn final rounding step rejected")
                require(primary.active_performance=="" and primary.pose_now()==primary.neutral_pose(),"Yawn did not finish neutral")
            status.text="EXP-163 / approved yawn / "+primary.performance_phase.replace("_"," ")
        elif tick==810:
            command({"perform_expression":"EXP-163"});status.text="Interrupt and manual takeover"
        elif tick>810 and tick<840:
            require(primary.advance(1.0/30.0),"Interrupted yawn advance rejected")
        elif tick==840:
            manual(Vector2(-1,1),Vector2(.4,.75));require(primary.active_performance=="","Manual takeover failed")
        elif tick==864:
            command({"release_performance":true});require(primary.release_time==0,"Release failed");status.text="Release / continuous return to neutral"
        elif tick>864 and tick<=885:
            require(primary.advance(1.0/30.0),"Release advance rejected")
        elif tick==900:
            command({"blink":1.0,"gaze_x":1.0,"gaze_y":-1.0});status.text="Reset from closed lids and nonzero gaze"
        elif tick==924:
            command({"reset":true});require(primary.pose_now()==primary.neutral_pose(),"Reset did not restore neutral");status.text="Neutral / exact return to this candidate's starting pose"
        sync_views()
        await process_frame;await RenderingServer.frame_post_draw
        require(root.get_texture().get_image().save_png(out+"/frames/frame_%06d.png"%tick)==OK,"Frame save failed")
        records.append({"frame":tick,"time":t,"label":status.text,"state":primary.get_state()})
    var file=FileAccess.open(out+"/controls.json",FileAccess.WRITE);file.store_string(JSON.stringify(records));file.close()
    print("GAZE_MOVIE_CAPTURE_PASS frames=1020 fps=30 approved_yawn_trigger_verified=true");quit()

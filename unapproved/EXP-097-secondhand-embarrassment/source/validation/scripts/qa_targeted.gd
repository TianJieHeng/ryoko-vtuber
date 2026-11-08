extends SceneTree
var rig
var out=""
var records=[]
func _initialize():call_deferred("run")
func capture(name:String):
    await process_frame
    await RenderingServer.frame_post_draw
    root.get_texture().get_image().save_png(out+"/"+name+".png")
func run():
    for arg in OS.get_cmdline_user_args():
        if arg.begins_with("--capture-dir="):out=arg.trim_prefix("--capture-dir=")
    DirAccess.make_dir_recursive_absolute(out)
    root.size=Vector2i(160,140);root.content_scale_size=Vector2i(160,140)
    rig=load("res://object_rig.tscn").instantiate();root.add_child(rig);await process_frame;rig.set_process(false)
    rig.body.hide();rig.hud.hide();rig.hint.hide();rig.pose_status.hide()
    rig.head.position=Vector2(-485,-590);rig.head.scale=Vector2.ONE
    for key in rig.face.objects:rig.face.objects[key].hide()
    var backing=Sprite2D.new();backing.texture=load("res://artwork/bust_base.png");backing.centered=false;backing.z_index=-100;rig.head.add_child(backing)
    var values=[0.0,.000001,.00001,.0001,.0005,.001,.002,.005,.01,.025,.05,.075,.1,.125,.15,.2,.25,.35,.5,.75,1.0]
    for view in ["source","native","oral"]:
        if view=="native":
            root.size=Vector2i(80,75);root.content_scale_size=Vector2i(80,75)
            rig.head.position=Vector2(-240,-290);rig.head.scale=Vector2(.49,.49)
        elif view=="oral":
            root.size=Vector2i(320,280);root.content_scale_size=Vector2i(320,280)
            rig.head.position=Vector2(-970,-1180);rig.head.scale=Vector2(2,2)
        for direction in ["forward","reverse"]:
            var sequence=range(values.size())
            if direction=="reverse":sequence.reverse()
            for i in sequence:
                rig.face.set_mouth_open(values[i])
                await capture("%s_%s_%02d"%[view,direction,i])
                records.append({"view":view,"direction":direction,"index":i,"opening":values[i]})
    var f=FileAccess.open(out+"/metadata.json",FileAccess.WRITE);f.store_string(JSON.stringify(records,"  "));f.close()
    print("TARGETED_TEETH_CAPTURE_COMPLETE ",records.size()," captures");quit()

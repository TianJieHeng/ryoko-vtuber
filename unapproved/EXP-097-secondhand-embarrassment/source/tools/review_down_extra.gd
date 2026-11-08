extends SceneTree
## Synthetic capability evidence, never an EXP-152 performance.
const Limits=preload("res://control_limits.gd")
var rig
var out=""
var mode="old"
var native=false
var records=[]
var checks=0
var fixed_head
var fixed_body
func _initialize():call_deferred("run")
func require(ok:bool,message:String):
    checks+=1
    if not ok:push_error("DOWN_EXTRA_CAPTURE_FAILED "+message);quit(2);assert(false,message)
func command(data):require(rig.apply_controls(data),"rejected "+JSON.stringify(data)+" / "+rig.last_error)
func hash_bytes(data):
    var h=HashingContext.new();h.start(HashingContext.HASH_SHA256);h.update(data);return h.finish().hex_encode()
func record(label,expected,save_png=false,hide_irises=false,scope="manual"):
    var actual=rig.pose_now()
    require(actual.size()==expected.size(),"complete expected channels "+label)
    for key in expected:require(abs(float(actual[key])-float(expected[key]))<.0000003,"actual channel "+key+" / "+label)
    require(rig.head.transform==fixed_head and rig.body.transform==fixed_body,"fixed head/body")
    var extra=float(actual.get("gaze_down_extra",0))
    var physical=Limits.gaze_pixels(Vector2(actual.gaze_x,actual.gaze_y))+Vector2(0,extra*5.0)
    for side in ["screen_left","screen_right"]:
        var key="iris_"+side;var sclera="sclera_"+side
        require(rig.face.homes[key].node.position.is_equal_approx(rig.face.homes[key].pivot+physical),"actual rigid iris sum")
        require(rig.face.objects[key].material.get_shader_parameter("rigid_gaze").is_equal_approx(physical),"actual shader sum")
        require(rig.face.homes[sclera].node.position==rig.face.homes[sclera].pivot,"fixed sclera")
        if hide_irises:rig.face.objects[key].hide()
        var present=rig.face.objects[sclera].material.get_shader_parameter("iris_present")
        # Godot returns null for an unset parameter; declared shader default is true.
        if present==null:present=true
        require(present==(not hide_irises),"backing visibility updates only iris owner")
    for key in rig.face.objects:
        var sprite=rig.face.objects[key];var pivot=rig.face.homes[key].node
        require(sprite.scale==Vector2.ONE and pivot.scale==Vector2.ONE,"unit local scale")
        require(sprite.modulate.a==1 and pivot.modulate.a==1,"fixed anatomical opacity")
    require(rig.face.oral_objects.upper_teeth.position==Vector2(533,626),"fixed white upper teeth")
    var state=rig.get_state();var face=rig.face.snapshot()
    var oldstate=state.duplicate(true);oldstate.controls.erase("gaze_down_extra");oldstate.displayed_controls.erase("gaze_down_extra")
    var oldface=face.duplicate(true);oldface.erase("gaze_down_extra")
    await process_frame;await RenderingServer.frame_post_draw
    var im=root.get_texture().get_image();require(im.get_size()==root.size,"viewport pixel size")
    if save_png:require(im.save_png(out+"/"+label+".png")==OK,"save capture")
    records.append({"label":label,"scope":scope,"physical_gaze":[physical.x,physical.y],"state":state,"face_old_fields_sha256":hash_bytes(JSON.stringify(oldface).to_utf8_buffer()),"state_old_fields":oldstate,"pixels_sha256":hash_bytes(im.get_data()),"saved_png":save_png,"hidden_irises":hide_irises,"scale":rig.head.scale.x,"origin":[rig.head.position.x,rig.head.position.y]})
    for side in ["screen_left","screen_right"]:rig.face.objects["iris_"+side].show()
func manual(label,controls,save_png=false,hide_irises=false):
    command({"reset":true});command(controls)
    var p=rig.neutral_pose();for k in controls:p[k]=controls[k]
    require(rig.active_performance=="" and rig.release_time<0,"manual scope")
    await record(label,p,save_png,hide_irises)
func old_domain():
    var index=0
    var lids=[Vector2.ZERO,Vector2(.12,.12),Vector2(.4,.4),Vector2(.8,.8),Vector2.ONE,Vector2(.2,.8),Vector2(.8,.2)]
    for lid in lids:
        for x in [-1.,0.,1.]:
            for y in [-1.,0.,1.]:
                await manual("old_%03d"%index,{"gaze_x":x,"gaze_y":y,"blink_R":lid.x,"blink_L":lid.y},index<9)
                index+=1
    for smile in [0.0,.3,.65,.9,1.0]:
        for x in [-1.,0.,1.]:
            for y in [-1.,0.,1.]:
                await manual("old_%03d"%index,{"gaze_x":x,"gaze_y":y,"eye_smile_R":smile,"eye_smile_L":smile},false)
                index+=1
    for hair in [-.07,.07]:
        for x in [-1.,1.]:
            for y in [-1.,1.]:
                for lid in [0.,.7,1.]:
                    await manual("old_%03d"%index,{"gaze_x":x,"gaze_y":y,"blink_R":lid,"blink_L":lid,"hair_sway":hair},false)
                    index+=1
    for entry in rig.list_expressions():
        var definition=rig.registry.definition(entry.id);var times=[]
        for i in range(definition.keyframes.size()):
            times.append(float(definition.keyframes[i].time))
            if i<definition.keyframes.size()-1:times.append((float(definition.keyframes[i].time)+float(definition.keyframes[i+1].time))*.5)
        for i in range(times.size()):
            command({"reset":true});require(rig.play_expression(entry.id),"actual old profile trigger")
            require(rig.active_performance==entry.id,"actual profile ownership before advance");require(rig.advance(times[i]),"actual timeline advance")
            var p=rig.sample_expression(entry.id,times[i])
            if times[i]<rig.RESTART_SECONDS:
                var blend=smoothstep(0.,rig.RESTART_SECONDS,times[i])
                for k in p:p[k]=float(p[k])*blend
            await record(entry.id+"_%02d"%i,p,i==int(times.size()/2),false,"actual "+entry.id)
    await manual("old_neutral_return",{},true)
func new_domain():
    var index=0
    for lid in [Vector2.ZERO,Vector2(.12,.12),Vector2(.4,.4),Vector2(.7,.7),Vector2.ONE,Vector2(.2,.8),Vector2(.8,.2)]:
        for x in [-1.,0.,1.]:
            for down in [1.,2.5,4.,5.5,6.]:
                await manual("new_%03d"%index,{"gaze_x":x,"gaze_y":1.,"gaze_down_extra":(down-1.)/5.,"blink_R":lid.x,"blink_L":lid.y},down==6. or (lid==Vector2(.12,.12) and x==0))
                index+=1
    for smile in [.3,.65,.9,1.]:
        for x in [-1.,0.,1.]:
            await manual("new_%03d"%index,{"gaze_x":x,"gaze_y":1.,"gaze_down_extra":1.,"eye_smile_R":smile,"eye_smile_L":smile},true);index+=1
    for hair in [-.07,.07]:
        for x in [-1.,0.,1.]:
            await manual("new_%03d"%index,{"gaze_x":x,"gaze_y":1.,"gaze_down_extra":1.,"hair_sway":hair},true);index+=1
    for x in [-1.,0.,1.]:
        for y in [-1.,0.,1.]:
            await manual("mixed_%d_%d"%[roundi(x),roundi(y)],{"gaze_x":x,"gaze_y":y,"gaze_down_extra":1.},true)
    for down in [0.,1.,3.5,6.]:
        for x in [-1.,0.,1.]:
            await manual("hidden_%s_%d"%[str(down),roundi(x)],{"gaze_x":x,"gaze_y":minf(down,1.),"gaze_down_extra":maxf(down-1.,0)/5.},true,true)
    # Exact reversal pairs with fractional combined x/y, independent of frame history.
    for i in range(25):
        var t=float(i)/24.;var x=sin(t*TAU);var y=-1.+2.*t
        await manual("reverse_forward_%02d"%i,{"gaze_x":x,"gaze_y":y,"gaze_down_extra":t,"blink_R":.12,"blink_L":.22},i in [0,6,12,18,24])
    for i in range(24,-1,-1):
        var t=float(i)/24.;var x=sin(t*TAU);var y=-1.+2.*t
        await manual("reverse_backward_%02d"%i,{"gaze_x":x,"gaze_y":y,"gaze_down_extra":t,"blink_R":.12,"blink_L":.22})
    await manual("new_neutral_return",{},true)
func movie():
    # Manual geometry trajectory, not private-pride acting or a registry entry.
    for i in range(360):
        var t=float(i)/30.;var down=0.;var x=0.;var lid=.12;var smile=0.
        if t>=1 and t<2:down=6*smoothstep(1.,2.,t)
        elif t>=2 and t<3:down=6.
        elif t>=3 and t<5:down=6.;x=sin((t-3)*PI)
        elif t>=5 and t<6:down=6.;lid=.12+.88*sin((t-5)*PI)
        elif t>=6 and t<7:down=6.;smile=sin((t-6)*PI)
        elif t>=7 and t<8:down=6*(1-smoothstep(7.,8.,t))
        elif t>=9 and t<10:down=6*smoothstep(9.,10.,t)
        elif t>=10 and t<11:down=6*(1-smoothstep(10.,11.,t))
        await manual("frame_%04d"%i,{"gaze_x":x,"gaze_y":minf(down,1.),"gaze_down_extra":maxf(down-1.,0)/5.,"blink_R":lid,"blink_L":lid,"eye_smile_R":smile,"eye_smile_L":smile},true)
func run():
    for arg in OS.get_cmdline_user_args():
        if arg.begins_with("--output="):out=arg.trim_prefix("--output=")
        if arg.begins_with("--mode="):mode=arg.trim_prefix("--mode=")
        if arg=="--native":native=true
    require(not out.is_empty(),"output dir");DirAccess.make_dir_recursive_absolute(out)
    root.size=Vector2i(1136,1384) if native else Vector2i(1136,800)
    rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
    require(rig.rig_ready and rig.registry_ready,"ready");require(rig.list_expressions().size()==6,"only six approved profiles")
    for id in ["EXP-002","EXP-003","EXP-152"]:require(rig.registry.definition(id).is_empty(),"no unapproved profile")
    rig.hud.hide();rig.hint.hide();rig.pose_status.hide()
    if native:rig.head.position=Vector2.ZERO;rig.body.position=Vector2.ZERO;rig.head.scale=Vector2.ONE;rig.body.scale=Vector2.ONE
    command({"reset":true});fixed_head=rig.head.transform;fixed_body=rig.body.transform
    if mode=="old":await old_domain()
    elif mode=="new":await new_domain()
    elif mode=="movie":await movie()
    else:require(false,"unknown capture mode")
    var f=FileAccess.open(out+"/records.json",FileAccess.WRITE);f.store_string(JSON.stringify(records,"  "));f.close()
    f=FileAccess.open(out+"/summary.json",FileAccess.WRITE);f.store_string(JSON.stringify({"status":"capture_assertions_pass","frames":records.size(),"checks":checks,"mode":mode,"native":native},"  "));f.close()
    print("DOWN_EXTRA_CAPTURE_PASS frames=",records.size()," checks=",checks," mode=",mode," native=",native);quit()

extends SceneTree
## Run enabled coverage in an isolated project; this suite never flips the source gate.
const Limits=preload("res://control_limits.gd")
var rig
var checks=0
var failures=0
var fixed_uniforms={}
var head_transform:Transform2D
var body_transform:Transform2D
func check(ok:bool,label:String):
    checks+=1
    if not ok:failures+=1;push_error("GAZE_RUNTIME "+label)
func _initialize():call_deferred("run")
func snapshot()->Dictionary:
    var s=rig.get_state();s.erase("last_error")
    s.face=rig.face.snapshot();s.current=rig.current_pose.duplicate(true)
    s.restart=rig.restart_pose.duplicate(true);s.release=rig.release_pose.duplicate(true)
    s.performance=rig.performance.duplicate(true);s.elapsed=rig.elapsed
    return s
func inspect_pose(expected:Vector2):
    var pixels=Limits.gaze_pixels(expected)
    check(rig.manual_gaze.is_equal_approx(expected) and rig.face.gaze.is_equal_approx(expected),"normalized control reaches face")
    check(rig.head.transform==head_transform and rig.body.transform==body_transform,"head and body stay fixed")
    var backing=rig.face.homes.stationary_backing
    check(backing.node.position==backing.pivot and backing.node.rotation==0,"face backing stays fixed")
    for key in rig.face.objects:
        var sprite=rig.face.objects[key];var pivot=rig.face.homes[key].node
        check(sprite.scale==Vector2.ONE and pivot.scale==Vector2.ONE,"unit object scales "+key)
        check(sprite.modulate.a==1.0 and pivot.modulate.a==1.0,"no object opacity fade "+key)
    for side in ["screen_left","screen_right"]:
        var iris="iris_"+side;var sclera="sclera_"+side
        check(rig.face.homes[iris].node.position.is_equal_approx(rig.face.homes[iris].pivot+pixels),"iris rigid calibrated offset "+side)
        check(rig.face.homes[sclera].node.position==rig.face.homes[sclera].pivot,"sclera pivot fixed "+side)
        var closure=rig.face.closure.x if side=="screen_left" else rig.face.closure.y
        for key in [iris,sclera]:
            var material=rig.face.objects[key].material
            check(material.get_shader_parameter("rigid_gaze").is_equal_approx(pixels),"shader physical offset "+key)
            check(is_equal_approx(material.get_shader_parameter("closure"),closure),"unilateral closure reaches shader "+key)
            for uniform in fixed_uniforms[key]:
                check(material.get_shader_parameter(uniform)==fixed_uniforms[key][uniform],"fixed aperture coordinate uniform "+key+"/"+uniform)
func exercise(gaze:Vector2,lids:Vector2,hair:float):
    # Compare identical non-gaze controls: only iris pivots may translate with gaze.
    var controls={"gaze_x":0.0,"gaze_y":0.0,"blink_R":lids.x,"blink_L":lids.y,"hair_sway":hair}
    check(rig.apply_controls(controls),"accept centered comparison")
    var baseline=rig.face.snapshot().objects
    controls.gaze_x=gaze.x;controls.gaze_y=gaze.y
    check(rig.apply_controls(controls),"accept gaze with lids and hair")
    var moved=rig.face.snapshot().objects
    for key in baseline:
        if key not in ["iris_screen_left","iris_screen_right"]:
            check(moved[key]==baseline[key],"gaze leaves non-iris object unchanged "+key)
        else:
            var before=baseline[key].duplicate(true);var after=moved[key].duplicate(true)
            before.erase("position");after.erase("position")
            check(before==after,"iris only translates "+key)
    inspect_pose(gaze)
func run():
    rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
    head_transform=rig.head.transform;body_transform=rig.body.transform
    if not Limits.GAZE_ENABLED:
        var before=snapshot()
        check(not rig.apply_controls({"gaze_x":.01,"mouth_open":.4}),"disabled gate rejects gaze")
        check(snapshot()==before,"disabled rejection atomic")
        print("GAZE_RUNTIME_DISABLED_PASS checks=",checks," failures=",failures," enabled physical suite requires isolated enabled copy")
        quit(0 if failures==0 else 1);return
    check(Limits.GAZE_LEFT_PIXELS==4 and Limits.GAZE_RIGHT_PIXELS==4 and Limits.GAZE_UP_PIXELS==2 and Limits.GAZE_DOWN_PIXELS==1,"reviewed directional calibration")
    for side in ["screen_left","screen_right"]:
        for prefix in ["iris_","sclera_"]:
            var key=prefix+side;fixed_uniforms[key]={}
            for uniform in ["eye_size","iris_size","iris_padding","sprite_origin","profile_texture","lower_profile_texture","aperture_texture"]:
                fixed_uniforms[key][uniform]=rig.face.objects[key].material.get_shader_parameter(uniform)
    for x in [-1.0,0.0,1.0]:
        for y in [-1.0,0.0,1.0]:
            for left in [0.0,1.0]:
                for right in [0.0,1.0]:
                    for hair in [-.07,0.0,.07]:exercise(Vector2(x,y),Vector2(left,right),hair)
    # 1,001 fractional samples each way, with identical states on the return path.
    var forward=[]
    for direction in [1,-1]:
        for step in range(1001):
            var i=step if direction==1 else 1000-step
            var u=i/1000.0
            exercise(Vector2(2*u-1,sin(u*TAU)),Vector2(u,1-u),.07*sin(u*TAU))
            if direction==1:forward.append(snapshot())
            else:check(snapshot()==forward[i],"forward/reverse deterministic sample")
    # Accepted trigger is a separate transaction, never reset+trigger.
    rig.reset();check(rig.play_expression("EXP-163"),"accepted authored yawn trigger")
    rig.advance(1.7)
    check(rig.active_performance=="EXP-163" and is_equal_approx(rig.performance_time,1.7),"real yawn active at requested time")
    check(rig.apply_controls({"gaze_x":.75,"gaze_y":-.5,"blink_R":.2,"blink_L":.8}),"manual gaze takes over active yawn")
    check(rig.active_performance=="" and rig.face.owners.eyes=="manual","manual ownership replaces performance")
    inspect_pose(Vector2(.75,-.5))
    var shown=rig.displayed_pose()
    check(rig.play_expression("EXP-163"),"accepted retrigger from manual gaze")
    check(rig.displayed_pose()==shown,"retrigger no pose jump")
    rig.advance(.05);shown=rig.displayed_pose()
    check(rig.release(),"accepted release")
    check(rig.displayed_pose()==shown and rig.face.owners.eyes=="release","release no pose jump")
    rig.advance(.45);check(rig.pose_now()==rig.neutral_pose(),"release reaches exact neutral")
    for mode in ["neutral","manual","performance","release"]:
        rig.reset()
        if mode=="manual":rig.apply_controls({"gaze_x":.5,"gaze_y":.5})
        if mode in ["performance","release"]:
            check(rig.play_expression("EXP-163"),"accepted atomicity setup yawn")
            rig.advance(1.7)
        if mode=="release":rig.release();rig.advance(.1)
        var saved=snapshot()
        for bad in [1.000001,-1.000001,NAN,INF,true,".5"]:
            check(not rig.apply_controls({"reset":true,"gaze_y":bad,"mouth_open":.3}),"reject mixed invalid gaze")
            check(snapshot()==saved,"mixed rejection preserves pose clock ownership "+mode)
        check(rig.reset(),"reset succeeds")
        check(rig.pose_now()==rig.neutral_pose(),"reset exact neutral")
        inspect_pose(Vector2.ZERO)
    print("GAZE_RUNTIME_", "PASS" if failures==0 else "FAIL", " checks=",checks," failures=",failures," fractional_samples=2002 endpoint_states=108")
    quit(0 if failures==0 else 1)

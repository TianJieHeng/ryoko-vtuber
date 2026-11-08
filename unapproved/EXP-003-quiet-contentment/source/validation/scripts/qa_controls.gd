extends SceneTree
var checks=0
var failures=[]
var peak=0.0
func check(ok:bool,why:String):
    checks+=1
    if not ok and why not in failures:failures.append(why)
func inspect(rig,label:String):
    var opening=float(rig.face.oral_objects.upper_teeth.material.get_shader_parameter("opening"))
    peak=maxf(peak,opening)
    check(is_finite(opening) and opening>=0 and opening<=.550001,label+": effective opening outside reference cap")
    check(rig.face.oral_objects.upper_teeth.position==Vector2(533,626),label+": upper tooth attachment changed")
    check(rig.face.oral_objects.upper_lip.position==Vector2(525,620),label+": upper lip translated")
    check(rig.face.oral_objects.lower_lip.position.y<=649.7001,label+": lower lip exceeds cap")
    check(rig.face.oral_objects.lower_lip.position.x==525,label+": lower lip x changed")
    for key in rig.face.oral_objects:
        var n=rig.face.oral_objects[key]
        check(n.scale==Vector2.ONE,label+": oral object scale "+key)
        check(n.rotation==0,label+": oral object rotation "+key)
        check(n.modulate.a==1,label+": oral object opacity "+key)
        check(abs(float(n.material.get_shader_parameter("opening"))-opening)<.000001,label+": shader cap not synchronized "+key)
func _initialize():call_deferred("run")
func run():
    var rig=load("res://yawn_rig.tscn").instantiate();root.add_child(rig)
    await process_frame;rig.set_process(false)
    for i in range(1001):
        check(rig.apply_controls({"mouth_open":i/1000.0}),"manual accepted")
        inspect(rig,"manual")
    check(abs(float(rig.face.oral_objects.upper_teeth.material.get_shader_parameter("opening"))-.55)<.000001,"manual1 maps to cap")
    for viseme in ["A","E","I","O","U"]:
        var before=rig.pose_now().duplicate()
        check(not rig.apply_controls({"mouth":viseme}),"legacy mouth bypass blocked")
        check(rig.pose_now()==before,"failed mouth transaction preserves pose")
        check(not rig.apply_controls({"viseme":viseme}),"legacy viseme bypass blocked")
        check(rig.pose_now()==before,"failed viseme transaction preserves pose")
    for invalid in [-1,.0-0.000001,1.000001,2,INF,NAN,"1"]:
        var before=rig.pose_now().duplicate()
        check(not rig.apply_controls({"mouth_open":invalid}),"invalid manual rejected")
        check(rig.pose_now()==before,"invalid manual preserves pose")
    for alias in ["REST","RELEASE","NEUTRAL"]:
        check(rig.apply_controls({"mouth":alias}),"neutral aliases accepted")
        check(rig.face.mouth_opening==0,"neutral alias closes mouth")
    for direct in [-5,0,.000000001,.5,1,5]:
        rig.face.set_mouth_open(direct);inspect(rig,"direct numeric")
    rig.apply_controls({"reset":true})
    check(rig.apply_controls({"perform_expression":"EXP-163"}),"performance trigger accepted")
    for i in range(3600):
        rig._process(1.0/600.0);inspect(rig,"performance")
    check(rig.face.mouth_opening==0,"performance exact neutral")
    for release_frame in [1,30,55,75,100,135,170]:
        rig.apply_controls({"reset":true});rig.apply_controls({"perform_expression":"EXP-163"})
        for i in range(release_frame):rig._process(1.0/30.0)
        var pre=rig.pose_now().duplicate();rig.apply_controls({"release_performance":true})
        check(rig.pose_now()==pre,"release command continuity")
        for i in range(60):rig._process(1.0/120.0);inspect(rig,"release")
        check(rig.face.mouth_opening==0,"release exact neutral")
    for retrigger_frame in [1,30,55,75,100,135,170]:
        rig.apply_controls({"reset":true});rig.apply_controls({"perform_expression":"EXP-163"})
        for i in range(retrigger_frame):rig._process(1.0/30.0)
        var pre=rig.pose_now().duplicate();rig.apply_controls({"perform_expression":"EXP-163"})
        check(rig.pose_now()==pre,"retrigger command continuity")
        for i in range(720):rig._process(1.0/120.0);inspect(rig,"retrigger")
        check(rig.face.mouth_opening==0,"retrigger exact neutral")
    print("INDEPENDENT_CAP_CONTROLS ",JSON.stringify({"checks":checks,"failures":failures,"effective_peak":peak}))
    quit(0 if failures.is_empty() else 1)

extends SceneTree
## EXP-006 data and lifecycle checks on the existing shared player.
var rig
var checks=0
var fails=[]
func _initialize():call_deferred("run")
func check(ok:bool,label:String):
    checks+=1
    if not ok:fails.append(label);push_error(label)
func neutral(label:String):
    check(rig.pose_now()==rig.neutral_pose(),label+" neutral controls")
    check(rig.active_performance=="" and rig.release_time<0,label+" no active owner")
func fixed_owners(label:String,head:Transform2D,body:Transform2D):
    check(rig.head.transform==head and rig.body.transform==body,label+" fixed head and body")
    for k in rig.face.objects:
        var n=rig.face.objects[k];var pivot=rig.face.homes[k].node
        check(n.scale==Vector2.ONE and pivot.scale==Vector2.ONE and n.modulate.a==1.0,label+" rigid opaque "+k)
func run():
    rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
    check(rig.registry_ready,"registry ready")
    check(rig.registry.resolve("giggle")=="EXP-006" and rig.registry.resolve("suppressed-giggle")=="EXP-006","aliases")
    check(rig.list_expressions().size()==11,"ten approved profiles plus scoped164")
    check(rig.registry.resolve("EXP-008")=="","next static catalogue item unavailable")
    var d=rig.registry.definition("EXP-006")
    check(d.duration==2.8 and d.keyframes.size()==13,"new authored duration and beats")
    var peaks=[]
    for i in range(1,d.keyframes.size()-1):
        if d.keyframes[i].values.mouth_open>d.keyframes[i-1].values.mouth_open and d.keyframes[i].values.mouth_open>d.keyframes[i+1].values.mouth_open:peaks.append([d.keyframes[i].time,d.keyframes[i].values.mouth_open])
    check(peaks==[[1.36,.16]],"one restrained leak, not three hearty-laugh pulses")
    check(rig.sample_expression("EXP-006",1.0).mouth_open==0 and rig.sample_expression("EXP-006",1.54).mouth_open==0,"pressed before and after leak")
    check(rig.sample_expression("EXP-006",1.0).mouth_corner_lift==.75 and rig.sample_expression("EXP-006",1.54).mouth_corner_lift==.75,"curved pressed hold and re-press")
    check(rig.sample_expression("EXP-006",1.36).mouth_lip_press==1.0,"bounded inner-lip leak coverage")
    for i in range(2801):
        var p=rig.sample_expression("EXP-006",i*.001)
        for k in p:
            var bounds=rig.Registry.CHANNEL_BOUNDS[k]
            check(p[k]>=bounds[0] and p[k]<=bounds[1],"bounded "+k)
        check(p.mouth_open<=.16+0.0000001,"small opening")
        check(p.eye_smile_R<.5 and p.eye_smile_L<.5,"eyes remain partly open, no full crescent")
        check(p.brow_screen_right>=p.brow_screen_left,"consistent one-brow asymmetry")
        check(p.gaze_x==0 and p.gaze_y==0 and p.hair_sway==0,"fixed gaze and hair")
    var times=[0.0,.000001,.20,.30,.44,.70,1.00,1.18,1.36,1.54,1.76,2.04,2.28,2.56,2.799999]
    for t in times:
        for action in ["release","EXP-006","EXP-005","EXP-163","EXP-001","manual","reset"]:
            rig.reset();rig.play_expression("EXP-006");rig.advance(t)
            var before=rig.displayed_pose();var h=rig.head.transform;var b=rig.body.transform
            if action=="release":
                check(rig.release(),"release accepted");check(rig.displayed_pose()==before,"release C0");rig.advance(.45);neutral("release")
            elif action.begins_with("EXP-"):
                check(rig.play_expression(action),"handover accepted");check(rig.displayed_pose()==before,"handover C0");rig.advance(10.0);neutral("handover")
            elif action=="manual":
                check(rig.apply_controls({"mouth_open":.08,"brow_screen_right":.2}),"manual accepted")
                check(rig.active_performance=="" and rig.release_time<0 and rig.manual_mouth_open==.08,"manual takeover")
            else:rig.reset();neutral("reset")
            fixed_owners("lifecycle",h,b)
    for id in ["EXP-163","EXP-005","EXP-001"]:
        for t in [.1,.3,1.3,1.91,2.53,4.5]:
            rig.reset();rig.play_expression(id);rig.advance(t);var before=rig.displayed_pose()
            check(rig.play_expression("EXP-006"),"incoming handover accepted");check(rig.displayed_pose()==before,"incoming handover C0");rig.advance(3.0);neutral("incoming handover")
    rig.reset();rig.play_expression("EXP-006");rig.advance(1.36);rig.release();rig.advance(.2)
    var before=rig.displayed_pose();rig.play_expression("EXP-006");check(rig.displayed_pose()==before,"retrigger during release C0");rig.advance(3.0);neutral("release retrigger")
    for repeat_index in range(5):
        rig.reset();rig.play_expression("EXP-006")
        for i in range(169):rig.advance(1.0/60.0)
        neutral("repeat")
    print("GIGGLE_RUNTIME checks=",checks," failures=",fails.size());quit(1 if fails.size() else 0)

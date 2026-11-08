extends SceneTree
const Limits=preload("res://control_limits.gd")
const Registry=preload("res://expression_registry.gd")
var checks=0
var failures=0
var rig
func check(ok:bool,label:String):
    checks+=1
    if not ok:failures+=1;push_error("BACKBONE_TEST "+label)
func _initialize():call_deferred("run")
func catalogue()->Dictionary:
    return JSON.parse_string(FileAccess.get_file_as_string("res://expressions/registry.json"))
func definition()->Dictionary:
    return JSON.parse_string(FileAccess.get_file_as_string("res://yawn_performance.json"))
func definitions(d:Dictionary)->Dictionary:
    var result={}
    for entry in catalogue().entries:result[entry.path]=JSON.parse_string(FileAccess.get_file_as_string(entry.path))
    result["res://yawn_performance.json"]=d
    return result
func state()->Dictionary:
    var s=rig.get_state();s.erase("last_error")
    s.snapshot=rig.face.snapshot();s.restart=rig.restart_pose.duplicate(true);s.release=rig.release_pose.duplicate(true);s.elapsed=rig.elapsed;s.current=rig.current_pose.duplicate(true);s.performance=rig.performance.duplicate(true)
    return s
func reject_catalogue(r,cat,defs,label:String):
    var old=r.list_expressions();var old_definition=r.definition("EXP-163")
    check(not r.load_catalogue(cat,defs),"reject registry "+label)
    check(r.list_expressions()==old and r.definition("EXP-163")==old_definition,"registry rejection atomic "+label)
func run():
    var r=Registry.new();check(r.load_file(),"registry loads")
    check(r.list_expressions().size()==18,"only authored expression registered")
    check(r.resolve("yawn")=="EXP-163" and r.resolve("EXP-163")=="EXP-163","ID and alias resolve")
    check(r.resolve("EXP-003")=="" and r.definition("unknown").is_empty(),"unimplemented IDs unavailable")
    var d=r.definition("yawn");d.keyframes[1].values.mouth_open=999
    var entries=r.list_expressions();entries[0].aliases.append("bad")
    check(r.definition("yawn").keyframes[1].values.mouth_open!=999 and r.resolve("bad")=="","defensive copies")
    for value in [null,[],"bad",{}, {"schema_version":2,"entries":[]},{"schema_version":true,"entries":[]}]:reject_catalogue(r,value,{},"malformed root")
    var cat=catalogue();cat.bad=true;reject_catalogue(r,cat,definitions(definition()),"unknown root key")
    cat=catalogue();cat.entries.append(cat.entries[0].duplicate(true));reject_catalogue(r,cat,definitions(definition()),"duplicate ID")
    cat=catalogue();cat.entries[0].aliases.append("EXP-163");reject_catalogue(r,cat,definitions(definition()),"alias ID collision")
    cat=catalogue();cat.entries[0].aliases=["yawn","yawn"];reject_catalogue(r,cat,definitions(definition()),"duplicate alias")
    for field in ["id","path","aliases","trigger_phase"]:
        cat=catalogue();cat.entries[0][field]=42;reject_catalogue(r,cat,definitions(definition()),"entry type "+field)
    cat=catalogue();cat.entries[0].surprise=1;reject_catalogue(r,cat,definitions(definition()),"unknown entry key")
    for path in ["https://example.com/x.json","res://../secret.json","res://code.gd"]:
        cat=catalogue();cat.entries[0].path=path;reject_catalogue(r,cat,definitions(definition()),"unsafe path")
    for field in ["id","title","duration","keyframes"]:
        d=definition();d.erase(field);reject_catalogue(r,catalogue(),definitions(d),"missing "+field)
    d=definition();d.unknown=true;reject_catalogue(r,catalogue(),definitions(d),"unknown definition key")
    d=definition();d.id="OTHER";reject_catalogue(r,catalogue(),definitions(d),"ID mismatch")
    for value in [0,-1,NAN,INF,"5.8",true]:
        d=definition();d.duration=value;reject_catalogue(r,catalogue(),definitions(d),"duration")
    for value in [-1,NAN,INF,999,"1",true]:
        d=definition();d.keyframes[1].time=value;reject_catalogue(r,catalogue(),definitions(d),"key time")
    d=definition();d.keyframes[1].time=0;reject_catalogue(r,catalogue(),definitions(d),"equal time")
    d=definition();d.keyframes[2].time=d.keyframes[1].time-.1;reject_catalogue(r,catalogue(),definitions(d),"backwards time")
    d=definition();d.keyframes[0].time=.01;reject_catalogue(r,catalogue(),definitions(d),"missing start")
    d=definition();d.keyframes[-1].time=5.79;reject_catalogue(r,catalogue(),definitions(d),"missing end")
    for value in [[],null,"pose",1]:
        d=definition();d.keyframes[1].values=value;reject_catalogue(r,catalogue(),definitions(d),"values type")
    d=definition();d.keyframes[1].unknown=1;reject_catalogue(r,catalogue(),definitions(d),"unknown keyframe key")
    d=definition();d.keyframes[1].values.face_scale=1;reject_catalogue(r,catalogue(),definitions(d),"unknown channel")
    for channel in Registry.CHANNEL_BOUNDS:
        var bounds=Registry.CHANNEL_BOUNDS[channel]
        for value in [bounds[0]-.001,bounds[1]+.001,NAN,INF,-INF,".5",true]:
            d=definition();d.keyframes[1].values[channel]=value;reject_catalogue(r,catalogue(),definitions(d),"channel "+channel)
    for endpoint in [0,-1]:
        d=definition();d.keyframes[endpoint].values.mouth_open=.01;reject_catalogue(r,catalogue(),definitions(d),"nonneutral endpoint")
    # A second data-only entry proves the controller has no EXP-163 dispatch dependency.
    # This is a test-only alias of the approved data, not an authored/shipped emotion.
    var test_definition=definition();test_definition.id="TEST-DATA";test_definition.title="Data-only fixture"
    cat=catalogue();cat.entries.append({"id":"TEST-DATA","path":"res://test-data.json","aliases":["fixture"]})
    var defs=definitions(definition());defs["res://test-data.json"]=test_definition
    check(r.load_catalogue(cat,defs),"second data entry without controller changes")
    rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
    check(rig.registry_ready,"generic rig loads validated registry")
    check(rig.pose_now()==rig.neutral_pose(),"start neutral")
    check(rig.registry.load_catalogue(cat,defs),"test registry on generic player")
    check(rig.play_expression("fixture") and rig.active_performance=="TEST-DATA","generic ID trigger")
    rig.advance(1.0);check(rig.face.owners.mouth=="TEST-DATA","ownership uses data ID")
    rig.reset();check(rig.registry.load_file(),"restore real registry")
    for mode in ["neutral","performance","release","manual"]:
        rig.reset()
        if mode!="neutral":rig.play_expression("EXP-163");rig.advance(1.7)
        if mode=="release":rig.release();rig.advance(.11)
        if mode=="manual":rig.apply_controls({"mouth_open":.3,"blink":.4,"auto_blink":true})
        var saved=state()
        check(rig.apply_controls({}),"empty command accepted")
        check(state()==saved,"empty command is no-op "+mode)
        check(rig.apply_controls({"reset":false}),"false reset accepted")
        check(state()==saved,"false reset is no-op "+mode)
        check(rig.apply_controls({"release_performance":false}),"false release accepted")
        check(state()==saved,"false release is no-op "+mode)
        for command in [{"perform_expression":"no"},{"perform_expression":"EXP-163","blink":.4},{"release_performance":1},{"release_performance":true,"reset":true},{"mouth_open":NAN},{"mouth_open":INF},{"mouth_open":-.01},{"mouth_open":1.01},{"mouth_open":true},{"blink":-.01},{"blink":1.01},{"brow_raise":INF},{"gaze_x":Limits.GAZE_MAX+.001},{"gaze_y":Limits.GAZE_MIN-.001},{"hair_sway":.070001},{"hair_sway":-.070001},{"reset":true,"bad":1},{"reset":"true"},{"auto_blink":1},{"mouth_open":.5,"mouth":"REST"},{"mouth":"A"},{"viseme":"O"},{"head_scale":1}]:
            check(not rig.apply_controls(command),"invalid API command "+mode)
            check(state()==saved,"invalid command preserves all state "+mode)
        for malformed in [null,[],"controls",1,true]:
            check(not rig.apply_controls(malformed),"non-dictionary command rejected")
            check(state()==saved,"non-dictionary command atomic")
        for delta in [-1,NAN,INF,true,false,"1",null,[],{}]:
            check(not rig.advance(delta),"invalid delta")
            check(state()==saved,"invalid delta atomic")
    rig.reset()
    var neutral=rig.face.snapshot()
    var sequence=[]
    for repeat in range(2):
        rig.reset();check(rig.play_expression("yawn"),"alias trigger")
        for frame in range(360):
            check(rig.advance(1.0/60),"advance")
            if repeat==0:sequence.append(state())
            else:check(state()==sequence[frame],"repeat deterministic")
        check(rig.active_performance=="" and rig.pose_now()==rig.neutral_pose(),"completed neutral")
    for i in range(25):
        rig.reset();rig.play_expression("EXP-163");rig.advance(.1+i*.19)
        var before=rig.displayed_pose();rig.play_expression("EXP-163")
        check(rig.displayed_pose()==before,"retrigger no transaction jump")
        rig.advance(.01);rig.release()
        check(rig.face.owners=={"eyes":"release","brows":"release","mouth":"release","hair":"release"},"immediate release ownership")
        rig.advance(.45)
        check(rig.pose_now()==rig.neutral_pose() and rig.release_time<0,"release exact neutral")
        rig.play_expression("EXP-163");rig.advance(1.5);rig.apply_controls({"mouth_open":.24})
        var manual=rig.pose_now();rig.advance(20)
        check(rig.pose_now()==manual and rig.face.owners.mouth=="manual","manual writer owns channels")
        rig.reset();check(rig.face.snapshot()==neutral,"reset exact appearance")
    for command in [{"perform_expression":"EXP-163"},{"release_performance":true}]:
        rig.reset();rig.apply_controls({"auto_blink":true});rig.advance(4.0)
        var displayed=rig.displayed_pose();check(displayed.blink_R>0,"visible auto blink before handover")
        check(rig.apply_controls(command),"auto blink handover")
        check(rig.displayed_pose()==displayed and not rig.auto_blink,"capture displayed blink continuously")
        rig.advance(8);check(rig.pose_now()==rig.neutral_pose(),"auto blink handover returns neutral")
    for channel in Registry.CHANNEL_BOUNDS:
        for value in Registry.CHANNEL_BOUNDS[channel]:
            rig.reset();check(rig.apply_controls({channel:value}),"supported manual endpoint")
            check(abs(rig.face.oral_objects.cavity.material.get_shader_parameter("opening"))<=.550001,"cap at manual endpoint")
    for x in [Limits.GAZE_MIN,0.0,Limits.GAZE_MAX]:
        for y in [Limits.GAZE_MIN,0.0,Limits.GAZE_MAX]:
            rig.reset();check(rig.apply_controls({"gaze_x":x,"gaze_y":y,"mouth_open":.3}),"gaze rectangle endpoint accepted")
            check(rig.pose_now().gaze_x==x and rig.pose_now().gaze_y==y,"normalized gaze preserved")
            rig.play_expression("EXP-163");rig.advance(.01);rig.release();rig.advance(.45)
            check(rig.pose_now()==rig.neutral_pose(),"gaze handover releases neutral")
    for mode in ["manual","performance","release"]:
        rig.reset();rig.apply_controls({"gaze_x":Limits.GAZE_MAX})
        if mode!="manual":rig.play_expression("EXP-163");rig.advance(.1)
        if mode=="release":rig.release()
        var gaze_saved=state()
        for value in [Limits.GAZE_MIN-.000001,Limits.GAZE_MAX+.000001,true,"0",NAN,INF]:
            check(not rig.apply_controls({"gaze_y":value,"mouth_open":.2,"reset":true}),"invalid mixed gaze rejected")
            check(state()==gaze_saved,"invalid mixed gaze preserves ownership and pose")
    check(Limits.gaze_pixels(Vector2.ZERO)==Vector2.ZERO,"zero gaze maps to zero pixels")
    check(Limits.gaze_pixels(Vector2(-1,-1))==(Vector2(-Limits.GAZE_LEFT_PIXELS,-Limits.GAZE_UP_PIXELS) if Limits.GAZE_ENABLED else Vector2.ZERO),"negative calibrated mapping")
    check(Limits.gaze_pixels(Vector2(1,1))==(Vector2(Limits.GAZE_RIGHT_PIXELS,Limits.GAZE_DOWN_PIXELS) if Limits.GAZE_ENABLED else Vector2.ZERO),"positive calibrated mapping")
    rig.reset();var saved=state();check(rig.sample_expression("no",1).is_empty(),"unknown sample ID")
    check(state()==saved,"sampling does not mutate state")
    for value in [NAN,INF,true,false,"1",null,[],{}]:
        check(rig.sample_expression("EXP-163",value).is_empty(),"invalid sample time")
        check(state()==saved,"invalid sample preserves state")
    for id in [1,true,null,[],{}]:
        check(not rig.play_expression(id),"invalid ID type")
        check(rig.sample_expression(id,1).is_empty(),"invalid sample ID type")
        check(state()==saved,"invalid ID preserves state")
    for i in range(10001):
        var pose=rig.sample_expression("EXP-163",i*5.8/10000.0)
        for channel in Registry.CHANNEL_BOUNDS:
            check(pose[channel]>=Registry.CHANNEL_BOUNDS[channel][0] and pose[channel]<=Registry.CHANNEL_BOUNDS[channel][1],"dense sample bounds")
    var viewer=load("res://expression_viewer.tscn").instantiate();root.add_child(viewer);viewer.rig.set_process(false);viewer.set_process(false)
    check(viewer.sliders.has("gaze_x")==Limits.GAZE_ENABLED and viewer.sliders.has("gaze_y")==Limits.GAZE_ENABLED,"gaze slider availability matches contract")
    check(viewer.list_expressions().size()==18,"viewer uses registry")
    var count=0
    for node in viewer.get_children():
        if node.get_script()==load("res://expression_rig.gd"):count+=1
    check(count==1,"viewer contains exactly one shared rig")
    viewer.apply_controls({"reset":true})
    viewer.sliders.mouth_open.value=.327
    check(is_equal_approx(viewer.rig.manual_mouth_open,.327),"slider signal reaches common controller")
    viewer.auto_blink_button.button_pressed=true
    check(viewer.rig.auto_blink,"checkbox signal reaches common controller")
    for key in [KEY_P,KEY_SPACE,KEY_0]:
        var event=InputEventKey.new();event.keycode=key;event.pressed=true
        Input.parse_input_event(event)
        Input.flush_buffered_events()
        await process_frame
        if key==KEY_P:check(viewer.rig.active_performance=="EXP-163","global play shortcut")
        elif key==KEY_SPACE:check(viewer.rig.release_time==0,"global release shortcut")
        else:check(viewer.rig.pose_now()==viewer.rig.neutral_pose(),"global reset shortcut")
    for repeat in range(5):
        check(viewer.play_selected(),"viewer play")
        viewer.rig.advance(.9);check(viewer.apply_controls({"release_performance":true}),"viewer release")
        viewer.rig.advance(.45);check(viewer.apply_controls({"reset":true}),"viewer reset")
    print("EXPRESSION_BACKBONE_", "PASS" if failures==0 else "FAIL", " checks=",checks," failures=",failures)
    quit(0 if failures==0 else 1)

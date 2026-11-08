extends SceneTree
const TRIO=["mouth_open","mouth_width_screen_left","mouth_width_screen_right"]
var rig
var checks=0
var failures=[]
var fixtures=[]
var fixture_definitions={}
var base_catalogue={}
var base_definitions={}
var fixture_count=0
var transition_samples=0
var pair_count=0
var bridge
var sequence=0
func _initialize():call_deferred("run")
func check(ok,label):
    checks+=1
    if not ok:
        failures.append(label)
        if failures.size()<20:push_error(label)
func state():
    var s=rig.get_state();s.erase("last_error");s.face=rig.face.snapshot();s.restart=rig.restart_pose.duplicate(true);s.release=rig.release_pose.duplicate(true);s.performance=rig.performance.duplicate(true);s.writes=rig.completed_write_count;return s
func domain(p):return not (p.mouth_open>0.0 and (p.mouth_width_screen_left>0.0 or p.mouth_width_screen_right>0.0))
func near(a,b,tolerance=0.000001):return abs(float(a)-float(b))<=tolerance
func zero_trio(p):return p.mouth_open==0.0 and p.mouth_width_screen_left==0.0 and p.mouth_width_screen_right==0.0
func fixture(id,values,duration=0.4):
    var frames=[]
    for item in values:frames.append({"time":float(item[0])*duration,"phase":"fixture","values":item[1]})
    var d={"id":id,"title":"Detached sealed-domain test","duration":duration,"keyframes":frames}
    fixtures.append({"id":id,"path":"res://test_fixtures/"+id+".json","aliases":[]})
    fixture_definitions[fixtures[-1].path]=d
    fixture_count+=1
func load_fixtures():
    var cat=base_catalogue.duplicate(true);cat.entries.append_array(fixtures)
    var defs=base_definitions.duplicate(true);defs.merge(fixture_definitions)
    check(rig.registry.load_catalogue(cat,defs),"load detached validated fixture catalogue")
func prepare(p):
    check(rig.reset(),"reset")
    if not p.is_empty():check(rig.apply_controls(p),"prepare manual source")
func expected_mode(source,d):
    var target_width=false;var target_open=false
    for f in d.keyframes:
        target_width=target_width or rig.Registry.width_present(f.values)
        target_open=target_open or float(f.values.get("mouth_open",0))>0
    var source_width=rig.Registry.width_present(source)
    if not source_width and not target_width:return "legacy"
    return "staged" if (source_width and target_open) or (source.mouth_open>0 and target_width) else "bounded_direct"
func expect_pose(source,d,t,mode):
    var p=rig._sample(d,t)
    if t>=d.duration:return p
    var target=p.duplicate(true)
    if t<.30:
        var u=smoothstep(0.0,.30,t)
        for key in rig.CHANNELS:p[key]=lerpf(source.get(key,0),target[key],u)
    if mode=="legacy":return p
    var duration=minf(.30,d.duration)
    if t>=duration:
        for key in TRIO:p[key]=target[key]
        return p
    var u=t/duration
    for key in TRIO:
        if mode=="bounded_direct":p[key]=lerpf(source[key],target[key],smoothstep(0.0,1.0,u))
        elif u<=.5:p[key]=source[key]*(1.0-smoothstep(0.0,.5,u))
        else:p[key]=target[key]*smoothstep(.5,1.0,u)
    return p
func check_pose(source,d,t,mode,label):
    var p=rig.pose_now();var expected=expect_pose(source,d,t,mode)
    check(domain(p),label+" valid domain")
    for key in rig.CHANNELS:check(near(p[key],expected[key]),label+" exact rule "+key)
    check(rig.face.mouth_width_sides==Vector2(p.mouth_width_screen_left,p.mouth_width_screen_right),label+" actual face widths")
    check(near(rig.face.mouth_opening,p.mouth_open),label+" actual face opening")
    transition_samples+=1
func atomic_checks():
    for initial in [{"mouth_open":.8},{"mouth_width_screen_left":.8,"mouth_width_screen_right":.3}]:
        prepare(initial)
        var before=state()
        var bad={"mouth_width_screen_left":.2} if initial.has("mouth_open") else {"mouth_open":.2}
        check(not rig.apply_controls(bad),"retained omitted field rejects")
        check(state()==before,"rejected request touches no writer or state")
        var good={"mouth_open":0.0,"mouth_width_screen_left":1.0} if initial.has("mouth_open") else {"mouth_width_screen_left":0.0,"mouth_width_screen_right":0.0,"mouth_open":1.0}
        check(rig.apply_controls(good) and domain(rig.pose_now()),"coherent atomic domain change")
        check(rig.apply_controls({"reset":true,"mouth_width_screen_right":.7}),"reset then explicit prospective fields")
        check(rig.pose_now().mouth_open==0 and near(rig.pose_now().mouth_width_screen_right,.7),"reset starts from zero")
    prepare({"mouth_open":.8})
    check(rig.apply_controls({"mouth":"REST","mouth_width_screen_left":.5}),"REST closes before width validation")
    for mode in ["manual","active","release","source_half","target_half"]:
        prepare({"mouth_width_screen_left":.7,"auto_blink":true})
        if mode!="manual":rig.play_expression("TEST-open_late")
        if mode=="active":rig.advance(.31)
        elif mode=="release":rig.advance(.07);rig.release();rig.advance(.01)
        elif mode=="source_half":rig.advance(.07)
        elif mode=="target_half":rig.advance(.21)
        for key in TRIO:
            for bad in [-.000001,1.000001,NAN,INF,-INF,true,false,".2",null,[],{}]:
                var before=state()
                check(not rig.apply_controls({"reset":true,key:bad}),"typed rejection "+mode)
                check(state()==before,"typed atomic preservation "+mode)
        var before=state()
        check(not rig.apply_controls({"reset":true,"mouth_open":1,"mouth_width_screen_right":1}),"full invalid trio rejects "+mode)
        check(state()==before,"full invalid preserves stage/blink "+mode)
        var p=rig.pose_now()
        if p.mouth_open>0:
            check(not rig.apply_controls({"mouth_width_screen_left":.2}),"actual authored retained opening rejects")
        elif rig.Registry.width_present(p):
            check(not rig.apply_controls({"mouth_open":.2}),"actual authored retained width rejects")
    check(rig.invalid_completed_writes.is_empty(),"every completed synchronous face write valid")
func registry_checks():
    var old=rig.list_expressions()
    var bad=[
        [[0,{}],[.25,{"mouth_open":.3,"mouth_width_screen_left":.2}],[1,{}]],
        [[0,{}],[.25,{"mouth_width_screen_left":1}],[.5,{"mouth_open":1}],[1,{}]],
        [[0,{}],[.25,{"mouth_open":1}],[.5,{"mouth_width_screen_right":1}],[1,{}]]]
    for frames in bad:
        var d={"id":"TEST-invalid","title":"Invalid detached fixture","duration":1.0,"keyframes":[]}
        for item in frames:d.keyframes.append({"time":item[0],"phase":"fixture","values":item[1]})
        var cat=base_catalogue.duplicate(true);cat.entries.append({"id":d.id,"path":"res://test_fixtures/bad.json"})
        var defs=base_definitions.duplicate(true);defs["res://test_fixtures/bad.json"]=d
        check(not rig.registry.load_catalogue(cat,defs),"invalid full segment rejects")
        check(rig.list_expressions()==old,"invalid catalogue atomic rollback")
    for entry in fixtures:
        var d=rig.registry.definition(entry.id)
        for i in range(501):check(domain(rig._sample(d,d.duration*float(i)/500)),"dense fixture valid segments")
func transition_checks():
    var source_controls=[{}, {"mouth_open":.8,"mouth_smile":.4,"mouth_corner_lift_screen_left":.7,"brow_screen_left":.4}, {"mouth_width_screen_left":1.0,"mouth_width_screen_right":.3,"mouth_purse":.7,"mouth_lip_press":.3,"hair_sway":.03}]
    for entry in fixtures:
        var d=rig.registry.definition(entry.id)
        for control in source_controls:
            prepare(control);var source=rig.displayed_pose();var mode=expected_mode(source,d)
            check(rig.play_expression(entry.id),"trigger fixture")
            check(rig.mouth_bridge_mode==mode,"trigger-fixed classification")
            check(rig.mouth_transition_state().duration==(.30 if mode=="legacy" else minf(.30,d.duration)),"metadata reports actual selected bridge duration")
            check(rig.displayed_pose()==source,"trigger C0")
            var duration=minf(.30,d.duration)
            var times=[0.0,duration*.5-1e-9,duration*.5,duration*.5+1e-9,duration-1e-9,duration,duration+1e-9,d.duration-1e-9,d.duration]
            for i in range(1,101):times.append(d.duration*float(i)/100)
            times.sort();var elapsed=0.0
            for target in times:
                target=minf(d.duration,target)
                check(rig.advance(maxf(0.0,target-elapsed)),"advance fixture")
                elapsed=target
                check_pose(source,d,rig.performance_time,mode,entry.id)
                if rig.active_performance!="":check(rig.mouth_bridge_mode==mode,"mode never flips on opening")
            check(rig.pose_now()==rig.neutral_pose(),"short and normal fixture completes neutral")
            # Real Godot elapsed-state comparison, not a pure formula re-evaluation.
            for destination in [duration*.51,duration*1.1,d.duration-1e-9,d.duration]:
                destination=minf(destination,d.duration)
                prepare(control);rig.play_expression(entry.id);rig.advance(destination);var large=rig.pose_now();var large_mode=rig.mouth_bridge_mode
                prepare(control);rig.play_expression(entry.id)
                for step in range(1,38):
                    var next=destination if step==37 else destination*float(step)/37
                    rig.advance(maxf(0.0,next-rig.performance_time))
                for key in rig.CHANNELS:check(near(rig.pose_now()[key],large[key]),"large step versus incremental "+key)
                check(rig.mouth_bridge_mode==large_mode,"large-step fixed mode")
            # The former short direct bug retained roughly 0.74 source width.
            if d.duration<.30 and mode!="legacy":
                prepare(control);rig.play_expression(entry.id);rig.advance(d.duration-1e-9)
                for key in TRIO:check(abs(rig.pose_now()[key])<1e-6,"new trio has no short-target completion snap")
                for key in ["mouth_smile","mouth_purse","mouth_lip_press","brow_screen_left","hair_sway"]:
                    check(near(rig.pose_now()[key],expect_pose(source,d,d.duration-1e-9,mode)[key]),"remaining old channel preserves inherited short behavior")
func pair_checks():
    var all=rig.list_expressions()
    for source in all:
        for target in all:
            for blink in [false,true]:
                prepare({"auto_blink":blink});rig.play_expression(source.id);rig.advance(source.duration*.37)
                var before=rig.displayed_pose()
                check(rig.play_expression(target.id) and rig.displayed_pose()==before,"ordered pair C0")
                var mode=rig.mouth_bridge_mode;var duration=minf(.30,target.duration)
                for step in [duration*.25,duration*.5,duration*.75,duration,target.duration]:
                    rig.advance(maxf(0.0,step-rig.performance_time))
                    check(domain(rig.pose_now()),"ordered pair no overlap")
                    if rig.active_performance!="":check(rig.mouth_bridge_mode==mode,"ordered fixed plan")
                check(rig.pose_now()==rig.neutral_pose() and rig.auto_blink==blink and not rig.auto_blink_pending_restore,"ordered blink neutral restoration")
                pair_count+=1
    for target in ["TEST-closed","TEST-open_late","TEST-mixed","TEST-short_closed"]:
        for phase in [.25,.5,.75]:
            for blink in [false,true]:
                prepare({"mouth_open":.8,"auto_blink":blink});rig.play_expression(target);rig.advance(minf(.30,rig.performance.duration)*phase)
                var before=rig.displayed_pose()
                check(rig.release() and rig.displayed_pose()==before,"release C0 during bridge")
                rig.advance(.1);before=rig.displayed_pose();check(rig.release() and rig.displayed_pose()==before,"repeated release C0")
                rig.advance(.45);check(rig.pose_now()==rig.neutral_pose() and rig.auto_blink==blink,"no former manual opening resurfaces")
                prepare({"mouth_width_screen_left":1,"auto_blink":blink});rig.play_expression("TEST-open_late");rig.advance(.30*phase)
                before=rig.displayed_pose();check(rig.play_expression(target) and rig.displayed_pose()==before,"retrigger or reversal C0")
                rig.advance(rig.performance.duration);check(rig.pose_now()==rig.neutral_pose() and rig.auto_blink==blink,"reversal completes neutral")
func dispatch(verb,args={}):
    sequence+=1
    var request={"protocol":1,"id":sequence,"verb":verb,"args":args}
    if verb in bridge.WRITE_VERBS:request.session=bridge.session
    bridge.dispatch(JSON.stringify(request).to_utf8_buffer())
    var response=JSON.parse_string(bridge.outgoing.get_string_from_utf8());bridge.outgoing.clear();return response
func ui_bridge_checks():
    bridge=load("res://control_bridge.gd").new();bridge.rig=rig;bridge.session=19;bridge.external_enabled=true
    var caps=dispatch("capabilities")
    check(caps.ok and caps.result.independent_width.scope=="sealed_mouth_only","bridge declares sealed domain")
    check(dispatch("apply_controls",{"reset":true,"mouth_open":1}).ok,"bridge open setup")
    var before=state();check(not dispatch("apply_controls",{"mouth_width_screen_left":1}).ok,"bridge rejects retained opening")
    check(state()==before,"bridge rejection atomic")
    check(dispatch("apply_controls",{"mouth_open":0,"mouth_width_screen_left":1}).ok,"bridge atomic switch")
    bridge.free()
    var viewer=load("res://expression_viewer.tscn").instantiate();root.add_child(viewer);viewer.set_process(false);viewer.rig.set_process(false)
    check(viewer.expression_ids==["EXP-163","EXP-005","EXP-001","EXP-006","EXP-107","EXP-007","EXP-002","EXP-152","EXP-160","EXP-177","EXP-164","EXP-021","EXP-158","EXP-181","EXP-102","EXP-116","EXP-050","EXP-186","EXP-114"],"viewer exact eighteen approved profiles")
    viewer.apply_controls({"mouth_open":.4});viewer._process(0)
    check(not viewer.sliders.mouth_width_screen_left.editable and viewer.sliders.mouth_open.editable,"viewer width disabled while open")
    check(not viewer.apply_controls({"mouth_width_screen_right":.5}),"viewer backend domain authoritative")
    viewer.apply_controls({"mouth_open":0,"mouth_width_screen_right":.5});viewer._process(0)
    check(not viewer.sliders.mouth_open.editable and viewer.sliders.mouth_width_screen_left.editable,"viewer opening disabled while wide")
    viewer.apply_controls({"reset":true});viewer._process(0)
    check(viewer.sliders.mouth_open.editable and viewer.sliders.mouth_width_screen_left.editable,"viewer neutral unlocks trio")
    viewer.queue_free()
func run():
    rig=load("res://expression_rig.tscn").instantiate()
    rig.set_script(load(get_script().resource_path.get_base_dir()+"/sealed_observed_rig.gd"))
    root.add_child(rig);rig.set_process(false)
    check(rig.rig_ready and rig.registry_ready,"ready")
    if not rig.rig_ready or not rig.registry_ready:quit(2);return
    base_catalogue=JSON.parse_string(FileAccess.get_file_as_string("res://expressions/registry.json"))
    for entry in base_catalogue.entries:base_definitions[entry.path]=JSON.parse_string(FileAccess.get_file_as_string(entry.path))
    check(base_catalogue.entries.size()==19,"eighteen approved profile baseline")
    var closed=[[0,{}],[.25,{"mouth_width_screen_left":1,"mouth_width_screen_right":.4,"mouth_purse":.2}],[1,{}]]
    var opened=[[0,{}],[.25,{"mouth_open":1}],[1,{}]]
    var mixed=[[0,{}],[.2,{"mouth_width_screen_left":1}],[.4,{}],[.6,{"mouth_open":1}],[1,{}]]
    var reverse=[[0,{}],[.2,{"mouth_open":1}],[.4,{}],[.6,{"mouth_width_screen_right":1}],[1,{}]]
    fixture("TEST-closed",closed);fixture("TEST-open",opened);fixture("TEST-mixed",mixed);fixture("TEST-reverse",reverse)
    fixture("TEST-open_late",[[0,{}],[.5,{}],[.75,{"mouth_open":1}],[1,{}]],1.2)
    fixture("TEST-short_neutral",[[0,{}],[1,{}]],.1)
    for setting in [["short",.1],["equal",.3],["above",.31]]:
        fixture("TEST-"+setting[0]+"_closed",closed,setting[1]);fixture("TEST-"+setting[0]+"_open",opened,setting[1]);fixture("TEST-"+setting[0]+"_mixed",mixed,setting[1]);fixture("TEST-"+setting[0]+"_reverse",reverse,setting[1])
    load_fixtures();atomic_checks();registry_checks();transition_checks();pair_checks();ui_bridge_checks()
    check(rig.invalid_completed_writes.is_empty(),"all completed face writes valid")
    var result={"status":"PASS" if failures.is_empty() else "FAIL","checks":checks,"failures":failures,"fixtures":fixture_count,"transition_samples":transition_samples,"ordered_pairs_with_blink_modes":pair_count,"completed_face_writes":rig.completed_write_count,"invalid_completed_face_writes":rig.invalid_completed_writes,"real_socket":false,"graphical_capture":false}
    var output=OS.get_cmdline_user_args()[0] if not OS.get_cmdline_user_args().is_empty() else "user://sealed_width_contract_results.json"
    var f=FileAccess.open(output,FileAccess.WRITE);f.store_string(JSON.stringify(result,"  "));f.close()
    print("SEALED_CONTRACT checks=",checks," failures=",failures.size()," samples=",transition_samples," pairs=",pair_count);quit(0 if failures.is_empty() else 1)

extends SceneTree
var checks=0
var failures=0
func verify(v,label):
    checks+=1
    if not v:push_error(label);failures+=1
func _initialize():call_deferred("run")
func run():
    var Store=load("res://pose_store.gd")
    var a=Store.new();a.path="user://test_pose_store.json"
    var data={"head_tilt":.35,"head_x":-.2,"head_y":0.1,"body_tilt":-.4,"body_x":.1,"body_y":-.1,"body_follow":false}
    verify(a.save_slot(1,data),"save")
    var b=Store.new();b.path=a.path;verify(b.load_disk(),"fresh instance load")
    verify(b.recall(1)==data,"round trip exact")
    var changed=b.recall(1);changed.head_tilt=1.0;verify(b.recall(1)==data,"snapshot isolation")
    verify(not b.save_slot(4,data),"slot bounds")
    var bad=data.duplicate();bad.head_tilt=NAN;verify(not b.save_slot(2,bad),"nonfinite rejected")
    bad=data.duplicate();bad.body_x=3;verify(not b.save_slot(2,bad),"out of range rejected")
    var file=FileAccess.open(a.path,FileAccess.WRITE);file.store_string("bad json");file.close()
    verify(not b.load_disk() and b.recall(1)==data,"corrupt file preserves memory")
    var rig=load("res://motion_rig.tscn").instantiate();root.add_child(rig);await process_frame;rig.set_process(false)
    rig.pose_store.path="user://test_rig_pose_store.json"
    rig.apply_controls({"head_tilt":.4,"body_tilt":-.2,"pose_save":1})
    rig.apply_controls({"head_tilt":-.3,"body_tilt":.3});rig._process(.2)
    var prior=rig.current;verify(rig.recall_pose(1),"recall")
    rig._process(.001);verify(rig.current.distance_to(prior)<.02,"recall eased")
    for i in range(150):
        rig._process(1.0/30)
        verify(rig.target==Vector3(.4,0,0) and rig.body_target==Vector3(-.2,0,0),"recalled targets persist")
    verify(rig.current.distance_to(rig.target)<.0001,"settles")
    rig.apply_controls({"gesture":"greet","wink":"screen_left","audio_level":.8});rig._process(.15)
    verify(rig.gestures.active=="greet" and rig.face.blink_right and rig.face.mouth_state=="A","other rig controls coexist")
    var stable=rig.target;verify(not rig.recall_pose(3) and rig.target==stable,"empty slot doesn't move")
    rig.apply_controls({"reset":true});verify(rig.pose_store.recall(1).size()>0,"reset preserves saved slots")
    rig.set_process(true)
    var key=InputEventKey.new();key.keycode=KEY_1;key.physical_keycode=KEY_1;key.pressed=true;Input.parse_input_event(key)
    await process_frame;await process_frame;verify(rig.target==Vector3(.4,0,0),"keyboard recall")
    if failures==0:print("POSE_STORE_CHECKS_PASS count=",checks)
    quit(1 if failures else 0)

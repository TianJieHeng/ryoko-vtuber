extends SceneTree
var checks=0
var failures=0
func verify(v,label):
    checks+=1
    if not v:push_error(label);failures+=1
func _initialize():call_deferred("run")
func run():
    var h=load("res://hair_secondary.gd").new()
    for y in [330,350,450,600,790,920,1100,1384]:
        for x in [0,300,568,800,1136]:verify(h.weight(Vector2(x,y))==0.0,"face/neck/body unaffected")
    verify(h.weight(Vector2(568,100))==1.0,"bun free weight")
    verify(h.weight(Vector2(568,200))>0 and h.weight(Vector2(568,200))<1,"root feather")
    h.step(Vector2.ZERO,1.0/30)
    for i in range(60):h.step(Vector2.ZERO,1.0/30);verify(h.offset==Vector2.ZERO,"no idle motion")
    var peak=0.0
    for i in range(60):
        h.step(Vector2(40,5),1.0/30);peak=max(peak,h.offset.length());verify(h.offset.length()<=8.001,"bounded")
    verify(peak>1,"movement drives lag")
    for i in range(120):h.step(Vector2(40,5),1.0/30)
    verify(h.offset==Vector2.ZERO and h.velocity==Vector2.ZERO,"held pose settles")
    h.enabled=false;h.step(Vector2(-40,0),.1);verify(h.offset==Vector2.ZERO,"off exact baseline")
    h.enabled=true;h.reset()
    for dt in [.016,.033,.1,.3]:
        for i in range(30):h.step(Vector2(i%2*200,0),dt);verify(h.offset.is_finite() and h.offset.length()<=8.001,"variable-frame stable")
    var rig=load("res://motion_rig.tscn").instantiate();root.add_child(rig);await process_frame;rig.set_process(false)
    rig.apply_controls({"head_tilt":.7,"body_tilt":0});var rig_peak=0.0
    for i in range(90):rig._process(1.0/30);rig_peak=max(rig_peak,rig.hair.offset.length())
    verify(rig_peak>.1,"head movement wired")
    verify(rig.hair.offset.length()<.01,"live hold settles")
    rig.apply_controls({"hair_secondary":false,"head_tilt":-.7});rig._process(.1)
    verify(rig.skin_material.get_shader_parameter("hair_offset")==Vector2.ZERO,"shader off")
    rig.apply_controls({"hair_secondary":true,"reset":true});verify(rig.hair.offset==Vector2.ZERO,"reset")
    if failures==0:print("HAIR_SECONDARY_CHECKS_PASS count=",checks," head_peak=",rig_peak)
    quit(1 if failures else 0)

extends SceneTree
const FPS=30
const SECONDS=17
var rig
func _initialize():call_deferred("run")
func matrix(node:Node2D)->Array:
    var t=node.global_transform
    return [t.x.x,t.x.y,t.y.x,t.y.y,t.origin.x,t.origin.y]
func run():
    rig=load("res://full_body/full_body_rig.tscn").instantiate();root.add_child(rig);rig.expression_rig.set_process(false)
    if not rig.ready_for_controls:quit(1);return
    var frames=[]
    for i in range(SECONDS*FPS+1):
        var t=float(i)/FPS
        var pose={"reset":true}
        var phase="Neutral assembly"
        if t>=1 and t<5:
            phase="Head attachment / +/- 3 degrees"
            pose.head_tilt=sin((t-1)/4*TAU)
        elif t>=5 and t<9:
            phase="Chest and spine / small joint sweep"
            var v=sin((t-5)/4*TAU)
            pose.spine_tilt=v;pose.chest_tilt=v*.5
        elif t>=9 and t<13:
            phase="Arms and legs / bounded overlap check"
            var v=sin((t-9)/4*TAU)
            for key in ["shoulder_L","elbow_L","wrist_L","hip_L","knee_L","ankle_L"]:pose[key]=v
            for key in ["shoulder_R","elbow_R","wrist_R","hip_R","knee_R","ankle_R"]:pose[key]=-v
        elif t>=13 and t<16:
            phase="Frame positioning / rigid whole-rig movement"
            var v=sin((t-13)/3*TAU)
            pose.frame_x=v;pose.frame_y=v*.5;pose.frame_roll=v*.5
        if not rig.apply_body_controls(pose):push_error(rig.last_error);quit(1);return
        var layer_transforms={}
        for id in rig.layer_nodes:layer_transforms[id]=matrix(rig.layer_nodes[id])
        frames.append({"time":t,"phase":phase,"layers":layer_transforms,"head":matrix(rig.expression_rig.head),"joints":rig.get_body_state().joints})
    var f=FileAccess.open("res://full_body/review/transform_samples.json",FileAccess.WRITE)
    f.store_string(JSON.stringify({"fps":FPS,"seconds":SECONDS,"source":"Actual Godot 4.6.3 full_body_rig global transforms; neutral approved face preview only.","frames":frames}));f.close()
    print("SAMPLED ",frames.size()," actual engine poses");quit()

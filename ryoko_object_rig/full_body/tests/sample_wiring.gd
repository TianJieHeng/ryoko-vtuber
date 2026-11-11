extends SceneTree
const FPS=30
const SECONDS=15
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
        # One owner at a time, always returning to neutral. No lean or actions.
        if t>=2 and t<6:
            phase="Head attachment only / +/- 3 degrees"
            pose.head_tilt=sin((t-2)/4*TAU)
        elif t>=6 and t<10:
            phase="Right elbow attachment only / +/- 2 degrees"
            pose.elbow_R=sin((t-6)/4*TAU)
        elif t>=10 and t<14:
            phase="Left elbow attachment only / +/- 2 degrees"
            pose.elbow_L=sin((t-10)/4*TAU)
        if not rig.apply_body_controls(pose):push_error(rig.last_error);quit(1);return
        var layer_transforms={}
        for id in rig.layer_nodes:layer_transforms[id]=matrix(rig.layer_nodes[id])
        frames.append({"time":t,"phase":phase,"layers":layer_transforms,"head":matrix(rig.expression_rig.head),"joints":rig.get_body_state().joints})
    var f=FileAccess.open("res://full_body/review/transform_samples.json",FileAccess.WRITE)
    f.store_string(JSON.stringify({"fps":FPS,"seconds":SECONDS,"source":"Actual Godot 4.6.3 full_body_rig global transforms; neutral approved face preview only.","frames":frames}));f.close()
    print("SAMPLED ",frames.size()," actual engine poses");quit()

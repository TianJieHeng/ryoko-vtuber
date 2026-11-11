extends SceneTree
## Sample actual runtime meshes, never an independent copy of the spring math.
const FPS = 30
const SECONDS = 8
var rig
func _initialize():call_deferred("run")
func matrix(node:Node2D)->Array:
    var t = node.global_transform
    return [t.x.x,t.x.y,t.y.x,t.y.y,t.origin.x,t.origin.y]
func vertices(points:PackedVector2Array)->Array:
    var out = []
    for p in points:out.append([snappedf(p.x,0.0001),snappedf(p.y,0.0001)])
    return out
func run():
    rig = load("res://full_body/full_body_rig.tscn").instantiate();root.add_child(rig)
    if not rig.ready_for_controls:push_error(rig.last_error);quit(1);return
    rig.set_physics_process(false);rig.expression_rig.set_process(false)
    rig.play_bounce_demo()
    var mesh_data = {}
    for id in rig.secondary_motion.meshes:
        var spec:Dictionary = rig.secondary_motion.meshes[id]
        var tris = []
        for triangle in spec.node.polygons:tris.append(Array(triangle))
        mesh_data[id] = {"uv":vertices(spec.node.uv), "rest_vertices":vertices(spec.rest), "triangles":tris}
    var frames = []
    for i in range(SECONDS * FPS + 1):
        if i > 0:
            for substep in range(4):rig.advance_secondary_motion(1.0/120.0)
        var layers = {}
        for id in rig.layer_nodes:layers[id] = matrix(rig.layer_nodes[id])
        var mesh_vertices = {}
        for id in rig.secondary_motion.meshes:mesh_vertices[id] = vertices(rig.layer_nodes[id].polygon)
        var physics:Dictionary = rig.secondary_motion.snapshot()
        frames.append({"time":float(i)/FPS,"phase":physics.phase,"layers":layers,"head":matrix(rig.expression_rig.head),"joints":rig.get_body_state().joints,"physics":physics,"mesh_vertices":mesh_vertices})
    var result = {"fps":FPS,"seconds":SECONDS,"step_hz":120,"source":"Actual Godot 4.6.3 spring states, global transforms, Polygon2D vertices/UVs/triangles. CPU preview must use this geometry; native pixels and pacing are unverified.","meshes":mesh_data,"frames":frames}
    var file = FileAccess.open("res://full_body/review/bounce_samples.json",FileAccess.WRITE)
    file.store_string(JSON.stringify(result));file.close()
    print("SAMPLED ",frames.size()," actual engine bounce poses, ",mesh_data.size()," meshes");quit()

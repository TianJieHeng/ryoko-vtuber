extends SceneTree
## Focused actual-runtime checks. This is not native visual/pixel validation.
var checks = 0
var failures = []
var rig
func _initialize():call_deferred("run")
func check(ok:bool, label:String):
    checks += 1
    if not ok:failures.append(label)
func meshes_at_rest()->bool:
    for spec in rig.secondary_motion.meshes.values():
        if spec.node.polygon != spec.rest:return false
    return true
func mesh_topology_valid()->bool:
    for spec in rig.secondary_motion.meshes.values():
        var points:PackedVector2Array = spec.node.polygon
        for p in points:
            if not is_finite(p.x) or not is_finite(p.y):return false
        for tri in spec.node.polygons:
            if (points[tri[1]]-points[tri[0]]).cross(points[tri[2]]-points[tri[0]]) <= 0.0:return false
    return true
func advance(duration:float, fps:float = 120.0):
    for i in range(int(round(duration * fps))):rig.advance_secondary_motion(1.0/fps)
func run():
    rig = load("res://full_body/full_body_rig.tscn").instantiate();root.add_child(rig)
    check(rig.ready_for_controls,"assembly readiness")
    if not rig.ready_for_controls:print(rig.last_error);quit(1);return
    rig.set_physics_process(false);rig.expression_rig.set_process(false)
    var neutral_joints:Dictionary = rig.get_body_state().joints
    var neutral_face:Dictionary = rig.expression_rig.face.snapshot()
    var neutral_layer_transforms = {}
    for id in rig.layer_nodes:neutral_layer_transforms[id] = rig.layer_nodes[id].transform
    check(rig.layer_nodes.size() == 23,"exactly 23 original artwork owners")
    check(rig.secondary_motion.meshes.size() == 5,"five textured meshes and no duplicate artwork")
    check(rig.joints.size() == 17,"17 unit-scale anatomical joints")
    check(rig.list_expressions().size() == 47,"47 approved facial profiles preserved")
    for spec in rig.registration.layers:
        var node:Node2D = rig.layer_nodes[spec.id]
        check(node.get_parent() == rig.joints[spec.parent],spec.id+" original parent")
        check(node.texture.resource_path == spec.file,spec.id+" original texture")
        check(node.scale.is_equal_approx(Vector2(float(spec.scale[0]),float(spec.scale[1]))),spec.id+" original scale")
    for id in ["blouse_collar_L","blouse_collar_R","blazer_button"]:
        var node:Node2D = rig.layer_nodes[id]
        var extent:Vector2 = node.texture.get_size()
        var pinned = true
        for y in range(11):
            for x in range(11):
                var p:Vector2 = rig.to_local(node.to_global(extent * Vector2(x/10.0,y/10.0)))
                if rig.secondary_motion.cloth_weight(p) != 0.0:pinned = false
        check(pinned,id+" entirely outside chest deformation support")
    advance(1.0)
    check(meshes_at_rest(),"no automatic idle cloth motion")
    check(rig.get_body_state().joints == neutral_joints,"no automatic idle body motion")
    check(rig.layer_nodes.necklace_pendant.transform == neutral_layer_transforms.necklace_pendant,"no idle pendant motion")
    rig.play_bounce_demo()
    var peak_chest = 0.0
    var peak_pendant = 0.0
    var peak_root = 0.0
    var topology_ok = true
    var settle_followthrough = false
    var mirrored_motion = false
    var sampled = []
    for i in range(961):
        if i > 0:rig.advance_secondary_motion(1.0/120.0)
        var state:Dictionary = rig.secondary_motion.snapshot()
        peak_chest = maxf(peak_chest,absf(state.chest_y))
        peak_pendant = maxf(peak_pendant,absf(state.pendant_y))
        peak_root = maxf(peak_root,absf(state.root_y))
        if i % 4 == 0:topology_ok = topology_ok and mesh_topology_valid()
        if state.elapsed > 3.02 and state.elapsed < 3.3 and absf(state.chest_y) > 0.2:settle_followthrough = true
        if state.root_acceleration < -300.0 and state.chest_y > 0.3:mirrored_motion = true
        if i == 120 or i == 360:sampled.append([state.chest_y,state.pendant_y,state.root_y])
    check(topology_ok,"all sampled mesh triangles finite, nondegenerate, no foldovers")
    check(peak_root > 19.99 and peak_root <= 20.00001,"20px maximum small bounce")
    check(peak_chest > 4.0 and peak_chest < 10.0,"restrained nonzero chest response below hard bound")
    check(peak_pendant > 1.0 and peak_pendant < 6.0,"restrained nonzero pendant response below hard bound")
    check(settle_followthrough,"chest keeps moving after root stops")
    check(mirrored_motion,"inertial lag opposes upward acceleration")
    check(meshes_at_rest(),"all meshes return to bit-exact rest vertices")
    check(rig.get_body_state().joints == neutral_joints,"settled skeleton returns to exact neutral")
    check(rig.layer_nodes.necklace_pendant.transform == neutral_layer_transforms.necklace_pendant,"pendant returns to exact neutral transform")
    check(rig.expression_rig.face.snapshot() == neutral_face,"bounce does not mutate face controls")
    check(not rig.secondary_motion.demo_active,"demo automatically sleeps after settling")
    for fps in [30.0,60.0]:
        rig.play_bounce_demo();advance(1.0,fps)
        var state:Dictionary = rig.secondary_motion.snapshot()
        check([state.chest_y,state.pendant_y,state.root_y] == sampled[0],str(fps)+"Hz caller equals 120Hz integration at1s")
        advance(2.0,fps);state = rig.secondary_motion.snapshot()
        check([state.chest_y,state.pendant_y,state.root_y] == sampled[1],str(fps)+"Hz caller equals 120Hz integration at3s")
    rig.apply_body_controls({"reset":true})
    check(meshes_at_rest(),"body reset cancels all deformation immediately")
    check(rig.secondary_motion.chest_velocity == 0.0 and rig.secondary_motion.pendant_velocity == 0.0,"body reset clears spring velocity")
    rig.apply_body_controls({"frame_y":1.0});rig.advance_secondary_motion(1.0/120.0)
    check(absf(rig.secondary_motion.chest_y) > 0.01,"live frame_y command drives secondary response without demo")
    rig.apply_body_controls({"reset":true,"frame_y":0.5});rig.advance_secondary_motion(1.0/120.0)
    check(meshes_at_rest(),"reset with frame reposition suppresses teleport impulse")
    rig.play_bounce_demo();advance(1.0)
    rig.reset()
    check(meshes_at_rest() and rig.get_body_state().joints == neutral_joints,"global reset cancels bounce and restores exact neutral")
    check(rig.expression_rig.face.snapshot() == neutral_face,"global reset retains face behavior")
    rig.play_bounce_demo();advance(0.8)
    rig.play_bounce_demo();advance(1.0)
    var restarted:Dictionary = rig.secondary_motion.snapshot()
    check([restarted.chest_y,restarted.pendant_y,restarted.root_y] == sampled[0],"repeated demo clicks restart deterministically")
    var before:Dictionary = rig.secondary_motion.snapshot()
    check(not rig.advance_secondary_motion(-1.0) and not rig.advance_secondary_motion(NAN),"negative and nonfinite simulation delta rejected")
    check(rig.secondary_motion.snapshot() == before,"invalid delta does not partially mutate state")
    var result = {"status":"PASS" if failures.is_empty() else "FAIL","checks":checks,"failures":failures,"peak_chest_spring_px":peak_chest,"peak_pendant_px":peak_pendant,"peak_root_px":peak_root,"scope":"Focused actual Godot 4.6.3 ownership, fixed-step spring response, live frame input, resets, caller-rate parity and mesh topology. Not native visual validation or a full regression suite."}
    var file = FileAccess.open("res://full_body/review/bounce_checks.json",FileAccess.WRITE)
    file.store_string(JSON.stringify(result,"  "));file.close();print(JSON.stringify(result));quit(0 if failures.is_empty() else 1)

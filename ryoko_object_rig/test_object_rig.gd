extends SceneTree
const Limits=preload("res://control_limits.gd")
var checks=0
var failed=0
var rig
func check(value:bool,label:String):
    checks+=1
    if not value:failed+=1;push_error("OBJECT_BASE_TEST "+label)
func _initialize():call_deferred("run")
func run():
    rig=load("res://object_rig.tscn").instantiate();root.add_child(rig)
    await process_frame;rig.set_process(false)
    var expected_objects=rig.face.manifest.objects.size()-5+1+rig.face.oral_objects.size()
    check(rig.apply_controls({"reset":true}),"reset")
    expected_objects+=rig.face.smile_lip_joints.size()+rig.face.smile_eye_joints.size()+rig.face.smile_lip_continuations.size()+rig.face.smile_manifest.residue_objects.size()
    check(rig.face.objects.size()==expected_objects,"manifest-declared independently owned sprites including dormant oral nodes")
    var iris=rig.face.objects.iris_screen_left.texture
    var backing=rig.face.objects.stationary_backing.texture
    for i in range(101):
        var v=i/100.0
        check(rig.apply_controls({"blink":v,"brow_screen_left":v,"brow_tilt_screen_right":-v,"hair_sway":(2.0*v-1.0)*rig.MAX_HAIR_SWAY,"gaze_x":0.0}),"base continuous parameter sample")
        for key in rig.face.objects:
            var node=rig.face.objects[key];var pivot=rig.face.homes[key].node
            check(node.modulate.a==1.0,"no opacity fade "+key)
            check(node.scale==Vector2.ONE and pivot.scale==Vector2.ONE,"no shape scale "+key)
        check(rig.face.objects.iris_screen_left.texture==iris,"constant iris artwork")
        check(rig.face.objects.stationary_backing.texture==backing,"constant clean face artwork")
        check(rig.face.homes.stationary_backing.node.position==Vector2(568,720) and rig.face.homes.stationary_backing.node.rotation==0,"face stays fixed")
        check(rig.face.mouth_variant=="neutral_lips","authored neutral lips retained")
        check(rig.face.objects.neutral_lips.visible and not rig.face.mouth_sprite.visible,"one neutral mouth owner")
    check(rig.apply_controls({"reset":true,"blink_R":0.35,"brow_screen_left":1,"mouth":"E"}),"independent channels")
    check(rig.face.closure==Vector2(.35,0),"independent eyelid")
    check(rig.face.homes.iris_screen_left.node.position==rig.face.homes.iris_screen_left.pivot,"zero gaze preserves canonical iris registration")
    check(rig.face.homes.brow_screen_right.node.rotation==0,"independent brow")
    for shape in ["A","E","I","O","U"]:
        check(rig.apply_controls({"mouth":shape}),"source viseme "+shape)
        check(rig.face.mouth_variant=="viseme_"+shape,"exclusive source variant "+shape)
        check(rig.face.objects.size()==expected_objects,"no duplicate object on swaps")
    check(rig.apply_controls({"mouth":"REST"}),"release mouth")
    check(rig.face.mouth_opening==0 and rig.face.mouth_variant=="neutral_lips","authored neutral oral object")
    for amount in [-rig.MAX_HAIR_SWAY,rig.MAX_HAIR_SWAY]:
        check(rig.apply_controls({"hair_sway":amount}),"supported hair endpoint accepted")
        check(is_equal_approx(rig.face.hair_sway,amount),"hair endpoint preserves requested coordinate")
    for x in [Limits.GAZE_MIN,0.0,Limits.GAZE_MAX]:
        for y in [Limits.GAZE_MIN,0.0,Limits.GAZE_MAX]:
            check(rig.apply_controls({"gaze_x":x,"gaze_y":y}),"base gaze contract corner")
            check(rig.manual_gaze==Vector2(x,y),"base preserves normalized gaze")
    var saved=rig.face.snapshot()
    for data in [{"perform_expression":"EXP-163"},{"expression":"EXP-005"},{"head_tilt":0.1},{"mouth_open":0.5},{"gaze_x":2},{"gaze_x":Limits.GAZE_MAX+.001},{"gaze_y":Limits.GAZE_MIN-.001},{"hair_sway":rig.MAX_HAIR_SWAY+0.000001},{"hair_sway":-rig.MAX_HAIR_SWAY-0.000001},{"hair_sway":1},{"reset":true,"hair_sway":-1},{"blink":0.8,"hair_sway":0.071},{"hair_sway":NAN},{"hair_sway":"yes"},{"auto_blink":"yes"},{"mouth":"bad"}]:
        check(not rig.apply_controls(data),"unsupported/invalid channel rejected")
        check(rig.face.snapshot()==saved,"rejection is atomic")
    for id in JSON.parse_string(FileAccess.get_file_as_string("res://legacy_expression_ids.json")).legacy_expression_ids:
        check(not rig.apply_controls({"expression":id}),"no emotion fallback "+id)
    check(rig.apply_controls({"reset":true,"auto_blink":true}),"auto blink")
    rig._process(4.0);check(rig.face.closure.x>0,"auto blink uses shared aperture")
    check(rig.apply_controls({"reset":true}),"reset after interruption")
    check(rig.face.closure==Vector2.ZERO and rig.face.gaze==Vector2.ZERO and rig.face.brow==Vector2.ZERO and rig.face.hair_sway==0 and rig.face.mouth_opening==0,"all base controls release")
    print("OBJECT_BASE_CHECKS_", "PASS" if failed==0 else "FAIL", " checks=",checks," failures=",failed)
    quit(0 if failed==0 else 1)

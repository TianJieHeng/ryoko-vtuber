extends Node2D
## Additive full-body cutout assembly. The approved face player remains unchanged.
## Bone2D nodes are rigid image owners, not a mesh-deformation or action system.
const REGISTRATION_PATH = "res://full_body/registration.json"
const FRAME_LIMITS = {"frame_x":18.0, "frame_y":10.0, "frame_roll":2.0}
var registration:Dictionary = {}
var expression_rig
var frame:Node2D
var skeleton:Skeleton2D
var joints:Dictionary = {}
var joint_homes:Dictionary = {}
var layer_nodes:Dictionary = {}
var body_controls:Dictionary = {}
var body_control_joints:Dictionary = {}
var ready_for_controls = false
var last_error = ""
var show_bones = false
var frame_pivot = Vector2.ZERO
var bone_overlay:Node2D

func _ready():
    var decoded = JSON.parse_string(FileAccess.get_file_as_string(REGISTRATION_PATH))
    if not decoded is Dictionary:
        _fail("Full-body registration is missing or invalid");return
    registration = decoded
    expression_rig = preload("res://expression_rig.gd").new()
    expression_rig.name = "ApprovedExpressionController"
    add_child(expression_rig)
    expression_rig.set_process_unhandled_key_input(false)
    expression_rig.hud.hide();expression_rig.hint.hide();expression_rig.pose_status.hide()
    if not expression_rig.rig_ready or not expression_rig.registry_ready:
        _fail(expression_rig.last_error);return
    # No face texture, channel, timeline or shader is replaced.
    expression_rig.body.hide()
    frame = Node2D.new();frame.name = "FrameTransform";add_child(frame)
    skeleton = Skeleton2D.new();skeleton.name = "CutoutSkeleton";frame.add_child(skeleton)
    for spec in registration.joints:
        var id:String = spec.id
        var bone = Bone2D.new();bone.name = id
        var absolute = _v(spec.position)
        var parent_id:String = spec.get("parent", "")
        if parent_id != "" and not joints.has(parent_id):
            _fail("Joint parent must precede child: " + id);return
        var parent_node = joints[parent_id] if parent_id != "" else skeleton
        var parent_home:Vector2 = joint_homes[parent_id] if parent_id != "" else Vector2.ZERO
        bone.position = absolute - parent_home
        bone.rest = Transform2D(0, bone.position)
        bone.set_autocalculate_length_and_angle(false)
        bone.length = float(spec.get("display_length", 35.0))
        parent_node.add_child(bone)
        joints[id] = bone;joint_homes[id] = absolute
        if spec.has("control") and spec.control != "":
            body_control_joints[spec.control] = spec
            body_controls[spec.control] = 0.0
    for key in FRAME_LIMITS:body_controls[key] = 0.0
    frame_pivot = _v(registration.get("frame_pivot", registration.joints[0].position))
    for spec in registration.layers:
        if not joints.has(spec.parent):
            _fail("Unknown layer parent: " + str(spec.parent));return
        var texture = load(spec.file)
        if not texture is Texture2D:
            _fail("Layer texture unavailable: " + str(spec.file));return
        var sprite = Sprite2D.new();sprite.name = spec.id;sprite.texture = texture
        sprite.centered = false;sprite.position = _v(spec.position) - joint_homes[spec.parent]
        sprite.scale = _v(spec.get("scale", [1,1]))
        sprite.z_index = int(spec.z);sprite.z_as_relative = false
        joints[spec.parent].add_child(sprite);layer_nodes[spec.id] = sprite
    var binding:Dictionary = registration.head_binding
    if not joints.has(binding.parent):_fail("Head attachment is missing");return
    # Reparent the existing live head, with all independent native owners intact.
    expression_rig.head.reparent(joints[binding.parent], false)
    expression_rig.head.position = _v(binding.position) - joint_homes[binding.parent]
    expression_rig.head.scale = Vector2.ONE * float(binding.scale)
    expression_rig.head.rotation = 0
    expression_rig.head.z_index = int(binding.get("z", 0))
    expression_rig.head.z_as_relative = false
    bone_overlay = Node2D.new();bone_overlay.name = "BoneOverlay";bone_overlay.z_index = 4000
    add_child(bone_overlay);bone_overlay.draw.connect(_draw_bones)
    ready_for_controls = true
    _write_body_pose()

func _v(pair)->Vector2:return Vector2(float(pair[0]), float(pair[1]))
func _fail(message:String):
    last_error = message;push_error(message);ready_for_controls = false

func apply_body_controls(data)->bool:
    if not ready_for_controls:last_error = "Full-body assembly unavailable";return false
    if not data is Dictionary:last_error = "Body controls must be a dictionary";return false
    # Validate the whole request before modifying any bone.
    for key in data:
        if key == "reset":
            if not data[key] is bool:last_error = "reset must be boolean";return false
        elif not body_controls.has(key):last_error = "Unknown body control: " + str(key);return false
        elif not (data[key] is float or data[key] is int) or not is_finite(float(data[key])) or absf(float(data[key])) > 1.0:
            last_error = "Body control must be finite in [-1,1]: " + str(key);return false
    if data.get("reset", false):
        for key in body_controls:body_controls[key] = 0.0
    for key in data:
        if key != "reset":body_controls[key] = float(data[key])
    _write_body_pose();last_error = "";return true

func _write_body_pose():
    frame.position = frame_pivot + Vector2(body_controls.frame_x * FRAME_LIMITS.frame_x, body_controls.frame_y * FRAME_LIMITS.frame_y)
    frame.rotation = deg_to_rad(body_controls.frame_roll * FRAME_LIMITS.frame_roll)
    skeleton.position = -frame_pivot
    for control in body_control_joints:
        var spec:Dictionary = body_control_joints[control]
        var value:float = body_controls[control]
        var limits:Array = spec.range_degrees
        joints[spec.id].rotation = deg_to_rad(value * (float(limits[1]) if value >= 0 else -float(limits[0])))
    if bone_overlay != null:bone_overlay.queue_redraw()

func apply_controls(data)->bool:
    # Face commands use the approved controller's validator and ownership exactly.
    if expression_rig == null:last_error = "Expression controller unavailable";return false
    var ok:bool = expression_rig.apply_controls(data)
    last_error = expression_rig.last_error
    if ok and data is Dictionary and data.get("reset", false):apply_body_controls({"reset":true})
    return ok

func reset()->bool:return apply_controls({"reset":true})
func play_expression(id)->bool:return apply_controls({"perform_expression":id})
func list_expressions()->Array:return expression_rig.list_expressions() if expression_rig != null else []
func get_body_state()->Dictionary:
    var transforms = {}
    for id in joints:
        var point:Vector2 = to_local(joints[id].global_position)
        transforms[id] = {"position":[point.x,point.y], "rotation_degrees":rad_to_deg(joints[id].rotation)}
    return {"ready":ready_for_controls,"controls":body_controls.duplicate(true),"joints":transforms,"last_error":last_error,"approval":"unapproved wiring review"}
func get_state()->Dictionary:
    var state:Dictionary = expression_rig.get_state() if expression_rig != null else {}
    state["body"] = get_body_state();return state
func set_bone_overlay(enabled:bool):
    show_bones = enabled
    if bone_overlay != null:bone_overlay.queue_redraw()
func _draw_bones():
    if not show_bones or not ready_for_controls:return
    for spec in registration.joints:
        var point = to_local(joints[spec.id].global_position)
        var parent_id:String = spec.get("parent", "")
        if parent_id != "":bone_overlay.draw_line(to_local(joints[parent_id].global_position),point,Color(0.2,0.95,0.85,0.8),2.5,true)
        bone_overlay.draw_circle(point,4.5,Color(1.0,0.76,0.25,0.95))

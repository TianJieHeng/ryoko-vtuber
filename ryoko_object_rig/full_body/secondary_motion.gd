extends RefCounted
## Small, acceleration-driven secondary motion. Textures and bind transforms are unchanged.
## Simulation units are the registration canvas pixels, independent of viewer zoom.
const STEP = 1.0 / 120.0
const CHEST_HZ = 2.9
const CHEST_DAMPING = 0.22
const CHEST_INERTIA = 1.1
const PENDANT_HZ = 3.5
const PENDANT_DAMPING = 0.24
const PENDANT_INERTIA = 0.9
const CHEST_LIMIT = 10.0
const PENDANT_LIMIT = 6.0
const MESH_LAYERS = ["blouse", "blazer_R", "blazer_L", "neck_skin", "necklace_chain"]
const PULSES = [[0.65, 0.8, 20.0], [2.35, 0.66, 14.0]]
var meshes:Dictionary = {}
var pendant:Node2D
var pendant_home = Vector2.ZERO
var accumulator = 0.0
var elapsed = 0.0
var demo_active = false
var root_y = 0.0
var root_acceleration = 0.0
var chest_y = 0.0
var chest_velocity = 0.0
var pendant_y = 0.0
var pendant_velocity = 0.0
var external_y = 0.0
var external_velocity = 0.0
var last_external_y = 0.0

func is_mesh_layer(id:String)->bool:return id in MESH_LAYERS

func create_mesh(id:String, texture:Texture2D, bind:Transform2D, parent_home:Vector2)->Polygon2D:
    var node = Polygon2D.new()
    node.texture = texture
    var size = texture.get_size()
    # Fine chain topology; the larger cloth grid is at most 20 canvas pixels apart.
    var spacing = 4.0 if id == "necklace_chain" else 20.0
    var nx = maxi(1, int(ceil(size.x * bind.x.length() / spacing)))
    var ny = maxi(1, int(ceil(size.y * bind.y.length() / spacing)))
    var vertices = PackedVector2Array()
    var weights = PackedFloat32Array()
    for row in range(ny + 1):
        for col in range(nx + 1):
            var vertex = Vector2(size.x * col / nx, size.y * row / ny)
            vertices.append(vertex)
            var canvas_point = parent_home + bind * vertex
            weights.append(chain_weight(canvas_point) if id == "necklace_chain" else cloth_weight(canvas_point))
    var triangles:Array[PackedInt32Array] = []
    for row in range(ny):
        for col in range(nx):
            var a = row * (nx + 1) + col
            var b = a + 1
            var c = a + nx + 1
            var d = c + 1
            triangles.append(PackedInt32Array([a, b, d]))
            triangles.append(PackedInt32Array([a, d, c]))
    node.polygon = vertices
    node.uv = vertices
    node.polygons = triangles
    meshes[id] = {"node":node, "rest":vertices, "weights":weights, "inverse_bind":bind.affine_inverse(), "triangles":triangles}
    return node

static func cloth_weight(point:Vector2)->float:
    # One shared C1 field across the skin/blouse/blazer owners. No rigid chest plates.
    # Shoulders and waist stay pinned. The V neckline is also pinned, rather than
    # pulling a garment edge away from its skin owner.
    var x = (point.x - 512.0) / 120.0
    if absf(x) >= 1.0:return 0.0
    var sides = pow(1.0 - x * x, 2.0)
    var vertical = smoothstep(330.0, 375.0, point.y) * (1.0 - smoothstep(430.0, 500.0, point.y))
    var neckline = smoothstep(2.0, 20.0, absf(point.x - 512.0) + 0.5 * (point.y - 390.0))
    return sides * vertical * neckline

static func chain_weight(point:Vector2)->float:
    # Both upper ends remain attached. The lowest chain follows the pendant.
    return smoothstep(282.0, 317.0, point.y)

func bind_pendant(node:Node2D):
    pendant = node
    pendant_home = node.position

func reset(base_y:float = 0.0):
    accumulator = 0.0;elapsed = 0.0;demo_active = false
    root_y = 0.0;root_acceleration = 0.0
    chest_y = 0.0;chest_velocity = 0.0
    pendant_y = 0.0;pendant_velocity = 0.0
    external_y = base_y;last_external_y = base_y;external_velocity = 0.0
    apply_deformation()

func start_demo(base_y:float = 0.0):
    reset(base_y)
    demo_active = true

func advance(delta:float, base_y:float)->bool:
    if not is_finite(delta) or delta < 0.0:return false
    # Catch up by fixed steps, so 30/60/120-Hz callers sample the same trajectory.
    accumulator += delta
    external_y = base_y
    while accumulator + 0.000000001 >= STEP:
        _step()
        accumulator -= STEP
    if absf(accumulator) < 0.000000001:accumulator = 0.0
    apply_deformation()
    return true

func _step():
    var midpoint = elapsed + STEP * 0.5
    var acceleration = _driver(midpoint).y if demo_active else 0.0
    var velocity = (external_y - last_external_y) / STEP
    # Manual frame edits have bounded inertia instead of an unbounded teleport impulse.
    acceleration += clampf((velocity - external_velocity) / STEP, -1800.0, 1800.0)
    last_external_y = external_y;external_velocity = velocity
    var chest_omega = TAU * CHEST_HZ
    chest_velocity += (-chest_omega * chest_omega * chest_y - 2.0 * CHEST_DAMPING * chest_omega * chest_velocity - CHEST_INERTIA * acceleration) * STEP
    chest_y += chest_velocity * STEP
    if absf(chest_y) > CHEST_LIMIT:
        chest_y = clampf(chest_y, -CHEST_LIMIT, CHEST_LIMIT)
        if chest_y * chest_velocity > 0.0:chest_velocity = 0.0
    var pendant_omega = TAU * PENDANT_HZ
    pendant_velocity += (-pendant_omega * pendant_omega * pendant_y - 2.0 * PENDANT_DAMPING * pendant_omega * pendant_velocity - PENDANT_INERTIA * acceleration) * STEP
    pendant_y += pendant_velocity * STEP
    if absf(pendant_y) > PENDANT_LIMIT:
        pendant_y = clampf(pendant_y, -PENDANT_LIMIT, PENDANT_LIMIT)
        if pendant_y * pendant_velocity > 0.0:pendant_velocity = 0.0
    elapsed += STEP
    var driver = _driver(elapsed) if demo_active else Vector2.ZERO
    root_y = driver.x;root_acceleration = driver.y
    # No idle breathing/wobble. Explicitly sleep only once both spring residuals are tiny.
    if acceleration == 0.0 and absf(chest_y) < 0.0001 and absf(chest_velocity) < 0.002:
        chest_y = 0.0;chest_velocity = 0.0
    if acceleration == 0.0 and absf(pendant_y) < 0.0001 and absf(pendant_velocity) < 0.002:
        pendant_y = 0.0;pendant_velocity = 0.0
    if demo_active and elapsed >= 3.01 and chest_y == 0.0 and pendant_y == 0.0:demo_active = false

func _driver(time:float)->Vector2:
    for pulse in PULSES:
        var start:float = pulse[0]
        var duration:float = pulse[1]
        var height:float = pulse[2]
        var u = (time - start) / duration
        if u > 0.0 and u < 1.0:
            var s = sin(PI * u)
            var c = cos(PI * u)
            var omega = PI / duration
            # sin^4 displacement has zero displacement, velocity AND acceleration
            # at its ends. The spring receives actual analytic acceleration, not a pose curve.
            return Vector2(-height * pow(s, 4.0), -height * omega * omega * (12.0 * s * s * c * c - 4.0 * pow(s, 4.0)))
    return Vector2.ZERO

func apply_deformation():
    for id in meshes:
        var spec:Dictionary = meshes[id]
        var rest:PackedVector2Array = spec.rest
        var amount = pendant_y if id == "necklace_chain" else chest_y
        if amount == 0.0:
            spec.node.polygon = rest
            continue
        var vertices = rest.duplicate()
        var inverse:Transform2D = spec.inverse_bind
        for i in range(vertices.size()):
            # Transform only the displacement vector; do not translate it by inverse origin.
            vertices[i] += inverse.basis_xform(Vector2(0.0, amount * spec.weights[i]))
        spec.node.polygon = vertices
    if pendant != null:pendant.position = pendant_home + Vector2(0.0, pendant_y)

func phase()->String:
    if not demo_active:
        if chest_y != 0.0 or pendant_y != 0.0:return "Live frame motion / secondary spring response"
        return "Settled / exact neutral" if elapsed >= 3.01 else "Neutral / springs at rest"
    if elapsed < 0.65:return "Neutral / springs at rest"
    if elapsed < 1.45:return "Small bounce / inertia-driven cloth"
    if elapsed < 2.35:return "First landing / spring follow-through"
    if elapsed < 3.01:return "Smaller bounce / pendant follow-through"
    if chest_y != 0.0 or pendant_y != 0.0:return "Damped settling / no driven body motion"
    return "Settled / exact neutral"

func snapshot()->Dictionary:
    return {"step_hz":120, "elapsed":elapsed, "demo_active":demo_active, "root_y":root_y, "root_acceleration":root_acceleration, "chest_y":chest_y, "chest_velocity":chest_velocity, "pendant_y":pendant_y, "pendant_velocity":pendant_velocity, "phase":phase()}

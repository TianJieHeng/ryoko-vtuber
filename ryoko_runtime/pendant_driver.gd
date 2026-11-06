extends RefCounted
# Short necklace pendant. Only attachment acceleration creates a transient sway.
# All angles are relative to its original source-canvas orientation.
const LENGTH=32.0
const FREQUENCY=13.0
const DAMPING=0.76
const SWING_LIMIT=deg_to_rad(6.0)
const RELATIVE_LIMIT=deg_to_rad(10.0)
const VERTICAL_FOLLOW=0.8
const ANCHOR_LIMIT=1000000.0
const SPEED_LIMIT=720.0
var enabled=true
var angle=0.0
var swing=0.0
var velocity=0.0
var previous_anchor=Vector2.ZERO
var previous_velocity=Vector2.ZERO
var initialized=false

func reset():
    angle=0.0;swing=0.0;velocity=0.0
    previous_anchor=Vector2.ZERO;previous_velocity=Vector2.ZERO;initialized=false

func step(anchor:Vector2,frame_angle:float,delta:float):
    if not anchor.is_finite() or not is_finite(frame_angle) or not is_finite(delta) or delta<=0:return
    if not enabled:reset();return
    if not is_finite(angle) or not is_finite(swing) or not is_finite(velocity) or not previous_anchor.is_finite() or not previous_velocity.is_finite():reset()
    var dt=clamp(delta,0.000001,0.1)
    # Limit finite but extreme caller values before any subtraction/division.
    anchor=anchor.clamp(Vector2(-ANCHOR_LIMIT,-ANCHOR_LIMIT),Vector2(ANCHOR_LIMIT,ANCHOR_LIMIT))
    frame_angle=clamp(frame_angle,-RELATIVE_LIMIT,RELATIVE_LIMIT)
    if not initialized:
        previous_anchor=anchor;previous_velocity=Vector2.ZERO;initialized=true
    else:
        var anchor_velocity=((anchor-previous_anchor)/dt).clamp(Vector2(-SPEED_LIMIT,-SPEED_LIMIT),Vector2(SPEED_LIMIT,SPEED_LIMIT))
        var acceleration_impulse=anchor_velocity-previous_velocity
        # Vertical acceleration affects a displaced/tilted pendant, but a pure
        # vertical lift of an exactly vertical pendant must not invent a swing.
        var hanging_angle=swing+frame_angle*(1.0-VERTICAL_FOLLOW)
        var tangent=Vector2(cos(hanging_angle),sin(hanging_angle))
        velocity-=clamp(acceleration_impulse.dot(tangent)/LENGTH,-2.0,2.0)*0.45
        previous_velocity=anchor_velocity;previous_anchor=anchor
    var count=maxi(1,int(ceil(dt*240.0)))
    var h=dt/count
    for i in range(count):
        velocity+=(-FREQUENCY*FREQUENCY*sin(swing)-2.0*DAMPING*FREQUENCY*velocity)*h
        swing+=velocity*h
        if abs(swing)>SWING_LIMIT:
            swing=clamp(swing,-SWING_LIMIT,SWING_LIMIT)
            if velocity*swing>0:velocity=0.0
    if abs(swing)<.00001 and abs(velocity)<.0001:swing=0.0;velocity=0.0
    angle=clamp(swing-frame_angle*VERTICAL_FOLLOW,-RELATIVE_LIMIT,RELATIVE_LIMIT)

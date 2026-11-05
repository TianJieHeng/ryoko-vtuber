extends RefCounted
# Rigid pendant about a fixed ear attachment. No procedural idle swing.
const LENGTH=135.0
const FREQUENCY=8.5
const DAMPING=0.64
const SWING_LIMIT=deg_to_rad(6.0)
const RELATIVE_LIMIT=deg_to_rad(15.0)
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
    if not anchor.is_finite() or not is_finite(frame_angle) or not is_finite(delta):return
    if not enabled:reset();return
    if delta<=0:return
    var dt=min(delta,0.1)
    if not initialized:
        previous_anchor=anchor;previous_velocity=Vector2.ZERO;initialized=true
    else:
        var anchor_velocity=(anchor-previous_anchor)/dt
        var impulse=clamp((anchor_velocity-previous_velocity).x/LENGTH,-3.0,3.0)
        velocity-=impulse*0.6
        previous_velocity=anchor_velocity;previous_anchor=anchor
    var n=maxi(1,int(ceil(dt*240.0)))
    var h=dt/n
    for i in range(n):
        velocity+=(-FREQUENCY*FREQUENCY*sin(swing)-2.0*DAMPING*FREQUENCY*velocity)*h
        swing+=velocity*h
        if abs(swing)>SWING_LIMIT:
            swing=clamp(swing,-SWING_LIMIT,SWING_LIMIT)
            if velocity*swing>0:velocity=0.0
    if abs(swing)<.00001 and abs(velocity)<.0001:swing=0.0;velocity=0.0
    angle=clamp(swing-frame_angle,-RELATIVE_LIMIT,RELATIVE_LIMIT)

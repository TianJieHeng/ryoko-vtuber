extends RefCounted
# Rigid hanging hairpin ornament. Angle is relative to the moving head frame.
# Gravity keeps it vertical, while anchor acceleration drives a bounded swing.
const PIVOT=Vector2(790.5,184.0)
const SOURCE_RECT=Rect2(781,184,22,131)
const LENGTH=126.0
const FREQUENCY=7.0
const DAMPING=0.52
const SWING_LIMIT=deg_to_rad(9.0)
const RELATIVE_LIMIT=deg_to_rad(14.0)
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
    if not enabled:
        reset();return
    if delta<=0:return
    var dt=min(delta,0.1)
    if not initialized:
        previous_anchor=anchor;previous_velocity=Vector2.ZERO;initialized=true
    else:
        var anchor_velocity=(anchor-previous_anchor)/dt
        # Bound impulses from frame stalls or discontinuous external controls.
        var impulse=clamp((anchor_velocity-previous_velocity).x/LENGTH,-4.0,4.0)
        velocity-=impulse*0.7
        previous_velocity=anchor_velocity
        previous_anchor=anchor
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

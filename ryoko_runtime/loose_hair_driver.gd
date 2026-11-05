extends RefCounted
# Existing outer hair tips, not separate strands. No idle oscillator.
const LIMIT=10.0
const FREQUENCY=10.0
const DAMPING=0.68
var enabled=true
var offset=Vector2.ZERO
var velocity=Vector2.ZERO
var previous_anchor=Vector2.ZERO
var initialized=false
func reset():
    offset=Vector2.ZERO;velocity=Vector2.ZERO;previous_anchor=Vector2.ZERO;initialized=false
func weight(rest:Vector2,side:String)->float:
    var lower=smoothstep(600.0,690.0,rest.y)*(1.0-smoothstep(750.0,795.0,rest.y))
    return lower*((1.0-smoothstep(335.0,390.0,rest.x)) if side=="screen_left" else smoothstep(746.0,790.0,rest.x))
func step(anchor:Vector2,delta:float):
    if not anchor.is_finite() or not is_finite(delta) or delta<=0:return
    if not enabled:reset();return
    if not initialized:
        previous_anchor=anchor;initialized=true;return
    var dt=min(delta,.1)
    var motion=anchor-previous_anchor
    previous_anchor=anchor
    offset-=Vector2(motion.x,motion.y*.35)*.8
    offset=offset.limit_length(LIMIT)
    var n=maxi(1,int(ceil(dt*240.0)))
    var h=dt/n
    for i in range(n):
        velocity+=(-FREQUENCY*FREQUENCY*offset-2.0*DAMPING*FREQUENCY*velocity)*h
        offset+=velocity*h
        if offset.length()>LIMIT:
            offset=offset.limit_length(LIMIT)
            var outward=velocity.dot(offset.normalized())
            if outward>0:velocity-=offset.normalized()*outward
    if offset.length()<.001 and velocity.length()<.01:offset=Vector2.ZERO;velocity=Vector2.ZERO

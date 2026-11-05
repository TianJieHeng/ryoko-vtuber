extends RefCounted
# Small inertial motion of the crown/bun; rooted above all facial eye assets.
var offset=Vector2.ZERO
var velocity=Vector2.ZERO
var previous_anchor=Vector2.ZERO
var initialized=false
var enabled=true
const LIMIT=8.0
const FREQUENCY=13.0
const DAMPING=0.66
func reset(anchor=Vector2.ZERO):
    offset=Vector2.ZERO;velocity=Vector2.ZERO;previous_anchor=anchor;initialized=false
func weight(rest:Vector2)->float:
    return 1.0-smoothstep(120.0,330.0,rest.y)
func step(anchor:Vector2,delta:float):
    if not initialized or not enabled:
        previous_anchor=anchor;offset=Vector2.ZERO;velocity=Vector2.ZERO;initialized=true;return
    var dt=clamp(delta,0.0,0.1)
    if dt<=0:return
    offset-=(anchor-previous_anchor)*0.8
    previous_anchor=anchor
    var n=max(1,int(ceil(dt/(1.0/120.0))))
    var h=dt/n
    for i in range(n):
        velocity+=(-FREQUENCY*FREQUENCY*offset-2.0*DAMPING*FREQUENCY*velocity)*h
        offset+=velocity*h
        if offset.length()>LIMIT:
            offset=offset.limit_length(LIMIT)
            var outward=velocity.dot(offset.normalized())
            if outward>0:velocity-=offset.normalized()*outward
    if offset.length()<.001 and velocity.length()<.01:offset=Vector2.ZERO;velocity=Vector2.ZERO

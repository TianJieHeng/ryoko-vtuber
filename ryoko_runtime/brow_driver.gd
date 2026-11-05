extends RefCounted
var target=Vector2.ZERO
var current=Vector2.ZERO
func axis(v):
    var value=float(v)
    return clamp(value,-1.0,1.0) if is_finite(value) else 0.0
func set_both(value):target=Vector2.ONE*axis(value)
func set_side(side,value):
    if side=="screen_left":target.x=axis(value)
    else:target.y=axis(value)
func reset():target=Vector2.ZERO;current=Vector2.ZERO
func step(delta):
    current=current.lerp(target,1.0-exp(-max(0.0,delta)/.15))
    if target==Vector2.ZERO and current.length()<.0001:current=Vector2.ZERO
func sample_pixel(p:Vector2,amount:float):return p+Vector2(0,axis(amount)*5.0)

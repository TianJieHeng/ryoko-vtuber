extends RefCounted
var target=Vector2.ZERO
var current=Vector2.ZERO
var mouse_follow=false
func axis(value):
    var v=float(value)
    return clamp(v,-1.0,1.0) if is_finite(v) else 0.0
func set_target(x,y):target=Vector2(axis(x),axis(y))
func reset():target=Vector2.ZERO;current=Vector2.ZERO;mouse_follow=false
func step(delta):current=current.lerp(target,1.0-exp(-max(0.0,delta)/0.12))
# Every iris texel uses exactly the same translation. No scale or warp.
func sample_pixel(p:Vector2,direction:Vector2):
    return p-direction*Vector2(7.0,2.0)

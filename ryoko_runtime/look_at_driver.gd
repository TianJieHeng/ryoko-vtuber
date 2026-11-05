extends RefCounted
# Opt-in stylized attention: eyes lead, head follows. No torso or art changes.
var target=Vector2.ZERO
var head=Vector3.ZERO
var eye=Vector2.ZERO
var active=false
var mouse_follow=false
var delay=0.0
func axis(v):
    return clamp(float(v),-1.0,1.0) if is_finite(float(v)) else 0.0
func aim(x,y):
    var next=Vector2(axis(x),axis(y))
    if not active or target.distance_to(next)>.55:delay=.18
    target=next;active=true
func release():
    active=false;mouse_follow=false;target=Vector2.ZERO;delay=0.0
func reset():
    release();head=Vector3.ZERO;eye=Vector2.ZERO
func step(delta):
    var dt=max(0.0,delta)
    var head_dt=dt
    if active and delay>0:
        head_dt=max(0.0,dt-delay)
        delay=max(0.0,delay-dt)
    var desired=Vector3(target.x*.18,target.x*.55,target.y*.35) if active else Vector3.ZERO
    head=head.lerp(desired,1.0-exp(-head_dt/.28))
    # Eyes remain directed at the target, easing toward center as head takes over.
    var desired_eye=(target-Vector2(head.y/.55,head.z/.35)*.35) if active else Vector2.ZERO
    eye=eye.lerp(desired_eye,1.0-exp(-dt/(.045 if active else .16)))
    if not active and head.length()<.0001 and eye.length()<.0001:
        head=Vector3.ZERO;eye=Vector2.ZERO

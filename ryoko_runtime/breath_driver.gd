extends RefCounted
# Optional controlled breathing. No automatic repeating oscillator.
var active=false
var elapsed=0.0
var strength=1.0
var manual=0.0
var amount=0.0
func finite_level(v):
    var f=float(v)
    return clamp(f,0.0,1.0) if is_finite(f) else 0.0
func trigger(level=1.0):
    strength=finite_level(level);elapsed=0.0;active=true;manual=0.0
func hold(level):active=false;manual=finite_level(level)
func cancel():active=false;manual=0.0
func reset():cancel();elapsed=0.0;amount=0.0
func step(delta):
    var dt=max(0.0,delta)
    var goal=manual
    if active:
        elapsed+=dt
        goal=smoothstep(0.0,2.0,elapsed)*(1.0-smoothstep(2.4,5.6,elapsed))*strength
        if elapsed>=6.0:active=false;goal=0.0
    amount=lerp(amount,goal,1.0-exp(-dt/.18))
    if not active and manual==0.0 and amount<.0001:amount=0.0
func offset(rest:Vector2):
    var lift=smoothstep(650.0,830.0,rest.y)*(1.0-smoothstep(1250.0,1384.0,rest.y))
    var ribs=smoothstep(850.0,1000.0,rest.y)*(1.0-smoothstep(1250.0,1384.0,rest.y))
    return Vector2((rest.x-568.0)*.012*ribs,-4.0*lift)*amount

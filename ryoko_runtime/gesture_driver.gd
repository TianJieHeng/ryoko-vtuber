extends RefCounted
# Finite additive gestures; leaves live control targets untouched.
var active=""
var elapsed=0.0
var strength=1.0
var head=Vector3.ZERO
var body=Vector3.ZERO
const DURATIONS={"acknowledge":1.35,"greet":2.2}
func trigger(id:String,intensity=1.0)->bool:
    if not DURATIONS.has(id):return false
    var value=float(intensity)
    strength=clamp(value,0.0,1.0) if is_finite(value) else 0.0
    active=id;elapsed=0.0;head=Vector3.ZERO;body=Vector3.ZERO
    return true
func cancel():
    active="";elapsed=0.0;head=Vector3.ZERO;body=Vector3.ZERO
func sample(delta:float):
    if active=="":return
    elapsed+=max(0.0,delta)
    var duration=float(DURATIONS[active])
    if elapsed>=duration:cancel();return
    var u=elapsed/duration
    # Smooth approach, brief hold, smooth release. No periodic oscillator.
    var amount=smoothstep(0.0,0.28,u)*(1.0-smoothstep(0.48,1.0,u))*strength
    if active=="acknowledge":
        head=Vector3(0.08,0,0.9)*amount
        body=Vector3(0,0,0.22)*amount
    else:
        head=Vector3(-0.55,-0.12,0.12)*amount
        body=Vector3(-0.3,-0.1,0)*amount

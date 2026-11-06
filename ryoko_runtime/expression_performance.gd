extends RefCounted
# Authored facial/body performance sampler. No tracking, randomness, or disk writes.
const AXES=["gaze_x","gaze_y","eye_left","eye_right","brow_left","brow_right","brow_tilt_left","brow_tilt_right","mouth_open","mouth_wide","mouth_curve","mouth_shift_x","mouth_shift_y","cheek_left","cheek_right","head_tilt","head_x","head_y","body_tilt","body_x","body_y"]
const LEVELS=["amount","effect_strength"]
const COMMANDS=["perform_expression","expression_strength","expression_speed","expression_loop","expression_paused","expression_cancel"]
var profiles={}
var active=false
var paused=false
var recovering=false
var id="neutral"
var elapsed=0.0
var strength=1.0
var speed=1.0
var looping=false
var phase="neutral"
var values={}
var pending={}
var release_from={}
var release_time=0.0
var release_duration=0.35
var error_message=""
func _init():values=zero()
static func zero()->Dictionary:
    var out={"amount":0.0,"effect_strength":1.0}
    for key in AXES:out[key]=0.0
    return out
static func number(v)->bool:return (v is float or v is int) and is_finite(float(v))
func load_data(data,registered:Array)->bool:
    if not data is Dictionary or data.get("version")!=1 or not data.get("profiles") is Dictionary:return false
    var next={}
    for key in data.profiles:
        var p=data.profiles[key]
        if not key in registered or not p is Dictionary or not p.get("name") is String:return false
        if not number(p.get("duration")) or p.duration<0.5 or p.duration>30:return false
        if not p.get("keyframes") is Array or p.keyframes.size()<3 or p.keyframes.size()>128:return false
        var last=-1.0
        for frame in p.keyframes:
            if not frame is Dictionary or not number(frame.get("time")) or frame.time<=last or frame.time>p.duration or not frame.get("values") is Dictionary:return false
            if not frame.get("phase","") is String:return false
            for channel in frame.values:
                var v=frame.values[channel]
                if channel not in AXES and channel not in LEVELS:return false
                if not number(v) or v>1 or v< (0 if channel in LEVELS else -1):return false
            last=frame.time
        if p.keyframes[0].time!=0 or not is_equal_approx(last,p.duration):return false
        for edge in [p.keyframes[0],p.keyframes[-1]]:
            for channel in AXES+["amount"]:
                if edge.values.get(channel,0)!=0:return false
        next[key]=p.duplicate(true)
    if next.is_empty():return false
    profiles=next;return true
func load_file(path:String,registered:Array)->bool:
    if not FileAccess.file_exists(path):return false
    return load_data(JSON.parse_string(FileAccess.get_file_as_string(path)),registered)
func valid_command(data:Dictionary)->bool:
    if data.has("perform_expression") and (not data.perform_expression is String or not profiles.has(data.perform_expression)):return false
    if data.has("expression_strength") and (not number(data.expression_strength) or data.expression_strength<0 or data.expression_strength>1):return false
    if data.has("expression_speed") and (not number(data.expression_speed) or data.expression_speed<0.25 or data.expression_speed>2):return false
    for key in ["expression_loop","expression_paused","expression_cancel"]:
        if data.has(key) and not data[key] is bool:return false
    # Options apply only to a new request; reject ambiguous silent no-ops.
    for key in ["expression_strength","expression_speed","expression_loop"]:
        if data.has(key) and not data.has("perform_expression"):return false
    return true
func play(request:Dictionary,existing_id:String="neutral"):
    var next={"id":request.perform_expression,"strength":float(request.get("expression_strength",1.0)),"speed":float(request.get("expression_speed",1.0)),"loop":request.get("expression_loop",false)}
    if active:
        pending=next
        if not recovering:cancel(false)
        paused=false
    elif existing_id!="neutral":
        id=existing_id;values=zero();values.amount=1.0;active=true
        pending=next;cancel(false)
    else:_begin(next)
func _begin(request:Dictionary):
    id=request.id;strength=request.strength;speed=request.speed;looping=request.loop
    active=true;paused=false;recovering=false;elapsed=0.0;values=zero();phase="neutral";pending={}
func cancel(clear_pending=true):
    if clear_pending:pending={}
    if not active:return
    if not recovering:
        release_from=values.duplicate(true);release_time=0.0;recovering=true
    paused=false;phase="recovery"
func reset():
    active=false;paused=false;recovering=false;id="neutral";elapsed=0.0;values=zero();phase="neutral";pending={}
func sample(profile:Dictionary,t:float)->Dictionary:
    var frames=profile.keyframes
    var out=zero()
    if t<=0:return out
    if t>=profile.duration:return out
    var a=frames[0];var b=frames[1]
    for n in range(1,frames.size()):
        if t<=frames[n].time:a=frames[n-1];b=frames[n];break
    var u=clamp((t-float(a.time))/(float(b.time)-float(a.time)),0.0,1.0)
    u=u*u*(3.0-2.0*u) # bounded C1 interpolation; no overshoot
    for key in out:
        var fallback=1.0 if key=="effect_strength" else 0.0
        out[key]=lerpf(float(a.values.get(key,fallback)),float(b.values.get(key,fallback)),u)
    return out
func step(delta:float):
    if not active or paused or not is_finite(delta) or delta<=0:return
    if recovering:
        release_time=min(release_duration,release_time+delta)
        var u=release_time/release_duration;u=u*u*(3.0-2.0*u)
        for key in values:
            var end=1.0 if key=="effect_strength" else 0.0
            values[key]=lerpf(float(release_from.get(key,end)),end,u)
        if release_time>=release_duration:
            if not pending.is_empty():_begin(pending.duplicate(true))
            else:reset()
        return
    var p=profiles[id]
    elapsed+=delta*speed
    if elapsed>=p.duration:
        if looping:elapsed=fmod(elapsed,float(p.duration))
        else:reset();return
    values=sample(p,elapsed)
    for key in values:
        if key!="effect_strength":values[key]*=strength
    phase="neutral"
    for frame in p.keyframes:
        if frame.time<=elapsed:phase=frame.get("phase","performance")
        else:break
func head()->Vector3:return Vector3(values.head_tilt,values.head_x,values.head_y)
func body()->Vector3:return Vector3(values.body_tilt,values.body_x,values.body_y)

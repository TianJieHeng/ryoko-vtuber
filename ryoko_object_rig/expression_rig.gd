extends "res://object_rig.gd"
## One reusable bounded control/timeline player. Expression identity comes only from data.
const Registry=preload("res://expression_registry.gd")
var registry=Registry.new()
var registry_ready=false
const RESTART_SECONDS=0.30
const RELEASE_SECONDS=0.45
const CHANNELS=["blink_R","blink_L","brow_screen_left","brow_screen_right","brow_tilt_screen_left","brow_tilt_screen_right","gaze_x","gaze_y","hair_sway","mouth_open","eye_smile_R","eye_smile_L","mouth_smile","mouth_spread"]
var active_performance=""
var performance_time=0.0
var performance_phase="neutral"
var release_time=-1.0
var current_pose:Dictionary={}
var restart_pose:Dictionary={}
var release_pose:Dictionary={}
var manual_mouth_open=0.0
var manual_eye_smile=Vector2.ZERO
var manual_mouth_smile=0.0
var manual_mouth_spread=0.0
var oral_mode="continuous"
var performance:Dictionary={} 
func _ready():
    registry_ready=registry.load_file()
    if not registry_ready:last_error=registry.last_error
    super._ready()
    if not rig_ready:registry_ready=false;return
    current_pose=neutral_pose();_apply_performance_pose(current_pose)
    hud.text="Ryoko / shared separate-part rig"
    hint.text="Space release · 0 reset"
func neutral_pose()->Dictionary:
    var p={}
    for key in CHANNELS:p[key]=0.0
    return p
func pose_now()->Dictionary:
    return {"blink_R":manual_lids.x,"blink_L":manual_lids.y,"brow_screen_left":manual_brow.x,"brow_screen_right":manual_brow.y,"brow_tilt_screen_left":manual_brow_tilt.x,"brow_tilt_screen_right":manual_brow_tilt.y,"gaze_x":manual_gaze.x,"gaze_y":manual_gaze.y,"hair_sway":float(manual_hair),"mouth_open":float(manual_mouth_open),"eye_smile_R":manual_eye_smile.x,"eye_smile_L":manual_eye_smile.y,"mouth_smile":float(manual_mouth_smile),"mouth_spread":float(manual_mouth_spread)}
func sample_expression(id,time)->Dictionary:
    if not id is String or not number(time):
        last_error="Expression ID must be a string and sample time a finite number";return {}
    var definition=registry.definition(id)
    if definition.is_empty():
        last_error="Unknown expression or nonfinite sample time";return {}
    return _sample(definition,time)
func _sample(definition:Dictionary,time:float)->Dictionary:
    var keys=definition.keyframes
    var p=neutral_pose()
    if time<=0:return p
    if time>=definition.duration:return p
    for i in range(keys.size()-1):
        var a=keys[i];var b=keys[i+1]
        if time>=a.time and time<=b.time:
            var u=clampf((time-a.time)/(b.time-a.time),0,1)
            u=u*u*(3-2*u)
            for key in CHANNELS:p[key]=lerpf(float(a.values.get(key,0)),float(b.values.get(key,0)),u)
            return p
    return p
func phase_at(time:float)->String:
    var phase="neutral"
    for k in performance.get("keyframes",[]):
        if time>=k.time:phase=k.phase
    return phase
func _apply_performance_pose(p:Dictionary):
    manual_lids=Vector2(p.blink_R,p.blink_L);manual_brow=Vector2(p.brow_screen_left,p.brow_screen_right)
    manual_brow_tilt=Vector2(p.brow_tilt_screen_left,p.brow_tilt_screen_right);manual_gaze=Vector2(p.gaze_x,p.gaze_y)
    manual_eye_smile=Vector2(p.get("eye_smile_R",0),p.get("eye_smile_L",0));manual_mouth_smile=p.get("mouth_smile",0);manual_mouth_spread=p.get("mouth_spread",0)
    manual_hair=p.hair_sway;manual_mouth_open=p.mouth_open;mouth_shape="neutral";oral_mode="continuous"
    current_pose=p.duplicate();_write_pose()
func _write_pose():
    if not face or not face.ready_for_controls:return
    super._write_pose()
    if oral_mode=="continuous":face.set_mouth_open(manual_mouth_open)
    face.set_smile_controls(manual_eye_smile,manual_mouth_smile,manual_mouth_spread)
    var owner=active_performance if active_performance!="" else ("release" if release_time>=0 else "manual")
    face.owners={"eyes":owner,"brows":owner,"mouth":owner,"hair":owner}
    hud.text="Ryoko / shared separate-part rig";hint.text="Space release · 0 reset"
    pose_status.text=(active_performance+" / " if active_performance!="" else "")+performance_phase
func apply_controls(data)->bool:
    if not data is Dictionary:last_error="Controls must be a dictionary";return false
    if not registry_ready:last_error="Registry unavailable: "+registry.last_error;return false
    if data.is_empty():last_error="";return true
    # Unapproved discrete source visemes can bypass the reference aperture cap.
    for shape_key in ["mouth","viseme"]:
        if data.has(shape_key) and (not data[shape_key] is String or data[shape_key].to_upper() not in ["REST","RELEASE","NEUTRAL"]):
            last_error="Discrete visemes are not supported by this bounded performance app; use mouth_open or REST";return false
    # Validate shared gaze bounds before any pose or ownership mutation.
    for gaze_key in ["gaze_x","gaze_y"]:
        if data.has(gaze_key) and not Limits.valid_gaze(data[gaze_key]):
            last_error="Gaze must be finite and within the advertised normalized bounds";return false
    # The flattened canonical hair has only a verified small reveal margin.
    if data.has("hair_sway") and (not number(data.hair_sway) or abs(float(data.hair_sway))>MAX_HAIR_SWAY):
        last_error="Canonical hair_sway supports only [-0.07,0.07]";return false
    # Validate the complete transaction before changing ownership or pose.
    var base=data.duplicate()
    for key in ["perform_expression","release_performance","mouth_open","eye_smile_R","eye_smile_L","mouth_smile","mouth_spread"]:base.erase(key)
    for key in base:
        if key not in NUMBERS and key not in ["reset","auto_blink","mouth","viseme"]:last_error="Unsupported control: "+str(key);return false
    for key in NUMBERS:
        if base.has(key) and (not number(base[key]) or abs(float(base[key]))>1 or (key in ["blink","blink_L","blink_R"] and base[key]<0)):
            last_error="Invalid numeric control: "+key;return false
    for key in ["reset","auto_blink"]:
        if base.has(key) and not base[key] is bool:last_error="Expected boolean: "+key;return false
    for key in ["mouth","viseme"]:
        if base.has(key) and (not base[key] is String or base[key].to_upper() not in ["A","E","I","O","U","REST","RELEASE","NEUTRAL"]):last_error="Invalid mouth shape";return false
    for key in ["eye_smile_R","eye_smile_L","mouth_smile","mouth_spread"]:
        if data.has(key) and (not number(data[key]) or data[key]<0 or data[key]>1):last_error=key+" must be in [0,1]";return false
    if data.has("mouth_open") and (not number(data.mouth_open) or data.mouth_open<0 or data.mouth_open>1):last_error="mouth_open must be in [0,1]";return false
    if data.has("perform_expression") and (not data.perform_expression is String or registry.resolve(data.perform_expression)==""):last_error="Unknown or unsupported expression ID";return false
    if data.has("release_performance") and not data.release_performance is bool:last_error="release_performance must be boolean";return false
    if data.has("perform_expression") and (data.size()!=1):last_error="Trigger is a separate atomic transaction";return false
    if data.has("release_performance") and (data.size()!=1):last_error="Release is a separate atomic transaction";return false
    if data.has("mouth_open") and (data.has("mouth") or data.has("viseme")):last_error="Mouth has one owner";return false
    if (data.has("perform_expression") or data.get("release_performance",false)) and oral_mode=="viseme":
        last_error="Release discrete viseme with REST before starting/releasing a continuous performance";return false
    if data.size()==1 and data.has("reset") and not data.reset:last_error="";return true
    if data.has("perform_expression"):
        restart_pose=displayed_pose();active_performance=registry.resolve(data.perform_expression)
        performance=registry.definition(active_performance);performance_time=0;release_time=-1;performance_phase=registry.trigger_phase(active_performance);auto_blink=false
        release_pose.clear();last_error=""
        _apply_performance_pose(restart_pose);return true
    if data.get("release_performance",false):
        release_pose=displayed_pose();active_performance="";release_time=0;performance_phase="interrupted_release";auto_blink=false
        last_error="";_apply_performance_pose(release_pose);return true
    if data.has("release_performance"):last_error="";return true
    if data.size()>0:
        active_performance="";release_time=-1;performance_phase="manual"
    if data.get("reset",false):
        manual_mouth_open=0;manual_eye_smile=Vector2.ZERO;manual_mouth_smile=0.0;manual_mouth_spread=0.0;oral_mode="continuous";performance_time=0;performance_phase="neutral"
        restart_pose.clear();release_pose.clear();performance.clear()
    if data.has("eye_smile_R"):manual_eye_smile.x=float(data.eye_smile_R)
    if data.has("eye_smile_L"):manual_eye_smile.y=float(data.eye_smile_L)
    if data.has("mouth_smile"):manual_mouth_smile=float(data.mouth_smile)
    if data.has("mouth_spread"):manual_mouth_spread=float(data.mouth_spread)
    if data.has("mouth_open"):manual_mouth_open=float(data.mouth_open);oral_mode="continuous"
    for key in ["mouth","viseme"]:
        if data.has(key):
            oral_mode="continuous" if data[key].to_upper() in ["REST","RELEASE","NEUTRAL"] else "viseme"
            if oral_mode=="continuous":manual_mouth_open=0
    var ok=super.apply_controls(base)
    current_pose=pose_now()
    if ok:last_error=""
    return ok
func _process(delta):advance(delta)
func advance(delta)->bool:
    if not number(delta) or delta<0:last_error="delta must be finite and nonnegative";return false
    if not rig_ready or not registry_ready:return false
    if active_performance!="":
        performance_time=minf(performance.duration,performance_time+delta)
        var p=_sample(performance,performance_time)
        # Retrigger from the displayed pose. These are control coordinates, never image opacity.
        if performance_time<RESTART_SECONDS:
            var u=smoothstep(0.0,RESTART_SECONDS,performance_time)
            for key in CHANNELS:p[key]=lerpf(restart_pose.get(key,0),p[key],u)
        performance_phase=phase_at(performance_time);_apply_performance_pose(p)
        if performance_time>=performance.duration:active_performance="";performance_phase="neutral_return";_apply_performance_pose(neutral_pose())
    elif release_time>=0:
        release_time+=delta;var u=smoothstep(0.0,RELEASE_SECONDS,release_time);var p=neutral_pose()
        for key in CHANNELS:p[key]=lerpf(release_pose[key],0,u)
        _apply_performance_pose(p)
        if release_time>=RELEASE_SECONDS:release_time=-1;performance_phase="neutral";_apply_performance_pose(neutral_pose())
    else:
        elapsed+=delta;_write_pose()
    return true
func _unhandled_key_input(event):
    if not event is InputEventKey or not event.pressed or event.echo:return
    if event.keycode==KEY_SPACE:apply_controls({"release_performance":true})
    else:super._unhandled_key_input(event)

func displayed_pose()->Dictionary:
    var p=pose_now()
    p.blink_R=face.closure.x;p.blink_L=face.closure.y
    return p
func list_expressions()->Array:return registry.list_expressions()
func play_expression(id)->bool:return apply_controls({"perform_expression":id})
func release()->bool:return apply_controls({"release_performance":true})
func reset()->bool:return apply_controls({"reset":true})
func get_state()->Dictionary:
    return {"registry_ready":registry_ready,"active_expression":active_performance,"time":performance_time,"phase":performance_phase,"release_time":release_time,"controls":pose_now(),"displayed_controls":displayed_pose(),"owners":face.owners.duplicate(),"auto_blink":auto_blink,"last_error":last_error}

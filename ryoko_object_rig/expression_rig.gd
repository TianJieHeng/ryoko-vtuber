extends "res://object_rig.gd"
## One reusable bounded control/timeline player. Expression identity comes only from data.
const Registry=preload("res://expression_registry.gd")
var registry=Registry.new()
var registry_ready=false
const RESTART_SECONDS=0.30
const RELEASE_SECONDS=0.45
const SCOPED_CHANNELS=["opening_px","aversion_px","uneasy_weight"]
var scoped_pose={"opening_px":0.0,"aversion_px":0.0,"uneasy_weight":0.0}
var scoped_parts
const CHANNELS=["opening_px","aversion_px","uneasy_weight","blink_R","blink_L","brow_screen_left","brow_screen_right","brow_tilt_screen_left","brow_tilt_screen_right","brow_inner_lift_screen_left","brow_inner_lift_screen_right","gaze_x","gaze_y","gaze_down_extra","hair_sway","mouth_open","eye_smile_R","eye_smile_L","mouth_smile","mouth_spread","mouth_corner_lift","mouth_corner_lift_screen_left","mouth_corner_lift_screen_right","mouth_width_screen_left","mouth_width_screen_right","mouth_lip_press","mouth_oral_lift","mouth_purse","mouth_kiss","blush_intensity"]
var active_performance=""
var performance_time=0.0
var performance_phase="neutral"
var release_time=-1.0
# Intent survives temporary suspension, never a later manual takeover.
var auto_blink_pending_restore=false
var current_pose:Dictionary={}
var restart_pose:Dictionary={}
var release_pose:Dictionary={}
const MOUTH_TRIO=["mouth_open","mouth_width_screen_left","mouth_width_screen_right","mouth_kiss"]
# Trigger-fixed lookahead; no mode change when a later target key opens.
const OPENING_CONFLICTS=["blink_L","blink_R","gaze_x","gaze_y","gaze_down_extra","eye_smile_L","eye_smile_R","aversion_px"]
var opening_bridge_active=false
var mouth_bridge_mode="none"
var mouth_bridge_duration=0.0
var manual_mouth_open=0.0
var manual_eye_smile=Vector2.ZERO
var manual_mouth_smile=0.0
var manual_mouth_spread=0.0
var manual_mouth_corner_lift=0.0
var manual_mouth_corner_sides=Vector2.ZERO
var manual_mouth_width_sides=Vector2.ZERO
var manual_mouth_lip_press=0.0
var manual_mouth_oral_lift=0.0
var manual_mouth_purse=0.0
var manual_mouth_kiss=0.0
var manual_blush_intensity=0.0
var oral_mode="continuous"
var performance:Dictionary={} 
func _ready():
    registry_ready=registry.load_file()
    if not registry_ready:last_error=registry.last_error
    super._ready()
    if not rig_ready:registry_ready=false;return
    scoped_parts=load("res://parts/caught_staring/components.gd").new();scoped_parts.setup(self)
    current_pose=neutral_pose();_apply_performance_pose(current_pose)
    hud.text="Ryoko / shared separate-part rig"
    hint.text="Space release · 0 reset"
func neutral_pose()->Dictionary:
    var p={}
    for key in CHANNELS:p[key]=0.0
    return p
func pose_now()->Dictionary:
    return {"opening_px":scoped_pose.opening_px,"aversion_px":scoped_pose.aversion_px,"uneasy_weight":scoped_pose.uneasy_weight,"blink_R":manual_lids.x,"blink_L":manual_lids.y,"brow_screen_left":manual_brow.x,"brow_screen_right":manual_brow.y,"brow_tilt_screen_left":manual_brow_tilt.x,"brow_tilt_screen_right":manual_brow_tilt.y,"brow_inner_lift_screen_left":manual_brow_inner_lift.x,"brow_inner_lift_screen_right":manual_brow_inner_lift.y,"gaze_x":manual_gaze.x,"gaze_y":manual_gaze.y,"gaze_down_extra":float(manual_gaze_down_extra),"hair_sway":float(manual_hair),"mouth_open":float(manual_mouth_open),"eye_smile_R":manual_eye_smile.x,"eye_smile_L":manual_eye_smile.y,"mouth_smile":float(manual_mouth_smile),"mouth_spread":float(manual_mouth_spread),"mouth_corner_lift":float(manual_mouth_corner_lift),"mouth_corner_lift_screen_left":manual_mouth_corner_sides.x,"mouth_corner_lift_screen_right":manual_mouth_corner_sides.y,"mouth_width_screen_left":manual_mouth_width_sides.x,"mouth_width_screen_right":manual_mouth_width_sides.y,"mouth_lip_press":float(manual_mouth_lip_press),"mouth_oral_lift":float(manual_mouth_oral_lift),"mouth_purse":float(manual_mouth_purse),"mouth_kiss":float(manual_mouth_kiss),"blush_intensity":float(manual_blush_intensity)}
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
func _clear_mouth_bridge():
    opening_bridge_active=false
    mouth_bridge_mode="none";mouth_bridge_duration=0.0
func _prepare_mouth_bridge():
    var source_width=Registry.width_present(restart_pose)
    var target_width=false;var target_open=false
    for frame in performance.keyframes:
        target_width=target_width or Registry.width_present(frame.values)
        target_open=target_open or float(frame.values.get("mouth_open",0.0))>0.0
    mouth_bridge_mode="legacy"
    if source_width or target_width:
        mouth_bridge_mode="staged" if (source_width and target_open) or (float(restart_pose.get("mouth_open",0.0))>0.0 and target_width) else "bounded_direct"
    mouth_bridge_duration=RESTART_SECONDS if mouth_bridge_mode=="legacy" else minf(RESTART_SECONDS,performance.duration)
func _compose_mouth_bridge(p:Dictionary,target:Dictionary):
    # p contains the literal old interpolation for all other channels.
    if mouth_bridge_mode in ["none","legacy"]:return
    if performance_time>=mouth_bridge_duration:
        for key in MOUTH_TRIO:p[key]=target[key]
        return
    var u=clampf(performance_time/mouth_bridge_duration,0.0,1.0)
    if mouth_bridge_mode=="bounded_direct":
        var weight=smoothstep(0.0,1.0,u)
        for key in MOUTH_TRIO:p[key]=lerpf(float(restart_pose.get(key,0.0)),float(target[key]),weight)
    elif u<=0.5:
        var weight=1.0-smoothstep(0.0,0.5,u)
        for key in MOUTH_TRIO:p[key]=float(restart_pose.get(key,0.0))*weight
    else:
        var weight=smoothstep(0.5,1.0,u)
        for key in MOUTH_TRIO:p[key]=float(target[key])*weight
func mouth_transition_state()->Dictionary:
    var stage="none"
    if mouth_bridge_mode!="none":
        stage="complete" if performance_time>=mouth_bridge_duration else ("source" if mouth_bridge_mode=="staged" and performance_time<=mouth_bridge_duration*.5 else ("target" if mouth_bridge_mode=="staged" else "direct"))
    return {"mode":mouth_bridge_mode,"stage":stage,"duration":mouth_bridge_duration,"classification":"entire target timeline at trigger"}
func phase_at(time:float)->String:
    var phase="neutral"
    for k in performance.get("keyframes",[]):
        if time>=k.time:phase=k.phase
    return phase
func _apply_performance_pose(p:Dictionary):
    assert(Registry.scoped_valid(p),"Invalid runtime scoped component composition")
    for key in SCOPED_CHANNELS:scoped_pose[key]=float(p.get(key,0))
    manual_lids=Vector2(p.blink_R,p.blink_L);manual_brow=Vector2(p.brow_screen_left,p.brow_screen_right)
    manual_brow_tilt=Vector2(p.brow_tilt_screen_left,p.brow_tilt_screen_right);manual_gaze=Vector2(p.gaze_x,p.gaze_y);manual_gaze_down_extra=float(p.get("gaze_down_extra",0.0))
    manual_brow_inner_lift=Vector2(p.get("brow_inner_lift_screen_left",0),p.get("brow_inner_lift_screen_right",0))
    manual_eye_smile=Vector2(p.get("eye_smile_R",0),p.get("eye_smile_L",0));manual_mouth_smile=p.get("mouth_smile",0);manual_mouth_spread=p.get("mouth_spread",0);manual_mouth_corner_lift=p.get("mouth_corner_lift",0);manual_mouth_lip_press=p.get("mouth_lip_press",0);manual_mouth_oral_lift=p.get("mouth_oral_lift",0);manual_mouth_purse=p.get("mouth_purse",0);manual_mouth_kiss=p.get("mouth_kiss",0);manual_blush_intensity=p.get("blush_intensity",0)
    manual_mouth_width_sides=Vector2(p.get("mouth_width_screen_left",0),p.get("mouth_width_screen_right",0))
    manual_mouth_corner_sides=Vector2(p.get("mouth_corner_lift_screen_left",0),p.get("mouth_corner_lift_screen_right",0))
    manual_hair=p.hair_sway;manual_mouth_open=p.mouth_open;mouth_shape="neutral";oral_mode="continuous"
    current_pose=p.duplicate();current_pose.mouth_purse=float(manual_mouth_purse);current_pose.mouth_kiss=float(manual_mouth_kiss)
    current_pose.mouth_width_screen_left=manual_mouth_width_sides.x;current_pose.mouth_width_screen_right=manual_mouth_width_sides.y
    current_pose.mouth_corner_lift_screen_left=manual_mouth_corner_sides.x;current_pose.mouth_corner_lift_screen_right=manual_mouth_corner_sides.y
    current_pose.brow_inner_lift_screen_left=manual_brow_inner_lift.x;current_pose.brow_inner_lift_screen_right=manual_brow_inner_lift.y;_write_pose()
func _write_pose():
    if not face or not face.ready_for_controls:return
    # Complete validated pose is committed synchronously. No yield or partial
    # low-level domain guard may reject half of an atomic open/width switch.
    if scoped_parts:scoped_parts.restore_eye()
    super._write_pose()
    if oral_mode=="continuous":face.set_mouth_open(manual_mouth_open)
    face.set_smile_controls(manual_eye_smile,manual_mouth_smile,manual_mouth_spread,manual_mouth_corner_lift,manual_mouth_lip_press,manual_mouth_oral_lift,manual_mouth_purse,manual_mouth_corner_sides,manual_mouth_width_sides)
    face.set_kiss_weight(manual_mouth_kiss)
    face.set_blush_intensity(manual_blush_intensity)
    if scoped_parts:scoped_parts.apply(scoped_pose)
    var owner=active_performance if active_performance!="" else ("release" if release_time>=0 else "manual")
    face.effect_owner=owner
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
    if data.has("gaze_down_extra") and not Limits.valid_gaze_down_extra(data.gaze_down_extra):
        last_error="gaze_down_extra must be finite and in [0,1]";return false
    # The flattened canonical hair has only a verified small reveal margin.
    if data.has("hair_sway") and (not number(data.hair_sway) or abs(float(data.hair_sway))>MAX_HAIR_SWAY):
        last_error="Canonical hair_sway supports only [-0.07,0.07]";return false
    # Validate the complete transaction before changing ownership or pose.
    var base=data.duplicate()
    for key in ["perform_expression","release_performance","mouth_open","eye_smile_R","eye_smile_L","mouth_smile","mouth_spread","mouth_corner_lift","mouth_corner_lift_screen_left","mouth_corner_lift_screen_right","mouth_width_screen_left","mouth_width_screen_right","mouth_lip_press","mouth_oral_lift","mouth_purse","mouth_kiss","blush_intensity"]:base.erase(key)
    for key in base:
        if key not in NUMBERS and key not in ["reset","auto_blink","mouth","viseme"]:last_error="Unsupported control: "+str(key);return false
    for key in NUMBERS:
        if base.has(key) and (not number(base[key]) or abs(float(base[key]))>1 or (key in ["blink","blink_L","blink_R","brow_inner_lift_screen_left","brow_inner_lift_screen_right"] and base[key]<0)):
            last_error="Invalid numeric control: "+key;return false
    for key in ["reset","auto_blink"]:
        if base.has(key) and not base[key] is bool:last_error="Expected boolean: "+key;return false
    for key in ["mouth","viseme"]:
        if base.has(key) and (not base[key] is String or base[key].to_upper() not in ["A","E","I","O","U","REST","RELEASE","NEUTRAL"]):last_error="Invalid mouth shape";return false
    for key in ["eye_smile_R","eye_smile_L","mouth_smile","mouth_spread","mouth_corner_lift","mouth_corner_lift_screen_left","mouth_corner_lift_screen_right","mouth_width_screen_left","mouth_width_screen_right","mouth_lip_press","mouth_oral_lift","mouth_purse","mouth_kiss","blush_intensity"]:
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
        performance=registry.definition(active_performance);performance_time=0;release_time=-1;performance_phase=registry.trigger_phase(active_performance);_suspend_auto_blink()
        release_pose.clear();_prepare_mouth_bridge();_prepare_opening_bridge();last_error=""
        _apply_performance_pose(restart_pose);return true
    if data.get("release_performance",false):
        release_pose=displayed_pose();active_performance="";release_time=0;performance_phase="interrupted_release";_suspend_auto_blink()
        _clear_mouth_bridge();last_error="";_apply_performance_pose(release_pose);return true
    if data.has("release_performance"):last_error="";return true
    # Validate retained authored/manual fields as a complete prospective pose
    # before taking ownership, cancelling blink intent or touching any setter.
    var prospective=neutral_pose() if data.get("reset",false) else pose_now()
    for key in ["mouth","viseme"]:
        if data.has(key):prospective.mouth_open=0.0
    for key in MOUTH_TRIO:
        if data.has(key):prospective[key]=float(data[key])
    if not Registry.sealed_mouth_valid(prospective):
        last_error="Positive mouth width or kiss requires mouth_open == 0; set the sealed-mouth fields atomically";return false
    if data.size()>0:
        for key in SCOPED_CHANNELS:scoped_pose[key]=0.0
        _clear_mouth_bridge()
        auto_blink_pending_restore=false
        active_performance="";release_time=-1;performance_phase="manual"
    if data.get("reset",false):
        manual_mouth_open=0;manual_eye_smile=Vector2.ZERO;manual_mouth_smile=0.0;manual_mouth_spread=0.0;manual_mouth_corner_lift=0.0;manual_mouth_corner_sides=Vector2.ZERO;manual_mouth_width_sides=Vector2.ZERO;manual_mouth_lip_press=0.0;manual_mouth_oral_lift=0.0;manual_mouth_purse=0.0;manual_mouth_kiss=0.0;manual_blush_intensity=0.0;oral_mode="continuous";performance_time=0;performance_phase="neutral"
        restart_pose.clear();release_pose.clear();performance.clear()
    if data.has("eye_smile_R"):manual_eye_smile.x=float(data.eye_smile_R)
    if data.has("eye_smile_L"):manual_eye_smile.y=float(data.eye_smile_L)
    if data.has("mouth_smile"):manual_mouth_smile=float(data.mouth_smile)
    if data.has("mouth_spread"):manual_mouth_spread=float(data.mouth_spread)
    if data.has("mouth_corner_lift"):manual_mouth_corner_lift=float(data.mouth_corner_lift)
    if data.has("mouth_corner_lift_screen_left"):manual_mouth_corner_sides.x=float(data.mouth_corner_lift_screen_left)
    if data.has("mouth_corner_lift_screen_right"):manual_mouth_corner_sides.y=float(data.mouth_corner_lift_screen_right)
    if data.has("mouth_width_screen_left"):manual_mouth_width_sides.x=float(data.mouth_width_screen_left)
    if data.has("mouth_width_screen_right"):manual_mouth_width_sides.y=float(data.mouth_width_screen_right)
    if data.has("mouth_lip_press"):manual_mouth_lip_press=float(data.mouth_lip_press)
    if data.has("mouth_oral_lift"):manual_mouth_oral_lift=float(data.mouth_oral_lift)
    if data.has("mouth_purse"):manual_mouth_purse=float(data.mouth_purse)
    if data.has("mouth_kiss"):manual_mouth_kiss=float(data.mouth_kiss)
    if data.has("blush_intensity"):manual_blush_intensity=float(data.blush_intensity)
    if data.has("mouth_open"):manual_mouth_open=float(data.mouth_open);oral_mode="continuous"
    for key in ["mouth","viseme"]:
        if data.has(key):
            oral_mode="continuous" if data[key].to_upper() in ["REST","RELEASE","NEUTRAL"] else "viseme"
            if oral_mode=="continuous":manual_mouth_open=0
    var ok=super.apply_controls(base)
    current_pose=pose_now()
    if ok:last_error=""
    return ok
func _suspend_auto_blink():
    auto_blink_pending_restore=auto_blink_pending_restore or auto_blink
    auto_blink=false
func _restore_auto_blink():
    if not auto_blink_pending_restore:return
    # Only completed neutral recovery may release the authored controller's pause.
    if active_performance!="" or release_time>=0 or pose_now()!=neutral_pose():return
    auto_blink_pending_restore=false
    # Reuse the base's existing cycle from its open phase. Resuming the old clock
    # could jump from recovered open eyes straight back to a captured mid-blink.
    elapsed=0.0;auto_blink=true;_write_pose()
func auto_blink_policy()->Dictionary:
    return {"default_enabled":false,"suspend_during_performance_and_release":true,
        "restore_after_neutral_recovery":true,"preserve_intent_across_retrigger":true,
        "manual_takeover_cancels_pending_restore":true,"reset_disables":true,
        "restore_clock":"restart_existing_cycle_open_phase",
        "actual_state_field":"auto_blink","pending_state_field":"auto_blink_pending_restore"}
func _process(delta):advance(delta)
func advance(delta)->bool:
    if not number(delta) or delta<0:last_error="delta must be finite and nonnegative";return false
    if not rig_ready or not registry_ready:return false
    if active_performance!="":
        performance_time=minf(performance.duration,performance_time+delta)
        var p=_sample(performance,performance_time)
        var target_trio={}
        if mouth_bridge_mode not in ["none","legacy"]:
            for key in MOUTH_TRIO:target_trio[key]=p[key]
        # Retrigger from the displayed pose. These are control coordinates, never image opacity.
        if performance_time<RESTART_SECONDS:
            var u=smoothstep(0.0,RESTART_SECONDS,performance_time)
            for key in CHANNELS:p[key]=lerpf(restart_pose.get(key,0),p[key],u)
        if has_scoped(restart_pose) and performance_time<RESTART_SECONDS:
            p=scoped_handoff(restart_pose,_sample(performance,performance_time),performance_time/RESTART_SECONDS)
        # Scoped handoff blends ordinary channels too. Apply the mouth-domain
        # bridge last so it cannot reintroduce opening with sealed width/kiss.
        if opening_bridge_active and performance_time<RESTART_SECONDS:
            _compose_opening_bridge(p,_sample(performance,performance_time),performance_time/RESTART_SECONDS)
        _compose_mouth_bridge(p,target_trio)
        performance_phase=phase_at(performance_time);_apply_performance_pose(p)
        if performance_time>=performance.duration:active_performance="";performance_phase="neutral_return";_clear_mouth_bridge();_apply_performance_pose(neutral_pose());_restore_auto_blink()
    elif release_time>=0:
        release_time+=delta;var u=smoothstep(0.0,RELEASE_SECONDS,release_time);var p=neutral_pose()
        for key in CHANNELS:p[key]=lerpf(release_pose[key],0,u)
        if has_scoped(release_pose):p=scoped_handoff(release_pose,neutral_pose(),release_time/RELEASE_SECONDS)
        _apply_performance_pose(p)
        if release_time>=RELEASE_SECONDS:release_time=-1;performance_phase="neutral";_apply_performance_pose(neutral_pose());_restore_auto_blink()
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
    return {"registry_ready":registry_ready,"active_expression":active_performance,"time":performance_time,"phase":performance_phase,"release_time":release_time,"controls":pose_now(),"displayed_controls":displayed_pose(),"owners":face.owners.duplicate(),"auto_blink":auto_blink,"auto_blink_pending_restore":auto_blink_pending_restore,"mouth_transition":mouth_transition_state(),"last_error":last_error}

func has_scoped(p:Dictionary)->bool:
    for key in SCOPED_CHANNELS:
        if float(p.get(key,0))>0:return true
    return false
func scoped_handoff(source:Dictionary,target:Dictionary,u:float)->Dictionary:
    # Clear constrained parts while retaining their valid ordinary pose. Only
    # then blend ordinary channels. Standalone authored timing is unchanged.
    var p=source.duplicate()
    if u<.5:
        var w=1.0-smoothstep(0.0,.5,u)
        for key in SCOPED_CHANNELS:p[key]=float(source.get(key,0))*w
    else:
        var w=smoothstep(.5,1.0,u)
        for key in CHANNELS:p[key]=lerpf(float(source.get(key,0)),float(target.get(key,0)),w)
        for key in SCOPED_CHANNELS:p[key]=float(target.get(key,0))*w
    return p

func _prepare_opening_bridge():
    opening_bridge_active=false
    var conflict=false
    for key in OPENING_CONFLICTS:
        conflict=conflict or float(restart_pose.get(key,0))!=0
    if not conflict:return
    if float(_sample(performance,RESTART_SECONDS).opening_px)>0:
        opening_bridge_active=true;return
    for key in performance.keyframes:
        if float(key.time)>0 and float(key.time)<RESTART_SECONDS and float(key.values.get("opening_px",0))>0:
            opening_bridge_active=true;return
func _compose_opening_bridge(p:Dictionary,target:Dictionary,u:float):
    # Clear source aversion before its supporting lids, then clear ordinary
    # eye controls before widening. Trigger-fixed and inactive from neutral.
    p.opening_px=0.0
    p.aversion_px=float(restart_pose.get("aversion_px",0))*(1.0-smoothstep(0.0,1.0/3.0,u))
    for key in OPENING_CONFLICTS:
        if key=="aversion_px":continue
        p[key]=float(restart_pose.get(key,0))*(1.0-smoothstep(1.0/3.0,2.0/3.0,u))
    if u>=2.0/3.0:
        var w=smoothstep(2.0/3.0,1.0,u)
        p.opening_px=float(target.opening_px)*w
        for key in OPENING_CONFLICTS:p[key]=float(target.get(key,0))*w

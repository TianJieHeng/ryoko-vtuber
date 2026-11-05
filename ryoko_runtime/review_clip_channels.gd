extends SceneTree
# Actual rig and clip-player capture; no substitute composited animation.
var rig
var wall=0.0
var ready=false
var started=false
var paused_once=false
var resumed_once=false
var replayed=false
var cancelled=false
var reset_done=false
var last_index=-1
var next_sample=0.0
func _initialize():call_deferred("setup")
func setup():
    rig=load("res://motion_rig.tscn").instantiate();root.add_child(rig)
    await process_frame;rig.set_process(false)
    rig.apply_controls({"reset":true,"auto_blink":false,"body_follow":false})
    ready=true
func _process(delta):
    if not ready:return false
    wall+=delta
    if wall>=1.0 and not started:
        started=true
        if not rig.play_clip("res://demo_bust_clip.json"):push_error(rig.clip.error_message);quit(1);return false
    if wall>=7.0 and not paused_once:
        paused_once=true;rig.pause_clip(true);print("REVIEW_PAUSE wall=",wall," clip=",rig.clip.elapsed)
    if wall>=8.5 and not resumed_once:
        resumed_once=true;rig.pause_clip(false);print("REVIEW_RESUME wall=",wall," clip=",rig.clip.elapsed)
    if wall>=21.0 and not replayed:
        replayed=true;rig.play_clip("res://demo_bust_clip.json");print("REVIEW_REPLAY wall=",wall)
    if wall>=23.0 and not cancelled:
        cancelled=true;rig.stop_clip();print("REVIEW_CANCEL wall=",wall)
    if wall>=25.0 and not reset_done:
        reset_done=true;rig.apply_controls({"reset":true,"auto_blink":false,"body_follow":false});print("REVIEW_RESET wall=",wall)
    rig._process(delta)
    if rig.clip.index!=last_index:
        last_index=rig.clip.index
        print("REVIEW_CUE ",JSON.stringify({"wall":wall,"clip_time":rig.clip.elapsed,"next_index":last_index}))
    var label="READY / timed bust channels"
    var t=rig.clip.elapsed
    if wall>=1.0:
        if t<1:label="REST / clip starts"
        elif t<4:label="IRIS + BROWS / independent cues"
        elif t<8.5:label="LOOK + BREATH / eyes lead, head follows"
        elif t<10:label="RELEASE / settle new channels"
        elif t<12:label="ORNAMENT OFF / original attachment"
        elif t<14.5:label="ORNAMENT ON / cue drives head turn"
        elif t<18:label="RECOVERY / explicit release cues"
        else:label="COMPLETE / one-shot, no loop"
    if rig.clip.paused:label="PAUSED / timeline and every rig channel frozen"
    elif replayed and not cancelled:label="REPLAY / cues run once again"
    elif cancelled and not reset_done:label="CANCELLED / owned channels settle"
    elif reset_done:label="RESET / neutral, ready for live control"
    rig.hud.text="RYOKO / TIMED BUST CONTROLS"
    rig.hint.text=label
    rig.pose_status.text="clip %.2f s / review %.2f s" % [rig.clip.elapsed,wall]
    if wall>=next_sample:
        next_sample+=.25
        print("REVIEW_SAMPLE ",JSON.stringify({"wall":wall,"clip_time":rig.clip.elapsed,"active":rig.clip.active,"paused":rig.clip.paused,"gaze":[rig.gaze.current.x,rig.gaze.current.y],"brows":[rig.brows.current.x,rig.brows.current.y],"breath":rig.breathing.amount,"look":[rig.attention.head.x,rig.attention.head.y,rig.attention.head.z],"ornament":rig.ornament.enabled,"ornament_angle":rig.ornament.angle,"head":[rig.current.x,rig.current.y,rig.current.z]}))
    if wall>=27.0:print("TIMED_BUST_REVIEW_COMPLETE");quit()
    return false

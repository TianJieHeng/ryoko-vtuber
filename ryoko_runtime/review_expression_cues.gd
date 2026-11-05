extends SceneTree
# Actual runtime clip playback. Expression changes come from the JSON cue file,
# except the final explicit keyboard takeover and reset demonstration.
var rig
var elapsed=0.0
var events={}
var next_sample=0.0
var label="READY / one clip, existing artwork"
func _initialize():call_deferred("setup")
func setup():
    rig=load("res://motion_rig.tscn").instantiate();root.add_child(rig)
    await process_frame;rig.set_process(false)
    rig.apply_controls({"reset":true,"auto_blink":false,"body_follow":false})
func once(name,time):
    if elapsed<time or events.has(name):return false
    events[name]=true
    return true
func _process(delta):
    if rig==null or not rig.rig_ready:return false
    elapsed+=delta
    if once("start",1.5):
        if not rig.play_clip("res://demo_expression_clip.json"):
            push_error(rig.clip.error_message);quit(1);return false
        print("EXPRESSION_CUE_REVIEW_STARTED")
    if once("pause",5.7):
        rig.pause_clip(true)
        print("EXPRESSION_CUE_PAUSE ",rig.clip.elapsed)
    if once("resume",7.2):
        rig.pause_clip(false)
        print("EXPRESSION_CUE_RESUME ",rig.clip.elapsed)
    if once("replay",22.0):
        if not rig.play_clip("res://demo_expression_clip.json"):
            push_error(rig.clip.error_message);quit(1);return false
        print("EXPRESSION_CUE_REPLAY")
    if once("takeover",25.0):
        var event=InputEventKey.new();event.keycode=KEY_PERIOD;event.pressed=true
        rig._unhandled_key_input(event)
        print("EXPRESSION_CUE_KEYBOARD_TAKEOVER ",rig.face.expression)
    if once("reset",28.0):
        rig.apply_controls({"reset":true,"auto_blink":false,"body_follow":false})
        print("EXPRESSION_CUE_RESET")
    rig._process(delta)
    var t=rig.clip.elapsed
    label="READY / one clip, existing artwork"
    if events.has("start"):
        label="CLIP COMPLETE / explicit neutral ending"
        if rig.clip.active:
            if t<1:label="CLIP / neutral starting pose"
            elif t<3:label="CLIP / EXP-064 + independent gaze"
            elif t<5:label="CLIP / expression + speech + wink"
            elif t<6:label="CLIP / release mouth and wink"
            elif t<7.5:label="CLIP / EXP-041 retains authored gaze"
            elif t<10:label="CLIP / switch to EXP-189 + gaze"
            elif t<11:label="CLIP / EXP-189 speech and other wink"
            elif t<13:label="CLIP / release speech + attention"
            else:label="CLIP / neutral recovery + breath"
        if rig.clip.paused:label="PAUSED / expression and timing held"
        if events.has("replay") and rig.clip.active:label="REPLAY / same validated cue sequence"
        if events.has("takeover"):label="MANUAL TAKEOVER / later cues canceled"
        if events.has("reset"):label="RESET / original neutral rendering"
    rig.hud.text="RYOKO / TIMED EXISTING EXPRESSIONS"
    rig.hint.text=label
    rig.pose_status.text="Face: %s  |  Clip: %.2f s  |  No new artwork"%[rig.face.expression,t]
    if elapsed>=next_sample:
        var gate=rig.skin_material.get_shader_parameter("gaze_open")
        print("EXPRESSION_CUE_SAMPLE ",JSON.stringify({"wall":elapsed,"clip":t,"active":rig.clip.active,"paused":rig.clip.paused,"label":label,"expression":rig.face.expression,"profile":rig.gaze_profile_name,"mouth":rig.face.mouth_state,"gaze":[rig.gaze.current.x,rig.gaze.current.y],"open":[gate.x,gate.y],"cue_index":rig.clip.index}))
        next_sample+=0.25
    if elapsed>=31.0:
        print("EXPRESSION_CUE_REVIEW_COMPLETE");quit()
    return false

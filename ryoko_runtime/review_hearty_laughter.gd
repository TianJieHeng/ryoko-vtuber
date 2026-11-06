extends SceneTree
# One complete expression, played twice through the public command API.
var rig
var elapsed=0.0
var first=false
var second=false
var next_sample=0.0
func _initialize():call_deferred("setup")
func setup():
    rig=load("res://motion_rig.tscn").instantiate();root.add_child(rig)
    await process_frame;rig.set_process(false)
    rig.apply_controls({"reset":true,"auto_blink":false})
    if not rig.face.articulated_mouths.has("EXP-005"):push_error("Missing isolated laughter mouth");quit(1)
func _process(delta):
    if rig==null or not rig.rig_ready:return false
    elapsed+=delta
    if elapsed>=1.0 and not first:
        first=true
        if not rig.apply_controls({"perform_expression":"EXP-005"}):quit(1)
        print("LAUGHTER_TRIGGER first")
    if elapsed>=8.0 and not second:
        second=true
        if not rig.apply_controls({"perform_expression":"EXP-005"}):quit(1)
        print("LAUGHTER_TRIGGER replay")
    rig._process(delta)
    rig.hud.text="EXP-005 / HEARTY LAUGHTER"
    rig.hud.add_theme_font_size_override("font_size",20)
    rig.hint.text="Neutral > anticipation > laugh > recovery"
    rig.hint.add_theme_font_size_override("font_size",14)
    rig.pose_status.text=("Replay / " if second else "Performance / ")+rig.expression_player.phase.replace("_"," ")
    rig.pose_status.add_theme_font_size_override("font_size",12)
    if elapsed>=next_sample:
        print("LAUGHTER_FRAME ",JSON.stringify({"time":elapsed,"phase":rig.expression_player.phase,"values":rig.expression_player.values,"expression":rig.face.expression,"isolated_mouth":rig.face.active_articulated_mouth,"global_mouth":rig.skin_material.get_shader_parameter("expression_mouth")}))
        next_sample+=.1
    if elapsed>=14.5:
        if rig.face.expression!="neutral" or rig.expression_player.active:push_error("Laughter did not recover");quit(1)
        else:print("LAUGHTER_REVIEW_COMPLETE");quit()
    return false

extends SceneTree
## Actual Godot movie-writer replay of the public stage, two complete cycles.
var stage
var tick=0
var out=""
var ready=false
func _initialize():call_deferred("setup")
func setup():
    for arg in OS.get_cmdline_user_args():
        if arg.begins_with("--capture-dir="):out=arg.trim_prefix("--capture-dir=")
    stage=load("res://yawn_stage.tscn").instantiate();root.add_child(stage)
    stage.set_process(false);stage.primary.set_process(false)
    await process_frame;stage.apply_controls({"reset":true});ready=true
func _process(_delta):
    if not ready:return false
    if tick in [30,255]:stage.apply_controls({"perform_expression":"EXP-163"})
    if tick>0:stage.advance(1.0/30.0)
    stage.status.text=("Cycle 1 / " if tick>=30 and tick<255 else ("Cycle 2 / " if tick>=255 else ""))+stage.primary.performance_phase.replace("_"," ")
    if tick%3==0 and out!="":save_frame.call_deferred(tick)
    if tick==465:
        print("YAWN_REVIEW_COMPLETE control_frames=466")
        finish.call_deferred()
    tick+=1
    return false
func save_frame(frame:int):
    await RenderingServer.frame_post_draw
    root.get_texture().get_image().save_png(out+"/frame_%06d.png"%frame)
func finish():
    await RenderingServer.frame_post_draw;quit()

extends SceneTree
# Generic base controls only. No expression/emotion performance timeline.
var rig
var elapsed=0.0
var capture_dir=""
var next_frame=0.0
func _initialize():call_deferred("setup")
func setup():
    rig=load("res://object_rig.tscn").instantiate();root.add_child(rig)
    await process_frame;rig.set_process(false);rig.apply_controls({"reset":true})
    for a in OS.get_cmdline_user_args():
        if a.begins_with("--capture-dir="):capture_dir=a.substr(14)
    if capture_dir!="":DirAccess.make_dir_recursive_absolute(capture_dir)
func _process(delta):
    if rig==null or not rig.rig_ready:return false
    elapsed+=delta
    var label="Neutral source assembly"
    var controls={"reset":true}
    if elapsed>=1 and elapsed<5:
        var u=(elapsed-1)/4;controls={"blink":sin(u*PI)};label="Independent eyelid aperture / fixed iris shape"
    elif elapsed>=5 and elapsed<8:
        var u=(elapsed-5)/3;controls={"blink":0.0,"gaze_x":sin(u*TAU),"gaze_y":0.25*sin(u*TAU)};label="Rigid iris gaze / fixed face and hair"
    elif elapsed>=8 and elapsed<11:
        var u=(elapsed-8)/3;controls={"gaze_x":0.0,"gaze_y":0.0,"brow_screen_left":sin(u*TAU),"brow_tilt_screen_right":sin(u*TAU)};label="Separate full-opacity eyebrow objects"
    elif elapsed>=11 and elapsed<15:
        var u=(elapsed-11)/4;controls={"brow_screen_left":0.0,"brow_tilt_screen_right":0.0,"mouth":"REST"};label="Original neutral-lips object / motion work deferred"
    elif elapsed>=15 and elapsed<18:
        var u=(elapsed-15)/3;controls={"mouth":"REST","hair_sway":sin(u*TAU)};label="Six independent rigid hair objects"
    elif elapsed>=18 and elapsed<21:
        var keys=["A","E","I","O","U"];controls={"hair_sway":0.0,"mouth":keys[min(int((elapsed-18)/.6),4)]};label="Exclusive source-art mouth variants"
    rig.apply_controls(controls);rig._process(delta);rig.pose_status.text=label
    if capture_dir!="" and elapsed>=next_frame:
        next_frame+=0.1;capture.call_deferred(capture_dir+"/frame_%06d.png"%int(round(elapsed*30)))
        print("BASE_SAMPLE ",JSON.stringify({"time":elapsed,"label":label,"snapshot":rig.face.snapshot()}))
    if elapsed>=22.0:print("OBJECT_BASE_REVIEW_COMPLETE");quit()
    return false
func capture(path):
    await RenderingServer.frame_post_draw
    root.get_texture().get_image().save_png(path)

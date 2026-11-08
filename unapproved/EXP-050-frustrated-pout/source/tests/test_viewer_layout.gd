extends SceneTree
const Limits=preload("res://control_limits.gd")
var checks=0
var failures=0
func check(ok:bool,label:String):
    checks+=1
    if not ok:failures+=1;push_error("VIEWER_LAYOUT "+label)
func _initialize():call_deferred("run")
func run():
    root.size=Vector2i(1136,800)
    var viewer=load("res://expression_viewer.tscn").instantiate();root.add_child(viewer)
    viewer.set_process(false);viewer.rig.set_process(false)
    # Exercise manual-lock geometry without opening a listener.
    viewer.bridge_label.text="External control: 127.0.0.1:18163 / manual lock"
    viewer.bridge_button.show()
    for i in range(4):await process_frame
    var viewport=Rect2(Vector2.ZERO,Vector2(1136,800))
    check(viewport.encloses(viewer.controls_scroll.get_global_rect()),"scroll viewport on-screen")
    check(viewport.encloses(viewer.bridge_button.get_global_rect()),"manual-lock recovery button on-screen")
    check(not viewer.controls_scroll.get_global_rect().intersects(viewer.bridge_button.get_global_rect()),"recovery button outside scrolling content")
    check(viewer.sliders.has("gaze_x")==Limits.GAZE_ENABLED and viewer.sliders.has("gaze_y")==Limits.GAZE_ENABLED,"actual switch selects gaze controls")
    check(viewer.controls_scroll.follow_focus,"keyboard focus scrolls into view")
    check(viewer.controls_panel.size.x<=viewer.controls_scroll.size.x,"no clipped horizontal controls")
    for channel in viewer.sliders:
        var slider=viewer.sliders[channel]
        viewer.controls_scroll.ensure_control_visible(slider)
        for i in range(2):await process_frame
        check(viewer.controls_scroll.get_global_rect().encloses(slider.get_global_rect()),"reachable slider "+channel)
    viewer.auto_blink_button.grab_focus()
    for i in range(3):await process_frame
    check(viewer.controls_scroll.get_global_rect().encloses(viewer.auto_blink_button.get_global_rect()),"keyboard can reach final checkbox")
    viewer.bridge_button.grab_focus()
    check(viewer.bridge_button.has_focus(),"recovery button keyboard focus")
    for key in [KEY_P,KEY_SPACE,KEY_0]:
        var event=InputEventKey.new();event.keycode=key;event.pressed=true;viewer._input(event)
        if key==KEY_P:check(viewer.rig.active_performance=="EXP-163","play shortcut remains global")
        elif key==KEY_SPACE:check(viewer.rig.release_time==0,"release shortcut remains global")
        else:check(viewer.rig.pose_now()==viewer.rig.neutral_pose(),"reset shortcut remains global")
    print("VIEWER_LAYOUT_", "PASS" if failures==0 else "FAIL", " enabled=",Limits.GAZE_ENABLED," checks=",checks," failures=",failures)
    quit(0 if failures==0 else 1)

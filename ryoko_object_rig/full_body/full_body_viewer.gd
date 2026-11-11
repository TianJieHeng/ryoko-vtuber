extends Node2D
## One full-body character, the original expression player, and opt-in local control.
const Limits = preload("res://control_limits.gd")
var rig
var status:Label
var body_sliders = {}
var face_sliders = {}
var expression_selector:OptionButton
var expression_status:Label
var expression_ids:Array = []
var auto_blink_button:CheckBox
var auto_blink_status:Label
var control_bridge
var bridge_label:Label
var bridge_button:Button
var view_mode = "Full body"
func _ready():
    process_priority = 10
    get_window().size = Vector2i(1440,1000)
    get_viewport().size = Vector2i(1440,1000)
    rig = preload("res://full_body/full_body_rig.gd").new();add_child(rig)
    var ui = CanvasLayer.new();ui.name = "WorkbenchControls";ui.layer = 10;add_child(ui)
    var backdrop = ColorRect.new();backdrop.position = Vector2(878,0);backdrop.size = Vector2(562,1000);backdrop.color = Color(.09,.11,.13,1);ui.add_child(backdrop)
    var title = Label.new();title.position = Vector2(26,18);title.text = "Ryoko / full-body VTuber";title.add_theme_font_size_override("font_size",27);ui.add_child(title)
    var note = Label.new();note.position = Vector2(26,57);note.text = "One character · approved expressions · live face · optional bounce";ui.add_child(note)
    var scroll = ScrollContainer.new();scroll.position = Vector2(890,24);scroll.size = Vector2(525,850);ui.add_child(scroll)
    scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED;scroll.follow_focus = true
    var panel = VBoxContainer.new();panel.custom_minimum_size.x = 495;panel.size_flags_horizontal = Control.SIZE_EXPAND_FILL;panel.add_theme_constant_override("separation",9);scroll.add_child(panel)
    var views = HBoxContainer.new();panel.add_child(views)
    for mode in ["Full body","Bust","Head"]:
        _button(views,mode,func():_set_view(mode))
    var buttons = HBoxContainer.new();panel.add_child(buttons)
    _button(buttons,"Reset all",func():apply_controls({"reset":true}))
    _button(buttons,"Reset body",func():apply_body_controls({"reset":true}))
    _button(buttons,"Small bounce",play_bounce)
    var overlay = CheckBox.new();overlay.text = "Show skeletal attachment points";panel.add_child(overlay)
    overlay.toggled.connect(func(on):rig.set_bone_overlay(on))
    status = Label.new();status.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART;panel.add_child(status)
    if not rig.ready_for_controls:status.text = rig.last_error;return
    _heading(panel,"Approved facial expressions")
    expression_selector = OptionButton.new();expression_selector.name = "ExpressionPicker"
    expression_selector.fit_to_longest_item = false;expression_selector.custom_minimum_size.x = 475
    panel.add_child(expression_selector)
    for entry in rig.list_expressions():
        expression_ids.append(entry.id);expression_selector.add_item(entry.id + " / " + entry.title)
    expression_selector.disabled = expression_ids.is_empty()
    var expression_buttons = HBoxContainer.new();panel.add_child(expression_buttons)
    var play_button = _button(expression_buttons,"Play [P]",play_selected_expression)
    play_button.name = "ExpressionPlay";play_button.disabled = expression_ids.is_empty()
    var stop_button = _button(expression_buttons,"Stop [Space]",stop_expression)
    stop_button.name = "ExpressionStop";stop_button.tooltip_text = "Release the expression smoothly to neutral without resetting the body."
    expression_status = Label.new();expression_status.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART;panel.add_child(expression_status)
    var info = Label.new();info.text = "Anatomical L = screen right. Sliders use normalized [-1,1].\nSmall calibration ranges only; frontal artwork is not a 3D rig.";info.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART;panel.add_child(info)
    _heading(panel,"Body / frame")
    for key in rig.body_controls:
        var label:String = key.replace("_"," ")
        if rig.body_control_joints.has(key):
            var limits = rig.body_control_joints[key].range_degrees
            label += " (%s to %s°)" % [limits[0],limits[1]]
        _slider(panel,key,label,-1,1,true)
    _heading(panel,"Existing head / face controls")
    for row in [["mouth_open","Mouth opening",0.0,1.0],["mouth_smile","Smile corners",0.0,1.0],["mouth_spread","Lateral smile spread",0.0,1.0],["mouth_corner_lift","Closed-smile curvature",0.0,1.0],["mouth_width_screen_left","Left sealed-mouth width",0.0,1.0],["mouth_width_screen_right","Right sealed-mouth width",0.0,1.0],["mouth_corner_lift_screen_left","Left corner remaining lift",0.0,1.0],["mouth_corner_lift_screen_right","Right corner remaining lift",0.0,1.0],["mouth_lip_press","Inner-lip pressure",0.0,1.0],["mouth_oral_lift","Lower oral-surface lift",0.0,1.0],["mouth_purse","Lip pursing",0.0,1.0],["mouth_kiss","Approved kiss-mouth blend",0.0,1.0],["blush_intensity","Separate cheek blush FX",0.0,1.0],["eye_smile_R","Screen-left smile eye",0.0,1.0],["eye_smile_L","Screen-right smile eye",0.0,1.0],["blink_R","Screen-left eyelid",0.0,1.0],["blink_L","Screen-right eyelid",0.0,1.0],["brow_screen_left","Screen-left brow",-1.0,1.0],["brow_screen_right","Screen-right brow",-1.0,1.0],["brow_tilt_screen_left","Screen-left brow tilt",-1.0,1.0],["brow_tilt_screen_right","Screen-right brow tilt",-1.0,1.0],["brow_inner_lift_screen_left","Screen-left inner brow lift",0.0,1.0],["brow_inner_lift_screen_right","Screen-right inner brow lift",0.0,1.0],["hair_sway","Hair sway",-0.07,0.07]]:
        _slider(panel,row[0],row[1],row[2],row[3],false)
    if Limits.GAZE_ENABLED:
        _slider(panel,"gaze_x","Gaze horizontal",Limits.GAZE_MIN,Limits.GAZE_MAX,false)
        _slider(panel,"gaze_y","Gaze vertical",Limits.GAZE_MIN,Limits.GAZE_MAX,false)
        _slider(panel,"gaze_down_extra","Extra downward gaze",0.0,1.0,false)
    auto_blink_button = CheckBox.new();auto_blink_button.text = "Auto blink preference (manual takeover)";panel.add_child(auto_blink_button)
    auto_blink_button.toggled.connect(func(value):apply_controls({"auto_blink":value}))
    auto_blink_button.tooltip_text = "Changing this preference takes manual ownership immediately and cancels playback/recovery. Reset disables it."
    auto_blink_status = Label.new();auto_blink_status.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART;panel.add_child(auto_blink_status)
    var limits = Label.new();limits.text = ("Gaze is normalized, with calibrated pixel travel." if Limits.GAZE_ENABLED else "Gaze is centered pending coverage QA.") + "\nDiscrete visemes unavailable; mouth/hair limits unchanged.\nManual face controls take ownership immediately.";limits.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART;panel.add_child(limits)
    _setup_control_bridge(ui)
    _set_view("Full body")
    _process(0)
func _heading(parent,text):
    var label = Label.new();label.text = text;label.add_theme_font_size_override("font_size",20);parent.add_child(label)
func _button(parent,text,action):
    var button = Button.new();button.text = text;button.pressed.connect(action);parent.add_child(button)
    return button
func play_selected_expression()->bool:
    if expression_selector == null or expression_selector.selected < 0 or expression_selector.selected >= expression_ids.size():return false
    return apply_controls({"perform_expression":expression_ids[expression_selector.selected]})
func stop_expression()->bool:
    return apply_controls({"release_performance":true})
func apply_controls(data)->bool:
    var ok:bool = rig.apply_controls(data)
    if ok and control_bridge != null and data is Dictionary and not data.is_empty() and data != {"reset":false} and data != {"release_performance":false}:
        control_bridge.manual_takeover()
    return ok
func apply_body_controls(data)->bool:
    var ok:bool = rig.apply_body_controls(data)
    if ok and control_bridge != null and data is Dictionary and not data.is_empty() and data != {"reset":false}:
        control_bridge.manual_takeover()
    return ok
func play_bounce()->bool:
    var ok:bool = rig.play_bounce_demo()
    if ok and control_bridge != null:control_bridge.manual_takeover()
    return ok
func get_state()->Dictionary:return rig.get_state()
func list_expressions()->Array:return rig.list_expressions()
func _setup_control_bridge(ui):
    # Same opt-in loopback adapter; its sole controller is this full-body rig.
    control_bridge = preload("res://control_bridge.gd").new();add_child(control_bridge)
    control_bridge.rig = rig
    var ports = []
    for argument in OS.get_cmdline_user_args():
        if argument.begins_with("--control-port="):ports.append(argument.trim_prefix("--control-port="))
    if ports.size() > 1:control_bridge.last_error = "Specify --control-port only once"
    elif ports.size() == 1:
        if not ports[0].is_valid_int():control_bridge.last_error = "Control port must be an integer in 1024..65535"
        else:control_bridge.start(rig,int(ports[0]))
    if control_bridge.last_error != "":push_error(control_bridge.last_error)
    # Keep recovery available even while the face/body controls are scrolled.
    var bridge_panel = VBoxContainer.new();bridge_panel.position = Vector2(890,890);bridge_panel.size = Vector2(525,96);bridge_panel.add_theme_constant_override("separation",8);ui.add_child(bridge_panel)
    bridge_label = Label.new();bridge_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART;bridge_panel.add_child(bridge_label)
    bridge_button = _button(bridge_panel,"Enable external control",func():control_bridge.allow_external())
func _slider(parent,key,label,low,high,body):
    var line = Label.new();line.text = label;parent.add_child(line)
    var slider = HSlider.new();slider.min_value = low;slider.max_value = high;slider.step = .01 if body else .001;slider.custom_minimum_size = Vector2(475,22);parent.add_child(slider)
    if body:
        body_sliders[key] = slider;slider.value_changed.connect(func(value):apply_body_controls({key:value}))
    else:
        face_sliders[key] = slider;slider.value_changed.connect(func(value):apply_controls({key:value}))
func _set_view(mode):
    view_mode = mode
    # Fixed presentation transforms, never animated scale on anatomical owners.
    if mode == "Full body":rig.scale = Vector2.ONE * .57;rig.position = Vector2(145,100)
    elif mode == "Bust":rig.scale = Vector2.ONE * 1.55;rig.position = Vector2(-350,80)
    else:rig.scale = Vector2.ONE * 2.2;rig.position = Vector2(-690,85)
func _process(_delta):
    if rig == null or status == null or not rig.ready_for_controls:return
    var body:Dictionary = rig.get_body_state()
    var state:Dictionary = rig.expression_rig.get_state()
    expression_status.text = (state.active_expression if state.active_expression != "" else "No active expression") + " / " + state.phase + " / %.2f s" % state.time
    for key in body_sliders:body_sliders[key].set_value_no_signal(body.controls[key])
    for key in face_sliders:face_sliders[key].set_value_no_signal(state.displayed_controls[key])
    var opening = float(state.displayed_controls.mouth_open)
    var has_width = float(state.displayed_controls.mouth_width_screen_left) > 0.0 or float(state.displayed_controls.mouth_width_screen_right) > 0.0
    var has_kiss = float(state.displayed_controls.mouth_kiss) > 0.0
    face_sliders.mouth_open.editable = not has_width and not has_kiss
    face_sliders.mouth_open.tooltip_text = "Set both widths and kiss blend to zero before opening. Atomic API requests may change them together." if has_width or has_kiss else "Opening is available when both independent widths and kiss blend are zero."
    for key in ["mouth_width_screen_left","mouth_width_screen_right","mouth_kiss"]:
        face_sliders[key].editable = opening == 0.0
        face_sliders[key].tooltip_text = "Sealed-mouth only. Set opening to zero first; atomic API requests may change them together."
    auto_blink_button.set_pressed_no_signal(state.auto_blink or state.auto_blink_pending_restore)
    auto_blink_status.text = "Auto blink: paused; resumes after neutral recovery." if state.auto_blink_pending_restore else ("Auto blink: active." if state.auto_blink else "Auto blink: off.")
    if control_bridge != null:
        var bridge = control_bridge.status()
        bridge_label.text = ("External control: 127.0.0.1:%d / " % bridge.port + ("enabled" if bridge.external_enabled else "manual lock")) if bridge.listening else "External control: off (opt-in at launch)"
        if bridge.last_error != "":bridge_label.text = bridge.last_error
        bridge_button.visible = bridge.listening and not bridge.external_enabled
    status.text = "%d joints · %d body layers · %d approved facial profiles\n%s\n%s" % [rig.joints.size(),rig.layer_nodes.size(),rig.list_expressions().size(),body.secondary_motion.phase,rig.last_error]
func _input(event):
    if not event is InputEventKey or not event.pressed or event.echo or rig == null or not rig.ready_for_controls:return
    if event.keycode == KEY_P:play_selected_expression()
    elif event.keycode == KEY_SPACE:stop_expression()
    elif event.keycode == KEY_0:apply_controls({"reset":true})
    else:return
    get_viewport().set_input_as_handled()

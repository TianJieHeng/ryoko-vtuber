extends Node2D
## Manual wiring workbench. No action choreography and no automatic body motion.
var rig
var status:Label
var body_sliders = {}
var face_sliders = {}
var view_mode = "Full body"
func _ready():
    get_window().size = Vector2i(1440,1000)
    get_viewport().size = Vector2i(1440,1000)
    rig = preload("res://full_body/full_body_rig.gd").new();add_child(rig)
    var ui = CanvasLayer.new();ui.name = "WorkbenchControls";ui.layer = 10;add_child(ui)
    var backdrop = ColorRect.new();backdrop.position = Vector2(878,0);backdrop.size = Vector2(562,1000);backdrop.color = Color(.09,.11,.13,1);ui.add_child(backdrop)
    var title = Label.new();title.position = Vector2(26,18);title.text = "Ryoko / full-body wiring review";title.add_theme_font_size_override("font_size",27);ui.add_child(title)
    var note = Label.new();note.position = Vector2(26,57);note.text = "Unapproved · manual joints · existing live face · no action animations";ui.add_child(note)
    var scroll = ScrollContainer.new();scroll.position = Vector2(890,24);scroll.size = Vector2(525,940);ui.add_child(scroll)
    var panel = VBoxContainer.new();panel.custom_minimum_size.x = 495;panel.add_theme_constant_override("separation",9);scroll.add_child(panel)
    var views = HBoxContainer.new();panel.add_child(views)
    for mode in ["Full body","Bust","Head"]:
        _button(views,mode,func():_set_view(mode))
    var buttons = HBoxContainer.new();panel.add_child(buttons)
    _button(buttons,"Reset all",func():rig.reset())
    _button(buttons,"Reset body",func():rig.apply_body_controls({"reset":true}))
    var overlay = CheckBox.new();overlay.text = "Show skeletal attachment points";panel.add_child(overlay)
    overlay.toggled.connect(func(on):rig.set_bone_overlay(on))
    status = Label.new();status.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART;panel.add_child(status)
    if not rig.ready_for_controls:status.text = rig.last_error;return
    var info = Label.new();info.text = "Anatomical L = screen right. Sliders use normalized [-1,1].\nSmall calibration ranges only; frontal artwork is not a 3D rig.";info.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART;panel.add_child(info)
    _heading(panel,"Body / frame")
    for key in rig.body_controls:
        var label:String = key.replace("_"," ")
        if rig.body_control_joints.has(key):
            var limits = rig.body_control_joints[key].range_degrees
            label += " (%s to %s°)" % [limits[0],limits[1]]
        _slider(panel,key,label,-1,1,true)
    _heading(panel,"Existing head / face controls")
    for row in [["blink_L",0,1],["blink_R",0,1],["gaze_x",-1,1],["gaze_y",-1,1],["brow_screen_left",-1,1],["brow_screen_right",-1,1],["mouth_open",0,1],["mouth_smile",0,1],["mouth_purse",0,1],["hair_sway",-.07,.07]]:
        _slider(panel,row[0],row[0].replace("_"," "),row[1],row[2],false)
    _set_view("Full body")
func _heading(parent,text):
    var label = Label.new();label.text = text;label.add_theme_font_size_override("font_size",20);parent.add_child(label)
func _button(parent,text,action):
    var button = Button.new();button.text = text;button.pressed.connect(action);parent.add_child(button)
func _slider(parent,key,label,low,high,body):
    var line = Label.new();line.text = label;parent.add_child(line)
    var slider = HSlider.new();slider.min_value = low;slider.max_value = high;slider.step = .01;slider.custom_minimum_size = Vector2(475,22);parent.add_child(slider)
    if body:
        body_sliders[key] = slider;slider.value_changed.connect(func(value):rig.apply_body_controls({key:value}))
    else:
        face_sliders[key] = slider;slider.value_changed.connect(func(value):rig.apply_controls({key:value}))
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
    for key in body_sliders:body_sliders[key].set_value_no_signal(body.controls[key])
    for key in face_sliders:face_sliders[key].set_value_no_signal(state.displayed_controls[key])
    status.text = "%d joints · %d body layers · %d approved facial profiles\n%s" % [rig.joints.size(),rig.layer_nodes.size(),rig.list_expressions().size(),rig.last_error]
func _unhandled_key_input(event):
    if event is InputEventKey and event.pressed and not event.echo and event.keycode == KEY_0:rig.reset()

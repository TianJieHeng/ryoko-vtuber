extends Node2D
## One shared rig. Review/capture scenes are separate entry points.
var rig
var selector:OptionButton
var state_label:Label
var error_label:Label
var auto_blink_button:CheckBox
var sliders:Dictionary={}
var expression_ids:Array=[]
var control_bridge
var bridge_label:Label
var bridge_button:Button
func _ready():
    process_priority=10
    rig=load("res://expression_rig.tscn").instantiate();add_child(rig)
    rig.set_process_unhandled_key_input(false)
    rig.hud.hide();rig.hint.hide();rig.pose_status.hide()
    label_at("Ryoko / shared expression rig",Vector2(24,18),25)
    label_at("One character · data-driven performances",Vector2(24,49),15)
    var panel=VBoxContainer.new();panel.position=Vector2(610,80);panel.custom_minimum_size=Vector2(490,0);panel.add_theme_constant_override("separation",10);add_child(panel)
    var heading=Label.new();heading.text="Performance";heading.add_theme_font_size_override("font_size",21);panel.add_child(heading)
    selector=OptionButton.new();panel.add_child(selector)
    for entry in rig.list_expressions():
        expression_ids.append(entry.id);selector.add_item(entry.id+" / "+entry.title)
    selector.disabled=expression_ids.is_empty()
    var buttons=HBoxContainer.new();panel.add_child(buttons)
    add_button(buttons,"Play [P]",play_selected)
    add_button(buttons,"Release [Space]",func():apply_controls({"release_performance":true}))
    add_button(buttons,"Reset [0]",func():apply_controls({"reset":true}))
    state_label=Label.new();panel.add_child(state_label)
    var note=Label.new();note.text="Manual controls take ownership immediately.\nOnly the registered performance is implemented.";panel.add_child(note)
    for item in [["mouth_open","Mouth opening",0.0,1.0],["blink_R","Screen-left eyelid",0.0,1.0],["blink_L","Screen-right eyelid",0.0,1.0],["brow_screen_left","Screen-left brow",-1.0,1.0],["brow_screen_right","Screen-right brow",-1.0,1.0],["brow_tilt_screen_left","Screen-left brow tilt",-1.0,1.0],["brow_tilt_screen_right","Screen-right brow tilt",-1.0,1.0],["hair_sway","Hair sway",-0.07,0.07]]:
        add_slider(panel,item)
    auto_blink_button=CheckBox.new();auto_blink_button.text="Auto blink in manual mode";panel.add_child(auto_blink_button)
    auto_blink_button.toggled.connect(func(value):apply_controls({"auto_blink":value}))
    var limits=Label.new();limits.text="Gaze is centered. Discrete visemes are unavailable.\nMouth and hair remain within approved limits.";panel.add_child(limits)
    error_label=Label.new();error_label.modulate=Color(1,.62,.52);error_label.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART;error_label.custom_minimum_size=Vector2(480,44);panel.add_child(error_label)
    # Opt-in only. No listener is created unless a port is explicitly supplied.
    control_bridge=preload("res://control_bridge.gd").new();add_child(control_bridge)
    var ports=[]
    for argument in OS.get_cmdline_user_args():
        if argument.begins_with("--control-port="):ports.append(argument.trim_prefix("--control-port="))
    if ports.size()>1:control_bridge.last_error="Specify --control-port only once"
    elif ports.size()==1:
        if not ports[0].is_valid_int():control_bridge.last_error="Control port must be an integer in 1024..65535"
        else:control_bridge.start(rig,int(ports[0]))
    if control_bridge.last_error!="":push_error(control_bridge.last_error)
    bridge_label=Label.new();bridge_label.autowrap_mode=TextServer.AUTOWRAP_WORD_SMART;panel.add_child(bridge_label)
    bridge_button=Button.new();bridge_button.text="Enable external control";panel.add_child(bridge_button)
    bridge_button.pressed.connect(func():control_bridge.allow_external())
    _process(0)
func label_at(text:String,position_value:Vector2,size:int):
    var label=Label.new();label.text=text;label.position=position_value;label.add_theme_font_size_override("font_size",size);add_child(label)
func add_button(parent:Node,title:String,action:Callable):
    var button=Button.new();button.text=title;button.pressed.connect(action);parent.add_child(button)
func add_slider(parent:Node,item:Array):
    var row=HBoxContainer.new();parent.add_child(row)
    var label=Label.new();label.text=item[1];label.custom_minimum_size.x=188;row.add_child(label)
    var slider=HSlider.new();slider.min_value=item[2];slider.max_value=item[3];slider.step=.001;slider.custom_minimum_size=Vector2(285,24);row.add_child(slider)
    var channel:String=item[0];sliders[channel]=slider
    slider.value_changed.connect(func(value):apply_controls({channel:value}))
func play_selected()->bool:
    if selector.selected<0 or selector.selected>=expression_ids.size():return false
    return apply_controls({"perform_expression":expression_ids[selector.selected]})
func apply_controls(data)->bool:
    var ok=rig.apply_controls(data)
    if ok and control_bridge!=null and data is Dictionary and not data.is_empty() and data!={"reset":false} and data!={"release_performance":false}:
        control_bridge.manual_takeover()
    return ok
func get_state()->Dictionary:return rig.get_state()
func list_expressions()->Array:return rig.list_expressions()
func _process(_delta):
    if rig==null or state_label==null:return
    var state=rig.get_state()
    state_label.text=(state.active_expression if state.active_expression!="" else "No active performance")+" / "+state.phase+" / %.2f s"%state.time
    for channel in sliders:sliders[channel].set_value_no_signal(state.displayed_controls[channel])
    auto_blink_button.set_pressed_no_signal(state.auto_blink)
    error_label.text=state.last_error
    if bridge_label!=null:
        var bridge=control_bridge.status()
        bridge_label.text=("External control: 127.0.0.1:%d / "%bridge.port+("enabled" if bridge.external_enabled else "manual lock")) if bridge.listening else "External control: off (opt-in at launch)"
        if bridge.last_error!="":bridge_label.text=bridge.last_error
        bridge_button.visible=bridge.listening and not bridge.external_enabled
func _input(event):
    if not event is InputEventKey or not event.pressed or event.echo:return
    if event.keycode==KEY_P:play_selected()
    elif event.keycode==KEY_SPACE:apply_controls({"release_performance":true})
    elif event.keycode==KEY_0:apply_controls({"reset":true})
    else:return
    get_viewport().set_input_as_handled()

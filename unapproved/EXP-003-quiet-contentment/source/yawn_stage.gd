extends Node2D
## Three synchronized actual rig views. Camera scales are fixed, not feature animation.
var primary
var closeups=[]
var status:Label
func _ready():
    process_priority=1
    primary=load("res://yawn_rig.tscn").instantiate();add_child(primary)
    primary.hud.hide();primary.hint.hide();primary.pose_status.hide();primary.position=Vector2(0,30)
    add_panel(Vector2i(540,330),Vector2(580,135),Vector2(-298,-425),1.0)
    add_panel(Vector2i(400,230),Vector2(650,520),Vector2(-937,-1210),2.0)
    label_at("Ryoko · Yawn",Vector2(22,14),26)
    label_at("EXP-163 / separate-object candidate",Vector2(22,48),15)
    label_at("Eyes, brows and mouth",Vector2(604,101),20)
    label_at("Oral close-up",Vector2(671,484),20)
    # A footer plate prevents the bust drawing over the status line.
    var footer=ColorRect.new();footer.position=Vector2(0,758);footer.size=Vector2(1136,42);footer.color=Color(.12,.13,.14);footer.z_index=100;add_child(footer)
    status=label_at("Y yawn · Space release · 0 reset",Vector2(22,771),16)
    label_at("Separate moving parts · stationary face",Vector2(611,771),16)
    sync_closeups()
func label_at(text:String,pos:Vector2,size:int)->Label:
    var l=Label.new();l.text=text;l.position=pos;l.z_index=101;l.add_theme_font_size_override("font_size",size);add_child(l);return l
func add_panel(size:Vector2i,pos:Vector2,head_pos:Vector2,head_scale:float):
    var viewport=SubViewport.new();viewport.size=size;viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS;viewport.world_2d=World2D.new();add_child(viewport)
    var rig=load("res://yawn_rig.tscn").instantiate();viewport.add_child(rig)
    rig.set_process(false);rig.set_process_unhandled_key_input(false);rig.body.show();rig.hud.hide();rig.hint.hide();rig.pose_status.hide()
    rig.head.position=head_pos;rig.head.scale=Vector2.ONE*head_scale
    # The split stationary neck/torso shares the exact fixed closeup transform.
    rig.body.position=head_pos;rig.body.scale=Vector2.ONE*head_scale;closeups.append(rig)
    var screen=TextureRect.new();screen.position=pos;screen.size=Vector2(size);screen.texture=viewport.get_texture();add_child(screen)
func sync_closeups():
    var pose=primary.pose_now()
    pose.blink_R=primary.face.closure.x;pose.blink_L=primary.face.closure.y
    for rig in closeups:
        rig._apply_performance_pose(pose)
        if primary.oral_mode=="viseme":
            rig.oral_mode="viseme";rig.mouth_shape=primary.mouth_shape;rig._write_pose()
func _process(_delta):sync_closeups()
func apply_controls(data:Dictionary)->bool:
    var ok=primary.apply_controls(data);sync_closeups();return ok
func advance(delta:float):
    primary._process(delta);sync_closeups()

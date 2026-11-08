extends SceneTree
var rig
var out=""
var evidence=[]
func _initialize():call_deferred("run")
func run():
 for arg in OS.get_cmdline_user_args():
  if arg.begins_with("--output="):out=arg.trim_prefix("--output=")
 if out.is_empty():quit(2);return
 DirAccess.make_dir_recursive_absolute(out)
 root.size=Vector2i(1136,1384)
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 if not rig.rig_ready or not rig.registry_ready:quit(2);return
 rig.hud.hide();rig.hint.hide();rig.pose_status.hide()
 rig.head.position=Vector2.ZERO;rig.body.position=Vector2.ZERO;rig.head.scale=Vector2.ONE;rig.body.scale=Vector2.ONE
 var cases=[
 {"mouth_open":0.0,"mouth_smile":0.0,"mouth_corner_lift":0.0,"mouth_lip_press":0.0},
 {"mouth_open":.72,"mouth_smile":0.0,"mouth_corner_lift":0.0,"mouth_lip_press":0.0},
 {"mouth_open":.72,"mouth_smile":0.0,"mouth_corner_lift":0.0,"mouth_lip_press":1.0},
 {"mouth_open":.75,"mouth_smile":.8,"mouth_spread":.9,"mouth_corner_lift":0.0,"mouth_lip_press":0.0},
 {"mouth_open":.75,"mouth_smile":.8,"mouth_spread":.9,"mouth_corner_lift":1.0,"mouth_lip_press":1.0},
 {"mouth_open":0.0,"mouth_smile":.8,"mouth_spread":.8,"mouth_corner_lift":1.0,"mouth_lip_press":1.0},
 {"mouth_open":1.0,"mouth_smile":0.0,"mouth_corner_lift":0.0,"mouth_lip_press":1.0},
 {"mouth_open":1.0,"mouth_smile":.5,"mouth_spread":0.0,"mouth_corner_lift":0.0,"mouth_lip_press":1.0}]
 for ci in range(cases.size()):
  for purse in [0.0,.00000001,.000001,.001,.4,.7,.702,.7025,.703,.75,.917,.9175,.918,1.0]:
   rig.reset();var p=cases[ci].duplicate();p.mouth_purse=purse;p.mouth_oral_lift=.8
   rig.apply_controls(p);await process_frame;await RenderingServer.frame_post_draw
   var file="case_%d_p%09d.png"%[ci,int(round(purse*100000000))]
   root.get_texture().get_image().save_png(out+"/"+file)
   var transforms={}
   for key in rig.face.objects:
    var n=rig.face.objects[key];var owner=rig.face.homes[key].node
    transforms[key]={"position":[owner.position.x,owner.position.y],"rotation":owner.rotation,"scale":[owner.scale.x,owner.scale.y],"sprite_scale":[n.scale.x,n.scale.y],"opacity":n.modulate.a,"visible":n.visible,"texture":n.texture.resource_path if n.texture else ""}
   evidence.append({"file":file,"case":ci,"purse":purse,"state":rig.get_state(),"transforms":transforms})
 var f=FileAccess.open(out+"/evidence.json",FileAccess.WRITE);f.store_string(JSON.stringify(evidence,"  "));f.close()
 print("PURSE_BOUNDARIES_PASS");quit(0)

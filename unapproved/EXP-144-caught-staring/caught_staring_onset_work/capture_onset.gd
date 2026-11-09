extends SceneTree
var rig
var mouth
var eye
var aversion
var saved={}
var output="/workspace/scratch/42f2baf55663/caught_staring_onset_work/gate_01"
var records=[]
func _initialize():call_deferred("run")
func hide_mouth():
 for key in rig.face.objects:
  if key=="neutral_lips" or key=="active_viseme" or "lip" in key or key.begins_with("oral_") or key.begins_with("spread_") or key.begins_with("mouth_corner"):
   if not saved.has(key):saved[key]=rig.face.objects[key].visible
   rig.face.objects[key].visible=false
 mouth.visible=true
func restore_mouth():
 mouth.visible=false
 for key in saved:rig.face.objects[key].visible=saved[key]
 saved.clear()
func capture(label,detail):
 root.size=Vector2i(568,800);root.canvas_transform=Transform2D.IDENTITY
 if detail:
  root.size=Vector2i(400,360)
  var camera=Transform2D.IDENTITY.scaled(Vector2.ONE/.49);camera.origin=-Vector2(6,70)/.49-Vector2(380,380);root.canvas_transform=camera
 await process_frame;await process_frame;await RenderingServer.frame_post_draw
 root.get_texture().get_image().save_png(output+"/"+label+".png")
func run():
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false);rig.auto_blink=false
 if not rig.rig_ready or not rig.registry_ready:quit(2);return
 rig.hud.hide();rig.hint.hide();rig.pose_status.hide();rig.reset()
 eye=load("/workspace/scratch/42f2baf55663/caught_staring_onset_work/upper_opening_part.gd").new();eye.rig=rig;eye.work="/workspace/scratch/42f2baf55663/caught_staring_onset_work"
 aversion=load("/workspace/scratch/42f2baf55663/horizontal_aversion_part_work/horizontal_aversion_part.gd").new()
 for side in ["screen_left","screen_right"]:
  var tex=ImageTexture.create_from_image(Image.load_from_file(ProjectSettings.globalize_path("res://rig_assets/gaze_eyes/iris_"+side+".png")))
  eye.repaired_textures[side]=tex;rig.face.objects["iris_"+side].texture=tex
  for prefix in ["iris_","sclera_"]:rig.face.objects[prefix+side].material.set_shader_parameter("iris_texture",tex)
 mouth=Sprite2D.new();mouth.centered=false;mouth.z_index=58;mouth.position=Vector2(537,628);mouth.visible=false
 mouth.texture=ImageTexture.create_from_image(Image.load_from_file("/workspace/scratch/42f2baf55663/caught_staring_mouth_work/uneasy_clear_parting.png"));rig.face.add_child(mouth)
 var baseline=rig.face.snapshot();var head=rig.head.transform;var body=rig.body.transform
 var plan=JSON.parse_string(FileAccess.get_file_as_string("/workspace/scratch/42f2baf55663/caught_staring_onset_work/plan.json"))
 for label in plan:
  eye.restore();restore_mouth();rig.reset();var p=rig.neutral_pose();var e=plan[label]
  for k in e.pose:p[k]=e.pose[k]
  rig._apply_performance_pose(p);eye.install_opening(e.opening)
  if not aversion.apply(rig.face,e.x):push_error("Aversion refused");quit(3);return
  if e.mouth:hide_mouth()
  await capture(label,true)
  if label in ["KP3_open4","KP4_avert"]:await capture(label+"_bust",false)
  records.append({"label":label,"opening_px":eye.opening_px,"x":e.x,"pose":p})
 eye.restore();restore_mouth();rig.reset();aversion.restore(rig.face)
 var f=FileAccess.open(output+"/result.json",FileAccess.WRITE);f.store_string(JSON.stringify({"snapshot_restored":baseline==rig.face.snapshot(),"head_body_exact":head==rig.head.transform and body==rig.body.transform,"records":records},"  "));f.close();quit()

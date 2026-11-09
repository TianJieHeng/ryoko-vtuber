extends SceneTree
var rig
var output="/workspace/scratch/42f2baf55663/caught_staring_mouth_work/gate_01"
var results=[]
func _initialize():call_deferred("run")
func capture(label):
 await process_frame;await process_frame;await RenderingServer.frame_post_draw
 root.get_texture().get_image().save_png(output+"/"+label+".png")
func set_aversion(x):
 # Private rigid-part proposal only. Public controller bounds are not changed.
 for side in ["screen_left","screen_right"]:
  var key="iris_"+side
  rig.face.homes[key].node.position=rig.face.homes[key].pivot+Vector2(x,0)
  for prefix in ["iris_","sclera_"]:
   rig.face.objects[prefix+side].material.set_shader_parameter("rigid_gaze",Vector2(x,0))
func run():
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false);rig.auto_blink=false
 if not rig.rig_ready or not rig.registry_ready:quit(2);return
 rig.hud.hide();rig.hint.hide();rig.pose_status.hide();rig.reset()
 for side in ["screen_left","screen_right"]:
  var tex=ImageTexture.create_from_image(Image.load_from_file(ProjectSettings.globalize_path("res://rig_assets/gaze_eyes/iris_"+side+".png")))
  rig.face.objects["iris_"+side].texture=tex
  for prefix in ["iris_","sclera_"]:
   rig.face.objects[prefix+side].material.set_shader_parameter("iris_texture",tex)
 var state=rig.face.snapshot()
 var poses=JSON.parse_string(FileAccess.get_file_as_string("/workspace/scratch/42f2baf55663/caught_staring_mouth_work/plan.json"))
 root.size=Vector2i(400,360)
 var camera=Transform2D.IDENTITY.scaled(Vector2.ONE/.49);camera.origin=-Vector2(6,70)/.49-Vector2(380,380);root.canvas_transform=camera
 for label in poses:
  rig.reset();var pose=rig.neutral_pose()
  for k in poses[label].pose:
   if not pose.has(k):push_error("Unknown pose key "+k);quit(3);return
   pose[k]=poses[label].pose[k]
  rig._apply_performance_pose(pose);set_aversion(poses[label].x);await capture(label)
  results.append({"label":label,"x_pixels":poses[label].x,"pose":pose})
 root.size=Vector2i(568,800);root.canvas_transform=Transform2D.IDENTITY
 var peak=rig.neutral_pose()
 for k in poses.caught_peak.pose:peak[k]=poses.caught_peak.pose[k]
 rig._apply_performance_pose(peak);set_aversion(12);await capture("caught_peak_bust")
 rig.reset();set_aversion(0)
 var f=FileAccess.open(output+"/result.json",FileAccess.WRITE);f.store_string(JSON.stringify({"snapshot_restored":state==rig.face.snapshot(),"poses":results},"  "));f.close();quit()

extends SceneTree
var rig
var output="/workspace/scratch/42f2baf55663/caught_staring_mouth_work/proposal_01"
var results=[]
var saved_visibility={}
var proposal
func restore_mouth():
 for key in saved_visibility:rig.face.objects[key].visible=saved_visibility[key]
 saved_visibility.clear()
func hide_mouth():
 for key in rig.face.objects:
  if key=="neutral_lips" or key=="active_viseme" or "lip" in key or key.begins_with("oral_") or key.begins_with("spread_") or key.begins_with("mouth_corner"):
   if not saved_visibility.has(key):saved_visibility[key]=rig.face.objects[key].visible
   rig.face.objects[key].visible=false
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
 proposal=Sprite2D.new();proposal.centered=false;proposal.z_index=58;proposal.position=Vector2(537,628)
 proposal.texture=ImageTexture.create_from_image(Image.load_from_file("/workspace/scratch/42f2baf55663/caught_staring_mouth_work/uneasy_authored.png"));proposal.visible=false;rig.face.add_child(proposal)
 var poses=JSON.parse_string(FileAccess.get_file_as_string("/workspace/scratch/42f2baf55663/caught_staring_mouth_work/plan.json"))
 root.size=Vector2i(400,360)
 var camera=Transform2D.IDENTITY.scaled(Vector2.ONE/.49);camera.origin=-Vector2(6,70)/.49-Vector2(380,380);root.canvas_transform=camera
 for label in poses:
  proposal.visible=false;restore_mouth();rig.reset();var pose=rig.neutral_pose()
  for k in poses[label].pose:
   if not pose.has(k):push_error("Unknown pose key "+k);quit(3);return
   pose[k]=poses[label].pose[k]
  rig._apply_performance_pose(pose);set_aversion(poses[label].x);await capture(label+"_old")
  if label in ["KP3_uneasy","KP4_aversion"]:
   hide_mouth();proposal.visible=true;await capture(label+"_proposal")
  results.append({"label":label,"x_pixels":poses[label].x,"pose":pose})
 proposal.visible=false;restore_mouth()
 root.size=Vector2i(568,800);root.canvas_transform=Transform2D.IDENTITY
 var peak=rig.neutral_pose()
 for k in poses.KP4_aversion.pose:peak[k]=poses.KP4_aversion.pose[k]
 rig._apply_performance_pose(peak);set_aversion(12);hide_mouth();proposal.visible=true;await capture("uneasy_proposal_bust")
 proposal.visible=false;restore_mouth()
 rig.reset();set_aversion(0)
 var f=FileAccess.open(output+"/result.json",FileAccess.WRITE);f.store_string(JSON.stringify({"snapshot_restored":state==rig.face.snapshot(),"poses":results},"  "));f.close();quit()

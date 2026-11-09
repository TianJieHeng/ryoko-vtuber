extends RefCounted
var rig
var eye
var aversion
var mouth
var timeline
var root_path="/workspace/scratch/42f2baf55663"
func setup(r):
 rig=r
 timeline=JSON.parse_string(FileAccess.get_file_as_string(root_path+"/caught_staring_performance_work/EXP-144-review.json"))
 eye=load(root_path+"/caught_staring_onset_work/upper_opening_part.gd").new();eye.rig=rig;eye.work=root_path+"/caught_staring_onset_work"
 aversion=load(root_path+"/horizontal_aversion_part_work/horizontal_aversion_part.gd").new()
 for side in ["screen_left","screen_right"]:eye.repaired_textures[side]=rig.face.objects["iris_"+side].texture
 mouth=Sprite2D.new();mouth.name="unapproved_uneasy_visible_part";mouth.centered=false;mouth.z_index=58;mouth.position=Vector2(537,628)
 mouth.texture=ImageTexture.create_from_image(Image.load_from_file(root_path+"/caught_staring_mouth_work/uneasy_clear_parting.png"));mouth.modulate.a=0;rig.face.add_child(mouth)
func sample(t):
 var frames=timeline.keyframes
 if t<=0:return frames[0].values.duplicate()
 if t>=timeline.duration:return frames[-1].values.duplicate()
 for i in range(1,frames.size()):
  if t<=frames[i].time:
   var a=frames[i-1];var b=frames[i];var u=smoothstep(0.0,1.0,(t-a.time)/(b.time-a.time));var out={}
   for key in a.values:out[key]=lerpf(a.values[key],b.values[key],u)
   return out
 return frames[-1].values.duplicate()
func set_mouth(weight):
 # Reuse the already-tested opacity mechanism, never display or animate kiss art.
 for key in rig.face.kiss_native_owners:
  var n=rig.face.objects[key];var c=rig.face.kiss_native_opacity[key];c.a*=1.0-weight;n.self_modulate=c
  if n.material is ShaderMaterial:n.material.set_shader_parameter("native_part_weight",1.0-weight)
 mouth.modulate.a=weight
func apply(t)->bool:
 var v=sample(t)
 if v.opening_px>0 and (v.blink_L!=0 or v.blink_R!=0 or v.aversion_px!=0 or v.gaze_y!=0 or v.gaze_down_extra!=0):return false
 if v.aversion_px>0 and (v.blink_L<.18 or v.blink_R<.18 or v.gaze_y!=0 or v.gaze_down_extra!=0):return false
 eye.restore();var pose=rig.neutral_pose()
 for key in v:
  if pose.has(key):pose[key]=v[key]
 rig._apply_performance_pose(pose)
 eye.install_opening(v.opening_px)
 if not aversion.apply(rig.face,v.aversion_px):return false
 set_mouth(v.uneasy_weight)
 return true
func reset():
 eye.restore();rig.reset();aversion.restore(rig.face);set_mouth(0)

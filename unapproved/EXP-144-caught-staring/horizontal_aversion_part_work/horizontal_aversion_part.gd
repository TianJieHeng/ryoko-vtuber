extends RefCounted
# Review-only one-frame applicator. This does not expand the public controller.
# Caller applies the ordinary pose first, then this part, every frame.
const Limits=preload("res://control_limits.gd")
func apply(face,pixels:float)->bool:
 if not is_finite(pixels) or pixels<0.0 or pixels>12.0:return false
 if is_zero_approx(pixels):restore(face);return true
 if face.closure.x<.18 or face.closure.y<.18:return false
 if face.gaze!=Vector2.ZERO or face.gaze_down_extra!=0.0 or face.smile_eyes!=Vector2.ZERO:return false
 _offset(face,Vector2(pixels,0));return true
func restore(face)->void:
 _offset(face,Limits.gaze_pixels(face.gaze,face.gaze_down_extra))
func _offset(face,offset:Vector2)->void:
 for side in ["screen_left","screen_right"]:
  var key="iris_"+side
  face.homes[key].node.position=face.homes[key].pivot+offset
  for prefix in ["iris_","sclera_"]:
   face.objects[prefix+side].material.set_shader_parameter("rigid_gaze",offset)

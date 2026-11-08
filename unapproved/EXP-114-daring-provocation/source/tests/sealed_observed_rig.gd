extends "res://expression_rig.gd"
var completed_write_count=0
var invalid_completed_writes=[]
func _write_pose():
    super._write_pose()
    if not face or not face.ready_for_controls:return
    completed_write_count+=1
    if not Registry.sealed_mouth_valid(pose_now()):invalid_completed_writes.append("controller domain")
    if face.mouth_opening>0.0 and face.mouth_width_sides!=Vector2.ZERO:invalid_completed_writes.append("face domain")
    if face.mouth_width_sides!=manual_mouth_width_sides:invalid_completed_writes.append("face width mismatch")
    if oral_mode=="continuous" and face.mouth_opening!=manual_mouth_open:invalid_completed_writes.append("face opening mismatch")

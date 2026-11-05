extends RefCounted
var path="user://rig_poses.json"
var poses={}
var error_message=""
func _valid_pose(p)->bool:
    if not p is Dictionary:return false
    if not p.get("body_follow") is bool:return false
    for key in ["head_tilt","head_x","head_y","body_tilt","body_x","body_y"]:
        if not p.has(key) or not (p[key] is float or p[key] is int):return false
        if not is_finite(float(p[key])) or abs(float(p[key]))>1.0:return false
    return true
func load_disk()->bool:
    error_message=""
    if not FileAccess.file_exists(path):return true
    var parser=JSON.new()
    if parser.parse(FileAccess.get_file_as_string(path))!=OK:
        error_message="Invalid pose file; existing file left unchanged."
        return false
    var data=parser.data
    if not data is Dictionary or data.get("version")!=1 or not data.get("poses") is Dictionary:
        error_message="Invalid pose file; existing file left unchanged."
        return false
    var candidate=data.poses
    for slot in candidate:
        if slot not in ["1","2","3"] or not _valid_pose(candidate[slot]):
            error_message="Invalid saved pose; existing file left unchanged."
            return false
    poses=candidate.duplicate(true)
    return true
func save_slot(slot:int,p:Dictionary)->bool:
    error_message=""
    if slot<1 or slot>3 or not _valid_pose(p):
        error_message="Invalid pose or slot."
        return false
    var candidate=poses.duplicate(true);candidate[str(slot)]=p.duplicate(true)
    var file=FileAccess.open(path+".tmp",FileAccess.WRITE)
    if file==null:error_message="Could not write pose file.";return false
    file.store_string(JSON.stringify({"version":1,"poses":candidate},"  "));file.close()
    var err=DirAccess.rename_absolute(path+".tmp",path)
    if err!=OK:error_message="Could not replace pose file.";return false
    poses=candidate
    return true
func recall(slot:int)->Dictionary:
    return poses.get(str(slot),{}).duplicate(true)

extends SceneTree
# The production sampler is used without rendering or editing the rig.
var w=get_script().resource_path.get_base_dir()
var checks=0
var failures=[]
const CHANNELS=["brow_screen_left","brow_screen_right","eye_smile_L","eye_smile_R","mouth_smile","mouth_corner_lift"]
func check(ok,label):
 checks+=1
 if not ok:failures.append(label)
func _initialize():call_deferred("run")
func run():
 var player=load("res://expression_rig.gd").new();var registry=load("res://expression_registry.gd").new()
 var candidate=JSON.parse_string(FileAccess.get_file_as_string(w+"/EXP-003.json"));var original=JSON.stringify(candidate)
 check(registry.validate_definition(candidate,"EXP-003"),"definition accepted: "+registry.last_error)
 var samples=0;var previous={};var max_step={}
 for i in range(4601):
  var t=float(i)/1000.0;var p=player._sample(candidate,t);samples+=1
  check(registry.scoped_valid(p),"scope "+str(i));check(registry.sealed_mouth_valid(p),"sealed mouth domain "+str(i))
  check(is_equal_approx(p.eye_smile_L,p.eye_smile_R) and is_equal_approx(p.brow_screen_left,p.brow_screen_right),"symmetric acting "+str(i))
  check(p.mouth_open==0 and p.mouth_spread==0 and p.mouth_purse==0,"sealed restrained mouth "+str(i))
  for channel in p:
   var bounds=registry.CHANNEL_BOUNDS[channel]
   check(registry.number(p[channel]) and p[channel]>=bounds[0] and p[channel]<=bounds[1],"bounded "+channel+" "+str(i))
   if channel not in CHANNELS:check(p[channel]==0,"excluded "+channel+" "+str(i))
  if t>.25 and t<=1.65 and not previous.is_empty():
   for channel in ["eye_smile_L","eye_smile_R","mouth_smile","mouth_corner_lift"]:check(p[channel]>=previous[channel]-.0000001,"single monotone settle "+channel+" "+str(i))
   check(p.brow_screen_left<=previous.brow_screen_left+.0000001,"brows lower without recoil "+str(i))
  if t>=1.65 and t<=2.8:
   for channel in player.CHANNELS:check(is_equal_approx(float(p[channel]),float(candidate.keyframes[4].values.get(channel,0))),"exact gentle hold "+channel+" "+str(i))
  if t>2.8 and not previous.is_empty():
   for channel in ["eye_smile_L","eye_smile_R","mouth_smile","mouth_corner_lift"]:check(p[channel]<=previous[channel]+.0000001,"single release "+channel+" "+str(i))
  if t<=.25 or t>=4.25:check(p==player.neutral_pose(),"neutral bookend "+str(i))
  if not previous.is_empty():
   for channel in CHANNELS:max_step[channel]=maxf(max_step.get(channel,0),absf(p[channel]-previous[channel]))
  previous=p
 for channel in registry.CHANNEL_BOUNDS:
  for value in [float(registry.CHANNEL_BOUNDS[channel][0])-.01,float(registry.CHANNEL_BOUNDS[channel][1])+.01]:
   var bad=candidate.duplicate(true);bad.keyframes[4].values[channel]=value
   check(not registry.validate_definition(bad,"EXP-003"),"out of bound rejected "+channel)
 var bad=candidate.duplicate(true);bad.keyframes[4].values["contentment_shape"]=.4
 check(not registry.validate_definition(bad,"EXP-003"),"invented anatomy rejected")
 bad=candidate.duplicate(true);bad.keyframes[4].values["opening_px"]=.1
 check(not registry.validate_definition(bad,"EXP-003"),"incompatible wider eyes rejected")
 bad=candidate.duplicate(true);bad.keyframes[3].values["opening_px"]=.1;bad.keyframes[3].values.erase("eye_smile_L");bad.keyframes[3].values.erase("eye_smile_R")
 check(not registry.validate_definition(bad,"EXP-003"),"adjacent incompatible eye segment rejected")
 check(JSON.stringify(candidate)==original,"candidate preserved after negative tests")
 check(registry.validate_definition(candidate,"EXP-003"),"valid profile still accepted")
 var result={"status":"PASS" if failures.is_empty() else "FAIL","checks":checks,"failures":failures,"sample_count":samples,"sampling_interval_seconds":.001,"max_control_step_per_millisecond":max_step,"runtime_sampler":"Unchanged expression_rig.gd _sample","visual_capture":false,"approval":"UNAPPROVED"}
 var file=FileAccess.open(w+"/candidate_checks.json",FileAccess.WRITE);file.store_string(JSON.stringify(result,"  "));file.close();player.free()
 print("CANDIDATE_",result.status," checks=",checks," failures=",failures);quit(0 if failures.is_empty() else 1)

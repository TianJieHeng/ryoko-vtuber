extends SceneTree
# Uses the unchanged production sampler and validation; no native render is requested.
var w=get_script().resource_path.get_base_dir()
var checks=0
var failures=[]
func check(ok,label):
 checks+=1
 if not ok:failures.append(label)
func _initialize():call_deferred("run")
func run():
 var player=load("res://expression_rig.gd").new()
 var registry=load("res://expression_registry.gd").new()
 var candidate=JSON.parse_string(FileAccess.get_file_as_string(w+"/EXP-067.json"))
 var original=JSON.stringify(candidate)
 check(registry.validate_definition(candidate,"EXP-067"),"candidate definition accepted: "+registry.last_error)
 var samples=0
 var previous={}
 for i in range(4801):
  var t=float(i)/1000.0
  var p=player._sample(candidate,t)
  samples+=1
  check(registry.scoped_valid(p),"scope "+str(i))
  check(registry.sealed_mouth_valid(p),"mouth "+str(i))
  for channel in p:
   var bounds=registry.CHANNEL_BOUNDS[channel]
   check(registry.number(p[channel]) and p[channel]>=bounds[0] and p[channel]<=bounds[1],"bounded "+channel+" "+str(i))
  if t<=0.8:check(p.mouth_open==0.0 and p.opening_px==0.0,"sealed anticipation "+str(i))
  if t>.8 and t<=2.5 and not previous.is_empty():
   for channel in ["brow_inner_lift_screen_left","brow_inner_lift_screen_right","opening_px","mouth_open"]:
    check(p[channel]>=previous[channel]-0.0000001,"gradual build "+channel+" "+str(i))
   check(p.mouth_lip_press<=previous.mouth_lip_press+0.0000001,"pressure releases "+str(i))
  if t>=2.5 and t<=3.0:
   for channel in player.CHANNELS:check(is_equal_approx(float(p[channel]),float(candidate.keyframes[5].values.get(channel,0))),"held peak "+channel+" "+str(i))
  previous=p
 for conflict in ["blink_L","blink_R","eye_smile_L","eye_smile_R","gaze_x","gaze_y","gaze_down_extra","aversion_px"]:
  var bad=candidate.duplicate(true);bad.keyframes[5].values[conflict]=0.01
  check(not registry.validate_definition(bad,"EXP-067"),"reject simultaneous opening conflict "+conflict)
  bad=candidate.duplicate(true);bad.keyframes[2].values[conflict]=0.01
  check(not registry.validate_definition(bad,"EXP-067"),"reject adjacent segment opening conflict "+conflict)
 for conflict in ["mouth_width_screen_left","mouth_width_screen_right","mouth_kiss","uneasy_weight"]:
  var bad=candidate.duplicate(true);bad.keyframes[5].values[conflict]=0.1
  check(not registry.validate_definition(bad,"EXP-067"),"reject mouth composition "+conflict)
 for channel in registry.CHANNEL_BOUNDS:
  for value in [float(registry.CHANNEL_BOUNDS[channel][0])-.01,float(registry.CHANNEL_BOUNDS[channel][1])+.01]:
   var bad=candidate.duplicate(true);bad.keyframes[5].values[channel]=value
   check(not registry.validate_definition(bad,"EXP-067"),"reject outside bound "+channel)
 var bad=candidate.duplicate(true);bad.keyframes[5].values["tense_lid"]=0.4
 check(not registry.validate_definition(bad,"EXP-067"),"reject invented anatomy channel")
 check(JSON.stringify(candidate)==original,"candidate unchanged by negative tests")
 check(registry.validate_definition(candidate,"EXP-067"),"valid candidate still accepted")
 check(player._sample(candidate,0.0)==player.neutral_pose(),"neutral start")
 check(player._sample(candidate,4.8)==player.neutral_pose(),"neutral end")
 var result={"status":"PASS" if failures.is_empty() else "FAIL","checks":checks,"failures":failures,"sample_count":samples,"sampling_interval_seconds":0.001,"runtime_sampler":"Unchanged expression_rig.gd _sample","visual_capture":false,"approval":"UNAPPROVED"}
 var file=FileAccess.open(w+"/candidate_checks.json",FileAccess.WRITE);file.store_string(JSON.stringify(result,"  "));file.close()
 player.free()
 print(JSON.stringify(result));quit(0 if failures.is_empty() else 1)

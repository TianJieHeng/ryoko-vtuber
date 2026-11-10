extends SceneTree
class Current:
 extends "res://expression_rig.gd"
 # Exercise production control code; only rendering/face setters are stubbed.
 func _ready():
  registry_ready=registry.load_file();rig_ready=true;current_pose=neutral_pose()
 func _apply_performance_pose(p:Dictionary):current_pose=p.duplicate(true)
 func pose_now()->Dictionary:return current_pose.duplicate(true)
 func displayed_pose()->Dictionary:return pose_now()
 func _write_pose():pass
 func _suspend_auto_blink():pass
 func _restore_auto_blink():pass
class Previous:
 extends "res://historical_capture_metadata/approved27_before_batch36/expression_rig.gd"
 # Exercise production control code; only rendering/face setters are stubbed.
 func _ready():
  registry_ready=registry.load_file();rig_ready=true;current_pose=neutral_pose()
 func _apply_performance_pose(p:Dictionary):current_pose=p.duplicate(true)
 func pose_now()->Dictionary:return current_pose.duplicate(true)
 func displayed_pose()->Dictionary:return pose_now()
 func _write_pose():pass
 func _suspend_auto_blink():pass
 func _restore_auto_blink():pass
var checks=0
var failures=[]
var failure_count=0
var failure_categories={}
var current
var previous
var comparisons=0
var pair_cases=0
var transition_samples=0
var previous_invalid=0
var changed_mouth_samples=0
var changed_new_target_samples=0
const NEW_IDS=["EXP-003","EXP-004","EXP-042","EXP-043","EXP-064","EXP-067","EXP-093","EXP-139","EXP-174"]
var regression_pairs={}
var times=[0.0,0.000000001,.03,.06,.09,.099999999,.1,.100000001,.12,.149999999,.15,.150000001,.18,.199999999,.2,.200000001,.21,.24,.27,.299999999,.3,.300000001,.33]
func _initialize():call_deferred("run")
func check(ok,label):
 checks+=1
 if not ok:
  failure_count+=1
  var category="scoped" if label.ends_with(" scoped") else ("mouth" if label.ends_with(" mouth") else "other")
  failure_categories[category]=failure_categories.get(category,0)+1
  if failures.size()<30:failures.append(label)
func seed_pose(rig,pose):
 rig.current_pose=pose.duplicate(true);rig.active_performance="";rig.release_time=-1;rig.performance_time=0;rig._clear_mouth_bridge()
func valid(p,label):
 check(current.Registry.scoped_valid(p),label+" scoped")
 check(current.Registry.sealed_mouth_valid(p),label+" mouth")
 for key in current.CHANNELS:
  var bounds=current.Registry.CHANNEL_BOUNDS[key]
  check(current.Registry.number(p[key]) and p[key]>=bounds[0] and p[key]<=bounds[1],label+" bounded "+key)
func run():
 current=Current.new();previous=Previous.new();root.add_child(current);root.add_child(previous)
 check(current.registry_ready and previous.registry_ready,"registries ready")
 var entries=current.list_expressions()
 check(entries.size()==36,"36 registry entries")
 # Exact old/new standalone control trajectory at every 30fps frame and each key.
 for entry in entries:
  var definition=current.registry.definition(entry.id);var sample_times=[]
  for i in range(int(ceil(definition.duration*30))+1):sample_times.append(minf(float(i)/30,definition.duration))
  for key in definition.keyframes:sample_times.append(float(key.time))
  sample_times.sort()
  seed_pose(current,current.neutral_pose());seed_pose(previous,previous.neutral_pose())
  check(current.play_expression(entry.id) and previous.play_expression(entry.id),"standalone trigger "+entry.id)
  var last=0.0
  for t in sample_times:
   current.advance(t-last);previous.advance(t-last);last=t
   check(current.pose_now()==previous.pose_now(),"standalone exact "+entry.id+" "+str(t));comparisons+=1
  check(current.pose_now()==current.neutral_pose(),"standalone neutral "+entry.id)
 # Every source/target pair at source keys and segment midpoints, sampled on
 # both sides of 0/.15/.30 bridge boundaries, with release after the handoff.
 for entry in entries:
  var definition=current.registry.definition(entry.id);var source_times=[]
  for i in range(definition.keyframes.size()):
   source_times.append(float(definition.keyframes[i].time))
   if i>0:source_times.append((float(definition.keyframes[i-1].time)+float(definition.keyframes[i].time))*.5)
  for source_time in source_times:
   var source=current.sample_expression(entry.id,source_time)
   for target in entries:
    pair_cases+=1
    var label=entry.id+"@"+str(source_time)+" -> "+target.id
    seed_pose(current,source);seed_pose(previous,source)
    check(current.play_expression(target.id) and previous.play_expression(target.id),label+" trigger")
    check(current.pose_now()==source,label+" continuous")
    var last=0.0
    for t in times:
     current.advance(t-last);previous.advance(t-last);last=t;transition_samples+=1
     var p=current.pose_now();var old=previous.pose_now()
     if target.id not in NEW_IDS:check(p==old,label+" prior-target controls unchanged")
     elif p!=old:changed_new_target_samples+=1
     valid(p,label+"@"+str(t))
     var different=false
     for key in current.CHANNELS:
      if key in current.MOUTH_TRIO:
       if p[key]!=old[key]:different=true
      elif target.id not in NEW_IDS or key not in current.OPENING_CONFLICTS+["opening_px"]:check(p[key]==old[key],label+" unrelated controls unchanged "+key)
     if different:changed_mouth_samples+=1
     if not previous.Registry.sealed_mouth_valid(old):
      previous_invalid+=1;regression_pairs[entry.id+" -> "+target.id]=true
    var before=current.pose_now();check(current.release(),label+" release");check(current.pose_now()==before,label+" release continuous")
    current.advance(.15);valid(current.pose_now(),label+" release .15")
    current.advance(.30000001);check(current.pose_now()==current.neutral_pose(),label+" release neutral")
 var out={"status":"PASS" if failures.is_empty() else "FAIL","checks":checks,"failure_count":failure_count,"failure_categories":failure_categories,"failures":failures,"standalone_exact_samples":comparisons,"source_target_cases":pair_cases,"transition_samples":transition_samples,"old_invalid_mouth_samples":previous_invalid,"changed_mouth_samples":changed_mouth_samples,"changed_new_target_samples":changed_new_target_samples,"old_invalid_pairs":regression_pairs.keys(),"boundary_times":times,"reference_note":"Archived prior27 runtime loads the current production36 registry, testing code parity for all36. This does not claim nine new profiles existed in prior27.","scope":"Actual production advance/trigger/release code with rendering setters stubbed. All36 standalone old/new control equality; all36 pairs at every source key and segment midpoint; dense bridge boundaries, mouth domain, scope, bounds, non-mouth equality and release. Not visual/native parity."}
 var f=FileAccess.open("res://validation/approved_batch36/handoff_boundary_checks.json",FileAccess.WRITE);f.store_string(JSON.stringify(out,"  "));f.close()
 print(JSON.stringify(out));quit(0 if failures.is_empty() else 1)

extends SceneTree
class Current:
 extends "res://expression_rig.gd"
 func _ready():registry_ready=registry.load_file();rig_ready=true;current_pose=neutral_pose()
 func _apply_performance_pose(p:Dictionary):current_pose=p.duplicate(true)
 func pose_now()->Dictionary:return current_pose.duplicate(true)
 func displayed_pose()->Dictionary:return pose_now()
 func _write_pose():pass
 func _suspend_auto_blink():pass
 func _restore_auto_blink():pass
var checks=0
var failures=[]
var prior_samples=0
var trajectory_samples=0
var cross_cases=0
var cross_samples=0
var lifecycle_cases=0
func _initialize():call_deferred("run")
func check(ok,label):
 checks+=1
 if not ok and failures.size()<50:failures.append(label)
func valid(rig,label):
 var p=rig.pose_now()
 check(rig.Registry.scoped_valid(p),label+" scope")
 check(rig.Registry.sealed_mouth_valid(p),label+" mouth")
 for k in rig.CHANNELS:
  var b=rig.Registry.CHANNEL_BOUNDS[k]
  check(rig.Registry.number(p[k]) and p[k]>=b[0] and p[k]<=b[1],label+" bounds "+k)
func run():
 var rig=Current.new();root.add_child(rig)
 var prior=Current.new();root.add_child(prior)
 var cat=JSON.parse_string(FileAccess.get_file_as_string("res://historical_capture_metadata/approved36_before_mental_arithmetic/expressions/registry.json"));var defs={}
 for entry in cat.entries:defs[entry.path]=JSON.parse_string(FileAccess.get_file_as_string(entry.path))
 check(prior.registry.load_catalogue(cat,defs),"load exact prior36 registry")
 check(rig.list_expressions().size()==39 and prior.list_expressions().size()==36,"registry counts")
 for e in prior.list_expressions():
  var d=rig.registry.definition(e.id)
  rig.reset();prior.reset();rig.play_expression(e.id);prior.play_expression(e.id)
  for i in range(int(ceil(d.duration*60))+1):
   var t=minf(float(i)/60,d.duration)
   rig.advance(maxf(0,t-rig.performance_time));prior.advance(maxf(0,t-prior.performance_time))
   check(rig.pose_now()==prior.pose_now(),"prior36 exact standalone "+e.id+" "+str(t));prior_samples+=1
 for pair in [["EXP-129","res://validation/approved_mental_arithmetic/approved_preview/motion_checks.json"],["EXP-041","res://validation/approved_pair38/EXP-041/motion_checks.json"],["EXP-061","res://validation/approved_batch39/EXP-061/motion_checks.json"]]:
  var expected=JSON.parse_string(FileAccess.get_file_as_string(pair[1]))
  rig.reset();rig.play_expression(pair[0])
  for r in expected.records:
   if r.frame>0:rig.advance(maxf(0.0,r.time-rig.performance_time))
   for k in rig.CHANNELS:check(absf(rig.pose_now()[k]-r.pose[k])<.0000001,"review pose parity "+k+" "+str(r.frame))
   valid(rig,"approved new trajectory");trajectory_samples+=1
 for source in rig.list_expressions():
  var d=rig.registry.definition(source.id);var times=[]
  for i in range(d.keyframes.size()):
   times.append(d.keyframes[i].time)
   if i>0:times.append((d.keyframes[i].time+d.keyframes[i-1].time)*.5)
  for target in rig.list_expressions():
   if source.id not in ["EXP-129","EXP-041","EXP-061"] and target.id not in ["EXP-129","EXP-041","EXP-061"]:continue
   for source_time in times:
    rig.reset();rig.play_expression(source.id);rig.advance(source_time)
    var before=rig.pose_now();check(rig.play_expression(target.id),"cross target");check(rig.pose_now()==before,"cross C0")
    var last=0.0
    for t in [0.0,.000001,.075,.149999,.15,.150001,.225,.299999,.3,.300001,.61]:
     rig.advance(t-last);last=t;valid(rig,"cross "+source.id+" -> "+target.id);cross_samples+=1
    rig.advance(rig.registry.definition(target.id).duration)
    check(rig.pose_now()==rig.neutral_pose(),"cross end neutral");cross_cases+=1
    for action in ["release","restart"]:
     rig.reset();rig.play_expression(source.id);rig.advance(source_time);rig.play_expression(target.id);rig.advance(.15)
     before=rig.pose_now()
     if action=="release":check(rig.release(),"release")
     else:check(rig.play_expression(target.id),"restart")
     check(rig.pose_now()==before,"interruption C0");rig.advance(.15);valid(rig,action+" midpoint");rig.advance(10)
     check(rig.pose_now()==rig.neutral_pose() and rig.active_performance=="" and rig.release_time<0,"interruption completed neutral");lifecycle_cases+=1
 var out={"status":"PASS" if failures.is_empty() else "FAIL","checks":checks,"failures":failures,"prior36_standalone_samples_at_60hz":prior_samples,"approved_preview_pose_samples":trajectory_samples,"directed_cross_key_midpoint_cases":cross_cases,"cross_boundary_samples":cross_samples,"interrupted_lifecycle_cases":lifecycle_cases,"runtime_sha256":FileAccess.get_sha256("res://expression_rig.gd"),"scope":"Unmodified production controller with rendering setters stubbed. Exact prior36 standalone controls versus archived registry at 60 Hz; all363 approved EXP-129, EXP-041 and EXP-061 pose records; every source key/midpoint in both directions involving EXP-129, EXP-041 or EXP-061 against all39 including self, 11 handoff checkpoints and mid-handoff release/restart. Not rendered visual evidence."}
 var f=FileAccess.open("res://validation/approved_batch39/dense_checks.json",FileAccess.WRITE);f.store_string(JSON.stringify(out,"  "));f.close();print(JSON.stringify(out));quit(0 if failures.is_empty() else 1)

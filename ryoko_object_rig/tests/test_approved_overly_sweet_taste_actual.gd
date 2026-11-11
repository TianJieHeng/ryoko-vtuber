extends SceneTree
# Prepared for future authorized Godot execution. NOT RUN during Python-only integration.
const NEW_IDS=["EXP-091"]
const EXPECTED={"EXP-091":"res://validation/approved_overly_sweet_taste/review_sources/capture/evidence.json"}
var rig
var checks=0
var failures=[]
var trajectory_samples=0
var lifecycle_cases=0
var cross_cases=0
var cross_samples=0
var baseline
var head
var body
func _initialize():call_deferred("run")
func check(ok,label):
 checks+=1
 if not ok and failures.size()<60:failures.append(label)
func valid(label):
 var p=rig.pose_now()
 check(rig.Registry.scoped_valid(p),label+" scope")
 check(rig.Registry.sealed_mouth_valid(p),label+" mouth")
 check(rig.head.transform==head and rig.body.transform==body,label+" fixed body")
 for k in rig.CHANNELS:
  var b=rig.Registry.CHANNEL_BOUNDS[k]
  check(rig.Registry.number(p[k]) and p[k]>=b[0] and p[k]<=b[1],label+" bounds "+k)
func neutral(label):
 check(rig.face.snapshot()==baseline,label+" exact face neutral")
 check(rig.pose_now()==rig.neutral_pose(),label+" exact controls neutral")
 check(rig.active_performance=="" and rig.release_time<0,label+" ownership cleared")
func run():
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false);rig.reset()
 check(rig.rig_ready and rig.registry_ready,"ready");check(rig.list_expressions().size()==47,"production47 registry")
 if not failures.is_empty():quit(2);return
 baseline=rig.face.snapshot();head=rig.head.transform;body=rig.body.transform
 for id in NEW_IDS:
  var e=JSON.parse_string(FileAccess.get_file_as_string(EXPECTED[id]))
  rig.reset();check(rig.play_expression(id),"play "+id)
  for record in e.records:
   if record.frame>0:check(rig.advance(maxf(0,record.time-rig.performance_time)),"advance")
   valid("trajectory "+id+" "+str(record.frame))
   for k in rig.CHANNELS:check(absf(rig.pose_now()[k]-record.pose[k])<.0000001,"approved preview pose "+id+" "+k)
   check(not rig.auto_blink,"authored blink ownership");trajectory_samples+=1
  neutral("complete "+id)
  for entry in rig.list_expressions():
   if entry.id!=id:continue
   for a in entry.aliases:
    rig.reset();check(rig.play_expression(a) and rig.performance.id==id,"registered alias "+a)
  for key in rig.registry.definition(id).keyframes:
   rig.reset();rig.play_expression(id);rig.advance(key.time)
   var before=rig.displayed_pose();check(rig.play_expression(id) and rig.displayed_pose()==before,"restart C0 "+id)
   rig.advance(.15);valid("restart");before=rig.displayed_pose()
   check(rig.release() and rig.displayed_pose()==before,"release C0");rig.advance(.15);valid("release")
   before=rig.displayed_pose();check(rig.release() and rig.displayed_pose()==before,"repeated release C0")
   rig.advance(.4500001);neutral("release complete "+id)
   rig.play_expression(id);rig.advance(key.time);rig.reset();neutral("reset "+id);lifecycle_cases+=1
 for source in rig.list_expressions():
  for target in rig.list_expressions():
   if source.id not in NEW_IDS and target.id not in NEW_IDS:continue
   rig.reset();check(rig.play_expression(source.id),"cross source");rig.advance(rig.performance.duration*.5)
   var before=rig.displayed_pose();check(rig.play_expression(target.id) and rig.displayed_pose()==before,"cross C0 "+source.id+" -> "+target.id)
   var last=0.0
   for t in [0.0,.000001,.075,.149999,.15,.150001,.225,.299999,.3,.300001,.61]:
    check(rig.advance(t-last),"cross advance");last=t;valid("cross "+source.id+" -> "+target.id);cross_samples+=1
   rig.advance(rig.registry.definition(target.id).duration);neutral("cross complete");cross_cases+=1
  print("EXP091_CROSS_DONE ",source.id)
 var out={"status":"PASS" if failures.is_empty() else "FAIL","checks":checks,"failures":failures,"production_profile_count":47,"new_profiles":NEW_IDS,"trajectory_samples":trajectory_samples,"lifecycle_key_cases":lifecycle_cases,"actual_object_directed_cross_cases":cross_cases,"actual_object_cross_samples":cross_samples,"runtime_sha256":FileAccess.get_sha256("res://expression_rig.gd"),"scope":"Actual production scene and face setters; full121 chronological frame states versus approved records, aliases, keyframe restart/repeated release/reset, all93 directed pairs involving a new profile at11 handoff checkpoints, and exact face/control neutral completion. No rendering or live pacing claim.","visual_capture":false}
 var f=FileAccess.open("res://validation/approved_overly_sweet_taste/actual_object_checks.json",FileAccess.WRITE);f.store_string(JSON.stringify(out,"  "));f.close();print(JSON.stringify(out));quit(0 if failures.is_empty() else 1)

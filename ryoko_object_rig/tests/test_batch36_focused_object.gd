extends SceneTree
var rig
var checks=0
var failures=[]
var failure_count=0
var trajectory_samples=0
var alias_cases=0
var lifecycle_cases=0
var cross_cases=0
var cross_samples=0
var baseline
var head
var body
func _initialize():call_deferred("run")
func check(ok,label):
 checks+=1
 if not ok:
  failure_count+=1
  if failures.size()<40:failures.append(label)
func valid(label):
 var p=rig.pose_now()
 check(rig.Registry.scoped_valid(p),label+" scope")
 check(rig.Registry.sealed_mouth_valid(p),label+" mouth")
 for k in rig.CHANNELS:
  var b=rig.Registry.CHANNEL_BOUNDS[k]
  check(rig.Registry.number(p[k]) and p[k]>=b[0] and p[k]<=b[1],label+" bounded "+k)
 check(rig.head.transform==head and rig.body.transform==body,label+" fixed head/body")
func neutral(label,blink=false):
 check(rig.pose_now()==rig.neutral_pose(),label+" control neutral")
 check(rig.face.snapshot()==baseline,label+" actual face exact neutral")
 check(rig.active_performance=="" and rig.release_time<0,label+" ownership cleared")
 check(rig.auto_blink==blink and not rig.auto_blink_pending_restore,label+" blink restored")
 valid(label)
func run():
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false);rig.reset()
 check(rig.rig_ready and rig.registry_ready,"ready")
 if not rig.rig_ready or not rig.registry_ready:quit(2);return
 baseline=rig.face.snapshot();head=rig.head.transform;body=rig.body.transform
 var entries=rig.list_expressions()
 check(entries.size()==36,"exact production36 count")
 var seen={}
 for e in entries:
  check(not seen.has(e.id),"unique ID "+e.id);seen[e.id]=true
  var d=rig.registry.definition(e.id)
  for a in e.aliases:
   rig.reset();check(rig.registry.resolve(a)==e.id,"alias resolves "+a)
   check(rig.play_expression(a) and rig.performance.id==e.id,"alias plays "+a);alias_cases+=1
  for hz in [1]:
   var times=[]
   for fraction in [0.0,.25,.5,.85,1.0]:times.append(d.duration*fraction)

   times.sort()
   rig.reset();check(rig.play_expression(e.id),"play "+e.id)
   var last=0.0
   for t in times:
    check(rig.advance(t-last),"advance "+e.id);last=t;trajectory_samples+=1
    valid(e.id+"@"+str(t))
    var p=rig.pose_now();var raw=rig.sample_expression(e.id,t)
    for k in rig.CHANNELS:
     var expected=raw[k]*smoothstep(0.0,.3,t) if t<.3 else raw[k]
     check(abs(p[k]-expected)<.000002,"trajectory "+e.id+" "+k)
   neutral(e.id+" complete")
  print("FOCUSED_TRAJECTORY_DONE ",e.id)
  for blink in [false]:
   for fraction in [.35]:
    rig.reset();rig.apply_controls({"auto_blink":blink});rig.play_expression(e.id);rig.advance(d.duration*fraction)
    var before=rig.displayed_pose();check(rig.play_expression(e.id) and rig.displayed_pose()==before,"restart C0 "+e.id)
    rig.advance(.15);valid("restart midpoint "+e.id)
    before=rig.displayed_pose();check(rig.release() and rig.displayed_pose()==before,"release C0 "+e.id)
    rig.advance(.15);valid("release midpoint "+e.id)
    before=rig.displayed_pose();check(rig.release() and rig.displayed_pose()==before,"repeated release C0 "+e.id)
    rig.advance(.4500001);neutral("release "+e.id,blink)
    rig.play_expression(e.id);rig.advance(d.duration*fraction);rig.reset();neutral("reset "+e.id)
    lifecycle_cases+=1
 # Full actual rig cross-product, including self transitions. Dense combinatorial
 # source-key/midpoint coverage is provided separately by handoff test.
 for source in entries:
  for target in entries:
   if not (source.id in ["EXP-163","EXP-144","EXP-197"] and target.id in ["EXP-064","EXP-004"]):continue
   rig.reset();rig.play_expression(source.id);rig.advance(rig.registry.definition(source.id).duration*.5)
   var before=rig.displayed_pose()
   check(rig.play_expression(target.id) and rig.displayed_pose()==before,"cross C0 "+source.id+" -> "+target.id)
   cross_cases+=1
   var last=0.0
   for t in [0.0,.000001,.075,.149999,.15,.150001,.225,.299999,.3,.300001,.61]:
    rig.advance(t-last);last=t;valid("actual cross "+source.id+" -> "+target.id);cross_samples+=1
   rig.advance(rig.registry.definition(target.id).duration);neutral("cross complete")
 var result={"status":"PASS" if failure_count==0 else "FAIL","checks":checks,"failure_count":failure_count,"failures":failures,"profile_count":entries.size(),"trajectory_samples":trajectory_samples,"trajectory_sample_fractions":[0.0,.25,.5,.85,1.0],"alias_cases":alias_cases,"lifecycle_cases":lifecycle_cases,"actual_rig_directed_cross_cases":cross_cases,"actual_rig_cross_samples":cross_samples,"scope":"Instantiated production scene with real face setters; fixed head/body, bounded/domain-safe controls, five trajectory samples per expression, all aliases, restarts, repeated releases, reset and exact face snapshot neutral; six representative directed cross-domain pairs at midpoint. Headless state checks, not rendered visual or native-app parity."}
 var f=FileAccess.open("res://validation/approved_batch36/focused_object_checks.json",FileAccess.WRITE);f.store_string(JSON.stringify(result,"  "));f.close()
 print(JSON.stringify(result));quit(0 if failure_count==0 else 1)

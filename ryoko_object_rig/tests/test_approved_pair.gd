extends SceneTree
var rig
var failures=[]
var checks=0
func _initialize():call_deferred("run")
func check(ok,label):
 checks+=1
 if not ok:failures.append(label);push_error(label)
func safe(label):
 check(rig.Registry.scoped_valid(rig.pose_now()),label+" composition")
 check(rig.Registry.sealed_mouth_valid(rig.pose_now()),label+" mouth domain")
 check(not(rig.scoped_parts.mouth.modulate.a>0 and rig.face.mouth_kiss>0),label+" mouth owner")
func run():
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 check(rig.rig_ready and rig.registry_ready,"ready "+rig.last_error)
 if not failures.is_empty():quit(1);return
 rig.reset();var neutral=rig.face.snapshot();var head=rig.head.transform;var body=rig.body.transform
 check(rig.list_expressions().size()==24,"24 registry entries")
 for id in ["EXP-144","EXP-197"]:
  rig.reset();check(rig.play_expression(id),"play "+id)
  var count=int(round(rig.performance.duration*30))
  for i in range(count+1):
   if i>0:rig.advance(1.0/30)
   safe(id+" frame "+str(i))
   check(rig.head.transform==head and rig.body.transform==body,"fixed head/body")
   if id=="EXP-144":check(rig.face.mouth_kiss==0 and not rig.face.kiss_sprite.visible,"144 kiss hidden")
   await process_frame
  rig.advance(.01)
  check(rig.pose_now()==rig.neutral_pose() and rig.face.snapshot()==neutral,"cycle neutral "+id)
  for t in ([1.1,2.4,3.9] if id=="EXP-144" else [1.0,3.0,5.8]):
   rig.reset();rig.play_expression(id);rig.advance(t);rig.release()
   for step in range(16):rig.advance(.03);safe("release");await process_frame
   check(rig.pose_now()==rig.neutral_pose() and rig.face.snapshot()==neutral,"release neutral")
   rig.play_expression(id);rig.advance(t);rig.play_expression(id)
   for step in range(11):rig.advance(.03);safe("retrigger");await process_frame
   rig.reset();check(rig.face.snapshot()==neutral,"retrigger reset")
 for entry in rig.list_expressions():
  for pair in [["EXP-144",entry.id],[entry.id,"EXP-144"],["EXP-197",entry.id],[entry.id,"EXP-197"]]:
   rig.reset();rig.play_expression(pair[0]);rig.advance(1.1 if pair[0]=="EXP-144" else rig.performance.duration*.5)
   rig.play_expression(pair[1])
   for step in range(11):rig.advance(.03);safe("handoff "+str(pair));await process_frame
   rig.reset();check(rig.face.snapshot()==neutral,"handoff neutral")
 # Manual takeover clears scoped parts, invalid requests are atomic.
 rig.play_expression("EXP-144");rig.advance(1.1);var before=rig.get_state()
 check(not rig.apply_controls({"opening_px":5}),"private component rejects manual")
 check(rig.get_state().controls==before.controls,"rejection atomic")
 check(rig.apply_controls({"blink_L":.5}),"manual takeover")
 check(not rig.has_scoped(rig.pose_now()),"manual clears components")
 rig.reset();check(rig.face.snapshot()==neutral,"final neutral")
 var out={"status":"PASS" if failures.is_empty() else "FAIL","checks":checks,"failures":failures,"registry":rig.list_expressions(),"scope":"Both full 30fps cycles, repeated/interrupted flows, bidirectional handoffs with all profiles, neutral state, manual ownership. Focused, not full legacy suite."}
 var f=FileAccess.open("/tmp/ryoko_pair_integration/state_checks.json",FileAccess.WRITE);f.store_string(JSON.stringify(out,"  "));f.close()
 print("APPROVED_PAIR ",out.status," checks=",checks);quit(0 if failures.is_empty() else 1)

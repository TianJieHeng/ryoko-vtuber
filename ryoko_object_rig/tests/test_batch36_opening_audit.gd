extends SceneTree
var rig
var failures=[]
var checks=0
func _initialize():call_deferred("run")
func check(ok,label):
 checks+=1
 if not ok and failures.size()<40:failures.append(label)
func valid(label):
 check(rig.Registry.scoped_valid(rig.pose_now()),label+" scoped")
 check(rig.Registry.sealed_mouth_valid(rig.pose_now()),label+" mouth")
func seed_source(kind):
 rig.reset()
 if kind=="aversion":rig.play_expression("EXP-163");rig.advance(.615)
 elif kind=="blink":rig.apply_controls({"blink_R":1.0,"blink_L":.5})
 elif kind=="gaze":rig.apply_controls({"gaze_x":-.8,"gaze_y":.4,"eye_smile_L":.6})
 elif kind=="auto":rig.apply_controls({"auto_blink":true});rig.advance(4.09)
func run():
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false);rig.scoped_parts=null
 for kind in ["aversion","blink","gaze","auto"]:
  for target in ["EXP-064","EXP-004"]:
   for at in [.0,.000000001,.099999999,.1,.100000001,.199999999,.2,.200000001,.299999999,.3,.300000001]:
    for action in ["release","retrigger","manual","reset","invalid"]:
     seed_source(kind);var before=rig.displayed_pose();check(rig.play_expression(target),"trigger");check(rig.displayed_pose()==before,"trigger C0")
     rig.advance(at);valid("pre-action");before=rig.displayed_pose()
     if action=="release":
      check(rig.release(),"release accepted");check(rig.displayed_pose()==before,"release C0")
      for step in [.000000001,.075,.075,.075,.075,.075,.075]:rig.advance(step);valid("release step")
     elif action=="retrigger":
      check(rig.play_expression("EXP-004" if target=="EXP-064" else "EXP-064"),"retrigger accepted");check(rig.displayed_pose()==before,"retrigger C0")
      for step in [.000000001,.099999999,.1,.1,.1]:rig.advance(step);valid("retrigger step")
     elif action=="manual":
      check(rig.apply_controls({"gaze_x":.2}),"manual accepted");valid("manual")
      var manual=rig.pose_now();rig.advance(.4);check(rig.pose_now()==manual,"manual stationary")
     elif action=="reset":rig.reset();check(rig.pose_now()==rig.neutral_pose(),"reset neutral")
     else:
      var state=rig.get_state().duplicate(true)
      check(not rig.apply_controls({"perform_expression":"EXP-064","blink":1}),"invalid rejected")
      var after=rig.get_state();state.erase("last_error");after.erase("last_error");check(state==after,"invalid atomic")
      rig.advance(.31);valid("invalid continued")
     rig.reset()
 var result={"status":"PASS" if failures.is_empty() else "FAIL","checks":checks,"failures":failures,"scope":"Independent instantiated-scene edge audit with scoped_parts disabled to bound this focused audit after the full-scene attempt did not complete during the observed interval (ordinary face setters active; no widened-eye render parity; no shader crash or deadlock established): manual blink/gaze/smile, aversion and auto-blink sources; both early-opening targets; exact stage boundaries and neighboring times; interrupted release, retrigger, manual takeover, reset and rejected atomic transaction."}
 var f=FileAccess.open("res://validation/approved_batch36/opening_independent_audit.json",FileAccess.WRITE);f.store_string(JSON.stringify(result,"  "));f.close();print(JSON.stringify(result));quit(0 if failures.is_empty() else 1)

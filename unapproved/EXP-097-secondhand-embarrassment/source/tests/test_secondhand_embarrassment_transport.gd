extends SceneTree
## In-process protocol dispatch only; no socket/listener or external integration claim.
var rig
var bridge
var request_id=0
var checks=0
var failures=[]
func _initialize():call_deferred("run")
func check(ok,label):
 checks+=1
 if not ok:
  failures.append(label)
  if failures.size()<15:push_error(label)
func request(verb,args={},session_id=1):
 request_id+=1
 var packet={"protocol":1,"id":request_id,"verb":verb,"args":args}
 if verb in bridge.WRITE_VERBS:packet.session=session_id
 bridge.outgoing.clear();bridge.dispatch(JSON.stringify(packet).to_utf8_buffer())
 var reply=JSON.parse_string(bridge.outgoing.get_string_from_utf8().strip_edges());bridge.outgoing.clear()
 check(reply is Dictionary and reply.id==request_id,"bounded matching reply")
 return reply
func state():
 var s=rig.get_state();s.erase("last_error");s.face=rig.face.snapshot();return s
func run():
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 check(rig.rig_ready and rig.registry_ready,"ready")
 if not rig.rig_ready or not rig.registry_ready:quit(2);return
 bridge=load("res://control_bridge.gd").new();bridge.rig=rig;bridge.session=1;bridge.external_enabled=true
 check(not bridge.enabled and not bridge.server.is_listening(),"no socket started")
 var r=request("capabilities");check(r.ok,"discovery")
 for k in rig.Registry.CHANNEL_BOUNDS:check(r.result.controls[k]==rig.Registry.CHANNEL_BOUNDS[k],"unchanged bounded controls "+k)
 r=request("list_expressions");check(r.ok and r.result.size()==20,"twenty local entries transported")
 var map=JSON.parse_string(FileAccess.get_file_as_string("res://source_references/secondhand_embarrassment_source_anchor_map.json"))
 for alias in ["EXP-097","secondhand-embarrassment","secondhand_embarrassment"]:
  for anchor in map.anchors:
   check(request("reset").ok,"transport reset")
   check(request("play_expression",{"expression_id":alias}).ok,"transport trigger alias")
   rig.advance(anchor.time)
   r=request("get_state");check(r.ok,"state read")
   for k in rig.CHANNELS:
    check(absf(r.result.rig.controls[k]-anchor.values[k])<.000001,"accepted anchor in transported state "+k)
    check(absf(rig.face.snapshot().mouth_opening)<.000001,"actual sealed mouth")
   check(request("release").ok,"transport release");rig.advance(.45)
   check(rig.pose_now()==rig.neutral_pose(),"transport release exact neutral")
 for origin in [.52,1.08,1.44,1.66,2.32]:
  request("reset");request("play_expression",{"expression_id":"EXP-097"});rig.advance(origin)
  for bad in [{"mouth_open":.1},{"blink_R":1.01},{"eye_smile_L":true},{"unknown":0},{"perform_expression":"EXP-097","reset":true}]:
   # Opening can be legal where width is exactly zero; test overlap atomically only during width-bearing states.
   if bad.has("mouth_open") and rig.pose_now().mouth_width_screen_left==0 and rig.pose_now().mouth_width_screen_right==0:continue
   var before=state();r=request("apply_controls",bad)
   check(not r.ok,"invalid transport rejected");check(state()==before,"invalid transport atomic")
  var before=state();r=request("reset",{},2);check(not r.ok and state()==before,"stale session cannot reset")
  check(request("apply_controls",{"mouth_corner_lift_screen_right":.2}).ok,"manual ownership via dispatch")
  var held=rig.pose_now();rig.advance(5);check(rig.pose_now()==held and rig.active_performance=="","manual holds")
 request("reset");check(rig.pose_now()==rig.neutral_pose(),"final exact reset")
 check(not bridge.enabled and not bridge.server.is_listening(),"no listener ever started");bridge.free()
 var out=""
 for a in OS.get_cmdline_user_args():
  if a.begins_with("--output="):out=a.trim_prefix("--output=")
 if out!="":
  var f=FileAccess.open(out,FileAccess.WRITE);f.store_string(JSON.stringify({"status":"PASS" if failures.is_empty() else "FAIL","checks":checks,"failures":failures,"socket_test_performed":false,"scope":"in-process existing protocol dispatch"},"  "));f.close()
 print("SECONDHAND_EMBARRASSMENT_TRANSPORT checks=",checks," failures=",failures.size());quit(0 if failures.is_empty() else 1)

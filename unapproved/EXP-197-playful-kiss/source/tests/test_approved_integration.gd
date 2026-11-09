extends SceneTree
const IDS=["EXP-163","EXP-005","EXP-001","EXP-006","EXP-107","EXP-007","EXP-002","EXP-152","EXP-160","EXP-177","EXP-164","EXP-021","EXP-158","EXP-181","EXP-102","EXP-116","EXP-050","EXP-186"]
const OLD=["EXP-163","EXP-005","EXP-001","EXP-006","EXP-107","EXP-007","EXP-002","EXP-152","EXP-160","EXP-177","EXP-164","EXP-021"]
const NEW=["EXP-158","EXP-181","EXP-102","EXP-116","EXP-050","EXP-186"]
const ALIASES={"EXP-163":["yawn"],"EXP-005":["hearty-laughter","laugh"],"EXP-001":["bright_welcome"],"EXP-006":["suppressed-giggle","giggle"],"EXP-107":["confident-reassurance","reassure"],"EXP-007":["relieved-smile","relief"],"EXP-002":["affectionate-warmth","affection"],"EXP-152":["private-pride","pride"],"EXP-160":["shy-laughter","shy_laughter"],"EXP-177":["meditative-calm","meditate"],"EXP-164":["fighting-sleep","fighting_sleep"],"EXP-021":["quiet-sadness","quiet_sadness"],"EXP-158":["post-confession-shyness","post_confession_shyness"],"EXP-181":["cheeky-wink","cheeky_wink"],"EXP-102":["knowing-smirk","knowing_smirk"],"EXP-116":["confident-denial","confident_denial"],"EXP-050":["frustrated-pout","frustrated_pout"],"EXP-186":["smug-cat-smile","smug_cat_smile"]}
const EXTRA=["mouth_corner_lift_screen_left","mouth_corner_lift_screen_right","mouth_width_screen_left","mouth_width_screen_right"]
const TRIO=["mouth_open","mouth_width_screen_left","mouth_width_screen_right"]
var rig
var checks=0
var failures=[]
var ordered_handoffs=0
var staged_handoffs=0
var transition_samples=0
var lifecycle_cases=0
func _initialize():call_deferred("run")
func check(ok,label):
 checks+=1
 if not ok:
  failures.append(label)
  if failures.size()<20:push_error(label)
func state():
 var s=rig.get_state();s.erase("last_error");s.face=rig.face.snapshot();s.restart=rig.restart_pose.duplicate(true);s.release=rig.release_pose.duplicate(true);s.elapsed=rig.elapsed;return s
func domain(p):return p.mouth_open==0 or (p.mouth_width_screen_left==0 and p.mouth_width_screen_right==0)
func neutral(wanted):
 check(rig.pose_now()==rig.neutral_pose() and rig.active_performance=="" and rig.release_time<0,"exact settled neutral ownership")
 check(rig.auto_blink==wanted and not rig.auto_blink_pending_restore,"settled blink intent")
func mode_for(source,d):
 var width=false;var opening=false
 for f in d.keyframes:
  width=width or f.values.get("mouth_width_screen_left",0)>0 or f.values.get("mouth_width_screen_right",0)>0
  opening=opening or f.values.get("mouth_open",0)>0
 var sw=source.mouth_width_screen_left>0 or source.mouth_width_screen_right>0
 if not sw and not width:return "legacy"
 return "staged" if (sw and opening) or (source.mouth_open>0 and width) else "bounded_direct"
func expected(source,d,t,mode):
 var target=rig.sample_expression(d.id,t);var out=target.duplicate(true)
 if t<d.duration and t<.3:
  var w=smoothstep(0.0,.3,t)
  for k in rig.CHANNELS:out[k]=lerpf(source.get(k,0),target[k],w)
 if mode!="legacy" and t<minf(.3,d.duration):
  var u=t/minf(.3,d.duration)
  for k in TRIO:
   if mode=="bounded_direct":out[k]=lerpf(source[k],target[k],smoothstep(0.0,1.0,u))
   elif u<=.5:out[k]=source[k]*(1.0-smoothstep(0.0,.5,u))
   else:out[k]=target[k]*smoothstep(.5,1.0,u)
 return out
func verify_transition(source,target,t,mode):
 var d=rig.registry.definition(target);var p=rig.pose_now();var want=expected(source,d,t,mode)
 check(domain(p),"strict width/open domain")
 for k in rig.CHANNELS:
  check(is_finite(p[k]) and abs(p[k]-want[k])<.000002,"whole-pose transition rule "+k)
 check(rig.mouth_transition_state().mode==mode,"trigger-fixed bridge mode")
 if mode=="staged" and t==.15:
  for k in TRIO:check(p[k]==0,"staged zero midpoint")
 transition_samples+=1
func strongest_time(id):
 var best=0.0;var strength=-1.0
 for f in rig.registry.definition(id).keyframes:
  var total=0.0
  for v in f.values.values():total+=abs(float(v))
  if total>strength:strength=total;best=f.time
 return best
func run():
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 check(rig.rig_ready and rig.registry_ready,"ready")
 if not rig.rig_ready or not rig.registry_ready:quit(2);return
 var ids=[]
 for e in rig.list_expressions():
  ids.append(e.id);check(e.aliases==ALIASES[e.id],"exact approved aliases")
  for a in ALIASES[e.id]:check(rig.registry.resolve(a)==e.id,"approved alias resolves")
 check(ids==IDS,"literal eighteen approved IDs and order")
 for id in ["EXP-003","EXP-097","EXP-139","EXP-170","EXP-153","EXP-161"]:check(rig.registry.resolve(id)=="","excluded unapproved or unfinished profile")
 for id in OLD:
  for f in rig.registry.definition(id).keyframes:
   for k in EXTRA:check(f.values.get(k,0)==0 and rig.sample_expression(id,f.time)[k]==0,"old twelve default-zero new axes")
 for id in IDS:
  var d=rig.registry.definition(id)
  for hz in [30,60]:
   rig.reset();rig.play_expression(id)
   for i in range(int(ceil(d.duration*hz))+1):
    var t=minf(float(i)/hz,d.duration)
    if i>0:rig.advance(t-minf(float(i-1)/hz,d.duration))
    var p=rig.pose_now();var raw=rig.sample_expression(id,t)
    for k in rig.CHANNELS:
     var v=raw[k]*smoothstep(0.0,.3,t) if t<.3 else raw[k]
     check(is_finite(p[k]) and abs(p[k]-v)<.000002,"all actual approved trajectories")
     if id in OLD and k in EXTRA:check(p[k]==0,"old trajectory extra channel zero")
    check(domain(p),"authored trajectory strict domain")
   neutral(false)
 # Every ordered source/destination including self, meaningful peak and recovery, both blink policies.
 for source_id in IDS:
  var source_d=rig.registry.definition(source_id)
  for target in IDS:
   for blink in [false,true]:
    for origin in [strongest_time(source_id),source_d.duration*.82]:
     rig.reset();rig.apply_controls({"auto_blink":blink});rig.play_expression(source_id);rig.advance(origin)
     var before=rig.displayed_pose();check(before!=rig.neutral_pose(),"meaningful source pose")
     check(rig.play_expression(target) and rig.displayed_pose()==before,"ordered handover C0")
     var mode=mode_for(before,rig.registry.definition(target));ordered_handoffs+=1
     if mode=="staged":staged_handoffs+=1
     var last=0.0
     for t in [0.0,.000001,.075,.149999,.15,.150001,.225,.299999,.3,.300001,.61]:
      rig.advance(t-last);last=t;verify_transition(before,target,t,mode)
     rig.advance(rig.registry.definition(target).duration);neutral(blink)
 # Every new expression lifecycle and state rejection, including an interrupted staged handover.
 for id in NEW:
  for blink in [false,true]:
   for mode in ["active","release","incoming_open","incoming_width"]:
    rig.reset();rig.apply_controls({"auto_blink":blink})
    if mode=="incoming_open":rig.apply_controls({"mouth_open":.8})
    if mode=="incoming_width":rig.apply_controls({"mouth_width_screen_left":.7,"mouth_width_screen_right":.3})
    check(rig.auto_blink==blink and not rig.auto_blink_pending_restore,"idle manual domain setup preserves requested blink")
    rig.play_expression(id);rig.advance(.075 if mode.begins_with("incoming") else strongest_time(id))
    check(not rig.auto_blink and rig.auto_blink_pending_restore==blink,"trigger suspends and saves requested idle blink")
    if mode=="release":rig.release();rig.advance(.1)
    for k in rig.Registry.CHANNEL_BOUNDS:
     var bounds=rig.Registry.CHANNEL_BOUNDS[k]
     for bad in [bounds[0]-.000001,bounds[1]+.000001,NAN,INF,-INF,true,"1",null]:
      var before=state();check(not rig.apply_controls({"reset":true,k:bad}),"invalid typed transaction rejected");check(state()==before,"invalid transaction atomic")
    var before=rig.displayed_pose();check(rig.release() and rig.displayed_pose()==before,"release C0")
    rig.advance(.1);before=rig.displayed_pose();check(rig.release() and rig.displayed_pose()==before,"repeated release C0")
    rig.advance(.45);neutral(blink)
    lifecycle_cases+=1
  rig.reset();rig.apply_controls({"auto_blink":true});rig.play_expression(id);rig.advance(strongest_time(id))
  check(not rig.auto_blink and rig.auto_blink_pending_restore,"active expression suspends enabled blink")
  check(rig.apply_controls({"mouth_open":.25,"mouth_width_screen_left":0.0,"mouth_width_screen_right":0.0}),"atomic explicit open takeover")
  check(not rig.auto_blink and not rig.auto_blink_pending_restore,"active manual takeover cancels pending restoration")
  var held=state();check(not rig.apply_controls({"mouth_width_screen_left":.1}),"retained opening rejects width");check(state()==held,"manual domain rejection atomic")
  check(rig.apply_controls({"mouth_open":0.0,"mouth_width_screen_left":.6}),"atomic explicit sealed takeover")
  held=state();check(not rig.apply_controls({"mouth_open":.1}),"retained width rejects opening");check(state()==held,"sealed rejection atomic")
  var pose=rig.pose_now();rig.advance(10);check(rig.pose_now()==pose and rig.active_performance=="" and not rig.auto_blink_pending_restore and not rig.auto_blink,"manual persists with cancelled blink restoration")
  rig.reset();neutral(false)
 check(ordered_handoffs==1296 and staged_handoffs>0,"complete ordered matrix with actual staged cases")
 var out=""
 for a in OS.get_cmdline_user_args():
  if a.begins_with("--output="):out=a.trim_prefix("--output=")
 var result={"status":"PASS" if failures.is_empty() else "FAIL","checks":checks,"failures":failures,"ordered_handoffs":ordered_handoffs,"staged_handoffs":staged_handoffs,"transition_samples":transition_samples,"lifecycle_cases":lifecycle_cases,"approved_ids":IDS}
 if not out.is_empty():
  var f=FileAccess.open(out,FileAccess.WRITE);f.store_string(JSON.stringify(result,"  "));f.close()
 print("APPROVED_INTEGRATION checks=",checks," failures=",failures.size()," ordered_handoffs=",ordered_handoffs," staged_handoffs=",staged_handoffs);quit(0 if failures.is_empty() else 1)

extends SceneTree
# Dense numeric sampler and live lifecycle checks. No native renderer or runtime edits.
var w=get_script().resource_path.get_base_dir()
var checks=0
var failures=[]
var rig
const ID="EXP-093"
const ACTING=["brow_screen_left","brow_screen_right","brow_tilt_screen_left","brow_tilt_screen_right","blink_L","blink_R","mouth_purse","mouth_open"]
func check(ok,label):
 checks+=1
 if not ok:failures.append(label)
func _initialize():call_deferred("run")
func valid_pose(p,label):
 check(rig.Registry.scoped_valid(p),label+" scoped")
 check(rig.Registry.sealed_mouth_valid(p),label+" mouth domain")
 for k in p:
  var bounds=rig.Registry.CHANNEL_BOUNDS[k]
  check(rig.Registry.number(p[k]) and p[k]>=bounds[0] and p[k]<=bounds[1],label+" bound "+k)
func run():
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false);rig.auto_blink=false
 check(rig.rig_ready and rig.registry_ready,"ready")
 if not failures.is_empty():quit(1);return
 rig.reset();var neutral=rig.face.snapshot()
 var candidate=JSON.parse_string(FileAccess.get_file_as_string(w+"/EXP-093.json"))
 var original=JSON.stringify(candidate)
 var registry_text=FileAccess.get_file_as_string("res://expressions/registry.json")
 var cat=JSON.parse_string(registry_text);var defs={};var prior_ids=[]
 for entry in cat.entries:
  defs[entry.path]=JSON.parse_string(FileAccess.get_file_as_string(entry.path));prior_ids.append(entry.id)
 check(prior_ids.size()==27 and ID not in prior_ids,"27 originals and candidate absent")
 cat.entries.append({"id":ID,"path":"res://candidate-093.json","aliases":[],"trigger_phase":"neutral"});defs["res://candidate-093.json"]=candidate
 check(rig.registry.load_catalogue(cat,defs),"candidate accepted "+rig.registry.last_error)
 var previous={};var samples=0
 for i in range(4001):
  var t=float(i)/1000;var p=rig.sample_expression(ID,t);samples+=1
  valid_pose(p,"sample "+str(i))
  for k in p:
   if k not in ACTING:check(p[k]==0,"excluded "+k+" "+str(i))
  check(p.blink_L==p.blink_R and p.brow_screen_left==p.brow_screen_right and p.brow_tilt_screen_left==-p.brow_tilt_screen_right,"symmetric "+str(i))
  if t>=.2 and t<=1.85 and not previous.is_empty():
   check(p.blink_L>=previous.blink_L-1e-7,"slow monotonic narrowing "+str(i))
   check(p.brow_screen_left<=previous.brow_screen_left+1e-7,"monotonic brow lowering "+str(i))
   check(p.mouth_open>=previous.mouth_open-1e-7,"monotonic lower lip opening "+str(i))
  if t>=1.85 and t<=2.25:
   for k in p:check(is_equal_approx(p[k],float(candidate.keyframes[4].values.get(k,0))),"exact held peak "+k+" "+str(i))
  if t>=2.65:check(p.mouth_open==0,"sealed aftertaste and release "+str(i))
  if t<=.2 or t>=3.75:check(p==rig.neutral_pose(),"exact neutral hold "+str(i))
  previous=p
 for key in candidate.keyframes:
  var p=rig.sample_expression(ID,key.time)
  for k in p:check(is_equal_approx(p[k],float(key.values.get(k,0))),"key exact "+str(key.time)+" "+k)
 for index in range(candidate.keyframes.size()-1):
  var a=candidate.keyframes[index];var b=candidate.keyframes[index+1]
  for fraction in [.001,.1,.25,.5,.75,.9,.999]:
   var eased=fraction*fraction*(3-2*fraction)
   var p=rig.sample_expression(ID,lerpf(a.time,b.time,fraction))
   for k in p:check(absf(p[k]-lerpf(float(a.values.get(k,0)),float(b.values.get(k,0)),eased))<1e-6,"unchanged cubic smoothstep "+str(index)+" "+str(fraction)+" "+k)
 # Reject invented anatomy, illegal mouth combinations and malformed data without mutating the candidate.
 for key in ["upper_lip_lift","upper_lip_curl","lower_lip_pull","mouth_sneer"]:
  var bad=candidate.duplicate(true);bad.keyframes[4].values[key]=.1
  check(not rig.registry.validate_definition(bad,ID),"reject unsupported "+key)
 for key in ["mouth_width_screen_left","mouth_width_screen_right","mouth_kiss","uneasy_weight"]:
  var bad=candidate.duplicate(true);bad.keyframes[4].values[key]=.1
  check(not rig.registry.validate_definition(bad,ID),"reject conflicting mouth "+key)
 for key in ["opening_px","aversion_px"]:
  var bad=candidate.duplicate(true);bad.keyframes[2].values[key]=.1
  check(not rig.registry.validate_definition(bad,ID),"reject incompatible eye scope "+key)
 for k in rig.Registry.CHANNEL_BOUNDS:
  for value in [float(rig.Registry.CHANNEL_BOUNDS[k][0])-.01,float(rig.Registry.CHANNEL_BOUNDS[k][1])+.01,NAN,INF,"0.5",true]:
   var bad=candidate.duplicate(true);bad.keyframes[4].values[k]=value
   check(not rig.registry.validate_definition(bad,ID),"reject bad value "+k+" "+str(value))
 check(JSON.stringify(candidate)==original,"negative tests preserve candidate")
 check(rig.registry.validate_definition(candidate,ID),"valid candidate remains accepted")
 # Every prior profile hands over in both directions without an ownership jump.
 var handover_samples=0
 for other in prior_ids:
  for direction in [false,true]:
   var from_id=ID if direction else other;var to_id=other if direction else ID
   rig.reset();check(rig.play_expression(from_id),"play source "+from_id)
   rig.advance(1.85 if direction else float(rig.registry.definition(from_id).duration)*.5)
   var before=rig.displayed_pose();check(rig.play_expression(to_id),"handover target "+to_id)
   check(rig.displayed_pose()==before,"handover no initial jump "+from_id+" to "+to_id)
   for j in range(25):
    check(rig.advance(.02),"handover advance");valid_pose(rig.displayed_pose(),"handover "+str(j));handover_samples+=1
   before=rig.displayed_pose();check(rig.release(),"handover release")
   check(rig.displayed_pose()==before,"handover release continuous")
   for j in range(24):rig.advance(.02)
   check(rig.face.snapshot()==neutral,"handover exact release neutral")
 # Auto-blink restoration, interrupted release, manual takeover and rejection preserve ownership.
 for t in [.35,.65,1.15,1.85,2.25,2.65,3.2,3.7]:
  rig.reset();check(rig.apply_controls({"auto_blink":true}),"enable auto blink")
  check(rig.play_expression(ID),"blink candidate play");rig.advance(t)
  check(not rig.auto_blink and rig.auto_blink_pending_restore,"blink suspended with intent")
  var before=rig.displayed_pose();rig.release();check(rig.displayed_pose()==before,"release starts displayed")
  rig.advance(.1);before=rig.displayed_pose();rig.play_expression(ID)
  check(rig.displayed_pose()==before,"retrigger during release continuous")
  check(rig.auto_blink_pending_restore and not rig.auto_blink,"retrigger retains blink intent")
  rig.advance(4);check(rig.auto_blink and not rig.auto_blink_pending_restore,"blink restored once after complete")
  check(rig.face.snapshot()==neutral,"blink restored at open neutral")
  rig.reset();rig.play_expression(ID);rig.advance(t)
  before=rig.displayed_pose();var active=rig.active_performance;var clock=rig.performance_time
  check(not rig.apply_controls({"mouth_open":.3,"mouth_width_screen_left":.2}),"reject illegal manual mouth")
  check(rig.displayed_pose()==before and rig.active_performance==active and rig.performance_time==clock,"invalid manual atomic")
  check(rig.apply_controls({"mouth_open":.15,"mouth_purse":.2}),"valid manual takeover")
  check(rig.active_performance=="" and not rig.auto_blink_pending_restore,"manual cancels performance and blink intent")
  var manual=rig.displayed_pose();rig.advance(.2);check(rig.displayed_pose()==manual,"manual state stable")
  rig.release();rig.advance(.5);check(rig.face.snapshot()==neutral,"manual release exact neutral")
 rig.reset()
 check(FileAccess.get_file_as_string("res://expressions/registry.json")==registry_text,"disk registry byte exact")
 var result={"status":"PASS" if failures.is_empty() else "FAIL","checks":checks,"failures":failures,"sample_count":samples,"sampling_interval_seconds":.001,"prior_profiles_handover_both_directions":27,"handover_samples":handover_samples,"lifecycle_probe_times":[.35,.65,1.15,1.85,2.25,2.65,3.2,3.7],"runtime_sampler":"Unchanged expression_rig.gd","visual_capture":false,"approval":"UNAPPROVED"}
 var f=FileAccess.open(w+"/candidate_checks.json",FileAccess.WRITE);f.store_string(JSON.stringify(result,"  "));f.close()
 print(JSON.stringify(result));quit(0 if failures.is_empty() else 1)

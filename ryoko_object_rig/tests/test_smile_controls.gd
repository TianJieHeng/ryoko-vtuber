extends SceneTree
var rig
var checks=0
var failures=[]
func _initialize():call_deferred("run")
func check(ok:bool,label:String):
 checks+=1
 if not ok:failures.append(label);push_error(label)
func full_state():
 var s=rig.get_state();s.erase("last_error");s.snapshot=rig.face.snapshot();s.shader={}
 for k in rig.face.objects:
  var m=rig.face.objects[k].material
  if m:s.shader[k]=[m.get_shader_parameter("smile"),m.get_shader_parameter("amount"),m.get_shader_parameter("closure")]
 return s
func run():
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 for mode in ["manual","performance","release"]:
  rig.reset();rig.apply_controls({"eye_smile_R":.31,"eye_smile_L":.67,"mouth_smile":.49,"mouth_open":.23})
  if mode=="performance":rig.play_expression("EXP-163");rig.advance(.12)
  if mode=="release":rig.release();rig.advance(.08)
  for k in ["eye_smile_R","eye_smile_L","mouth_smile"]:
   for v in [-.001,1.001,NAN,INF,-INF,true,false,null,[],{},"0.5"]:
    var before=full_state();var bad={"reset":true,k:v}
    check(not rig.apply_controls(bad),"reject "+mode+" "+k+" "+str(v))
    check(full_state()==before,"atomic "+mode+" "+k+" "+str(v))
 rig.reset()
 for k in ["eye_smile_R","eye_smile_L","mouth_smile"]:
  for v in [0,.001,.5,.999,1]:
   check(rig.apply_controls({k:v}),"valid "+k+" "+str(v))
   check(is_equal_approx(rig.pose_now()[k],float(v)),"exposed "+k+" "+str(v))
 rig.apply_controls({"reset":true,"mouth_smile":1.0,"mouth_open":.8,"eye_smile_R":1.0,"eye_smile_L":.6})
 var start=rig.displayed_pose();check(rig.release(),"release");check(rig.displayed_pose()==start,"release C0 control continuity")
 for i in range(28):rig.advance(1.0/60)
 check(rig.pose_now()==rig.neutral_pose(),"release exact neutral")
 rig.apply_controls({"mouth_smile":1.0,"eye_smile_R":.8});start=rig.displayed_pose();check(rig.play_expression("EXP-163"),"handover yawn");check(rig.displayed_pose()==start,"trigger C0 control continuity")
 rig.advance(6);check(rig.pose_now()==rig.neutral_pose(),"end exact neutral")
 var bridge=load("res://control_bridge.gd").new();root.add_child(bridge);bridge.rig=rig
 var cap=bridge.capabilities()
 for k in ["eye_smile_R","eye_smile_L","mouth_smile"]:check(cap.controls[k]==[0.0,1.0],"advertised "+k)
 print("SMILE_CONTROLS checks=",checks," failures=",failures.size());quit(1 if failures.size()>0 else 0)

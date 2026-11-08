extends SceneTree
var rig
var checks=0
var fails=[]
func _initialize():call_deferred("run")
func check(ok:bool,label:String):
 checks+=1
 if not ok:fails.append(label);push_error(label)
func neutral(label:String):
 check(rig.pose_now()==rig.neutral_pose(),label+" neutral controls");check(rig.active_performance=="",label+" no active performance")
func run():
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 check(rig.registry_ready,"registry ready");check(rig.registry.resolve("laugh")=="EXP-005","laugh alias");check(rig.registry.resolve("hearty-laughter")=="EXP-005","title alias")
 var d=rig.registry.definition("EXP-005");check(d.duration==5.4 and d.keyframes.size()==15,"duration and authored beats")
 var peaks=[]
 for i in range(1,d.keyframes.size()-1):
  if d.keyframes[i].values.mouth_open>d.keyframes[i-1].values.mouth_open and d.keyframes[i].values.mouth_open>d.keyframes[i+1].values.mouth_open:peaks.append([d.keyframes[i].time,d.keyframes[i].values.mouth_open])
 check(peaks==[[1.3,.94],[1.91,1.0],[2.53,.88]],"three unequal laugh pulses")
 for i in range(5401):
  var p=rig.sample_expression("EXP-005",i*.001)
  for k in p:
   var bounds=rig.Registry.CHANNEL_BOUNDS[k];check(p[k]>=bounds[0] and p[k]<=bounds[1],"bounded "+k)
  check(p.gaze_x==0 and p.gaze_y==0 and p.hair_sway==0,"no added head/gaze/hair motion")
 for t in [0.0,.000001,.3,.44,.55,.66,1.3,1.91,2.53,3.48,4.28,4.5,5.399999]:
  for action in ["release","laugh","yawn","manual","reset"]:
   rig.reset();rig.play_expression("EXP-005");rig.advance(t);var before=rig.displayed_pose()
   var face_pos=rig.face.position;var head_pos=rig.head.position;var body_pos=rig.body.position
   if action=="release":
    check(rig.release(),"release accepted");check(rig.displayed_pose()==before,"release C0");rig.advance(.5);neutral("release")
   elif action in ["laugh","yawn"]:
    check(rig.play_expression("EXP-005" if action=="laugh" else "EXP-163"),"handover accepted");check(rig.displayed_pose()==before,"handover C0");rig.advance(6.0);neutral("handover")
   elif action=="manual":
    check(rig.apply_controls({"mouth_open":.31}),"manual accepted");check(rig.active_performance=="" and rig.manual_mouth_open==.31,"manual takeover")
   else:rig.reset();neutral("reset")
   check(rig.face.position==face_pos and rig.head.position==head_pos and rig.body.position==body_pos,"fixed face head body")
   for k in rig.face.objects:
    var n=rig.face.objects[k];var pivot=rig.face.homes[k].node
    check(n.scale==Vector2.ONE and pivot.scale==Vector2.ONE and n.modulate.a==1.0,"rigid opaque owner "+k)
 rig.reset();rig.play_expression("EXP-163");rig.advance(1.7);var before=rig.displayed_pose();rig.play_expression("EXP-005");check(rig.displayed_pose()==before,"yawn to laugh C0");rig.advance(10.0);neutral("large delta")
 for i in range(3):
  rig.play_expression("EXP-005")
  for j in range(325):rig.advance(1.0/60.0)
  neutral("repeat")
 print("LAUGHTER_RUNTIME checks=",checks," failures=",fails.size());quit(1 if fails.size() else 0)

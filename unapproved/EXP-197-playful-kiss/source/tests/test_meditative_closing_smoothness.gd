extends SceneTree
var rig
var checks=0
var failures=[]
func _initialize():call_deferred("run")
func check(ok,label):
 checks+=1
 if not ok:
  failures.append(label)
  if failures.size()<8:push_error(label)
func run():
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 check(rig.rig_ready and rig.registry_ready,"ready")
 if not rig.rig_ready or not rig.registry_ready:quit(2);return
 var v0=JSON.parse_string(FileAccess.get_file_as_string("res://source_references/EXP-177_v0.json"))
 var d=rig.registry.definition("EXP-177");check(d.keyframes.size()==7,"one closing interval")
 for i in range(2701):
  var t=1.2+i*.001
  check(rig._sample(d,t)==rig._sample(v0,t),"exact v0 hold/opening sample "+str(t))
 for i in range(1201):
  var t=i*.001;var u=t/1.2;var p=rig.sample_expression("EXP-177",t)
  check(abs(p.blink_L-u*u*(3-2*u))<1e-12,"existing single smoothstep")
  check(p.blink_L==p.blink_R,"bilateral")
  for key in rig.CHANNELS:
   if key not in ["blink_L","blink_R"]:check(p[key]==0,"other channels remain zero")
 for t in [.4,.85]:
  var h=.0001;var a=rig.sample_expression("EXP-177",t-h).blink_L;var b=rig.sample_expression("EXP-177",t+h).blink_L
  check((b-a)/(2*h)>.9,"no interior stop at old key "+str(t))
 var anchors=[[.4866515881418201,.36],[.6400595242051585,.55]]
 for a in anchors:
  rig.reset();rig.play_expression("EXP-177");rig.advance(a[0]);check(abs(rig.face.closure.x-a[1])<.00000005,"exact retimed source pose")
 rig.reset();rig.play_expression("EXP-177")
 var positions=[0.0];var velocities=[];var max_v=0.;var max_a=0.
 for i in range(144):
  rig.advance(1.0/120);positions.append(rig.face.closure.x)
  var v=(positions[-1]-positions[-2])*120;velocities.append(v);max_v=maxf(max_v,v)
  check(v>=0 and v<1.251,"bounded positive played velocity")
  if velocities.size()>1:max_a=maxf(max_a,abs(velocities[-1]-velocities[-2])*120)
 check(max_a<7.4,"bounded played acceleration including existing restart")
 check(rig.face.closure==Vector2.ONE,"unchanged closed arrival")
 print("MEDITATIVE_CLOSING_SMOOTHNESS checks=",checks," failures=",failures.size()," max_played_velocity=",max_v," max_played_acceleration=",max_a)
 quit(0 if failures.is_empty() else 1)

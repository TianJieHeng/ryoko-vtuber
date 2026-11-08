extends SceneTree
var rig
var records=[]
var failures=[]
const NEW=[]
func _initialize():call_deferred("run")
func normalize(value):
 if value is Dictionary:
  var r={}
  for k in value:

   r[k]=normalize(value[k])
  return r
 if value is Array:
  var r=[]
  for v in value:r.append(normalize(v))
  return r
 if value is Resource:return value.resource_path
 return value
func digest(v):return JSON.stringify(normalize(v),"",true,true).sha256_text()
func record(label):
 var s=rig.get_state();s.erase("last_error")
 var material={}
 for k in rig.face.objects:
  var n=rig.face.objects[k]
  if n.material is ShaderMaterial:
   var p={}
   for uniform in n.material.shader.get_shader_uniform_list():

    p[uniform.name]=normalize(n.material.get_shader_parameter(uniform.name))
   material[k]=p
 records.append({"label":label,"state":digest(s),"face":digest(rig.face.snapshot()),"materials":digest(material),"head":str(rig.head.transform),"body":str(rig.body.transform)})
func run():
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 if not rig.rig_ready or not rig.registry_ready:push_error("Not ready");quit(2);return
 record("neutral")
 for entry in rig.list_expressions():
  if entry.id=="EXP-114":continue
  var d=rig.registry.definition(entry.id);var times=[0.0,.000001,.299999,.3,.300001,d.duration-.000001,d.duration]
  for i in range(d.keyframes.size()-1):
   var a=d.keyframes[i].time;var b=d.keyframes[i+1].time
   for f in [0.0,.25,.5,.75,1.0]:times.append(lerpf(a,b,f))
  times.sort()
  var last=-1.0
  for t in times:
   if t==last:continue
   last=t;rig.reset();rig.play_expression(entry.id);rig.advance(t);record(entry.id+"/"+str(t))
  for blink in [false,true]:
   rig.reset();rig.apply_controls({"auto_blink":blink});rig.advance(4.03)
   rig.play_expression(entry.id);record(entry.id+"/incoming/"+str(blink));rig.advance(d.duration*.4)
   rig.release();record(entry.id+"/release/"+str(blink));rig.advance(.17);rig.release();rig.advance(.45);record(entry.id+"/returned/"+str(blink))
 # Legacy manual control cube, using a deterministic distributed set rather than new formulas.
 for i in range(81):
  var p={"reset":true,"mouth_open":float(i%3)/2,"mouth_smile":float((i/3)%3)/2,"mouth_corner_lift":float((i/9)%3)/2,"mouth_purse":float((i/27)%3)/2,"mouth_spread":float((i*7)%11)/10,"mouth_lip_press":float((i*3)%11)/10,"mouth_oral_lift":float((i*5)%11)/10,"mouth_corner_lift_screen_left":float((i*2)%11)/10,"mouth_corner_lift_screen_right":float((i*9)%11)/10}
  if not rig.apply_controls(p):failures.append("manual"+str(i))
  record("manual/"+str(i))
 # Sealed width remains an existing capability and all prior profiles keep their actual bridge metadata.
 for left in [0.0,.5,1.0]:
  for right in [0.0,.5,1.0]:
   rig.reset();rig.apply_controls({"mouth_width_screen_left":left,"mouth_width_screen_right":right,"mouth_purse":.6});record("sealed_width/"+str(left)+"/"+str(right))
 var ids=[]
 for e in rig.list_expressions():
  if e.id!="EXP-114":ids.append(e.id)
 for source in ids:
  for target in ids:
   rig.reset();rig.play_expression(source);rig.advance(rig.registry.definition(source).duration*.5);rig.play_expression(target)
   var last=0.0
   for t in [0.0,.149999,.15,.150001,.299999,.3,.300001]:
    rig.advance(t-last);last=t;record("old_pair/"+source+"/"+target+"/"+str(t))
 var result={"samples":records.size(),"failures":failures,"records":records}
 var path=OS.get_cmdline_user_args()[0];var f=FileAccess.open(path,FileAccess.WRITE);f.store_string(JSON.stringify(result,"  "));f.close()
 print("INDEPENDENT_PARITY_PROBE samples=",records.size()," failures=",failures.size());quit(0 if failures.is_empty() else 1)

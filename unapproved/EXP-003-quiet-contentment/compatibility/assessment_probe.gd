extends SceneTree
var rig
var count=0
var output
var failures=[]
const IDS=["EXP-163","EXP-005","EXP-001","EXP-006","EXP-107","EXP-007","EXP-003"]
func _initialize():call_deferred("run")
func serial(v):
 if v is Resource:
  if v is AtlasTexture:return {"type":"atlas","atlas":v.atlas.resource_path,"region":str(v.region),"margin":str(v.margin),"filter_clip":v.filter_clip}
  return {"resource":v.resource_path,"class":v.get_class()}
 if v is Array:
  var a=[]
  for x in v:a.append(serial(x))
  return a
 if v is Dictionary:
  var d={}
  for k in v:d[str(k)]=serial(v[k])
  return d
 if v is Vector2 or v is Vector2i or v is Color or v is Transform2D or v is Rect2 or v is Rect2i:return str(v)
 return v
func record(label):
 var state=rig.get_state();state.erase("last_error")
 var objects={}
 for k in rig.face.objects:
  var n=rig.face.objects[k];var owner=rig.face.homes[k].node
  var p={"local":str(n.transform),"global":str(n.global_transform),"owner":str(owner.transform),"owner_global":str(owner.global_transform),"texture":serial(n.texture),"offset":str(n.offset),"region":str(n.region_rect),"region_enabled":n.region_enabled,"modulate":str(n.modulate),"self_modulate":str(n.self_modulate),"visible":n.visible,"z_index":n.z_index,"z_relative":n.z_as_relative}
  if n.material is ShaderMaterial:
   p.shader=n.material.shader.resource_path;p.uniforms={}
   for u in n.material.shader.get_shader_uniform_list():p.uniforms[u.name]=serial(n.material.get_shader_parameter(u.name))
  objects[k]=p
 output.store_line(JSON.stringify({"case":label,"state":serial(state),"face":serial(rig.face.snapshot()),"objects":objects,"head":str(rig.head.transform),"body":str(rig.body.transform)},"",true,true));count+=1
func invoke(ok,label):
 if not ok:failures.append(label+": "+rig.last_error)
func run():
 output=FileAccess.open(OS.get_cmdline_user_args()[0],FileAccess.WRITE)
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false)
 if not rig.rig_ready or not rig.registry_ready:push_error(rig.last_error);quit(2);return
 record("neutral")
 # Dense finite headless natural samples include all exact source keys and boundaries.
 var times=[]
 for i in range(115):times.append(minf(float(i)/60.0,1.9))
 for t in [0.0,.000001,.149999,.15,.150001,.299999,.3,.300001,.499999,.5,.500001,.749999,.75,.750001,1.049999,1.05,1.050001,1.349999,1.35,1.350001,1.649999,1.65,1.650001,1.899999,1.9]:times.append(t)
 times.sort();var last=-1.0
 for t in times:
  if t==last:continue
  last=t;rig.reset();invoke(rig.play_expression("EXP-003"),"natural play");invoke(rig.advance(t),"natural advance");record("natural/"+str(t))
 for blink in [false,true]:
  for t in [.0,.3,.5,.6,.75,1.05,1.35,1.899999]:
   for action in ["release","retrigger","manual","reset"]:
    rig.reset();rig.apply_controls({"auto_blink":blink});rig.advance(4.03)
    rig.play_expression("EXP-003");rig.advance(t);record(str(blink)+"/"+str(t)+"/"+action+"/before")
    if action=="release":invoke(rig.release(),action)
    elif action=="retrigger":invoke(rig.play_expression("EXP-003"),action)
    elif action=="manual":invoke(rig.apply_controls({"eye_smile_R":.37,"mouth_corner_lift":.13}),action)
    else:invoke(rig.reset(),action)
    record(str(blink)+"/"+str(t)+"/"+action+"/after")
    rig.advance(.15);record(str(blink)+"/"+str(t)+"/"+action+"/mid")
    rig.advance(3.0);record(str(blink)+"/"+str(t)+"/"+action+"/end")
 for id in IDS:
  for direction in ["incoming","outgoing"]:
   for t in [.3,.9,1.35]:
    rig.reset();rig.play_expression(id if direction=="incoming" else "EXP-003");rig.advance(t)
    invoke(rig.play_expression("EXP-003" if direction=="incoming" else id),"handoff")
    for dt in [0.0,.000001,.15,.149999,.000001,3.0]:
     rig.advance(dt);record(direction+"/"+id+"/"+str(t)+"/"+str(dt))
 output.close()
 print("CONTENTMENT_COMPATIBILITY_PROBE samples=",count," failures=",failures.size());quit(0 if failures.is_empty() else 1)

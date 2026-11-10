extends SceneTree
var rig
var failures=[]
var checks=0
var w=get_script().resource_path.get_base_dir()
var visual=false
func _initialize():
 visual="--capture" in OS.get_cmdline_user_args()
 call_deferred("run")
func check(ok,label):
 checks+=1
 if not ok:failures.append(label)
func capture(label,detail):
 root.size=Vector2i(568,800);root.canvas_transform=Transform2D.IDENTITY
 if detail:
  root.size=Vector2i(400,360)
  var camera=Transform2D.IDENTITY.scaled(Vector2.ONE/.49);camera.origin=-Vector2(6,70)/.49-Vector2(380,380);root.canvas_transform=camera
 await process_frame;await process_frame;await RenderingServer.frame_post_draw
 root.get_texture().get_image().save_png(w+"/capture/"+label+".png")
func run():
 rig=load("res://expression_rig.tscn").instantiate();root.add_child(rig);rig.set_process(false);rig.auto_blink=false
 check(rig.rig_ready and rig.registry_ready,"rig ready")
 if not failures.is_empty():quit(1);return
 rig.hud.hide();rig.hint.hide();rig.pose_status.hide();rig.reset()
 var baseline=rig.face.snapshot();var head=rig.head.transform;var body=rig.body.transform
 var plan=JSON.parse_string(FileAccess.get_file_as_string(w+"/plan.json"))
 if visual:DirAccess.make_dir_recursive_absolute(w+"/capture")
 var cat=JSON.parse_string(FileAccess.get_file_as_string("res://expressions/registry.json"));var defs={}
 for entry in cat.entries:defs[entry.path]=JSON.parse_string(FileAccess.get_file_as_string(entry.path))
 check(rig.list_expressions().size()==24,"production registry unchanged")
 for row in plan:
  var id="PROBE-063-"+row.name;var path="res://probe-"+row.name+".json"
  cat.entries.append({"id":id,"path":path,"aliases":[]})
  defs[path]={"id":id,"title":row.name,"duration":3.0,"keyframes":[{"time":0.0,"phase":"neutral","values":{}},{"time":1.0,"phase":"probe","values":row.pose},{"time":2.0,"phase":"hold","values":row.pose},{"time":3.0,"phase":"neutral_return","values":{}}]}
 check(rig.registry.load_catalogue(cat,defs),"static probe catalogue: "+rig.registry.last_error)
 for row in plan:
  rig.reset()
  check(rig.play_expression("PROBE-063-"+row.name),row.name+" play: "+rig.last_error)
  check(rig.advance(1.5),row.name+" advance")
  check(rig.Registry.scoped_valid(rig.pose_now()),row.name+" scope")
  check(rig.Registry.sealed_mouth_valid(rig.pose_now()),row.name+" mouth domain")
  check(rig.head.transform==head and rig.body.transform==body,row.name+" fixed body")
  if visual:
   await capture(row.name+"_detail",true);await capture(row.name+"_bust",false)
  rig.reset();check(rig.face.snapshot()==baseline,row.name+" reset")
 check(rig.list_expressions().size()==29,"five in-memory probes only")
 var result={"status":"PASS" if failures.is_empty() else "FAIL","checks":checks,"failures":failures,"visual_capture":visual,"scope":"Five isolated state and reset checks, not visual fit or complete performance"}
 var f=FileAccess.open(w+("/capture/checks.json" if visual else "/state_checks.json"),FileAccess.WRITE);f.store_string(JSON.stringify(result,"  "));f.close()
 print(JSON.stringify(result));quit(0 if failures.is_empty() else 1)

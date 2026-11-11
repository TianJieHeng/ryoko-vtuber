"""Prepare separate GUI launch project. Does not launch a renderer or display server."""
import json,shutil
from pathlib import Path
W=Path(__file__).resolve().parent; D=W/'native_launcher';f=json.loads((W/'BASELINE_FREEZE.json').read_text())
assert not D.exists(), "Do not overwrite an existing native launcher."
D.mkdir()
for n in f['source_files_sha256'] | f['extra_manifests_sha256']:
 dst=D/n;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(W/'rig'/n,dst)
for name in ['static','motion']:
 src=W/('check_and_capture.gd' if name=='static' else 'render_motion.gd')
 s=src.read_text().replace('extends SceneTree','extends Node\nvar root\nvar exit_code=0')
 s=s.replace('var w=get_script().resource_path.get_base_dir()', 'var w='+json.dumps(str(W)))
 s=s.replace('func _initialize():\n visual="--capture" in OS.get_cmdline_user_args()\n call_deferred("run")','func _ready():\n root=get_tree().root\n visual=true\n call_deferred("run")')
 s=s.replace('await process_frame','await get_tree().process_frame').replace('quit(', 'finish(')
 s += '\nfunc finish(code):\n exit_code=code\n if is_instance_valid(rig):rig.queue_free()\n queue_free()\n'
 (D/(name+'.gd')).write_text(s)
(D/'launcher.gd').write_text('''extends Node
func _ready():
 var w="'''+str(W)+'''"
 if DirAccess.dir_exists_absolute(w+"/capture") or DirAccess.dir_exists_absolute(w+"/motion"):
  push_error("Existing capture must be preserved; refusing overwrite")
  return
 var static_probe=load("res://static.gd").new()
 add_child(static_probe)
 await static_probe.tree_exited
 var receipt=JSON.parse_string(FileAccess.get_file_as_string(w+"/capture/checks.json"))
 if receipt==null or receipt.get("status")!="PASS":
  push_error("Static capture failed; motion not started")
  return
 await get_tree().process_frame
 var motion_probe=load("res://motion.gd").new()
 add_child(motion_probe)
 await motion_probe.tree_exited
 print("Native capture finished. Inspect receipts before encoding or approval.")
''')
(D/'launcher.tscn').write_text('[gd_scene load_steps=2 format=3]\n[ext_resource type="Script" path="res://launcher.gd" id="1"]\n[node name="HeadacheTension096ReviewLauncher" type="Node"]\nscript = ExtResource("1")\n')
p=(D/'project.godot').read_text();import re
p=re.sub(r'run/main_scene=.*','run/main_scene="res://launcher.tscn"',p)
p=re.sub(r'config/name=.*','config/name="Ryoko EXP096 Headache tension PREVIEW ONLY"',p)
(D/'project.godot').write_text(p)
print(D/'project.godot')

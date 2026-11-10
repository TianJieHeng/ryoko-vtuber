"""Create an isolated Godot desktop parity project. Does not launch native rendering."""
from pathlib import Path
import argparse,hashlib,json,re,shutil
p=argparse.ArgumentParser();p.add_argument('output',type=Path,help='New or empty output directory outside production');a=p.parse_args()
R=Path(__file__).resolve().parents[1];W=a.output.resolve();D=W/'native_launcher';V=R/'validation/approved_batch39/native_parity'
assert not W.is_relative_to(R),'Choose an output directory outside production'
assert not W.exists() or not any(W.iterdir()),'Output must be new or empty; captures must never be overwritten'
D.mkdir(parents=True)
m=json.loads((R/'APPROVED_SOURCE_MANIFEST.json').read_text());copied={}
for n,h in m['files'].items():
 s=R/n;assert hashlib.sha256(s.read_bytes()).hexdigest()==h,n
 q=D/n;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(s,q);copied[n]=h
shutil.copy2(V/'expected_checkpoints.json',W/'expected_checkpoints.json')
s=(V/'launcher.gd').read_text();s=re.sub(r'^var w = .*$', 'var w = '+json.dumps(str(W)),s,flags=re.M)
(D/'launcher.gd').write_text(s);shutil.copy2(V/'launcher.tscn',D/'launcher.tscn')
s=(D/'project.godot').read_text();s=re.sub(r'run/main_scene=.*','run/main_scene="res://launcher.tscn"',s);(D/'project.godot').write_text(s)
copied.pop('project.godot',None)
shutil.copy2(V/'verify_native_result.py',W/'verify_native_result.py')
before={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in R.rglob('*') if p.is_file() and not {'.git','.godot','__pycache__'}&set(p.relative_to(R).parts)}
(W/'native_preflight_baseline.json').write_text(json.dumps({'source':str(R),'source_files':len(before),'files':before},indent=2)+'\n')
(W/'source_copy_receipt.json').write_text(json.dumps({'files':copied,'runtime_sha256':copied['expression_rig.gd'],'production_profile_count':39,'allowed_launcher_changes':['launcher.gd','launcher.tscn','project.godot']},indent=2)+'\n')
print(D/'project.godot')
print('Import through Godot desktop. Disable Game Embed Mode, reload project, run standalone, then restore the previous preference. Do not use headless pixels as native parity.')

print('After capture, run python3 '+str(W/'verify_native_result.py')+' for independent PNG and source-preservation verification.')

#!/usr/bin/env python3
"""Verify the precise new capability delta while retaining all baseline sources."""
from meditative_source_guard import meditative_extra_paths
from pathlib import Path
import json,hashlib,subprocess,sys
from private_pride_source_guard import private_pride_matches
R=Path(__file__).resolve().parents[1];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
b=json.loads((R/'source_references/down_extra_parent_inventory.json').read_text());m=json.loads((R/'validation/down_extra_runtime_migration.json').read_text());checks=0
def check(ok,label):
 global checks
 checks+=1;assert ok,label
check(b['commit']=='8c349e29fb1e742231918260d7db56026492a6c9','exact main parent')
check(len(b['files'])==450,'complete450-file parent')
allowed={'control_limits.gd','object_rig.gd','object_face.gd','expression_rig.gd','expression_registry.gd','expression_viewer.gd','control_bridge.gd','rig_assets/gaze_eyes/manifest.json','rig_assets/gaze_eyes/iris_screen_left.png','rig_assets/gaze_eyes/iris_screen_right.png','rig_assets/gaze_eyes/completed_iris_screen_left.png','rig_assets/gaze_eyes/completed_iris_screen_right.png','tools/build_gaze_eyes.py','tools/verify_lid_handoff.py','tools/verify_smile_support.py','tools/verify_spread_support.py','tools/verify_closed_smile_support.py','tools/verify_gaze_coverage.py','tools/autoblink_source_guard.py','tools/verify_autoblink_scope.py','tools/verify_relief_scope.py','tools/verify_reassurance_scope.py','tools/verify_giggle_scope.py','README.md','CONTROL_API.md','LOCAL_CONTROL_BRIDGE.md'}
check(set(m['files'])==allowed,'exact narrow migration paths')
for p,h in b['files'].items():
 check((R/p).is_file(),'retained parent '+p)
 if p=='SOURCE_FILES.sha256':continue
 e=m['files'].get(p)
 if e:check(e['baseline_sha256']==h,'migration prior hash '+p)
 expected=e['candidate_sha256'] if e else h
 check(sha(R/p)==expected or private_pride_matches(p,expected),'exact source '+p)
for p,h in m['new_files'].items():check(sha(R/p)==h or private_pride_matches(p,h),'exact added source '+p)
existing={str(p.relative_to(R)) for p in R.rglob('*') if p.is_file() and '.godot' not in p.parts and '__pycache__' not in p.parts}
successor=json.loads((R/'validation/private_pride_runtime_migration.json').read_text())
merged=json.loads((R/'validation/approved_merge_migration.json').read_text())
shy=json.loads((R/'validation/approved_shy_merge_migration.json').read_text())
check(existing==set(b['files'])|set(m['new_files'])|set(successor['new_files'])|{'validation/down_extra_runtime_migration.json','validation/private_pride_runtime_migration.json'}|set(merged['new_paths_from_pride'])|set(shy['new_paths_from_152'])|meditative_extra_paths(),'no silently included source')
check(sum(p.endswith('.png') for p in existing)==182,'no extra diagnostic/artwork PNG files')
changed_png={p for p in m['files'] if p.endswith('.png')}
check(changed_png=={f'rig_assets/gaze_eyes/{kind}_{side}.png' for kind in ['iris','completed_iris'] for side in ['screen_left','screen_right']},'only two iris RGB owners and two provenance masks')
for p in ['yawn_performance.json','expressions/registry.json',*[f'expressions/EXP-{i}.json' for i in ['005','001','006','107','007']]]:check(sha(R/p)==b['files'][p] or (p=='expressions/registry.json' and private_pride_matches(p,b['files'][p])),'all six profiles unchanged / pinned registry extension '+p)
for p in b['files']:
 if p.endswith('.gdshader') or p.endswith('.png.import'):check(sha(R/p)==b['files'][p],'shader/import exact '+p)
limits=(R/'control_limits.gd').read_text();check('const GAZE_DOWN_PIXELS=1.0' in limits and 'const GAZE_DOWN_EXTRA_PIXELS=5.0' in limits,'legacy1 plus explicit5 only')
subprocess.run([sys.executable,str(R/'tools/verify_hidden_iris_support.py')],check=True,stdout=subprocess.DEVNULL)
print(json.dumps({'status':'pass','checks':checks,'parent_files':450,'pngs':182,'changed_runtime_iris_pngs':2,'changed_provenance_masks':2,'all_other_pngs_unchanged':178,'registered_profiles':9,'scope':'historical hidden-cap capability with exact pinned approved002/152 merge'},indent=2))

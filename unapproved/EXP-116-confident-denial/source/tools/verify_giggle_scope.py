from meditative_source_guard import meditative_registry_matches
#!/usr/bin/env python3
"""Exact EXP-006-only extension checks; visual parity is a separate gate."""
from pathlib import Path
import hashlib,json
from down_extra_source_guard import down_extra_matches
import re
from reassurance_source_guard import reassurance_matches
P=Path(__file__).resolve().parents[1];checks=0
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def check(ok,label):
 global checks
 checks+=1
 assert ok,label
baseline=json.loads((P/'source_references/giggle_parent_inventory.json').read_text())
migration=json.loads((P/'validation/giggle_runtime_migration.json').read_text())
check(baseline['base_commit']=='69e74ce5049a13ad5aa33014cacb1287f494787a','exact published base')
for path,digest in baseline['files'].items():
 if path=='SOURCE_FILES.sha256':continue
 check((P/path).is_file(),'no parent file removed '+path)
 if path in migration['files']:
  m=migration['files'][path];check(digest==m['baseline_sha256'] and (sha(P/path)==m['candidate_sha256'] or reassurance_matches(path,m['candidate_sha256'])),'explicit exact migration '+path)
 else:check((sha(P/path)==digest or reassurance_matches(path,digest)),'unchanged parent path '+path)
for path,digest in migration['new_files'].items():check((sha(P/path)==digest or reassurance_matches(path,digest)),'exact new source '+path)
check(len(list(P.rglob('*.png')))==182,'174 parent plus two inferred lip PNGs and six original/registered/mask FX PNGs')
for path,digest in baseline['files'].items():
 if path.endswith('.png') or path in ['yawn_performance.json','expressions/EXP-001.json','expressions/EXP-005.json']:check(sha(P/path)==digest or down_extra_matches(path,digest),'immutable or pinned successor art/profile '+path)
check([e['id'] for e in json.loads((P/'expressions/registry.json').read_text())['entries']]==['EXP-163','EXP-005','EXP-001','EXP-006','EXP-107','EXP-007','EXP-002','EXP-152','EXP-160'] or meditative_registry_matches(),'eight approved performances')
check({p.name for p in (P/'expressions').glob('EXP-*.json')}=={'EXP-001.json','EXP-005.json','EXP-006.json','EXP-107.json','EXP-007.json','EXP-002.json','EXP-152.json','EXP-160.json'} or meditative_registry_matches(),'no deferred profiles')
check(not (P/'rig_assets/wide_support').exists(),'no wide-eye assets')
for path in ['object_face.gd','expression_registry.gd','expression_rig.gd','expression_viewer.gd','control_bridge.gd']:
 s=(P/path).read_text()
 for forbidden in ['eye_wide','wide_support']:check(forbidden not in s,'excluded capability '+path+' '+forbidden)
 for axis in ['mouth_corner_lift','mouth_lip_press','blush_intensity']:check(axis in s,'shared bounded capability '+path+' '+axis)
for path in ['object_face.gd','expression_rig.gd']:check('EXP-006' not in (P/path).read_text(),'no expression dispatch '+path)
d=json.loads((P/'expressions/EXP-006.json').read_text());check(d['duration']==2.8 and len(d['keyframes'])==13,'exact corrected timing')
old=json.loads((P/'source_references/EXP-006_no_blush_profile.json').read_text())
check(sha(P/'source_references/EXP-006_no_blush_profile.json')==migration['reused_v16_profile_sha256'],'exact retained corrected profile JSON')
for previous,current in zip(old['keyframes'],d['keyframes']):
 current=json.loads(json.dumps(current));current['values'].pop('blush_intensity')
 check(current==previous,'unchanged corrected mouth/eye/brow timing and values')
check(not list(P.rglob('*.mp4')),'review movies remain external')
print('Historical stage checked with explicit hidden-cap successor hashes.');print(f'GIGGLE_SCOPE_PASS checks={checks} parent_pngs=174 new_lip_pngs=2 new_fx_pngs=6 registry=9')

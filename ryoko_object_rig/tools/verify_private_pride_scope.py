#!/usr/bin/env python3
"""Exact data-only performance on an explicitly unapproved frozen capability."""
from pathlib import Path
import hashlib,json
from approved_merge_source_guard import approved_merge_matches
P=Path(__file__).resolve().parents[1];checks=0
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def check(ok,label):
 global checks
 checks+=1;assert ok,label
b=json.loads((P/'source_references/private_pride_parent_inventory.json').read_text());m=json.loads((P/'validation/private_pride_runtime_migration.json').read_text())
check(b['base_main']=='8c349e29fb1e742231918260d7db56026492a6c9','main base')
check(len(b['files'])==463,'complete unapproved capability parent')
check(hashlib.sha256(''.join(f'{h}  {n}\n' for n,h in sorted(b['files'].items())).encode()).hexdigest()=='7d5004d5a7ef4e3518b994752fb5d9afb7e0a458f5a1d084fa156677a4f06fb1','exact parent inventory')
for n,h in b['files'].items():
 check((P/n).is_file(),'parent retained '+n)
 if n=='SOURCE_FILES.sha256':continue
 v=m['files'].get(n);check((sha(P/n)==(v['candidate_sha256'] if v else h) or approved_merge_matches(n,v['candidate_sha256'] if v else h)),'exact source '+n)
 if v:check(v['baseline_sha256']==h,'migration parent '+n)
for n,h in m['new_files'].items():check(sha(P/n)==h or approved_merge_matches(n,h),'exact new '+n)
for n,h in b['files'].items():
 if n.endswith(('.png','.gdshader','.tscn','.png.import')) or n in ['object_face.gd','object_rig.gd','expression_rig.gd','expression_registry.gd','expression_viewer.gd','control_bridge.gd','control_limits.gd','strict_control_json.gd','project.godot','yawn_performance.json'] or n.startswith('expressions/EXP-'):
  check(sha(P/n)==h or approved_merge_matches(n,h),'immutable runtime/art/prior profile '+n)
ids=['EXP-163','EXP-005','EXP-001','EXP-006','EXP-107','EXP-007','EXP-002','EXP-152']
check([e['id'] for e in json.loads((P/'expressions/registry.json').read_text())['entries']]==ids,'only eight approved performances')
check({p.name for p in (P/'expressions').glob('EXP-*.json')}=={x+'.json' for x in ids if x!='EXP-163'},'no held002/003')
check(len(list(P.rglob('*.png')))==182,'no performance artwork')
d=json.loads((P/'expressions/EXP-152.json').read_text());ref=json.loads((P/'source_references/EXP-152_reference_metadata.json').read_text())
check(d['duration']==1.9 and len(d['keyframes'])==9,'nine source anchors')
check([k['time'] for k in d['keyframes']]==[k['time_seconds'] for k in ref['key_pose_sequence']],'proposed source timing interpreted')
check(d['source_catalogue_sha256']==ref['asset_production']['sha256']=='46d16e1eabfe7ea709252b0e3c47707613df3a8f6a41483e740981866ead6408','exact v002 source')
for k in d['keyframes']:
 v=k['values'];check(v['blink_R']==v['blink_L'] and v['gaze_y']==v['gaze_down_extra'],'symmetric ordinary lids and coupled gaze')
 for axis in ['eye_smile_R','eye_smile_L','mouth_open','mouth_spread','mouth_purse','mouth_oral_lift','gaze_x','hair_sway','blush_intensity']:check(v[axis]==0,'quiet closed acting '+axis)
for i in [1,6,7]:
 v=d['keyframes'][i]['values'];check(v['gaze_down_extra']>0 and all(v[k]==0 for k in ['mouth_smile','mouth_corner_lift','mouth_lip_press']),'gaze precedes and outlasts smile')
release=json.loads((P/'RELEASE.json').read_text());check(release['authored_registry']==ids and release['approved_predecessors']==ids[:-1],'approval distinct from authorship')
check(release['user_approved'] is True and release['approved_registry']==ids,'explicit user approval')
for n in ['README.md','CONTROL_API.md','LOCAL_CONTROL_BRIDGE.md','PACKAGING.md','PRIVATE_PRIDE_SCOPE_VALIDATION.md']:
 t=(P/n).read_text();check('EXP-152' in t and 'approved' in t.lower(),'honest current status '+n)
check(not list(P.rglob('*.mp4')),'media external')
print(f'PRIVATE_PRIDE_SCOPE_PASS checks={checks} parent_files=463 protected_pngs=182 new_pngs=0 registry=8')

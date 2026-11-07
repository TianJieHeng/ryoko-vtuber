#!/usr/bin/env python3
"""Exact profile-only EXP-002 extension and immutable published-parent guard."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parents[1];checks=0
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def check(ok,label):
 global checks
 checks+=1
 assert ok,label
b=json.loads((P/'source_references/affection_parent_inventory.json').read_text());m=json.loads((P/'validation/affection_runtime_migration.json').read_text())
check(b['base_commit']=='8c349e29fb1e742231918260d7db56026492a6c9','published parent')
check(b['inventory_sha256']=='70e8593da87a240bfa024c58677f53560f4ff7afc6d6fa07f7f54665d1072cf6','parent inventory')
check(len(b['files'])==450,'complete parent')
for p,h in b['files'].items():
 check((P/p).is_file(),'parent retained '+p)
 if p=='SOURCE_FILES.sha256':continue
 v=m['files'].get(p);check(sha(P/p)==(v['candidate_sha256'] if v else h),'exact source '+p)
 if v:check(v['baseline_sha256']==h,'migration parent '+p)
for p,h in m['new_files'].items():check(sha(P/p)==h,'exact new '+p)
for p,h in b['files'].items():
 if p.endswith(('.png','.gdshader')) or p in ['object_face.gd','object_rig.gd','expression_rig.gd','expression_registry.gd','expression_viewer.gd','control_bridge.gd','control_limits.gd','strict_control_json.gd','yawn_performance.json','expressions/EXP-005.json','expressions/EXP-001.json','expressions/EXP-006.json','expressions/EXP-107.json','expressions/EXP-007.json']:
  check(sha(P/p)==h,'immutable runtime art prior profile '+p)
check(len(list(P.rglob('*.png')))==182,'no artwork added')
ids=['EXP-163','EXP-005','EXP-001','EXP-006','EXP-107','EXP-007','EXP-002']
check([x['id'] for x in json.loads((P/'expressions/registry.json').read_text())['entries']]==ids,'exact registry')
check({p.name for p in (P/'expressions').glob('EXP-*.json')}=={x+'.json' for x in ids if x!='EXP-163'},'only authored profiles')
d=json.loads((P/'expressions/EXP-002.json').read_text());ref=json.loads((P/'source_references/EXP-002_reference_metadata.json').read_text())
check(d['duration']==1.9 and len(d['keyframes'])==9,'nine keys 1.9 seconds')
check([k['time'] for k in d['keyframes']]==[k['time_seconds'] for k in ref['key_pose_sequence']],'original proposed timing')
check(d['source_catalogue_sha256']==ref['asset_production']['sha256']=='76ab1be9b8e3dc12447dd9045e9356452da12182be70700b5f06eac2faff9efd','exact v001 source')
check(d['keyframes'][3]['values']['eye_smile_R']<.1 and d['keyframes'][5]['values']['eye_smile_R']<.1,'open eye contact before and after peak')
check(d['keyframes'][4]['values']['eye_smile_R']>=.85,'upward smiling closure')
check(d['keyframes'][5]['values']['mouth_smile']==d['keyframes'][4]['values']['mouth_smile'] and d['keyframes'][7]['values']['mouth_smile']>0,'smile lingers beyond closure')
for k in d['keyframes']:
 v=k['values'];check(v['eye_smile_R']==v['eye_smile_L'],'symmetric pleased eyes')
 for key in ['mouth_open','mouth_spread','mouth_purse','mouth_lip_press','mouth_oral_lift','blink_R','blink_L','gaze_x','gaze_y','hair_sway','blush_intensity']:check(v.get(key,0)==0,'quiet sealed scope '+key)
check(not list(P.rglob('*.mp4')),'media external')
# Current summary consistency is checked separately from immutable historical receipts.
release=json.loads((P/'RELEASE.json').read_text())
check(release['authored_registry']==ids and release['approved_predecessors']==ids[:-1],'release authored/approved split')
for name,fragments in {
 'README.md':['EXP-002 (Affectionate warmth)','seven actual authored','All seven are user-approved','current 20-suite','AFFECTION_SCOPE_VALIDATION.md'],
 'CONTROL_API.md':['EXP-002 / Affectionate warmth','All seven authored IDs','All seven are user-approved'],
 'LOCAL_CONTROL_BRIDGE.md':['Seven performances are authored','EXP-107, EXP-007 and EXP-002','All seven are user-approved'],
 'PACKAGING.md':['seven authored performances','EXP-002 affectionate warmth','All seven are user-approved','current complete 20-suite','user-approved for publication'],
}.items():
 text=(P/name).read_text()
 for fragment in fragments:check(fragment in text,'current documentation '+name+' '+fragment)
for name in ['README.md','PACKAGING.md']:
 text=(P/name).read_text()
 check('current 18-suite' not in text and 'current complete 18-suite' not in text,'no stale current suite count '+name)
check(release['user_approved'] is True and release['approved_registry']==ids,'explicit publication approval')
check('## Complete current runtime checklist' in (P/'AFFECTION_SCOPE_VALIDATION.md').read_text(),'complete current checklist')
print(f'AFFECTION_SCOPE_PASS checks={checks} parent_files=450 protected_pngs=182 new_pngs=0 registry=7')

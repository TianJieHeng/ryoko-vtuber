#!/usr/bin/env python3
"""Exact EXP-107-only extension; not a substitute for actual render review."""
from pathlib import Path
import hashlib,json
from down_extra_source_guard import down_extra_matches
from relief_source_guard import relief_matches
P=Path(__file__).resolve().parents[1];checks=0
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def check(ok,label):
 global checks
 checks+=1
 assert ok,label
base=json.loads((P/'source_references/reassurance_parent_inventory.json').read_text())
m=json.loads((P/'validation/reassurance_runtime_migration.json').read_text())
check(base['base_commit']=='4f3deaa2de3eedb691a9f0c795c7b8563663e472','verified parent commit')
check(len(base['files'])==399 and all('__pycache__' not in p and not p.endswith('.pyc') for p in base['files']),'399 packaged parent paths, no caches')
for p,h in base['files'].items():
 check((P/p).is_file(),'retained parent '+p)
 if p=='SOURCE_FILES.sha256':continue
 if p in m['files']:
  v=m['files'][p];check(v['baseline_sha256']==h and (sha(P/p)==v['candidate_sha256'] or relief_matches(p,v['candidate_sha256'])),'exact migration '+p)
 else:check((sha(P/p)==h or relief_matches(p,h)),'unchanged parent '+p)
for p,h in m['new_files'].items():check((sha(P/p)==h or relief_matches(p,h)),'exact added source '+p)
for p,h in base['files'].items():
 if p.endswith('.png') or p in ['yawn_performance.json','expressions/EXP-005.json','expressions/EXP-001.json','expressions/EXP-006.json']:check(sha(P/p)==h or down_extra_matches(p,h),'immutable or pinned successor art/profile '+p)
check(len(list(P.rglob('*.png')))==182,'no new artwork')
check([e['id'] for e in json.loads((P/'expressions/registry.json').read_text())['entries']]==['EXP-163','EXP-005','EXP-001','EXP-006','EXP-107','EXP-007','EXP-002','EXP-152'],'eight approved performances')
check({p.name for p in (P/'expressions').glob('EXP-*.json')}=={'EXP-001.json','EXP-005.json','EXP-006.json','EXP-107.json','EXP-007.json','EXP-002.json','EXP-152.json'},'only scoped profiles')
for p in ['object_face.gd','expression_rig.gd','expression_registry.gd','expression_viewer.gd','control_bridge.gd']:
 s=(P/p).read_text();check('mouth_oral_lift' in s,'shared bounded control '+p)
 for bad in ['eye_wide','wide_support']:check(bad not in s,'excluded '+bad)
for p in ['object_face.gd','expression_rig.gd']:check('EXP-107' not in (P/p).read_text(),'no profile-specific runtime dispatch')
check(not (P/'rig_assets/wide_support').exists(),'no wide artwork')
check(not list(P.rglob('*.mp4')),'movies external')
d=json.loads((P/'expressions/EXP-107.json').read_text());check(d['duration']==3 and len(d['keyframes'])==11,'authored timing')
check(d['source_catalogue_sha256']=='08e4f43e20144930411dd49087eaa76d70bde1fb0214b70b6d56bd5ed42797d0','exact source sheet')
print('Historical stage checked with explicit hidden-cap successor hashes.');print(f'REASSURANCE_SCOPE_PASS checks={checks} protected_pngs=182 new_pngs=0 registry=8')

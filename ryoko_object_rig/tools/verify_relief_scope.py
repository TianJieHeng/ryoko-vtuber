#!/usr/bin/env python3
"""Exact EXP-007 and generic rigid-purse scope, source and immutable-parent guard."""
from pathlib import Path
import hashlib,json
from autoblink_source_guard import autoblink_matches
P=Path(__file__).resolve().parents[1];checks=0
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def check(ok,label):
 global checks
 checks+=1
 assert ok,label
b=json.loads((P/'source_references/relief_parent_inventory.json').read_text());m=json.loads((P/'validation/relief_runtime_migration.json').read_text())
check(b['base_commit']=='35a7ddc615e7501a9a814ca02d722ddb40f200c9','approved base')
check(len(b['files'])==418,'all parent paths')
for p,h in b['files'].items():
 check((P/p).is_file(),'retained '+p)
 if p=='SOURCE_FILES.sha256':continue
 v=m['files'].get(p)
 expected=v['candidate_sha256'] if v else h
 check(sha(P/p)==expected or autoblink_matches(p,expected),'exact scoped '+p)
 if v:check(v['baseline_sha256']==h,'migration parent '+p)
for p,h in m['new_files'].items():check(sha(P/p)==h or autoblink_matches(p,h),'exact new '+p)
for p,h in b['files'].items():
 if p.endswith('.png') or p in ['canonical_eye_alpha.gdshader','object_eye_clip.gdshader','object_rig.gd','control_limits.gd','strict_control_json.gd','yawn_performance.json','expressions/EXP-005.json','expressions/EXP-001.json','expressions/EXP-006.json','expressions/EXP-107.json']:
  check(sha(P/p)==h,'unchanged runtime/art/prior profile '+p)
check(len(list(P.rglob('*.png')))==182,'no new artwork')
check([e['id'] for e in json.loads((P/'expressions/registry.json').read_text())['entries']]==['EXP-163','EXP-005','EXP-001','EXP-006','EXP-107','EXP-007'],'only six authored profiles')
check({p.name for p in (P/'expressions').glob('EXP-*.json')}=={'EXP-001.json','EXP-005.json','EXP-006.json','EXP-107.json','EXP-007.json'},'narrow scope')
d=json.loads((P/'expressions/EXP-007.json').read_text());check(d['duration']==3.2 and len(d['keyframes'])==9,'authored timing')
check(d['source_catalogue_sha256']=='906ddfe017b15ad415d3ffc44ec930cab6ebf8c377da970259a1125bfb9bf2ad','exact sheet')
check(not list(P.rglob('*.mp4')),'movies external')
print(f'RELIEF_SCOPE_PASS checks={checks} protected_pngs=182 new_pngs=0 registry=6')

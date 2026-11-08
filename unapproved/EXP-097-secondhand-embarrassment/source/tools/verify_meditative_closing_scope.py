#!/usr/bin/env python3
"""Narrow closing-data correction over the exact preserved v0 review freeze."""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parents[1];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();digest=lambda x:hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
v=json.loads((P/'source_references/meditative_v0_inventory.json').read_text());assert v['inventory_sha256']=='27194683cd21c95c2bdbd6bc469c0d637872c8c40163af2014e44229e27bef6c'==digest(v['files']);assert len(v['files'])==538
allowed={'README.md','PACKAGING.md','CONTROL_API.md','LOCAL_CONTROL_BRIDGE.md','RELEASE.json','tools/verify_affection_scope.py','tools/verify_private_pride_scope.py','tools/verify_approved_shy_merge.py','expressions/EXP-177.json','MEDITATIVE_STATUS.json','MEDITATIVE_SCOPE_VALIDATION.md','tests/test_meditative_runtime.gd','tools/review_meditative_gate.gd','tools/review_meditative_scope.gd','tools/meditative_source_guard.py','tools/verify_meditative_scope.py','validation/meditative_runtime_migration.json','SOURCE_FILES.sha256'}
new={'MEDITATIVE_PUBLICATION_VALIDATION.md','source_references/meditative_v1_review_inventory.json','MEDITATIVE_CLOSING_REVISION.md','source_references/meditative_v0_inventory.json','source_references/EXP-177_v0.json','tools/verify_meditative_closing_scope.py','tests/test_meditative_closing_smoothness.gd'}
actual={p.relative_to(P).as_posix() for p in P.rglob('*') if p.is_file() and not set(p.parts)&{'.godot','__pycache__'}};assert actual==set(v['files'])|new
changed={n for n,h in v['files'].items() if sha(P/n)!=h};assert changed==allowed,(changed-allowed,allowed-changed)
assert sha(P/'source_references/EXP-177_v0.json')==v['files']['expressions/EXP-177.json']=='581c3d34be7b99dc8dbf5df3d68b46e9014eed9fd60dae52d70ce38ea48afa6f'
o=json.loads((P/'source_references/EXP-177_v0.json').read_text());d=json.loads((P/'expressions/EXP-177.json').read_text());assert d['duration']==o['duration']==3.9
assert d['keyframes'][1:]==o['keyframes'][3:],'all hold/opening key objects exact'
assert d['keyframes'][0]['time']==0 and d['keyframes'][0]['values']==o['keyframes'][0]['values'] and d['keyframes'][0]['phase']=='settling'
assert set(d)==set(o) and {k for k in d if d[k]!=o[k]}=={'status','timing_origin','interpolation','keyframes'}
assert len(d['keyframes'])==7 and [x['time'] for x in d['keyframes']]==[0,1.2,1.75,2.35,2.85,3.35,3.9]
review=json.loads((P/'source_references/meditative_v1_review_inventory.json').read_text())
assert len(review['files'])==543 and review['inventory_sha256']=='b5a10081697aa3cfaa28484db1b035a94b9c954c54f44623b0d2da2acfca1ec8'==digest(review['files'])
overlay={'expressions/EXP-177.json','README.md','PACKAGING.md','CONTROL_API.md','LOCAL_CONTROL_BRIDGE.md','RELEASE.json','MEDITATIVE_STATUS.json','MEDITATIVE_SCOPE_VALIDATION.md','MEDITATIVE_CLOSING_REVISION.md','tools/meditative_source_guard.py','tools/verify_meditative_scope.py','tools/verify_meditative_closing_scope.py','tools/verify_affection_scope.py','tools/verify_private_pride_scope.py','tools/verify_approved_shy_merge.py','validation/meditative_runtime_migration.json','SOURCE_FILES.sha256'}
assert {n for n,h in review['files'].items() if sha(P/n)!=h}==overlay, 'exact publication-only overlay'
assert hashlib.sha256(review['profile_text'].encode()).hexdigest()==review['files']['expressions/EXP-177.json']=='5787127ef22f05714b3219e20a3a329945ec09dec70f8a814da131778d512881'
review_profile=json.loads(review['profile_text'])
assert set(d)==set(review_profile) and {k for k in d if d[k]!=review_profile[k]}=={'status'}, 'only publication status differs from reviewed profile'
assert d['status']=='User-approved revised meditative calm; published with the containing repository commit'
assert actual==set(review['files'])|{'MEDITATIVE_PUBLICATION_VALIDATION.md','source_references/meditative_v1_review_inventory.json'}
import verify_meditative_scope  # Full path/hash/manifest and publication status validation.
print('MEDITATIVE_CLOSING_SCOPE_PASS files=545 publication_overlay=17 additions=2 runtime_art_prior_profiles_unchanged=true opening_hold_keys_exact=true')

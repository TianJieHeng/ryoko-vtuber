#!/usr/bin/env python3
"""Verify the exact approved integration tree, independently of working directory."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parents[1]
read=lambda n:json.loads((P/n).read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
digest=lambda x:hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
SKIP={'.godot','.git','__pycache__'}
files={p.relative_to(P).as_posix():sha(p) for p in sorted(P.rglob('*')) if p.is_file() and not any(x in SKIP for x in p.relative_to(P).parts)}
assert not any(p.is_symlink() for p in P.rglob('*')),'symlink outside exact source contract'
m=read('APPROVED_SOURCE_MANIFEST.json');proof=read('source_references/approved_integration_sources.json')
assert m['files']=={k:v for k,v in files.items() if k not in {'APPROVED_SOURCE_MANIFEST.json','APPROVED_SOURCE_FILES.sha256'}},'complete source inventory mismatch'
assert digest(m['files'])==m['inventory_sha256'],'manifest digest mismatch'
lines=(P/'APPROVED_SOURCE_FILES.sha256').read_text().splitlines();checks={x[66:]:x[:64] for x in lines}
assert checks=={k:v for k,v in files.items() if k!='APPROVED_SOURCE_FILES.sha256'},'checksum index mismatch'
source=proof['accepted_source_files'];base=proof['approved_parent_files']
assert len(source)==628 and digest(source)=='3c3e1a30b0ee90062de767bbda84de81d653e56742a5b7aa9ec7b599e13a6dc3','accepted source identity mismatch'
assert len(base)==585 and digest(base)=='e55db994b937f53680cf0bba8aa3b54461334c9d62272b2fbf1f45024c39aaba','approved predecessor identity mismatch'
assert set(base)<=set(source)<=set(files),'approved historical files missing'
ids=['EXP-163','EXP-005','EXP-001','EXP-006','EXP-107','EXP-007','EXP-002','EXP-152','EXP-160','EXP-177','EXP-164','EXP-021','EXP-158','EXP-181','EXP-102','EXP-116','EXP-050','EXP-186']
registry=read('expressions/registry.json');assert [e['id'] for e in registry['entries']]==ids,'wrong registry'
assert files['expressions/registry.json']==source['expressions/registry.json'],'registry differs from accepted source'
assert len(list((P/'expressions').glob('EXP-*.json')))==17,'extra expression file'
for e in registry['entries']:
 n=e['path'][6:];assert files[n]==source[n],n+' differs from accepted profile'
 if e['id'] in ids[:12]:assert files[n]==base[n],n+' differs from old approved profile'
status=read('APPROVED_INTEGRATION_STATUS.json');release=read('RELEASE.json')
assert status['approved_profile_ids']==ids and status['newly_approved_profile_ids']==ids[12:] and status['approved_profile_count']==18
assert release['approved_registry']==ids and release['approved_published_count']==18 and release['pending_review']==[]
assert 'EXP-003' in status['excluded_profile_ids'] and 'EXP-097' in status['excluded_profile_ids']
assert status['EXP-003_status']=='unapproved historical; not user-rejected; NOT_REPLAYED'
# All captured runtime, artwork, scenes, imports and profiles stay exact. Only explicit current docs and reviewed tests may differ.
allowed=set(m['accepted_source_overlay_paths'])
actual={n for n in source if files[n]!=source[n]};assert actual==allowed,'unexpected accepted-source overlay'
assert allowed=={'README.md','CONTROL_API.md','LOCAL_CONTROL_BRIDGE.md','PACKAGING.md','RELEASE.json'}|set(m['adapted_historical_tests']),'invalid overlay class'
for n in source:
 if n in allowed:continue
 assert files[n]==source[n],n+' captured source changed'
pngs=[n for n in files if n.endswith('.png')];assert len(pngs)==182
for n in pngs:assert files[n]==source[n]==base[n],n+' artwork changed'
assert files['source_references/quiet_sadness_release_checkpoint.json']==source['RELEASE.json']
assert 'test_expression_backbone.gd' in m['adapted_historical_tests']
assert 'tests/test_approved_integration.gd' in files
print('APPROVED_INTEGRATION_GUARD PASS files=%d profiles=18 old_profiles_exact=12 pngs_exact=182 accepted_runtime_exact=true historical_receipts_exact=true'%len(files))

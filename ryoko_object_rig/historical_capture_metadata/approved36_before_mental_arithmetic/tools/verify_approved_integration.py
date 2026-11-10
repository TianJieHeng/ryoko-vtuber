"""Current approved36 inventory, predecessor and exact-review guard."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1]
def read(n):return json.loads((R/n).read_text())
def sha(n):return hashlib.sha256((R/n).read_bytes()).hexdigest()
m=read('APPROVED_SOURCE_MANIFEST.json');assert m['approved_profiles']==36
excluded={'APPROVED_SOURCE_MANIFEST.json','APPROVED_SOURCE_FILES.sha256'}
actual={str(p.relative_to(R)) for p in R.rglob('*') if p.is_file() and not {'.godot','__pycache__','test_home','test_xdg'}&set(p.parts) and not p.name.endswith('.pyc')}
actual={p for p in actual if not p.endswith(('.uid','.import')) or p in m['files']}
assert actual-excluded==set(m['files']),f'Inventory mismatch: added={actual-excluded-set(m["files"])} missing={set(m["files"])-actual}'
for n,h in m['files'].items():assert sha(n)==h,'Changed source: '+n
assert (R/'APPROVED_SOURCE_FILES.sha256').read_text()==''.join(f'{h}  {n}\n' for n,h in sorted(m['files'].items()))
ids=[e['id'] for e in read('expressions/registry.json')['entries']]
old=read('historical_capture_metadata/approved27_before_batch36/expressions/registry.json')['entries']
assert len(ids)==len(set(ids))==36 and ids[:27]==[e['id'] for e in old]
assert read('expressions/registry.json')['entries'][:27]==old
assert ids[27:]==['EXP-139','EXP-174','EXP-067','EXP-093','EXP-003','EXP-043','EXP-064','EXP-004','EXP-042']
for e in read('expressions/registry.json')['entries']:
 d=read(e['path'][6:]);assert d['id']==e['id']
 assert d['keyframes'][0]['time']==0 and d['keyframes'][-1]['time']==d['duration']
 assert all(v==0 for k in [d['keyframes'][0],d['keyframes'][-1]] for v in k['values'].values())
p=read('validation/approved_batch36/predecessor_preservation.json')
assert p['profile_count']==27 and p['png_count']==184 and p['runtime_changed'] is True
for n,h in p['protected_files'].items():assert sha(n)==h,'Predecessor changed: '+n
for n in p['modified_archived_files']:
 if n.startswith('tests/'):
  assert sha('historical_capture_metadata/approved27_before_batch36/'+n)==read('historical_capture_metadata/approved27_before_batch36/APPROVED_SOURCE_MANIFEST.json')['files'][n]
assert sha('expression_rig.gd')!=sha('historical_capture_metadata/approved27_before_batch36/expression_rig.gd')
for item in read('validation/approved_batch36/approved_review_identity.json')['profiles']:
 assert sha('expressions/'+item['id']+'.json')==item['profile_sha256']
 assert sha('validation/approved_batch36/'+item['id']+'/'+item['video_name'])==item['video_sha256']
result=read('APPROVED_INTEGRATION_TEST_RESULTS.json');assert result['status']=='PASS' and result['runtime_changed'] and not result['ci_run']
assert result['runtime_sha256']==sha('expression_rig.gd')
for filename in ['handoff_boundary_checks.json','bridge_lifecycle_checks.json','focused_object_checks.json']:
 assert read('validation/approved_batch36/'+filename)['runtime_sha256_at_start']==result['runtime_sha256']
assert read('validation/approved_batch36/native_parity/numeric_source_parity.json')['validated_runtime_expression_rig_sha256']==result['runtime_sha256']
for n,e in result['receipts'].items():
 path='validation/approved_batch36/'+n;c=read(path)
 assert c['status']=='PASS' and c['failures']==[] and c['checks']==e['checks'] and sha(path)==e['sha256']
s=read('APPROVED_INTEGRATION_STATUS.json');assert s['approved_profile_ids']==ids and s['current_runtime_changes'] and not s['normal_speed_playback_observed'] and not s['live_engine_pacing_measured']
r=read('RELEASE.json');assert r['approved_registry']==ids and r['approved_published_count']==36 and r['newly_approved']==ids[27:]
assert 'BLOCKED' in r['native_visual_parity']
print('APPROVED36_GUARD PASS prior_profiles=27 PNGs=184 new_profiles=9 runtime_changed=bounded_opening_handoff fresh_native_parity=BLOCKED live_pacing=UNVERIFIED')

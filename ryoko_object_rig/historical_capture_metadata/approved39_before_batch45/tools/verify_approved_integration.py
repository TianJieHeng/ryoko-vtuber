"""Current approved39 source, preservation, approval identity and validation guard."""
from pathlib import Path
import hashlib,json,sys
R=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[1]
def read(n):return json.loads((R/n).read_text())
def sha(n):return hashlib.sha256((R/n).read_bytes()).hexdigest()
m=read('APPROVED_SOURCE_MANIFEST.json');assert m['approved_profiles']==39
excluded={'APPROVED_SOURCE_MANIFEST.json','APPROVED_SOURCE_FILES.sha256'}
actual={str(p.relative_to(R)) for p in R.rglob('*') if p.is_file() and not {'.godot','__pycache__','test_home','test_xdg'}&set(p.relative_to(R).parts) and not p.name.endswith('.pyc')}
actual={p for p in actual if not p.endswith(('.uid','.import')) or p in m['files']}
assert actual-excluded==set(m['files']),f'Inventory mismatch: added={actual-excluded-set(m["files"])} missing={set(m["files"])-actual}'
for n,h in m['files'].items():assert sha(n)==h,'Changed source: '+n
assert (R/'APPROVED_SOURCE_FILES.sha256').read_text()==''.join(f'{h}  {n}\n' for n,h in sorted(m['files'].items()))
H='historical_capture_metadata/approved36_before_mental_arithmetic/'
entries=read('expressions/registry.json')['entries'];old=read(H+'expressions/registry.json')['entries'];ids=[e['id'] for e in entries]
assert len(ids)==len(set(ids))==39 and entries[:36]==old
assert ids[36:]==['EXP-129','EXP-041','EXP-061']
assert entries[36]['aliases']==['mental_arithmetic'] and entries[37]['aliases']==['controlled_anger'] and entries[38]['aliases']==['broad_surprise']
for e in entries:
 d=read(e['path'][6:]);assert d['id']==e['id']
 assert d['keyframes'][0]['time']==0 and d['keyframes'][-1]['time']==d['duration']
 assert all(v==0 for k in [d['keyframes'][0],d['keyframes'][-1]] for v in k['values'].values())
V='validation/approved_batch39/'
p=read(V+'predecessor_preservation.json');assert p['prior_profile_count']==36 and p['png_count']==184 and p['runtime_changed'] is False
base=read(H+'APPROVED_SOURCE_MANIFEST.json')
assert len(base['files'])==999 and len(p['protected_files'])==993
assert sum(n.endswith('.png') for n in p['protected_files'])==184
profile_paths={entry['path'][6:] for entry in old};assert len(profile_paths)==36
assert all(name in p['protected_files'] for name in profile_paths)
for n,h in p['protected_files'].items():assert sha(n)==h,'Predecessor changed: '+n
for n in p['modified_archived_files']:assert sha(H+n)==base['files'][n]
assert sha('expression_rig.gd')==base['files']['expression_rig.gd']
for item in read(V+'approved_review_identity.json')['profiles']:
 assert sha('expressions/'+item['id']+'.json')==item['profile_sha256']
 assert sha(item['video_path'])==item['video_sha256']
runtime=sha('expression_rig.gd')
result=read('APPROVED_INTEGRATION_TEST_RESULTS.json');assert result['status']=='PASS' and not result['runtime_changed'] and not result['artwork_changed'] and not result['ci_run']
assert result['runtime_sha256']==runtime
for n,e in result['receipts'].items():
 c=read(V+n);assert c['status']=='PASS' and c.get('failures',[])==[] and c['checks']==e['checks'] and sha(V+n)==e['sha256']
a=read(V+'actual_object_checks.json');assert a['production_profile_count']==39 and a['actual_object_directed_cross_cases']==225 and a['actual_object_cross_samples']==2475 and a['trajectory_samples']==363 and a['runtime_sha256']==runtime
d=read(V+'dense_checks.json');assert d['prior36_standalone_samples_at_60hz']==8560 and d['directed_cross_key_midpoint_cases']==4611 and d['interrupted_lifecycle_cases']==9222 and d['approved_preview_pose_samples']==363 and d['runtime_sha256']==runtime
n=read(V+'native_parity/RESULT.json');assert n['pixel_matches']==n['image_comparisons_run']==726 and n['captured_checkpoints']==363 and n['profiles']==3
approved_sources={'EXP-129':'validation/approved_mental_arithmetic/approved_preview/motion_checks.json','EXP-041':'validation/approved_pair38/EXP-041/motion_checks.json','EXP-061':V+'EXP-061/motion_checks.json'}
expected_pngs={}
for id in ['EXP-129','EXP-041','EXP-061']:
 approved=read(approved_sources[id])['records'];assert [int(r['frame']) for r in approved]==list(range(121))
 records=[r for r in n['records'] if r['id']==id];assert [int(r['frame']) for r in records]==list(range(121))
 for r,a in zip(records,approved):
  assert r['hashes']==r['expected_hashes']==a['hashes'] and len(r['hashes'])==2
  for j,(view,size) in enumerate([('full',[568,800]),('detail',[400,360])]):
   expected_pngs[f'captures/{id}/{int(r["frame"]):04d}_{view}.png']=(size,a['hashes'][j])
ind=read(V+'native_parity/independent_png_verification.json')
assert ind['status']=='PASS' and ind['checks']==ind['actual_png_count']==len(ind['records'])==726 and all(ind['summary_checks'].values())
assert {r['path'] for r in ind['records']}==set(expected_pngs)
for r in ind['records']:
 size,h=expected_pngs[r['path']];assert r['pass'] and r['size']==size and r['sha256_rgba']==r['expected']==h
preservation=read(V+'native_parity/source_preservation.json')
assert preservation['status']=='PASS' and preservation['production_differences']==[] and preservation['copied_source_differences']==[] and preservation['source_runtime_sha256']==runtime
remote=read(V+'remote_baseline_verification.json');assert remote['status']=='PASS' and remote['local_files']==remote['remote_files']==1001 and remote['differences']==[]
copied=read(V+'native_parity/source_copy_receipt.json')['files']
assert copied['expression_rig.gd']==runtime
for name in [name for name in p['protected_files'] if name!='project.godot']+['expressions/registry.json','expressions/EXP-129.json','expressions/EXP-041.json','expressions/EXP-061.json']:
 assert copied[name]==sha(name),'Native-tested source differs from current production: '+name
prior=read('validation/approved_mental_arithmetic/prior36_native_parity/RESULT.json');assert prior['status']=='PASS' and prior['checks']==731 and prior['pixel_matches']==180 and prior['captured_checkpoints']==90
s=read('APPROVED_INTEGRATION_STATUS.json');assert s['approved_profile_ids']==ids and not s['current_runtime_changes'] and not s['normal_speed_playback_observed'] and not s['live_engine_pacing_measured']
r=read('RELEASE.json');assert r['approved_registry']==ids and r['approved_published_count']==39 and r['newly_approved']==ids[36:]
assert r['native_visual_parity'].startswith('PASS') and 'pixel-identical' in r['new_expression_limits']['EXP-041']
print('APPROVED39_GUARD PASS prior_profiles=36 PNGs=184 new_profiles=3 runtime_changed=false native_pairs=726 live_pacing=UNVERIFIED')

"""Current single-expression approved46 integrity guard, not engine validation."""
from pathlib import Path
import hashlib,json,sys
R=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[1]
def read(n):return json.loads((R/n).read_text())
def sha(n):return hashlib.sha256((R/n).read_bytes()).hexdigest()
BASE_MANIFEST_SHA256='636b1e0dc488c89edbebe8ae542a1078faf679f37afbc180f512d52bf6f6660b'
PROFILE_SHA256='1de491628e031953c765a47287d3ac230abb73e6adbdab15a3f8c11d1b41161e'
VIDEO_SHA256='ecceb235ec358e99302e78d8b065d0c2f6edf8cb4fdbe7e86a3a1abab0bd0e29'
V='validation/approved_exasperated_sigh/';H='historical_capture_metadata/approved45_before_exasperated_sigh/'
m=read('APPROVED_SOURCE_MANIFEST.json');assert m['approved_profiles']==46 and m['new_profiles']==['EXP-046']
excluded={'APPROVED_SOURCE_MANIFEST.json','APPROVED_SOURCE_FILES.sha256'}
actual={str(p.relative_to(R)) for p in R.rglob('*') if p.is_file() and not {'.godot','__pycache__','test_home','test_xdg'}&set(p.relative_to(R).parts) and not p.name.endswith('.pyc')}
actual={p for p in actual if not p.endswith(('.uid','.import')) or p in m['files']}
assert actual-excluded==set(m['files']),'Inventory mismatch'
for n,h in m['files'].items():assert sha(n)==h,'Changed source: '+n
assert (R/'APPROVED_SOURCE_FILES.sha256').read_text()==''.join(f'{h}  {n}\n' for n,h in sorted(m['files'].items()))
assert sha(H+'APPROVED_SOURCE_MANIFEST.json')==BASE_MANIFEST_SHA256
base=read(H+'APPROVED_SOURCE_MANIFEST.json');p=read(V+'predecessor_preservation.json')
assert p['prior_profile_count']==45 and p['png_count']==184 and not p['runtime_changed'] and not p['artwork_changed']
assert p['protected_files']=={n:h for n,h in base['files'].items() if n not in p['modified_archived_files']}
for n,h in p['protected_files'].items():assert sha(n)==h,'Predecessor changed: '+n
for n,h in p['modified_archived_files'].items():
 assert sha(H+n)==h,'Archived predecessor changed: '+n
 if n in base['files']:assert h==base['files'][n]
assert len([n for n in actual if n.endswith('.png')])==184
entries=read('expressions/registry.json')['entries'];old=read(H+'expressions/registry.json')['entries'];ids=[e['id'] for e in entries]
assert len(ids)==len(set(ids))==46 and entries[:45]==old and ids[45:]==['EXP-046']
assert entries[-1]=={'id':'EXP-046','path':'res://expressions/EXP-046.json','aliases':['exasperated_sigh'],'trigger_phase':'weary_onset'}
assert not set(ids)&{'EXP-091','EXP-092','EXP-192','EXP-097','EXP-170','EXP-187','EXP-142','EXP-033'}
for e in entries:
 d=read(e['path'][6:]);assert d['id']==e['id'] and d['keyframes'][0]['time']==0 and d['keyframes'][-1]['time']==d['duration']
 assert all(v==0 for k in [d['keyframes'][0],d['keyframes'][-1]] for v in k['values'].values())
i=read(V+'approved_review_identity.json')['profiles'];assert len(i)==1;i=i[0]
assert i['id']=='EXP-046' and i['profile_sha256']==PROFILE_SHA256 and i['video_sha256']==VIDEO_SHA256
assert sha(i['profile_path'])==PROFILE_SHA256 and sha(i['video_path'])==VIDEO_SHA256
for f in i['preserved_review_files']:assert sha(f['path'])==f['sha256']
r=read(i['motion_path']);assert r['status']=='PASS' and r['failures']==[] and r['profile_sha256']==PROFILE_SHA256 and [x['frame'] for x in r['records']]==list(range(145))
a=read(V+'current_user_approvals.json')['profiles'];assert len(a)==1 and a[0]['id']=='EXP-046' and a[0]['status']=='USER_APPROVED_EXACT_REVIEW_VERSION' and a[0]['profile_sha256']==PROFILE_SHA256 and a[0]['review_video_sha256']==VIDEO_SHA256
assert {'speaker':'user','text':'good.'} in a[0]['approval_evidence']
c=read(V+'review_runtime_compatibility.json');assert c['status']=='PASS' and c['required_runtime_delta'] is None and not c['native_engine_rerun']
for n,h in c['production_runtime_and_artwork_sha256'].items():assert sha(n)==h
result=read('APPROVED_INTEGRATION_TEST_RESULTS.json');assert result['status']=='PASS_WITH_ENGINE_CHECKS_NOT_RUN' and not result['runtime_changed'] and not result['artwork_changed'] and not result['ci_run']
assert result['runtime_sha256']==sha('expression_rig.gd')==base['files']['expression_rig.gd']
model=read(V+'python_model_checks.json');assert model['status']=='PASS' and model['failures']==[] and model['checks']==6675775
for k,v in {'validated_profiles':46,'prior45_samples_at_60hz':10815,'approved_review_pose_samples':145,'all46_samples_at_240hz':44017,'directed_pairs':91,'cross_key_midpoint_cases':1965,'cross_boundary_samples':141480,'interrupted_lifecycle_cases':9825}.items():assert model[k]==v
assert model['maximum_review_pose_error']<1e-7 and not model['godot_executed'] and not model['native_rendering_executed'] and not model['historical_tests_rerun'] and not model['ci_run']
assert sha(V+'python_model_checks.json')==result['current_python_model']['sha256']
log=(R/V/'python_model_unit_tests.log').read_text();assert 'Ran 28 tests' in log and log.rstrip().endswith('OK')
media=read(V+'media_integrity.json');assert media['status']=='PASS' and media['baseline_pngs_decoded']==184 and media['historical_native_rgba_images_verified']==310 and media['historical_video_frames_decoded']==145 and media['new_images_rendered']==0 and not media['current_engine_executed']
assert sha(V+'media_integrity.json')==result['current_media_integrity']['sha256']
release=read('RELEASE.json');assert release['approved_registry']==ids and release['approved_published_count']==46 and release['newly_approved']==['EXP-046'] and 'NOT RUN' in release['native_visual_parity']
status=read('APPROVED_INTEGRATION_STATUS.json');assert status['approved_profile_ids']==ids and status['current_engine_validation']=='NOT RUN' and status['current_native_validation']=='NOT RUN'
assert result['current_godot_state_checks']=='NOT RUN' and result['current_native_visual_parity']=='NOT RUN'
negative=read(V+'guard_negative_results.json');assert negative['status']=='PASS' and negative['tamper_cases']==12 and negative['all_rejected'] and negative['restored_copy_passes']==12
print('APPROVED46_GUARD PASS prior_profiles=45 PNGs=184 new_profiles=1 model_checks=6675775 current_engine=NOT_RUN current_native=NOT_RUN')

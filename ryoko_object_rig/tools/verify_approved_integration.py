"""Approved47 expression and approved full-body source-integrity guard, not engine validation."""
from pathlib import Path
import hashlib,json,sys
R=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[1]
def read(n):return json.loads((R/n).read_text())
def sha(n):return hashlib.sha256((R/n).read_bytes()).hexdigest()
face_approval=read('full_body/face_review/APPROVAL.json')
approved_edits=face_approval['approved_existing_changes']
def check_protected(name, expected):
 if name in approved_edits:
  edit=approved_edits[name]
  assert edit['before_sha256']==expected,'Unexpected approval predecessor: '+name
  expected=edit['after_sha256']
 assert sha(name)==expected,'Protected source changed: '+name
BASE_MANIFEST_SHA256='f17df8990d20f8e11918f535ae3f838ad132b25a18442f41115fc16bf44a2ebd'
PROFILE_SHA256='67cae056cbc90fe0de20820131d750a97ada4ccc0340575ee43ec18963bbda6a'
VIDEO_SHA256='035ed33369ba957d2e2c1275cee377b0f9a21d3b6b2c529ea88592dbddfb4d19'
V='validation/approved_overly_sweet_taste/';H='historical_capture_metadata/approved46_before_overly_sweet_taste/'
m=read('APPROVED_SOURCE_MANIFEST.json');assert m['approved_profiles']==47 and m['new_profiles']==['EXP-091']
excluded={'APPROVED_SOURCE_MANIFEST.json','APPROVED_SOURCE_FILES.sha256'}
actual={str(p.relative_to(R)) for p in R.rglob('*') if p.is_file() and not {'.godot','__pycache__','test_home','test_xdg'}&set(p.relative_to(R).parts) and not p.name.endswith('.pyc')}
actual={p for p in actual if not p.endswith(('.uid','.import')) or p in m['files']}
assert actual-excluded==set(m['files']),'Inventory mismatch'
for n,h in m['files'].items():assert sha(n)==h,'Changed source: '+n
assert (R/'APPROVED_SOURCE_FILES.sha256').read_text()==''.join(f'{h}  {n}\n' for n,h in sorted(m['files'].items()))
assert sha(H+'APPROVED_SOURCE_MANIFEST.json')==BASE_MANIFEST_SHA256
base=read(H+'APPROVED_SOURCE_MANIFEST.json');p=read(V+'predecessor_preservation.json')
assert p['prior_profile_count']==46 and p['png_count']==184 and not p['runtime_changed'] and not p['artwork_changed']
assert p['protected_files']=={n:h for n,h in base['files'].items() if n not in p['modified_archived_files']}
for n,h in p['protected_files'].items():check_protected(n,h)
for n,h in p['modified_archived_files'].items():
 assert sha(H+n)==h,'Archived predecessor changed: '+n
 if n in base['files']:assert h==base['files'][n]
assert len([n for n in actual if n.endswith('.png') and not n.startswith('full_body/')])==184
entries=read('expressions/registry.json')['entries'];old=read(H+'expressions/registry.json')['entries'];ids=[e['id'] for e in entries]
assert len(ids)==len(set(ids))==47 and entries[:46]==old and ids[46:]==['EXP-091']
assert entries[-1]=={'id':'EXP-091','path':'res://expressions/EXP-091.json','aliases':['overly_sweet_taste'],'trigger_phase':'taste_intake'}
assert not set(ids)&{'EXP-092','EXP-192','EXP-097','EXP-170','EXP-187','EXP-142','EXP-033'}
for e in entries:
 d=read(e['path'][6:]);assert d['id']==e['id'] and d['keyframes'][0]['time']==0 and d['keyframes'][-1]['time']==d['duration']
 assert all(v==0 for k in [d['keyframes'][0],d['keyframes'][-1]] for v in k['values'].values())
i=read(V+'approved_review_identity.json')['profiles'];assert len(i)==1;i=i[0]
assert i['id']=='EXP-091' and i['profile_sha256']==PROFILE_SHA256 and i['video_sha256']==VIDEO_SHA256
assert sha(i['profile_path'])==PROFILE_SHA256 and sha(i['video_path'])==VIDEO_SHA256
for f in i['preserved_review_files']:assert sha(f['path'])==f['sha256']
r=read(i['motion_path']);assert r['status']=='PASS' and r['failures']==[] and r['profile_sha256']==PROFILE_SHA256 and [x['frame'] for x in r['records']]==list(range(121))
a=read(V+'current_user_approvals.json')['profiles'];assert len(a)==1 and a[0]['id']=='EXP-091' and a[0]['status']=='USER_APPROVED_EXACT_REVIEW_VERSION' and a[0]['profile_sha256']==PROFILE_SHA256 and a[0]['review_video_sha256']==VIDEO_SHA256
assert {'speaker':'user','text':'Nice'} in a[0]['approval_evidence']
c=read(V+'review_runtime_compatibility.json');assert c['status']=='PASS' and c['required_runtime_delta'] is None and not c['native_engine_rerun']
for n,h in c['production_runtime_and_artwork_sha256'].items():check_protected(n,h)
result=read('APPROVED_INTEGRATION_TEST_RESULTS.json');assert result['status']=='PASS_WITH_ENGINE_CHECKS_NOT_RUN' and not result['runtime_changed'] and not result['artwork_changed'] and not result['ci_run']
assert result['runtime_sha256']==sha('expression_rig.gd')==base['files']['expression_rig.gd']
model=read(V+'python_model_checks.json');assert model['status']=='PASS' and model['failures']==[] and model['checks']==6613546
for k,v in {'validated_profiles':47,'prior46_samples_at_60hz':11104,'approved_review_pose_samples':121,'approved_review_static_pose_samples':9,'approved_review_lifecycle_pose_samples':270,'all47_samples_at_240hz':44978,'directed_pairs':93,'cross_key_midpoint_cases':1917,'cross_boundary_samples':138024,'interrupted_lifecycle_cases':9585}.items():assert model[k]==v
assert model['maximum_review_pose_error']<1e-7 and not model['godot_executed'] and not model['native_rendering_executed'] and not model['historical_tests_rerun'] and not model['ci_run']
assert sha(V+'python_model_checks.json')==result['current_python_model']['sha256']
log=(R/V/'python_model_unit_tests.log').read_text();assert 'Ran 28 tests' in log and log.rstrip().endswith('OK')
media=read(V+'media_integrity.json');assert media['status']=='PASS' and media['baseline_pngs_decoded']==184 and media['historical_native_rgba_images_verified']==260 and media['historical_frozen_inputs_verified']==1175 and media['historical_video_frames_decoded']==121 and media['new_images_rendered']==0 and not media['current_engine_executed']
assert sha(V+'media_integrity.json')==result['current_media_integrity']['sha256']
release=read('RELEASE.json');assert release['approved_registry']==ids and release['approved_published_count']==47 and release['approved_local_count']==47 and release['published_with_containing_commit'] and release['newly_approved']==['EXP-091'] and 'NOT RUN' in release['native_visual_parity']
status=read('APPROVED_INTEGRATION_STATUS.json');assert status['approved_profile_ids']==ids and status['current_engine_validation']=='NOT RUN' and status['current_native_validation']=='NOT RUN'
assert result['current_godot_state_checks']=='NOT RUN' and result['current_native_visual_parity']=='NOT RUN'
assert result['remote_backup']=='NOT VERIFIED' and status['remote_backup']=='NOT VERIFIED'
assert result['publication']=='AUTHORIZED_FOR_SINGLE_EXPRESSION_MAIN_UPDATE' and status['remote_publication'].startswith('Effective when containing commit is published;')
negative=read(V+'guard_negative_results.json');assert negative['status']=='PASS' and negative['tamper_cases']==12 and negative['all_rejected'] and negative['restored_copy_passes']==12
print('APPROVED47_GUARD PASS prior_profiles=46 PNGs=184 new_profiles=1 model_checks=6613546 current_engine=NOT_RUN current_native=NOT_RUN')

# The original body approval remains historical; exact later integrated-face edits are separately approved.
body=read('full_body/APPROVAL.json')
assert body['status']=='USER_APPROVED_FULL_BODY_AND_SMALL_BOUNCE'
assert {'speaker':'user','text':'nice'} in body['approval_evidence']
assert release['full_body']['record']=='full_body/APPROVAL.json'
for n,h in body['reviewed_files_unchanged'].items():check_protected('full_body/'+n,h)
for n,h in body['predecessor_metadata_archived'].items():assert sha('full_body/approval/predecessor_metadata/'+n)==h,'Archived predecessor metadata changed: '+n
for key in ['neutral_preview','bounce_preview']:
 assert sha('full_body/'+body[key]['path'])==body[key]['sha256']
assert read('full_body/registration.json')['version']==5
assert read('full_body/review/bounce_checks.json')['status']=='PASS'
print('APPROVED_FULL_BODY_GUARD PASS reviewed source identity retained; native rendering/pacing UNVERIFIED')

assert face_approval['status']=='USER_APPROVED_ALL47_EXPRESSIONS_ON_FULL_BODY'
assert {'speaker':'user','text':'good','context':'Response to the delivered complete all47 full-body expression MP4.'} in face_approval['approval_evidence']
assert set(approved_edits)=={'project.godot','full_body/full_body_rig.gd','full_body/full_body_viewer.gd','parts/caught_staring/transport.gdshader','parts/caught_staring/upper_opening_part.gd'}
for n,edit in approved_edits.items():
 assert sha(n)==edit['after_sha256']
 assert sha('full_body/face_review/approval/predecessor_metadata/'+n)==edit['before_sha256']
for n,h in face_approval['predecessor_metadata_archived'].items():assert sha('full_body/face_review/approval/predecessor_metadata/'+n)==h
video=face_approval['approved_video']
assert sha('full_body/face_review/'+video['path'])==video['sha256']
assert not video['native_godot_capture']
import subprocess
subprocess.run([sys.executable,str(R/'full_body/face_review/verify_integration.py')],check=True)
print('APPROVED_FULL_BODY_EXPRESSIONS_GUARD PASS exact reviewed implementation and MP4 retained; all47 original profiles preserved')

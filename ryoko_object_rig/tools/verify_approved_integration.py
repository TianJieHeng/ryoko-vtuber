"""Current approved45 source/identity/preservation guard, not engine validation."""
from pathlib import Path
import hashlib,json,sys
R=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[1]
def read(n):return json.loads((R/n).read_text())
def sha(n):return hashlib.sha256((R/n).read_bytes()).hexdigest()
EXPECTED={'EXP-123': {'profile': 'a0ebc834b361cee3352b9687de768895c4c6182cc90c343ebff0851c6037661e', 'video': '5df48deb24bc3a86084799084fd65a004bd7b4af4459ed1eea6d838225930db3', 'commit': '21cf405c00545b8e420428d74bc841bf4882b670'}, 'EXP-081': {'profile': '4a6783b9232217ed468f626dc36e5c4c43dc0a5a284108a210ef1975496e1dd9', 'video': '71bf7075205155776165e147b06ae5ada1c1158f2a0401dcc8be94d39babbc6f', 'commit': '4949bfce015e0a078fe9210c6b8e037b533c1221'}, 'EXP-161': {'profile': 'c260d3a88b6e3ed02877cf9f334de5e6e43f921f14c96f952b78193498b3486e', 'video': '9ee4cbb7cee2dd79549363c472dd0ff7f0234e40282951745e90f921aef38475', 'commit': 'b9b42fa411bf6180168b2cee704f9c02167ca45d'}, 'EXP-045': {'profile': '53f59fc53968bc626e0f3ead5e9f66f03e24d06c1a900106e442cc04dc28180d', 'video': 'e323bd40288f1907033a94ad7a24418ecd9ace7e8e39dd2da609e2d61357bae7', 'commit': 'd61feabd293a28222331129e511cf3da51bdf67c'}, 'EXP-104': {'profile': 'c25530c816fb25c52387d430ba2174287a960c740ce85e11745a35f4f34617fd', 'video': 'caa4914959146c87fa371a17e829ca3c5d85b4db4a273b341f62781a8b33d17b', 'commit': 'da2695dd923e87204adb3156ebb39236c841e5e1'}, 'EXP-096': {'profile': '21ba5c4393ed672a5496ed28577068bd4b56e3b8ff5d7ac4f9674df03badf1fe', 'video': '2b410146ed28ec4d6240e3e47c6b6f27d9c33b1a8087c101941da9a6a2d58716', 'commit': '85a8bcd62a428087eb5702cb8cdee9d7594a072e'}}
BASE_MANIFEST_SHA256='5cce84a2bf043409f7ab68a5cbda3f8c87095360b0e921435a0cf8e0f5e3e2f5'
V='validation/approved_batch45/';H='historical_capture_metadata/approved39_before_batch45/'
m=read('APPROVED_SOURCE_MANIFEST.json');assert m['approved_profiles']==45
excluded={'APPROVED_SOURCE_MANIFEST.json','APPROVED_SOURCE_FILES.sha256'}
actual={str(p.relative_to(R)) for p in R.rglob('*') if p.is_file() and not {'.godot','__pycache__','test_home','test_xdg'}&set(p.relative_to(R).parts) and not p.name.endswith('.pyc')}
actual={p for p in actual if not p.endswith(('.uid','.import')) or p in m['files']}
assert actual-excluded==set(m['files']),f'Inventory mismatch: added={actual-excluded-set(m["files"])} missing={set(m["files"])-actual}'
for n,h in m['files'].items():assert sha(n)==h,'Changed source: '+n
assert (R/'APPROVED_SOURCE_FILES.sha256').read_text()==''.join(f'{h}  {n}\n' for n,h in sorted(m['files'].items()))
assert sha(H+'APPROVED_SOURCE_MANIFEST.json')==BASE_MANIFEST_SHA256,'Predecessor manifest changed'
base=read(H+'APPROVED_SOURCE_MANIFEST.json');p=read(V+'predecessor_preservation.json')
assert p['prior_profile_count']==39 and p['png_count']==184 and not p['runtime_changed'] and not p['artwork_changed']
expected_protected={n:h for n,h in base['files'].items() if n not in p['modified_archived_files']}
assert p['protected_files']==expected_protected
for n,h in p['protected_files'].items():assert sha(n)==h,'Predecessor changed: '+n
for n,h in p['modified_archived_files'].items():
 assert sha(H+n)==h,'Archived source changed: '+n
 if n in base['files']:assert h==base['files'][n]
assert len([n for n in actual if n.endswith('.png')])==184
entries=read('expressions/registry.json')['entries'];old=read(H+'expressions/registry.json')['entries'];ids=[e['id'] for e in entries]
assert len(ids)==len(set(ids))==45 and entries[:39]==old and ids[39:]==list(EXPECTED)
assert not set(ids)&{'EXP-046','EXP-091','EXP-092','EXP-192','EXP-097','EXP-170','EXP-187','EXP-142','EXP-033'}
aliases=['puzzled','mild_disgust','sleepy','irritated_side_eye','triumphant_grin','headache_tension']
assert [e['aliases'] for e in entries[39:]]==[[a] for a in aliases]
for e in entries:
 d=read(e['path'][6:]);assert d['id']==e['id'];assert d['keyframes'][0]['time']==0 and d['keyframes'][-1]['time']==d['duration']
 assert all(v==0 for k in [d['keyframes'][0],d['keyframes'][-1]] for v in k['values'].values())
identity=read(V+'approved_review_identity.json')['profiles'];assert [i['id'] for i in identity]==list(EXPECTED)
for i in identity:
 e=EXPECTED[i['id']];assert i['review_commit']==e['commit'] and i['profile_sha256']==e['profile'] and i['video_sha256']==e['video']
 assert sha(i['profile_path'])==e['profile'] and sha(i['video_path'])==e['video']
 for f in i['preserved_review_files']:assert sha(f['path'])==f['sha256']
 records=read(i['motion_path']);assert records['profile_sha256']==e['profile'] and [r['frame'] for r in records['records']]==list(range(121))
a=read(V+'current_user_approvals.json')['profiles'];assert [i['id'] for i in a]==list(EXPECTED)
for i in a:assert i['status']=='USER_APPROVED_EXACT_REVIEW_VERSION' and i['profile_sha256']==EXPECTED[i['id']]['profile'] and i['review_video_sha256']==EXPECTED[i['id']]['video']
assert a[0]['approval_evidence'][-1]=={'speaker':'user','text':'yah thats good'}
for i in read(V+'review_runtime_compatibility.json')['profiles']:assert not i['runtime_scenes_shaders_artwork_changed'] and i['required_runtime_delta'] is None and i['png_count']==184
result=read('APPROVED_INTEGRATION_TEST_RESULTS.json');assert result['status']=='PASS_WITH_ENGINE_CHECKS_NOT_RUN' and not result['runtime_changed'] and not result['artwork_changed'] and not result['ci_run']
assert result['runtime_sha256']==sha('expression_rig.gd')==base['files']['expression_rig.gd']
model=read(V+'python_model_checks.json');assert model['status']=='PASS' and model['failures']==[] and model['checks']==27453131
for k,v in {'validated_profiles':45,'prior39_samples_at_60hz':9369,'approved_review_pose_samples':726,'all45_samples_at_240hz':42864,'directed_pairs':504,'cross_key_midpoint_cases':10356,'cross_boundary_samples':745632,'interrupted_lifecycle_cases':51780}.items():assert model[k]==v
assert model['maximum_review_pose_error']<1e-7 and not model['godot_executed'] and not model['native_rendering_executed'] and not model['historical_tests_rerun'] and not model['ci_run']
assert sha(V+'python_model_checks.json')==result['current_python_model']['sha256']
assert 'Ran 28 tests' in (R/(V+'python_model_unit_tests.log')).read_text() and (R/(V+'python_model_unit_tests.log')).read_text().rstrip().endswith('OK')
media=read(V+'media_integrity.json');assert media['status']=='PASS' and media['baseline_pngs_decoded']==184 and media['historical_video_frames_decoded']==726 and media['new_images_rendered']==0
assert sha(V+'media_integrity.json')==result['current_media_integrity']['sha256']
negative=read(V+'guard_negative_results.json');assert negative['status']=='PASS' and negative['tamper_cases']==12 and negative['all_rejected'] and negative['restored_copy_passes']==12
release=read('RELEASE.json');assert release['approved_registry']==ids and release['approved_published_count']==45 and release['newly_approved']==ids[39:] and 'NOT RUN' in release['native_visual_parity']
status=read('APPROVED_INTEGRATION_STATUS.json');assert status['approved_profile_ids']==ids and status['current_engine_validation']=='NOT RUN' and status['current_native_validation']=='NOT RUN'
assert result['current_godot_state_checks']=='NOT RUN' and result['current_native_visual_parity']=='NOT RUN'
print('APPROVED45_GUARD PASS prior_profiles=39 PNGs=184 new_profiles=6 runtime_changed=false Python_model_checks=27453131 current_engine=NOT_RUN current_native=NOT_RUN')

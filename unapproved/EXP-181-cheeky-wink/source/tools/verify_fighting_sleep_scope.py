"""Exact scoped EXP-164 successor guard. Does not write or rebuild artwork."""
from pathlib import Path
import json,hashlib,sys
P=Path(__file__).resolve().parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
freeze=json.loads((P/'source_references/fighting_sleep_parent_inventory.json').read_text())
base=freeze['files'];assert len(base)==545 and sum(x.endswith('.png') for x in base)==182
assert hashlib.sha256(json.dumps(base,sort_keys=True,separators=(',',':')).encode()).hexdigest()=='806ffe2b9ed198e4a9d0eb3e4b8a441e14c113110601dec7a70b0fb7a5714438'
allowed_changed={'tests/test_meditative_runtime.gd', 'tests/test_brow_inner_lift_contract.gd', 'tests/test_auto_blink_lifecycle.gd', 'tests/test_giggle_runtime.gd', 'tests/test_spread_runtime.gd', 'test_expression_backbone.gd', 'expressions/registry.json', 'tests/test_oral_lift_contract.gd', 'tests/test_purse_contract.gd', 'tests/test_shy_laughter_runtime.gd', 'tests/test_down_extra_runtime.gd', 'tests/test_relief_runtime.gd', 'SOURCE_FILES.sha256', 'RELEASE.json', 'tests/test_affection_runtime.gd', 'tests/test_reassurance_runtime.gd', 'README.md', 'tests/test_purse_transport.gd', 'tests/test_private_pride_runtime.gd'}
allowed_new={'tools/verify_fighting_sleep_scope.py', 'source_references/fighting_sleep_static_acceptance.json', 'source_references/fighting_sleep_timing_review.md', 'source_references/fighting_sleep_predecessor_registry.json', 'source_references/fighting_sleep_pose_timing_map.json', 'source_references/fighting_sleep_parent_inventory.json', 'source_references/EXP-164_reference_metadata.json', 'source_references/fighting_sleep_selected_timing_probe.json', 'source_references/fighting_sleep_accepted_pose_plan.json', 'source_references/fighting_sleep_predecessor_RELEASE.json', 'validation/fighting_sleep_scope_delta.json', 'tests/test_fighting_sleep_runtime.gd', 'source_references/EXP-164_original_390.json', 'FIGHTING_SLEEP_VALIDATION.md', 'expressions/EXP-164.json', 'source_references/fighting_sleep_parent_overrides.json', 'tools/review_fighting_sleep_trajectory.gd'}
review_changed=set(allowed_changed)
allowed_changed|={'PACKAGING.md','CONTROL_API.md','LOCAL_CONTROL_BRIDGE.md'}
allowed_new|={'FIGHTING_SLEEP_PUBLICATION_VALIDATION.md','source_references/fighting_sleep_review_inventory.json'}
actual={p.relative_to(P).as_posix():sha(p) for p in P.rglob('*') if p.is_file()}
changed={x for x in base if actual.get(x)!=base[x]};assert changed==allowed_changed,(changed-allowed_changed,allowed_changed-changed)
assert set(actual)-set(base)==allowed_new,(set(actual)-set(base)-allowed_new,allowed_new-(set(actual)-set(base)))
for x in base:
 if x not in allowed_changed:assert actual[x]==base[x],x
assert sum(x.endswith('.png') for x in actual)==182
assert not any(x.startswith('.godot/') for x in actual)
assert not any(x.endswith(('.uid','.import')) for x in allowed_new)
prior=['EXP-163','EXP-005','EXP-001','EXP-006','EXP-107','EXP-007','EXP-002','EXP-152','EXP-160','EXP-177']
reg=json.loads((P/'expressions/registry.json').read_text())
assert [e['id'] for e in reg['entries']]==prior+['EXP-164']
parent_registry=P/'source_references/fighting_sleep_predecessor_registry.json'
assert sha(parent_registry)==base['expressions/registry.json']
assert reg['entries'][:-1]==json.loads(parent_registry.read_text())['entries']
assert {p.name for p in (P/'expressions').glob('EXP-*.json')}=={e+'.json' for e in prior[1:]+['EXP-164']}
assert reg['entries'][-1]=={'id':'EXP-164','path':'res://expressions/EXP-164.json','aliases':['fighting-sleep','fighting_sleep'],'trigger_phase':'first_sink'}
oldreg=json.loads((P/'source_references/fighting_sleep_predecessor_RELEASE.json').read_text())
assert oldreg['approved_registry']==prior
profile=json.loads((P/'expressions/EXP-164.json').read_text());assert profile['duration']==3.47 and len(profile['keyframes'])==15
assert 'Newly authored' in profile['timing_origin']
plan=json.loads((P/'source_references/fighting_sleep_accepted_pose_plan.json').read_text())
mapfile=json.loads((P/'source_references/fighting_sleep_pose_timing_map.json').read_text())
assert mapfile['profile_sha256']=='bb5d72a568358aa655f5acb81889c80aa2ee9a4d6214cdf62421c5504f7da64d', 'frozen review pose map retained'
assert mapfile['accepted_plan_sha256']==sha(P/'source_references/fighting_sleep_accepted_pose_plan.json')
for pose in plan['poses']:
 for t in mapfile['key_pose_times'][str(pose['key_pose'])]:
  assert next(k for k in profile['keyframes'] if k['time']==t)['values']==pose['values']
allowed={'blink_R','blink_L','brow_screen_left','brow_screen_right','brow_tilt_screen_left','brow_tilt_screen_right','brow_inner_lift_screen_left','brow_inner_lift_screen_right','mouth_purse'}
for k in profile['keyframes']:
 assert all(v==0 for c,v in k['values'].items() if c not in allowed)
 assert 0<=k['values']['mouth_purse']<=.2 and 0<=k['values']['blink_R']<=.7 and 0<=k['values']['blink_L']<=.7
release=json.loads((P/'RELEASE.json').read_text());assert release['user_approved'] is True and release['published'] is True and release['approved_registry']==release['authored_registry']==prior+['EXP-164'] and release['approved_predecessors']==prior and release['pending_review']==[]
receipt=json.loads((P/'validation/fighting_sleep_scope_delta.json').read_text())
assert receipt['parent_inventory_sha256']==freeze['inventory_sha256']
assert receipt['candidate_user_approved'] is True and receipt['published'] is True
assert receipt['files']=={x:actual[x] for x in sorted(actual) if x not in {'validation/fighting_sleep_scope_delta.json','SOURCE_FILES.sha256'}}
overrides=json.loads((P/'source_references/fighting_sleep_parent_overrides.json').read_text())
assert set(overrides)==review_changed
assert all(hashlib.sha256(text.encode()).hexdigest()==base[n] for n,text in overrides.items())
manifest={}
for row in (P/'SOURCE_FILES.sha256').read_text().splitlines():
 h,sep,n=row.partition('  ');assert sep=='  ' and n not in manifest;manifest[n]=h
assert manifest=={n:h for n,h in actual.items() if n!='SOURCE_FILES.sha256'}
selected=json.loads((P/'source_references/fighting_sleep_selected_timing_probe.json').read_text())
assert [k['time'] for k in profile['keyframes']]==selected['alternative_times']
original=json.loads((P/'source_references/EXP-164_original_390.json').read_text())
assert [k['values'] for k in profile['keyframes']]==[k['values'] for k in original['keyframes']]
holds=[(profile['keyframes'][i-1]['time'],k['time']) for i,k in enumerate(profile['keyframes']) if i and k['values']==profile['keyframes'][i-1]['values']]
assert len(holds)==6
assert all(abs((b-a)-old)<1e-10 for (a,b),old in zip(holds,[.12,.08,.16,.08,.14,.16]))
review=json.loads((P/'source_references/fighting_sleep_review_inventory.json').read_text())
assert len(review['files'])==562 and hashlib.sha256(json.dumps(review['files'],sort_keys=True,separators=(',',':')).encode()).hexdigest()==review['inventory_sha256']=='c7bbb9de9edff9f7f5c3647d93b7cda275706dd33f213885ea97b61ff0fa87be'
overlay={'README.md','PACKAGING.md','CONTROL_API.md','LOCAL_CONTROL_BRIDGE.md','RELEASE.json','FIGHTING_SLEEP_VALIDATION.md','expressions/EXP-164.json','tools/verify_fighting_sleep_scope.py','validation/fighting_sleep_scope_delta.json','SOURCE_FILES.sha256'}
assert {n for n,h in review['files'].items() if actual[n]!=h}==overlay
assert set(actual)==set(review['files'])|{'FIGHTING_SLEEP_PUBLICATION_VALIDATION.md','source_references/fighting_sleep_review_inventory.json'}
assert hashlib.sha256(review['profile_text'].encode()).hexdigest()==review['files']['expressions/EXP-164.json']=='bb5d72a568358aa655f5acb81889c80aa2ee9a4d6214cdf62421c5504f7da64d'
review_profile=json.loads(review['profile_text']);assert set(profile)==set(review_profile) and {k for k in profile if profile[k]!=review_profile[k]}=={'status'}
assert profile['status']=='User-approved fighting sleep; published with the containing repository commit'
assert sha(P/'expressions/EXP-164.json')==release['published_profile_sha256']=='30b7adfd10aeb10b6edb7eefb968ae44d589c9a516cd161ff39c5833c466e110'
assert release['reviewed_profile_sha256']=='bb5d72a568358aa655f5acb81889c80aa2ee9a4d6214cdf62421c5504f7da64d' and release['approved_review_inventory_sha256']==review['inventory_sha256']
assert receipt['parent_commit']==release['base_main']==freeze['commit']=='958eb944a37ce836fec5acf369f12b89f47b6656'
print(json.dumps({'status':'PASS','parent_commit':freeze['commit'],'files':len(actual),'pngs':182,'protected_parent_files':len(base)-len(changed),'changed_paths':sorted(changed),'new_paths':sorted(allowed_new),'runtime_art_old_profiles_unchanged':True,'only_registered_addition':'EXP-164','generated_extras':[]},indent=2))

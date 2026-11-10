"""Current approved26 source guard; prior receipts retain historical scope."""
from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text())
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
m=read('APPROVED_SOURCE_MANIFEST.json')
assert m['approved_profiles']==26
exclude={'APPROVED_SOURCE_MANIFEST.json','APPROVED_SOURCE_FILES.sha256'}
tracked=subprocess.check_output(['git','ls-files','-z','--cached','--others','--exclude-standard','--','ryoko_object_rig'],cwd=R.parent).decode().split('\0')
actual={str(Path(p).relative_to('ryoko_object_rig')) for p in tracked if p}
# Godot creates .uid sidecars when importing old scripts. Existing pinned sidecars remain checked.
actual={p for p in actual if not p.endswith('.uid') or p in m['files']}
assert actual-exclude==set(m['files']),f'Inventory mismatch: added={actual-exclude-set(m["files"])} missing={set(m["files"])-actual}'
for name,h in m['files'].items():assert sha(name)==h,name
assert (R/'APPROVED_SOURCE_FILES.sha256').read_text()==''.join(f'{h}  {p}\n' for p,h in sorted(m['files'].items()))
entries=read('expressions/registry.json')['entries'];ids=[e['id'] for e in entries]
assert len(ids)==len(set(ids))==26 and ids[-1]=='EXP-090'
assert not {'EXP-142','EXP-033','EXP-097','EXP-187'}&set(ids)
for entry in entries:
 d=read(entry['path'][6:]);assert d['id']==entry['id']
 assert d['keyframes'][0]['time']==0 and d['keyframes'][-1]['time']==d['duration']
 assert all(v==0 for f in [d['keyframes'][0],d['keyframes'][-1]] for v in f['values'].values())
s=read('APPROVED_INTEGRATION_STATUS.json');assert s['approved_profile_ids']==ids and s['native_visual_parity']=='NOT RUN'
assert not s['normal_speed_playback_observed'] and not s['live_engine_pacing_measured'] and not s['current_runtime_changes']
p=read('validation/approved_queasy/predecessor_preservation.json')
for name,h in p['protected_files'].items():assert sha(name)==h,'Predecessor mutation: '+name
assert p['profile_count']==25 and p['png_count']==184 and not p['runtime_changed']
assert sha('expression_rig.gd')==sha('historical_capture_metadata/approved25_before_queasy/expression_rig.gd')
assert sha('expression_rig.gd')==read('historical_capture_metadata/approved25_before_queasy/APPROVED_SOURCE_MANIFEST.json')['files']['expression_rig.gd']
assert read('historical_capture_metadata/approved25_before_queasy/RELEASE.json')['approved_registry']==ids[:-1]
assert read('historical_capture_metadata/approved25_before_queasy/PUBLICATION_RECEIPT.json')['commit']==m['base_main']=='b8697a7be03f789d7e881e472acf05bb8e6fbc19'
b=read('validation/approved_queasy/handoff_boundary_checks.json')
assert b['standalone_exact_samples']>3197 and b['source_target_cases']>12875 and b['transition_samples']==b['source_target_cases']*len(b['boundary_times'])
assert b['old_invalid_pairs']==[] and b['old_invalid_mouth_samples']==0 and b['changed_mouth_samples']==0
for name,expected in read('APPROVED_INTEGRATION_TEST_RESULTS.json')['checks'].items():
 c=read('validation/approved_queasy/'+name);assert c['status']=='PASS' and c['checks']==expected and c['failures']==[]
native=read('validation/approved_queasy/native_parity.json')
review_motion=read('validation/approved_queasy/review_motion_checks.json')
assert native['checks']==53 and [x['frame'] for x in native['records']]==[0,8,17,29,39,60,72,80,113,120]
for record in native['records']:assert record['hashes']==review_motion['records'][record['frame']]['hashes']
for name,expected in [('review_motion_checks.json',3536),('review_motion_state_checks.json',3293)]:
 c=read('validation/approved_queasy/'+name);assert c['status']=='PASS' and c['checks']==expected and not c['failures']
r=read('RELEASE.json');assert r['approved_registry']==ids and r['approved_published_count']==26
assert sha('expressions/EXP-090.json')==m['approved_review_profile_sha256']=='08813729222c8231500233ec6952459b6549e5fd534e87516fb1f99efa17676c'
review=read('validation/approved_queasy/review_REVIEW_RESULT.json')
assert review['profile_sha256']==m['approved_review_profile_sha256']
assert review['video_sha256']==m['approved_review_video_sha256']=='6597d8405fec550a0a9dec4b206e97608cc14a6686fd023a7a0ed928a8198e81'
assert m['approved_review_commit']=='3fca7bd9f82e5d421b7173af9dff3ac8e4adc652'
assert entries[-1]['aliases']==['queasy'] and entries[-1]['trigger_phase']=='neutral'
assert all(read('validation/approved_queasy/guard_negative_tests.json').values())
print('APPROVED_INTEGRATION_GUARD PASS profiles=26 old_profiles=25 old_pngs=184 whole_rig_native_parity=NOT_RUN live_pacing=UNVERIFIED')

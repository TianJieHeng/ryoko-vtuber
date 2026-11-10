"""Current approved27 source guard; prior receipts retain historical scope."""
from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text())
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
m=read('APPROVED_SOURCE_MANIFEST.json')
assert m['approved_profiles']==27
exclude={'APPROVED_SOURCE_MANIFEST.json','APPROVED_SOURCE_FILES.sha256'}
tracked=subprocess.check_output(['git','ls-files','-z','--cached','--others','--exclude-standard','--','ryoko_object_rig'],cwd=R.parent).decode().split('\0')
actual={str(Path(p).relative_to('ryoko_object_rig')) for p in tracked if p}
# Godot creates .uid sidecars when importing old scripts. Existing pinned sidecars remain checked.
actual={p for p in actual if not p.endswith('.uid') or p in m['files']}
assert actual-exclude==set(m['files']),f'Inventory mismatch: added={actual-exclude-set(m["files"])} missing={set(m["files"])-actual}'
for name,h in m['files'].items():assert sha(name)==h,name
assert (R/'APPROVED_SOURCE_FILES.sha256').read_text()==''.join(f'{h}  {p}\n' for p,h in sorted(m['files'].items()))
entries=read('expressions/registry.json')['entries'];ids=[e['id'] for e in entries]
assert len(ids)==len(set(ids))==27 and ids[-1]=='EXP-153'
assert not {'EXP-142','EXP-033','EXP-097','EXP-187'}&set(ids)
for entry in entries:
 d=read(entry['path'][6:]);assert d['id']==entry['id']
 assert d['keyframes'][0]['time']==0 and d['keyframes'][-1]['time']==d['duration']
 assert all(v==0 for f in [d['keyframes'][0],d['keyframes'][-1]] for v in f['values'].values())
s=read('APPROVED_INTEGRATION_STATUS.json');assert s['approved_profile_ids']==ids and s['native_visual_parity']=='NOT RUN'
assert not s['normal_speed_playback_observed'] and not s['live_engine_pacing_measured'] and not s['current_runtime_changes']
p=read('validation/approved_hiding_smile/predecessor_preservation.json')
for name,h in p['protected_files'].items():assert sha(name)==h,'Predecessor mutation: '+name
assert p['profile_count']==26 and p['png_count']==184 and not p['runtime_changed']
assert sha('expression_rig.gd')==sha('historical_capture_metadata/approved26_before_hiding_smile/expression_rig.gd')
assert sha('expression_rig.gd')==read('historical_capture_metadata/approved26_before_hiding_smile/APPROVED_SOURCE_MANIFEST.json')['files']['expression_rig.gd']
assert read('historical_capture_metadata/approved26_before_hiding_smile/RELEASE.json')['approved_registry']==ids[:-1]
assert read('historical_capture_metadata/approved26_before_hiding_smile/PUBLICATION_RECEIPT.json')['commit']==m['base_main']=='2663835145ca90bb1125803a05363f257034de9f'
b=read('validation/approved_hiding_smile/handoff_boundary_checks.json')
assert b['standalone_exact_samples']>3327 and b['source_target_cases']>13832 and b['transition_samples']==b['source_target_cases']*len(b['boundary_times'])
assert b['old_invalid_pairs']==[] and b['old_invalid_mouth_samples']==0 and b['changed_mouth_samples']==0
for name,expected in read('APPROVED_INTEGRATION_TEST_RESULTS.json')['checks'].items():
 c=read('validation/approved_hiding_smile/'+name);assert c['status']=='PASS' and c['checks']==expected and c['failures']==[]
native=read('validation/approved_hiding_smile/native_parity.json')
review_motion=read('validation/approved_hiding_smile/review_motion_checks.json')
assert native['checks']==53 and [x['frame'] for x in native['records']]==[0,7,16,28,42,61,81,103,113,120]
for record in native['records']:assert record['hashes']==review_motion['records'][record['frame']]['hashes']
for name,expected in [('review_motion_checks.json',3536),('review_motion_state_checks.json',3293)]:
 c=read('validation/approved_hiding_smile/'+name);assert c['status']=='PASS' and c['checks']==expected and not c['failures']
r=read('RELEASE.json');assert r['approved_registry']==ids and r['approved_published_count']==27
assert sha('expressions/EXP-153.json')==m['approved_review_profile_sha256']=='8a6b61f41a7d6e619f7bcbee188008d5c454cb2295e2c22460829c40f1b87b76'
review=read('validation/approved_hiding_smile/review_REVIEW_RESULT.json')
assert review['profile_sha256']==m['approved_review_profile_sha256']
assert review['video_sha256']==m['approved_review_video_sha256']=='9642f1afbef44680cc81b2a32a8c49d00a7b6c87f6ba266f39a4f44bf0addfbd'
assert m['approved_review_commit']=='8892bc6e7a7734e3f4d12592b09bf44765058234'
assert entries[-1]['aliases']==['hiding_a_smile'] and entries[-1]['trigger_phase']=='neutral'
assert read('validation/approved_hiding_smile/guard_negative_tests.json')=={key:True for key in ['corrupt_source_rejected','missing_source_rejected','unexpected_source_rejected','restored_clean_pass']}
print('APPROVED_INTEGRATION_GUARD PASS profiles=27 old_profiles=26 old_pngs=184 whole_rig_native_parity=NOT_RUN live_pacing=UNVERIFIED')

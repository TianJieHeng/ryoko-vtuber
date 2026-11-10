"""Current approved24 source guard; prior receipts retain historical scope."""
from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text())
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
m=read('APPROVED_SOURCE_MANIFEST.json')
assert m['approved_profiles']==24
exclude={'APPROVED_SOURCE_MANIFEST.json','APPROVED_SOURCE_FILES.sha256'}
tracked=subprocess.check_output(['git','ls-files','-z','--cached','--others','--exclude-standard','--','ryoko_object_rig'],cwd=R.parent).decode().split('\0')
actual={str(Path(p).relative_to('ryoko_object_rig')) for p in tracked if p}
# Godot creates .uid sidecars when importing old scripts. Existing pinned sidecars remain checked.
actual={p for p in actual if not p.endswith('.uid') or p in m['files']}
assert actual-exclude==set(m['files']),f'Inventory mismatch: added={actual-exclude-set(m["files"])} missing={set(m["files"])-actual}'
for name,h in m['files'].items():assert sha(name)==h,name
assert (R/'APPROVED_SOURCE_FILES.sha256').read_text()==''.join(f'{h}  {p}\n' for p,h in sorted(m['files'].items()))
entries=read('expressions/registry.json')['entries'];ids=[e['id'] for e in entries]
assert len(ids)==len(set(ids))==24 and ids[-1]=='EXP-125'
assert not {'EXP-142','EXP-033','EXP-097','EXP-187'}&set(ids)
for entry in entries:
 d=read(entry['path'][6:]);assert d['id']==entry['id']
 assert d['keyframes'][0]['time']==0 and d['keyframes'][-1]['time']==d['duration']
 assert all(v==0 for f in [d['keyframes'][0],d['keyframes'][-1]] for v in f['values'].values())
s=read('APPROVED_INTEGRATION_STATUS.json');assert s['approved_profile_ids']==ids and s['native_visual_parity']=='NOT RUN'
assert not s['normal_speed_playback_observed'] and not s['live_engine_pacing_measured']
p=read('validation/approved_insight/predecessor_preservation.json')
for name,h in p['protected_files'].items():assert sha(name)==h,'Predecessor mutation: '+name
assert p['profile_count']==23 and p['png_count']==184
assert read('historical_capture_metadata/approved23_before_insight/RELEASE.json')['approved_registry']==ids[:-1]
for name,expected in read('APPROVED_INTEGRATION_TEST_RESULTS.json')['checks'].items():
 c=read('validation/approved_insight/'+name);assert c['status']=='PASS' and c['checks']==expected and c['failures']==[]
for name,expected in [('review_motion_checks.json',788),('review_motion_state_checks.json',569)]:
 c=read('validation/approved_insight/'+name);assert c['status']=='PASS' and c['checks']==expected and not c['failures']
r=read('RELEASE.json');assert r['approved_registry']==ids and r['approved_published_count']==24
assert sha('expressions/EXP-125.json')==m['approved_review_profile_sha256']
print('APPROVED_INTEGRATION_GUARD PASS profiles=24 old_profiles=23 old_pngs=184 whole_rig_native_parity=NOT_RUN live_pacing=UNVERIFIED')

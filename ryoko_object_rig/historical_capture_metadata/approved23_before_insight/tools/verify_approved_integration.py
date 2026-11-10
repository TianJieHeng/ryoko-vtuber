"""Current approved23 source guard; historical receipts retain original scope."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text())
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
m=read('APPROVED_SOURCE_MANIFEST.json')
assert m['approved_profiles']==23
for name,h in m['files'].items():assert sha(name)==h,name
entries=read('expressions/registry.json')['entries'];ids=[e['id'] for e in entries]
assert len(ids)==len(set(ids))==23
assert {'EXP-040','EXP-197','EXP-144'}<=set(ids) and not {'EXP-142','EXP-033','EXP-097','EXP-187'}&set(ids)
for entry in entries:
 d=read(entry['path'][6:]);assert d['id']==entry['id']
 assert d['keyframes'][0]['time']==0 and d['keyframes'][-1]['time']==d['duration']
 assert all(v==0 for f in [d['keyframes'][0],d['keyframes'][-1]] for v in f['values'].values())
s=read('APPROVED_INTEGRATION_STATUS.json')
assert s['approved_profile_ids']==ids and s['native_visual_parity']=='NOT RUN'
assert not s['normal_speed_playback_observed'] and not s['live_engine_pacing_measured']
p=read('validation/approved_composure/predecessor_preservation.json')
for name,h in p['protected_files'].items():assert sha(name)==h,'Predecessor mutation: '+name
assert p['profile_count']==22 and p['png_count']==184
h=read('historical_capture_metadata/approved22_before_composure/RELEASE.json')
assert h['approved_registry']==ids[:-1]
for name,expected in [('integrated_state_checks.json',2108),('pair_state_checks.json',5290),('native_parity.json',53),('pair_state_checks.json',5290),('native_parity.json',53),('review_motion_checks.json',1333),('review_motion_state_checks.json',958)]:
 c=read('validation/approved_composure/'+name);assert c['status']=='PASS' and c['checks']==expected and c['failures']==[]
r=read('RELEASE.json');assert r['approved_registry']==ids and r['approved_published_count']==23
assert sha('expressions/EXP-040.json')==m['approved_review_profile_sha256']
print('APPROVED_INTEGRATION_GUARD PASS profiles=23 old_profiles=22 old_pngs=184 whole_rig_native_parity=NOT_RUN live_pacing=UNVERIFIED')

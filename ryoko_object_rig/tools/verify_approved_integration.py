from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1]
m=json.loads((R/'APPROVED_SOURCE_MANIFEST.json').read_text())
assert m['approved_profiles']==22
for name,sha in m['files'].items():
 assert hashlib.sha256((R/name).read_bytes()).hexdigest()==sha,name
entries=json.loads((R/'expressions/registry.json').read_text())['entries']
ids=[e['id'] for e in entries]
assert len(ids)==len(set(ids))==22
assert {'EXP-197','EXP-144'}<=set(ids) and not {'EXP-142','EXP-033','EXP-097','EXP-187'}&set(ids)
for entry in entries:
 d=json.loads((R/entry['path'][6:]).read_text());assert d['id']==entry['id']
 assert d['keyframes'][0]['time']==0 and d['keyframes'][-1]['time']==d['duration']
 assert all(v==0 for f in [d['keyframes'][0],d['keyframes'][-1]] for v in f['values'].values())
s=json.loads((R/'APPROVED_INTEGRATION_STATUS.json').read_text())
assert s['approved_profile_ids']==ids and s['native_visual_parity']=='NOT RUN'
checks=json.loads((R/'validation/approved_pair/state_checks.json').read_text())
assert checks['status']=='PASS' and checks['checks']==5154
print('APPROVED_INTEGRATION_GUARD PASS profiles=22 native_visual_parity=NOT_RUN')

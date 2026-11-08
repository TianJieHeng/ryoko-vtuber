#!/usr/bin/env python3
"""Read-only source and approval guard for the shared twenty-profile rig."""
from pathlib import Path
import hashlib,json,re,math
P=Path(__file__).resolve().parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
digest=lambda v:hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
read=lambda n:json.loads((P/n).read_text())
C={'ids': ['EXP-163', 'EXP-005', 'EXP-001', 'EXP-006', 'EXP-107', 'EXP-007', 'EXP-002', 'EXP-152', 'EXP-160', 'EXP-177', 'EXP-164', 'EXP-021', 'EXP-158', 'EXP-181', 'EXP-102', 'EXP-116', 'EXP-050', 'EXP-186', 'EXP-114', 'EXP-148'], 'historical_validation_sha256': 'aa2829f4c73ee742f38eda21c2efa44cef6960d3b88e76f69339504c1e423b25', 'published_profile_sha256': 'd803a850c3eda78f4f27586c0798432367fd66c9093c5cd7364bed0020ba47dd', 'registry_sha256': '0cf5a26d2cc4174198624960edd946d47d91eb58796e4cc30c1d703655c03346', 'acting_sha256': 'ac23f5dfc1d5aa1792e218949140ed62de1ffb13601fa1fffceb6741f94f6d46'}
assert not any(p.is_symlink() for p in P.rglob('*')),'symlinks forbidden'
files={p.relative_to(P).as_posix():sha(p) for p in sorted(P.rglob('*')) if p.is_file()}
assert len(files)==664,'missing or extra source files, including generated caches'
frozen={'DARING_PROVOCATION_SOURCE_MANIFEST.json':'789c7136d0765154a9e892c26442e3b6895718e6ea399a58730bb72384b168e4','DARING_PROVOCATION_SOURCE_FILES.sha256':'77e4538d2452084216fbf861a683f0c447c967120728c32aead825d94b2856c9'}
assert all(files[n]==h for n,h in frozen.items()),'historical source evidence changed'
source=read('DARING_PROVOCATION_SOURCE_MANIFEST.json')['files']|frozen
assert len(source)==660 and digest(source)=='515010bd965ac86ccb261e2288ba90935451dc2ef5d262c2d50f48d453389d05'
overlay={'README.md','CONTROL_API.md','LOCAL_CONTROL_BRIDGE.md','PACKAGING.md','RELEASE.json','APPROVED_INTEGRATION_STATUS.json','APPROVED_SOURCE_MANIFEST.json','APPROVED_SOURCE_FILES.sha256','tools/verify_approved_integration.py','expressions/registry.json'}
assert set(source)<=set(files)
assert {n for n in source if files[n]!=source[n]}==overlay,'unexpected source delta'
assert set(files)-set(source)=={'APPROVED_DARING_PROVOCATION_VALIDATION.md','APPROVED_NERVOUS_LAUGH_VALIDATION.md','NERVOUS_LAUGH_CANDIDATE.md','expressions/EXP-148.json'}
assert files['APPROVED_DARING_PROVOCATION_VALIDATION.md']==C['historical_validation_sha256']
m=read('APPROVED_SOURCE_MANIFEST.json')
assert m['schema_version']==3 and m['approved_profiles']==20
assert m['accepted_source_git_tree']=='c3fab643b2d8048ade34c703b4110c7ca4955c4b'
assert m['files']=={n:h for n,h in files.items() if n not in {'APPROVED_SOURCE_MANIFEST.json','APPROVED_SOURCE_FILES.sha256'}}
assert digest(m['files'])==m['inventory_sha256']
lines=(P/'APPROVED_SOURCE_FILES.sha256').read_text().splitlines()
assert all(re.fullmatch(r'[0-9a-f]{64}  [^\r\n]+',line) for line in lines)
checks={line[66:]:line[:64] for line in lines}
assert len(checks)==len(lines) and checks=={n:h for n,h in files.items() if n!='APPROVED_SOURCE_FILES.sha256'}
registry=read('expressions/registry.json');entries=registry['entries'];ids=[e['id'] for e in entries]
assert ids==C['ids'] and len(set(ids))==20 and len({e['path'] for e in entries})==20
assert files['expressions/registry.json']==C['registry_sha256']
assert entries[:-2]==read('source_references/daring_provocation_approved18_registry.json')['entries']
assert len(list((P/'expressions').glob('EXP-*.json')))==19
names=[]
for e in entries:
 names += [e['id']]+e['aliases']
 n=e['path'][6:];assert e['path'].startswith('res://') and '..' not in n
 d=read(n);assert d['id']==e['id'] and isinstance(d['title'],str) and d['title']
 assert math.isfinite(d['duration']) and d['duration']>0
 frames=d['keyframes'];assert len(frames)>=2
 times=[f['time'] for f in frames];assert times==sorted(set(times)) and times[0]==0 and times[-1]==d['duration']
 assert all(math.isfinite(x) and 0<=x<=d['duration'] for x in times)
 assert e['trigger_phase'] in [f['phase'] for f in frames]
 assert all(isinstance(f['phase'],str) and f['phase'] and all(isinstance(x,(int,float)) and math.isfinite(x) for x in f['values'].values()) for f in frames)
 assert all(x==0 for f in [frames[0],frames[-1]] for x in f['values'].values())
 if e['id']!='EXP-148':assert files[n]==source[n],n+' predecessor profile changed'
assert len(names)==len(set(names)),'duplicate ID/alias'
assert not {'EXP-003','EXP-097','EXP-187','EXP-197'}&set(ids)
d=read('expressions/EXP-148.json')
assert files['expressions/EXP-148.json']==C['published_profile_sha256']
assert digest({k:v for k,v in d.items() if k!='status'})==C['acting_sha256']
assert d['status'].startswith('User-approved') and d['duration']==3.6
pngs=[n for n in files if n.endswith('.png')];assert len(pngs)==182
assert all(files[n]==source[n] for n in pngs)
assert sorted(n for n in files if n.endswith('.import'))==['rig_assets/gaze_eyes/iris_screen_left.png.import','rig_assets/gaze_eyes/iris_screen_right.png.import']
s=read('APPROVED_INTEGRATION_STATUS.json');r=read('RELEASE.json')
assert s['approved_profile_ids']==r['approved_registry']==ids
assert s['approved_profile_count']==r['approved_published_count']==r['authored_local_count']==20
assert s['newly_approved_profile_ids']==r['newly_approved']==['EXP-148']
assert r['user_approved'] is True and r['pending_review']==[] and r['approved_predecessors']==ids[:-1]
assert s['accepted_acting_data_sha256']==C['acting_sha256'] and s['published_profile_sha256']==files['expressions/EXP-148.json']
assert s['accepted_registry_sha256']==files['expressions/registry.json']
assert s['capture_frames']==109 and s['capture_fps']==30 and s['separate_anatomical_objects']==262
assert s['pixel_exact_neutral_return'] and s['restart_release_neutral_restoration']
assert all(s[k] is False for k in ['live_engine_pacing_measured','normal_speed_playback_observed','continuous_normal_speed_observation','new_engine_or_display_run','ci_run'])
assert s['smooth_realtime_pacing_status']==r['smooth_realtime_pacing_status']=='UNVERIFIED'
assert s['inherited_exp114_qualification']['smooth_realtime_pacing_status']=='HOLD'
assert {'EXP-097','EXP-187'}<=set(s['excluded_profile_ids'])
print('APPROVED_INTEGRATION_GUARD PASS files=664 profiles=20 old_profiles_exact=19 pngs_exact=182 accepted_acting_exact=true runtime_exact=true live_pacing=UNVERIFIED')

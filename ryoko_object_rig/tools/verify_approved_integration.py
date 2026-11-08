#!/usr/bin/env python3
"""Portable, read-only guard for the current nineteen-profile approval overlay."""
from pathlib import Path
import hashlib,json,re
P=Path(__file__).resolve().parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
digest=lambda v:hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
read=lambda n:json.loads((P/n).read_text())
assert not any(p.is_symlink() for p in P.rglob('*')),'symlink outside exact source contract'
files={p.relative_to(P).as_posix():sha(p) for p in sorted(P.rglob('*')) if p.is_file()}
assert len(files)==661,'extra or missing source files, including caches, are forbidden'
frozen={'DARING_PROVOCATION_SOURCE_MANIFEST.json':'789c7136d0765154a9e892c26442e3b6895718e6ea399a58730bb72384b168e4','DARING_PROVOCATION_SOURCE_FILES.sha256':'77e4538d2452084216fbf861a683f0c447c967120728c32aead825d94b2856c9'}
assert all(files[n]==h for n,h in frozen.items()),'frozen candidate evidence changed'
assert files['source_references/daring_provocation_guard_contract.json']=='66954b3e95adc6a2b2ef2ad5780fee4155f90ac829b2204994c4faa22d5fea73','predecessor contract changed'
source=read('DARING_PROVOCATION_SOURCE_MANIFEST.json')['files']|frozen
base=read('source_references/daring_provocation_guard_contract.json')['approved_files']
assert len(source)==660 and digest(source)=='515010bd965ac86ccb261e2288ba90935451dc2ef5d262c2d50f48d453389d05','accepted source identity mismatch'
assert len(base)==646 and digest(base)=='37d2ac563100386fdc40be0cc4f7595dfb40cff16fed57f1a7b25a6e7f8aa043','approved predecessor identity mismatch'
assert set(base)<=set(source)<=set(files),'historical source file missing'
assert [n for n in base if source[n]!=base[n]]==['expressions/registry.json'],'accepted base delta mismatch'
overlay={'README.md','CONTROL_API.md','LOCAL_CONTROL_BRIDGE.md','PACKAGING.md','RELEASE.json','APPROVED_INTEGRATION_STATUS.json','APPROVED_SOURCE_MANIFEST.json','APPROVED_SOURCE_FILES.sha256','tools/verify_approved_integration.py'}
assert {n for n in source if files[n]!=source[n]}==overlay,'unexpected accepted-source overlay'
assert set(files)-set(source)=={'APPROVED_DARING_PROVOCATION_VALIDATION.md'},'unexpected new source path'
for n in source:
 if n not in overlay:assert files[n]==source[n],n+' differs from tested source'
m=read('APPROVED_SOURCE_MANIFEST.json')
assert m['schema_version']==2 and m['approved_profiles']==19
assert m['accepted_source_git_tree']=='bd83f0e1d7cadea349a1d0cfbd8dd50cb1ba225c' and m['accepted_source_inventory_sha256']==digest(source)
assert m['accepted_source_overlay_paths']==sorted(overlay) and m['added_paths']==['APPROVED_DARING_PROVOCATION_VALIDATION.md']
assert m['files']=={n:h for n,h in files.items() if n not in {'APPROVED_SOURCE_MANIFEST.json','APPROVED_SOURCE_FILES.sha256'}},'complete source inventory mismatch'
assert digest(m['files'])==m['inventory_sha256'],'current manifest digest mismatch'
lines=(P/'APPROVED_SOURCE_FILES.sha256').read_text().splitlines()
assert all(re.fullmatch(r'[0-9a-f]{64}  [^\r\n]+',line) for line in lines),'invalid checksum syntax'
checks={line[66:]:line[:64] for line in lines}
assert len(checks)==len(lines),'duplicate checksum entry'
assert checks=={n:h for n,h in files.items() if n!='APPROVED_SOURCE_FILES.sha256'},'checksum index mismatch'
ids=['EXP-163','EXP-005','EXP-001','EXP-006','EXP-107','EXP-007','EXP-002','EXP-152','EXP-160','EXP-177','EXP-164','EXP-021','EXP-158','EXP-181','EXP-102','EXP-116','EXP-050','EXP-186','EXP-114']
registry=read('expressions/registry.json');entries=registry['entries']
assert [e['id'] for e in entries]==ids and len(set(ids))==19,'wrong current catalogue'
assert entries[:-1]==read('source_references/daring_provocation_approved18_registry.json')['entries'],'old catalogue entries changed'
assert files['expressions/registry.json']==source['expressions/registry.json'],'catalogue differs from tested source'
assert len(list((P/'expressions').glob('EXP-*.json')))==18,'extra expression profile'
assert len({e['path'] for e in entries})==19,'duplicate profile path'
for e in entries:
 assert e['path'].startswith('res://')
 n=e['path'][6:];assert files[n]==source[n],n+' differs from accepted profile'
 if e['id']!='EXP-114':assert files[n]==base[n],n+' differs from old approved profile'
assert files['expressions/EXP-114.json']=='96eed6ccf108e2e54590f953ae01b129a04af223245fecc1fc59c2af19f8c107'
pngs=[n for n in files if n.endswith('.png')];assert len(pngs)==182
for n in pngs:assert files[n]==source[n]==base[n],n+' artwork changed'
status=read('APPROVED_INTEGRATION_STATUS.json');release=read('RELEASE.json')
assert status['approved_profile_ids']==ids and status['newly_approved_profile_ids']==['EXP-114'] and status['approved_profile_count']==19
assert status['accepted_source_inventory_sha256']==digest(source) and status['accepted_source_git_tree']==m['accepted_source_git_tree']
assert status['base_commit']=='3e7f43ca9684bcafc9329ff5c14aa9ffcb57915b' and status['approved_parent_git_tree']=='28d7b124d9d46a3b87cd3e821669ae87b3d47719'
assert status['accepted_profile_sha256']==files['expressions/EXP-114.json']
assert release['user_approved'] is True and release['approved_registry']==ids and release['approved_published_count']==19
assert release['authored_registry']==ids and release['authored_local_count']==19 and release['approved_predecessors']==ids[:-1]
assert release['newly_approved']==['EXP-114'] and release['pending_review']==[]
assert status['smooth_realtime_pacing_status']==release['smooth_realtime_pacing_status']=='HOLD'
assert status['smooth_realtime_pacing_pass'] is False and status['continuous_normal_speed_observation'] is False
assert status['normal_speed_playback_observed'] is False and release['normal_speed_playback_observed'] is False
assert status['normal_execution_ownership_neutral_pass'] is True and status['normal_execution_checks_passed']==1946 and status['normal_cycles']==4
assert status['normal_gaps_over_50ms']==6 and [status[k] for k in ['normal_bust_max_gap_ms','normal_native_opening_gap_ms','normal_native_resealing_gap_ms']]==[119.921,512.158,407.784]
assert status['accepted_runtime_jobs']==20 and status['accepted_runtime_checks']==5380806 and status['old18_exact_paired_records']==3230
assert [status[k] for k in ['rendered_trajectory_records','actual_rendered_views','rendered_trajectory_checks']]==[701,1402,687526]
assert status['failed_headless_job21_status']=='NOT_PASS' and status['ci_run'] is False and status['new_engine_or_display_run'] is False
assert status['independent_clearance_sha256']=='ad4ee18995988007e9cde9494d6aa2500f9299b6e539e589090122b5e9363ff6'
assert {'EXP-003','EXP-097','EXP-197'}<=set(status['excluded_profile_ids'])
assert status['EXP-003_status']=='unapproved historical; not user-rejected; NOT_REPLAYED'
for n in ['README.md','CONTROL_API.md','LOCAL_CONTROL_BRIDGE.md','PACKAGING.md','APPROVED_DARING_PROVOCATION_VALIDATION.md']:
 text=(P/n).read_text();assert all(s in text for s in ['HOLD','119.921','512.158','407.784','intermittent','not continuous']),n+' missing qualification limits'
assert read('DARING_PROVOCATION_STATUS.json')['approved'] is False,'historical pending status was rewritten'
print('APPROVED_INTEGRATION_GUARD PASS files=661 profiles=19 old_profiles_exact=18 pngs_exact=182 accepted_runtime_exact=true historical_evidence_exact=true smooth_realtime_pacing=HOLD')

#!/usr/bin/env python3
"""Portable read-only recovery verification. No Git, Godot, cache import, or network."""
from pathlib import Path
import hashlib,json,subprocess,sys
P=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
m=json.loads((P/'BACKUP_MANIFEST.json').read_text());assert m['schema_version']==1 and m['expression']=='EXP-114'
files={p.relative_to(P).as_posix():p for p in P.rglob('*') if p.is_file()}
assert not any(p.is_symlink() for p in P.rglob('*'))
assert set(files)==set(m['files'])|{'BACKUP_MANIFEST.json'},'unexpected/missing files in recovery package'
for n,r in m['files'].items():
 b=files[n].read_bytes();assert len(b)==r['size'] and sha(files[n])==r['sha256'] and blob(b)==r['git_blob_sha'],n
source={n[7:]:r['sha256'] for n,r in m['files'].items() if n.startswith('source/')}
assert len(source)==660 and digest(source)==m['full_source_inventory_sha256']=='515010bd965ac86ccb261e2288ba90935451dc2ef5d262c2d50f48d453389d05'
assert source['expressions/EXP-114.json']=='96eed6ccf108e2e54590f953ae01b129a04af223245fecc1fc59c2af19f8c107'
assert not m['user_approved'] and not m['approved_integration'] and m['pending_profiles']==['EXP-114']
for excluded in ['expressions/EXP-003.json','expressions/EXP-097.json','expressions/EXP-197.json']:assert excluded not in source
v=json.loads((P/'gate_records/actual/PERFORMANCE_ACTUAL_CAPTURE_REVIEW.json').read_text())
assert sha(P/'gate_records/actual/PERFORMANCE_ACTUAL_CAPTURE_REVIEW.json')=='54fc255ceaa74a525cd1d4d2600cf2d97a2b4550123f2097f814a9c6fce57e13'
assert v['status']=='PASS_RUNTIME_AND_ACTUAL_CAPTURE_WITH_DISCLOSED_AMBER' and v['old_failed_trajectory_status']=='NOT_PASS'
r=json.loads((P/'gate_records/actual/RUN_RESULT.json').read_text());assert r['status']=='PASS' and r['engine']['returncode']==0
assert sha(P/'gate_records/actual/RUN_RESULT.json')==v['native_run_sha256']=='127dda938bdb75270aa3969b24aa2ee8c6fb23d16b4f7aed33bb71ba8f43558a'
c=json.loads((P/'gate_records/actual/completion_manifest.json').read_text());assert sha(P/'gate_records/actual/completion_manifest.json')==v['completion_manifest_sha256']=='06f450210e70e45ad6d1be7c66f5bef6df00b506990066b2f18ef04be7ec9bbc'
assert c['status']=='PASS' and c['serialization_complete'] and c['record_count']==c['expected_record_count']==len(c['record_files'])==701
assert c['harness_sha256']==sha(P/'capture_support/proposals/serialization_successor/trajectory_record_files.gd')
assert c['plan_sha256']==sha(P/'capture_support/capture_plan.json') and c['profile_sha256']==source['expressions/EXP-114.json']
final=json.loads((P/'gate_records/final/PERFORMANCE_FINAL_SOURCE_CLEARANCE.json').read_text())
assert sha(P/'gate_records/final/PERFORMANCE_FINAL_SOURCE_CLEARANCE.json')=='ad4ee18995988007e9cde9494d6aa2500f9299b6e539e589090122b5e9363ff6'
assert final['scoped_unapproved_source_backup_clearance'] and final['normal_execution_pass'] and not final['smooth_realtime_performance_clearance']
assert final['normal_execution_checks']==1946 and final['normal_cycles']==4 and not final['continuous_normal_speed_visual_observation']
assert sha(P/'gate_records/normal/RUN_RESULT.json')==final['normal_run_result_sha256']
assert sha(P/'gate_records/final/PERFORMANCE_ACTUAL_IDENTITY_BINDING.json')==final['actual_identity_binding_sha256']
assert m['normal_stage_status']=='EXECUTION_OWNERSHIP_NEUTRAL_PASS_SMOOTH_PACING_HOLD'
result=subprocess.run([sys.executable,'-B',str(P/'recovery/check_source_recovery.py'),str(P/'source')],capture_output=True,text=True)
assert result.returncode==0,(result.stdout,result.stderr);recovery=json.loads(result.stdout)
print(json.dumps({'status':'PASS_PORTABLE_SOURCE_RECOVERY_AND_PRESERVED_GATE_RECORD_IDENTITIES','source_files':660,'reconstructed_approved_predecessor_files':646,'package_files':len(files),'full_source_inventory_sha256':digest(source),'source_guard':recovery['candidate_guard'],'actual_capture_review':v['status'],'normal_stage_status':m['normal_stage_status'],'user_approved':False,'approved_integration':False,'historical_omitted_render_evidence_reverified':False,'engine_started':False,'git_written':False},indent=2))

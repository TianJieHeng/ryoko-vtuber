"""Additive read-only continuation identity, preserving every frozen original input and failed attempt."""
import json,sys
from pathlib import Path
from verify_inputs import W,R,sha,verify as original_verify
ORIGINAL='f87c137ecdbfdeb425f060f4944858086689a41f203456d8038582253e77deed'
CORRECTED='9a05e9a9f193a1bc5f1119f4b6c948f1b5da5c6c62a911b2bf6368a628272cea'
def verify():
 identity=original_verify();assert sha(W/'evidence/PREPARED_PACKAGE.json')==ORIGINAL
 proposal=W/'proposals/headless_fixture_correction/PROPOSED_BINDING.json';assert sha(proposal)=='de7a384df82e809abfeb0bbed2993fb0b5370cabd7497a169258615f73026df9'
 p=json.loads(proposal.read_text())
 for path,h in p['files'].items():assert sha(W/path)==h
 diagnosis=json.loads((W/'evidence/HEADLESS_01_FAILURE_DIAGNOSIS.json').read_text());assert sha(W/'evidence/HEADLESS_01_FAILURE_DIAGNOSIS.json')=='09447d863367459b68c0e3d3b087eb7727bf0681e21ff5b20651708ca6acabe3'
 for path,h in diagnosis['attempt_files'].items():assert sha(W/path)==h,('preserved failed attempt changed',path)
 r=R/'daring_provocation_independent_review/PERFORMANCE_PATH_CORRECTION_PROPOSAL_REVIEW.json';assert sha(r)=='df1d3b310a3c9e1a0d718e742e3a562a54de12086c316a3b50fccb92d94afbb0'
 scope=json.loads(r.read_text());assert scope['passed_jobs_1_through_7_independently_accepted'] and scope['passed_checks']==2085236 and scope['correction_exactly_one_path_expression']
 review=json.loads((R/'daring_provocation_independent_review/PERFORMANCE_HEADLESS_01_REVIEW.json').read_text());rows=json.loads((W/'headless_01/RUN_ROWS.json').read_text())
 assert len(rows)==8 and rows[7]['name']=='candidate_test_sealed_width_contract' and rows[7]['returncode']==-15
 assert len(review['passed_jobs'])==7 and review['passed_check_total']==2085236
 for n,(row,accepted) in enumerate(zip(rows[:7],review['passed_jobs'],strict=True),1):
  assert accepted['job_number']==n and accepted['name']==row['name'] and row['returncode']==accepted['returncode']==0 and accepted['status']=='PASS'
  assert sha(W/'headless_01'/(row['name']+'.log'))==row['log_sha256']==accepted['log_sha256']
  if accepted['json_receipt_sha256']:assert sha(W/'headless_01'/(row['name']+'.json'))==accepted['json_receipt_sha256']
 fixture=W/'harness/test_sealed_width_contract_candidate19_corrected.gd';assert sha(fixture)==CORRECTED
 frozen=(W/'harness/test_sealed_width_contract_candidate19.gd').read_text();assert fixture.read_text()==frozen.replace('get_script().resource_path.get_base_dir()+"/sealed_observed_rig.gd"','"res://tests/sealed_observed_rig.gd"',1)
 assert (W/'verify_records_headless02.py').read_text()==(W/'verify_records.py').read_text().replace("W/'headless_01/trajectory/evidence.json'","W/'headless_02/trajectory/evidence.json'",1)
 jobs=json.loads((W/'plan/HEADLESS_02_JOBS.json').read_text());expected=json.loads((W/'plan/HEADLESS_JOBS.json').read_text())['jobs'][7:];expected[0]['script']=str(fixture)
 assert jobs['jobs']==expected and jobs['original_job_numbers']==list(range(8,22)) and len(expected)==14
 binding=W/'evidence/HEADLESS_02_INPUT_BINDING.json'
 if binding.exists():
  frozen=json.loads(binding.read_text());assert frozen['original_package_sha256']==ORIGINAL
  for path,h in frozen['files'].items():assert sha(W/path)==h,('successor input changed',path)
  for path,h in frozen['external_review_files'].items():assert sha(R/path)==h,('independent review changed',path)
 return identity|{'continuation_stage':'headless_02','continuation_input_binding_sha256':sha(binding) if binding.exists() else None,'continuation_original_jobs':list(range(8,22)),'accepted_prior_jobs':7,'accepted_prior_checks':2085236,'failed_attempt_preserved':True,'corrected_fixture_sha256':CORRECTED,'future_native_successful_trajectory':'headless_02/trajectory/evidence.json','future_native_verifier_sha256':sha(W/'verify_records_headless02.py')}
def require_review_and_lease():
 binding=sha(W/'evidence/HEADLESS_02_INPUT_BINDING.json')
 rp=W/'evidence/HEADLESS_02_REVIEW_APPROVAL.json';lp=W/'evidence/HEADLESS_02_LEASE.json';review=json.loads(rp.read_text());lease=json.loads(lp.read_text())
 assert review['approved'] is True and review['stage']=='headless_02' and review['binding_sha256']==binding
 assert sha(Path(review['review_path']))==review['review_sha256']
 assert lease['stage']=='headless_02' and lease['binding_sha256']==binding and lease['exclusive_godot_lease'] is True and lease['display_lease'] is False and lease['original_job_numbers']==list(range(8,22))
 return review,lease
if __name__=='__main__':print(json.dumps(verify()))

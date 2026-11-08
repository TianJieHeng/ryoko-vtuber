"""Read-only additive native-stream input guard, retaining failed attempts and all accepted test evidence."""
from pathlib import Path
import hashlib,json,sys
P=Path(__file__).resolve().parent;W=P.parents[1];R=W.parent;sys.path.insert(0,str(W))
from verify_headless02_inputs import verify as predecessor_verify
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
BINDING=P/'NATIVE_STREAM_INPUT_BINDING.json'
def verify():
 identity=predecessor_verify()
 diagnosis=W/'evidence/HEADLESS_02_FAILURE_DIAGNOSIS.json';assert sha(diagnosis)=='72c0ff8fb7055dbbe05941a8dd3ab7afc5636a130b849c2d4705c4c3d93be5ac'
 for path,h in json.loads(diagnosis.read_text())['attempt_files'].items():assert sha(W/path)==h,('preserved failed attempt02 changed',path)
 review=R/'daring_provocation_independent_review/PERFORMANCE_HEADLESS_02_FAILURE_REVIEW.json';assert sha(review)=='c68b1c19be4dbfa8a4136153da7ba5fc2d93abdfa950f3bd214968f2faf915e4'
 accepted=json.loads(review.read_text());rows=json.loads((W/'headless_02/RUN_ROWS.json').read_text());assert len(rows)==14 and all(r['returncode']==0 for r in rows[:13]) and rows[13]['returncode']==-9
 assert (W/'headless_02/trajectory/evidence.json').stat().st_size==0,'failed trajectory must remain unrelabeled'
 a=json.loads((W/'headless_02/prior18_approved.json').read_text());b=json.loads((W/'headless_02/prior18_candidate.json').read_text());assert a==b and not a['failures'] and a['samples']==3230
 if BINDING.exists():
  binding=json.loads(BINDING.read_text());assert binding['original_package_sha256']==sha(W/'evidence/PREPARED_PACKAGE.json')
  for path,h in binding['files'].items():assert sha(W/path)==h,('native-stream input changed',path)
  for path,h in binding['external_review_files'].items():assert sha(R/path)==h
 identity=dict(identity);identity.pop('future_native_successful_trajectory');identity.pop('future_native_verifier_sha256')
 return identity|{'superseded_headless02_future_reference':'NOT_PASS; never used as successful native reference','native_stream_binding_sha256':sha(BINDING) if BINDING.exists() else None,'accepted_completed_jobs':20,'accepted_completed_checks':5380806,'old18_exact_parity_samples':3230,'failed_job21_not_pass':True,'no_headless_native_cross_run_claim':True,'successor_harness_sha256':sha(P/'trajectory_record_files.gd'),'checkpoints':701,'actual_images_required':1402}
def require_review_and_lease():
 binding=sha(BINDING);rp=W/'evidence/NATIVE_STREAM_REVIEW_APPROVAL.json';lp=W/'evidence/NATIVE_STREAM_LEASE.json';review=json.loads(rp.read_text());lease=json.loads(lp.read_text())
 assert review['approved'] is True and review['stage']=='native_stream_01' and review['binding_sha256']==binding and sha(Path(review['review_path']))==review['review_sha256']
 assert lease['stage']=='native_stream_01' and lease['binding_sha256']==binding and lease['exclusive_godot_lease'] is True and lease['display_lease'] is True and lease['scope']=='one_combined_native_trajectory_and_pixel_gate'
 return review,lease
if __name__=='__main__':print(json.dumps(verify()))

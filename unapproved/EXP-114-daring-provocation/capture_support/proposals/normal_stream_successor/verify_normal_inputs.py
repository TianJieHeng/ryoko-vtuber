"""Read-only normal-stage successor identity. No engine and no old headless PASS claim."""
from pathlib import Path
import hashlib,json,sys
P=Path(__file__).resolve().parent;W=P.parents[1];sys.path.insert(0,str(W/'proposals/serialization_successor'))
from verify_native_stream_inputs import verify as native_inputs_verify
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
BINDING=P/'NORMAL_STREAM_INPUT_BINDING.json'
def verify():
 identity=native_inputs_verify();binding=json.loads(BINDING.read_text())
 assert binding['stage']=='normal' and binding['native_stream_binding_sha256']==identity['native_stream_binding_sha256']
 for path,h in binding['files'].items():assert sha(W/path)==h,('normal successor input changed',path)
 out=W/'native_stream_01'
 assert {p.relative_to(out).as_posix():sha(p) for p in sorted(out.rglob('*')) if p.is_file()}==binding['successful_native_capture_files']
 assert not any(p.is_symlink() for p in out.rglob('*'))
 run=json.loads((out/'RUN_RESULT.json').read_text());proof=json.loads((W/'evidence/NATIVE_STREAM_VERIFICATION.json').read_text());manifest=json.loads((out/'evidence.json').read_text())
 assert run['status']=='PASS' and run['returncode']==0 and run['engine']['returncode']==0 and run['lease_released'] and not run['remaining_godot_processes']
 assert run['verification_sha256']==sha(W/'evidence/NATIVE_STREAM_VERIFICATION.json')
 assert proof['status']=='PASS' and proof['render_invariance_captures_verified']==1402 and proof['headless_native_cross_run_comparison_performed'] is False
 assert manifest['status']=='PASS' and manifest['serialization_complete'] is True and manifest['record_count']==manifest['expected_record_count']==701 and not manifest['failures']
 return identity|{'normal_stream_binding_sha256':sha(BINDING),'successful_native_verification_sha256':sha(W/'evidence/NATIVE_STREAM_VERIFICATION.json'),'successful_native_run_sha256':sha(out/'RUN_RESULT.json'),'normal_harness_unchanged':True,'normal_visual_observation_claim':False}
if __name__=='__main__':print(json.dumps(verify()))

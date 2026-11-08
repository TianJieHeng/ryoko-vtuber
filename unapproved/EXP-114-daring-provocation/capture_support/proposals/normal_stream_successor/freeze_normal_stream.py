"""Offline final freeze only after a successful complete native stream. Does not authorize normal execution."""
from pathlib import Path
import hashlib,json,ast
P=Path(__file__).resolve().parent;W=P.parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
out=W/'native_stream_01';run=json.loads((out/'RUN_RESULT.json').read_text());proof=json.loads((W/'evidence/NATIVE_STREAM_VERIFICATION.json').read_text())
assert run['status']=='PASS' and run['returncode']==0 and run['engine']['returncode']==0 and run['lease_released']
assert proof['status']=='PASS' and proof['render_invariance_captures_verified']==1402
for p in P.glob('*.py'):ast.parse(p.read_text())
paths=[*P.glob('*.py'),*P.glob('*.sh'),P/'REPORT.md',P/'ROUTING_ONLY.patch',W/'evidence/NATIVE_STREAM_VERIFICATION.json',W/'source/ryoko_object_rig/tools/review_daring_provocation_normal_playback.gd',W/'runtime/candidate/tools/review_daring_provocation_normal_playback.gd']
assert not (P/'NORMAL_STREAM_INPUT_BINDING.json').exists()
binding={'stage':'normal','native_stream_binding_sha256':sha(W/'proposals/serialization_successor/NATIVE_STREAM_INPUT_BINDING.json'),'files':{p.relative_to(W).as_posix():sha(p) for p in sorted(paths)},'successful_native_capture_files':{p.relative_to(out).as_posix():sha(p) for p in sorted(out.rglob('*')) if p.is_file()},'scope':'one unchanged real-time native harness; two bust and two native cycles; separate supported CUA launch','no_old_headless_success_claim':True,'normal_speed_visual_observation_not_assumed':True}
(P/'NORMAL_STREAM_INPUT_BINDING.json').write_text(json.dumps(binding,indent=2)+'\n')
from verify_normal_inputs import verify
print(json.dumps(verify(),indent=2))

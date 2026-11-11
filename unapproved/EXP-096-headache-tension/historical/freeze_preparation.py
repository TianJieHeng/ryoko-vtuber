"""Create an explicit author-input handoff freeze, excluding later reviewer output."""
import hashlib,json
from pathlib import Path
W=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
files=['BASELINE_FREEZE.json','EXP-096.json','plan.json','SOURCE_CATALOGUE_ENTRY.json','SOURCE_REFERENCE.json','PREPARATION_STATUS.json','README.md','prepare_candidate.py','prepare_native_launcher.py','check_and_capture.gd','render_motion.gd','run_motion.sh','verify_preparation.py','independent_geometry.py','review_validation.py','encode_preview.py','test_encode_preview.py','test_independent_geometry.py','test_review_validation.py','verify_input_freeze.py','freeze_preparation.py','state_checks.json','motion_state_checks.json','independent_geometry_checks.json','preparation_verification.json','launcher_preparation_verification.json','DISTINCTNESS_CHECK.json','import.log','launcher_import.log','launcher_static_parse.log','launcher_motion_parse.log','launcher_launcher_parse.log','encoder_preflight.log','native_launcher/project.godot','native_launcher/launcher.gd','native_launcher/launcher.tscn','native_launcher/static.gd','native_launcher/motion.gd']
f=dict(candidate='EXP-096',status='UNAPPROVED author preparation; independent source and native reviews pending',files={n:sha(W/n) for n in files},exclusions='Independent reviewer artifacts, later capture/MP4 evidence, test logs and generated review reports are not author-input freeze members.')
(W/'review_input_freeze.json').write_text(json.dumps(f,indent=2)+'\n')
(W/'REVIEW_FREEZE.sha256').write_text(sha(W/'review_input_freeze.json')+'  review_input_freeze.json\n')
print(len(files),'author preparation files frozen;',sha(W/'review_input_freeze.json'))

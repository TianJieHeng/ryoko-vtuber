"""Verify the static-only v2 alternatives and unchanged approved27 baseline."""
import ast
import hashlib
import json
from pathlib import Path

w = Path(__file__).resolve().parent
rig = w / 'rig'
freeze = json.loads((w / 'BASELINE_FREEZE.json').read_text())
known = freeze['source_files_sha256']
current = {str(p.relative_to(rig)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(rig.rglob('*')) if p.is_file() and '.godot' not in p.parts and '__pycache__' not in p.parts}
plan = json.loads((w / 'plan.json').read_text())
state = json.loads((w / 'state_checks.json').read_text())
ids = [r['id'] for r in json.loads((rig / 'expressions/registry.json').read_text())['entries']]
v1plan = json.loads((w.parent / 'focused_determination_work/plan.json').read_text())
v1peak = next(r['pose'] for r in v1plan if r['name'] == 'focused_determination')
allowed = {'brow_screen_left', 'brow_screen_right', 'brow_tilt_screen_left', 'brow_tilt_screen_right', 'mouth_lip_press', 'mouth_width_screen_left', 'mouth_width_screen_right'}
for p in w.glob('*.py'):
    ast.parse(p.read_text(), filename=str(p))
alternatives = plan[2:5]
checks = {
    'frozen_baseline_exact_no_extra_files': current == known,
    'actual_approved27_registry_unchanged': ids == freeze['baseline_profile_ids'] and len(ids) == len(set(ids)) == 27,
    'new_candidate_never_written_in_rig': 'EXP-139' not in ids and not list(rig.rglob('*139*.json')),
    'static_only_no_final_profile_or_motion': not (w / 'EXP-139.json').exists() and not (w / 'render_motion.gd').exists() and not (w / 'motion').exists(),
    'six_studies_three_stronger_alternatives': len(plan) == 6 and len(alternatives) == 3 and len({r['name'] for r in plan}) == 6,
    'v1_comparison_pose_exact': plan[1]['pose'] == v1peak,
    'neutral_bookends': plan[0]['pose'] == plan[-1]['pose'] == {},
    'only_existing_selected_controls': all(set(r['pose']) <= allowed for r in plan),
    'materially_stronger_brow_lowering': all(-1 <= r['pose']['brow_screen_left'] <= -.65 and r['pose']['brow_screen_left'] == r['pose']['brow_screen_right'] for r in alternatives),
    'stronger_opposing_brow_tilts_in_bounds': all(.8 <= r['pose']['brow_tilt_screen_left'] <= 1 and r['pose']['brow_tilt_screen_left'] == -r['pose']['brow_tilt_screen_right'] for r in alternatives),
    'eyes_open_and_no_smile_pout_or_opening': all(not any(k in r['pose'] for k in ['blink_L', 'blink_R', 'eye_smile_L', 'eye_smile_R', 'mouth_smile', 'mouth_corner_lift', 'mouth_purse', 'mouth_open']) for r in plan),
    'bounded_symmetric_sealed_width_study': [r['pose']['mouth_width_screen_left'] for r in alternatives] == [0, .12, .25] and all(r['pose']['mouth_width_screen_left'] == r['pose']['mouth_width_screen_right'] for r in alternatives),
    'headless_static_geometry_scope_reset_pass': state['status'] == 'PASS' and not state['failures'] and state['baseline_profile_count'] == 27 and not state['visual_capture'] and len(state['records']) == 6,
    'reference_sheet_unchanged': hashlib.sha256(Path(freeze['source_sheet']).read_bytes()).hexdigest() == freeze['source_sheet_sha256'],
    'python_syntax': True,
}
result = {'status': 'PASS' if all(checks.values()) else 'FAIL', 'checks': checks, 'source_files': len(known), 'source_png_files': sum(n.endswith('.png') for n in known), 'missing': sorted(set(known)-set(current)), 'extra': sorted(set(current)-set(known)), 'changed': [n for n in known if n in current and known[n] != current[n]], 'scope': 'Static alternatives only. No native visual fit, selected pose, final motion, approval or production integration implied.'}
(w / 'preparation_verification.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
raise SystemExit(0 if result['status'] == 'PASS' else 1)

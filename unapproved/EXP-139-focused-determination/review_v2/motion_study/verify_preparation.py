"""Verify selected-C blink motion without changing original static evidence."""
import ast
import hashlib
import json
import subprocess
from pathlib import Path

w = Path(__file__).resolve().parent
root = w.parent
rig = root / 'rig'
freeze = json.loads((root / 'BASELINE_FREEZE.json').read_text())
known = freeze['source_files_sha256']
actual = {str(p.relative_to(rig)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(rig.rglob('*')) if p.is_file() and '.godot' not in p.parts and '__pycache__' not in p.parts}
original = json.loads((root / 'STATIC_ALTERNATIVES_FREEZE.json').read_text())['files']
preserved = all((root / n).is_file() and hashlib.sha256((root / n).read_bytes()).hexdigest() == sha for n, sha in original.items())
plan = json.loads((root / 'plan.json').read_text())
selected = next(r['pose'] for r in plan if r['name'] == 'c_strongest_open')
profile = json.loads((w / 'EXP-139.json').read_text())
keys = profile['keyframes']
onset = json.loads((root / 'onset_study/plan.json').read_text())
static = json.loads((root / 'onset_study/state_checks.json').read_text())
motion = json.loads((w / 'motion_state_checks.json').read_text())
ids = [r['id'] for r in json.loads((rig / 'expressions/registry.json').read_text())['entries']]
allowed = {'brow_screen_left', 'brow_screen_right', 'brow_tilt_screen_left', 'brow_tilt_screen_right', 'mouth_width_screen_left', 'mouth_width_screen_right', 'mouth_lip_press', 'blink_L', 'blink_R'}
for directory in [root, root / 'onset_study', w]:
    for p in directory.glob('*.py'):
        ast.parse(p.read_text(), filename=str(p))
subprocess.run(['sh', '-n', str(w / 'run_motion.sh')], check=True)
checks = {
    'frozen_rig_and_artwork_exact': actual == known,
    'all_original_static_files_and_captures_preserved': preserved,
    'production_registry_unchanged_27_and_no_exp139': ids == freeze['baseline_profile_ids'] and len(ids) == 27 and 'EXP-139' not in ids and not list(rig.rglob('*139*.json')),
    'four_second_unapproved_candidate': profile['duration'] == 4.0 and profile['status'].startswith('UNAPPROVED'),
    'eleven_ordered_keys_with_neutral_bookends': len(keys) == 11 and keys[0]['time'] == 0 and keys[-1]['time'] == 4 and keys[0]['values'] == keys[-1]['values'] == {} and all(a['time'] < b['time'] for a, b in zip(keys, keys[1:])),
    'only_existing_selected_channels': all(set(k['values']) <= allowed for k in keys),
    'exact_selected_c_peak_and_1620ms_hold': [k['time'] for k in keys if k['phase'] == 'selected_focus'] == [.78, 2.40] and all(k['values'] == selected for k in keys if k['phase'] == 'selected_focus'),
    'one_symmetric_authored_onset_blink': all(k['values'].get('blink_L', 0) == k['values'].get('blink_R', 0) for k in keys) and [(k['time'], k['values'].get('blink_L', 0)) for k in keys if k['values'].get('blink_L', 0) > 0] == [(.48, 1.0), (.54, 1.0)],
    'eyes_open_by_070_and_through_hold_release': all(k['values'].get('blink_L', 0) == k['values'].get('blink_R', 0) == 0 for k in keys if k['time'] >= .70) and all(r['pose']['blink_L'] == r['pose']['blink_R'] == 0 for r in motion['records'] if r['time'] >= .70),
    'authored_blink_disclosed_not_recovered': 'not recovered source animation' in profile['timing_origin'] and 'deliberate refocusing blink is new timing' in profile['timing_origin'],
    'onset_static_exact_c_reference': len(onset) == 6 and next(r['pose'] for r in onset if r['name'] == 'selected_focus') == selected,
    'onset_static_headless_pass': static['status'] == 'PASS' and not static['failures'] and static['baseline_profile_count'] == 27 and not static['visual_capture'],
    'motion_headless_dense_and_chronological_pass': motion['status'] == 'PASS' and not motion['failures'] and motion['baseline_profile_count'] == 27 and not motion['visual_capture'] and len(motion['records']) == 121,
    'exact_chronological_neutral_endpoints': motion['records'][0]['pose'] == motion['records'][-1]['pose'] and all(v == 0 for v in motion['records'][-1]['pose'].values()),
    'source_sheet_unchanged': hashlib.sha256(Path(freeze['source_sheet']).read_bytes()).hexdigest() == freeze['source_sheet_sha256'],
    'python_and_shell_syntax': True,
}
result = {'status': 'PASS' if all(checks.values()) else 'FAIL', 'checks': checks, 'baseline': freeze['baseline'], 'source_files': len(known), 'source_png_files': sum(n.endswith('.png') for n in known), 'original_static_files_preserved': len(original), 'static_checks': static['checks'], 'motion_checks': motion['checks'], 'dense_timeline_samples': 4001, 'chronological_frames': 121, 'approval': 'UNAPPROVED', 'scope': 'Preparation integrity and state evidence. Native blink fit, native motion, video playback, normal-speed perception and user approval remain separate gates.'}
(w / 'preparation_verification.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
raise SystemExit(0 if result['status'] == 'PASS' else 1)

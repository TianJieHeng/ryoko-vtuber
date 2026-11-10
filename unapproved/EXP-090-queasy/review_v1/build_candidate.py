"""Build only the unapproved EXP-090 data file from the six-pose study.

The approved25 rig and its on-disk catalogue are never written. Harnesses are
standalone checked-in files adapted from the preceding EXP-063 preparation.
"""
import json
from pathlib import Path

w = Path(__file__).resolve().parent
poses = {row['name']: row['pose'] for row in json.loads((w / 'plan.json').read_text())}
freeze = json.loads((w / 'BASELINE_FREEZE.json').read_text())
keys = [
    (0.0, 'neutral'), (0.25, 'neutral'), (0.55, 'onset'),
    (0.95, 'build'), (1.30, 'queasy'), (2.00, 'queasy'),
    (2.65, 'soften'), (3.75, 'neutral_return'), (4.0, 'neutral_return'),
]
definition = {
    'id': 'EXP-090', 'title': 'Queasy', 'duration': 4.0,
    'status': 'UNAPPROVED review candidate only; preparation against approved25',
    'intent': 'Inner brows rise, heavy lids narrow, lips press forward, then gradually release to exact neutral. Cheek tension is source intent only, not implemented deformation.',
    'scope': 'Existing approved25 ordinary lids, rigid outer-anchor inner-brow controls and sealed mouth purse/pressure only. Painted brow curvature and forward lip contour are approximations. No cheek deformation exists in this preparation. No new artwork, anatomy, runtime changes, gaze, blush, smile, auto-blink or head/body acting.',
    'timing_origin': 'New 4.0-second interpretation of nine static source panels. The catalogue 1.9-second schedule is proposed reference timing, not recovered animation. A 0.7-second queasy hold is followed by gradual recovery.',
    'interpolation': 'Existing shared cubic smoothstep, displayed-pose restart and release. Exact neutral bookends; no player or rendering changes.',
    'source_catalogue_sha256': freeze['catalogue_sha256'],
    'keyframes': [{'time': time, 'phase': phase, 'values': poses[phase]} for time, phase in keys],
}
assert len(poses) == 6
assert definition['keyframes'][0]['values'] == definition['keyframes'][-1]['values'] == {}
(w / 'EXP-090.json').write_text(json.dumps(definition, indent=2) + '\n')
print('Built unapproved EXP-090: 4.0 s, 9 keys, 6 static poses; rig not modified.')

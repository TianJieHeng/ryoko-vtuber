"""Build the unapproved EXP-153 data file, never the production catalogue."""
import json
from pathlib import Path

w = Path(__file__).resolve().parent
poses = {row['name']: row['pose'] for row in json.loads((w / 'plan.json').read_text())}
freeze = json.loads((w / 'BASELINE_FREEZE.json').read_text())
keys = [
    (0.0, 'neutral'), (0.20, 'neutral'), (0.55, 'onset'),
    (0.95, 'build'), (1.40, 'hiding_smile'), (2.05, 'hiding_smile'),
    (2.70, 'soften'), (3.75, 'neutral_return'), (4.0, 'neutral_return'),
]
definition = {
    'id': 'EXP-153', 'title': 'Hiding a smile', 'duration': 4.0,
    'status': 'UNAPPROVED review candidate only; preparation against ' + freeze['baseline'],
    'intent': 'Brows soften slightly; eyes narrow while remaining open; lips press tightly while their corners continue lifting, then release to exact neutral. Source eye crinkle is only partly represented.',
    'scope': 'Existing ordinary lids, small rigid outer-anchor inner-brow lifts and vertical brow offsets, sealed bilateral corner lift and lip pressure only. Partial source fidelity: open-eye lower-lid crinkle and painted brow/lip contours cannot be reproduced by these controls. Closed crescent smile-eye owners are not substituted for the source open eyes. No new artwork, anatomy, runtime, gaze, blush, mouth opening, automatic blink, or head/body acting.',
    'timing_origin': 'New 4.0-second interpretation of nine static EXP-153 source panels. The catalogue 1.9-second schedule is proposed reference timing, not recovered animation. Lip pressure leads the last corner lift, followed by a 0.65-second held peak and gradual release.',
    'interpolation': 'Unchanged shared cubic smoothstep, displayed-pose restart and release. Six static study poses and nine timeline keys; exact neutral bookends. No player or rendering changes.',
    'source_catalogue_sha256': freeze['catalogue_sha256'],
    'keyframes': [{'time': time, 'phase': phase, 'values': poses[phase]} for time, phase in keys],
}
assert len(poses) == 6
assert definition['keyframes'][0]['values'] == definition['keyframes'][-1]['values'] == {}
(w / 'EXP-153.json').write_text(json.dumps(definition, indent=2) + '\n')
print('Built unapproved EXP-153: 4.0 s, 9 keys, 6 static poses; rig not modified.')

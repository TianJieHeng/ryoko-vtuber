"""Build an isolated, unapproved EXP-067 definition without editing the rig."""
import json
from pathlib import Path

w = Path(__file__).resolve().parent
poses = {row['name']: row['pose'] for row in json.loads((w / 'plan.json').read_text())}
freeze = json.loads((w / 'BASELINE_FREEZE.json').read_text())
keys = [(0.0, 'neutral'), (0.25, 'neutral'), (0.8, 'pressed'),
        (1.35, 'onset'), (1.9, 'build'), (2.5, 'creeping_dread'),
        (3.0, 'creeping_dread'), (3.7, 'soften'),
        (4.55, 'neutral_return'), (4.8, 'neutral_return')]
definition = {
    'id': 'EXP-067', 'title': 'Creeping dread', 'duration': 4.8,
    'status': 'UNAPPROVED review candidate only; preparation against ' + freeze['baseline'],
    'intent': 'The inner brows slowly lift while the mouth first forms a pressed line; the eyes progressively widen and the lips gradually separate. A short worried hold releases slowly to exact neutral.',
    'scope': 'Existing outer-anchor rigid inner-brow lift, bounded upper eye opening, mouth opening, lip pressure and modest purse only. Partial source fidelity: the rigid brows cannot reproduce painted curvature; lip pressure reveals existing inferred inner-upper-lip tissue rather than compressing the outer contour. Eye opening is limited to four source pixels and cannot coexist with closure, smile lids, gaze or aversion. Tense lid contour and pupil-size change in the source are not implemented. No new artwork, anatomy, runtime, teeth control, blush, automatic blink, gaze or head/body acting.',
    'timing_origin': 'New 4.8-second interpretation of nine static EXP-067 source panels. The catalogue 1.9-second schedule is proposed reference timing, not recovered animation; no numeric control weights are supplied. The mouth remains sealed through the 0.8-second pressure key, then opens gradually as pressure recedes. Inner-brow lift and eye widening develop through 2.5 seconds, followed by a 0.5-second held peak and slow recovery.',
    'interpolation': 'Unchanged shared cubic smoothstep, displayed-pose restart and release. Seven static poses and ten timeline keys, with exact neutral bookends. No player or rendering changes.',
    'source_catalogue_sha256': freeze['catalogue_sha256'],
    'keyframes': [{'time': t, 'phase': phase, 'values': poses[phase]} for t, phase in keys],
}
assert len(poses) == 7
assert definition['keyframes'][0]['values'] == definition['keyframes'][-1]['values'] == {}
(w / 'EXP-067.json').write_text(json.dumps(definition, indent=2) + '\n')
print('Built unapproved EXP-067: 4.8 s, 10 keys, 7 static poses; rig unchanged.')

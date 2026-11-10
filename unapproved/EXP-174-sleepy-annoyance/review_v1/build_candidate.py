"""Build the unapproved EXP-174 profile outside the production rig."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent
poses = {row['name']: row['pose'] for row in json.loads((W / 'plan.json').read_text())}
freeze = json.loads((W / 'BASELINE_FREEZE.json').read_text())
keys = [(0.0, 'neutral'), (0.20, 'neutral'), (0.52, 'drowsy_onset'),
        (0.82, 'annoyed_build'), (1.12, 'sleepy_annoyance'), (2.20, 'sleepy_annoyance'),
        (2.95, 'soften'), (3.70, 'neutral_return'), (4.0, 'neutral_return')]
definition = {
    'id': 'EXP-174', 'title': 'Sleepy annoyance', 'duration': 4.0,
    'status': 'UNAPPROVED review v1; data-only candidate against ' + freeze['baseline'],
    'intent': 'Heavy lids arrive first, then brows lower sharply into a held sleepy annoyance with narrow open eyes and a sealed compact pout. All controls release to exact neutral.',
    'scope': 'Existing ordinary lid closure, symmetric vertical brow lowering, opposing rigid brow tilt, and sealed mouth purse only. Peak uses ten source pixels of brow lowering, opposing eight-degree tilts, 14.4 source pixels of upper-lash travel and 10.5 source pixels of inward mouth travel on each side. Partial source fidelity: no lower-lip projection, independent lower-lip push, depth, or new lip shape is supported. Purse narrows and articulates the existing whole closed contour; it does not project the lower lip. No inward horizontal brow convergence or local knit. No new artwork, anatomy, shader, control, runtime, automatic blink, gaze, lip pressure, smile, opening, width, blush, hair, or head/body acting.',
    'timing_origin': 'New four-second interpretation of the nine static EXP-174 panels, not recovered animation. The catalogue timing is explicitly proposed, with no numeric rig weights. Neutral holds through 0.20 seconds. Heavy lids arrive at 0.52, sharp brow lowering develops at 0.82, peak arrives at 1.12 and holds through 2.20, then releases through a 2.95-second softened pose to exact neutral at 3.70 through 4.0. No automatic or full blink is added.',
    'interpolation': 'Unchanged shared cubic smoothstep, displayed-pose restart and release. Six static anchors and nine timeline keys. Exact neutral bookends; candidate loads only into memory.',
    'source_catalogue_sha256': freeze['catalogue_sha256'],
    'keyframes': [{'time': t, 'phase': p, 'values': poses[p]} for t, p in keys],
}
assert len(poses) == 6
assert definition['keyframes'][0]['values'] == definition['keyframes'][-1]['values'] == {}
(W / 'EXP-174.json').write_text(json.dumps(definition, indent=2) + '\n')
print('Built UNAPPROVED EXP-174: 4.0 seconds, nine keys, six static anchors; production rig unchanged.')

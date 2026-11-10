"""Build selected-C motion and isolated blink-study poses; never edit the rig."""
import json
from pathlib import Path

w = Path(__file__).resolve().parent
root = w.parent
plan = json.loads((root / 'plan.json').read_text())
selected = next(r['pose'] for r in plan if r['name'] == 'c_strongest_open')
freeze = json.loads((root / 'BASELINE_FREEZE.json').read_text())

def pose(drop, tilt, width, press, blink=0):
    return {'brow_screen_left': drop, 'brow_screen_right': drop,
            'brow_tilt_screen_left': tilt, 'brow_tilt_screen_right': -tilt,
            'mouth_width_screen_left': width, 'mouth_width_screen_right': width,
            'mouth_lip_press': press, 'blink_L': blink, 'blink_R': blink}

poses = {
    'neutral': {},
    'gather': pose(-.20, .25, .05, .20),
    'blink_closed': pose(-.75, .85, .20, .85, 1.0),
    'reopened': pose(-.95, 1.0, .25, 1.0),
    'selected_focus': selected,
    'soften': pose(-.35, .40, .08, .35),
    'neutral_return': {},
}
keys = [(0.0, 'neutral'), (.24, 'neutral'), (.36, 'gather'),
        (.48, 'blink_closed'), (.54, 'blink_closed'), (.70, 'reopened'),
        (.78, 'selected_focus'), (2.40, 'selected_focus'),
        (3.00, 'soften'), (3.65, 'neutral_return'), (4.0, 'neutral_return')]
definition = {
    'id': 'EXP-139', 'title': 'Focused determination', 'duration': 4.0,
    'status': 'UNAPPROVED review v2; selected static C, new refocusing-blink interpretation; ' + freeze['baseline'],
    'intent': 'A short refocusing blink marks a clear arrival into firm lowered brows and a sealed purposeful mouth line. Both eyes reopen fully before the selected focus pose and stay fully open throughout its hold and recovery.',
    'scope': 'Existing symmetric brow lowering and opposing rigid tilt, sealed independent width and lip pressure, plus ordinary blink controls during onset only. Exact selected C peak: ten source pixels of brow lowering, opposing eight-degree tilts, five source pixels of outward mouth travel per side, lip pressure one. No glare or squint at the peak; no smile, purse, corner lift, opening, gaze, head/body motion, new artwork, anatomy or runtime. Horizontal brow convergence and lip compression remain approximations.',
    'timing_origin': 'Newly authored four-second interpretation, not recovered source animation. The source permits normal blinking and requires open eyes at the focused peak. The deliberate refocusing blink is new timing: neutral through 0.24 s; ordinary lids close from 0.36 to 0.48, hold fully closed through 0.54, and reopen completely at 0.70. Exact selected C arrives at 0.78 and holds through 2.40; release reaches neutral at 3.65, held to 4.0.',
    'interpolation': 'Unchanged shared cubic smoothstep between eleven keys; no runtime easing change. Crisp 0.54-second gathering interval from the initial neutral hold to the selected open-eyed C peak, then a 1.62-second exact peak hold. Displayed-pose restart and release retain the shared player behavior.',
    'source_catalogue_sha256': freeze['catalogue_sha256'],
    'keyframes': [{'time': t, 'phase': phase, 'values': poses[phase]} for t, phase in keys],
}
(w / 'EXP-139.json').write_text(json.dumps(definition, indent=2) + '\n')
(w / 'poses.json').write_text(json.dumps(poses, indent=2) + '\n')
# At t=.42, smoothstep is exactly .5 between gather and closed blink.
half = {k: (poses['gather'][k] + poses['blink_closed'][k]) / 2 for k in poses['gather']}
onset_plan = [{'name': 'neutral', 'pose': {}},
              {'name': 'blink_approach', 'pose': half},
              {'name': 'blink_closed', 'pose': poses['blink_closed']},
              {'name': 'reopened', 'pose': poses['reopened']},
              {'name': 'selected_focus', 'pose': selected},
              {'name': 'neutral_return', 'pose': {}}]
(root / 'onset_study/plan.json').write_text(json.dumps(onset_plan, indent=2) + '\n')
print('Built unapproved v2: 4.0 s, 11 keys, selected C, one 0.34 s onset blink, 1.62 s open-eyed hold.')

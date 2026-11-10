"""Prepare EXP-123 outside the immutable approved36 runtime and registry."""
import hashlib
import json
import shutil
from pathlib import Path

W = Path(__file__).resolve().parent
ROOT = W.parent
source = ROOT / 'approved36_integration_work/ryoko_object_rig'
h = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
write = lambda p, d: p.write_text(json.dumps(d, indent=2) + '\n')
assert not (W / 'rig').exists(), 'Do not overwrite a prepared rig.'
files = json.loads((source / 'APPROVED_SOURCE_MANIFEST.json').read_text())['files']
assert len(files) == 999 and sum(n.endswith('.png') for n in files) == 184
for n, v in files.items():
    assert h(source / n) == v, n
    dst = W / 'rig' / n
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source / n, dst)
extra = {}
for n in ['APPROVED_SOURCE_MANIFEST.json', 'PUBLICATION_SOURCE_MANIFEST.json']:
    if n not in files:
        shutil.copy2(source / n, W / 'rig' / n)
        extra[n] = h(source / n)
ids = [r['id'] for r in json.loads((source / 'expressions/registry.json').read_text())['entries']]
assert len(ids) == 36 and 'EXP-123' not in ids
ref = ROOT / 'insight_integration_work/avatar_build_assets/reference_library'
cat = ref / 'metadata/expressions.json'
entry = next(r for r in json.loads(cat.read_text())['expressions'] if r['id'] == 'EXP-123')
sheet = ref / entry['asset_production']['actual_path']
assert h(sheet) == entry['asset_production']['sha256']
for panel in entry['key_pose_sequence']:
    assert h(ref / panel['actual_panel_path']) == panel['sha256']
freeze = dict(baseline='approved36', baseline_profile_count=36,
    published_baseline_commit='3ce98774282ad6c20dfbd7018d20838ff861b762',
    source_rig=str(source), source_files=999, source_png_files=184,
    source_files_sha256=files, extra_manifests_sha256=extra,
    baseline_profile_ids=ids, source_sheet=str(sheet), source_sheet_sha256=h(sheet),
    source_catalogue=str(cat), catalogue_sha256=h(cat))
write(W / 'BASELINE_FREEZE.json', freeze)
write(W / 'SOURCE_CATALOGUE_ENTRY.json', entry)

def pose(left, right, tl, tr, inner, lid_left, lid_right, purse, width):
    return dict(brow_screen_left=left, brow_screen_right=right,
        brow_tilt_screen_left=tl, brow_tilt_screen_right=tr,
        brow_inner_lift_screen_left=inner, blink_L=lid_right, blink_R=lid_left,
        mouth_purse=purse, mouth_width_screen_right=width)

poses = {
    'neutral': {},
    'notice': pose(-.04, -.10, 0, -.06, .10, .04, .02, 0, 0),
    'question': pose(-.10, -.24, 0, -.15, .22, .14, .06, .24, .06),
    'puzzled': pose(-.16, -.34, 0, -.24, .30, .28, .11, .58, .20),
    'reconsider': pose(-.16, -.40, 0, -.30, .26, .32, .15, .52, .16),
    'release_pout': pose(-.10, -.22, 0, -.14, .18, .14, .06, .08, 0),
    'settle': pose(-.03, -.06, 0, -.04, .05, .04, .02, 0, 0),
    'neutral_return': {},
}
write(W / 'plan.json', [dict(name=k, pose=v) for k, v in poses.items()])
keys = [(0, 'neutral'), (.2, 'neutral'), (.55, 'notice'), (.95, 'question'),
    (1.4, 'puzzled'), (1.9, 'puzzled'), (2.3, 'reconsider'),
    (2.85, 'release_pout'), (3.25, 'settle'), (3.7, 'neutral_return'), (4, 'neutral_return')]
d = dict(id='EXP-123', title='Puzzled', duration=4.0,
    status='UNAPPROVED shared-rig preparation v1; native visual review pending',
    intent=entry['distinctive_facial_intent'],
    scope='Existing outer-anchored screen-left inner-brow lift, opposing lowered screen-right brow, uneven ordinary lid closure, sealed purse and small screen-right sealed-width bias only. Width biases the outline but cannot translate the whole mouth or reproduce the painted oblique pout. No new anatomy, art, shader, runtime, gaze, smile, speech, head or body movement.',
    timing_origin='New four-second interpretation of the inspected nine-panel EXP-123 sheet, not recovered motion. A questioning inner-brow cue precedes the uneven squint and side-biased pout; a held peak gives way to a small rechecking narrowing, then the lip bias releases before the brows. Sheet head tilt is omitted. Unlike EXP-129, there is no alternating brow lift or upward glance; unlike EXP-050, the inner lift and unilateral width remain intentionally asymmetric.',
    interpolation='Unchanged shared smoothstep; eight static anchors, eleven timeline keys, exact neutral bookends, in-memory registration only.',
    source_catalogue_sha256=h(cat),
    keyframes=[dict(time=t, phase=p, values=poses[p]) for t, p in keys])
write(W / 'EXP-123.json', d)
write(W / 'SOURCE_REFERENCE.json', dict(sheet=str(sheet), sha256=h(sheet),
    dimensions=[1159, 1358], pixels_inspected=True,
    observations='All nine sheet panels inspected before authoring. Viewer-left inner brow curves upward while the other brow lowers; viewer-left eye is narrower around the middle panels. The compact sealed mouth becomes oblique and biased sideways, strongest around panels 4-6. Panel 5 includes a head tilt, excluded from the facial-only scope. Bottom row unwinds to neutral.',
    left_right_convention='Brow and width controls use screen/viewer sides. Blink controls use character sides: blink_R narrows screen-left and blink_L narrows screen-right. The catalogue specifies no side for this expression.',
    approximation='Existing rigid outer-anchor lift approximates the local inner-brow curve without reshaping. Unilateral positive width plus symmetric purse yields a 2-source-pixel endpoint-midpoint bias at peak, not whole-mouth translation or a literal diagonal pout. Central mouth position remains fixed.',
    panel_hashes={p['actual_panel_path']: p['sha256'] for p in entry['key_pose_sequence']},
    approval='Accepted reference art is not approval of this candidate or its animation.'))
print('Prepared EXP-123: 999 pinned files, 184 PNGs and manifests; candidate outside production registry.')

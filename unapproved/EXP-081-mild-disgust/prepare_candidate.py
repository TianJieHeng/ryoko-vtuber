"""Prepare EXP-081 outside the immutable approved36 runtime and registry."""
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
assert len(ids) == 36 and 'EXP-081' not in ids
ref = ROOT / 'insight_integration_work/avatar_build_assets/reference_library'
cat = ref / 'metadata/expressions.json'
entry = next(r for r in json.loads(cat.read_text())['expressions'] if r['id'] == 'EXP-081')
sheet = ref / entry['asset_production']['actual_path']
assert h(sheet) == entry['asset_production']['sha256']
for panel in entry['key_pose_sequence']:
    assert h(ref / panel['actual_panel_path']) == panel['sha256']
# Runtime and artwork, but not expanded registry/docs, match the current published39 tree.
current = ROOT / 'approved39_integration_work/ryoko_object_rig'
parity_exclusions = ['APPROVED_INTEGRATION_STATUS.json', 'APPROVED_INTEGRATION_TEST_RESULTS.json', 'README.md', 'RELEASE.json', 'expressions/registry.json', 'tools/verify_approved_integration.py']
parity = {n: v for n,v in files.items() if n not in parity_exclusions}
for n, digest in parity.items():
    assert h(current/n) == digest, n
freeze = dict(baseline='approved36', baseline_profile_count=36,
    published_baseline_commit='3ce98774282ad6c20dfbd7018d20838ff861b762',
    source_rig=str(source), source_files=999, source_png_files=184,
    source_files_sha256=files, extra_manifests_sha256=extra,
    baseline_profile_ids=ids, source_sheet=str(sheet), source_sheet_sha256=h(sheet),
    source_catalogue=str(cat), catalogue_sha256=h(cat),
    published39_runtime_artwork_parity=dict(path=str(current), files_sha256=parity, count=len(parity), excluded_changed_metadata_registry_and_aggregate_guard=parity_exclusions))
write(W / 'BASELINE_FREEZE.json', freeze)
write(W / 'SOURCE_CATALOGUE_ENTRY.json', entry)
def pose(left,right,tl,tr,lid_left,lid_right,opening,purse,corner):
    return dict(brow_screen_left=left,brow_screen_right=right,
        brow_tilt_screen_left=tl,brow_tilt_screen_right=tr,
        blink_R=lid_left,blink_L=lid_right,mouth_open=opening,
        mouth_purse=purse,mouth_corner_lift_screen_right=corner)
poses = {
    'neutral': {},
    'detect': pose(-.14,-.03,.06,-.02,.08,.04,0,0,0),
    'recoil': pose(-.32,-.08,.15,-.06,.22,.11,0,.08,.08),
    'disgust_peak': pose(-.44,-.12,.22,-.10,.34,.18,.18,.12,.32),
    'suppress': pose(-.38,-.10,.18,-.08,.28,.14,0,.16,.12),
    'release': pose(-.20,-.06,.09,-.04,.14,.07,0,.04,0),
    'settle': pose(-.05,-.015,.02,-.01,.035,.015,0,0,0),
    'neutral_return': {},
}
write(W / 'plan.json', [dict(name=k, pose=v) for k,v in poses.items()])
keys=[(0,'neutral'),(.2,'neutral'),(.6,'detect'),(1.0,'recoil'),(1.4,'disgust_peak'),(1.75,'disgust_peak'),(2.15,'suppress'),(2.7,'release'),(3.25,'settle'),(3.7,'neutral_return'),(4,'neutral_return')]
write(W/'EXP-081.json',dict(id='EXP-081',title='Mild disgust',duration=4.0,
 status='UNAPPROVED shared-rig preparation v1; native visual review pending',
 intent=entry['distinctive_facial_intent'],
 scope='Existing unequal brow lowering/tilt, unequal ordinary lid narrowing, small split-lip opening, mild purse and screen-right common corner lift only. This corner moves BOTH lip contours; it is not independent upper-lip lift, curl or nose wrinkling. No new anatomy, art, shader or runtime; no head/body movement, smile-eye, gaze, blush or speech.',
 timing_origin='New four-second interpretation of the inspected EXP-081 nine-panel reference. Unequal brow/lid tension leads the brief parted common-corner lift at 1.4-1.75; lips seal by 2.15 while the asymmetric objection persists, then mouth bias releases before brow/lid recovery. The proposed catalogue timing is not recovered motion. Unlike Bitter taste, the tension is mild, asymmetric and not a prolonged bilateral open grimace; unlike Queasy, there is no inner-brow lift or lip pressure.',
 interpolation='Unchanged shared smoothstep; eight static anchors, eleven timeline keys, exact neutral bookends. Candidate registered only in memory.',
 source_catalogue_sha256=h(cat),keyframes=[dict(time=t,phase=p,values=poses[p]) for t,p in keys]))
write(W/'SOURCE_REFERENCE.json',dict(sheet=str(sheet),sha256=h(sheet),dimensions=[1213,1296],pixels_inspected=True,
 observations='Actual full nine-panel sheet viewed before authoring. Panels 2-4 gather uneven brow and eyelid tension; the screen-left eye narrows more. Panel 5 lifts the screen-right mouth side and parts the lips, while the opposing side remains comparatively low. Panel 6 closes the mouth but retains asymmetrical tension; panels 7-8 relax and panel 9 returns to neutral. The source head pose and subtle nose/upper-lip anatomy cannot be reconstructed by the frozen facial controls.',
 left_right_convention='Brow and corner names use screen sides. Blink names use character sides: blink_R closes screen-left and blink_L closes screen-right. The catalogue itself leaves the side unspecified.',
 approximation='The existing screen-right corner lift shifts both upper and lower lip contours together, not the upper lip independently. At peak the common screen-right endpoint is 2.4 source pixels above neutral, while the other endpoint is 1.44 pixels below; the central split-lip gap is 5.2164 source pixels. This is a partial acting approximation that may read as objection or a restrained smirk, pending native visual review. Nose wrinkle, independent upper-lip curl/lift, head tilt/recoil, cheek deformation and paired body gestures are unsupported or omitted, never claimed as simulated.',
 panel_hashes={p['actual_panel_path']:p['sha256'] for p in entry['key_pose_sequence']},
 approval='Accepted reference art does not approve this candidate or its animation.'))
print('Prepared EXP-081 with frozen 999 files and 184 PNGs, external candidate only.')

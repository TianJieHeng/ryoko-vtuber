"""Prepare EXP-104 outside the immutable approved36 runtime and registry."""
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
assert len(ids) == 36 and 'EXP-104' not in ids
ref = ROOT / 'insight_integration_work/avatar_build_assets/reference_library'
cat = ref / 'metadata/expressions.json'
entry = next(r for r in json.loads(cat.read_text())['expressions'] if r['id'] == 'EXP-104')
sheet = ref / entry['asset_production']['actual_path']
assert h(sheet) == entry['asset_production']['sha256']
for panel in entry['key_pose_sequence']:
    assert h(ref / panel['actual_panel_path']) == panel['sha256']
# Registry/release metadata is newer; common runtime/artwork is byte-identical.
parity_exclusions = ['APPROVED_INTEGRATION_STATUS.json', 'APPROVED_INTEGRATION_TEST_RESULTS.json', 'README.md', 'RELEASE.json', 'expressions/registry.json', 'tools/verify_approved_integration.py']
parity = {n: v for n,v in files.items() if n not in parity_exclusions}
freeze = dict(baseline='approved36', baseline_profile_count=36,
    published_baseline_commit='3ce98774282ad6c20dfbd7018d20838ff861b762',
    source_rig=str(source), source_files=999, source_png_files=184,
    source_files_sha256=files, extra_manifests_sha256=extra,
    baseline_profile_ids=ids, source_sheet=str(sheet), source_sheet_sha256=h(sheet),
    source_catalogue=str(cat), catalogue_sha256=h(cat))
for release in [40,41]:
    current=ROOT/f'approved{release}_integration_work/ryoko_object_rig'
    for n,digest in parity.items():assert h(current/n)==digest, str(current/n)
    freeze[f'published{release}_runtime_artwork_parity']=dict(path=str(current), files_sha256=parity, count=len(parity), excluded_changed_metadata_registry_and_aggregate_guard=parity_exclusions)
write(W / 'BASELINE_FREEZE.json', freeze)
write(W / 'SOURCE_CATALOGUE_ENTRY.json', entry)


def pose(brow,tilt,lid,smile,spread,opening):
    return dict(brow_screen_left=brow,brow_screen_right=brow,
        brow_tilt_screen_left=tilt,brow_tilt_screen_right=-tilt,
        blink_R=lid,blink_L=lid,mouth_smile=smile,mouth_spread=spread,mouth_open=opening)
poses={
 'neutral':{},
 'onset':pose(-.10,.14,.04,.18,.28,0),
 'grin_build':pose(-.22,.30,.09,.46,.60,.06),
 'tooth_grin':pose(-.32,.42,.12,.84,.86,.30),
 'open_grin':pose(-.30,.40,.10,.88,.90,.46),
 'recover':pose(-.22,.30,.08,.55,.62,.15),
 'settle':pose(-.08,.12,.03,.22,.30,0),
 'neutral_return':{},
}
write(W/'plan.json',[dict(name=k,pose=v) for k,v in poses.items()])
keys=[(0,'neutral'),(.2,'neutral'),(.6,'onset'),(1.0,'grin_build'),(1.6,'tooth_grin'),(2.0,'tooth_grin'),(2.4,'open_grin'),(2.8,'recover'),(3.2,'settle'),(3.7,'neutral_return'),(4,'neutral_return')]
write(W/'EXP-104.json',dict(id='EXP-104',title='Triumphant Grin',duration=4.0,
 status='UNAPPROVED shared-rig preparation v1; native visual review pending',
 intent=entry['distinctive_facial_intent'],
 scope='Existing bilateral equal low brow heights, mirrored inward brow tilts, equal ordinary partial lids, centered legacy smile/spread and modest opening only. Smile and spread use existing tooth and mouth support; no independent dental control, exact opposing tooth rows, clench, cheek anatomy or jaw rotation. No new art, shader, runtime, gaze, smile-eye, corner bias, head/body gesture, hair, speech or effects.',
 timing_origin='New four-second interpretation of the inspected EXP-104 nine-panel static reference, not recovered motion. Focused symmetric brows precede a centered grin, a 1.6-2.0-second shallow tooth-bearing hold, then a somewhat more open grin at 2.4 seconds. Recovery reseals the lips before exact neutral. EXP-114 has unequal lids, opposed brow heights and a crooked grin; EXP-152 has downcast sealed private pride; EXP-001 raises its brows with a much larger welcoming opening.',
 interpolation='Unchanged shared smoothstep; eight static anchors, eleven timeline keys, 121 endpoint-inclusive samples and exact neutral bookends. Candidate is registered only in memory. Zero-velocity anchor joins are deliberate; this does not claim recovered continuous source motion.',
 source_catalogue_sha256=h(cat),keyframes=[dict(time=t,phase=p,values=poses[p]) for t,p in keys]))
write(W/'SOURCE_REFERENCE.json',dict(sheet=str(sheet),sha256=h(sheet),dimensions=[1159,1358],pixels_inspected=True,
 observations='Actual full nine-panel sheet viewed before authoring. Brows descend and angle inward on both sides while eyes remain forward and visibly open. The smile broadens through panels 2-4 into a centered tooth-showing grin in panel 5, then a somewhat more open grin in panel 6. Panels 7-8 release the smile and brow tension before panel 9 returns to neutral. The expression is bilateral, not a crooked unilateral smirk.',
 left_right_convention='Brow names use screen sides. Positive left and negative right tilt lower their inner ends symmetrically. Blink names use character sides: blink_R closes screen-left and blink_L closes screen-right. Both lid values are equal throughout.',
 approximation='Uses existing upper tooth arch and spread support passively coupled to smile/spread/opening. There is no independent dental or clench control, no claim of exact opposing tooth-row anatomy, and no source-art alteration. The rendered mouth is a shallow open grin rather than a true sealed clench. Effective horizontal spread equals public mouth_spread multiplied by mouth_smile. Tooth-grin controls yield 8.91 source pixels of central aperture and 28.896 source pixels of added width; the later open grin yields 13.662 pixels of aperture and 31.68 pixels of added width. Native visible tooth exposure, lip seams, focused-eye appearance and perceptual distinction remain pending visual review.',
 panel_hashes={p['actual_panel_path']:p['sha256'] for p in entry['key_pose_sequence']},
 approval='Accepted reference art does not approve this candidate or its animation.'))
print('Prepared EXP-104 against frozen approved36: 999 files and 184 PNGs; runtime parity with approved40/41.')

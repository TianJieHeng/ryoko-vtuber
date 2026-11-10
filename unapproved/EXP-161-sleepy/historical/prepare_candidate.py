"""Prepare EXP-161 outside the immutable approved36 runtime and registry."""
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
assert len(ids) == 36 and 'EXP-161' not in ids
ref = ROOT / 'insight_integration_work/avatar_build_assets/reference_library'
cat = ref / 'metadata/expressions.json'
entry = next(r for r in json.loads(cat.read_text())['expressions'] if r['id'] == 'EXP-161')
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
current40 = ROOT / 'approved40_integration_work/ryoko_object_rig'
for n,digest in parity.items():
    assert h(current40/n) == digest, n
freeze['published40_runtime_artwork_parity'] = dict(path=str(current40), files_sha256=parity, count=len(parity), excluded_changed_metadata_registry_and_aggregate_guard=parity_exclusions)
write(W / 'BASELINE_FREEZE.json', freeze)
write(W / 'SOURCE_CATALOGUE_ENTRY.json', entry)

def pose(brow,lid,opening):
    return dict(brow_screen_left=brow,brow_screen_right=brow,blink_R=lid,blink_L=lid,mouth_open=opening)
poses={
 'neutral':{},
 'onset':pose(-.07,.14,0),
 'droop':pose(-.14,.32,.07),
 'sleepy_peak':pose(-.22,.57,.16),
 'recover':pose(-.15,.40,.11),
 'release':pose(-.08,.22,.04),
 'settle':pose(-.025,.06,0),
 'neutral_return':{},
}
write(W/'plan.json',[dict(name=k,pose=v) for k,v in poses.items()])
keys=[(0,'neutral'),(.2,'neutral'),(.6,'onset'),(1.0,'droop'),(1.6,'sleepy_peak'),(2.4,'sleepy_peak'),(2.8,'recover'),(3.2,'release'),(3.5,'settle'),(3.7,'neutral_return'),(4,'neutral_return')]
write(W/'EXP-161.json',dict(id='EXP-161',title='Sleepy',duration=4.0,
 status='UNAPPROVED shared-rig preparation v1; native visual review pending',
 intent=entry['distinctive_facial_intent'],
 scope='Existing bilateral vertical brow lowering, bilateral ordinary partial lid closure and slight split-lip opening only. Jaw relaxation is suggested solely by lip separation; there is no jaw rotation, cheek deformation, chin or skull change. Brows have no tilt or inner lift. No new anatomy, art, shader, runtime, head/body movement, gaze, smile, purse, lip pressure, blush, or speech.',
 timing_origin='New four-second interpretation of the inspected EXP-161 nine-panel static reference, not recovered motion. Gentle lid and low-brow onset precedes lip parting, followed by one gradual sink into an uninterrupted 1.6-2.4-second heavy-lid hold with slightly open lips. The recovery has no second sag, effortful snap-open or brow overshoot. Unlike EXP-164 Fighting sleep there are no repeated fighting-sleep rebounds or sealed downturn. Unlike EXP-174 Sleepy annoyance there is no sharp brow knit/tilt or pout. Unlike EXP-177 Meditative calm, eyes remain partially open and lips part slightly.',
 interpolation='Unchanged shared smoothstep; eight static anchors, eleven timeline keys and exact neutral bookends. Candidate registered only in memory. Smoothstep joins at onset/droop/recovery anchors have zero velocity; no uninterrupted constant-speed descent is claimed.',
 source_catalogue_sha256=h(cat),keyframes=[dict(time=t,phase=p,values=poses[p]) for t,p in keys]))
write(W/'SOURCE_REFERENCE.json',dict(sheet=str(sheet),sha256=h(sheet),dimensions=[1254,1254],pixels_inspected=True,
 observations='Actual full nine-panel sheet viewed before authoring. Upper lids gradually droop together from panels 2-5 without fully closing. Lips begin parting in panel 3 and stay slightly open across panels 4-6. Brows remain low and relaxed, without the acute opposing tilt of annoyance. Panels 7-8 recover toward the neutral ninth panel. Static panels imply one sustained drowsy sink rather than repeated catch-and-reopen cycles.',
 left_right_convention='Brow names use screen sides. Blink names use character sides: blink_R closes screen-left and blink_L closes screen-right. Both are equal throughout this candidate.',
 approximation='Only existing rigid vertical brow movement, ordinary lash/iris closure and split-lip opening are used. Peak lowers both brows 2.2 source pixels, advances each upper lash 20.52 source pixels, and separates lip contours by 4.752 source pixels (2.32848 at bust scale). There is no anatomical jaw rotation, chin descent, cheek inflation, new relaxed lip shape, head nod, breathing or body gesture. Heavy-lid/open-lip perceptual fidelity and distinction remain pending native review.',
 panel_hashes={p['actual_panel_path']:p['sha256'] for p in entry['key_pose_sequence']},
 approval='Accepted reference art does not approve this candidate or its animation.'))
# Read-only feasibility finding, not a replacement candidate.
cheek=next(r for r in json.loads(cat.read_text())['expressions'] if r['id']=='EXP-192')
cs=ref/cheek['asset_production']['actual_path']
assert h(cs)==cheek['asset_production']['sha256']
registry=(source/'expression_registry.gd').read_text()
assert 'cheek' not in registry.lower() and 'jaw' not in registry.lower()
write(W/'SKIPPED_EXP-192.json',dict(id='EXP-192',title='Cheeks puffed',status='SKIPPED_UNSUPPORTED_REQUIRED_ANATOMY',
 source_sheet=str(cs),source_sheet_sha256=h(cs),catalogue_sha256=h(cat),pixels_inspected=True,
 intent=cheek['distinctive_facial_intent'],
 observation='Inspected nine-panel art shows the central puffed-cheek protest with sealed puckered lips and expanded cheek contours. Cheek expansion is essential to the named expression.',
 evidence=dict(registry_path=str(source/'expression_registry.gd'),sha256=h(source/'expression_registry.gd'),finding='CHANNEL_BOUNDS contains no cheek inflation or jaw shape channel. Existing lip purse cannot inflate the cheeks.'),
 decision='Do not prepare a pout substitute, alter artwork, add anatomy, or modify the runtime. EXP-161 is the next feasible candidate.'))
print('Prepared EXP-161 against frozen approved36; 999 files, 184 PNGs, runtime parity with approved39/40. EXP-192 skipped.')

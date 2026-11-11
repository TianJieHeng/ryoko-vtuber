"""Author a NEW unapproved Sour candidate from pinned recovered bytes, once only.

Pure Python copying/JSON only. Does not import or run Godot, ffmpeg or builders.
"""
from pathlib import Path
import hashlib
import json
import shutil

W = Path(__file__).resolve().parent
RECOVERY = W.parent / 'ryoko_expression_recovery_20261111'
MAIN = RECOVERY / 'main'
HEADACHE = RECOVERY / 'headache_review_backup/EXP-096-headache-tension/historical/EXP-096.json'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

def write(p, value):
    with p.open('x') as f:
        f.write(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + '\n')

def pose(brow, tilt, lid, press, purse):
    return dict(brow_screen_left=brow, brow_screen_right=brow,
                brow_tilt_screen_left=tilt, brow_tilt_screen_right=-tilt,
                blink_L=lid, blink_R=lid, mouth_lip_press=press, mouth_purse=purse)

def main():
    if (W / 'rig').exists() or (W / 'EXP-092.json').exists():
        raise SystemExit('Prepared source is preserved; refusing overwrite.')
    inventory = json.loads((RECOVERY / 'RECOVERY_MANIFEST.json').read_text())['files']
    baseline = {}
    for item in sorted(inventory, key=lambda r: r['destination']):
        if item['destination'].startswith('main/ryoko_object_rig/'):
            src = RECOVERY / item['destination']
            assert sha(src) == item['sha256'], src
            name = item['destination'].split('main/ryoko_object_rig/', 1)[1]
            dst = W / 'rig' / name
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
            baseline[name] = sha(dst)
    assert len(baseline) == 1124
    assert sum(n.endswith('.png') for n in baseline) == 184
    ids = [r['id'] for r in json.loads((W / 'rig/expressions/registry.json').read_text())['entries']]
    assert len(ids) == 39 and not set(ids) & {'EXP-092', 'EXP-096', 'EXP-091'}
    (W / 'comparators').mkdir()
    assert sha(HEADACHE) == '21ba5c4393ed672a5496ed28577068bd4b56e3b8ff5d7ac4f9674df03badf1fe'
    shutil.copyfile(HEADACHE, W / 'comparators/EXP-096.json')
    cat = MAIN / 'avatar_build_assets/reference_library/metadata/expressions.json'
    catalogue = json.loads(cat.read_text())
    entry = next(r for r in catalogue['expressions'] if r['id'] == 'EXP-092')
    refroot = MAIN / 'avatar_build_assets/reference_library'
    source_files = {}
    for src in sorted((refroot / 'assets/expressions/EXP-092_sour-taste').glob('*.png')):
        dst = W / 'references' / src.name
        dst.parent.mkdir(exist_ok=True)
        shutil.copyfile(src, dst)
        source_files[str(dst.relative_to(W))] = sha(dst)
    assert len(source_files) == 11
    assert sha(refroot / entry['asset_production']['actual_path']) == entry['asset_production']['sha256']
    for panel in entry['key_pose_sequence']:
        assert sha(refroot / panel['actual_panel_path']) == panel['sha256']
    write(W / 'SOURCE_CATALOGUE_ENTRY.json', entry)
    write(W / 'BASELINE_FREEZE.json', {
        'identity': 'NEW recovery-based EXP-092 rebuild, 2026-11-11; NOT former local freeze',
        'repository': 'TianJieHeng/ryoko-vtuber',
        'baseline': 'approved39', 'baseline_profile_count': 39,
        'published_baseline_commit': '419450d2302d471aa009557289ad509ffb413349',
        'files_sha256': baseline, 'baseline_profile_ids': ids,
        'png_count': 184, 'recovery_manifest_sha256': sha(RECOVERY / 'RECOVERY_MANIFEST.json'),
        'headache_review_commit': '85a8bcd62a428087eb5702cb8cdee9d7594a072e',
        'headache_profile_sha256': sha(HEADACHE),
        'headache_historical_base_commit': '3ce98774282ad6c20dfbd7018d20838ff861b762',
        'headache_is_separate_approved_review_not_production': True,
        'reference_files_sha256': source_files,
        'historical_receipts_are_not_new_native_tests': True,
    })
    anchors = {
        'neutral': {},
        'taste_tension': pose(-.12, .18, .10, .12, .04),
        'sour_build': pose(-.30, .38, .28, .30, .18),
        'tighten': pose(-.45, .55, .55, .50, .40),
        'sour_peak': pose(-.55, .65, 1.0, .65, .90),
        'ease_closed': pose(-.35, .40, 1.0, .45, .55),
        'reopen_tense': pose(-.14, .18, .35, .18, .18),
        'settle': pose(-.04, .035, .10, .04, .05),
        'neutral_return': {},
    }
    keys = [(0,'neutral'),(.2,'neutral'),(.6,'taste_tension'),(1.0,'sour_build'),
            (1.3,'tighten'),(1.6,'sour_peak'),(2.0,'sour_peak'),(2.4,'ease_closed'),
            (2.8,'reopen_tense'),(3.2,'settle'),(3.7,'neutral_return'),(4.0,'neutral_return')]
    write(W / 'plan.json', [dict(name=name, pose=values) for name,values in anchors.items()])
    write(W / 'EXP-092.json', {
        'id': 'EXP-092', 'title': 'Sour Taste', 'duration': 4.0,
        'status': 'UNAPPROVED fresh recovery-based candidate; numeric preparation only; native review and MP4 pending',
        'intent': entry['distinctive_facial_intent'],
        'scope': 'Existing low/opposed rigid brows, ordinary bilateral lids, sealed lip press and substantial symmetric purse only. No new artwork, mouth_kiss, smile-eye, smile, blush, cheek hollowing, nose wrinkles, brow furrows, gaze, head/body motion, speech, runtime edits or production registry edits.',
        'timing_origin': 'Fresh four-second interpretation after inspecting the recovered nine-panel sheet. This is not recovered motion or restoration of a lost frozen profile. KP5 holds at 1.6-2.0; KP6 eases the purse with ordinary lids closed at 2.4; KP7 starts reopening with residual tension at 2.8.',
        'interpolation': 'Unchanged shared smoothstep. Nine anchors, twelve keys, exact neutral bookends. Compare native frames against exact approved EXP-096 and fresh EXP-091 before review release. Numeric separation is not proof of visual distinctness.',
        'source_catalogue_sha256': sha(cat),
        'keyframes': [dict(time=t, phase=name, values=anchors[name]) for t,name in keys],
    })
    write(W / 'SOURCE_REFERENCE.json', {
        'actual_pixels_inspected': True,
        'inspection_scope': 'Recovered EXP-092 and EXP-091 full nine-panel source sheets; no rendered candidate inspected.',
        'sheet': next(n for n in source_files if '_sheet_' in n),
        'sheet_dimensions': [1159,1358],
        'observations': 'Sour KP2-4 progressively lowers/opposes brows and narrows ordinary lids. KP5 has tightly closed eyes and a small strongly puckered sealed lip contour. KP6 remains closed but the purse eases. KP7 reopens with mild brow/lip tension; KP8 settles and KP9 is neutral. Source cheek/nose crease marks are not implemented. Sweet shows blush, a slight early mouth parting and a much broader pressed peak, so sour must not substitute that acting.',
        'panel_to_anchor': {'1':'neutral','2':'taste_tension','3':'sour_build','4':'tighten','5':'sour_peak','6':'ease_closed','7':'reopen_tense','8':'settle','9':'neutral_return'},
        'screen_convention': 'blink_R closes screen-left; blink_L closes screen-right. Screen-left positive and screen-right negative brow tilt oppose inward.',
        'approximations': ['Rigid brows cannot pinch horizontally, curve or form furrows.', 'Existing mouth_purse narrows and lowers a sealed contour; it does not reproduce real protrusion, cheek hollowing or nose wrinkles.', 'No kiss artwork, new texture, shader change, smile-eye or painted expression swap is used.'],
        'peak_numeric_geometry': {'ordinary_lash_travel_source_px':36.0,'brow_down_source_px':5.5,'brow_rotations_degrees':[5.2,-5.2],'purse':.90,'lip_press':.65,'contour_width_source_px':45.8,'central_contour_drop_source_px':3.6,'endpoint_contour_drop_source_px':10.8,'aperture_source_px':0.0},
        'headache_comparison': 'Same peak brow/lid/press controls as the exact approved EXP-096; purse .90 versus .05 gives 23.8 source-pixel formula contraction relative to EXP-096. This is not a visual result or evidence of perceptual distinctness.',
        'approval': 'Accepted reference artwork does not approve this new candidate.',
    })
    write(W / 'NATIVE_GATE.json', {
        'allowed': False,
        'status': 'BLOCKED: prior Godot launch denied; no new execution authorization established',
        'scope': 'Preparation only. No Godot/headless/render/UI/ffmpeg execution in this task.',
        'authorization_is_external': 'This file is not permission. A later authorized task must resolve the actual access restriction before any launch.',
    })
    print('Prepared NEW UNAPPROVED EXP-092; exact 1124-file/184-PNG approved39 copy, exact separate EXP-096 comparator. No native process launched.')

if __name__ == '__main__':
    main()

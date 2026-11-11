#!/usr/bin/env python3
"""Read-only EXP096 evidence validator, adapted from EXP023/EXP123 review_validation.py.

Never starts Godot, a native renderer, UI, encoding, or publication. Inputs are
read only; reports/contact sheets are written only to --output (review_evidence
by default). Missing captures/video produce PENDING and exit 2, not a false pass.
Exit 0: complete checks pass. Exit 1: failed/malformed evidence. Exit 2: pending.
MP4 layout: native full 568x800 left; native detail 400x360 at right y=220.
This checks frame evidence, not source-art fidelity or normal-speed observation.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import subprocess
import tempfile
import numpy as np
from PIL import Image, ImageDraw

ID = 'EXP-096'
# The separately pinned REVIEW_FREEZE.sha256 avoids a self-referential hash.
INPUT_FREEZE_RECEIPT = 'REVIEW_FREEZE.sha256'
FRAMES = 121
FPS = 30
ACTING = {'brow_screen_left', 'brow_screen_right', 'brow_tilt_screen_left', 'brow_tilt_screen_right', 'blink_L', 'blink_R', 'mouth_lip_press', 'mouth_purse'}
SIZES = {'full': (568, 800), 'detail': (400, 360)}
SELECTED = [0, 18, 30, 39, 48, 72, 84, 96, 120]
STATIC_FRAMES = {'neutral':0,'tension_onset':18,'heavy_build':30,'close_build':39,'headache_peak':48,'soften_closed':84,'reopen':96,'neutral_return':120}
INTERRUPTIONS = [.35, .6, 1., 1.6, 2.4, 2.8, 3.2, 3.5, 3.7]
BROW_ANCHORS = {'screen_left': (466.550, 452.350),
                'screen_right': (646.227, 453.773)}



def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text())


def write(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def read_png(path, size):
    with Image.open(path) as im:
        if im.size != size:
            raise ValueError(f'Native dimensions {path}: {im.size}, expected {size}')
        if im.mode != 'RGBA':
            raise ValueError(f'Native pixel mode {path}: {im.mode}, expected RGBA')
        im.load()
        return np.asarray(im).copy()


def bbox(mask):
    ys, xs = np.nonzero(mask)
    return [int(xs.min()), int(ys.min()), int(xs.max()+1), int(ys.max()+1)] if len(xs) else None


def outside_face_unchanged(mask):
    return bool(not mask[:270].any() and not mask[410:].any()
                and not mask[:, :200].any() and not mask[:, 360:].any())


def expected_pose(keys, t, channels):
    a, b = keys[0], keys[-1]
    for left, right in zip(keys, keys[1:]):
        if left['time'] <= t <= right['time']:
            a, b = left, right
            break
    u = max(0., min(1., (t-a['time'])/(b['time']-a['time'])))
    q = u*u*(3-2*u)
    restart = 1.
    if t < .3:
        v = t/.3
        restart = v*v*(3-2*v)
    return {k: (a['values'].get(k, 0.) +
                (b['values'].get(k, 0.)-a['values'].get(k, 0.))*q)*restart
            for k in channels}


def timeline_checks(records, keys):
    if len(records) != FRAMES:
        raise ValueError(f'Expected {FRAMES} state records, found {len(records)}')
    channels = set(records[0]['pose'])
    if not ACTING <= channels:
        raise ValueError('Missing acting channels in recorded pose')
    errors = []
    for i, row in enumerate(records):
        if row['frame'] != i or abs(row['time']-i/FPS) > 1e-12:
            raise ValueError(f'Incorrect frame number/time at record {i}')
        if set(row['pose']) != channels:
            raise ValueError(f'Pose channel set changed at frame {i}')
        expected = expected_pose(keys, row['time'], channels)
        for k, value in row['pose'].items():
            if not math.isfinite(value):
                raise ValueError(f'Non-finite pose {i} {k}')
            errors.append(abs(value-expected[k]))
    poses = [r['pose'] for r in records]
    peak = poses[48]
    gaps = [lip_geometry(p, 39.5)[1] for p in poses]
    def invariant(p):
        return all(v==0 for k,v in p.items() if k not in ACTING) and 0<=p['blink_L']==p['blink_R']<=1 and 0<=p['mouth_purse']<=.050001 and 0<=p['mouth_lip_press']<=.650001
    tests = {
        'independent_smoothstep_timeline': max(errors)<1e-6,
        'only_eight_nonzero_channels_act': all(v==0 for p in poses for k,v in p.items() if k not in ACTING),
        'acting_channels_within_shared_bounds': all(-1<=p[k]<=1 if k.startswith('brow_') else 0<=p[k]<=1 for p in poses for k in ACTING),
        'sealed_frontal_scope': all(invariant(p) for p in poses),
        'lowered_equal_brows': all(-.550001<=p['brow_screen_left']==p['brow_screen_right']<=0 for p in poses) and abs(peak['brow_screen_left']+.55)<1e-6,
        'opposed_brow_tilts': all(0<=p['brow_tilt_screen_left']<=.650001 and abs(p['brow_tilt_screen_left']+p['brow_tilt_screen_right'])<1e-6 for p in poses) and abs(peak['brow_tilt_screen_left']-.65)<1e-6,
        'ordinary_bilateral_lids': all(0<=p['blink_R']==p['blink_L']<=1 for p in poses),
        'fully_closed_peak': peak['blink_R']==peak['blink_L']==1,
        'closed_through_KP7': all(p['blink_L']==p['blink_R']==1 for p in poses[48:85]),
        'tension_softens_before_reopening': poses[84]['brow_screen_left']>peak['brow_screen_left'] and poses[84]['brow_tilt_screen_left']<peak['brow_tilt_screen_left'] and poses[84]['mouth_lip_press']<peak['mouth_lip_press'] and poses[84]['mouth_purse']==0 and poses[84]['blink_L']==1,
        'sealed_pressure_and_tiny_purse': abs(peak['mouth_lip_press']-.65)<1e-6 and abs(peak['mouth_purse']-.05)<1e-6 and all(g==0 for g in gaps),
        'exact_peak_hold_48_through_72': all(p==peak for p in poses[48:73]),
        'monotone_closure': all(poses[i]['blink_L']>=poses[i-1]['blink_L'] for i in range(1,49)),
        'delayed_monotone_reopening': all(poses[i]['blink_L']<=poses[i-1]['blink_L'] for i in range(85,121)),
        'no_opening_smile_corners_gaze_aversion': all(p[k]==0 for p in poses for k in ['mouth_open','mouth_smile','mouth_corner_lift','mouth_corner_lift_screen_left','mouth_corner_lift_screen_right','gaze_x','gaze_y','gaze_down_extra','aversion_px','opening_px','eye_smile_L','eye_smile_R']),
        'neutral_hold_states': all(v==0 for r in records if r['time']<=.2 or r['time']>=3.7 for v in r['pose'].values()),
        'bounded_frame_steps': all(abs(poses[i][k]-poses[i-1][k])<.20 for i in range(1,FRAMES) for k in ACTING),
        'all_recorded_mouth_gaps_match_independent_math': all(math.isfinite(r['central_lip_gap_native_px']) and abs(r['central_lip_gap_native_px']-g)<1e-5 for r,g in zip(records,gaps)),
        'actual_iris_sprite_and_shader_offsets': all(max(abs(r['iris_geometry'][side][field][j]) for j in range(2))<1e-4 for r in records for side in ['screen_left','screen_right'] for field in ['sprite_delta_source_px','iris_shader_offset_source_px']),
        'actual_pressed_lip_owners': all(bool(r['pressure_owners']) and all(abs(x['amount']-r['pose']['mouth_lip_press'])<1e-6 and x['visible']==(r['pose']['mouth_lip_press']>0) for x in r['pressure_owners']) for r in records),
    }
    return {'max_smoothstep_control_error': max(errors), 'assertions': tests}


def lip_geometry(p, x):
    """Frozen no-smile/no-spread formula: common lift, then symmetric aperture.

    Returns upper contour and gap, not an independent upper-lip-only lift.
    """
    radius = min(abs((x-39.5)/35.5), 1.)
    purse, opening = p['mouth_purse'], p['mouth_open']
    side = p['mouth_corner_lift_screen_right'] if x >= 39.5 else 0.
    upper = purse*(4+8*radius**2)-12*side*radius**3
    aperture = 1.
    if purse > 0:
        width_scale = 1-14*purse/35.5
        cavity = 38-12*opening*.55-14*purse
        h = max(0., min(abs((x-39.5)*width_scale)/cavity, 1.))
        aperture = 1+(math.sqrt(max(0., 1-h*h))-1)*purse
    gap = max(0., opening*.55*54*aperture-1.5*purse*min(opening*4, 1.))
    return upper, gap


def static_geometry_checks(rows, records, rig):
    """Recompute from frozen object pivots; never runs the Godot probes."""
    objects = load(rig/'rig_assets/object_face/manifest.json')['objects']
    tests = {'exact_eight_static_records': len(rows) == len(records) == 8,
             'static_pose_values': True, 'anchored_brow_geometry': True,
             'blink_sides_and_lash_travel': True, 'symmetric_purse_width': True,
             'common_corner_and_purse_lip_contour': True, 'both_lips_share_side_bias': True, 'central_mouth_gap': True,
             'horizontal_mapping_monotonic': True, 'actual_aversion_offsets': True, 'actual_pressed_lip_owners':True}
    evidence = []

    def rotated(v, angle):
        c, s = math.cos(angle), math.sin(angle)
        return np.array([v[0]*c-v[1]*s, v[0]*s+v[1]*c])

    for plan, row in zip(rows, records):
        p = row['pose']
        tests['static_pose_values'] &= plan['name'] == row['name'] and all(math.isfinite(v) and abs(v-plan['pose'].get(k, 0)) < 1e-6 for k, v in p.items())
        for side, sign in [('screen_left', -1), ('screen_right', 1)]:
            legacy = math.radians(8*p['brow_tilt_'+side])
            lift = math.radians(sign*26*p['brow_inner_lift_'+side])
            anchor = np.asarray(BROW_ANCHORS[side])
            pivot = np.asarray(objects['brow_'+side]['pivot'])
            a = anchor-pivot
            expected = np.array([0., -10*p['brow_'+side]]) + rotated(a-rotated(a, lift), legacy)
            actual = row['brow_geometry'][side]
            tests['anchored_brow_geometry'] &= bool(np.max(np.abs(np.asarray(actual['pivot_delta_source_px'])-expected)) < 1e-4 and abs(actual['rotation_degrees']-math.degrees(legacy+lift)) < 1e-5 and abs(actual['inner_lift']-p['brow_inner_lift_'+side]) < 1e-6 and np.max(np.abs(np.asarray(actual['outer_anchor'])-anchor)) < 1e-4)
            # The explicit screen-side controls and character-side blinks differ.
            amount = p['blink_R' if side == 'screen_left' else 'blink_L']
            lash = row['lash_geometry'][side]
            tests['blink_sides_and_lash_travel'] &= abs(lash['closure']-amount) < 1e-6 and abs(lash['pivot_delta_source_px'][0]) < 1e-6 and abs(lash['pivot_delta_source_px'][1]-36*amount) < 1e-4
        tests['actual_aversion_offsets'] &= all(max(abs(row['iris_geometry'][side][field][j]-expected) for j,expected in enumerate([p['aversion_px'],0]))<1e-4 for side in ['screen_left','screen_right'] for field in ['sprite_delta_source_px','iris_shader_offset_source_px'])
        tests['actual_pressed_lip_owners'] &= bool(row['pressure_owners']) and all(abs(x['amount']-p['mouth_lip_press'])<1e-6 and x['visible']==(p['mouth_lip_press']>0) for x in row['pressure_owners'])
        purse, opening = p['mouth_purse'], p['mouth_open']
        left, right = 14*purse, -14*purse
        tests['symmetric_purse_width'] &= p['mouth_width_screen_left'] == p['mouth_width_screen_right'] == 0 and max(abs(a-b) for a, b in zip(row['actual_mouth_side_delta_source_px'], [left, right])) < 1e-6
        offsets = row['lip_contour_offsets']
        tests['common_corner_and_purse_lip_contour'] &= [r['x'] for r in offsets] == [4., 39.5, 75.]
        for r in offsets:
            upper, gap = lip_geometry(p, r['x'])
            tests['common_corner_and_purse_lip_contour'] &= abs(r['upper_y']-upper) < 1e-5 and abs(r['lower_y']-upper-gap) < 1e-5 and r['lower_y'] >= r['upper_y']
        tests['both_lips_share_side_bias'] &= all(abs(offsets[0][k]-offsets[2][k]-12*p['mouth_corner_lift_screen_right']) < 1e-5 for k in ['upper_y', 'lower_y'])
        central = max(0., opening*.55*54-1.5*purse*min(opening*4, 1.))
        tests['central_mouth_gap'] &= abs(row['central_lip_gap_native_px']-central) < 1e-5 and abs(row['central_lip_gap_bust_px']-.49*central) < 1e-5
        xs = [4+i*.5 for i in range(143)]
        mapped = [x-14*purse*(x-39.5)/35.5 for x in xs]
        tests['horizontal_mapping_monotonic'] &= all(b > a for a, b in zip(mapped, mapped[1:]))
        evidence.append({'pose': row['name'], 'endpoint_deltas_source_px': [left, right],
                         'central_gap_source_px': central, 'central_gap_bust_px': central*.49,
                         'horizontal_center_motion_source_px': 0.,
                         'mouth_width_source_px': 71+right-left,
                         'upper_endpoint_offsets_source_px': [lip_geometry(p, 4)[0], lip_geometry(p, 75)[0]],
                         'note': 'Sealed pressure and a tiny symmetric purse approximate the pressed line. Purse shifts the center and both endpoints; this is not a genuine independent downturned corner. No mouth opening or corner control is used.'})
    return {'assertions': tests, 'mouth_approximation': evidence}


def source_catalogue_checks(w, freeze, ref, check, report):
    catalogue = load(Path(freeze['source_catalogue']))
    entries = [r for r in catalogue['expressions'] if r['id'] == ID]
    check('exact_source_catalogue_entry', len(entries) == 1 and entries[0] == load(w/'SOURCE_CATALOGUE_ENTRY.json'))
    entry = entries[0]
    root = Path(freeze['source_catalogue']).parent.parent
    panels = entry['key_pose_sequence']
    check('exact_nine_source_panels', len(panels) == len(ref['panel_hashes']) == 9)
    hashes, crops = {}, {}
    with Image.open(ref['sheet']) as sheet:
        for panel in panels:
            name = panel['actual_panel_path']
            hashes[name] = sha(root/name) == ref['panel_hashes'][name] == panel['sha256']
            with Image.open(root/name) as im:
                crops[name] = bool(np.array_equal(np.asarray(sheet.crop(panel['crop_bounds_xyxy']).convert('RGBA')), np.asarray(im.convert('RGBA'))))
    report['source_panel_hash_checks'] = hashes
    report['source_panel_lossless_crop_checks'] = crops
    check('source_panel_hashes', all(hashes.values()))
    check('source_panels_are_exact_sheet_crops', all(crops.values()))


def compare_profiles(w, freeze, candidate, channels):
    """No visual distinction claim: independently sampled profile trajectories."""
    root = Path(freeze['source_rig'])
    registry = load(root/'expressions/registry.json')
    paths = [root/r['path'].removeprefix('res://') for r in registry['entries']]
    paths += [w.parent/'mental_arithmetic_work/EXP-129.json',
              w.parent/'controlled_anger_work/EXP-041.json',
              w.parent/'broad_surprise_work/EXP-061.json',
              w.parent/'puzzled_work/EXP-123.json',
              w.parent/'open_sobbing_work/EXP-023.json', w.parent/'mild_disgust_work/EXP-081.json', w.parent/'sleepy_work/EXP-161.json', w.parent/'irritated_side_eye_work/EXP-045.json', w.parent/'triumphant_grin_work/EXP-104.json']
    active = lambda d: sorted({k for f in d['keyframes'] for k, v in f['values'].items() if v != 0})
    own = active(candidate)
    results = []
    for path in paths:
        other = load(path)
        delta = []
        for i in range(FRAMES):
            a = expected_pose(candidate['keyframes'], candidate['duration']*i/(FRAMES-1), channels)
            b = expected_pose(other['keyframes'], other['duration']*i/(FRAMES-1), channels)
            delta.extend(abs(a[k]-b[k]) for k in channels)
        results.append({'id': other['id'], 'title': other['title'], 'path': str(path),
                        'sha256': sha(path), 'active_controls': active(other),
                        'same_active_controls': own == active(other),
                        'maximum_control_difference': max(delta),
                        'rms_all_channel_difference': math.sqrt(sum(v*v for v in delta)/len(delta))})
    return {'compared_profiles': len(results), 'candidate_active_controls': own,
            'all_distinct': all(r['maximum_control_difference'] > .01 for r in results),
            'limitation': 'Numeric control/timing differences do not prove perceptual distinction. The 36-profile baseline is intentionally separate from the newer integration checkpoints.',
            'comparisons': results}


def run(args):
    w = args.work.resolve()
    out = args.output.resolve() if args.output else w/'review_evidence'
    out.mkdir(parents=True, exist_ok=True)
    video = args.video.resolve() if args.video else w/'Headache_tension_review_v1.mp4'
    report = {
        'candidate': ID, 'approval': 'UNAPPROVED; isolated evidence review only',
        'scope': 'Source preservation, independent pose math, all native RGBA frames, dimensions, neutral/body pixels, complete MP4 decode and frame order. No renderer or UI is invoked.',
        'normal_speed_continuous_observation': False,
        'perceptual_source_fidelity_or_distinction_proven': False,
        'checks': {}, 'pending': [], 'failures': [], 'video_path': str(video),
    }

    def check(name, passed):
        report['checks'][name] = bool(passed)
        if not passed:
            report['failures'].append(name)

    def finish():
        report['independent_checks_pass'] = not report['failures'] and not report['pending']
        report['status'] = 'FAIL' if report['failures'] else ('PENDING' if report['pending'] else 'PASS')
        write(out/'review_checks.json', report)
        if report['pending']:
            write(out/'partial_review.json', report)
        print(json.dumps({k: report[k] for k in ['status', 'independent_checks_pass', 'failures', 'pending', 'approval']}, indent=2))
        return 1 if report['failures'] else (2 if report['pending'] else 0)

    try:
        freeze = load(w/'BASELINE_FREEZE.json')
        known = freeze['source_files_sha256']
        roots = [w/'rig', Path(freeze['source_rig'])]
        report.update(baseline=freeze['baseline'], baseline_commit=freeze.get('baseline_commit', freeze.get('published_baseline_commit')),
                      baseline_file_count=len(known), baseline_png_count=sum(p.endswith('.png') for p in known))
        report['frozen_source_changes'] = {str(root): [n for n, h in known.items() if not (root/n).is_file() or sha(root/n) != h] for root in roots}
        check('all_999_pinned_source_files_unchanged_in_both_roots', len(known) == 999 and sum(p.endswith('.png') for p in known) == 184 and not any(report['frozen_source_changes'].values()))
        report['extra_manifest_hash_checks'] = {str(root): {n: (root/n).is_file() and sha(root/n) == h for n, h in freeze['extra_manifests_sha256'].items()} for root in roots}
        check('approved_manifest_unchanged', all(all(v.values()) for v in report['extra_manifest_hash_checks'].values()))
        parity = freeze['published41_runtime_artwork_parity']
        exclusions = {'APPROVED_INTEGRATION_STATUS.json', 'APPROVED_INTEGRATION_TEST_RESULTS.json', 'README.md', 'RELEASE.json', 'expressions/registry.json', 'tools/verify_approved_integration.py'}
        report['published41_runtime_parity_changes'] = [n for n, h in parity['files_sha256'].items() if not (Path(parity['path'])/n).is_file() or sha(Path(parity['path'])/n) != h or known.get(n) != h]
        check('all_993_runtime_artwork_files_match_published41', parity['count'] == len(parity['files_sha256']) == 993 and set(parity['files_sha256']) == set(known)-exclusions and set(parity['excluded_changed_metadata_registry_and_aggregate_guard']) == exclusions and not report['published41_runtime_parity_changes'])
        report['registry_ids'] = {str(root): [e['id'] for e in load(root/'expressions/registry.json')['entries']] for root in roots}
        check('approved36_registry_unchanged_candidate_absent', all(ids == freeze['baseline_profile_ids'] and ID not in ids for ids in report['registry_ids'].values()))
        check('expected_review_input_freeze_identity', sha(w/'review_input_freeze.json') == (w/INPUT_FREEZE_RECEIPT).read_text().split()[0])
        input_freeze = load(w/'review_input_freeze.json')
        check('complete_preparation_freeze', input_freeze['candidate'] == ID and len(input_freeze['files']) >= 35 and {'EXP-096.json','plan.json','check_and_capture.gd','render_motion.gd','review_validation.py','native_launcher/project.godot','state_checks.json','motion_state_checks.json','SOURCE_REFERENCE.json'} <= set(input_freeze['files']))
        report['review_input_changes'] = [n for n, h in input_freeze['files'].items() if not (w/n).is_file() or sha(w/n) != h]
        check('reviewed_candidate_and_capture_inputs_unchanged', not report['review_input_changes'])
        launcher = w/'native_launcher'
        report['launcher_pinned_changes'] = [n for n, h in known.items() if not (launcher/n).is_file() or sha(launcher/n) != h]
        check('launcher_only_expected_project_override', report['launcher_pinned_changes'] == ['project.godot'])
        # This launcher also retained the extra approved source manifest.
        report['launcher_extra_manifests'] = {n: ('matching' if sha(launcher/n) == h else 'MISMATCH') if (launcher/n).is_file() else 'MISSING' for n, h in freeze['extra_manifests_sha256'].items()}
        check('launcher_present_extra_manifests_match', all(v == 'matching' for v in report['launcher_extra_manifests'].values()))
        ref = load(w/'SOURCE_REFERENCE.json')
        check('source_sheet_hash', sha(Path(ref['sheet'])) == ref['sha256'] == freeze['source_sheet_sha256'])
        check('source_catalogue_hash', sha(Path(freeze['source_catalogue'])) == freeze['catalogue_sha256'])
        with Image.open(ref['sheet']) as im:
            check('source_sheet_dimensions', im.size == (1159, 1358) and list(im.size) == ref['dimensions'])
        source_catalogue_checks(w, freeze, ref, check, report)
        candidate = load(w/'EXP-096.json')
        keys = candidate['keyframes']
        check('candidate_id_duration_and_unapproved', candidate['id'] == ID and candidate['duration'] == 4 and candidate['status'].startswith('UNAPPROVED'))
        check('ordered_eleven_timeline_keys', len(keys) == 11 and keys[0]['time'] == 0 and keys[-1]['time'] == 4 and all(b['time'] > a['time'] for a, b in zip(keys, keys[1:])))
        rows = load(w/'plan.json')
        names = [r['name'] for r in rows]
        check('eight_unique_static_anchors', len(names) == len(set(names)) == 8)
        state = load(w/'state_checks.json')
        motion_state = load(w/'motion_state_checks.json')
        for label, receipt, count in [('static_state', state, 1806), ('motion_state', motion_state, 16260)]:
            check(label+'_receipt_pass', receipt['status'] == 'PASS' and not receipt['failures'] and receipt['checks'] == count and receipt['visual_capture'] is False and receipt['production_registry_unchanged'])
        check('static_record_order', [r['name'] for r in state['records']] == names)
        report['independent_static_geometry'] = static_geometry_checks(rows, state['records'], w/'rig')
        check('independent_static_poses_and_geometry', all(report['independent_static_geometry']['assertions'].values()))
        check('headless_receipts_tied_to_frozen_inputs', state['plan_sha256'] == sha(w/'plan.json') and motion_state['profile_sha256'] == sha(w/'EXP-096.json') and state['baseline_freeze_sha256'] == motion_state['baseline_freeze_sha256'] == sha(w/'BASELINE_FREEZE.json'))
        check('headless_receipts_correct_baseline', all(r['baseline'] == freeze['baseline'] and r['baseline_profile_count'] == 36 for r in [state, motion_state]))
        check('headless_receipts_do_not_invent_native_pixels', motion_state['display'] == 'headless' and not motion_state['renderer'] and all(r['hashes'] == [] for r in motion_state['records']))
        check('headless_lifecycle_receipt', motion_state['lifecycle_assertions'] == 36 and motion_state['lifecycle_interruption_times'] == INTERRUPTIONS)
        life=motion_state['lifecycle_scoped_samples']
        check('252_lifecycle_scoped_samples', len(life)==252 and all(r['pose']['blink_L']==r['pose']['blink_R'] and all(v==0 for k,v in r['pose'].items() if k not in ACTING) for r in life))
        expected_channels = set(json.loads((w/'rig/expression_rig.gd').read_text().split('const CHANNELS=', 1)[1].splitlines()[0]))
        check('headless_pose_has_exact_shared_channels', all(set(r['pose']) == expected_channels for r in state['records'] + motion_state['records']))
        check('candidate_uses_only_allowed_channels', all(set(k['values']) <= ACTING for k in keys))
        check('eight_anchors_are_exact_key_values', all(any(r['pose'] == k['values'] for k in keys) for r in rows))
        report['independent_profile_comparison'] = compare_profiles(w, freeze, candidate, expected_channels)
        check('independent_45_profile_nonduplication', report['independent_profile_comparison']['all_distinct'] and report['independent_profile_comparison']['compared_profiles'] == 45)
        report['headless_independent_timeline'] = timeline_checks(motion_state['records'], keys)
        check('headless_independent_timeline_and_intent', all(report['headless_independent_timeline']['assertions'].values()))

        required_static = [w/f'capture/{n}_{v}.png' for n in names for v in ['bust', 'detail']]
        missing_static = [str(p.relative_to(w)) for p in required_static+[w/'capture/checks.json'] if not p.is_file()]
        report['missing_static_inputs'] = missing_static
        static_arrays = {}
        if (w/'capture/checks.json').is_file():
            receipt = load(w/'capture/checks.json')
            report['static_native_receipt'] = {k: v for k, v in receipt.items() if k != 'records'}
            check('native_static_receipt_pass', receipt['status'] == 'PASS' and not receipt['failures'] and receipt['visual_capture'] is True and receipt['production_registry_unchanged'] and receipt['checks'] == 1838)
            check('native_static_receipt_tied_to_frozen_inputs', receipt['plan_sha256'] == sha(w/'plan.json') and receipt['baseline_freeze_sha256'] == sha(w/'BASELINE_FREEZE.json') and receipt['baseline'] == freeze['baseline'] and receipt['baseline_profile_count'] == 36)
            check('native_static_records_equal_headless', receipt['records'] == state['records'])
        if missing_static:
            report['pending'].append('Native static capture incomplete: '+str(len(missing_static))+' required files missing.')
        else:
            check('exact_16_native_static_filenames', sorted(p.name for p in (w/'capture').glob('*.png')) == sorted(p.name for p in required_static))
            report['static_pixel_changes'] = {}
            for view, size in SIZES.items():
                suffix = 'bust' if view == 'full' else 'detail'
                arrays = {n: read_png(w/f'capture/{n}_{suffix}.png', size) for n in names}
                static_arrays[view] = arrays
                evidence = []
                for n, ar in arrays.items():
                    mask = np.any(ar != arrays['neutral'], axis=2)
                    evidence.append({'pose': n, 'changed_pixels': int(mask.sum()), 'difference_bbox_xyxy': bbox(mask),
                                     'png_sha256': sha(w/f'capture/{n}_{suffix}.png'), 'rgba_sha256': hashlib.sha256(ar.tobytes()).hexdigest()})
                    if view == 'full':
                        check('static_body_unchanged_'+n, outside_face_unchanged(mask))
                report['static_pixel_changes'][view] = evidence
                check('static_neutral_exact_'+view, np.array_equal(arrays['neutral'], arrays['neutral_return']))
            sheet = Image.new('RGB', (1200, 1200), (32, 34, 36)); draw = ImageDraw.Draw(sheet)
            for j, n in enumerate(names):
                x, y = (j%3)*400, (j//3)*400
                sheet.paste(Image.fromarray(static_arrays['detail'][n]).convert('RGB'), (x, y+30))
                draw.text((x+10, y+8), n, fill='white')
            sheet.save(out/'static_faces.png')

        required_motion = [w/f'motion/{view}/{i:04d}.png' for view in SIZES for i in range(FRAMES)]
        missing_motion = [str(p.relative_to(w)) for p in required_motion+[w/'motion_checks.json'] if not p.is_file()]
        report['missing_motion_inputs'] = missing_motion
        if (w/'motion_checks.json').is_file():
            motion = load(w/'motion_checks.json')
            report['native_motion_receipt'] = {k: v for k, v in motion.items() if k != 'records'}
            check('native_motion_receipt_pass', motion['checks'] == 16745 and motion['status'] == 'PASS' and not motion['failures'] and motion['visual_capture'] is True and motion['production_registry_unchanged'] and motion['display'] not in ['', 'headless'] and bool(motion['renderer']) and motion['frames'] == FRAMES and motion['fps'] == FPS and motion['duration'] == 4)
            check('native_motion_receipt_tied_to_frozen_inputs', motion['profile_sha256'] == sha(w/'EXP-096.json') and motion['baseline_freeze_sha256'] == sha(w/'BASELINE_FREEZE.json') and motion['baseline'] == freeze['baseline'] and motion['baseline_profile_count'] == 36)
            check('native_lifecycle_receipt', motion['lifecycle_assertions'] == 36 and motion['lifecycle_interruption_times'] == INTERRUPTIONS)
            report['native_independent_timeline'] = timeline_checks(motion['records'], keys)
            check('native_independent_timeline_and_intent', all(report['native_independent_timeline']['assertions'].values()))
            check('all_native_poses_match_headless', [r['pose'] for r in motion['records']] == [r['pose'] for r in motion_state['records']])
        if missing_motion:
            report['pending'].append('Native motion capture incomplete: '+str(len(missing_motion))+' required files missing.')
            if not video.is_file():
                report['pending'].append('Review MP4 absent; decode/order checks not run.')
            else:
                report['pending'].append('Review MP4 exists but cannot be checked against incomplete native frames.')
            return finish()

        arrays_by_view = {}; all_hashes = []; diffs = {}
        for vi, (view, size) in enumerate(SIZES.items()):
            paths = sorted((w/'motion'/view).glob('*.png'))
            check('exact_121_native_filenames_'+view, [p.name for p in paths] == [f'{i:04d}.png' for i in range(FRAMES)])
            arrays = [read_png(w/f'motion/{view}/{i:04d}.png', size) for i in range(FRAMES)]
            union = np.zeros(arrays[0].shape[:2], dtype=bool); counts = []
            for i, ar in enumerate(arrays):
                raw = hashlib.sha256(ar.tobytes()).hexdigest()
                hashes = motion['records'][i]['hashes']
                ok = len(hashes) == 2 and raw == hashes[vi]
                all_hashes.append({'view': view, 'frame': i, 'png_sha256': sha(w/f'motion/{view}/{i:04d}.png'), 'rgba_sha256': raw, 'matches_capture_record': ok})
                mask = np.any(ar != arrays[0], axis=2); union |= mask; counts.append(int(mask.sum()))
            diffs[view] = {'changed_pixels_each_frame': counts, 'union_difference_bbox_xyxy': bbox(union), 'neutral_bookends_identical': np.array_equal(arrays[0], arrays[-1])}
            check('native_neutral_holds_exact_'+view, all(counts[i] == 0 for i in list(range(7))+list(range(111, 121))))
            check('nontrivial_native_expression_'+view, max(counts) > 0)
            check('sustained_peak_pixels_'+view, all(np.array_equal(arrays[48], arrays[i]) for i in range(48, 73)))
            if view == 'full':
                diffs[view]['all_pixels_outside_face_box_200_270_360_410_unchanged'] = outside_face_unchanged(union)
                check('all_native_body_pixels_fixed', outside_face_unchanged(union))
            if static_arrays:
                for name, i in STATIC_FRAMES.items():
                    check('static_motion_exact_'+view+'_'+name, np.array_equal(static_arrays[view][name], arrays[i]))
            arrays_by_view[view] = [ar[:, :, :3].copy() for ar in arrays]
        report['motion_pixel_changes'] = diffs
        write(out/'native_frame_hashes.json', all_hashes)
        check('all_242_native_rgba_hashes_match', len(all_hashes) == 242 and all(r['matches_capture_record'] for r in all_hashes))
        if not video.is_file():
            report['pending'].append('Review MP4 absent; decode/order checks not run.')
            return finish()

        probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_frames', '-show_entries', 'stream=codec_name,width,height,pix_fmt,r_frame_rate,nb_frames,nb_read_frames:format=duration,size', '-of', 'json', str(video)], timeout=120))
        report['video_probe'] = probe; report['video_sha256'] = sha(video)
        s = probe['streams'][0]
        check('video_encoding_and_duration', s['codec_name'] == 'h264' and s['pix_fmt'] == 'yuv420p' and abs(float(probe['format']['duration'])-FRAMES/FPS) < .002)
        check('video_geometry_and_count', s['width'] == 968 and s['height'] == 800 and s['r_frame_rate'] == '30/1' and int(s['nb_read_frames']) == FRAMES)
        if (s['width'], s['height']) != (968, 800):
            raise ValueError('MP4 layout mismatch; refusing misaligned frame comparisons')
        pts = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'frame=best_effort_timestamp_time', '-of', 'json', str(video)], timeout=120))['frames']
        check('mp4_all_monotonic_30fps_pts', len(pts) == FRAMES and all(abs(float(r['best_effort_timestamp_time'])-i/FPS) < 1e-5 for i, r in enumerate(pts)))
        features = np.asarray([a[55:285, 40:320][::2, ::2].astype(np.float32) for a in arrays_by_view['detail']])
        errors = {'full': [], 'detail': []}; nearest = []; selected = {}; count = 0
        with tempfile.TemporaryFile() as err:
            p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', str(video), '-map', '0:v:0', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE, stderr=err)
            try:
                rbytes = 968*800*3
                while True:
                    buf = p.stdout.read(rbytes)
                    if not buf:
                        break
                    if len(buf) != rbytes:
                        raise ValueError(f'Incomplete decoded frame {count}: {len(buf)} bytes')
                    if count >= FRAMES:
                        raise ValueError('MP4 contains more than 121 decoded frames')
                    ar = np.frombuffer(buf, np.uint8).reshape(800, 968, 3)
                    for view, crop in [('full', ar[:, :568]), ('detail', ar[220:580, 568:968])]:
                        errors[view].append(float(np.abs(crop.astype(np.int16)-arrays_by_view[view][count].astype(np.int16)).mean()))
                    feat = ar[275:505, 608:888][::2, ::2].astype(np.float32)
                    dist = np.abs(features-feat).mean(axis=(1, 2, 3)); best = float(dist.min())
                    nearest.append({'frame': count, 'expected_face_mae': float(dist[count]), 'best_face_mae': best, 'expected_minus_best': float(dist[count]-best), 'best_matching_frame': int(dist.argmin())})
                    if count in SELECTED:
                        selected[count] = ar[220:580, 568:968].copy()
                    count += 1
                code = p.wait(timeout=60)
            finally:
                if p.poll() is None:
                    p.kill(); p.wait()
                p.stdout.close()
            err.seek(0); stderr = err.read().decode(errors='replace')
        report['mp4_full_decode'] = {'frames': count, 'exit_code': code, 'stderr': stderr}
        check('mp4_complete_clean_decode', count == FRAMES and code == 0 and not stderr)
        if not nearest:
            raise ValueError('No video frames available for comparison')
        report['mp4_source_panel_mae'] = {v: {'mean': float(np.mean(a)), 'max': max(a), 'frames': len(a)} for v, a in errors.items()}
        report['mp4_order_checks'] = {'method': 'All decoded frames compared with same-index full/detail native panels and all-frame nearest-face errors; identical and near-identical holds remain ambiguous under lossy encoding.', 'max_expected_face_mae': max(r['expected_face_mae'] for r in nearest), 'max_expected_minus_best_face_mae': max(r['expected_minus_best'] for r in nearest), 'selected': [r for r in nearest if r['frame'] in SELECTED], 'all_frame_detail_file': 'decoded_frame_order.json'}
        write(out/'decoded_frame_order.json', nearest)
        check('mp4_no_material_frame_reorder', max(r['expected_minus_best'] for r in nearest) < .10)
        check('mp4_same_index_native_panel_similarity', all(max(a) < 3.0 for a in errors.values()) and max(r['expected_face_mae'] for r in nearest) < 5.0)
        sheet = Image.new('RGB', (1200, 1170), (32, 34, 36)); draw = ImageDraw.Draw(sheet)
        for j, i in enumerate(SELECTED):
            if i in selected:
                x, y = j%3*400, j//3*390
                sheet.paste(Image.fromarray(selected[i]), (x, y+30)); draw.text((x+10, y+8), f'Encoded frame {i:03d} | {i/FPS:.3f} s', fill='white')
        sheet.save(out/'encoded_keyframes.png')
        sheet = Image.new('RGB', (568*4, 830), (32, 34, 36)); draw = ImageDraw.Draw(sheet)
        for j, i in enumerate([0, 30, 48, 84]):
            sheet.paste(Image.fromarray(arrays_by_view['full'][i]), (568*j, 30)); draw.text((568*j+12, 9), f'Native frame {i:03d} | {i/FPS:.3f} s', fill='white')
        sheet.save(out/'bust_progression.png')
    except Exception as exc:
        report['failures'].append(f'{type(exc).__name__}: {exc}')
    return finish()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--video', type=Path, help='Default: WORK/Headache_tension_review_v1.mp4')
    raise SystemExit(run(parser.parse_args()))

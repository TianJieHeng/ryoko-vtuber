#!/usr/bin/env python3
"""Independent read-only EXP104 reviewer, using the established reviewer-only capture/decode scaffold.

Triumphant Grin-specific intent and geometry are checked separately from the author probes.
The author freeze and its validator are never modified.

Never starts Godot, a native renderer, UI, encoding, or publication. Inputs are
read only; reports/contact sheets are written only to --output (independent_review_evidence
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

ID = 'EXP-104'
# This independently recorded constant is not read from a mutable checksum sidecar.
EXPECTED_INPUT_FREEZE_SHA256 = '40f54ee01529ef96d18404cd2f3ebb1e2bf3004662cf2c45055434fb063aef7a'
FRAMES = 121
FPS = 30
ACTING = {'brow_screen_left', 'brow_screen_right', 'brow_tilt_screen_left', 'brow_tilt_screen_right', 'blink_L', 'blink_R', 'mouth_smile', 'mouth_spread', 'mouth_open'}
SIZES = {'full': (568, 800), 'detail': (400, 360)}
SELECTED = [0, 18, 30, 48, 60, 72, 84, 96, 120]
STATIC_FRAMES = {'neutral': 0, 'onset': 18, 'grin_build': 30,
                 'tooth_grin': 48, 'open_grin': 72, 'recover': 84,
                 'settle': 96, 'neutral_return': 120}
INTERRUPTIONS = [.35, .6, 1., 1.6, 2., 2.4, 2.8, 3.2, 3.7]
KEY_TIMES = [0, .2, .6, 1., 1.6, 2., 2.4, 2.8, 3.2, 3.7, 4.]
# Independent interpretation contract: height, inward tilt, equal lid closure,
# smile, public spread, opening. Right tilt is the negative of left tilt.
ANCHOR_VALUES = {
    'neutral': (0, 0, 0, 0, 0, 0),
    'onset': (-.10, .14, .04, .18, .28, 0),
    'grin_build': (-.22, .30, .09, .46, .60, .06),
    'tooth_grin': (-.32, .42, .12, .84, .86, .30),
    'open_grin': (-.30, .40, .10, .88, .90, .46),
    'recover': (-.22, .30, .08, .55, .62, .15),
    'settle': (-.08, .12, .03, .22, .30, 0),
    'neutral_return': (0, 0, 0, 0, 0, 0),
}
KEY_NAMES = ['neutral','neutral','onset','grin_build','tooth_grin',
             'tooth_grin','open_grin','recover','settle','neutral_return','neutral_return']
CHANNELS = set('aversion_px blink_L blink_R blush_intensity brow_inner_lift_screen_left brow_inner_lift_screen_right brow_screen_left brow_screen_right brow_tilt_screen_left brow_tilt_screen_right eye_smile_L eye_smile_R gaze_down_extra gaze_x gaze_y hair_sway mouth_corner_lift mouth_corner_lift_screen_left mouth_corner_lift_screen_right mouth_kiss mouth_lip_press mouth_open mouth_oral_lift mouth_purse mouth_smile mouth_spread mouth_width_screen_left mouth_width_screen_right opening_px uneasy_weight'.split())

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


def near(a, b, tolerance=1e-6):
    return math.isfinite(a) and math.isfinite(b) and abs(a-b) < tolerance


def anchor_pose(name):
    h, tilt, blink, smile, spread, opening = ANCHOR_VALUES[name]
    p = dict.fromkeys(CHANNELS, 0.)
    p.update(brow_screen_left=h, brow_screen_right=h,
             brow_tilt_screen_left=tilt, brow_tilt_screen_right=-tilt,
             blink_L=blink, blink_R=blink, mouth_smile=smile,
             mouth_spread=spread, mouth_open=opening)
    return p


def contract_checks(profile, plan):
    tests = {'independent_eleven_key_times': [k['time'] for k in profile['keyframes']] == KEY_TIMES,
             'independent_eight_anchor_names': [p['name'] for p in plan] == list(STATIC_FRAMES),
             'independent_key_vectors': len(profile['keyframes']) == len(KEY_NAMES),
             'independent_static_vectors': len(plan) == len(ANCHOR_VALUES)}
    for key, name in zip(profile['keyframes'], KEY_NAMES):
        expected = anchor_pose(name)
        tests['independent_key_vectors'] &= set(key['values']) <= ACTING and all(near(key['values'].get(k, 0), expected[k]) for k in CHANNELS)
    for row, name in zip(plan, ANCHOR_VALUES):
        expected = anchor_pose(name)
        tests['independent_static_vectors'] &= set(row['pose']) <= ACTING and all(near(row['pose'].get(k, 0), expected[k]) for k in CHANNELS)
    return tests


def timeline_checks(records, keys):
    if len(records) != FRAMES:
        raise ValueError(f'Expected {FRAMES} state records, found {len(records)}')
    errors = []
    for i, row in enumerate(records):
        if row['frame'] != i or not near(row['time'], i/FPS, 1e-12):
            raise ValueError(f'Incorrect frame number/time at record {i}')
        if set(row['pose']) != CHANNELS:
            raise ValueError(f'Exact shared pose channels required at frame {i}')
        expected = expected_pose(keys, row['time'], CHANNELS)
        for k, value in row['pose'].items():
            if not math.isfinite(value):
                raise ValueError(f'Non-finite pose {i} {k}')
            errors.append(abs(value-expected[k]))
    poses = [r['pose'] for r in records]
    peak, opened = poses[48], poses[72]
    gaps = [lip_geometry(p, 39.5)[1]-lip_geometry(p, 39.5)[0] for p in poses]
    tests = {
        'independent_smoothstep_timeline': max(errors) < 1e-6,
        'only_nine_authorized_channels_act': all(v == 0 for p in poses for k, v in p.items() if k not in ACTING),
        'acting_channels_bounded': all(-1 <= p[k] <= 1 if k.startswith('brow_') else 0 <= p[k] <= 1 for p in poses for k in ACTING),
        'equal_lowered_brows': all(-.320001 <= p['brow_screen_left'] == p['brow_screen_right'] <= 0 for p in poses),
        'mirrored_inward_tilts': all(near(p['brow_tilt_screen_left'], -p['brow_tilt_screen_right']) and 0 <= p['brow_tilt_screen_left'] <= .420001 for p in poses),
        'equal_focused_ordinary_lids': all(0 <= p['blink_L'] == p['blink_R'] <= .120001 for p in poses),
        'fixed_forward_gaze': all(p[k] == 0 for p in poses for k in ['gaze_x','gaze_y','gaze_down_extra']),
        'brows_and_sealed_smile_precede_opening': poses[18]['brow_screen_left'] < 0 and poses[18]['brow_tilt_screen_left'] > 0 and poses[18]['mouth_smile'] > .179 and all(p['mouth_open'] == 0 for p in poses[:19]),
        'independent_shallow_peak_vector': all(near(peak[k], anchor_pose('tooth_grin')[k]) for k in CHANNELS),
        'independent_later_open_vector': all(near(opened[k], anchor_pose('open_grin')[k]) for k in CHANNELS),
        'shallow_peak_aperture_8_91': near(gaps[48], 8.91),
        'later_open_aperture_13_662': near(gaps[72], 13.662),
        'exact_shallow_hold_frames_48_through_60': all(p == peak for p in poses[48:61]),
        'single_monotone_opening_and_smile_build': all(poses[i][k] >= poses[i-1][k] for i in range(1,73) for k in ['mouth_open','mouth_smile','mouth_spread']),
        'single_gradual_recovery': all(poses[i][k] <= poses[i-1][k] for i in range(73,121) for k in ['mouth_open','mouth_smile','mouth_spread']),
        'reseal_precedes_final_smile_and_brow_release': poses[96]['mouth_open'] == 0 and poses[96]['mouth_smile'] > .219 and poses[96]['brow_screen_left'] < 0,
        'neutral_hold_states': all(v == 0 for r in records if r['time'] <= .2 or r['time'] >= 3.7 for v in r['pose'].values()),
        'bounded_frame_steps': all(abs(poses[i][k]-poses[i-1][k]) < .20 for i in range(1, FRAMES) for k in ACTING),
        'all_recorded_gaps_match_math': all(near(r['central_lip_gap_native_px'], g, 1e-5) for r, g in zip(records, gaps)),
    }
    return {'max_smoothstep_control_error': max(errors), 'assertions': tests}


def lip_geometry(p, x):
    """Legacy centered smile/spread/opening subset, independently evaluated.

    Spread is smile-coupled. Upper/lower offsets are geometry, not visible enamel
    evidence. Purse, oral lift, pressure, independent corners and widths are zero.
    No clench, opposing tooth rows or jaw movement can be inferred from this.
    """
    radius = min(1., abs((x-39.5)/35.5))
    smile = p['mouth_smile']; spread = smile*p['mouth_spread']
    upper = -4*spread-(4+5*spread)*smile*radius**1.5
    opening = 29.7*p['mouth_open']*((1-smile)+smile*max(0.,1-radius*radius)**.72)
    return upper, upper+opening


def static_geometry_checks(rows, records, rig):
    objects = load(rig/'rig_assets/object_face/manifest.json')['objects']
    tests = {'exact_eight_static_records': len(rows) == len(records) == 8,
             'static_pose_values': True, 'nine_channel_scope': True,
             'anchored_brow_geometry': True, 'blink_sides_and_lash_travel': True,
             'smile_coupled_spread': True, 'symmetric_upper_lower_lips': True,
             'central_mouth_gap': True, 'bilateral_brow_lid_symmetry': True}
    evidence = []
    for plan, row in zip(rows, records):
        p = row['pose']; name = plan['name']
        expected_pose_values = anchor_pose(name)
        tests['static_pose_values'] &= name == row['name'] and set(p) == CHANNELS and all(near(v, expected_pose_values[k]) for k,v in p.items())
        tests['nine_channel_scope'] &= all(v == 0 for k, v in p.items() if k not in ACTING)
        tests['bilateral_brow_lid_symmetry'] &= p['brow_screen_left'] == p['brow_screen_right'] and p['blink_L'] == p['blink_R'] and near(p['brow_tilt_screen_left'], -p['brow_tilt_screen_right'])
        brow_evidence = {}
        for side in ['screen_left', 'screen_right']:
            anchor = np.asarray(BROW_ANCHORS[side]); pivot = np.asarray(objects['brow_'+side]['pivot'])
            actual = row['brow_geometry'][side]; translation = np.asarray([0., -10*p['brow_'+side]])
            angle = math.radians(8*p['brow_tilt_'+side]); rotation = np.asarray([[math.cos(angle),-math.sin(angle)],[math.sin(angle),math.cos(angle)]])
            transformed_anchor = pivot+translation+rotation@(anchor-pivot)
            actual_angle = math.radians(actual['rotation_degrees']); actual_rotation = np.asarray([[math.cos(actual_angle),-math.sin(actual_angle)],[math.sin(actual_angle),math.cos(actual_angle)]])
            observed_anchor = pivot+np.asarray(actual['pivot_delta_source_px'])+actual_rotation@(np.asarray(actual['outer_anchor'])-pivot)
            tests['anchored_brow_geometry'] &= bool(np.max(np.abs(np.asarray(actual['pivot_delta_source_px'])-translation)) < 1e-4 and near(actual['rotation_degrees'], 8*p['brow_tilt_'+side], 1e-5) and actual['inner_lift'] == 0 and np.max(np.abs(np.asarray(actual['outer_anchor'])-anchor)) < 1e-4 and np.max(np.abs(observed_anchor-transformed_anchor)) < 2e-4)
            brow_evidence[side] = {'pivot': pivot.tolist(), 'translation_source_px': translation.tolist(), 'rotation_degrees': math.degrees(angle), 'transformed_outer_anchor': transformed_anchor.tolist()}
            amount = p['blink_R' if side == 'screen_left' else 'blink_L']; lash = row['lash_geometry'][side]
            tests['blink_sides_and_lash_travel'] &= near(lash['closure'], amount) and near(lash['pivot_delta_source_px'][0], 0) and near(lash['pivot_delta_source_px'][1], 36*amount, 1e-4)
        spread = p['mouth_smile']*p['mouth_spread']; upper, lower = lip_geometry(p, 39.5); central = lower-upper
        tests['smile_coupled_spread'] &= len(row['actual_mouth_side_delta_source_px']) == 2 and all(near(a,b,1e-5) for a,b in zip(row['actual_mouth_side_delta_source_px'],[-20*spread,20*spread]))
        offsets = row['lip_contour_offsets']
        tests['symmetric_upper_lower_lips'] &= [r['x'] for r in offsets] == [4., 39.5, 75.] and all(near(r['upper_y'],lip_geometry(p,r['x'])[0],1e-5) and near(r['lower_y'],lip_geometry(p,r['x'])[1],1e-5) for r in offsets)
        tests['central_mouth_gap'] &= near(row['central_lip_gap_native_px'],central,1e-5) and near(row['central_lip_gap_bust_px'],.49*central,1e-5)
        evidence.append({'pose': name, 'brows': brow_evidence, 'effective_spread': spread,
                         'added_width_source_px': 40*spread, 'central_gap_source_px': central,
                         'central_gap_bust_px': central*.49, 'corner_upper_offset_source_px': lip_geometry(p,4)[0],
                         'note': 'Split-lip open grin, not exact dental clench. Native visible enamel, mouth seams and likeness still require visual review.'})
    return {'assertions': tests, 'geometry_evidence': evidence}


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
    comparisons = {}
    for other_id in ['EXP-114','EXP-152','EXP-001']:
        other = next(r for r in catalogue['expressions'] if r['id'] == other_id)
        a = other['asset_production']; path = root/a['actual_path']
        with Image.open(path) as image:
            dimensions = list(image.size)
        comparisons[other_id] = {'path': str(path), 'sha256': sha(path),
            'catalogue_sha256': a['sha256'], 'dimensions': dimensions,
            'matches_catalogue': sha(path) == a['sha256'] and dimensions == [a['native_width'],a['native_height']]}
    report['comparison_source_sheets'] = comparisons
    check('three_comparison_source_sheets_match_catalogue', all(r['matches_catalogue'] for r in comparisons.values()))



def compare_profiles(w, freeze, candidate, channels):
    """No visual distinction claim: independently sampled profile trajectories."""
    root = Path(freeze['source_rig'])
    registry = load(root/'expressions/registry.json')
    paths = [root/r['path'].removeprefix('res://') for r in registry['entries']]
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


def frame_order_comparison(features, frame, index):
    """All-frame nearest-face error, explicitly tolerant of indistinguishable holds."""
    dist = np.abs(features-frame).mean(axis=(1, 2, 3))
    best = float(dist.min())
    return {'frame': index, 'expected_face_mae': float(dist[index]),
            'best_face_mae': best, 'expected_minus_best': float(dist[index]-best),
            'best_matching_frame': int(dist.argmin())}


def native_pixel_checks(arrays, receipt_hashes, view, static=None):
    """All-frame identity, holds, fixed body and exact static-anchor comparisons."""
    if len(arrays) != FRAMES or len(receipt_hashes) != FRAMES:
        raise ValueError('Expected exactly 121 pixel arrays and hash receipts')
    shape = (SIZES[view][1], SIZES[view][0], 4)
    if any(a.shape != shape or a.dtype != np.uint8 for a in arrays):
        raise ValueError('Native arrays must have exact RGBA dimensions and uint8 pixels')
    vi = list(SIZES).index(view)
    checks = {}; counts = []; union = np.zeros(shape[:2], dtype=bool)
    for i, ar in enumerate(arrays):
        mask = np.any(ar != arrays[0], axis=2); union |= mask; counts.append(int(mask.sum()))
        checks['rgba_receipt_'+str(i)] = len(receipt_hashes[i]) == 2 and hashlib.sha256(ar.tobytes()).hexdigest() == receipt_hashes[i][vi]
    checks['neutral_holds'] = all(counts[i] == 0 for i in list(range(7))+list(range(111,121)))
    checks['nontrivial_expression'] = max(counts) > 0
    checks['shallow_hold'] = all(np.array_equal(arrays[48], arrays[i]) for i in range(48,61))
    if view == 'full':
        checks['fixed_body_pixels'] = outside_face_unchanged(union)
    if static is not None:
        checks['exact_static_anchor_set'] = set(static) == set(STATIC_FRAMES)
        for name, frame in STATIC_FRAMES.items():
            checks['static_anchor_'+name] = name in static and np.array_equal(static[name], arrays[frame])
    return {'assertions': checks, 'changed_pixels_each_frame': counts,
            'union_difference_bbox_xyxy': bbox(union)}


def video_metadata_checks(probe, pts):
    s = probe['streams'][0]
    return {
        'encoding_duration': s['codec_name'] == 'h264' and s['pix_fmt'] == 'yuv420p' and near(float(probe['format']['duration']), FRAMES/FPS, .002),
        'geometry_count': s['width'] == 968 and s['height'] == 800 and s['r_frame_rate'] == '30/1' and int(s['nb_read_frames']) == FRAMES and int(s['nb_frames']) == FRAMES,
        'all_30fps_pts': len(pts) == FRAMES and all(near(float(r['best_effort_timestamp_time']), i/FPS, 1e-5) for i,r in enumerate(pts)),
    }


def video_similarity_checks(errors, nearest):
    return {
        'complete_comparisons': set(errors) == {'full','detail'} and all(len(a) == FRAMES for a in errors.values()) and len(nearest) == FRAMES,
        'no_material_reorder': bool(nearest) and all(math.isfinite(r['expected_minus_best']) and r['expected_minus_best'] < .10 for r in nearest),
        'same_index_native_similarity': all(a and all(math.isfinite(e) and 0 <= e < 3.0 for e in a) for a in errors.values()) and bool(nearest) and all(math.isfinite(r['expected_face_mae']) and 0 <= r['expected_face_mae'] < 5.0 for r in nearest),
    }


def decode_rgb_frames(video, width, height, result):
    """Fully decode an existing video only. No encoding or renderer is started."""
    with tempfile.TemporaryFile() as err:
        p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', str(video), '-map', '0:v:0', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE, stderr=err)
        count = 0
        try:
            rbytes = width*height*3
            while True:
                buf = p.stdout.read(rbytes)
                if not buf:
                    break
                if len(buf) != rbytes:
                    raise ValueError(f'Incomplete decoded frame {count}: {len(buf)} bytes')
                yield np.frombuffer(buf, np.uint8).reshape(height, width, 3)
                count += 1
            code = p.wait(timeout=60)
        finally:
            if p.poll() is None:
                p.kill(); p.wait()
            p.stdout.close()
        err.seek(0); stderr = err.read().decode(errors='replace')
    result.update(frames=count, exit_code=code, stderr=stderr)


def run(args):
    w = args.work.resolve()
    out = args.output.resolve() if args.output else w/'independent_review_evidence'
    protected = [w/p for p in ['capture', 'motion', 'rig', 'native_launcher', 'development_audit']]
    if out == w or w not in out.parents or any(out == p.resolve() or p.resolve() in out.parents for p in protected):
        raise ValueError('Reviewer output must be a separate directory below WORK, outside all protected input trees')
    out.mkdir(parents=True, exist_ok=True)
    video = args.video.resolve() if args.video else w/'TriumphantGrin_review_v1.mp4'
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
        if sha(w/'review_input_freeze.json') != EXPECTED_INPUT_FREEZE_SHA256:
            raise ValueError('Pinned author contract digest mismatch; refusing changed inputs')
        input_freeze = load(w/'review_input_freeze.json')
        for name, digest in input_freeze['files'].items():
            relative = Path(name)
            if relative.is_absolute() or '..' in relative.parts:
                raise ValueError('Unsafe pinned input path: '+name)
            if not (w/name).is_file() or sha(w/name) != digest:
                raise ValueError('Pinned author input missing or changed: '+name)
        freeze = load(w/'BASELINE_FREEZE.json')
        known = freeze['source_files_sha256']
        roots = [w/'rig', Path(freeze['source_rig'])]
        report.update(baseline=freeze['baseline'], baseline_commit=freeze.get('baseline_commit', freeze.get('published_baseline_commit')),
                      baseline_file_count=len(known), baseline_png_count=sum(p.endswith('.png') for p in known))
        report['frozen_source_changes'] = {str(root): [n for n, h in known.items() if not (root/n).is_file() or sha(root/n) != h] for root in roots}
        check('all_999_pinned_source_files_unchanged_in_both_roots', len(known) == 999 and sum(p.endswith('.png') for p in known) == 184 and not any(report['frozen_source_changes'].values()))
        report['extra_manifest_hash_checks'] = {str(root): {n: (root/n).is_file() and sha(root/n) == h for n, h in freeze['extra_manifests_sha256'].items()} for root in roots}
        check('approved_manifest_unchanged', all(all(v.values()) for v in report['extra_manifest_hash_checks'].values()))
        parity = freeze['published40_runtime_artwork_parity']
        exclusions = {'APPROVED_INTEGRATION_STATUS.json', 'APPROVED_INTEGRATION_TEST_RESULTS.json', 'README.md', 'RELEASE.json', 'expressions/registry.json', 'tools/verify_approved_integration.py'}
        report['published40_runtime_parity_changes'] = [n for n, h in parity['files_sha256'].items() if not (Path(parity['path'])/n).is_file() or sha(Path(parity['path'])/n) != h or known.get(n) != h]
        check('all_993_runtime_artwork_files_match_published40', parity['count'] == len(parity['files_sha256']) == 993 and set(parity['files_sha256']) == set(known)-exclusions and set(parity['excluded_changed_metadata_registry_and_aggregate_guard']) == exclusions and not report['published40_runtime_parity_changes'])
        parity41 = freeze['published41_runtime_artwork_parity']
        report['published41_runtime_parity_changes'] = [n for n,h in parity41['files_sha256'].items() if not (Path(parity41['path'])/n).is_file() or sha(Path(parity41['path'])/n) != h or known.get(n) != h]
        check('all_993_runtime_artwork_files_match_published41', parity41['count'] == len(parity41['files_sha256']) == 993 and set(parity41['files_sha256']) == set(known)-exclusions and set(parity41['excluded_changed_metadata_registry_and_aggregate_guard']) == exclusions and not report['published41_runtime_parity_changes'])
        report['registry_ids'] = {str(root): [e['id'] for e in load(root/'expressions/registry.json')['entries']] for root in roots}
        check('approved36_registry_unchanged_candidate_absent', all(ids == freeze['baseline_profile_ids'] and ID not in ids for ids in report['registry_ids'].values()))
        check('expected_review_input_freeze_identity', sha(w/'review_input_freeze.json') == EXPECTED_INPUT_FREEZE_SHA256)
        input_freeze = load(w/'review_input_freeze.json')
        check('complete_preparation_freeze', input_freeze['candidate'] == ID and len(input_freeze['files']) == 47 and {'EXP-104.json','plan.json','check_and_capture.gd','render_motion.gd','source_guards.py','native_launcher/project.godot','state_checks.json','motion_state_checks.json','SOURCE_REFERENCE.json'} <= set(input_freeze['files']))
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
        candidate = load(w/'EXP-104.json')
        keys = candidate['keyframes']
        check('candidate_id_duration_and_unapproved', candidate['id'] == ID and candidate['duration'] == 4 and candidate['status'].startswith('UNAPPROVED'))
        check('ordered_eleven_timeline_keys', len(keys) == 11 and keys[0]['time'] == 0 and keys[-1]['time'] == 4 and all(b['time'] > a['time'] for a, b in zip(keys, keys[1:])))
        rows = load(w/'plan.json')
        names = [r['name'] for r in rows]
        report['independent_contract_checks'] = contract_checks(candidate, rows)
        check('independent_expression_contract', all(report['independent_contract_checks'].values()))
        check('eight_unique_static_anchors', len(names) == len(set(names)) == 8)
        state = load(w/'state_checks.json')
        motion_state = load(w/'motion_state_checks.json')
        for label, receipt, count in [('static_state', state, 1582), ('motion_state', motion_state, 12646)]:
            check(label+'_receipt_pass', receipt['status'] == 'PASS' and not receipt['failures'] and receipt['checks'] == count and receipt['visual_capture'] is False and receipt['production_registry_unchanged'])
        check('static_record_order', [r['name'] for r in state['records']] == names)
        report['independent_static_geometry'] = static_geometry_checks(rows, state['records'], w/'rig')
        check('independent_static_poses_and_geometry', all(report['independent_static_geometry']['assertions'].values()))
        check('headless_receipts_tied_to_frozen_inputs', state['plan_sha256'] == sha(w/'plan.json') and motion_state['profile_sha256'] == sha(w/'EXP-104.json') and state['baseline_freeze_sha256'] == motion_state['baseline_freeze_sha256'] == sha(w/'BASELINE_FREEZE.json'))
        check('headless_receipts_correct_baseline', all(r['baseline'] == freeze['baseline'] and r['baseline_profile_count'] == 36 for r in [state, motion_state]))
        check('headless_receipts_do_not_invent_native_pixels', motion_state['display'] == 'headless' and not motion_state['renderer'] and all(r['hashes'] == [] for r in motion_state['records']))
        check('headless_lifecycle_receipt', motion_state['lifecycle_assertions'] == 36 and motion_state['lifecycle_interruption_times'] == INTERRUPTIONS)
        expected_channels = set(json.loads((w/'rig/expression_rig.gd').read_text().split('const CHANNELS=', 1)[1].splitlines()[0]))
        check('exact_shared_channel_contract', expected_channels == CHANNELS)
        check('headless_pose_has_exact_shared_channels', all(set(r['pose']) == expected_channels for r in state['records'] + motion_state['records']))
        check('candidate_uses_only_allowed_channels', all(set(k['values']) <= ACTING for k in keys))
        check('eight_anchors_are_exact_key_values', all(any(r['pose'] == k['values'] for k in keys) for r in rows))
        report['independent_profile_comparison'] = compare_profiles(w, freeze, candidate, expected_channels)
        check('independent_36_baseline_profile_nonduplication', report['independent_profile_comparison']['all_distinct'] and report['independent_profile_comparison']['compared_profiles'] == 36)
        report['headless_independent_timeline'] = timeline_checks(motion_state['records'], keys)
        check('headless_independent_timeline_and_intent', all(report['headless_independent_timeline']['assertions'].values()))

        required_static = [w/f'capture/{n}_{v}.png' for n in names for v in ['bust', 'detail']]
        missing_static = [str(p.relative_to(w)) for p in required_static+[w/'capture/checks.json'] if not p.is_file()]
        report['missing_static_inputs'] = missing_static
        static_arrays = {}
        if (w/'capture').is_dir():
            check('no_unexpected_static_pngs', {p.name for p in (w/'capture').glob('*.png')} <= {p.name for p in required_static})
        if (w/'capture/checks.json').is_file():
            receipt = load(w/'capture/checks.json')
            report['static_native_receipt'] = {k: v for k, v in receipt.items() if k != 'records'}
            check('native_static_receipt_pass', receipt['status'] == 'PASS' and not receipt['failures'] and receipt['visual_capture'] is True and receipt['production_registry_unchanged'] and receipt['checks'] == 1614)
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
        for view in SIZES:
            if (w/'motion'/view).is_dir():
                check('no_unexpected_motion_pngs_'+view, {p.name for p in (w/'motion'/view).glob('*.png')} <= {f'{i:04d}.png' for i in range(FRAMES)})
        if (w/'motion_checks.json').is_file():
            motion = load(w/'motion_checks.json')
            report['native_motion_receipt'] = {k: v for k, v in motion.items() if k != 'records'}
            check('native_motion_receipt_pass', motion['checks'] == 13131 and motion['status'] == 'PASS' and not motion['failures'] and motion['visual_capture'] is True and motion['production_registry_unchanged'] and motion['display'] not in ['', 'headless'] and bool(motion['renderer']) and motion['frames'] == FRAMES and motion['fps'] == FPS and motion['duration'] == 4)
            check('native_motion_receipt_tied_to_frozen_inputs', motion['profile_sha256'] == sha(w/'EXP-104.json') and motion['baseline_freeze_sha256'] == sha(w/'BASELINE_FREEZE.json') and motion['baseline'] == freeze['baseline'] and motion['baseline_profile_count'] == 36)
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
            check('sustained_peak_pixels_'+view, all(np.array_equal(arrays[48], arrays[i]) for i in range(48, 61)))
            if view == 'full':
                diffs[view]['all_pixels_outside_face_box_200_270_360_410_unchanged'] = outside_face_unchanged(union)
                check('all_native_body_pixels_fixed', outside_face_unchanged(union))
            if static_arrays:
                for name, i in STATIC_FRAMES.items():
                    check('static_motion_exact_'+view+'_'+name, np.array_equal(static_arrays[view][name], arrays[i]))
            report.setdefault('native_all_frame_checks', {})[view] = native_pixel_checks(arrays, [r['hashes'] for r in motion['records']], view, static_arrays.get(view))
            check('all_frame_pixel_contract_'+view, all(report['native_all_frame_checks'][view]['assertions'].values()))
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
        report['video_metadata_checks'] = video_metadata_checks(probe, pts)
        check('independent_video_metadata', all(report['video_metadata_checks'].values()))
        features = np.asarray([a[55:285, 40:320][::2, ::2].astype(np.float32) for a in arrays_by_view['detail']])
        errors = {'full': [], 'detail': []}; nearest = []; selected = {}; count = 0
        decode_result = {}
        for ar in decode_rgb_frames(video, 968, 800, decode_result):
            if count >= FRAMES:
                raise ValueError('MP4 contains more than 121 decoded frames')
            for view, crop in [('full', ar[:, :568]), ('detail', ar[220:580, 568:968])]:
                errors[view].append(float(np.abs(crop.astype(np.int16)-arrays_by_view[view][count].astype(np.int16)).mean()))
            feat = ar[275:505, 608:888][::2, ::2].astype(np.float32)
            nearest.append(frame_order_comparison(features, feat, count))
            if count in SELECTED:
                selected[count] = ar[220:580, 568:968].copy()
            count += 1
        code, stderr = decode_result['exit_code'], decode_result['stderr']
        report['mp4_full_decode'] = {'frames': count, 'exit_code': code, 'stderr': stderr}
        check('mp4_complete_clean_decode', count == FRAMES and code == 0 and not stderr)
        if not nearest:
            raise ValueError('No video frames available for comparison')
        report['mp4_source_panel_mae'] = {v: {'mean': float(np.mean(a)), 'max': max(a), 'frames': len(a)} for v, a in errors.items()}
        report['mp4_order_checks'] = {'method': 'All decoded frames compared with same-index full/detail native panels and all-frame nearest-face errors; identical and near-identical holds remain ambiguous under lossy encoding.', 'max_expected_face_mae': max(r['expected_face_mae'] for r in nearest), 'max_expected_minus_best_face_mae': max(r['expected_minus_best'] for r in nearest), 'selected': [r for r in nearest if r['frame'] in SELECTED], 'all_frame_detail_file': 'decoded_frame_order.json'}
        write(out/'decoded_frame_order.json', nearest)
        report['video_similarity_checks'] = video_similarity_checks(errors, nearest)
        check('complete_video_similarity_checks', all(report['video_similarity_checks'].values()))
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
    parser.add_argument('--video', type=Path, help='Default: WORK/TriumphantGrin_review_v1.mp4')
    raise SystemExit(run(parser.parse_args()))

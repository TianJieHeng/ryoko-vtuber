#!/usr/bin/env python3
"""Reviewer-owned, read-only EXP-045 evidence audit. No renderer or encoder.

This implementation does not import the author's validators. Its trust root is
the independently recorded author freeze below, not a writable checksum file.
Exit 0 means machine evidence complete, 1 failed, 2 native evidence pending.
Even exit 0 does not constitute visual approval or normal-speed observation.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import tempfile

import numpy as np
from PIL import Image

FROZEN_INPUT = '7f9e1bd006a91ff30d66b6da8231b4cb86e4b0bdd72162d9bc794401e51cc5ae'
FROZEN_PROFILE = '53f59fc53968bc626e0f3ead5e9f66f03e24d06c1a900106e442cc04dc28180d'
FROZEN_SHEET = '5e3287f39ac6102934cfa2001150036345103d398760f738b6f1055c45b7f3ad'
ACTING = {'aversion_px', 'blink_L', 'blink_R', 'brow_screen_left',
          'brow_screen_right', 'brow_tilt_screen_left', 'brow_tilt_screen_right'}
CONFLICTS = {'gaze_x', 'gaze_y', 'gaze_down_extra', 'opening_px', 'eye_smile_L', 'eye_smile_R'}
CHANNELS = set('aversion_px blink_L blink_R blush_intensity brow_inner_lift_screen_left brow_inner_lift_screen_right brow_screen_left brow_screen_right brow_tilt_screen_left brow_tilt_screen_right eye_smile_L eye_smile_R gaze_down_extra gaze_x gaze_y hair_sway mouth_corner_lift mouth_corner_lift_screen_left mouth_corner_lift_screen_right mouth_kiss mouth_lip_press mouth_open mouth_oral_lift mouth_purse mouth_smile mouth_spread mouth_width_screen_left mouth_width_screen_right opening_px uneasy_weight'.split())
INTERRUPTIONS = [.35, .6, 1., 1.6, 2.4, 2.8, 3.2, 3.5, 3.7]
ANCHORS = {'neutral': 0, 'prepare_lids': 18, 'glance': 30, 'side_eye_peak': 48,
           'recover_gaze': 84, 'center_gaze': 96, 'settle': 105, 'neutral_return': 120}
SIZES = {'full': (568, 800), 'detail': (400, 360)}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path):
    # Reject duplicate JSON keys and NaN rather than allowing silent overrides.
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('Duplicate JSON key: '+key)
            result[key] = value
        return result
    def bad(value):
        raise ValueError('Non-finite JSON constant: '+value)
    return json.loads(Path(path).read_text(), object_pairs_hook=pairs, parse_constant=bad)


def require(ok, label):
    if not ok:
        raise ValueError(label)


def near(a, b, tolerance=1e-6):
    return math.isfinite(a) and math.isfinite(b) and abs(a-b) <= tolerance


def smooth(x):
    x = min(1., max(0., x))
    return x*x*(3.-2.*x)


def sample(keys, time, initial=True):
    require(len(keys) >= 2, 'Missing timeline keys')
    for a, b in zip(keys, keys[1:]):
        if time <= b['time']:
            break
    weight = smooth((time-a['time'])/(b['time']-a['time']))
    join = smooth(time/.3) if initial else 1.
    return {k: ((1.-weight)*a['values'].get(k, 0.)+weight*b['values'].get(k, 0.))*join for k in CHANNELS}


def pose_valid(p):
    require(set(p) == CHANNELS, 'Exact shared channel set required')
    require(all(type(v) in (int, float) and math.isfinite(v) for v in p.values()), 'Nonfinite or nonnumeric pose')
    require(all(v == 0 for k, v in p.items() if k not in ACTING), 'Excluded control, including mouth, must remain zero')
    require(0 <= p['aversion_px'] <= 12, 'Aversion source-pixel bounds')
    require(0 <= p['blink_L'] <= .300001 and 0 <= p['blink_R'] <= .380001, 'Unequal lid bounds')
    require(-.650001 <= p['brow_screen_left'] <= 0 and 0 <= p['brow_screen_right'] <= .220001, 'Opposed brow height bounds')
    require(0 <= p['brow_tilt_screen_left'] <= .500001 and -.280001 <= p['brow_tilt_screen_right'] <= 0, 'Opposed brow tilt bounds')
    if p['aversion_px'] > 0:
        require(min(p['blink_L'], p['blink_R']) >= .18, 'Active aversion requires BOTH lids >= .18')
        require(all(p[k] == 0 for k in CONFLICTS), 'Aversion conflicts')


def compare_pose(actual, expected):
    pose_valid(actual)
    require(all(near(actual[k], expected[k]) for k in CHANNELS), 'Pose differs from independent interpolation')
    return max(abs(actual[k]-expected[k]) for k in CHANNELS)


def segment_checks(keys):
    require([k['time'] for k in keys] == [0, .2, .6, 1., 1.6, 2.4, 2.8, 3.2, 3.5, 3.7, 4.], 'Eleven ordered frozen timeline times')
    active_segments = []
    for i, (a, b) in enumerate(zip(keys, keys[1:])):
        require(set(a['values']) <= ACTING and set(b['values']) <= ACTING, 'Unsupported authored controls')
        # Smoothstep is a convex interpolation. Endpoint bounds prove the
        # entire closed segment, including the zero-aversion boundary poses.
        if max(a['values'].get('aversion_px', 0), b['values'].get('aversion_px', 0)) > 0:
            for end in [a, b]:
                require(all(end['values'].get(lid, 0) >= .18 for lid in ['blink_L', 'blink_R']), 'Unsupported adjoining aversion segment endpoint')
                require(all(end['values'].get(k, 0) == 0 for k in CONFLICTS), 'Conflict at adjoining aversion endpoint')
            require(a['time'] >= .3, 'Initial restart blend must finish before aversion onset')
            active_segments.append(i)
        for fraction in [0., 1e-10, .001, .01, .1, .25, .5, .75, .9, .99, .999, 1-1e-10, 1.]:
            pose_valid(sample(keys, a['time']+(b['time']-a['time'])*fraction))
        speed = 1.5*abs(b['values'].get('aversion_px', 0)-a['values'].get('aversion_px', 0))/(30*(b['time']-a['time']))
        require(speed < .9, 'Analytic aversion per-frame derivative bound')
    require(active_segments == [2, 3, 4, 5, 6], 'Expected five supported aversion segments')
    return active_segments


def iris_checks(row):
    require(set(row['iris_geometry']) == {'screen_left', 'screen_right'}, 'Two iris records')
    for side, geo in row['iris_geometry'].items():
        require(set(geo) == {'sprite_delta_source_px', 'iris_shader_offset_source_px'}, 'Iris geometry schema')
        for offset in geo.values():
            require(len(offset) == 2 and near(offset[0], row['pose']['aversion_px'], 1e-4) and offset[1] == 0, 'Actual lateral iris sprite AND shader displacement')


def timeline_checks(records, keys):
    require(len(records) == 121, 'Exactly 121 motion records')
    segment_checks(keys)
    maximum = 0.
    for i, row in enumerate(records):
        require(row['frame'] == i and near(row['time'], i/30., 1e-12), 'Motion frame/time order')
        maximum = max(maximum, compare_pose(row['pose'], sample(keys, i/30.)))
        require(row['central_lip_gap_native_px'] == 0, 'Sealed unmodified mouth gap')
        iris_checks(row)
        if i <= 6 or i >= 111:
            require(all(v == 0 for v in row['pose'].values()), 'Exact neutral hold')
        if i:
            require(all(abs(row['pose'][k]-records[i-1]['pose'][k]) < (.9 if k == 'aversion_px' else .20) for k in ACTING), 'Frame-step bound')
    peak = records[48]['pose']
    require(peak['aversion_px'] == 12 and near(peak['blink_L'], .30) and near(peak['blink_R'], .38), 'Side-eye peak')
    require(all(row['pose'] == peak for row in records[48:73]), 'Sustained exact peak')
    for i in [18, 96]:
        p = records[i]['pose']
        require(p['aversion_px'] == 0 and min(p['blink_L'], p['blink_R']) >= .18, 'Lids lead and outlast aversion')
    require(all(records[i]['pose']['aversion_px'] >= records[i-1]['pose']['aversion_px'] for i in range(1, 49)), 'Monotone onset')
    require(all(records[i]['pose']['aversion_px'] <= records[i-1]['pose']['aversion_px'] for i in range(73, 121)), 'Monotone recovery')
    return {'samples': 121, 'maximum_control_error': maximum, 'supported_aversion_segments': [2, 3, 4, 5, 6]}


def lifecycle_pose(keys, interruption, stage, elapsed):
    source = sample(keys, interruption)
    target = sample(keys, elapsed, initial=False) if stage == 'restart' else dict.fromkeys(CHANNELS, 0.)
    duration = .3 if stage == 'restart' else .45
    if source['aversion_px'] > 0 and elapsed < duration:
        if elapsed < duration/2:
            result = source.copy()
            result['aversion_px'] *= 1.-smooth(elapsed/(duration/2))
            return result
        w = smooth((elapsed-duration/2)/(duration/2))
        result = {k: source[k]*(1-w)+target[k]*w for k in CHANNELS}
        result['aversion_px'] = target['aversion_px']*w
        return result
    w = smooth(elapsed/duration)
    return {k: source[k]*(1-w)+target[k]*w for k in CHANNELS}


def lifecycle_checks(receipt, keys):
    require(receipt['lifecycle_interruption_times'] == INTERRUPTIONS and receipt['lifecycle_assertions'] == 36, 'Lifecycle interruptions and assertion count')
    rows = receipt['lifecycle_scoped_samples']
    expected = [(t, stage, j) for t in INTERRUPTIONS for stage, count in [('restart', 12), ('release', 16)] for j in range(1, count+1)]
    require([(r['interruption_time'], r['stage'], r['step']) for r in rows] == expected, 'All 252 lifecycle records in exact order')
    maximum = 0.
    for r in rows:
        maximum = max(maximum, compare_pose(r['pose'], lifecycle_pose(keys, r['interruption_time'], r['stage'], r['step']/30.)))
        if r['stage'] == 'release' and r['step'] == 16:
            require(all(v == 0 for v in r['pose'].values()), 'Release exact neutral')
    # Probe either side of the scoped handoff boundary, separately from the
    # recorded 30 Hz grid. Read source establishes the analytic two-stage rule:
    # retain ordinary lids while clearing aversion, then release ordinary lids.
    dense = 0
    for t in INTERRUPTIONS:
        for stage, duration in [('restart', .3), ('release', .45)]:
            for f in [0, 1e-10, .001, .1, .25, .4999999999, .5, .5000000001, .75, .999, 1, 1.1]:
                pose_valid(lifecycle_pose(keys, t, stage, duration*f))
                dense += 1
    return {'samples': len(rows), 'boundary_model_samples': dense, 'maximum_control_error': maximum,
            'continuous_support_proof': 'Frozen scoped_handoff retains both valid source lids until aversion is exactly zero, then blends ordinary controls. Restart target through .3 seconds has zero aversion and all conflicts zero.'}


def static_checks(rows, plan):
    require([r['name'] for r in rows] == list(ANCHORS), 'Eight static records in order')
    require([r['name'] for r in plan] == list(ANCHORS), 'Eight plan entries in order')
    for row, anchor in zip(rows, plan):
        p = row['pose']
        compare_pose(p, {k: anchor['pose'].get(k, 0) for k in CHANNELS})
        iris_checks(row)
        for side, lid in [('screen_left', 'blink_R'), ('screen_right', 'blink_L')]:
            b = row['brow_geometry'][side]
            require(b['inner_lift'] == 0 and near(b['rotation_degrees'], 8*p['brow_tilt_'+side]), 'Rigid opposed brow rotations')
            require(b['pivot_delta_source_px'][0] == 0 and near(b['pivot_delta_source_px'][1], -10*p['brow_'+side], 1e-4), 'Rigid brow translations')
            l = row['lash_geometry'][side]
            require(near(l['closure'], p[lid]) and l['pivot_delta_source_px'][0] == 0 and near(l['pivot_delta_source_px'][1], 36*p[lid], 1e-4), 'Character/screen lid mapping and travel')
        require(row['actual_mouth_side_delta_source_px'] == [0, 0] and row['central_lip_gap_native_px'] == row['central_lip_gap_bust_px'] == 0, 'Unmodified mouth geometry')
        require([r['x'] for r in row['lip_contour_offsets']] == [4, 39.5, 75] and all(r['upper_y'] == r['lower_y'] == 0 for r in row['lip_contour_offsets']), 'No invented downward or upward lip corner')


def pinned_checks(work):
    require(sha(work/'review_input_freeze.json') == FROZEN_INPUT, 'Independent hardcoded freeze pin mismatch')
    require((work/'REVIEW_FREEZE.sha256').read_text() == FROZEN_INPUT+'  review_input_freeze.json\n', 'Author checksum receipt changed')
    freeze = load(work/'review_input_freeze.json')
    require(freeze['candidate'] == 'EXP-045' and len(freeze['files']) == 38, '38 author input files required')
    for name, digest in freeze['files'].items():
        require(sha(work/name) == digest, 'Author input changed: '+name)
    require(sha(work/'EXP-045.json') == FROZEN_PROFILE, 'Independent candidate pin mismatch')
    return freeze


def source_checks(work):
    baseline = load(work/'BASELINE_FREEZE.json')
    known = baseline['source_files_sha256']
    require(len(known) == 999 and sum(n.endswith('.png') for n in known) == 184, '999 source files / 184 PNGs')
    require(baseline['published_baseline_commit'] == '3ce98774282ad6c20dfbd7018d20838ff861b762', 'Baseline commit')
    for root in [Path(baseline['source_rig']), work/'rig', work/'native_launcher']:
        for name, digest in {**known, **baseline['extra_manifests_sha256']}.items():
            if root == work/'native_launcher' and name == 'project.godot':
                continue
            require(sha(root/name) == digest, 'Frozen source changed: '+str(root/name))
        ids = [r['id'] for r in load(root/'expressions/registry.json')['entries']]
        require(ids == baseline['baseline_profile_ids'] and len(ids) == 36 and 'EXP-045' not in ids, 'Production registry changed')
    parity = baseline['published41_runtime_artwork_parity']
    exclusions = {'APPROVED_INTEGRATION_STATUS.json', 'APPROVED_INTEGRATION_TEST_RESULTS.json', 'README.md', 'RELEASE.json', 'expressions/registry.json', 'tools/verify_approved_integration.py'}
    require(parity['count'] == len(parity['files_sha256']) == 993 and set(parity['files_sha256']) == set(known)-exclusions, '993 parity file coverage')
    require(set(parity['excluded_changed_metadata_registry_and_aggregate_guard']) == exclusions, 'Parity exclusion scope')
    for name, digest in parity['files_sha256'].items():
        require(sha(Path(parity['path'])/name) == known[name] == digest, 'Approved41 runtime/artwork parity')
    ref = load(work/'SOURCE_REFERENCE.json')
    require(sha(Path(ref['sheet'])) == ref['sha256'] == baseline['source_sheet_sha256'] == FROZEN_SHEET, 'Actual source sheet hash')
    require(sha(Path(baseline['source_catalogue'])) == baseline['catalogue_sha256'], 'Catalogue hash')
    catalogue = load(baseline['source_catalogue'])
    entry = load(work/'SOURCE_CATALOGUE_ENTRY.json')
    require([r for r in catalogue['expressions'] if r['id'] == 'EXP-045'] == [entry], 'Exact catalogue entry')
    panels = entry['key_pose_sequence']
    require(len(panels) == len(ref['panel_hashes']) == 9, 'Nine source panels')
    root = Path(baseline['source_catalogue']).parent.parent
    with Image.open(ref['sheet']) as sheet:
        require(sheet.size == (1159, 1358) and ref['dimensions'] == [1159, 1358], 'Source dimensions')
        for panel in panels:
            name = panel['actual_panel_path']
            require(sha(root/name) == panel['sha256'] == ref['panel_hashes'][name], 'Source panel hash')
            with Image.open(root/name) as crop:
                expected = sheet.crop(panel['crop_bounds_xyxy']).convert('RGBA')
                require(crop.size == expected.size and crop.convert('RGBA').tobytes() == expected.tobytes(), 'Lossless source panel crop')
    return {'baseline_files_each_root': 999, 'pngs_each_root': 184, 'runtime_parity': 993, 'exact_source_crops': 9}


def distinctness_checks(work, candidate):
    receipt = load(work/'DISTINCTNESS_CHECK.json')
    require(len(receipt['comparisons']) == receipt['compared_profiles'] == 43, '43 comparison profiles')
    results = []
    ids = set()
    own_samples = [sample(candidate['keyframes'], 4*i/120) for i in range(121)]
    for r in receipt['comparisons']:
        path = Path(r['path'])
        require(sha(path) == r['sha256'], 'Comparison input changed: '+str(path))
        other = load(path)
        require(other['id'] == r['id'] and r['id'] not in ids, 'Comparison ID mismatch or duplicate')
        ids.add(r['id'])
        other_samples = [sample(other['keyframes'], other['duration']*i/120) for i in range(121)]
        differences = [abs(a[k]-b[k]) for a, b in zip(own_samples, other_samples) for k in sorted(CHANNELS)]
        maximum = max(differences)
        rms = math.sqrt(sum(d*d for d in differences)/len(differences))
        require(maximum > .01, 'Numerically duplicate profile: '+r['id'])
        require(near(maximum, r['max_control_difference_at_normalized_time'], 1e-9) and near(rms, r['rms_control_difference'], 1e-9), 'Distinctness receipt disagrees with independent sampling')
        results.append({'id': r['id'], 'maximum': maximum, 'rms': rms})
    require({'EXP-042', 'EXP-081', 'EXP-144'} <= ids, 'Required nearby expressions absent')
    return {'count': len(results), 'comparisons': results, 'perceptual_distinctness': 'NOT ESTABLISHED'}


def common_receipt(receipt, work, native, motion):
    require(receipt['status'] == 'PASS' and receipt['failures'] == [] and receipt['production_registry_unchanged'] is True, 'Receipt must pass with preserved registry')
    require(receipt['visual_capture'] is native, 'Headless/native evidence mismatch')
    require(receipt['baseline'] == 'approved36' and receipt['baseline_profile_count'] == 36 and receipt['baseline_freeze_sha256'] == sha(work/'BASELINE_FREEZE.json'), 'Receipt baseline identity')
    input_name = 'EXP-045.json' if motion else 'plan.json'
    require(receipt['profile_sha256' if motion else 'plan_sha256'] == sha(work/input_name), 'Receipt input identity')
    require(receipt['checks'] == ((13186 if native else 12701) if motion else (1614 if native else 1582)), 'Receipt assertion count')
    if motion:
        require(receipt['frames'] == 121 and receipt['fps'] == 30 and receipt['duration'] == 4, 'Motion dimensions in time')
        require(receipt['approval'] == 'UNAPPROVED' and receipt['normal_speed_observed'] is False, 'No invented review claim')
        require(bool(receipt['renderer']) and receipt['display'] not in ['', 'headless'] if native else receipt['display'] == 'headless' and not receipt['renderer'], 'Native display/renderer identity')
        require(all(len(r['hashes']) == (2 if native else 0) for r in receipt['records']), 'Every frame needs two native hashes, none headless')


def read_png(path, size):
    with Image.open(path) as im:
        require(im.size == size and im.mode == 'RGBA', 'PNG must have exact native dimensions and RGBA mode: '+str(path))
        im.load()
        return np.asarray(im).copy()


def body_unchanged(mask):
    return not (mask[:270].any() or mask[410:].any() or mask[:, :200].any() or mask[:, 360:].any())


def pixels_checks(arrays, view):
    require(len(arrays) == 121, '121 native image arrays')
    diffs = [np.any(ar != arrays[0], axis=2) for ar in arrays]
    require(all(not diffs[i].any() for i in list(range(7))+list(range(111, 121))), 'Pixel-exact neutral holds')
    require(any(d.any() for d in diffs), 'Nontrivial expression pixels required')
    require(all(np.array_equal(arrays[i], arrays[48]) for i in range(48, 73)), 'Pixel-exact peak hold')
    if view == 'full':
        require(all(body_unchanged(m) for m in diffs), 'Body/head/background pixels outside face changed')
    return [int(d.sum()) for d in diffs]


def video_probe_checks(probe, timestamps):
    require(len(probe['streams']) == 1, 'One selected video stream')
    s = probe['streams'][0]
    require(s['codec_name'] == 'h264' and s['pix_fmt'] == 'yuv420p' and (s['width'], s['height']) == (968, 800), 'MP4 codec/layout')
    require(s['r_frame_rate'] == '30/1' and int(s['nb_read_frames']) == int(s['nb_frames']) == 121, 'MP4 frame rate/count')
    require(abs(float(probe['format']['duration'])-121/30) < .002, 'MP4 duration')
    require(len(timestamps) == 121 and all(abs(float(r['best_effort_timestamp_time'])-i/30) < 1e-5 for i, r in enumerate(timestamps)), 'Every MP4 presentation timestamp in order')


def decoded_frame_checks(decoded, i, arrays, features):
    require(decoded.shape == (800, 968, 3), 'Decoded MP4 dimensions')
    errors = {}
    for view, crop in [('full', decoded[:, :568]), ('detail', decoded[220:580, 568:968])]:
        errors[view] = float(np.abs(crop.astype(np.int16)-arrays[view][i][:, :, :3].astype(np.int16)).mean())
        require(errors[view] < 3., 'Decoded same-index native panel mismatch')
    feature = decoded[275:505, 608:888][::2, ::2].astype(np.float32)
    distances = np.abs(features-feature).mean(axis=(1, 2, 3))
    require(distances[i] < 5. and distances[i]-distances.min() < .10, 'Material MP4 frame reorder or wrong face')
    return {'frame': i, 'full_mae': errors['full'], 'detail_mae': errors['detail'], 'expected_face_mae': float(distances[i]), 'expected_minus_best': float(distances[i]-distances.min()), 'nearest': int(distances.argmin())}


def decode_video(path, arrays):
    probe = load_subprocess(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_frames', '-show_entries', 'stream=codec_name,width,height,pix_fmt,r_frame_rate,nb_frames,nb_read_frames:format=duration', '-of', 'json', str(path)])
    pts = load_subprocess(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'frame=best_effort_timestamp_time', '-of', 'json', str(path)])['frames']
    video_probe_checks(probe, pts)
    features = np.asarray([ar[55:285, 40:320, :3][::2, ::2].astype(np.float32) for ar in arrays['detail']])
    rows = []
    with tempfile.TemporaryFile() as stderr:
        process = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:v:0', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE, stderr=stderr)
        try:
            while True:
                buf = process.stdout.read(968*800*3)
                if not buf:
                    break
                require(len(buf) == 968*800*3 and len(rows) < 121, 'Truncated or extra decoded MP4 frame')
                decoded = np.frombuffer(buf, dtype=np.uint8).reshape(800, 968, 3)
                rows.append(decoded_frame_checks(decoded, len(rows), arrays, features))
            code = process.wait(timeout=60)
        finally:
            if process.poll() is None:
                process.kill()
                process.wait()
            process.stdout.close()
        stderr.seek(0)
        error = stderr.read().decode(errors='replace')
    require(len(rows) == 121 and code == 0 and not error, 'Complete clean 121-frame MP4 decode required')
    return {'sha256': sha(path), 'probe': probe, 'decoded_frames': len(rows), 'all_frame_order': rows,
            'order_limit': 'Visually identical or near-identical frames cannot be ordered uniquely after lossy encoding; same-index similarity and timestamps remain mandatory.'}


def load_subprocess(args):
    return json.loads(subprocess.check_output(args, timeout=120))


def native_checks(work, static, motion, candidate, report):
    receipts = {}
    for label, path in [('static', work/'capture/checks.json'), ('motion', work/'motion_checks.json')]:
        if not path.is_file():
            report['pending'].append('Missing native '+label+' receipt')
            continue
        receipts[label] = load(path)
        common_receipt(receipts[label], work, True, label == 'motion')
        report['native_hashes'].append({'path': str(path.relative_to(work)), 'sha256': sha(path)})
        if label == 'static':
            require(receipts[label]['records'] == static['records'], 'All native static geometry/poses equal frozen headless evidence')
            static_checks(receipts[label]['records'], load(work/'plan.json'))
        else:
            n = receipts[label]
            timeline_checks(n['records'], candidate['keyframes'])
            lifecycle_checks(n, candidate['keyframes'])
            require(n['lifecycle_scoped_samples'] == motion['lifecycle_scoped_samples'], 'Native full lifecycle poses differ')
            for a, b in zip(n['records'], motion['records']):
                require({k: v for k, v in a.items() if k != 'hashes'} == {k: v for k, v in b.items() if k != 'hashes'}, 'Native full motion geometry/poses differ')
    static_arrays, motion_arrays = {}, {}
    for view, size in SIZES.items():
        suffix = 'bust' if view == 'full' else 'detail'
        desired = {f'{name}_{suffix}.png' for name in ANCHORS}
        actual = {p.name for p in (work/'capture').glob('*_'+suffix+'.png')}
        require(actual <= desired, 'Unexpected native static filenames')
        static_arrays[view] = {}
        for name in ANCHORS:
            path = work/f'capture/{name}_{suffix}.png'
            if path.is_file():
                ar = read_png(path, size)
                static_arrays[view][name] = ar
                report['native_hashes'].append({'path': str(path.relative_to(work)), 'sha256': sha(path), 'rgba_sha256': hashlib.sha256(ar.tobytes()).hexdigest()})
        if actual != desired:
            report['pending'].append(f'Missing {len(desired-actual)} native static {view} PNGs')
        path_root = work/'motion'/view
        desired_motion = {f'{i:04d}.png' for i in range(121)}
        actual_motion = {p.name for p in path_root.glob('*.png')}
        require(actual_motion <= desired_motion, 'Unexpected motion PNG filename/order')
        arrays = []
        for i in range(121):
            path = path_root/f'{i:04d}.png'
            if not path.is_file():
                continue
            ar = read_png(path, size)
            raw = hashlib.sha256(ar.tobytes()).hexdigest()
            report['native_hashes'].append({'path': str(path.relative_to(work)), 'sha256': sha(path), 'rgba_sha256': raw})
            if 'motion' in receipts:
                require(receipts['motion']['records'][i]['hashes'][0 if view == 'full' else 1] == raw, 'Native per-frame RGBA hash mismatch')
            arrays.append(ar)
        if actual_motion != desired_motion:
            report['pending'].append(f'Missing {len(desired_motion-actual_motion)} native motion {view} PNGs')
        else:
            report['native_pixels'][view] = pixels_checks(arrays, view)
            for name, ar in static_arrays[view].items():
                require(np.array_equal(ar, arrays[ANCHORS[name]]), 'Static anchor/motion pixel mismatch')
            motion_arrays[view] = arrays
        if len(static_arrays[view]) == 8:
            rows = static_arrays[view]
            require(np.array_equal(rows['neutral'], rows['neutral_return']), 'Static neutral bookends')
            require(any(not np.array_equal(rows['neutral'], ar) for ar in rows.values()), 'Static expression must change pixels')
            if view == 'full':
                require(all(body_unchanged(np.any(ar != rows['neutral'], axis=2)) for ar in rows.values()), 'Static body pixels changed')
    require({p.name for p in (work/'capture').glob('*.png')} <= {f'{n}_{v}.png' for n in ANCHORS for v in ['bust', 'detail']}, 'Unexpected static capture PNG')
    video = work/'Irritated_side_eye_review_v1.mp4'
    if not video.is_file():
        report['pending'].append('Native review MP4 absent; full decode not run')
    elif set(motion_arrays) != set(SIZES) or set(receipts) != {'static', 'motion'}:
        report['pending'].append('MP4 present but native inputs incomplete; full decode comparison pending')
    else:
        report['video'] = decode_video(video, motion_arrays)


def run(work, output):
    report = {'candidate': 'EXP-045', 'approval': 'UNAPPROVED', 'independent_freeze_pin': FROZEN_INPUT,
              'normal_speed_observation': False, 'visual_fidelity_pass': False,
              'checks': {}, 'failures': [], 'pending': [], 'native_hashes': [], 'native_pixels': {}}
    try:
        pinned_checks(work)
        report['checks']['pinned_38_author_inputs'] = True
        report['source'] = source_checks(work)
        report['checks']['all_source_hashes_and_crops'] = True
        candidate = load(work/'EXP-045.json')
        require(candidate['id'] == 'EXP-045' and candidate['duration'] == 4 and candidate['status'].startswith('UNAPPROVED'), 'Candidate identity and status')
        static, motion = load(work/'state_checks.json'), load(work/'motion_state_checks.json')
        common_receipt(static, work, False, False)
        common_receipt(motion, work, False, True)
        static_checks(static['records'], load(work/'plan.json'))
        report['checks']['all_static_pose_and_geometry'] = True
        report['timeline'] = timeline_checks(motion['records'], candidate['keyframes'])
        report['lifecycle'] = lifecycle_checks(motion, candidate['keyframes'])
        report['checks']['timeline_and_continuous_lifecycle_support'] = True
        report['distinctness'] = distinctness_checks(work, candidate)
        report['checks']['independent_43_profile_numeric_distinctness'] = True
        native_checks(work, static, motion, candidate, report)
    except Exception as exc:
        report['failures'].append(type(exc).__name__+': '+str(exc))
    report['status'] = 'FAIL' if report['failures'] else 'PENDING' if report['pending'] else 'PASS_MACHINE_EVIDENCE_ONLY'
    report['native_evidence_complete'] = not report['failures'] and not report['pending']
    output.mkdir(parents=True, exist_ok=True)
    (output/'independent_review_checks.json').write_text(json.dumps(report, indent=2, allow_nan=False)+'\n')
    print(json.dumps({k: report[k] for k in ['status', 'approval', 'checks', 'failures', 'pending']}, indent=2))
    return 1 if report['failures'] else 2 if report['pending'] else 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    raise SystemExit(run(args.work.resolve(), (args.output or args.work/'independent_review_evidence').resolve()))

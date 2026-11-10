#!/usr/bin/env python3
"""Read-only EXP061 evidence validator, adapted from EXP129 review_validation.py.

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

ID = 'EXP-061'
FRAMES = 121
FPS = 30
ACTING = {'brow_screen_left', 'brow_screen_right', 'opening_px',
          'mouth_open', 'mouth_purse', 'mouth_lip_press'}
SIZES = {'full': (568, 800), 'detail': (400, 360)}
SELECTED = [0, 15, 27, 41, 55, 70, 86, 111, 120]
STATIC_FRAMES = {'neutral': 0, 'notice': 15, 'rise': 27,
                 'broad_surprise': 41, 'neutral_return': 120}


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
    tests = {
        'independent_smoothstep_timeline': max(errors) < 1e-6,
        'only_six_allowed_channels_act': all(v == 0 for p in poses for k, v in p.items() if k not in ACTING),
        'symmetric_whole_brows': all(p['brow_screen_left'] == p['brow_screen_right'] for p in poses),
        'slow_notice': poses[15]['mouth_open'] < .09,
        'whole_brows_peak': poses[41]['brow_screen_left'] > .999,
        'peak_opening_and_purse': poses[41]['mouth_open'] > .949 and poses[41]['mouth_purse'] < .321,
        'sustained_broad_aperture': poses[55]['mouth_open'] > .949 and poses[70]['mouth_open'] > .85,
        'no_smile_or_spread': all(p['mouth_smile'] == p['mouth_spread'] == 0 for p in poses),
        'no_inner_only_brow_lift': all(p['brow_inner_lift_screen_left'] == p['brow_inner_lift_screen_right'] == 0 for p in poses),
        'bounded_upper_opening': all(0 <= p['opening_px'] <= 4 for p in poses),
        'neutral_hold_states': all(v == 0 for r in records if r['time'] <= .2 or r['time'] >= 3.7 for v in r['pose'].values()),
        'bounded_frame_steps': all(abs(poses[i][k]-poses[i-1][k]) < .25 for i in range(1, FRAMES) for k in ACTING),
    }
    return {'max_smoothstep_control_error': max(errors), 'assertions': tests}


def run(args):
    w = args.work.resolve()
    out = args.output.resolve() if args.output else w/'review_evidence'
    out.mkdir(parents=True, exist_ok=True)
    video = args.video.resolve() if args.video else w/'Broad_surprise_review_v1.mp4'
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
        check('all_999_pinned_source_files_unchanged_in_both_roots', len(known) == 999 and not any(report['frozen_source_changes'].values()))
        report['extra_manifest_hash_checks'] = {str(root): {n: (root/n).is_file() and sha(root/n) == h for n, h in freeze['extra_manifests_sha256'].items()} for root in roots}
        check('approved_manifest_unchanged', all(all(v.values()) for v in report['extra_manifest_hash_checks'].values()))
        report['registry_ids'] = {str(root): [e['id'] for e in load(root/'expressions/registry.json')['entries']] for root in roots}
        check('approved36_registry_unchanged_candidate_absent', all(ids == freeze['baseline_profile_ids'] and ID not in ids for ids in report['registry_ids'].values()))
        input_freeze = load(w/'review_input_freeze.json')
        report['review_input_changes'] = [n for n, h in input_freeze['sha256'].items() if not (w/n).is_file() or sha(w/n) != h]
        check('reviewed_candidate_and_capture_inputs_unchanged', not report['review_input_changes'])
        launcher = w/'native_launcher'
        report['launcher_pinned_changes'] = [n for n, h in known.items() if not (launcher/n).is_file() or sha(launcher/n) != h]
        check('launcher_only_expected_project_override', report['launcher_pinned_changes'] == ['project.godot'])
        # The prepared launcher copies pinned runtime files, not extra audit manifests.
        report['launcher_extra_manifests'] = {n: ('matching' if sha(launcher/n) == h else 'MISMATCH') if (launcher/n).is_file() else 'not copied by launcher preparation; verified in source and rig' for n, h in freeze['extra_manifests_sha256'].items()}
        check('launcher_present_extra_manifests_match', all(v != 'MISMATCH' for v in report['launcher_extra_manifests'].values()))
        ref = load(w/'SOURCE_REFERENCE.json')
        check('source_sheet_hash', sha(Path(ref['sheet'])) == ref['sha256'] == freeze['source_sheet_sha256'])
        check('source_catalogue_hash', sha(Path(freeze['source_catalogue'])) == freeze['catalogue_sha256'])
        with Image.open(ref['sheet']) as im:
            check('source_sheet_dimensions', im.size == (1254, 1254))
        candidate = load(w/'EXP-061.json')
        keys = candidate['keyframes']
        check('candidate_id_duration_and_unapproved', candidate['id'] == ID and candidate['duration'] == 4 and candidate['status'].startswith('UNAPPROVED'))
        check('ordered_eleven_timeline_keys', len(keys) == 11 and keys[0]['time'] == 0 and keys[-1]['time'] == 4 and all(b['time'] > a['time'] for a, b in zip(keys, keys[1:])))
        rows = load(w/'plan.json')
        names = [r['name'] for r in rows]
        check('eight_unique_static_anchors', len(names) == len(set(names)) == 8)
        state = load(w/'state_checks.json')
        motion_state = load(w/'motion_state_checks.json')
        for label, receipt, count in [('static_state', state, 838), ('motion_state', motion_state, 9023)]:
            check(label+'_receipt_pass', receipt['status'] == 'PASS' and not receipt['failures'] and receipt['checks'] == count and receipt['visual_capture'] is False and receipt['production_registry_unchanged'])
        check('static_record_order', [r['name'] for r in state['records']] == names)
        geometry_checks = []
        for plan, r in zip(rows, state['records']):
            geometry_checks.append(all(abs(v-plan['pose'].get(k, 0)) < 1e-6 for k, v in r['pose'].items()))
            for side in ['screen_left', 'screen_right']:
                g = r['brow_geometry'][side]
                geometry_checks.append(abs(g['pivot_delta_source_px'][0]) < 1e-6 and abs(g['pivot_delta_source_px'][1]+10*plan['pose'].get('brow_'+side, 0)) < 1e-6 and g['rotation_degrees'] == 0)
            p = r['pose']
            gap = max(0., p['mouth_open']*.55*54 - 1.5*p['mouth_purse']*min(p['mouth_open']*4, 1))
            geometry_checks.append(abs(r['central_lip_gap_native_px']-gap) < 1e-6 and abs(r['central_lip_gap_bust_px']-gap*.49) < 1e-6 and r['upper_opening_native_px'] == p['opening_px'])
        check('independent_static_poses_and_geometry', all(geometry_checks))
        report['headless_independent_timeline'] = timeline_checks(motion_state['records'], keys)
        check('headless_independent_timeline_and_intent', all(report['headless_independent_timeline']['assertions'].values()))

        required_static = [w/f'capture/{n}_{v}.png' for n in names for v in ['bust', 'detail']]
        missing_static = [str(p.relative_to(w)) for p in required_static+[w/'capture/checks.json'] if not p.is_file()]
        report['missing_static_inputs'] = missing_static
        static_arrays = {}
        if missing_static:
            report['pending'].append('Native static capture incomplete: '+str(len(missing_static))+' required files missing.')
        else:
            receipt = load(w/'capture/checks.json')
            report['static_native_receipt'] = {k: v for k, v in receipt.items() if k != 'records'}
            check('native_static_receipt_pass', receipt['status'] == 'PASS' and not receipt['failures'] and receipt['visual_capture'] and receipt['production_registry_unchanged'])
            check('native_static_records_equal_headless', receipt['records'] == state['records'])
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
            sheet = Image.new('RGB', (1600, 800), (32, 34, 36)); draw = ImageDraw.Draw(sheet)
            for j, n in enumerate(names):
                x, y = (j%4)*400, (j//4)*400
                sheet.paste(Image.fromarray(static_arrays['detail'][n]).convert('RGB'), (x, y+30))
                draw.text((x+10, y+8), n, fill='white')
            sheet.save(out/'static_faces.png')

        required_motion = [w/f'motion/{view}/{i:04d}.png' for view in SIZES for i in range(FRAMES)]
        missing_motion = [str(p.relative_to(w)) for p in required_motion+[w/'motion_checks.json'] if not p.is_file()]
        report['missing_motion_inputs'] = missing_motion
        if missing_motion:
            report['pending'].append('Native motion capture incomplete: '+str(len(missing_motion))+' required files missing.')
            if not video.is_file():
                report['pending'].append('Review MP4 absent; decode/order checks not run.')
            else:
                report['pending'].append('Review MP4 exists but cannot be checked against incomplete native frames.')
            return finish()

        motion = load(w/'motion_checks.json')
        report['native_motion_receipt'] = {k: v for k, v in motion.items() if k != 'records'}
        check('native_motion_receipt_pass', motion['status'] == 'PASS' and not motion['failures'] and motion['visual_capture'] and motion['production_registry_unchanged'] and motion['display'] not in ['', 'headless'] and bool(motion['renderer']) and motion['frames'] == FRAMES and motion['fps'] == FPS and motion['duration'] == 4)
        report['native_independent_timeline'] = timeline_checks(motion['records'], keys)
        check('native_independent_timeline_and_intent', all(report['native_independent_timeline']['assertions'].values()))
        check('all_native_poses_match_headless', [r['pose'] for r in motion['records']] == [r['pose'] for r in motion_state['records']])
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
            check('sustained_peak_pixels_'+view, np.array_equal(arrays[41], arrays[55]))
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
        for j, i in enumerate([0, 27, 41, 70]):
            sheet.paste(Image.fromarray(arrays_by_view['full'][i]), (568*j, 30)); draw.text((568*j+12, 9), f'Native frame {i:03d} | {i/FPS:.3f} s', fill='white')
        sheet.save(out/'bust_progression.png')
    except Exception as exc:
        report['failures'].append(f'{type(exc).__name__}: {exc}')
    return finish()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--video', type=Path, help='Default: WORK/Broad_surprise_review_v1.mp4')
    raise SystemExit(run(parser.parse_args()))

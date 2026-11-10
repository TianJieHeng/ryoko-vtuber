"""Reviewer-owned mutation tests. Synthetic pixels never count as native evidence."""
import copy
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest import mock

import numpy as np
from PIL import Image
import independent_review_validation as v

WORK = Path(__file__).resolve().parent


class NumericalTests(unittest.TestCase):
    def setUp(self):
        self.profile = v.load(WORK/'EXP-045.json')
        self.keys = self.profile['keyframes']
        self.motion = v.load(WORK/'motion_state_checks.json')
        self.static = v.load(WORK/'state_checks.json')
        self.plan = v.load(WORK/'plan.json')

    def test_frozen_preparation_passes(self):
        v.pinned_checks(WORK)
        v.static_checks(self.static['records'], self.plan)
        v.timeline_checks(self.motion['records'], self.keys)
        v.lifecycle_checks(self.motion, self.keys)

    def test_entrance_zero_aversion_endpoint_still_needs_both_lids(self):
        self.keys[2]['values']['blink_L'] = .179
        with self.assertRaisesRegex(ValueError, 'adjoining'):
            v.segment_checks(self.keys)

    def test_exit_zero_aversion_endpoint_still_needs_both_lids(self):
        self.keys[7]['values']['blink_R'] = .179
        with self.assertRaisesRegex(ValueError, 'adjoining'):
            v.segment_checks(self.keys)

    def test_conflict_at_zero_aversion_exit_rejected(self):
        self.keys[7]['values']['gaze_x'] = .1
        with self.assertRaises(ValueError):
            v.segment_checks(self.keys)

    def test_one_supported_lid_not_enough(self):
        p = self.motion['records'][48]['pose']
        p['blink_L'] = .17
        with self.assertRaisesRegex(ValueError, 'BOTH'):
            v.pose_valid(p)

    def test_negative_aversion_rejected(self):
        p = self.motion['records'][48]['pose']
        p['aversion_px'] = -12
        with self.assertRaises(ValueError):
            v.pose_valid(p)

    def test_nonfinite_pose_rejected(self):
        self.motion['records'][12]['pose']['blink_R'] = float('nan')
        with self.assertRaises(ValueError):
            v.timeline_checks(self.motion['records'], self.keys)

    def test_missing_or_extra_channel_rejected(self):
        p = self.motion['records'][48]['pose']
        p['invented_corner_down'] = .5
        with self.assertRaisesRegex(ValueError, 'channel'):
            v.pose_valid(p)

    def test_all_excluded_channels_rejected(self):
        for k in v.CHANNELS-v.ACTING:
            with self.subTest(channel=k):
                p = self.motion['records'][48]['pose'].copy()
                p[k] = .01
                with self.assertRaises(ValueError):
                    v.pose_valid(p)

    def test_timeline_pose_mutation_rejected(self):
        self.motion['records'][20]['pose']['brow_screen_left'] = -.3
        with self.assertRaisesRegex(ValueError, 'interpolation'):
            v.timeline_checks(self.motion['records'], self.keys)

    def test_frame_reorder_rejected(self):
        r = self.motion['records']
        r[21], r[22] = r[22], r[21]
        with self.assertRaisesRegex(ValueError, 'order'):
            v.timeline_checks(r, self.keys)

    def test_nonzero_neutral_rejected(self):
        self.motion['records'][120]['pose']['blink_R'] = .00001
        with self.assertRaises(ValueError):
            v.timeline_checks(self.motion['records'], self.keys)

    def test_sprite_shift_required_not_only_shader(self):
        self.motion['records'][48]['iris_geometry']['screen_left']['sprite_delta_source_px'] = [0, 0]
        with self.assertRaisesRegex(ValueError, 'sprite AND shader'):
            v.timeline_checks(self.motion['records'], self.keys)

    def test_shader_shift_required_not_only_sprite(self):
        self.static['records'][3]['iris_geometry']['screen_right']['iris_shader_offset_source_px'] = [0, 0]
        with self.assertRaisesRegex(ValueError, 'sprite AND shader'):
            v.static_checks(self.static['records'], self.plan)

    def test_vertical_iris_motion_rejected(self):
        self.motion['records'][48]['iris_geometry']['screen_right']['sprite_delta_source_px'][1] = .1
        with self.assertRaises(ValueError):
            v.timeline_checks(self.motion['records'], self.keys)

    def test_downturned_lip_geometry_rejected(self):
        self.static['records'][3]['lip_contour_offsets'][0]['upper_y'] = 2
        with self.assertRaisesRegex(ValueError, 'invented'):
            v.static_checks(self.static['records'], self.plan)

    def test_mouth_width_mutation_rejected(self):
        self.static['records'][3]['actual_mouth_side_delta_source_px'] = [1, -1]
        with self.assertRaises(ValueError):
            v.static_checks(self.static['records'], self.plan)

    def test_wrong_lid_screen_mapping_rejected(self):
        r = self.static['records'][3]['lash_geometry']
        r['screen_left'], r['screen_right'] = r['screen_right'], r['screen_left']
        with self.assertRaisesRegex(ValueError, 'lid mapping'):
            v.static_checks(self.static['records'], self.plan)

    def test_brow_geometry_mutation_rejected(self):
        self.static['records'][3]['brow_geometry']['screen_left']['pivot_delta_source_px'][1] += 1
        with self.assertRaisesRegex(ValueError, 'translations'):
            v.static_checks(self.static['records'], self.plan)

    def test_lifecycle_missing_sample_rejected(self):
        self.motion['lifecycle_scoped_samples'].pop()
        with self.assertRaisesRegex(ValueError, '252'):
            v.lifecycle_checks(self.motion, self.keys)

    def test_lifecycle_reorder_rejected(self):
        rows = self.motion['lifecycle_scoped_samples']
        rows[22], rows[23] = rows[23], rows[22]
        with self.assertRaisesRegex(ValueError, 'order'):
            v.lifecycle_checks(self.motion, self.keys)

    def test_direct_release_unsupported_lid_decay_rejected(self):
        r = next(r for r in self.motion['lifecycle_scoped_samples'] if r['interruption_time'] == 1.6 and r['stage'] == 'release' and r['step'] == 6)
        source = v.sample(self.keys, 1.6)
        weight = v.smooth(.2/.45)
        r['pose'] = {k: source[k]*(1-weight) for k in v.CHANNELS}
        with self.assertRaises(ValueError):
            v.lifecycle_checks(self.motion, self.keys)

    def test_lifecycle_safe_but_wrong_pose_rejected(self):
        r = next(r for r in self.motion['lifecycle_scoped_samples'] if r['interruption_time'] == 1.6 and r['stage'] == 'restart')
        r['pose']['brow_screen_left'] = -.60
        with self.assertRaisesRegex(ValueError, 'interpolation'):
            v.lifecycle_checks(self.motion, self.keys)

    def test_subframe_boundary_support(self):
        for stage, half in [('restart', .15), ('release', .225)]:
            before = v.lifecycle_pose(self.keys, 1.6, stage, half-1e-6)
            at = v.lifecycle_pose(self.keys, 1.6, stage, half)
            after = v.lifecycle_pose(self.keys, 1.6, stage, half+1e-6)
            self.assertGreater(before['aversion_px'], 0)
            self.assertEqual(at['aversion_px'], 0)
            self.assertEqual(after['aversion_px'], 0)
            for p in [before, at, after]:
                v.pose_valid(p)
            self.assertAlmostEqual(before['blink_L'], .3)


class EvidenceTests(unittest.TestCase):
    def test_rebased_author_freeze_cannot_reset_review_trust(self):
        with tempfile.TemporaryDirectory() as d:
            w = Path(d)
            (w/'review_input_freeze.json').write_text('{"candidate":"EXP-045","files":{}}')
            (w/'REVIEW_FREEZE.sha256').write_text(v.sha(w/'review_input_freeze.json')+'  review_input_freeze.json\n')
            with self.assertRaisesRegex(ValueError, 'hardcoded freeze'):
                v.pinned_checks(w)

    def test_duplicate_json_key_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'a.json'
            p.write_text('{"a":1,"a":2}')
            with self.assertRaisesRegex(ValueError, 'Duplicate'):
                v.load(p)

    def test_nonfinite_json_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'a.json'
            p.write_text('{"a":NaN}')
            with self.assertRaises(ValueError):
                v.load(p)

    def test_headless_cannot_be_native(self):
        r = v.load(WORK/'motion_state_checks.json')
        with self.assertRaisesRegex(ValueError, 'Headless/native'):
            v.common_receipt(r, WORK, True, True)

    def test_native_renderer_required(self):
        r = v.load(WORK/'motion_state_checks.json')
        r.update(visual_capture=True, checks=13186)
        with self.assertRaisesRegex(ValueError, 'display/renderer'):
            v.common_receipt(r, WORK, True, True)

    def test_stale_profile_receipt_rejected(self):
        r = v.load(WORK/'motion_state_checks.json')
        r['profile_sha256'] = '0'*64
        with self.assertRaisesRegex(ValueError, 'input identity'):
            v.common_receipt(r, WORK, False, True)

    def test_missing_native_hash_rejected(self):
        r = v.load(WORK/'motion_state_checks.json')
        r.update(visual_capture=True, checks=13186, renderer='SYNTHETIC TEST ONLY', display='SYNTHETIC')
        with self.assertRaisesRegex(ValueError, 'two native hashes'):
            v.common_receipt(r, WORK, True, True)

    def test_bad_native_dimensions_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'wrong.png'
            Image.new('RGBA', (20, 20)).save(p)
            with self.assertRaisesRegex(ValueError, 'dimensions'):
                v.read_png(p, (400, 360))

    def test_bad_native_mode_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'wrong.png'
            Image.new('RGB', (400, 360)).save(p)
            with self.assertRaisesRegex(ValueError, 'RGBA'):
                v.read_png(p, (400, 360))

    def test_partial_missing_native_is_pending_not_pass(self):
        with tempfile.TemporaryDirectory() as d:
            w = Path(d)
            report = {'pending': [], 'native_hashes': [], 'native_pixels': {}}
            v.native_checks(w, {}, {}, {}, report)
            self.assertEqual(len(report['pending']), 7)
            self.assertEqual(report['native_hashes'], [])

    def test_malformed_partial_native_image_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            w = Path(d)
            (w/'motion/full').mkdir(parents=True)
            (w/'motion/full/0000.png').write_bytes(b'not an image')
            with self.assertRaises(Exception):
                v.native_checks(w, {}, {}, {}, {'pending': [], 'native_hashes': [], 'native_pixels': {}})

    def test_unexpected_native_png_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            w = Path(d)
            (w/'motion/full').mkdir(parents=True)
            (w/'motion/full/9999.png').write_bytes(b'irrelevant')
            with self.assertRaisesRegex(ValueError, 'Unexpected'):
                v.native_checks(w, {}, {}, {}, {'pending': [], 'native_hashes': [], 'native_pixels': {}})

    def test_actual_native_rgba_hash_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            w = Path(d)
            for name in ['BASELINE_FREEZE.json', 'EXP-045.json']:
                shutil.copyfile(WORK/name, w/name)
            motion = v.load(WORK/'motion_state_checks.json')
            native = copy.deepcopy(motion)
            native.update(visual_capture=True, checks=13186, renderer='SYNTHETIC TEST ONLY', display='SYNTHETIC')
            for row in native['records']:
                row['hashes'] = ['0'*64, '0'*64]
            (w/'motion_checks.json').write_text(json.dumps(native))
            (w/'motion/full').mkdir(parents=True)
            Image.new('RGBA', (568, 800)).save(w/'motion/full/0000.png')
            with self.assertRaisesRegex(ValueError, 'RGBA hash mismatch'):
                v.native_checks(w, {}, motion, v.load(WORK/'EXP-045.json'), {'pending': [], 'native_hashes': [], 'native_pixels': {}})


class PixelTests(unittest.TestCase):
    def arrays(self):
        neutral = np.zeros((800, 568, 4), dtype=np.uint8)
        peak = neutral.copy()
        peak[300:320, 250:270] = [100, 80, 60, 255]
        return [peak if 48 <= i <= 72 else neutral for i in range(121)]

    def test_body_fixed_synthetic_fixture_passes(self):
        self.assertGreater(max(v.pixels_checks(self.arrays(), 'full')), 0)

    def test_body_drift_rejected(self):
        a = self.arrays()
        a[30] = a[30].copy()
        a[30][500, 300] = 255
        with self.assertRaisesRegex(ValueError, 'outside face'):
            v.pixels_checks(a, 'full')

    def test_neutral_pixel_drift_rejected(self):
        a = self.arrays()
        a[120] = a[120].copy()
        a[120][300, 250] = 255
        with self.assertRaisesRegex(ValueError, 'neutral'):
            v.pixels_checks(a, 'full')

    def test_peak_pixel_drift_rejected(self):
        a = self.arrays()
        a[60] = a[60].copy()
        a[60][300, 250] = 0
        with self.assertRaisesRegex(ValueError, 'peak'):
            v.pixels_checks(a, 'full')

    def test_blank_expression_rejected(self):
        a = self.arrays()[0]
        with self.assertRaisesRegex(ValueError, 'Nontrivial'):
            v.pixels_checks([a]*121, 'full')


class VideoTests(unittest.TestCase):
    def setUp(self):
        self.probe = {'streams': [{'codec_name': 'h264', 'pix_fmt': 'yuv420p', 'width': 968, 'height': 800, 'r_frame_rate': '30/1', 'nb_frames': '121', 'nb_read_frames': '121'}], 'format': {'duration': '4.033333'}}
        self.pts = [{'best_effort_timestamp_time': str(i/30)} for i in range(121)]

    def test_video_metadata_pass(self):
        v.video_probe_checks(self.probe, self.pts)

    def test_video_order_timestamp_rejected(self):
        self.pts[15], self.pts[16] = self.pts[16], self.pts[15]
        with self.assertRaisesRegex(ValueError, 'timestamp'):
            v.video_probe_checks(self.probe, self.pts)

    def test_video_bad_frame_count_rejected(self):
        self.probe['streams'][0]['nb_read_frames'] = '120'
        with self.assertRaises(ValueError):
            v.video_probe_checks(self.probe, self.pts)

    def test_video_bad_layout_rejected(self):
        self.probe['streams'][0]['width'] = 1136
        with self.assertRaises(ValueError):
            v.video_probe_checks(self.probe, self.pts)

    def test_video_bad_duration_rejected(self):
        self.probe['format']['duration'] = '8'
        with self.assertRaises(ValueError):
            v.video_probe_checks(self.probe, self.pts)

    def test_same_index_image_and_face_order(self):
        a = np.zeros((800, 568, 4), dtype=np.uint8)
        b = np.zeros((360, 400, 4), dtype=np.uint8)
        arrays = {'full': [a], 'detail': [b]}
        decoded = np.zeros((800, 968, 3), dtype=np.uint8)
        features = np.zeros((1, 115, 140, 3), dtype=np.float32)
        v.decoded_frame_checks(decoded, 0, arrays, features)
        decoded[275:505, 608:888] = 10
        with self.assertRaises(ValueError):
            v.decoded_frame_checks(decoded, 0, arrays, features)

    def test_similar_but_reordered_face_rejected(self):
        a = np.zeros((800, 568, 4), dtype=np.uint8)
        b = np.zeros((360, 400, 4), dtype=np.uint8)
        decoded = np.zeros((800, 968, 3), dtype=np.uint8)
        decoded[275:505, 608:888] = 1
        features = np.asarray([np.zeros((115, 140, 3)), np.ones((115, 140, 3))], dtype=np.float32)
        with self.assertRaisesRegex(ValueError, 'reorder'):
            v.decoded_frame_checks(decoded, 0, {'full': [a], 'detail': [b]}, features)

    def fake_decode(self, frames=121, truncated=False, code=0):
        class Reader:
            def __init__(self):
                self.n = 0
            def read(self, count):
                self.n += 1
                if self.n > frames:
                    return b''
                return bytes(count-1 if truncated else count)
            def close(self):
                pass
        process = mock.Mock()
        process.stdout = Reader()
        process.wait.return_value = code
        process.poll.return_value = code
        arrays = {'detail': [np.zeros((360, 400, 4), dtype=np.uint8)]*121}
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'synthetic.mp4'
            p.write_bytes(b'SYNTHETIC DECODER MOCK ONLY')
            with mock.patch.object(v, 'load_subprocess', side_effect=[self.probe, {'frames': self.pts}]), mock.patch.object(v.subprocess, 'Popen', return_value=process), mock.patch.object(v, 'decoded_frame_checks', side_effect=lambda frame, i, ar, feat: {'frame': i}) as compare:
                result = v.decode_video(p, arrays)
                self.assertEqual(compare.call_count, 121)
                return result

    def test_full_decode_visits_all_121_frames(self):
        self.assertEqual(self.fake_decode()['decoded_frames'], 121)

    def test_full_decode_missing_last_frame_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Complete clean'):
            self.fake_decode(frames=120)

    def test_full_decode_extra_frame_rejected(self):
        with self.assertRaisesRegex(ValueError, 'extra'):
            self.fake_decode(frames=122)

    def test_full_decode_truncated_frame_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Truncated'):
            self.fake_decode(truncated=True)

    def test_full_decode_nonzero_exit_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Complete clean'):
            self.fake_decode(code=1)


if __name__ == '__main__':
    unittest.main()

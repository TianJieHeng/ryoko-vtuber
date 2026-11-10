"""Small read-only-validator unit tests. Synthetic fixtures are not native evidence."""
import argparse
import contextlib
import copy
import io
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import numpy as np
from PIL import Image

W = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('mild_disgust_review', W/'review_validation.py')
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)


class ReviewValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.keys = json.loads((W/'EXP-081.json').read_text())['keyframes']
        cls.records = json.loads((W/'motion_state_checks.json').read_text())['records']

    def test_existing_headless_state_math(self):
        result = review.timeline_checks(self.records, self.keys)
        self.assertTrue(all(result['assertions'].values()))
        self.assertLess(result['max_smoothstep_control_error'], 1e-6)

    def test_exact_peak_and_neutral_interpolation(self):
        channels = self.records[0]['pose'].keys()
        peak = review.expected_pose(self.keys, 1.5, channels)
        self.assertEqual(peak['mouth_open'], .18)
        self.assertEqual(peak['mouth_purse'], .12)
        self.assertEqual(peak['mouth_width_screen_right'], 0.)
        self.assertEqual(peak['brow_inner_lift_screen_left'], 0.)
        self.assertEqual(peak['brow_tilt_screen_left'], .22)
        self.assertEqual(peak['brow_tilt_screen_right'], -.10)
        self.assertEqual(peak['mouth_corner_lift_screen_right'], .32)
        self.assertEqual(peak['blink_R'], .34)
        self.assertEqual(peak['blink_L'], .18)
        self.assertEqual(peak['mouth_smile'], 0.)
        self.assertTrue(all(v == 0 for v in review.expected_pose(self.keys, 3.8, channels).values()))

    def test_out_of_order_record_rejected(self):
        records = copy.deepcopy(self.records)
        records[15], records[16] = records[16], records[15]
        with self.assertRaisesRegex(ValueError, 'Incorrect frame'):
            review.timeline_checks(records, self.keys)

    def test_nonfinite_pose_rejected(self):
        records = copy.deepcopy(self.records)
        records[15]['pose']['mouth_open'] = float('nan')
        with self.assertRaisesRegex(ValueError, 'Non-finite'):
            review.timeline_checks(records, self.keys)

    def test_forbidden_control_detected(self):
        records = copy.deepcopy(self.records)
        records[41]['pose']['mouth_smile'] = .1
        result = review.timeline_checks(records, self.keys)
        self.assertFalse(result['assertions']['only_nine_nonzero_channels_act'])
        self.assertFalse(result['assertions']['independent_smoothstep_timeline'])

    def test_native_image_guards(self):
        with tempfile.TemporaryDirectory(prefix='exp081-validator-test-') as tmp:
            p = Path(tmp)/'synthetic.png'
            Image.new('RGBA', (400, 360), (0, 0, 0, 255)).save(p)
            self.assertEqual(review.read_png(p, (400, 360)).shape, (360, 400, 4))
            with self.assertRaisesRegex(ValueError, 'Native dimensions'):
                review.read_png(p, (568, 800))
            Image.new('RGB', (400, 360)).save(p)
            with self.assertRaisesRegex(ValueError, 'Native pixel mode'):
                review.read_png(p, (400, 360))

    def test_body_guard_and_empty_bbox(self):
        mask = np.zeros((800, 568), dtype=bool)
        self.assertIsNone(review.bbox(mask))
        mask[300, 250] = True
        self.assertTrue(review.outside_face_unchanged(mask))
        self.assertEqual(review.bbox(mask), [250, 300, 251, 301])
        mask[500, 250] = True
        self.assertFalse(review.outside_face_unchanged(mask))

    def test_wrong_blink_side_detected(self):
        records = copy.deepcopy(self.records)
        p = records[63]['pose']
        p['blink_L'], p['blink_R'] = p['blink_R'], p['blink_L']
        result = review.timeline_checks(records, self.keys)
        self.assertFalse(result['assertions']['bounded_correct_mild_lid_asymmetry'])

    def test_existing_static_geometry(self):
        rows = review.load(W/'plan.json')
        records = review.load(W/'state_checks.json')['records']
        result = review.static_geometry_checks(rows, records, W/'rig')
        self.assertTrue(all(result['assertions'].values()))
        peak = result['mouth_approximation'][3]
        self.assertAlmostEqual(peak['central_gap_source_px'], 5.2164, places=6)
        self.assertAlmostEqual(peak['central_gap_bust_px'], 2.556036, places=6)
        self.assertEqual(peak['endpoint_deltas_source_px'], [1.68, -1.68])
        self.assertEqual(peak['horizontal_center_motion_source_px'], 0)

    def test_wrong_brow_geometry_detected(self):
        rows = review.load(W/'plan.json')
        records = review.load(W/'state_checks.json')['records']
        records[3]['brow_geometry']['screen_left']['pivot_delta_source_px'][0] += 1
        result = review.static_geometry_checks(rows, records, W/'rig')
        self.assertFalse(result['assertions']['anchored_brow_geometry'])

    def test_wrong_mouth_geometry_detected(self):
        rows = review.load(W/'plan.json')
        records = review.load(W/'state_checks.json')['records']
        records[3]['actual_mouth_side_delta_source_px'][1] += 1
        result = review.static_geometry_checks(rows, records, W/'rig')
        self.assertFalse(result['assertions']['symmetric_purse_width'])

    def test_only_grid_aligned_static_anchors_used(self):
        for name, i in review.STATIC_FRAMES.items():
            values = next(r['pose'] for r in review.load(W/'plan.json') if r['name'] == name)
            expected = review.expected_pose(self.keys, i/30, self.records[0]['pose'])
            self.assertTrue(all(abs(v-values.get(k, 0)) < 1e-12 for k, v in expected.items()))
        self.assertNotIn('suppress', review.STATIC_FRAMES)
        self.assertNotIn('settle', review.STATIC_FRAMES)

    def test_incorrect_lip_contour_detected(self):
        rows = review.load(W/'plan.json')
        records = review.load(W/'state_checks.json')['records']
        records[3]['lip_contour_offsets'][1]['lower_y'] += 1.
        result = review.static_geometry_checks(rows, records, W/'rig')
        self.assertFalse(result['assertions']['common_corner_and_purse_lip_contour'])

    def test_incorrect_static_gap_detected(self):
        rows = review.load(W/'plan.json')
        records = review.load(W/'state_checks.json')['records']
        records[3]['central_lip_gap_bust_px'] += 1.
        result = review.static_geometry_checks(rows, records, W/'rig')
        self.assertFalse(result['assertions']['central_mouth_gap'])

    def test_incorrect_motion_gap_detected(self):
        records = copy.deepcopy(self.records)
        records[42]['central_lip_gap_native_px'] += 1.
        result = review.timeline_checks(records, self.keys)
        self.assertFalse(result['assertions']['all_recorded_mouth_gaps_match_independent_math'])

    def test_laugh_control_is_excluded(self):
        records = copy.deepcopy(self.records)
        records[42]['pose']['eye_smile_L'] = .5
        result = review.timeline_checks(records, self.keys)
        self.assertFalse(result['assertions']['only_nine_nonzero_channels_act'])
        self.assertFalse(result['assertions']['no_inner_lift_pressure_smile_width_gaze_blush_hair'])

    def test_mild_narrowing_cannot_be_replaced_by_widening(self):
        records = copy.deepcopy(self.records)
        records[42]['pose']['blink_L'] = records[42]['pose']['blink_R'] = 0.
        records[42]['pose']['opening_px'] = 4.
        result = review.timeline_checks(records, self.keys)
        self.assertFalse(result['assertions']['partial_unequal_narrowing_at_peak'])
        self.assertFalse(result['assertions']['no_inner_lift_pressure_smile_width_gaze_blush_hair'])

    def test_wrong_common_corner_direction_detected(self):
        records = copy.deepcopy(self.records)
        records[42]['pose']['mouth_corner_lift_screen_right'] = 0.
        records[42]['pose']['mouth_corner_lift_screen_left'] = .32
        result = review.timeline_checks(records, self.keys)['assertions']
        self.assertFalse(result['small_parted_common_corner_peak'])
        self.assertFalse(result['only_nine_nonzero_channels_act'])

    def test_lip_pressure_and_inner_lift_are_excluded(self):
        records = copy.deepcopy(self.records)
        records[42]['pose']['mouth_lip_press'] = .2
        records[42]['pose']['brow_inner_lift_screen_left'] = .2
        result = review.timeline_checks(records, self.keys)['assertions']
        self.assertFalse(result['no_inner_lift_pressure_smile_width_gaze_blush_hair'])

    def test_symmetric_brow_replacement_detected(self):
        records = copy.deepcopy(self.records)
        records[42]['pose']['brow_screen_right'] = -.44
        self.assertFalse(review.timeline_checks(records, self.keys)['assertions']['one_brow_dominantly_lowered'])

    def test_full_blink_is_not_mild_disgust(self):
        records = copy.deepcopy(self.records)
        records[42]['pose']['blink_R'] = records[42]['pose']['blink_L'] = 1.
        result = review.timeline_checks(records, self.keys)['assertions']
        self.assertFalse(result['bounded_correct_mild_lid_asymmetry'])
        self.assertFalse(result['partial_unequal_narrowing_at_peak'])

    def test_open_mouth_after_suppress_is_detected(self):
        records = copy.deepcopy(self.records)
        records[65]['pose']['mouth_open'] = .18
        self.assertFalse(review.timeline_checks(records, self.keys)['assertions']['lips_seal_while_objection_persists'])

    def test_timing_releases_corner_before_brow(self):
        records = copy.deepcopy(self.records)
        records[81]['pose']['mouth_corner_lift_screen_right'] = .12
        self.assertFalse(review.timeline_checks(records, self.keys)['assertions']['mouth_bias_releases_before_brow'])

    def test_both_lips_share_corner_bias_not_upper_only(self):
        rows = review.load(W/'plan.json')
        records = review.load(W/'state_checks.json')['records']
        records[3]['lip_contour_offsets'][2]['lower_y'] += 3.84
        result = review.static_geometry_checks(rows, records, W/'rig')['assertions']
        self.assertFalse(result['both_lips_share_side_bias'])
        self.assertFalse(result['common_corner_and_purse_lip_contour'])

    def test_peak_lip_geometry_and_symmetric_aperture(self):
        p = review.expected_pose(self.keys, 1.5, self.records[0]['pose'])
        left = review.lip_geometry(p, 4)
        right = review.lip_geometry(p, 75)
        center = review.lip_geometry(p, 39.5)
        self.assertAlmostEqual(left[0], 1.44)
        self.assertAlmostEqual(right[0], -2.4)
        self.assertAlmostEqual(left[1], right[1])
        self.assertAlmostEqual(center[1], 5.2164)
        self.assertAlmostEqual((left[0]+left[1])-(right[0]+right[1]), 3.84)

    def test_eight_static_anchors_not_nine(self):
        rows = review.load(W/'plan.json')
        records = review.load(W/'state_checks.json')['records']
        records.append(copy.deepcopy(records[-1]))
        result = review.static_geometry_checks(rows, records, W/'rig')['assertions']
        self.assertFalse(result['exact_eight_static_records'])

    def test_missing_or_changed_pose_channels_rejected(self):
        records = copy.deepcopy(self.records)
        del records[1]['pose']['mouth_corner_lift_screen_right']
        with self.assertRaisesRegex(ValueError, 'Pose channel set changed'):
            review.timeline_checks(records, self.keys)

    def test_wrong_held_peak_or_neutral_detected(self):
        records = copy.deepcopy(self.records)
        records[52]['pose']['mouth_corner_lift_screen_right'] = .31
        records[112]['pose']['mouth_open'] = .01
        result = review.timeline_checks(records, self.keys)['assertions']
        self.assertFalse(result['exact_peak_hold_42_through_52'])
        self.assertFalse(result['neutral_hold_states'])

    def run_isolated_fixture(self, transform=None):
        # Symlinks point only to read-only inputs; changed receipts are fresh
        # temp files. Synthetic fixtures must never be counted as native proof.
        with tempfile.TemporaryDirectory(prefix='exp081-review-fixture-') as tmp:
            root = Path(tmp)
            work = root/'mild_disgust_work'
            work.mkdir()
            skip = {'capture', 'motion', 'motion_checks.json', 'review_evidence',
                    'Mild_disgust_review_v1.mp4', '__pycache__'}
            for path in W.iterdir():
                if path.name not in skip:
                    (work/path.name).symlink_to(path, target_is_directory=path.is_dir())
            for name in ['mental_arithmetic_work', 'controlled_anger_work', 'broad_surprise_work', 'puzzled_work', 'open_sobbing_work']:
                (root/name).symlink_to(W.parent/name, target_is_directory=True)
            if transform:
                transform(work)
            before = {n: review.sha(W/n) for n in review.load(W/'review_input_freeze.json')['files']}
            with contextlib.redirect_stdout(io.StringIO()):
                code = review.run(argparse.Namespace(work=work, output=root/'reports', video=None))
            result = review.load(root/'reports/review_checks.json')
            after = {n: review.sha(W/n) for n in before}
            self.assertEqual(before, after)
            return code, result

    def test_no_native_inputs_is_pending_not_pass(self):
        code, result = self.run_isolated_fixture()
        self.assertEqual(code, 2)
        self.assertEqual(result['status'], 'PENDING')
        self.assertFalse(result['independent_checks_pass'])
        self.assertEqual(result['failures'], [])
        self.assertEqual(len(result['pending']), 3)
        self.assertFalse(result['normal_speed_continuous_observation'])

    def test_bad_freeze_is_fail_not_pending_only(self):
        def change(work):
            p = work/'review_input_freeze.json'
            data = review.load(p)
            p.unlink()  # Remove temp symlink, never the real input.
            data['status'] = 'TEST ONLY altered freeze'
            review.write(p, data)
        code, result = self.run_isolated_fixture(change)
        self.assertEqual(code, 1)
        self.assertIn('expected_review_input_freeze_identity', result['failures'])

    def test_failed_receipt_is_not_hidden_by_missing_frames(self):
        def change(work):
            (work/'capture').mkdir()
            data = review.load(W/'state_checks.json')
            data.update(status='FAIL', visual_capture=True, checks=1558,
                        failures=['TEST ONLY capture dimensions failure'])
            review.write(work/'capture/checks.json', data)
        code, result = self.run_isolated_fixture(change)
        self.assertEqual(code, 1)
        self.assertIn('native_static_receipt_pass', result['failures'])
        self.assertTrue(result['pending'])

    def test_failed_motion_receipt_not_hidden_by_missing_frames(self):
        def change(work):
            data = review.load(W/'motion_state_checks.json')
            data.update(status='FAIL', visual_capture=True, checks=11815,
                        display='TEST ONLY native fixture', renderer='TEST ONLY',
                        failures=['TEST ONLY native failure'])
            review.write(work/'motion_checks.json', data)
        code, result = self.run_isolated_fixture(change)
        self.assertEqual(code, 1)
        self.assertIn('native_motion_receipt_pass', result['failures'])
        self.assertTrue(result['pending'])


if __name__ == '__main__':
    unittest.main(verbosity=2)

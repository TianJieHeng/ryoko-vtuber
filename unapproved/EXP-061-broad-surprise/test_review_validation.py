"""Small read-only-validator unit tests. Synthetic fixtures are not native evidence."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import numpy as np
from PIL import Image

W = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('broad_surprise_review', W/'review_validation.py')
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)


class ReviewValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.keys = json.loads((W/'EXP-061.json').read_text())['keyframes']
        cls.records = json.loads((W/'motion_state_checks.json').read_text())['records']

    def test_existing_headless_state_math(self):
        result = review.timeline_checks(self.records, self.keys)
        self.assertTrue(all(result['assertions'].values()))
        self.assertLess(result['max_smoothstep_control_error'], 1e-6)

    def test_exact_peak_and_neutral_interpolation(self):
        channels = self.records[0]['pose'].keys()
        peak = review.expected_pose(self.keys, 1.5, channels)
        self.assertEqual(peak['mouth_open'], .95)
        self.assertEqual(peak['brow_screen_left'], 1.)
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
        self.assertFalse(result['assertions']['only_six_allowed_channels_act'])
        self.assertFalse(result['assertions']['independent_smoothstep_timeline'])

    def test_native_image_guards(self):
        with tempfile.TemporaryDirectory(prefix='exp061-validator-test-') as tmp:
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


if __name__ == '__main__':
    unittest.main(verbosity=2)

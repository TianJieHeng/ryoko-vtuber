"""Guard tests using temporary receipts and mocked pixels, never preview art."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import encode_preview as enc


class FakeImage:
    mode = 'RGBA'
    def __init__(self, size):
        self.size = size
    def __enter__(self):
        return self
    def __exit__(self, *args):
        pass
    def tobytes(self):
        return b'mocked unit-test pixels, not artwork'


class CaptureGuards(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='exp045_encoder_test_')
        self.w = Path(self.tmp.name)
        self.write('BASELINE_FREEZE.json', {'baseline_profile_count': 36})
        self.write('EXP-045.json', {'id': 'EXP-045'})
        self.write('plan.json', [{'name': 'neutral', 'pose': {}}])
        freeze = enc.sha(self.w/'BASELINE_FREEZE.json')
        self.static = dict(status='PASS', failures=[], visual_capture=True,
            baseline_freeze_sha256=freeze, plan_sha256=enc.sha(self.w/'plan.json'))
        self.digest = hashlib.sha256(FakeImage((1, 1)).tobytes()).hexdigest()
        self.motion = dict(status='PASS', failures=[], visual_capture=True,
            baseline_freeze_sha256=freeze, profile_sha256=enc.sha(self.w/'EXP-045.json'),
            display='unit-test-mock', renderer='unit-test-mock', frames=121, fps=30,
            duration=4.0, baseline_profile_count=36,
            records=[dict(frame=i, time=i/30, hashes=[self.digest, self.digest]) for i in range(121)])
        for view in ['full', 'detail']:
            directory = self.w/'motion'/view
            directory.mkdir(parents=True)
            for i in range(121):
                (directory/f'{i:04d}.png').write_bytes(b'')
        self.save()

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name, value):
        p = self.w/name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(value))

    def save(self):
        self.write('capture/checks.json', self.static)
        self.write('motion_checks.json', self.motion)

    def fake_open(self, path):
        return FakeImage((400, 360) if 'detail' in str(path) else (568, 800))

    def validate(self):
        with patch.object(enc.Image, 'open', side_effect=self.fake_open):
            return enc.validate_capture(self.w)

    def test_complete_mock_receipts(self):
        self.assertEqual(self.validate()['frames'], 121)

    def test_missing_native_receipts(self):
        (self.w/'motion_checks.json').unlink()
        with self.assertRaisesRegex(ValueError, 'pending'):
            self.validate()

    def test_headless_rejected(self):
        self.motion['display'] = 'headless'; self.save()
        with self.assertRaisesRegex(ValueError, 'Headless'):
            self.validate()

    def test_failed_static_rejected(self):
        self.static['status'] = 'FAIL'; self.save()
        with self.assertRaisesRegex(ValueError, 'must pass'):
            self.validate()

    def test_changed_profile_rejected(self):
        self.write('EXP-045.json', {'id': 'changed'})
        with self.assertRaisesRegex(ValueError, 'changed after capture'):
            self.validate()

    def test_changed_baseline_rejected(self):
        self.write('BASELINE_FREEZE.json', {'baseline_profile_count': 39})
        with self.assertRaisesRegex(ValueError, 'another baseline'):
            self.validate()

    def test_missing_frame_rejected(self):
        (self.w/'motion/full/0060.png').unlink()
        with self.assertRaisesRegex(ValueError, 'incomplete or extra'):
            self.validate()

    def test_extra_frame_rejected(self):
        (self.w/'motion/detail/0121.png').write_bytes(b'')
        with self.assertRaisesRegex(ValueError, 'incomplete or extra'):
            self.validate()

    def test_wrong_size_rejected(self):
        with patch.object(enc.Image, 'open', return_value=FakeImage((1136, 800))):
            with self.assertRaisesRegex(ValueError, 'native RGBA'):
                enc.validate_capture(self.w)

    def test_wrong_pixel_mode_rejected(self):
        with patch.object(FakeImage, 'mode', 'RGB'):
            with self.assertRaisesRegex(ValueError, 'native RGBA'):
                self.validate()

    def test_wrong_pixels_rejected(self):
        self.motion['records'][50]['hashes'][0] = 'stale'; self.save()
        with self.assertRaisesRegex(ValueError, 'pixel receipt'):
            self.validate()

    def test_wrong_time_rejected(self):
        self.motion['records'][50]['time'] = 0; self.save()
        with self.assertRaisesRegex(ValueError, 'order/time'):
            self.validate()

    def test_existing_video_preserved(self):
        (self.w/'Irritated_side_eye_review_v1.mp4').write_bytes(b'preserve')
        with patch.object(enc, 'W', self.w), patch.object(enc, 'validate_capture'), patch.object(enc.subprocess, 'run') as run:
            with self.assertRaisesRegex(ValueError, 'refusing overwrite'):
                enc.main()
            run.assert_not_called()
        self.assertEqual((self.w/'Irritated_side_eye_review_v1.mp4').read_bytes(), b'preserve')


    def test_changed_plan_rejected(self):
        self.write('plan.json', [{'name': 'changed', 'pose': {}}])
        with self.assertRaisesRegex(ValueError, 'changed after capture'):
            self.validate()

    def test_wrong_profile_count_rejected(self):
        self.motion['baseline_profile_count'] = 39; self.save()
        with self.assertRaisesRegex(ValueError, 'profile count'):
            self.validate()

    def test_wrong_fps_rejected(self):
        self.motion['fps'] = 60; self.save()
        with self.assertRaisesRegex(ValueError, '121 frames'):
            self.validate()

    def test_wrong_record_count_rejected(self):
        self.motion['records'].pop(); self.save()
        with self.assertRaisesRegex(ValueError, 'frame receipts'):
            self.validate()

    def test_missing_renderer_rejected(self):
        self.motion['renderer'] = ''; self.save()
        with self.assertRaisesRegex(ValueError, 'Headless'):
            self.validate()

    def test_nonvisual_static_rejected(self):
        self.static['visual_capture'] = False; self.save()
        with self.assertRaisesRegex(ValueError, 'must pass'):
            self.validate()

    def test_static_dimensions_rejected(self):
        def wrong_static(path):
            return FakeImage((1136, 800)) if '/capture/' in str(path) else self.fake_open(path)
        with patch.object(enc.Image, 'open', side_effect=wrong_static):
            with self.assertRaisesRegex(ValueError, 'Static capture'):
                enc.validate_capture(self.w)


if __name__ == '__main__':
    unittest.main()

"""Pure-Python numerical/specification tests. Never launches a native process."""
import copy
import json
import math
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from numeric_model import *
from encode_preview import require_native_gate,validate_capture,command

class CandidateTests(unittest.TestCase):
    def setUp(self):
        self.p=json.loads((W/'EXP-092.json').read_text())

    def reject(self,mutate):
        p=copy.deepcopy(self.p); mutate(p)
        with self.assertRaises(ValueError): validate_profile(p)

    def test_schema(self):
        self.assertTrue(validate_profile(self.p))
        self.assertEqual(len(self.p['keyframes']),12)
        self.assertEqual(self.p['duration'],4)

    def test_unknown_field(self): self.reject(lambda p:p.update({'approved':True}))
    def test_unknown_id(self): self.reject(lambda p:p.update({'id':'EXP-096'}))
    def test_boolean_value(self): self.reject(lambda p:p['keyframes'][2]['values'].update({'mouth_purse':True}))
    def test_nonfinite_value(self): self.reject(lambda p:p['keyframes'][2]['values'].update({'mouth_purse':float('nan')}))
    def test_nonfinite_duration(self): self.reject(lambda p:p.update({'duration':float('inf')}))
    def test_purse_bounds(self): self.reject(lambda p:p['keyframes'][5]['values'].update({'mouth_purse':1.01}))
    def test_kiss_excluded(self): self.reject(lambda p:p['keyframes'][5]['values'].update({'mouth_kiss':.1}))
    def test_smile_eye_excluded(self): self.reject(lambda p:p['keyframes'][5]['values'].update({'eye_smile_L':.1}))
    def test_open_mouth_excluded(self): self.reject(lambda p:p['keyframes'][5]['values'].update({'mouth_open':.01}))
    def test_duplicate_time(self): self.reject(lambda p:p['keyframes'][2].update({'time':.2}))
    def test_missing_endpoint(self): self.reject(lambda p:p['keyframes'][-1].update({'time':3.9}))
    def test_nonneutral_endpoint(self): self.reject(lambda p:p['keyframes'][-1]['values'].update({'mouth_purse':.1}))
    def test_lid_asymmetry(self): self.reject(lambda p:p['keyframes'][5]['values'].update({'blink_L':.9}))
    def test_brow_opposition(self): self.reject(lambda p:p['keyframes'][5]['values'].update({'brow_tilt_screen_right':.65}))

    def test_dense_bounds_and_scope(self):
        for i in range(961):
            p=playback_from_neutral(self.p,i/240)
            for key,value in p.items():
                self.assertTrue(math.isfinite(value))
                self.assertLessEqual(value,1)
                self.assertGreaterEqual(value,-1 if key.startswith('brow_') else 0)
                if key not in ACTING: self.assertEqual(value,0)
            self.assertEqual(p['blink_L'],p['blink_R'])
            self.assertEqual(geometry(p)['central_aperture_source_px'],0)

    def test_exact_endpoints_and_holds(self):
        for t in [-.1,0,.1,.2,3.7,3.9,4,4.1]: self.assertEqual(sample(self.p,t),neutral())
        peak=sample(self.p,1.6)
        for i in range(48,61): self.assertEqual(sample(self.p,i/30),peak)
        self.assertEqual(sample(self.p,2.4)['blink_L'],1)
        self.assertLess(sample(self.p,2.8)['blink_L'],1)

    def test_initial_restart_envelope(self):
        raw=sample(self.p,.25); actual=playback_from_neutral(self.p,.25)
        self.assertGreater(raw['mouth_purse'],actual['mouth_purse'])
        self.assertGreater(actual['mouth_purse'],0)
        player=RestrictedLifecycle(self.p); player.trigger(); player.advance(.25)
        self.assertEqual(player.pose,actual)

    def test_peak_matches_headache_except_purse(self):
        h=json.loads((W/'comparators/EXP-096.json').read_text())
        sour=sample(self.p,1.6); head=sample(h,1.6)
        for key in CHANNELS:
            if key!='mouth_purse': self.assertEqual(sour[key],head[key])
        self.assertAlmostEqual(sour['mouth_purse']-head['mouth_purse'],.85)
        self.assertAlmostEqual(geometry(head)['mouth_contour_width_source_px']-geometry(sour)['mouth_contour_width_source_px'],23.8)

    def test_maximum_frame_step(self):
        rows=[playback_from_neutral(self.p,i/30) for i in range(121)]
        for key in ACTING:
            self.assertLess(max(abs(a[key]-b[key]) for a,b in zip(rows,rows[1:])),.20)

    def test_retrigger_continuity(self):
        for t in [.35,.6,1,1.6,2,2.4,2.8,3.2,3.7]:
            player=RestrictedLifecycle(self.p); player.trigger(); player.advance(t)
            before=player.pose.copy(); player.trigger()
            self.assertEqual(player.pose,before)
            for _ in range(5):
                player.advance(.03); before=player.pose.copy(); player.trigger(); self.assertEqual(before,player.pose)
            player.advance(4); self.assertEqual(player.pose,neutral())

    def test_release_continuity_and_exact_neutral(self):
        for t in [.35,.6,1,1.6,2,2.4,2.8,3.2,3.7]:
            player=RestrictedLifecycle(self.p); player.trigger(); player.advance(t)
            before=player.pose.copy(); player.release(); self.assertEqual(before,player.pose)
            player.advance(.45); self.assertEqual(player.pose,neutral())

    def test_reset_exact_neutral(self):
        player=RestrictedLifecycle(self.p); player.trigger(); player.advance(1.6); player.reset()
        self.assertEqual(player.pose,neutral()); self.assertFalse(player.auto_blink); self.assertFalse(player.pending)

    def test_auto_blink_restoration_model(self):
        for final in ['completion','release']:
            player=RestrictedLifecycle(self.p); player.auto_blink=True; player.trigger(); player.advance(1.6)
            self.assertFalse(player.auto_blink); self.assertTrue(player.pending)
            player.trigger(); self.assertTrue(player.pending)
            if final=='release': player.release()
            player.advance(4)
            self.assertEqual(player.pose,neutral()); self.assertTrue(player.auto_blink); self.assertFalse(player.pending)

    def test_manual_takeover_cancels_restore(self):
        player=RestrictedLifecycle(self.p); player.auto_blink=True; player.trigger(); player.advance(1.6)
        player.manual({'mouth_purse':.2}); before=player.pose.copy(); player.advance(4)
        self.assertEqual(player.pose,before); self.assertFalse(player.auto_blink); self.assertFalse(player.pending)

    def test_invalid_transactions_are_atomic(self):
        player=RestrictedLifecycle(self.p); player.trigger(); player.advance(1.6)
        for controls in [{'mouth_purse':2},{'mouth_purse':True},{'mouth_purse':.5,'mouth_kiss':.1}]:
            before=copy.deepcopy(player.__dict__)
            with self.assertRaises(ValueError): player.manual(controls)
            self.assertEqual(player.__dict__,before)
        for delta in [-1,float('nan'),float('inf'),True]:
            before=copy.deepcopy(player.__dict__)
            with self.assertRaises(ValueError): player.advance(delta)
            self.assertEqual(player.__dict__,before)

    def test_frozen_numeric_receipts(self):
        for filename,expected in zip(['NUMERIC_TRAJECTORY.json','NUMERIC_LIFECYCLE.json'],build_receipts()):
            self.assertEqual((W/filename).read_text(),canonical(expected))

    def test_native_gate_blocks_before_external_process(self):
        with patch('subprocess.run',side_effect=AssertionError('External process forbidden')),patch('subprocess.check_output',side_effect=AssertionError('External process forbidden')):
            with self.assertRaisesRegex(ValueError,'blocked'): validate_capture(W)

    def test_missing_gate_and_capture_fail_closed(self):
        with tempfile.TemporaryDirectory() as folder:
            temp=Path(folder)
            with self.assertRaises(ValueError): require_native_gate(temp)
            (temp/'NATIVE_GATE.json').write_text('{"allowed":true}')
            with self.assertRaisesRegex(ValueError,'missing'): validate_capture(temp)

    def test_encoder_never_overwrites(self):
        with tempfile.TemporaryDirectory() as folder:
            temp=Path(folder)
            (temp/'Sour_taste_rebuild_UNAPPROVED.mp4').write_bytes(b'preserve')
            with self.assertRaisesRegex(ValueError,'overwrite'): command(temp)
            self.assertEqual((temp/'Sour_taste_rebuild_UNAPPROVED.mp4').read_bytes(),b'preserve')

    def test_trajectory_matches_numeric_playback(self):
        player=RestrictedLifecycle(self.p); player.trigger()
        for i in range(121):
            if i: player.advance(i/30-player.t)
            expected=playback_from_neutral(self.p,i/30)
            for key in CHANNELS: self.assertAlmostEqual(player.pose[key],expected[key],places=12)

    def make_fake_receipt(self,temp):
        # Deliberately synthetic metadata for negative tests. No images or native
        # evidence are created, and this never leaves a temporary directory.
        (temp/'NATIVE_GATE.json').write_text('{"allowed":true}')
        (temp/'INPUT_FREEZE.json').write_text('{"files_sha256":{}}')
        (temp/'BASELINE_FREEZE.json').write_text('{}')
        (temp/'native_capture').mkdir()
        return {'status':'PASS','failures':[],'visual_capture':True,'display':'x11','renderer':'test-only',
            'input_freeze_sha256':sha(temp/'INPUT_FREEZE.json'),'baseline_freeze_sha256':sha(temp/'BASELINE_FREEZE.json'),
            'frames_per_profile':121,'fps':30,'duration':4.0,
            'records':{'EXP-092':[],'EXP-096':[],'EXP-091':[]},
            'profile_hashes':{'EXP-092':'fake','EXP-096':'fake','EXP-091':'fake'}}

    def test_headless_capture_receipt_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            temp=Path(folder); receipt=self.make_fake_receipt(temp); receipt['display']='headless'
            (temp/'native_capture/motion_checks.json').write_text(canonical(receipt))
            with self.assertRaisesRegex(ValueError,'headless'): validate_capture(temp)

    def test_wrong_capture_freeze_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            temp=Path(folder); receipt=self.make_fake_receipt(temp); receipt['input_freeze_sha256']='wrong'
            (temp/'native_capture/motion_checks.json').write_text(canonical(receipt))
            with self.assertRaisesRegex(ValueError,'another input freeze'): validate_capture(temp)

    def test_missing_sweet_comparator_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            temp=Path(folder); receipt=self.make_fake_receipt(temp); del receipt['records']['EXP-091']
            (temp/'native_capture/motion_checks.json').write_text(canonical(receipt))
            with self.assertRaisesRegex(ValueError,'comparators'): validate_capture(temp)

    def test_mismatched_captured_profile_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            temp=Path(folder); receipt=self.make_fake_receipt(temp)
            (temp/'EXP-092.json').write_text('{}')
            (temp/'native_capture/motion_checks.json').write_text(canonical(receipt))
            with self.assertRaisesRegex(ValueError,'Profile hash mismatch'): validate_capture(temp)

if __name__=='__main__': unittest.main()

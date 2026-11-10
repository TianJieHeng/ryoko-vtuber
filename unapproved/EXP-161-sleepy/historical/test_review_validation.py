"""Read-only review guard tests. Synthetic temporary fixtures are not native evidence."""
import argparse
import contextlib
import copy
import io
from pathlib import Path
import tempfile
import unittest
import numpy as np
from PIL import Image
import review_validation as review
W=Path(__file__).resolve().parent
class ReviewValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.keys=review.load(W/'EXP-161.json')['keyframes']
        cls.records=review.load(W/'motion_state_checks.json')['records']
    def mutate(self,frame,key,value):
        records=copy.deepcopy(self.records);records[frame]['pose'][key]=value
        return review.timeline_checks(records,self.keys)['assertions']
    def test_current_headless_math(self):
        r=review.timeline_checks(self.records,self.keys)
        self.assertTrue(all(r['assertions'].values()));self.assertLess(r['max_smoothstep_control_error'],1e-6)
    def test_exact_peak_and_neutral(self):
        p=review.expected_pose(self.keys,2,self.records[0]['pose'])
        self.assertEqual({k:v for k,v in p.items() if v},{'blink_R':.57,'blink_L':.57,'brow_screen_left':-.22,'brow_screen_right':-.22,'mouth_open':.16})
        self.assertTrue(all(v==0 for v in review.expected_pose(self.keys,3.8,p).values()))
    def test_out_of_order(self):
        r=copy.deepcopy(self.records);r[15],r[16]=r[16],r[15]
        with self.assertRaisesRegex(ValueError,'Incorrect frame'):review.timeline_checks(r,self.keys)
    def test_nonfinite(self):
        with self.assertRaisesRegex(ValueError,'Non-finite'):self.mutate(15,'mouth_open',float('nan'))
    def test_forbidden_smile(self):
        self.assertFalse(self.mutate(48,'mouth_smile',.1)['only_five_nonzero_channels_act'])
    def test_forbidden_brow_tilt(self):
        self.assertFalse(self.mutate(48,'brow_tilt_screen_left',.5)['no_tilt_inner_lift_purse_pressure_smile_width_gaze_blush_hair'])
    def test_forbidden_pout(self):
        self.assertFalse(self.mutate(48,'mouth_purse',.5)['only_five_nonzero_channels_act'])
    def test_lid_asymmetry(self):
        self.assertFalse(self.mutate(48,'blink_R',.4)['bounded_bilateral_heavy_lids'])
    def test_full_blink(self):
        self.assertFalse(self.mutate(48,'blink_R',1)['partial_heavy_lids_at_peak'])
    def test_sealed_peak(self):
        self.assertFalse(self.mutate(48,'mouth_open',0)['slight_parted_lips_at_peak'])
    def test_brow_depth(self):
        self.assertFalse(self.mutate(48,'brow_screen_left',-.9)['equal_relaxed_low_brows'])
    def test_second_sag(self):
        self.assertFalse(self.mutate(90,'blink_L',.8)['no_repeated_sag_during_recovery'])
    def test_peak_hold_change(self):
        self.assertFalse(self.mutate(65,'mouth_open',.15)['exact_peak_hold_48_through_72'])
    def test_neutral_drift(self):
        self.assertFalse(self.mutate(112,'mouth_open',.01)['neutral_hold_states'])
    def test_missing_channel(self):
        r=copy.deepcopy(self.records);del r[1]['pose']['mouth_open']
        with self.assertRaisesRegex(ValueError,'Pose channel set changed'):review.timeline_checks(r,self.keys)
    def test_recorded_gap(self):
        r=copy.deepcopy(self.records);r[48]['central_lip_gap_native_px']+=1
        self.assertFalse(review.timeline_checks(r,self.keys)['assertions']['all_recorded_mouth_gaps_match_independent_math'])
    def test_current_static_geometry(self):
        r=review.static_geometry_checks(review.load(W/'plan.json'),review.load(W/'state_checks.json')['records'],W/'rig')
        self.assertTrue(all(r['assertions'].values()))
        p=r['mouth_approximation'][3]
        self.assertAlmostEqual(p['central_gap_source_px'],4.752)
        self.assertAlmostEqual(p['central_gap_bust_px'],2.32848)
        self.assertEqual(p['endpoint_deltas_source_px'],[0,0])
    def test_static_mutations(self):
        rows=review.load(W/'plan.json');r=review.load(W/'state_checks.json')['records']
        r[3]['brow_geometry']['screen_left']['pivot_delta_source_px'][0]+=1
        r[3]['actual_mouth_side_delta_source_px'][1]+=1
        r[3]['lip_contour_offsets'][1]['lower_y']+=1
        checks=review.static_geometry_checks(rows,r,W/'rig')['assertions']
        self.assertFalse(checks['anchored_brow_geometry']);self.assertFalse(checks['symmetric_purse_width']);self.assertFalse(checks['common_corner_and_purse_lip_contour'])
    def test_all_static_anchors_grid_aligned(self):
        for name,i in review.STATIC_FRAMES.items():
            p=next(r['pose'] for r in review.load(W/'plan.json') if r['name']==name)
            expected=review.expected_pose(self.keys,i/30,self.records[0]['pose'])
            self.assertTrue(all(abs(v-p.get(k,0))<1e-12 for k,v in expected.items()))
        self.assertEqual(len(review.STATIC_FRAMES),8)
    def test_lip_geometry(self):
        p=review.expected_pose(self.keys,2,self.records[0]['pose'])
        self.assertEqual(review.lip_geometry(p,4),review.lip_geometry(p,75))
        self.assertAlmostEqual(review.lip_geometry(p,39.5)[1],4.752)
        self.assertEqual(review.lip_geometry(p,39.5)[0],0)
    def test_native_image_guards(self):
        with tempfile.TemporaryDirectory(prefix='exp161-unit-') as d:
            p=Path(d)/'synthetic.png'
            Image.new('RGBA',(400,360),(0,0,0,255)).save(p)
            self.assertEqual(review.read_png(p,(400,360)).shape,(360,400,4))
            with self.assertRaisesRegex(ValueError,'Native dimensions'):review.read_png(p,(568,800))
            Image.new('RGB',(400,360)).save(p)
            with self.assertRaisesRegex(ValueError,'Native pixel mode'):review.read_png(p,(400,360))
    def test_body_guard(self):
        m=np.zeros((800,568),dtype=bool);self.assertIsNone(review.bbox(m))
        m[300,250]=True;self.assertTrue(review.outside_face_unchanged(m));self.assertEqual(review.bbox(m),[250,300,251,301])
        m[500,250]=True;self.assertFalse(review.outside_face_unchanged(m))
    def fixture(self,transform=None):
        with tempfile.TemporaryDirectory(prefix='exp161-review-unit-') as d:
            root=Path(d);work=root/'sleepy_work';work.mkdir()
            skip={'capture','motion','motion_checks.json','review_evidence','Sleepy_review_v1.mp4','__pycache__'}
            for p in W.iterdir():
                if p.name not in skip:(work/p.name).symlink_to(p,target_is_directory=p.is_dir())
            for n in ['mental_arithmetic_work','controlled_anger_work','broad_surprise_work','puzzled_work','open_sobbing_work','mild_disgust_work']:
                (root/n).symlink_to(W.parent/n,target_is_directory=True)
            if transform:transform(work)
            before={n:review.sha(W/n) for n in review.load(W/'review_input_freeze.json')['files']}
            with contextlib.redirect_stdout(io.StringIO()):code=review.run(argparse.Namespace(work=work,output=root/'reports',video=None))
            result=review.load(root/'reports/review_checks.json')
            self.assertEqual(before,{n:review.sha(W/n) for n in before})
            return code,result
    def test_missing_native_is_pending(self):
        code,r=self.fixture();self.assertEqual(code,2);self.assertEqual(r['status'],'PENDING');self.assertEqual(r['failures'],[]);self.assertEqual(len(r['pending']),3);self.assertFalse(r['normal_speed_continuous_observation'])
    def test_changed_freeze_is_failure(self):
        def change(w):
            p=w/'review_input_freeze.json';d=review.load(p);p.unlink();d['status']='TEST ONLY';review.write(p,d)
        code,r=self.fixture(change);self.assertEqual(code,1);self.assertIn('expected_review_input_freeze_identity',r['failures'])
    def test_failed_static_receipt_is_not_hidden(self):
        def change(w):
            (w/'capture').mkdir();d=review.load(W/'state_checks.json');d.update(status='FAIL',visual_capture=True,checks=1590,failures=['TEST ONLY']);review.write(w/'capture/checks.json',d)
        code,r=self.fixture(change);self.assertEqual(code,1);self.assertIn('native_static_receipt_pass',r['failures'])
    def test_failed_motion_receipt_is_not_hidden(self):
        def change(w):
            d=review.load(W/'motion_state_checks.json');d.update(status='FAIL',visual_capture=True,checks=12125,display='TEST ONLY',renderer='TEST ONLY',failures=['TEST ONLY']);review.write(w/'motion_checks.json',d)
        code,r=self.fixture(change);self.assertEqual(code,1);self.assertIn('native_motion_receipt_pass',r['failures'])
if __name__=='__main__':unittest.main(verbosity=2)

"""Mutation tests for independent numerical checks, not generated artwork."""
import copy
import unittest
from pathlib import Path
import independent_geometry as audit
W=Path(__file__).resolve().parent
class AuditMutations(unittest.TestCase):
    def setUp(self):
        self.plan=audit.load(W/'plan.json');self.static=audit.load(W/'state_checks.json')
        self.motion=audit.load(W/'motion_state_checks.json');self.profile=audit.load(W/'EXP-104.json')
    def result(self):return audit.audit(self.plan,self.static,self.motion,self.profile)
    def test_actual_frozen_evidence_passes(self):self.assertEqual(self.result()['status'],'PASS')
    def test_lid_asymmetry_rejected(self):
        self.static['records'][3]['lash_geometry']['screen_left']['closure']=.18
        self.assertEqual(self.result()['status'],'FAIL')
    def test_brow_direction_rejected(self):
        self.static['records'][3]['brow_geometry']['screen_left']['rotation_degrees']=-1.76
        self.assertEqual(self.result()['status'],'FAIL')
    def test_unexpected_lip_corner_rejected(self):
        self.static['records'][3]['lip_contour_offsets'][2]['lower_y']+=3.84
        self.assertEqual(self.result()['status'],'FAIL')
    def test_peak_gap_mutation_rejected(self):
        self.motion['records'][48]['central_lip_gap_native_px']=9
        self.assertEqual(self.result()['status'],'FAIL')
    def test_smile_mismatch_rejected(self):
        self.motion['records'][48]['pose']['mouth_smile']=.1
        self.assertEqual(self.result()['status'],'FAIL')
    def test_gaze_drift_rejected(self):
        self.motion['records'][12]['pose']['gaze_x']=.01
        self.assertEqual(self.result()['status'],'FAIL')
    def test_frame_time_rejected(self):
        self.motion['records'][48]['time']=1.5
        self.assertEqual(self.result()['status'],'FAIL')
    def test_neutral_endpoint_drift_rejected(self):
        self.motion['records'][120]['pose']['mouth_open']=.01
        self.assertEqual(self.result()['status'],'FAIL')
    def test_lifecycle_evidence_change_rejected(self):
        self.motion['lifecycle_assertions']=32
        self.assertEqual(self.result()['status'],'FAIL')
    def test_sample_peak_analytic_values(self):
        p=self.motion['records'][48]['pose']
        self.assertAlmostEqual(audit.gap(p,39.5),8.91,places=6)
        self.assertAlmostEqual(audit.upper(p,75),-9.28368,places=6)
        self.assertAlmostEqual(audit.upper(p,4),-9.28368,places=6)
    def test_crooked_corner_bias_rejected(self):
        self.motion['records'][48]['pose']['mouth_corner_lift_screen_right']=.2
        self.assertEqual(self.result()['status'],'FAIL')
    def test_opposed_brow_height_rejected(self):
        self.motion['records'][48]['pose']['brow_screen_right']=.32
        self.assertEqual(self.result()['status'],'FAIL')
    def test_wrong_inward_tilt_rejected(self):
        self.motion['records'][48]['pose']['brow_tilt_screen_right']=.42
        self.assertEqual(self.result()['status'],'FAIL')
    def test_false_public_spread_geometry_rejected(self):
        p=self.static['records'][3]['pose']
        self.static['records'][3]['actual_mouth_side_delta_source_px']=[-20*p['mouth_spread'],20*p['mouth_spread']]
        self.assertEqual(self.result()['status'],'FAIL')
    def test_second_open_phase_gap_rejected(self):
        self.motion['records'][72]['central_lip_gap_native_px']=8.91
        self.assertEqual(self.result()['status'],'FAIL')
    def test_open_phase_larger_than_tooth_phase(self):
        p=self.motion['records'][48]['pose'];q=self.motion['records'][72]['pose']
        self.assertGreater(audit.gap(q,39.5),audit.gap(p,39.5))
        self.assertAlmostEqual(40*audit.effective_spread(p),28.896,places=5)
        self.assertAlmostEqual(40*audit.effective_spread(q),31.68,places=5)
if __name__=='__main__':unittest.main()

"""Read-only numerical mutation tests, not native visual evidence."""
import unittest
import independent_geometry as audit
from pathlib import Path
W=Path(__file__).resolve().parent
class AuditMutations(unittest.TestCase):
 def setUp(self):
  self.plan=audit.load(W/'plan.json');self.static=audit.load(W/'state_checks.json');self.motion=audit.load(W/'motion_state_checks.json');self.profile=audit.load(W/'EXP-045.json')
 def result(self):return audit.audit(self.plan,self.static,self.motion,self.profile)
 def test_current_evidence(self):self.assertEqual(self.result()['status'],'PASS')
 def test_brow_direction(self):
  self.static['records'][3]['brow_geometry']['screen_left']['rotation_degrees']=-4
  self.assertEqual(self.result()['status'],'FAIL')
 def test_lash_travel(self):
  self.static['records'][3]['lash_geometry']['screen_right']['pivot_delta_source_px'][1]+=1
  self.assertEqual(self.result()['status'],'FAIL')
 def test_actual_iris_offset(self):
  self.motion['records'][48]['iris_geometry']['screen_right']['sprite_delta_source_px'][0]-=1
  self.assertEqual(self.result()['status'],'FAIL')
 def test_static_iris_shader(self):
  self.static['records'][3]['iris_geometry']['screen_left']['iris_shader_offset_source_px'][0]=-12
  self.assertEqual(self.result()['status'],'FAIL')
 def test_active_aversion_lid_support(self):
  self.motion['records'][25]['pose']['blink_L']=.17
  self.assertEqual(self.result()['status'],'FAIL')
 def test_adjoining_zero_gaze_endpoint_support(self):
  self.profile['keyframes'][2]['values']['blink_R']=.17999
  self.assertEqual(self.result()['status'],'FAIL')
 def test_ordinary_gaze_conflict(self):
  self.motion['records'][48]['pose']['gaze_x']=.1
  self.assertEqual(self.result()['status'],'FAIL')
 def test_smile_eye_conflict(self):
  self.motion['records'][48]['pose']['eye_smile_L']=.1
  self.assertEqual(self.result()['status'],'FAIL')
 def test_opening_conflict(self):
  self.motion['records'][48]['pose']['opening_px']=1
  self.assertEqual(self.result()['status'],'FAIL')
 def test_unwanted_sneer(self):
  self.motion['records'][48]['pose']['mouth_corner_lift_screen_right']=.1
  self.assertEqual(self.result()['status'],'FAIL')
 def test_lip_geometry(self):
  self.static['records'][3]['lip_contour_offsets'][2]['lower_y']+=1
  self.assertEqual(self.result()['status'],'FAIL')
 def test_frame_order(self):
  self.motion['records'][48]['time']=1.5
  self.assertEqual(self.result()['status'],'FAIL')
 def test_neutral_drift(self):
  self.motion['records'][120]['pose']['mouth_open']=.01
  self.assertEqual(self.result()['status'],'FAIL')
 def test_lifecycle_count(self):
  self.motion['lifecycle_scoped_samples'].pop()
  self.assertEqual(self.result()['status'],'FAIL')
 def test_lifecycle_unsupported_aversion(self):
  row=next(r for r in self.motion['lifecycle_scoped_samples'] if r['pose']['aversion_px']>0 and r['stage']=='release')
  row['pose']['blink_L']=.17
  self.assertEqual(self.result()['status'],'FAIL')
 def test_lifecycle_numeric_drift(self):
  row=next(r for r in self.motion['lifecycle_scoped_samples'] if r['pose']['aversion_px']>1 and r['stage']=='restart')
  row['pose']['aversion_px']-=.1
  self.assertEqual(self.result()['status'],'FAIL')
 def test_peak_geometry(self):
  p=self.motion['records'][48]['pose'];self.assertEqual(p['aversion_px'],12)
  self.assertEqual(audit.gap(p,39.5),0);self.assertEqual(audit.upper(p,4),0);self.assertEqual(audit.upper(p,75),0)
 def test_scoped_boundary(self):
  self.assertTrue(audit.scoped_valid(dict(aversion_px=1e-15,blink_L=.18,blink_R=.18)))
  self.assertFalse(audit.scoped_valid(dict(aversion_px=1e-15,blink_L=.18-1e-12,blink_R=.18)))
if __name__=='__main__':unittest.main(verbosity=2)

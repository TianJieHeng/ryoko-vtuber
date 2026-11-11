"""Mutate headless numerical evidence; no native image or render claim."""
import unittest
from pathlib import Path
import independent_geometry as audit
W=Path(__file__).resolve().parent
class AuditTests(unittest.TestCase):
 def setUp(self):
  self.plan=audit.load(W/'plan.json');self.static=audit.load(W/'state_checks.json');self.motion=audit.load(W/'motion_state_checks.json');self.profile=audit.load(W/'EXP-096.json')
 def result(self):return audit.audit(self.plan,self.static,self.motion,self.profile)
 def fails(self):self.assertEqual(self.result()['status'],'FAIL')
 def test_current_evidence(self):self.assertEqual(self.result()['status'],'PASS')
 def test_brow_direction(self):
  self.static['records'][4]['brow_geometry']['screen_left']['rotation_degrees']=-5.2;self.fails()
 def test_horizontal_brow_drift(self):
  self.static['records'][4]['brow_geometry']['screen_right']['pivot_delta_source_px'][0]=1;self.fails()
 def test_lash_travel(self):
  self.static['records'][4]['lash_geometry']['screen_right']['pivot_delta_source_px'][1]+=1;self.fails()
 def test_iris_offset(self):
  self.motion['records'][48]['iris_geometry']['screen_left']['sprite_delta_source_px'][0]=1;self.fails()
 def test_static_iris_shader(self):
  self.static['records'][4]['iris_geometry']['screen_left']['iris_shader_offset_source_px'][0]=-1;self.fails()
 def test_peak_partial_lids(self):
  self.motion['records'][48]['pose']['blink_L']=.8;self.fails()
 def test_early_reopening_KP7(self):
  self.motion['records'][84]['pose']['blink_R']=.8;self.fails()
 def test_KP7_tension_retained(self):
  self.motion['records'][84]['pose']['mouth_lip_press']=.65;self.fails()
 def test_smile_eye(self):
  self.motion['records'][48]['pose']['eye_smile_L']=.1;self.fails()
 def test_mouth_open(self):
  self.motion['records'][48]['pose']['mouth_open']=.01;self.fails()
 def test_opening(self):
  self.motion['records'][48]['pose']['opening_px']=1;self.fails()
 def test_gaze(self):
  self.motion['records'][48]['pose']['gaze_x']=.1;self.fails()
 def test_aversion(self):
  self.motion['records'][48]['pose']['aversion_px']=1;self.fails()
 def test_unwanted_corner(self):
  self.motion['records'][48]['pose']['mouth_corner_lift_screen_right']=.1;self.fails()
 def test_excessive_purse(self):
  self.motion['records'][48]['pose']['mouth_purse']=.3;self.fails()
 def test_lip_geometry(self):
  self.static['records'][4]['lip_contour_offsets'][2]['lower_y']+=1;self.fails()
 def test_pressure_shader(self):
  self.static['records'][4]['pressure_owners'][0]['amount']=0;self.fails()
 def test_pressure_visibility(self):
  self.motion['records'][48]['pressure_owners'][0]['visible']=False;self.fails()
 def test_frame_order(self):
  self.motion['records'][48]['time']=1.5;self.fails()
 def test_neutral_drift(self):
  self.motion['records'][120]['pose']['mouth_open']=.01;self.fails()
 def test_lifecycle_count(self):
  self.motion['lifecycle_scoped_samples'].pop();self.fails()
 def test_lifecycle_asymmetry(self):
  row=next(r for r in self.motion['lifecycle_scoped_samples'] if r['pose']['blink_L']>.5 and r['stage']=='release');row['pose']['blink_L']=.17;self.fails()
 def test_lifecycle_numeric_drift(self):
  row=next(r for r in self.motion['lifecycle_scoped_samples'] if r['pose']['mouth_lip_press']>.1 and r['stage']=='restart');row['pose']['mouth_lip_press']-=.1;self.fails()
 def test_peak_geometry(self):
  p=self.motion['records'][48]['pose'];self.assertEqual(p['blink_L'],1);self.assertEqual(audit.gap(p,39.5),0);self.assertAlmostEqual(audit.upper(p,4),.6);self.assertAlmostEqual(audit.upper(p,39.5),.2)
 def test_scope_zero_exclusions(self):
  self.assertTrue(audit.scoped_valid(dict(blink_L=1,blink_R=1,mouth_purse=.05,mouth_lip_press=.65)))
  self.assertFalse(audit.scoped_valid(dict(blink_L=1,blink_R=1,mouth_open=.01)))
if __name__=='__main__':unittest.main(verbosity=2)

"""Read-only author guard tests. Synthetic temporary fixtures are not native evidence."""
import argparse,contextlib,copy,io,tempfile,unittest
from pathlib import Path
import numpy as np
from PIL import Image
import review_validation as review
W=Path(__file__).resolve().parent
class ReviewTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.keys=review.load(W/'EXP-096.json')['keyframes'];cls.records=review.load(W/'motion_state_checks.json')['records']
 def mutate(self,frame,key,value):
  r=copy.deepcopy(self.records);r[frame]['pose'][key]=value
  return review.timeline_checks(r,self.keys)['assertions']
 def test_current_timeline(self):self.assertTrue(all(review.timeline_checks(self.records,self.keys)['assertions'].values()))
 def test_exact_peak(self):
  p=review.expected_pose(self.keys,2,self.records[0]['pose'])
  self.assertEqual({k:v for k,v in p.items() if v},{'blink_R':1,'blink_L':1,'brow_screen_left':-.55,'brow_screen_right':-.55,'brow_tilt_screen_left':.65,'brow_tilt_screen_right':-.65,'mouth_lip_press':.65,'mouth_purse':.05})
 def test_out_of_order(self):
  r=copy.deepcopy(self.records);r[15],r[16]=r[16],r[15]
  with self.assertRaisesRegex(ValueError,'Incorrect frame'):review.timeline_checks(r,self.keys)
 def test_nonfinite(self):
  with self.assertRaisesRegex(ValueError,'Non-finite'):self.mutate(15,'mouth_purse',float('nan'))
 def test_partial_peak(self):self.assertFalse(self.mutate(48,'blink_R',.8)['fully_closed_peak'])
 def test_early_reopening(self):self.assertFalse(self.mutate(84,'blink_L',.8)['closed_through_KP7'])
 def test_no_KP7_softening(self):self.assertFalse(self.mutate(84,'mouth_lip_press',.65)['tension_softens_before_reopening'])
 def test_gaze(self):self.assertFalse(self.mutate(48,'gaze_x',.1)['no_opening_smile_corners_gaze_aversion'])
 def test_aversion(self):self.assertFalse(self.mutate(48,'aversion_px',1)['no_opening_smile_corners_gaze_aversion'])
 def test_smile_eye(self):self.assertFalse(self.mutate(48,'eye_smile_R',.1)['no_opening_smile_corners_gaze_aversion'])
 def test_opening(self):self.assertFalse(self.mutate(48,'opening_px',1)['no_opening_smile_corners_gaze_aversion'])
 def test_sneer(self):self.assertFalse(self.mutate(48,'mouth_corner_lift_screen_right',.1)['no_opening_smile_corners_gaze_aversion'])
 def test_pout(self):self.assertFalse(self.mutate(48,'mouth_purse',.3)['sealed_pressure_and_tiny_purse'])
 def test_brow_direction(self):self.assertFalse(self.mutate(48,'brow_screen_right',.55)['lowered_equal_brows'])
 def test_hold_changed(self):self.assertFalse(self.mutate(65,'mouth_lip_press',.6)['exact_peak_hold_48_through_72'])
 def test_neutral_drift(self):self.assertFalse(self.mutate(112,'mouth_open',.01)['neutral_hold_states'])
 def test_missing_channel(self):
  r=copy.deepcopy(self.records);del r[1]['pose']['mouth_lip_press']
  with self.assertRaisesRegex(ValueError,'Pose channel set changed'):review.timeline_checks(r,self.keys)
 def test_iris_geometry_mutated(self):
  r=copy.deepcopy(self.records);r[48]['iris_geometry']['screen_right']['iris_shader_offset_source_px'][0]=1
  self.assertFalse(review.timeline_checks(r,self.keys)['assertions']['actual_iris_sprite_and_shader_offsets'])
 def test_pressure_shader(self):
  r=copy.deepcopy(self.records);r[48]['pressure_owners'][0]['amount']=0
  self.assertFalse(review.timeline_checks(r,self.keys)['assertions']['actual_pressed_lip_owners'])
 def test_current_static_geometry(self):self.assertTrue(all(review.static_geometry_checks(review.load(W/'plan.json'),review.load(W/'state_checks.json')['records'],W/'rig')['assertions'].values()))
 def test_static_geometry_mutations(self):
  r=review.load(W/'state_checks.json')['records'];r[4]['brow_geometry']['screen_left']['pivot_delta_source_px'][0]=1;r[4]['iris_geometry']['screen_left']['sprite_delta_source_px'][0]=-1
  tests=review.static_geometry_checks(review.load(W/'plan.json'),r,W/'rig')['assertions']
  self.assertFalse(tests['anchored_brow_geometry']);self.assertFalse(tests['actual_aversion_offsets'])
 def test_all_anchors_on_grid(self):
  for n,i in review.STATIC_FRAMES.items():
   p=next(r['pose'] for r in review.load(W/'plan.json') if r['name']==n)
   self.assertTrue(all(abs(v-p.get(k,0))<1e-12 for k,v in review.expected_pose(self.keys,i/30,self.records[0]['pose']).items()))
 def test_native_dimensions(self):
  with tempfile.TemporaryDirectory(prefix='exp096-unit-') as d:
   p=Path(d)/'synthetic.png';Image.new('RGBA',(400,360)).save(p)
   self.assertEqual(review.read_png(p,(400,360)).shape,(360,400,4))
   with self.assertRaisesRegex(ValueError,'Native dimensions'):review.read_png(p,(568,800))
   Image.new('RGB',(400,360)).save(p)
   with self.assertRaisesRegex(ValueError,'Native pixel mode'):review.read_png(p,(400,360))
 def test_body_guard(self):
  m=np.zeros((800,568),dtype=bool);m[300,250]=True;self.assertTrue(review.outside_face_unchanged(m));m[500,250]=True;self.assertFalse(review.outside_face_unchanged(m))
 def fixture(self,transform=None):
  with tempfile.TemporaryDirectory(prefix='exp096-review-unit-') as d:
   root=Path(d);work=root/'headache_tension_work';work.mkdir()
   skip={'capture','motion','motion_checks.json','review_evidence','Headache_tension_review_v1.mp4','__pycache__'}
   for p in W.iterdir():
    if p.name not in skip:(work/p.name).symlink_to(p,target_is_directory=p.is_dir())
   for n in ['mental_arithmetic_work','controlled_anger_work','broad_surprise_work','puzzled_work','open_sobbing_work','mild_disgust_work','sleepy_work','irritated_side_eye_work','triumphant_grin_work']:(root/n).symlink_to(W.parent/n,target_is_directory=True)
   if transform:transform(work)
   before={n:review.sha(W/n) for n in review.load(W/'review_input_freeze.json')['files']}
   with contextlib.redirect_stdout(io.StringIO()):code=review.run(argparse.Namespace(work=work,output=root/'reports',video=None))
   r=review.load(root/'reports/review_checks.json')
   self.assertEqual(before,{n:review.sha(W/n) for n in before});return code,r
 def test_missing_native_pending(self):
  code,r=self.fixture();self.assertEqual(code,2);self.assertEqual(r['status'],'PENDING');self.assertEqual(r['failures'],[]);self.assertEqual(len(r['pending']),3);self.assertFalse(r['normal_speed_continuous_observation'])
 def test_changed_freeze_failure(self):
  def change(w):
   p=w/'review_input_freeze.json';d=review.load(p);p.unlink();d['status']='TEST ONLY';review.write(p,d)
  code,r=self.fixture(change);self.assertEqual(code,1);self.assertIn('expected_review_input_freeze_identity',r['failures'])
 def test_failed_static_not_hidden(self):
  def change(w):
   (w/'capture').mkdir();d=review.load(W/'state_checks.json');d.update(status='FAIL',visual_capture=True,failures=['TEST ONLY']);review.write(w/'capture/checks.json',d)
  code,r=self.fixture(change);self.assertEqual(code,1);self.assertIn('native_static_receipt_pass',r['failures'])
 def test_failed_motion_not_hidden(self):
  def change(w):
   d=review.load(W/'motion_state_checks.json');d.update(status='FAIL',visual_capture=True,display='TEST ONLY',renderer='TEST ONLY',failures=['TEST ONLY']);review.write(w/'motion_checks.json',d)
  code,r=self.fixture(change);self.assertEqual(code,1);self.assertIn('native_motion_receipt_pass',r['failures'])
if __name__=='__main__':unittest.main(verbosity=2)

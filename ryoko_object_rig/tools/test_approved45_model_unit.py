"""Unit/negative checks of the explicitly limited Python controller model."""
import copy,unittest
from approved45_model import *
def definition(id='T',channel='mouth_open',value=.4,duration=1.):
 return {'id':id,'duration':duration,'keyframes':[{'time':0.,'values':{}},{'time':duration*.5,'values':{channel:value}},{'time':duration,'values':{}}]}
class ModelUnit(unittest.TestCase):
 def setUp(self):self.d=definition();self.m=Model({'T':self.d,'W':definition('W','mouth_width_screen_left',.6),'O':definition('O','opening_px',3.)})
 def test_sample_zero(self):self.assertEqual(sample(self.d,0),neutral())
 def test_sample_negative(self):self.assertEqual(sample(self.d,-1),neutral())
 def test_sample_end(self):self.assertEqual(sample(self.d,1),neutral())
 def test_sample_after(self):self.assertEqual(sample(self.d,2),neutral())
 def test_sample_peak(self):self.assertEqual(sample(self.d,.5)['mouth_open'],.4)
 def test_sample_independent_polynomial(self):
  for i in range(1001):
   t=i/1000;u=t/.5 if t<.5 else (1-t)/.5
   self.assertAlmostEqual(sample(self.d,t)['mouth_open'],.4*(3*u*u-2*u*u*u),places=14)
 def test_sample_omissions_zero(self):self.assertTrue(all(v==0 for k,v in sample(self.d,.5).items() if k!='mouth_open'))
 def test_scoped_opening_reject(self):self.assertFalse(scoped_valid({'opening_px':1,'blink_L':.1}))
 def test_scoped_aversion_low_lids(self):self.assertFalse(scoped_valid({'aversion_px':1,'blink_L':.179999,'blink_R':.18}))
 def test_scoped_aversion_exact_lids(self):self.assertTrue(scoped_valid({'aversion_px':1,'blink_L':.18,'blink_R':.18}))
 def test_scoped_uneasy_open(self):self.assertFalse(scoped_valid({'uneasy_weight':1,'mouth_open':.1}))
 def test_mouth_width_open(self):self.assertFalse(mouth_valid({'mouth_width_screen_left':.1,'mouth_open':.1}))
 def test_mouth_kiss_open(self):self.assertFalse(mouth_valid({'mouth_kiss':.1,'mouth_open':.1}))
 def test_mouth_width_sealed(self):self.assertTrue(mouth_valid({'mouth_width_screen_left':.1,'mouth_open':0}))
 def test_mouth_width_staged(self):
  self.m.play('W');self.m.advance(.5);before=self.m.pose.copy();self.m.play('T');self.assertEqual(self.m.mode,'staged');self.assertEqual(self.m.pose,before)
  self.m.advance(.15);self.assertTrue(all(self.m.pose[k]==0 for k in TRIO));self.m.advance(.01);self.assertTrue(mouth_valid(self.m.pose))
 def test_mouth_open_to_width_staged(self):self.m.play('T');self.m.advance(.5);self.m.play('W');self.assertEqual(self.m.mode,'staged')
 def test_mouth_width_direct(self):self.m.play('W');self.m.advance(.5);self.m.play('W');self.assertEqual(self.m.mode,'bounded_direct')
 def test_mouth_legacy(self):self.m.play('T');self.assertEqual(self.m.mode,'legacy')
 def test_opening_bridge(self):
  self.m.pose['blink_L']=.5;self.m.play('O');self.assertTrue(self.m.opening_bridge)
  for i in range(101):self.m.advance(.003);self.assertTrue(scoped_valid(self.m.pose))
 def test_scoped_handoff_source_stage(self):
  p=neutral();p['aversion_px']=4;p['blink_L']=p['blink_R']=.2;q=scoped_handoff(p,neutral(),.25);self.assertEqual(q['aversion_px'],2);self.assertEqual(q['blink_L'],.2)
 def test_release_continuity(self):self.m.play('T');self.m.advance(.5);p=self.m.pose.copy();self.m.release();self.assertEqual(self.m.pose,p)
 def test_repeated_release_continuity(self):self.m.play('T');self.m.advance(.5);self.m.release();self.m.advance(.2);p=self.m.pose.copy();self.m.release();self.assertEqual(self.m.pose,p)
 def test_blink_restore(self):self.m.auto_blink=True;self.m.play('T');self.assertTrue(self.m.pending);self.assertFalse(self.m.auto_blink);self.m.advance(1);self.assertTrue(self.m.auto_blink);self.assertFalse(self.m.pending)
 def test_reset_disables_blink(self):self.m.auto_blink=True;self.m.play('T');self.m.reset();self.assertFalse(self.m.auto_blink or self.m.pending)
 def test_manual_cancels_intent(self):self.m.auto_blink=True;self.m.play('T');self.m.advance(.5);self.m.manual_takeover();self.assertFalse(self.m.pending or self.m.auto_blink)
 def test_invalid_delta_transaction(self):
  self.m.play('T');before=copy.deepcopy(self.m.__dict__)
  for d in [-1,float('nan'),float('inf'),True,None,'1']:self.assertFalse(self.m.advance(d));self.assertEqual(self.m.__dict__,before)
 def test_unknown_id_transaction(self):
  self.m.play('T');before=copy.deepcopy(self.m.__dict__);self.assertFalse(self.m.play('EXP-046'));self.assertEqual(self.m.__dict__,before)
 def test_definitions_copied(self):self.m.play('T');self.d['keyframes'][1]['values']['mouth_open']=1;self.assertEqual(self.m.performance['keyframes'][1]['values']['mouth_open'],.4)
if __name__=='__main__':unittest.main()

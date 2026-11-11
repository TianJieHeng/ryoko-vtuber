"""Stdlib-only tests. No renderer, image synthesis, native tools or network."""
import ast
import copy
import hashlib
import json
import math
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import author_once
import encode_preflight as encoder
import numeric_model as m

class CandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.profile=m.load(m.W/'EXP-091.json')
    def test_definition(self):self.assertTrue(m.valid_definition(self.profile))
    def test_author_reproduces_profile(self):self.assertEqual(author_once.build()['EXP-091.json'],self.profile)
    def test_author_reproduces_plan(self):self.assertEqual(author_once.build()['plan.json'],m.load(m.W/'plan.json'))
    def test_author_reproduces_map(self):self.assertEqual(author_once.build()['SOURCE_MAP.json'],m.load(m.W/'SOURCE_MAP.json'))
    def test_approved39_registry_excludes_091(self):
        ids=[r['id'] for r in m.load(m.W/'rig/expressions/registry.json')['entries']]
        self.assertEqual(len(ids),39);self.assertNotIn('EXP-091',ids)
    def test_bounds_rejected(self):
        for key,value in [('mouth_purse',1.01),('mouth_open',-.01),('mouth_smile',True),('blink_L',float('nan')),('eye_smile_R',float('inf')),('made_up_control',0)]:
            with self.subTest(key=key):
                p=copy.deepcopy(self.profile);p['keyframes'][4]['values'][key]=value
                with self.assertRaises(ValueError):m.valid_definition(p)
    def test_unsupported_parts_rejected(self):
        for key in ['mouth_kiss','opening_px','gaze_x','hair_sway','mouth_width_screen_left']:
            p=copy.deepcopy(self.profile);p['keyframes'][4]['values'][key]=.01
            with self.assertRaises(ValueError):m.valid_definition(p)
    def test_bad_timeline_rejected(self):
        for value in [-.1,True,float('nan'),.55,5.]:
            p=copy.deepcopy(self.profile);p['keyframes'][3]['time']=value
            with self.assertRaises(ValueError):m.valid_definition(p)
    def test_non_neutral_end_rejected(self):
        p=copy.deepcopy(self.profile);p['keyframes'][-1]['values']={'mouth_purse':.01}
        with self.assertRaises(ValueError):m.valid_definition(p)
    def test_exact_peak(self):
        p=m.sample(self.profile,1.65);g=m.geometry(p)
        self.assertEqual(g['eye_curved_shape'],1);self.assertEqual(g['eye_effective_closure'],1)
        self.assertEqual(p['blink_L'],0);self.assertEqual(p['mouth_open'],0)
        self.assertAlmostEqual(g['mouth_width_source_px'],49.16)
        self.assertAlmostEqual(g['lip_samples'][0]['upper_y']-g['lip_samples'][1]['upper_y'],-.84)
    def test_intake_precedes_sealed_peak(self):
        self.assertEqual(m.sample(self.profile,.55)['mouth_open'],.07)
        for i in range(27,121):self.assertEqual(m.sample(self.profile,i/30)['mouth_open'],0)
    def test_curve_and_brow_not_generic_warm_smile(self):
        p=m.sample(self.profile,1.65)
        self.assertGreater(p['brow_inner_lift_screen_left'],.3)
        self.assertGreater(p['mouth_purse'],.7);self.assertLess(p['mouth_smile'],.2)
        self.assertEqual(p['mouth_spread'],0)
        self.assertEqual(m.load(m.W/'STATUS.json')['source_fidelity'],'PENDING_NATIVE_REVIEW')
    def test_dense_independent_sampler(self):
        for i in range(4001):
            a=m.sample(self.profile,i/1000);b=m.independent_sample(self.profile,i/1000)
            self.assertTrue(all(abs(a[k]-b[k])<1e-12 for k in m.CHANNELS))
    def test_cubic_join_velocity(self):
        h=1e-7
        for key in self.profile['keyframes'][1:-1]:
            t=key['time'];before=m.sample(self.profile,t-h);at=m.sample(self.profile,t);after=m.sample(self.profile,t+h)
            for k in m.CHANNELS:
                self.assertLess(abs((at[k]-before[k])/h),1e-4)
                self.assertLess(abs((after[k]-at[k])/h),1e-4)
    def test_lifecycle_continuity_and_release(self):
        for t in m.INTERRUPTIONS:
            p=m.Lifecycle(self.profile);p.trigger();p.advance(t);source=dict(p.pose)
            p.trigger();self.assertEqual(p.pose,source);p.advance(.3)
            self.assertEqual(p.pose,m.sample(self.profile,.3))
            p=m.Lifecycle(self.profile);p.trigger();p.advance(t);p.release()
            self.assertEqual(p.pose,source);p.advance(.45);self.assertEqual(p.pose,m.neutral())
    def test_reset_during_release(self):
        p=m.Lifecycle(self.profile);p.trigger();p.advance(1.8);p.release();p.advance(.1);p.reset()
        self.assertEqual(p.pose,m.neutral());p.advance(1);self.assertEqual(p.pose,m.neutral())
    def test_manual_takeover(self):
        p=m.Lifecycle(self.profile);p.trigger();p.advance(1.8)
        p.manual({'blush_intensity':.2});state=dict(p.pose);p.advance(10)
        self.assertEqual(p.pose,state);self.assertEqual(p.mode,'manual')
    def test_invalid_manual_is_atomic(self):
        p=m.Lifecycle(self.profile);p.trigger();p.advance(1.8);before=(dict(p.pose),p.mode,p.t)
        with self.assertRaises(ValueError):p.manual({'mouth_open':2})
        self.assertEqual((p.pose,p.mode,p.t),before)
    def test_invalid_delta_is_atomic(self):
        for dt in [-1,float('nan'),float('inf'),True]:
            p=m.Lifecycle(self.profile);p.trigger();p.advance(.9);before=(dict(p.pose),p.mode,p.t)
            with self.assertRaises(ValueError):p.advance(dt)
            self.assertEqual((p.pose,p.mode,p.t),before)
    def test_completed_play_returns_neutral(self):
        p=m.Lifecycle(self.profile);p.trigger();p.advance(8)
        self.assertEqual(p.pose,m.neutral());self.assertEqual(p.mode,'manual')
    def test_same_profile_zero_distance(self):self.assertEqual(m.numerical_distance(self.profile,self.profile)['rms'],0)
    def test_distance_stable_under_key_order(self):
        q=m.load(m.W/'comparators/EXP-160.json');r=copy.deepcopy(q)
        for frame in r['keyframes']:frame['values']=dict(reversed(list(frame['values'].items())))
        self.assertEqual(m.numerical_distance(self.profile,q),m.numerical_distance(self.profile,r))
    def test_compare_four_critical_profiles(self):
        for id in ['197','160','090','096']:
            r=m.numerical_distance(self.profile,m.load(m.W/f'comparators/EXP-{id}.json'))
            self.assertGreater(r['rms'],0);self.assertEqual(r['perceptual_distinctness'],'PENDING')
    def test_runtime_equations_static_contract(self):
        runtime=(m.W/'rig/expression_rig.gd').read_text()
        for text in ['const RESTART_SECONDS=0.30','const RELEASE_SECONDS=0.45','u=u*u*(3-2*u)','restart_pose=displayed_pose()','release_pose=displayed_pose()']:
            self.assertIn(text,runtime)
        face=(m.W/'rig/object_face.gd').read_text()
        for text in ['minf(amount*2.0,1.0)','clampf((amount-.5)*2.0,0.0,1.0)','-14.0*mouth_purse/35.5']:
            self.assertIn(text,face)
    def test_native_guard_disabled(self):self.assertIn('const NATIVE_EXECUTION_ALLOWED=false',(m.W/'native_capture.gd').read_text())
    def test_no_native_receipts_or_mp4(self):
        self.assertFalse((m.W/'capture').exists());self.assertFalse((m.W/encoder.OUTPUT).exists())
    def test_encoder_missing_evidence_refused(self):
        with self.assertRaisesRegex(ValueError,'fresh native captures absent'):encoder.validate_capture()
    def test_encoder_never_executes_program(self):
        tree=ast.parse((m.W/'encode_preflight.py').read_text())
        imports=[n.name for node in ast.walk(tree) if isinstance(node,(ast.Import,ast.ImportFrom)) for n in node.names]
        self.assertNotIn('subprocess',imports);self.assertNotIn('os',imports)
        self.assertNotIn('exec(', (m.W/'encode_preflight.py').read_text())
    def test_freeze_read_only(self):
        before={p:m.sha(p) for p in m.W.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
        m.verify_freeze()
        self.assertTrue(all(m.sha(p)==h for p,h in before.items()))
    def test_stale_freeze_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            w=Path(tmp);(w/'data').write_text('changed')
            (w/'INPUT_FREEZE.json').write_text(json.dumps({'files':{'data':'0'*64}}))
            with self.assertRaisesRegex(ValueError,'Frozen input mismatch'):m.verify_freeze(w)
    def test_native_metadata_guards(self):
        good={'status':'PASS','failures':[],'visual_capture':True,'display':'native','renderer':'gl',
          'input_freeze_sha256':m.sha(m.W/'INPUT_FREEZE.json'),'profile_sha256':m.sha(m.W/'EXP-091.json'),
          'frames':121,'fps':30,'duration':4.,'baseline_profile_count':39,'records':[{}]*121,
          'static_records':[{}]*9,'lifecycle_records':[{}]*270}
        for key,value in [('status','FAIL'),('failures',['bad']),('visual_capture',False),('display','headless'),
                ('renderer',''),('input_freeze_sha256','old'),('profile_sha256','old'),('frames',120),('fps',60),
                ('duration',3.9),('baseline_profile_count',36),('records',[]),('static_records',[]),('lifecycle_records',[])]:
            r=copy.deepcopy(good);r[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):encoder.validate_metadata(m.W,r)
    def test_png_non_png_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'x.png';p.write_bytes(b'not a PNG')
            with self.assertRaises(ValueError):encoder.read_rgba(p)
    def test_reference_not_native_frame(self):
        p=next((m.W/'reference').glob('*sheet*.png'))
        with self.assertRaises(ValueError):encoder.read_rgba(p)
    def test_validator_fails_on_frozen_input_change(self):
        with patch.object(m,'sha',return_value='changed'):
            with self.assertRaises(ValueError):m.verify_freeze()

if __name__=='__main__':unittest.main()

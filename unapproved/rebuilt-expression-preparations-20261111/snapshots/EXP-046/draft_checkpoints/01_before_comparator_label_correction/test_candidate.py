"""Pure Python/static tests only. No engine, renderer, FFmpeg or network is invoked."""
import copy
import hashlib
import json
import math
import unittest
from pathlib import Path
from unittest.mock import patch
import trajectory_model as m
import encode_preview as e
import freeze_candidate as f
W=Path(__file__).resolve().parent
class NumericalTests(unittest.TestCase):
    def test_profile_schema_and_bounds(self):self.assertTrue(m.validate_profile(m.PROFILE))
    def test_reject_bad_profiles(self):
        for key,value in [('gaze_y',-1.01),('mouth_open',float('nan')),('blink_L',True),('invented_anatomy',1),('mouth_smile',.1)]:
            p=copy.deepcopy(m.PROFILE);p['keyframes'][3]['values'][key]=value
            with self.subTest(key=key),self.assertRaises(AssertionError):m.validate_profile(p)
    def test_exclusion_and_trajectory_bounds(self):
        for i in range(4801):
            p=m.sample(i/1000)
            self.assertTrue(m.valid_pose(p));self.assertTrue(all(p[k]==0 for k in set(m.CHANNELS)-m.ACTING))
            self.assertEqual(p['blink_L'],p['blink_R']);self.assertLessEqual(p['blink_L'],.5)
            self.assertGreaterEqual(p['gaze_y'],-1);self.assertLessEqual(p['gaze_y'],0)
    def test_smoothstep_known_values_and_midpoint(self):
        self.assertEqual([m.smooth(v) for v in [0,.25,.5,.75,1]],[0,.15625,.5,.84375,1])
        a=m.sample(.7);b=m.sample(1.15);mid=m.sample((.7+1.15)/2)
        for k in m.CHANNELS:self.assertAlmostEqual(mid[k],(a[k]+b[k])/2,places=12)
    def test_boundary_neutral_and_exact_anchors(self):
        self.assertEqual(m.sample(-1),m.neutral());self.assertEqual(m.sample(99),m.neutral())
        for row in m.PROFILE['keyframes']:
            for k,v in m.sample(row['time']).items():self.assertAlmostEqual(v,row['values'].get(k,0),places=12)
        for t in [0,.15,.3,4.5,4.65,4.8]:self.assertEqual(m.sample(t),m.neutral())
    def test_glance_precedes_exhale_without_smile(self):
        glance=m.sample(1.5);exhale=m.sample(2.25)
        self.assertEqual(glance['gaze_y'],-1);self.assertEqual(exhale['gaze_y'],0)
        self.assertEqual(exhale['mouth_open'],.5);self.assertEqual(exhale['blink_L'],.5)
        self.assertLess(glance['mouth_open'],exhale['mouth_open'])
        for t in [2.25,2.7,3.15,3.7]:self.assertEqual(m.sample(t)['gaze_y'],0)
        self.assertEqual(m.sample(3.7)['mouth_open'],0)
    def test_source_geometry_contract(self):
        glance=m.geometry(m.sample(1.5));peak=m.geometry(m.sample(2.25))
        self.assertEqual(glance['gaze_source_px'],[0.,-2.]);self.assertAlmostEqual(peak['central_gap_source_px'],14.46)
        self.assertEqual(peak['lash_source_px'],{'screen_left':18.,'screen_right':18.})
        self.assertAlmostEqual(peak['brows']['screen_left']['angle_degrees'],-13.52)
        self.assertAlmostEqual(peak['brows']['screen_right']['angle_degrees'],13.52)
        manifests=json.loads((W/'rig/rig_assets/object_face/manifest.json').read_text())['objects']
        for side,anchor in [('screen_left',(466.550,452.350)),('screen_right',(646.227,453.773))]:
            pivot=manifests['brow_'+side]['pivot'];g=peak['brows'][side]
            r=m.rotate((anchor[0]-pivot[0],anchor[1]-pivot[1]),math.radians(g['angle_degrees']))
            tail=[pivot[i]+g['pivot_delta_source_px'][i]+r[i] for i in [0,1]]
            self.assertAlmostEqual(tail[0],anchor[0]);self.assertAlmostEqual(tail[1],anchor[1]+.7)
    def test_frame_series_deterministic(self):
        a=m.expected_frames();b=m.expected_frames();self.assertEqual(a,b)
        stored=json.loads((W/'EXPECTED_TRAJECTORY.json').read_text());self.assertEqual(a,stored['records'])
        self.assertEqual(len(a),145);self.assertEqual(a[-1]['time'],4.8)
        self.assertEqual(a[0]['pose'],a[-1]['pose'])
        for row,prior in zip(a[1:],a):
            self.assertLess(max(abs(row['pose'][k]-prior['pose'][k]) for k in m.ACTING),.13)
    def test_lifecycle_continuity_and_eventual_neutral(self):
        for t in m.INTERRUPTIONS:
            for action in ['play','release','reset']:
                p=m.Player();p.play();p.advance(t);before=p.pose.copy();getattr(p,action)()
                if action=='reset':self.assertEqual(p.pose,m.neutral());continue
                self.assertEqual(p.pose,before)
                for _ in range(145):self.assertTrue(m.valid_pose(p.advance(1/30)))
                self.assertEqual(p.pose,m.neutral());self.assertFalse(p.active);self.assertEqual(p.release_time,-1)
    def test_release_formula_and_reset_after_release_retrigger(self):
        p=m.Player();p.play();p.advance(2.25);before=p.pose.copy();p.release();p.advance(.225)
        for k in m.CHANNELS:self.assertAlmostEqual(p.pose[k],before[k]/2)
        before=p.pose.copy();p.play();self.assertEqual(p.pose,before);p.advance(.15)
        for k in m.CHANNELS:self.assertAlmostEqual(p.pose[k],before[k]/2)
        p.reset();self.assertEqual(p.pose,m.neutral());self.assertFalse(p.active)
    def test_invalid_delta_transactional(self):
        p=m.Player();p.play();p.advance(1.5)
        for value in [-1,float('nan'),float('inf'),True,'0.1']:
            before=copy.deepcopy(p.__dict__)
            with self.assertRaises(ValueError):p.advance(value)
            self.assertEqual(p.__dict__,before)
    def test_control_distinctness_is_not_visual_distinctness(self):
        peak=m.sample(2.25);glance=m.sample(1.5)
        for expression in ['EXP-007','EXP-050','EXP-093']:
            other=json.loads((W/'rig/expressions'/f'{expression}.json').read_text())
            self.assertNotEqual(m.PROFILE['keyframes'],other['keyframes'])
            self.assertTrue(all(row['values'].get('gaze_y',0)!=glance['gaze_y'] or row['values'].get('mouth_open',0)!=glance['mouth_open'] for row in other['keyframes']))
        self.assertGreater(peak['mouth_open'],0);self.assertEqual(peak['mouth_smile'],0)
class PreservationTests(unittest.TestCase):
    def test_frozen_input_identity(self):f.verify()
    def test_approved39_and_096_preserved(self):
        baseline=json.loads((W/'BASELINE_FREEZE.json').read_text());recovery=W.parent.parent
        self.assertEqual(len(baseline['baseline_files_sha256']),1124)
        for rel,digest in baseline['baseline_files_sha256'].items():self.assertEqual(f.sha(recovery/'main/ryoko_object_rig'/rel),digest,rel)
        self.assertEqual(len(json.loads((W/'rig/expressions/registry.json').read_text())['entries']),39)
        self.assertFalse((W/'rig/expressions/EXP-046.json').exists())
        self.assertEqual(f.sha(recovery/'headache_review_backup/EXP-096-headache-tension/historical/EXP-096.json'),baseline['headache_profile_sha256'])
    def test_no_native_claim_or_capture(self):
        self.assertFalse((W/'native_capture').exists());self.assertFalse(list(W.glob('*.mp4')))
        guard=json.loads((W/'LAUNCH_CLEARANCE.json').read_text());self.assertFalse(guard['cleared'])
        self.assertEqual(guard['state'],'DENIED_PENDING_RESOLUTION')
    def test_native_preparation_is_guarded_not_verified(self):
        text=(W/'native_capture.gd').read_text()
        self.assertLess(text.index('Outstanding project-launch denial'),text.index('rig = load('))
        self.assertIn('Headless/state-only execution is not native capture evidence',text)
    def test_pinned_sampler_formulas_static_only(self):
        text=(W/'rig/expression_rig.gd').read_text()
        for token in ['const RESTART_SECONDS=0.30','const RELEASE_SECONDS=0.45','u=u*u*(3-2*u)','time>=definition.duration','restart_pose=displayed_pose()']:self.assertIn(token,text)
        limits=(W/'rig/control_limits.gd').read_text();self.assertIn('const GAZE_UP_PIXELS=2.0',limits);self.assertIn('const BROW_INNER_LIFT_DEGREES=26.0',limits)
class EncoderGuardTests(unittest.TestCase):
    def fixture(self):
        # Deliberately synthetic metadata in memory only; never saved as native evidence.
        records=[dict(frame=r['frame'],time=r['time'],pose=r['pose'],hashes=['0'*64,'1'*64]) for r in m.expected_frames()]
        return dict(status='PASS',checks=1,failures=[],visual_capture=True,profile_sha256=f.sha(W/'EXP-046.json'),freeze_sha256=f.sha(W/'CANDIDATE_FREEZE.json'),expected_sha256=f.sha(W/'EXPECTED_TRAJECTORY.json'),baseline_profile_count=39,production_registry_unchanged=True,frames=145,fps=30,duration=4.8,approval='UNAPPROVED',display='synthetic-unit-test',renderer='synthetic-unit-test',records=records,static_records=[dict(name=r['name'],pose={**m.neutral(),**r['pose']},hashes=['0'*64,'1'*64]) for r in json.loads((W/'plan.json').read_text())],lifecycle_records=[dict(interruption_time=t,retrigger_steps=145,release_steps=16,reset_checked=True) for t in m.INTERRUPTIONS])
    def test_missing_capture_never_invokes_subprocess(self):
        with patch.object(e.subprocess,'run') as run,patch.object(e.subprocess,'check_output') as probe:
            with self.assertRaisesRegex(ValueError,'Native capture NOT RUN'):e.validate_capture()
            run.assert_not_called();probe.assert_not_called()
    def test_metadata_rejects_invalid_or_stale_receipts(self):
        good=self.fixture();e.validate_metadata(good)
        for key,value in [('status','FAIL'),('visual_capture',False),('checks',0),('display','headless'),('renderer',''),('profile_sha256','wrong'),('freeze_sha256','wrong'),('expected_sha256','wrong'),('baseline_profile_count',40),('production_registry_unchanged',False),('frames',144),('fps',60),('duration',4.9),('approval','APPROVED'),('records',[]),('static_records',[]),('lifecycle_records',[])]:
            bad=copy.deepcopy(good);bad[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):e.validate_metadata(bad)
    def test_metadata_rejects_frame_time_pose_hash_errors(self):
        for mutation in ['order','time','pose','hash','neutral']:
            bad=self.fixture()
            if mutation=='order':bad['records'][3]['frame']=4
            if mutation=='time':bad['records'][3]['time']=float('nan')
            if mutation=='pose':bad['records'][3]['pose']['gaze_y']=-99
            if mutation=='hash':bad['records'][3]['hashes']=['x','y']
            if mutation=='neutral':bad['records'][-1]['hashes'][0]='2'*64
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):e.validate_metadata(bad)
if __name__=='__main__':unittest.main(verbosity=2)

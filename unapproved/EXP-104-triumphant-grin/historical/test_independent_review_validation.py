"""Reviewer-owned mutation tests. Synthetic fixtures stay in temporary directories.
They are test bytes only, never native artwork or approval evidence.
"""
import contextlib
import copy
import hashlib
import io
import json
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import patch
import numpy as np
from PIL import Image
import independent_review_validation as v

W = Path(__file__).resolve().parent
load = lambda n: json.loads((W/n).read_text())


class ContractAndMathTests(unittest.TestCase):
    def setUp(self):
        self.profile = load('EXP-104.json')
        self.plan = load('plan.json')
        self.records = load('motion_state_checks.json')['records']
        self.static = load('state_checks.json')['records']

    def timeline(self):
        return v.timeline_checks(self.records, self.profile['keyframes'])['assertions']

    def geometry(self):
        return v.static_geometry_checks(self.plan, self.static, W/'rig')['assertions']

    def test_01_frozen_contract_and_numeric_records_pass(self):
        self.assertTrue(all(v.contract_checks(self.profile,self.plan).values()))
        self.assertTrue(all(self.timeline().values()))
        self.assertTrue(all(self.geometry().values()))

    def test_02_timeline_key_mutation_rejected_independently(self):
        self.profile['keyframes'][4]['values']['mouth_open'] = .31
        self.assertFalse(v.contract_checks(self.profile,self.plan)['independent_key_vectors'])

    def test_03_anchor_mutation_rejected(self):
        self.plan[3]['pose']['mouth_smile'] = .82
        self.assertFalse(v.contract_checks(self.profile,self.plan)['independent_static_vectors'])

    def test_04_changed_timing_rejected(self):
        self.profile['keyframes'][5]['time'] = 2.01
        self.assertFalse(v.contract_checks(self.profile,self.plan)['independent_eleven_key_times'])

    def test_05_anchor_reorder_rejected(self):
        self.plan[1],self.plan[2] = self.plan[2],self.plan[1]
        self.assertFalse(v.contract_checks(self.profile,self.plan)['independent_eight_anchor_names'])

    def test_06_asymmetric_lids_rejected(self):
        self.records[48]['pose']['blink_L'] += .01
        self.assertFalse(self.timeline()['equal_focused_ordinary_lids'])

    def test_07_asymmetric_brows_rejected(self):
        self.records[48]['pose']['brow_screen_right'] = -.3
        self.assertFalse(self.timeline()['equal_lowered_brows'])

    def test_08_outward_brow_tilt_rejected(self):
        self.records[48]['pose']['brow_tilt_screen_right'] = .42
        self.assertFalse(self.timeline()['mirrored_inward_tilts'])

    def test_09_downcast_gaze_rejected(self):
        self.records[48]['pose']['gaze_y'] = .05
        self.assertFalse(self.timeline()['fixed_forward_gaze'])

    def test_10_independent_corner_rejected(self):
        self.records[48]['pose']['mouth_corner_lift_screen_left'] = .1
        self.assertFalse(self.timeline()['only_nine_authorized_channels_act'])

    def test_11_shallow_hold_mutation_rejected(self):
        self.records[54]['pose']['mouth_smile'] = .83
        self.assertFalse(self.timeline()['exact_shallow_hold_frames_48_through_60'])

    def test_12_open_grin_mutation_rejected(self):
        self.records[72]['pose']['mouth_open'] = .3
        self.assertFalse(self.timeline()['independent_later_open_vector'])

    def test_13_reseal_must_precede_smile_release(self):
        self.records[96]['pose']['mouth_open'] = .01
        self.assertFalse(self.timeline()['reseal_precedes_final_smile_and_brow_release'])

    def test_14_neutral_drift_rejected(self):
        self.records[-1]['pose']['mouth_smile'] = .0001
        self.assertFalse(self.timeline()['neutral_hold_states'])

    def test_15_nonfinite_pose_rejected(self):
        self.records[50]['pose']['mouth_open'] = float('nan')
        with self.assertRaises(ValueError): self.timeline()

    def test_16_frame_reorder_rejected(self):
        self.records[40],self.records[41] = self.records[41],self.records[40]
        with self.assertRaises(ValueError): self.timeline()

    def test_17_missing_pose_channel_rejected(self):
        del self.records[20]['pose']['gaze_x']
        with self.assertRaises(ValueError): self.timeline()

    def test_18_missing_frame_rejected(self):
        self.records.pop()
        with self.assertRaises(ValueError): self.timeline()

    def test_19_gap_mutation_rejected(self):
        self.records[48]['central_lip_gap_native_px'] = 8.9
        self.assertFalse(self.timeline()['all_recorded_gaps_match_math'])

    def test_20_brow_translation_mutation_rejected(self):
        self.static[3]['brow_geometry']['screen_left']['pivot_delta_source_px'][1] += .1
        self.assertFalse(self.geometry()['anchored_brow_geometry'])

    def test_21_outer_anchor_mutation_rejected(self):
        self.static[3]['brow_geometry']['screen_right']['outer_anchor'][0] += 1
        self.assertFalse(self.geometry()['anchored_brow_geometry'])

    def test_22_brow_rotation_mutation_rejected(self):
        self.static[3]['brow_geometry']['screen_left']['rotation_degrees'] *= -1
        self.assertFalse(self.geometry()['anchored_brow_geometry'])

    def test_23_lash_travel_mutation_rejected(self):
        self.static[3]['lash_geometry']['screen_left']['pivot_delta_source_px'][1] += .1
        self.assertFalse(self.geometry()['blink_sides_and_lash_travel'])

    def test_24_raw_spread_instead_of_smile_product_rejected(self):
        self.static[3]['actual_mouth_side_delta_source_px'] = [-20*.86,20*.86]
        self.assertFalse(self.geometry()['smile_coupled_spread'])

    def test_25_lip_contour_mutation_rejected(self):
        self.static[3]['lip_contour_offsets'][2]['lower_y'] += .1
        self.assertFalse(self.geometry()['symmetric_upper_lower_lips'])

    def test_26_independent_peak_geometry_constants(self):
        p = v.anchor_pose('tooth_grin')
        self.assertAlmostEqual(v.lip_geometry(p,39.5)[1]-v.lip_geometry(p,39.5)[0],8.91)
        self.assertAlmostEqual(v.lip_geometry(p,4)[0],-9.28368)
        self.assertAlmostEqual(v.lip_geometry(p,75)[0],-9.28368)
        self.assertAlmostEqual(40*p['mouth_smile']*p['mouth_spread'],28.896)
        q = v.anchor_pose('open_grin')
        self.assertAlmostEqual(v.lip_geometry(q,39.5)[1]-v.lip_geometry(q,39.5)[0],13.662)
        self.assertAlmostEqual(40*q['mouth_smile']*q['mouth_spread'],31.68)


class PixelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base = np.zeros((800,568,4),dtype=np.uint8); base[:,:,3]=255
        active = base.copy(); active[300:305,250:255,:3]=100
        cls.arrays = [base if i<=6 or i>=111 else active for i in range(121)]
        cls.hashes = [[hashlib.sha256(a.tobytes()).hexdigest(),'detail-placeholder'] for a in cls.arrays]
        cls.static = {name:cls.arrays[i] for name,i in v.STATIC_FRAMES.items()}

    def checks(self,arrays=None,hashes=None,static=None):
        return v.native_pixel_checks(arrays or self.arrays, hashes or self.hashes, 'full', self.static if static is None else static)['assertions']

    def test_27_valid_synthetic_native_contract(self):
        self.assertTrue(all(self.checks().values()))

    def test_28_hash_mismatch_rejected(self):
        h=copy.deepcopy(self.hashes); h[50][0]='0'*64
        self.assertFalse(self.checks(hashes=h)['rgba_receipt_50'])

    def test_29_body_drift_rejected(self):
        a=list(self.arrays); a[50]=a[50].copy();a[50][700,200,0]=1
        self.assertFalse(self.checks(arrays=a)['fixed_body_pixels'])

    def test_30_neutral_drift_rejected(self):
        a=list(self.arrays);a[-1]=a[-1].copy();a[-1][300,250,0]=1
        self.assertFalse(self.checks(arrays=a)['neutral_holds'])

    def test_31_broken_hold_rejected(self):
        a=list(self.arrays);a[54]=a[54].copy();a[54][300,250,0]=1
        self.assertFalse(self.checks(arrays=a)['shallow_hold'])

    def test_32_static_anchor_mismatch_rejected(self):
        s=dict(self.static);s['open_grin']=self.arrays[0]
        self.assertFalse(self.checks(static=s)['static_anchor_open_grin'])

    def test_33_static_anchor_set_mismatch_rejected(self):
        s=dict(self.static);s.pop('settle')
        self.assertFalse(self.checks(static=s)['exact_static_anchor_set'])

    def test_34_no_expression_rejected(self):
        a=[self.arrays[0]]*121
        self.assertFalse(self.checks(arrays=a)['nontrivial_expression'])

    def test_35_wrong_array_dimensions_rejected(self):
        a=list(self.arrays);a[20]=a[20][:-1]
        with self.assertRaises(ValueError): self.checks(arrays=a)

    def test_36_wrong_array_count_rejected(self):
        with self.assertRaises(ValueError): self.checks(arrays=self.arrays[:-1])

    def test_37_rgb_png_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.png';Image.new('RGB',(400,360)).save(p)
            with self.assertRaisesRegex(ValueError,'pixel mode'):v.read_png(p,(400,360))

    def test_38_wrong_png_dimensions_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.png';Image.new('RGBA',(399,360)).save(p)
            with self.assertRaisesRegex(ValueError,'dimensions'):v.read_png(p,(400,360))


class VideoTests(unittest.TestCase):
    def setUp(self):
        self.probe={'streams':[{'codec_name':'h264','pix_fmt':'yuv420p','width':968,'height':800,'r_frame_rate':'30/1','nb_frames':'121','nb_read_frames':'121'}], 'format':{'duration':str(121/30)}}
        self.pts=[{'best_effort_timestamp_time':str(i/30)} for i in range(121)]
        self.errors={'full':[1.]*121,'detail':[1.]*121}
        self.nearest=[{'expected_minus_best':0.,'expected_face_mae':1.} for i in range(121)]

    def test_39_video_contract_passes(self):
        self.assertTrue(all(v.video_metadata_checks(self.probe,self.pts).values()))
        self.assertTrue(all(v.video_similarity_checks(self.errors,self.nearest).values()))

    def test_40_wrong_video_count_rejected(self):
        self.probe['streams'][0]['nb_frames']='120'
        self.assertFalse(v.video_metadata_checks(self.probe,self.pts)['geometry_count'])

    def test_41_wrong_video_geometry_rejected(self):
        self.probe['streams'][0]['width']=960
        self.assertFalse(v.video_metadata_checks(self.probe,self.pts)['geometry_count'])

    def test_42_wrong_video_timing_rejected(self):
        self.pts[60]['best_effort_timestamp_time']='2.04'
        self.assertFalse(v.video_metadata_checks(self.probe,self.pts)['all_30fps_pts'])

    def test_43_video_wrong_codec_rejected(self):
        self.probe['streams'][0]['codec_name']='mpeg4'
        self.assertFalse(v.video_metadata_checks(self.probe,self.pts)['encoding_duration'])

    def test_44_missing_decoded_comparison_rejected(self):
        self.errors['full'].pop()
        self.assertFalse(v.video_similarity_checks(self.errors,self.nearest)['complete_comparisons'])

    def test_45_reordered_frame_similarity_rejected(self):
        self.nearest[60]['expected_minus_best']=.11
        self.assertFalse(v.video_similarity_checks(self.errors,self.nearest)['no_material_reorder'])

    def test_46_nonfinite_similarity_rejected(self):
        self.errors['detail'][40]=float('nan')
        self.assertFalse(v.video_similarity_checks(self.errors,self.nearest)['same_index_native_similarity'])

    def test_47_nearest_face_order_identifies_swap(self):
        features=np.stack([np.zeros((2,2,3)),np.ones((2,2,3))*100]).astype(np.float32)
        r=v.frame_order_comparison(features,features[1],0)
        self.assertEqual(r['best_matching_frame'],1)
        self.assertEqual(r['expected_minus_best'],100.)

    def test_48_identical_holds_remain_ambiguous(self):
        features=np.zeros((2,2,2,3),dtype=np.float32)
        self.assertEqual(v.frame_order_comparison(features,features[1],1)['expected_minus_best'],0)

    def test_49_full_decode_reads_every_frame(self):
        proc=SimpleNamespace(stdout=io.BytesIO(bytes(range(18))),wait=lambda timeout:0,poll=lambda:0)
        with patch.object(v.subprocess,'Popen',return_value=proc):
            r={};frames=list(v.decode_rgb_frames(Path('unused-test.mp4'),1,2,r))
        self.assertEqual(len(frames),3);self.assertEqual(r['frames'],3);self.assertEqual(r['exit_code'],0)

    def test_50_partial_decode_rejected(self):
        proc=SimpleNamespace(stdout=io.BytesIO(b'12345'),wait=lambda timeout:0,poll=lambda:0)
        with patch.object(v.subprocess,'Popen',return_value=proc):
            with self.assertRaisesRegex(ValueError,'Incomplete decoded frame'):list(v.decode_rgb_frames(Path('unused-test.mp4'),1,2,{}))


class PendingAndFreezeTests(unittest.TestCase):
    def fixture(self,root):
        # Frozen read-only inputs are symlinked; native fixtures/output stay local.
        for p in W.iterdir():
            if p.name in ['rig','native_launcher'] or p.name in load('review_input_freeze.json')['files'] or p.name=='review_input_freeze.json':
                (root/p.name).symlink_to(p,target_is_directory=p.is_dir())
        (root/'development_audit').symlink_to(W/'development_audit',target_is_directory=True)

    def execute(self,root):
        with contextlib.redirect_stdout(io.StringIO()):
            code=v.run(SimpleNamespace(work=root,output=None,video=None))
        return code,json.loads((root/'independent_review_evidence/review_checks.json').read_text())

    def test_51_missing_native_is_pending_not_pass(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.fixture(root);code,r=self.execute(root)
        self.assertEqual(code,2);self.assertEqual(r['status'],'PENDING');self.assertFalse(r['independent_checks_pass']);self.assertFalse(r['normal_speed_continuous_observation']);self.assertFalse(r['failures'])

    def test_52_wrong_author_contract_refused(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'review_input_freeze.json').write_text('{}')
            code,r=self.execute(root)
        self.assertEqual(code,1);self.assertIn('digest mismatch',r['failures'][0])

    def test_53_changed_pinned_file_refused(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.fixture(root);(root/'EXP-104.json').unlink();(root/'EXP-104.json').write_text('{}')
            code,r=self.execute(root)
        self.assertEqual(code,1);self.assertIn('Pinned author input',r['failures'][0])

    def test_54_headless_static_cannot_count_as_native(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.fixture(root);(root/'capture').mkdir();(root/'capture/checks.json').write_text((W/'state_checks.json').read_text());code,r=self.execute(root)
        self.assertEqual(code,1);self.assertIn('native_static_receipt_pass',r['failures'])

    def test_55_headless_motion_cannot_count_as_native(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.fixture(root);(root/'motion_checks.json').write_text((W/'motion_state_checks.json').read_text());code,r=self.execute(root)
        self.assertEqual(code,1);self.assertIn('native_motion_receipt_pass',r['failures'])

    def test_56_extra_motion_filename_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.fixture(root);(root/'motion/full').mkdir(parents=True);(root/'motion/full/0121.png').write_bytes(b'not native');code,r=self.execute(root)
        self.assertEqual(code,1);self.assertIn('no_unexpected_motion_pngs_full',r['failures'])

    def test_57_stale_native_profile_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.fixture(root);motion=load('motion_state_checks.json');motion['profile_sha256']='0'*64;(root/'motion_checks.json').write_text(json.dumps(motion));code,r=self.execute(root)
        self.assertEqual(code,1);self.assertIn('native_motion_receipt_tied_to_frozen_inputs',r['failures'])

    def test_58_protected_output_refused(self):
        with self.assertRaisesRegex(ValueError,'protected input trees'):
            v.run(SimpleNamespace(work=W,output=W/'rig/reviewer',video=None))


if __name__=='__main__':unittest.main()

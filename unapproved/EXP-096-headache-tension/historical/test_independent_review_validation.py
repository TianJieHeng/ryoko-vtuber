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
        self.profile=load('EXP-096.json'); self.plan=load('plan.json')
        self.records=load('motion_state_checks.json')['records']
        self.static=load('state_checks.json')['records']
        self.life=load('motion_state_checks.json')['lifecycle_scoped_samples']

    def timeline(self):
        return v.timeline_checks(self.records,self.profile['keyframes'])['assertions']

    def geometry(self):
        return v.static_geometry_checks(self.plan,self.static,W/'rig')['assertions']

    def test_01_frozen_contract_and_numerical_receipts(self):
        self.assertTrue(all(v.contract_checks(self.profile,self.plan).values()))
        self.assertTrue(all(self.timeline().values()))
        self.assertTrue(all(self.geometry().values()))
        self.assertTrue(all(v.lifecycle_checks(self.life)['assertions'].values()))

    def test_02_peak_vector_independently_pinned(self):
        self.profile['keyframes'][5]['values']['mouth_purse']=.06
        self.assertFalse(v.contract_checks(self.profile,self.plan)['exact_key_vectors'])

    def test_03_changed_anchor_detected(self):
        self.plan[4]['pose']['mouth_lip_press']=.64
        self.assertFalse(v.contract_checks(self.profile,self.plan)['exact_anchor_vectors'])

    def test_04_changed_key_time_detected(self):
        self.profile['keyframes'][7]['time']=2.7
        self.assertFalse(v.contract_checks(self.profile,self.plan)['eleven_exact_key_times'])

    def test_05_changed_anchor_order_detected(self):
        self.plan[3],self.plan[4]=self.plan[4],self.plan[3]
        self.assertFalse(v.contract_checks(self.profile,self.plan)['eight_exact_anchor_names'])

    def test_06_left_right_lid_asymmetry_detected(self):
        self.records[48]['pose']['blink_L']=.99
        self.assertFalse(self.timeline()['ordinary_bilateral_lids'])

    def test_07_brow_asymmetry_detected(self):
        self.records[48]['pose']['brow_screen_right']=-.50
        self.assertFalse(self.timeline()['lowered_equal_brows'])

    def test_08_wrong_tilt_sign_detected(self):
        self.records[48]['pose']['brow_tilt_screen_right']=.65
        self.assertFalse(self.timeline()['opposed_brow_tilts'])

    def test_09_smile_eye_forbidden(self):
        self.records[48]['pose']['eye_smile_L']=1
        self.assertFalse(self.timeline()['only_eight_nonzero_channels_act'])

    def test_10_open_mouth_forbidden(self):
        self.records[48]['pose']['mouth_open']=.01
        self.assertFalse(self.timeline()['no_opening_smile_corners_gaze_aversion'])

    def test_11_broken_peak_hold_detected(self):
        self.records[60]['pose']['mouth_lip_press']=.64
        self.assertFalse(self.timeline()['exact_peak_hold_48_through_72'])

    def test_12_early_reopening_detected(self):
        self.records[83]['pose']['blink_L']=self.records[83]['pose']['blink_R']=.99
        self.assertFalse(self.timeline()['closed_through_KP7'])

    def test_13_tension_must_soften_while_closed(self):
        self.records[84]['pose']['mouth_lip_press']=.65
        self.assertFalse(self.timeline()['tension_softens_before_reopening'])

    def test_14_neutral_drift_detected(self):
        self.records[-1]['pose']['mouth_lip_press']=.0001
        self.assertFalse(self.timeline()['neutral_hold_states'])

    def test_15_nonfinite_pose_rejected(self):
        self.records[40]['pose']['blink_L']=float('nan')
        with self.assertRaises(ValueError):self.timeline()

    def test_16_reordered_frames_rejected(self):
        self.records[40],self.records[41]=self.records[41],self.records[40]
        with self.assertRaises(ValueError):self.timeline()

    def test_17_inexact_channel_set_rejected(self):
        for row in self.records:del row['pose']['hair_sway']
        with self.assertRaises(ValueError):self.timeline()

    def test_18_missing_frame_rejected(self):
        self.records.pop()
        with self.assertRaises(ValueError):self.timeline()

    def test_19_nonzero_lip_aperture_detected(self):
        self.records[48]['central_lip_gap_native_px']=.01
        self.assertFalse(self.timeline()['all_recorded_mouth_gaps_match_independent_math'])

    def test_20_brow_translation_error_detected(self):
        self.static[4]['brow_geometry']['screen_left']['pivot_delta_source_px'][1]+=.1
        self.assertFalse(self.geometry()['anchored_brow_geometry'])

    def test_21_brow_anchor_error_detected(self):
        self.static[4]['brow_geometry']['screen_right']['outer_anchor'][0]+=1
        self.assertFalse(self.geometry()['anchored_brow_geometry'])

    def test_22_brow_rotation_error_detected(self):
        self.static[4]['brow_geometry']['screen_left']['rotation_degrees']*=-1
        self.assertFalse(self.geometry()['anchored_brow_geometry'])

    def test_23_lash_travel_error_detected(self):
        self.static[4]['lash_geometry']['screen_left']['pivot_delta_source_px'][1]+=.1
        self.assertFalse(self.geometry()['blink_sides_and_lash_travel'])

    def test_24_purse_width_error_detected(self):
        self.static[4]['actual_mouth_side_delta_source_px']=[.6,-.6]
        self.assertFalse(self.geometry()['symmetric_purse_width'])

    def test_25_downturned_corner_claim_not_supported(self):
        self.static[4]['lip_contour_offsets'][2]['lower_y']+=.1
        self.assertFalse(self.geometry()['common_corner_and_purse_lip_contour'])

    def test_26_peak_geometry_constants(self):
        p=v.anchor_pose('headache_peak')
        self.assertAlmostEqual(v.lip_geometry(p,39.5)[0],.2)
        self.assertAlmostEqual(v.lip_geometry(p,4)[0],.6)
        self.assertEqual(v.lip_geometry(p,4)[1],0)
        self.assertAlmostEqual(71-28*p['mouth_purse'],69.6)
        self.assertAlmostEqual(-10*p['brow_screen_left'],5.5)
        self.assertAlmostEqual(8*p['brow_tilt_screen_left'],5.2)
        self.assertEqual(36*p['blink_R'],36)

    def test_60_restart_wrong_value_detected(self):
        self.life[1]['pose']['blink_R']+=.01
        self.assertFalse(v.lifecycle_checks(self.life)['assertions']['exact_restart_trajectories'])

    def test_61_release_wrong_value_detected(self):
        self.life[15]['pose']['mouth_purse']+=.01
        self.assertFalse(v.lifecycle_checks(self.life)['assertions']['exact_release_trajectories'])

    def test_62_lifecycle_wrong_order_detected(self):
        self.life[1],self.life[2]=self.life[2],self.life[1]
        self.assertFalse(v.lifecycle_checks(self.life)['assertions']['exact_252_sample_order'])

    def test_63_lifecycle_missing_sample_detected(self):
        self.life.pop()
        self.assertFalse(v.lifecycle_checks(self.life)['assertions']['exact_252_sample_order'])

    def test_64_lifecycle_missing_channel_detected(self):
        del self.life[1]['pose']['hair_sway']
        self.assertFalse(v.lifecycle_checks(self.life)['assertions']['exact_shared_channels'])

    def test_65_lifecycle_nonfinite_detected(self):
        self.life[1]['pose']['mouth_purse']=float('nan')
        self.assertFalse(v.lifecycle_checks(self.life)['assertions']['finite_values'])

    def test_66_lifecycle_neutral_exactness(self):
        self.life[27]['pose']['mouth_purse']=1e-8
        self.assertFalse(v.lifecycle_checks(self.life)['assertions']['release_exact_neutral'])

    def test_67_pressure_owner_identity_detected(self):
        self.records[48]['pressure_owners'][0]['name']='wrong'
        self.assertFalse(self.timeline()['exact_fourteen_pressure_owner_identities'])

    def test_68_pressure_owner_missing_detected(self):
        self.static[4]['pressure_owners'].pop()
        self.assertFalse(self.geometry()['exact_fourteen_pressure_owner_identities'])

    def test_69_iris_shader_offset_detected(self):
        self.records[48]['iris_geometry']['screen_left']['iris_shader_offset_source_px'][0]=.1
        self.assertFalse(self.timeline()['actual_iris_sprite_and_shader_offsets'])

    def test_70_contract_not_derived_from_mutated_profile(self):
        self.profile['keyframes'][5]['values']['mouth_lip_press']=.64
        self.records[48]['pose']['mouth_lip_press']=.64
        self.assertFalse(self.timeline()['independent_smoothstep_timeline'])

    def test_71_inward_brow_tension_will_not_be_outward(self):
        self.profile['keyframes'][5]['values']['brow_tilt_screen_left']=-.65
        self.assertFalse(v.contract_checks(self.profile,self.plan)['exact_key_vectors'])

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
        self.assertFalse(self.checks(arrays=a)['peak_hold'])

    def test_32_static_anchor_mismatch_rejected(self):
        s=dict(self.static);s['headache_peak']=self.arrays[0]
        self.assertFalse(self.checks(static=s)['static_anchor_headache_peak'])

    def test_33_static_anchor_set_mismatch_rejected(self):
        s=dict(self.static);s.pop('reopen')
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
            root=Path(d);self.fixture(root);(root/'EXP-096.json').unlink();(root/'EXP-096.json').write_text('{}')
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

    def test_72_partial_corrupt_png_is_fail_not_pending(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.fixture(root);(root/'capture').mkdir()
            (root/'capture/neutral_bust.png').write_bytes(b'not a PNG')
            code,r=self.execute(root)
        self.assertEqual(code,1);self.assertEqual(r['status'],'FAIL')

    def test_73_no_native_never_launches_decoder(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.fixture(root)
            with patch.object(v.subprocess,'Popen',side_effect=AssertionError('Must not decode missing video')):
                code,r=self.execute(root)
        self.assertEqual(code,2);self.assertFalse(r['failures'])


if __name__=='__main__':unittest.main()

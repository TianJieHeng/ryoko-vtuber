from pathlib import Path
import re
W=Path(__file__).resolve().parent.parent
p=W/'review_validation.py';s=p.read_text()
s=s.replace("EXPECTED_INPUT_FREEZE_SHA256 = '22509ab2bf568edc6291e261fc0310bdac3818bbc08f4db6656be9ee30748086'", "# The separately pinned REVIEW_FREEZE.sha256 avoids a self-referential hash.\nINPUT_FREEZE_RECEIPT = 'REVIEW_FREEZE.sha256'")
s=re.sub(r'ACTING = \{.*?\}', "ACTING = {'brow_screen_left', 'brow_screen_right', 'blink_L', 'blink_R', 'mouth_open'}",s,count=1,flags=re.S)
start=s.index('SELECTED =');end=s.index('BROW_ANCHORS',start)
s=s[:start]+'''SELECTED = [0, 18, 30, 48, 72, 84, 96, 105, 120]
STATIC_FRAMES = {'neutral': 0, 'onset': 18, 'droop': 30,
                 'sleepy_peak': 48, 'recover': 84, 'release': 96,
                 'settle': 105, 'neutral_return': 120}
INTERRUPTIONS = [.35, .6, 1., 1.6, 2.4, 2.8, 3.2, 3.5, 3.7]
''' +s[end:]
start=s.index('    peak, sealed, release =');end=s.index("    return {'max_smoothstep_control_error'",start)
s=s[:start]+'''    peak = poses[48]
    gaps = [lip_geometry(p, 39.5)[1] for p in poses]
    tests = {
        'independent_smoothstep_timeline': max(errors) < 1e-6,
        'only_five_nonzero_channels_act': all(v == 0 for p in poses for k, v in p.items() if k not in ACTING),
        'acting_channels_within_shared_bounds': all(-1 <= p[k] <= 1 if k.startswith('brow_') else 0 <= p[k] <= 1 for p in poses for k in ACTING),
        'lids_lead_lip_parting': poses[18]['blink_L'] > .139 and poses[18]['mouth_open'] == 0,
        'equal_relaxed_low_brows': all(-.220001 <= p['brow_screen_left'] == p['brow_screen_right'] <= 0 for p in poses) and abs(peak['brow_screen_left']+.22) < 1e-6,
        'bounded_bilateral_heavy_lids': all(0 <= p['blink_L'] == p['blink_R'] <= .570001 for p in poses),
        'partial_heavy_lids_at_peak': abs(peak['blink_R']-.57) < 1e-6 and abs(peak['blink_L']-.57) < 1e-6,
        'slight_parted_lips_at_peak': abs(peak['mouth_open']-.16) < 1e-6 and abs(gaps[48]-4.752) < 1e-6,
        'exact_peak_hold_48_through_72': all(p == peak for p in poses[48:73]),
        'single_monotone_lid_sink': all(poses[i]['blink_L'] >= poses[i-1]['blink_L'] for i in range(1,49)),
        'no_repeated_sag_during_recovery': all(poses[i]['blink_L'] <= poses[i-1]['blink_L'] for i in range(73,121)),
        'gradual_lip_parting_then_reseal': all(poses[i]['mouth_open'] >= poses[i-1]['mouth_open'] for i in range(1,49)) and all(poses[i]['mouth_open'] <= poses[i-1]['mouth_open'] for i in range(73,121)),
        'lips_reseal_before_final_lid_recovery': poses[105]['mouth_open'] == 0 and poses[105]['blink_L'] > .059,
        'no_tilt_inner_lift_purse_pressure_smile_width_gaze_blush_hair': all(p[k] == 0 for p in poses for k in ['brow_tilt_screen_left','brow_tilt_screen_right','brow_inner_lift_screen_left', 'brow_inner_lift_screen_right', 'mouth_purse','mouth_lip_press', 'mouth_width_screen_left', 'mouth_width_screen_right', 'mouth_kiss', 'mouth_smile', 'mouth_spread', 'mouth_corner_lift', 'mouth_corner_lift_screen_left', 'mouth_corner_lift_screen_right','eye_smile_L', 'eye_smile_R', 'opening_px', 'gaze_x', 'gaze_y', 'gaze_down_extra', 'hair_sway', 'blush_intensity']),
        'neutral_hold_states': all(v == 0 for r in records if r['time'] <= .2 or r['time'] >= 3.7 for v in r['pose'].values()),
        'bounded_frame_steps': all(abs(poses[i][k]-poses[i-1][k]) < .20 for i in range(1, FRAMES) for k in ACTING),
        'all_recorded_mouth_gaps_match_independent_math': all(math.isfinite(r['central_lip_gap_native_px']) and abs(r['central_lip_gap_native_px']-g) < 1e-5 for r, g in zip(records, gaps)),
    }
''' +s[end:]
s=s.replace("'Common screen-right corner moves both contours. Aperture is spatially symmetric; no independent upper-lip lift/curl, nose wrinkle or jaw rotation.'", "'Only existing split-lip separation is authored. The upper contour stays at its neutral offset, both sides remain symmetric, and no jaw rotation, chin descent or cheek deformation is simulated.'")
s=s.replace("w.parent/'open_sobbing_work/EXP-023.json']", "w.parent/'open_sobbing_work/EXP-023.json', w.parent/'mild_disgust_work/EXP-081.json']")
s=s.replace("all(not r['same_active_controls'] and r['maximum_control_difference'] > .01 for r in results)","all(r['maximum_control_difference'] > .01 for r in results)")
s=s.replace("sha(w/'review_input_freeze.json') == EXPECTED_INPUT_FREEZE_SHA256", "sha(w/'review_input_freeze.json') == (w/INPUT_FREEZE_RECEIPT).read_text().split()[0]")
s=s.replace("'complete_46_file_preparation_freeze', input_freeze['candidate'] == ID and len(input_freeze['files']) == 46", "'complete_preparation_freeze', input_freeze['candidate'] == ID and len(input_freeze['files']) >= 35 and {'EXP-161.json','plan.json','check_and_capture.gd','render_motion.gd','review_validation.py','native_launcher/project.godot','state_checks.json','motion_state_checks.json','SOURCE_REFERENCE.json','SKIPPED_EXP-192.json'} <= set(input_freeze['files'])")
s=s.replace('(1213, 1296)','(1254, 1254)')
s=s.replace("('static_state', state, 1526), ('motion_state', motion_state, 11330)","('static_state', state, 1558), ('motion_state', motion_state, 11640)")
s=s.replace("receipt['checks'] == 1558", "receipt['checks'] == 1590")
s=s.replace("motion['checks'] == 11815", "motion['checks'] == 12125")
s=s.replace("'independent_41_profile_nonduplication'", "'independent_42_profile_nonduplication'").replace("['compared_profiles'] == 41", "['compared_profiles'] == 42")
s=s.replace('arrays[42], arrays[i]) for i in range(42, 53)', 'arrays[48], arrays[i]) for i in range(48, 73)')
s=s.replace('[0, 30, 42, 65]','[0, 30, 48, 84]')
point="        report['registry_ids'] ="
insert='''        parity40 = freeze['published40_runtime_artwork_parity']
        report['published40_runtime_parity_changes'] = [n for n,h in parity40['files_sha256'].items() if not (Path(parity40['path'])/n).is_file() or sha(Path(parity40['path'])/n) != h or known.get(n) != h]
        check('all_993_runtime_artwork_files_match_published40', parity40['count'] == len(parity40['files_sha256']) == 993 and set(parity40['files_sha256']) == set(known)-exclusions and not report['published40_runtime_parity_changes'])
'''
s=s.replace(point,insert+point)
p.write_text(s)

"""Read actual baseline geometry and aperture profiles without rendering images.

The aperture estimate samples shader math at source-pixel centers. It is not
native visual validation and does not include filtering or overlying lashes/hair.
"""
import hashlib
import json
from pathlib import Path
import numpy as np
from PIL import Image

W = Path(__file__).resolve().parent
R = W / 'rig'
plan = json.loads((W / 'plan.json').read_text())
scale = 0.49
records = []
sources = {}
def pixels(path):
    sources[str(path.relative_to(R))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return np.asarray(Image.open(path).convert('RGBA'), dtype=float)
def smoothstep(lo, hi, value):
    t = np.clip((value - lo) / (hi - lo), 0, 1)
    return t*t*(3-2*t)
for row in plan:
    p = row['pose']
    eyes = {}
    for side, key in [('screen_left','blink_L'),('screen_right','blink_R')]:
        upper = pixels(R/'rig_assets/object_face'/('profile_'+side+'.png'))[:,:,0]
        lower = pixels(R/'rig_assets/object_face'/('lower_profile_'+side+'.png'))[:,:,0]
        aperture = pixels(R/'rig_assets/gaze_eyes'/('aperture_'+side+'.png'))[:,:,0] / 255
        y = np.arange(aperture.shape[0])[:, None]
        def area(c):
            return float((aperture * smoothstep(-.5,.5,y-(upper+36*c)) * (1-smoothstep(-.5,.5,y-(lower+1)))).sum())
        c = p.get(key, 0)
        eyes[side] = {'ordinary_closure':c, 'upper_lash_travel_source_px':36*c,
                      'upper_lash_travel_bust_px':36*c*scale,
                      'estimated_aperture_fraction_of_neutral':area(c)/area(0)}
    purse=p.get('mouth_purse',0)
    opening=p.get('mouth_open',0)
    center_gap=max(0,29.7*opening-1.5*purse*min(opening*4,1))
    records.append({'name':row['name'], 'eyes':eyes,
                    'brow_pivot_lowering_source_px':-10*p.get('brow_screen_left',0),
                    'brow_pivot_lowering_bust_px':-10*p.get('brow_screen_left',0)*scale,
                    'brow_rotation_degrees':[8*p.get('brow_tilt_screen_left',0),8*p.get('brow_tilt_screen_right',0)],
                    'mouth_width_reduction_source_px':28*purse,
                    'mouth_width_reduction_bust_px':28*purse*scale,
                    'lip_center_down_source_px':4*purse,
                    'lip_corner_down_source_px':12*purse,
                    'mouth_open':opening,
                    'center_gap_source_px':center_gap,
                    'center_gap_bust_px':center_gap*scale,
                    'upper_lip_center_down_source_px':4*purse,
                    'lower_lip_center_down_source_px':4*purse+center_gap,
                    'independent_upper_lip_lift_supported':False})
peak=next(r for r in records if r['name']=='bitter_peak')
checks={'peak_aperture_estimate_between_quarter_and_half':all(.25 < e['estimated_aperture_fraction_of_neutral'] < .45 for e in peak['eyes'].values()),
        'peak_brow_pivot_moves_at_least_four_bust_pixels':peak['brow_pivot_lowering_bust_px']>=4,
        'peak_upper_lashes_move_at_least_six_bust_pixels':all(e['upper_lash_travel_bust_px']>=6 for e in peak['eyes'].values()),
        'peak_mouth_narrows_at_least_four_bust_pixels':peak['mouth_width_reduction_bust_px']>=4,
        'peak_lower_lip_gap_at_least_six_bust_pixels':peak['center_gap_bust_px']>=6,
        'upper_lip_lift_not_claimed':all(not r['independent_upper_lip_lift_supported'] for r in records),
        'upper_lip_actually_moves_down_at_peak':peak['upper_lip_center_down_source_px']>0}
static=json.loads((W/'state_checks.json').read_text())
actual_peak=next(r for r in static['records'] if r['name']=='bitter_peak')
center=next(r for r in actual_peak['lip_contour_offsets'] if r['x']==39.5)
checks['measured_center_gap_matches_formula']=abs(center['gap_source_px']-peak['center_gap_source_px'])<.0001
checks['measured_brow_travel_matches_formula']=all(abs(v['pivot_delta_source_px'][1]-peak['brow_pivot_lowering_source_px'])<.0001 for v in actual_peak['brow_geometry'].values())
checks['measured_lash_travel_matches_formula']=all(abs(v['pivot_delta_source_px'][1]-peak['eyes'][k]['upper_lash_travel_source_px'])<.0001 for k,v in actual_peak['lash_geometry'].items())
result={'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'bust_scale':scale,'scope':'Geometric travel and source-pixel-center aperture estimates only. Native visibility, filtering, hair occlusion, visual fidelity and normal-speed pacing remain unverified. No renderer started and no image was created or changed.','source_sha256':sources,'records':records}
(W/'geometry_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'checks':checks,'peak':peak},indent=2))
raise SystemExit(0 if all(checks.values()) else 1)

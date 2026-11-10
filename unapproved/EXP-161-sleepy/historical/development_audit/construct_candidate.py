from pathlib import Path
import json
W=Path(__file__).resolve().parent.parent
S=W.parent/'mild_disgust_work'
for name in ['check_and_capture.gd','render_motion.gd','prepare_native_launcher.py','run_motion.sh','encode_preview.py','test_encode_preview.py','verify_preparation.py','independent_geometry.py','test_independent_geometry.py','verify_input_freeze.py','review_validation.py']:
 s=(S/name).read_text().replace('081','161').replace('Mild Disgust','Sleepy').replace('Mild disgust','Sleepy').replace('Mild_disgust','Sleepy').replace('MildDisgust','Sleepy')
 (W/name).write_text(s)
# Preserve the proven source copy and parity scaffolding, write new source-specific semantics.
s=(S/'prepare_candidate.py').read_text().split('def pose(')[0].replace('081','161')
s=s.replace("write(W / 'BASELINE_FREEZE.json', freeze)","""current40 = ROOT / 'approved40_integration_work/ryoko_object_rig'
for n,digest in parity.items():
    assert h(current40/n) == digest, n
freeze['published40_runtime_artwork_parity'] = dict(path=str(current40), files_sha256=parity, count=len(parity), excluded_changed_metadata_registry_and_aggregate_guard=parity_exclusions)
write(W / 'BASELINE_FREEZE.json', freeze)""")
s+='''
def pose(brow,lid,opening):
    return dict(brow_screen_left=brow,brow_screen_right=brow,blink_R=lid,blink_L=lid,mouth_open=opening)
poses={
 'neutral':{},
 'onset':pose(-.07,.14,0),
 'droop':pose(-.14,.32,.07),
 'sleepy_peak':pose(-.22,.57,.16),
 'recover':pose(-.15,.40,.11),
 'release':pose(-.08,.22,.04),
 'settle':pose(-.025,.06,0),
 'neutral_return':{},
}
write(W/'plan.json',[dict(name=k,pose=v) for k,v in poses.items()])
keys=[(0,'neutral'),(.2,'neutral'),(.6,'onset'),(1.0,'droop'),(1.6,'sleepy_peak'),(2.4,'sleepy_peak'),(2.8,'recover'),(3.2,'release'),(3.5,'settle'),(3.7,'neutral_return'),(4,'neutral_return')]
write(W/'EXP-161.json',dict(id='EXP-161',title='Sleepy',duration=4.0,
 status='UNAPPROVED shared-rig preparation v1; native visual review pending',
 intent=entry['distinctive_facial_intent'],
 scope='Existing bilateral vertical brow lowering, bilateral ordinary partial lid closure and slight split-lip opening only. Jaw relaxation is suggested solely by lip separation; there is no jaw rotation, cheek deformation, chin or skull change. Brows have no tilt or inner lift. No new anatomy, art, shader, runtime, head/body movement, gaze, smile, purse, lip pressure, blush, or speech.',
 timing_origin='New four-second interpretation of the inspected EXP-161 nine-panel static reference, not recovered motion. Gentle lid and low-brow onset precedes lip parting, followed by one gradual sink into an uninterrupted 1.6-2.4-second heavy-lid hold with slightly open lips. The recovery has no second sag, effortful snap-open or brow overshoot. Unlike EXP-164 Fighting sleep there are no repeated fighting-sleep rebounds or sealed downturn. Unlike EXP-174 Sleepy annoyance there is no sharp brow knit/tilt or pout. Unlike EXP-177 Meditative calm, eyes remain partially open and lips part slightly.',
 interpolation='Unchanged shared smoothstep; eight static anchors, eleven timeline keys and exact neutral bookends. Candidate registered only in memory. Smoothstep joins at onset/droop/recovery anchors have zero velocity; no uninterrupted constant-speed descent is claimed.',
 source_catalogue_sha256=h(cat),keyframes=[dict(time=t,phase=p,values=poses[p]) for t,p in keys]))
write(W/'SOURCE_REFERENCE.json',dict(sheet=str(sheet),sha256=h(sheet),dimensions=[1254,1254],pixels_inspected=True,
 observations='Actual full nine-panel sheet viewed before authoring. Upper lids gradually droop together from panels 2-5 without fully closing. Lips begin parting in panel 3 and stay slightly open across panels 4-6. Brows remain low and relaxed, without the acute opposing tilt of annoyance. Panels 7-8 recover toward the neutral ninth panel. Static panels imply one sustained drowsy sink rather than repeated catch-and-reopen cycles.',
 left_right_convention='Brow names use screen sides. Blink names use character sides: blink_R closes screen-left and blink_L closes screen-right. Both are equal throughout this candidate.',
 approximation='Only existing rigid vertical brow movement, ordinary lash/iris closure and split-lip opening are used. Peak lowers both brows 2.2 source pixels, advances each upper lash 20.52 source pixels, and separates lip contours by 4.752 source pixels (2.32848 at bust scale). There is no anatomical jaw rotation, chin descent, cheek inflation, new relaxed lip shape, head nod, breathing or body gesture. Heavy-lid/open-lip perceptual fidelity and distinction remain pending native review.',
 panel_hashes={p['actual_panel_path']:p['sha256'] for p in entry['key_pose_sequence']},
 approval='Accepted reference art does not approve this candidate or its animation.'))
# Read-only feasibility finding, not a replacement candidate.
cheek=next(r for r in json.loads(cat.read_text())['expressions'] if r['id']=='EXP-192')
cs=ref/cheek['asset_production']['actual_path']
assert h(cs)==cheek['asset_production']['sha256']
registry=(source/'expression_registry.gd').read_text()
assert 'cheek' not in registry.lower() and 'jaw' not in registry.lower()
write(W/'SKIPPED_EXP-192.json',dict(id='EXP-192',title='Cheeks puffed',status='SKIPPED_UNSUPPORTED_REQUIRED_ANATOMY',
 source_sheet=str(cs),source_sheet_sha256=h(cs),catalogue_sha256=h(cat),pixels_inspected=True,
 intent=cheek['distinctive_facial_intent'],
 observation='Inspected nine-panel art shows the central puffed-cheek protest with sealed puckered lips and expanded cheek contours. Cheek expansion is essential to the named expression.',
 evidence=dict(registry_path=str(source/'expression_registry.gd'),sha256=h(source/'expression_registry.gd'),finding='CHANNEL_BOUNDS contains no cheek inflation or jaw shape channel. Existing lip purse cannot inflate the cheeks.'),
 decision='Do not prepare a pout substitute, alter artwork, add anatomy, or modify the runtime. EXP-161 is the next feasible candidate.'))
print('Prepared EXP-161 against frozen approved36; 999 files, 184 PNGs, runtime parity with approved39/40. EXP-192 skipped.')
'''
(W/'prepare_candidate.py').write_text(s)
acting='["brow_screen_left","brow_screen_right","blink_L","blink_R","mouth_open"]'
for name in ['check_and_capture.gd','render_motion.gd']:
 s=(W/name).read_text()
 import re
 s=re.sub(r'const ACTING_CHANNELS=.*', 'const ACTING_CHANNELS='+acting,s)
 s=s.replace('p.blink_R>=p.blink_L and p.blink_R<=.340001 and p.blink_L<=.180001','p.blink_R==p.blink_L and p.blink_R<=.570001')
 s=s.replace('mild unequal ordinary lids only','heavy bilateral partial lids only').replace('bounded uneven lids','bounded bilateral heavy lids')
 s=s.replace('p.mouth_corner_lift_screen_right<=.320001','p.mouth_corner_lift_screen_right==0 and p.mouth_purse==0')
 s=s.replace('no smile control; bounded common corner lift only','no smile, purse or common corner lift')
 s=s.replace('Eight Sleepy anchors with unequal lowered/tilted brow geometry, ordinary lid narrowing and common-corner/purse opening checks.','Eight Sleepy anchors with relaxed bilateral low brows, heavy ordinary partial lid closure and slight lip separation. No jaw or cheek anatomy is simulated.')
 if name=='render_motion.gd':
  start=s.index(' # Source-specific temporal relationships')
  end=s.index(' for record in records:',start)
  s=s[:start]+''' # One gradual sustained drowsy sink, not repeated fighting sleep.
 var onset=records[18].pose;var peak=records[48].pose
 check(onset.blink_L>.139 and onset.mouth_open==0,"heavy lids begin before lips part")
 check(is_equal_approx(peak.brow_screen_left,-.22) and peak.brow_screen_left==peak.brow_screen_right,"relaxed equal low brows")
 check(is_equal_approx(peak.blink_R,.57) and peak.blink_R==peak.blink_L,"heavy but partially open eyes")
 check(is_equal_approx(peak.mouth_open,.16),"slightly parted lips at peak")
 check(is_equal_approx(records[48].central_lip_gap_native_px,4.752),"small lip separation, no jaw control")
 for i in range(48,73):
  for key in ACTING_CHANNELS:check(is_equal_approx(records[48].pose[key],records[i].pose[key]),"sustained sleepy hold "+str(i)+" "+key)
 for i in range(1,49):
  check(records[i].pose.blink_L>=records[i-1].pose.blink_L,"single monotone lid sink "+str(i))
  check(records[i].pose.mouth_open>=records[i-1].pose.mouth_open,"gradual lip parting "+str(i))
 for i in range(73,121):
  check(records[i].pose.blink_L<=records[i-1].pose.blink_L,"recovery without second sag "+str(i))
  check(records[i].pose.mouth_open<=records[i-1].pose.mouth_open,"gradual lip reseal "+str(i))
 check(records[105].pose.mouth_open==0 and records[105].pose.blink_L>.059,"lips seal before final lid recovery")
''' + s[end:]
  s=s.replace('[.35,.6,1.0,1.4,1.75,2.15,2.7,3.25,3.7]','[.35,.6,1.0,1.6,2.4,2.8,3.2,3.5,3.7]')
 (W/name).write_text(s)
# Full preservation checker: add 40 parity and the prior candidate.
s=(W/'verify_preparation.py').read_text()
s=s.replace("assert len(f['source_files_sha256']) == 999", "for n,digest in f['published40_runtime_artwork_parity']['files_sha256'].items():\n    assert h(Path(f['published40_runtime_artwork_parity']['path'])/n) == digest, n\nassert len(f['source_files_sha256']) == 999")
s=s.replace("W.parent / 'open_sobbing_work/EXP-023.json']", "W.parent / 'open_sobbing_work/EXP-023.json', W.parent / 'mild_disgust_work/EXP-081.json']")
s=s.replace("interpretation='Asymmetric low brow and unequal partial lid closure lead a brief small parted common-corner lift, then mouth seals before brow release. Bitter taste uses stronger bilateral lowering and a longer symmetric open grimace; Queasy uses inner-brow lift and pressure rather than this side-biased common contour. Upper-lip-only lift and nose wrinkling are not implemented.'", "interpretation='A single sustained bilateral drowsy sink with low untitled brows, heavy but open lids and slight lip parting. EXP-164 repeats sealed-mouth fighting-sleep rebounds; EXP-174 adds sharp opposing brow tilt and pout; EXP-177 fully closes eyes with a sealed mouth. No jaw or cheek anatomy is simulated.'")
(W/'verify_preparation.py').write_text(s)
# Independent geometry and source checks.
s=(W/'independent_geometry.py').read_text()
s=re.sub(r'ACTING=.*',"ACTING={'brow_screen_left','brow_screen_right','blink_L','blink_R','mouth_open'}",s)
s=s.replace("0<=p['blink_L']<=p['blink_R']<=.340001,'mild asymmetrical eyelids '","0<=p['blink_L']==p['blink_R']<=.570001,'bilateral heavy lids '")
s=s.replace("p['brow_screen_left']<=p['brow_screen_right']<=0,'asymmetrical lowered brows '","-.220001<=p['brow_screen_left']==p['brow_screen_right']<=0,'relaxed equal low brows '")
start=s.index("    p=motion['records'][42]['pose']")
end=s.index('    return dict(status=',start)
s=s[:start]+'''    p=motion['records'][48]['pose']
    check(close(gap(p,39.5),4.752),'peak aperture')
    check(close(upper(p,75),0) and close(upper(p,4),0),'no lifted or pursed lip contour')
    check(all(close(row['pose'][k],p[k]) for row in motion['records'][48:73] for k in controls),'sustained held peak')
    onset=motion['records'][18]['pose']
    check(onset['blink_L']>.139 and onset['mouth_open']==0,'lids lead lip parting')
    check(all(motion['records'][i]['pose']['blink_L']>=motion['records'][i-1]['pose']['blink_L'] for i in range(1,49)),'monotone lid sink')
    check(all(motion['records'][i]['pose']['blink_L']<=motion['records'][i-1]['pose']['blink_L'] for i in range(73,121)),'no repeated sag')
    check(motion['records'][105]['pose']['mouth_open']==0 and motion['records'][105]['pose']['blink_L']>.059,'lips reseal before full lid recovery')
    check(motion['lifecycle_interruption_times']==[.35,.6,1,1.6,2.4,2.8,3.2,3.5,3.7] and motion['lifecycle_assertions']==36,'lifecycle evidence')
''' +s[end:]
s=s.replace('[1213,1296]','[1254,1254]')
(W/'independent_geometry.py').write_text(s)
s=(W/'test_independent_geometry.py').read_text().replace("['records'][42]","['records'][48]").replace('5.2164','4.752').replace(',-2.4',',0').replace(',1.44',',0')
s=s.replace('test_lid_side_swap_rejected','test_lid_asymmetry_rejected').replace('test_upper_only_corner_fiction_rejected','test_unexpected_lip_corner_rejected')
(W/'test_independent_geometry.py').write_text(s)

"""Adapt only candidate-author preparation helpers, never reviewer artifacts."""
from pathlib import Path
import json
W=Path(__file__).resolve().parents[1]; S=W.parent/'sleepy_work'
# These files belong to the candidate preparation, not independent reviewer evidence.
files=['prepare_candidate.py','check_and_capture.gd','render_motion.gd','prepare_native_launcher.py','verify_preparation.py','independent_geometry.py','test_independent_geometry.py','encode_preview.py','test_encode_preview.py','run_motion.sh','verify_input_freeze.py']
for name in files:
 s=(S/name).read_text().replace('EXP-161','EXP-104').replace('EXP161','EXP104').replace('exp161','exp104').replace('PROBE-161','PROBE-104').replace('probe-161','probe-104').replace('candidate-161','candidate-104').replace('Sleepy161','TriumphantGrin104').replace('Sleepy_review','TriumphantGrin_review').replace('Sleepy','Triumphant Grin')
 (W/name).write_text(s)
p=W/'prepare_candidate.py';s=p.read_text();s=s[:s.index('def pose(')]+'''
def pose(brow,tilt,lid,smile,spread,opening):
    return dict(brow_screen_left=brow,brow_screen_right=brow,
        brow_tilt_screen_left=tilt,brow_tilt_screen_right=-tilt,
        blink_R=lid,blink_L=lid,mouth_smile=smile,mouth_spread=spread,mouth_open=opening)
poses={
 'neutral':{},
 'onset':pose(-.10,.14,.04,.18,.28,0),
 'grin_build':pose(-.22,.30,.09,.46,.60,.06),
 'tooth_grin':pose(-.32,.42,.12,.84,.86,.30),
 'open_grin':pose(-.30,.40,.10,.88,.90,.46),
 'recover':pose(-.22,.30,.08,.55,.62,.15),
 'settle':pose(-.08,.12,.03,.22,.30,0),
 'neutral_return':{},
}
write(W/'plan.json',[dict(name=k,pose=v) for k,v in poses.items()])
keys=[(0,'neutral'),(.2,'neutral'),(.6,'onset'),(1.0,'grin_build'),(1.6,'tooth_grin'),(2.0,'tooth_grin'),(2.4,'open_grin'),(2.8,'recover'),(3.2,'settle'),(3.7,'neutral_return'),(4,'neutral_return')]
write(W/'EXP-104.json',dict(id='EXP-104',title='Triumphant Grin',duration=4.0,
 status='UNAPPROVED shared-rig preparation v1; native visual review pending',
 intent=entry['distinctive_facial_intent'],
 scope='Existing bilateral equal low brow heights, mirrored inward brow tilts, equal ordinary partial lids, centered legacy smile/spread and modest opening only. Smile and spread use existing tooth and mouth support; no independent dental control, exact opposing tooth rows, clench, cheek anatomy or jaw rotation. No new art, shader, runtime, gaze, smile-eye, corner bias, head/body gesture, hair, speech or effects.',
 timing_origin='New four-second interpretation of the inspected EXP-104 nine-panel static reference, not recovered motion. Focused symmetric brows precede a centered grin, a 1.6-2.0-second shallow tooth-bearing hold, then a somewhat more open grin at 2.4 seconds. Recovery reseals the lips before exact neutral. EXP-114 has unequal lids, opposed brow heights and a crooked grin; EXP-152 has downcast sealed private pride; EXP-001 raises its brows with a much larger welcoming opening.',
 interpolation='Unchanged shared smoothstep; eight static anchors, eleven timeline keys, 121 endpoint-inclusive samples and exact neutral bookends. Candidate is registered only in memory. Zero-velocity anchor joins are deliberate; this does not claim recovered continuous source motion.',
 source_catalogue_sha256=h(cat),keyframes=[dict(time=t,phase=p,values=poses[p]) for t,p in keys]))
write(W/'SOURCE_REFERENCE.json',dict(sheet=str(sheet),sha256=h(sheet),dimensions=[1159,1358],pixels_inspected=True,
 observations='Actual full nine-panel sheet viewed before authoring. Brows descend and angle inward on both sides while eyes remain forward and visibly open. The smile broadens through panels 2-4 into a centered tooth-showing grin in panel 5, then a somewhat more open grin in panel 6. Panels 7-8 release the smile and brow tension before panel 9 returns to neutral. The expression is bilateral, not a crooked unilateral smirk.',
 left_right_convention='Brow names use screen sides. Positive left and negative right tilt lower their inner ends symmetrically. Blink names use character sides: blink_R closes screen-left and blink_L closes screen-right. Both lid values are equal throughout.',
 approximation='Uses existing upper tooth arch and spread support passively coupled to smile/spread/opening. There is no independent dental or clench control, no claim of exact opposing tooth-row anatomy, and no source-art alteration. The rendered mouth is a shallow open grin rather than a true sealed clench. Effective horizontal spread equals public mouth_spread multiplied by mouth_smile. Tooth-grin controls yield 8.91 source pixels of central aperture and 28.896 source pixels of added width; the later open grin yields 13.662 pixels of aperture and 31.68 pixels of added width. Native visible tooth exposure, lip seams, focused-eye appearance and perceptual distinction remain pending visual review.',
 panel_hashes={p['actual_panel_path']:p['sha256'] for p in entry['key_pose_sequence']},
 approval='Accepted reference art does not approve this candidate or its animation.'))
print('Prepared EXP-104 against frozen approved36: 999 files and 184 PNGs; runtime parity with approved40/41.')
'''
# Verify and retain only current requested parity comparisons, not historical39.
a=s.index('# Runtime and artwork');b=s.index("write(W / 'BASELINE_FREEZE.json', freeze)")
s=s[:a]+'''# Registry/release metadata is newer; common runtime/artwork is byte-identical.
parity_exclusions = ['APPROVED_INTEGRATION_STATUS.json', 'APPROVED_INTEGRATION_TEST_RESULTS.json', 'README.md', 'RELEASE.json', 'expressions/registry.json', 'tools/verify_approved_integration.py']
parity = {n: v for n,v in files.items() if n not in parity_exclusions}
freeze = dict(baseline='approved36', baseline_profile_count=36,
    published_baseline_commit='3ce98774282ad6c20dfbd7018d20838ff861b762',
    source_rig=str(source), source_files=999, source_png_files=184,
    source_files_sha256=files, extra_manifests_sha256=extra,
    baseline_profile_ids=ids, source_sheet=str(sheet), source_sheet_sha256=h(sheet),
    source_catalogue=str(cat), catalogue_sha256=h(cat))
for release in [40,41]:
    current=ROOT/f'approved{release}_integration_work/ryoko_object_rig'
    for n,digest in parity.items():assert h(current/n)==digest, str(current/n)
    freeze[f'published{release}_runtime_artwork_parity']=dict(path=str(current), files_sha256=parity, count=len(parity), excluded_changed_metadata_registry_and_aggregate_guard=parity_exclusions)
''' + s[b:]
p.write_text(s)
# Static and motion probe geometry remains explicit, including nonlinear effective spread.
acting='["brow_screen_left","brow_screen_right","brow_tilt_screen_left","brow_tilt_screen_right","blink_L","blink_R","mouth_smile","mouth_spread","mouth_open"]'
for name in ['check_and_capture.gd','render_motion.gd']:
 p=W/name;s=p.read_text();a=s.index('const ACTING_CHANNELS=');b=s.index('\n',a);s=s[:a]+'const ACTING_CHANNELS='+acting+s[b:]
 s=s.replace('is_equal_approx(delta.y,36.0*amount)','absf(delta.y-36.0*amount)<.0001')
 s=s.replace('.570001','.120001').replace('heavy bilateral partial lids only','equal focused ordinary partial lids').replace('bounded bilateral heavy lids','bounded bilateral focused lids')
 s=s.replace('14.0*p.mouth_purse','-20.0*p.mouth_spread*p.mouth_smile')
 # Replacement changes both source-side signs correctly: negative(+left), positive(right).
 s=s.replace('symmetric purse horizontal travel','symmetric effective spread travel').replace('timeline actual symmetric purse','timeline actual symmetric effective spread')
 s=s.replace('p.mouth_corner_lift==0 and p.mouth_corner_lift_screen_left==0 and p.mouth_corner_lift_screen_right==0 and p.mouth_purse==0 and p.mouth_smile==0 and p.mouth_spread==0','p.mouth_corner_lift==0 and p.mouth_corner_lift_screen_left==0 and p.mouth_corner_lift_screen_right==0 and p.mouth_purse==0')
 s=s.replace('no smile, purse or common corner lift','no purse or independent/common corner lift')
 old='p.mouth_purse*(4.0+8.0*pow(abs((x-39.5)/35.5),2))-12.0*p.mouth_corner_lift_screen_right*pow(maxf((x-39.5)/35.5,0.0),3)'
 new='-4.0*p.mouth_spread*p.mouth_smile-(4.0+5.0*p.mouth_spread*p.mouth_smile)*p.mouth_smile*pow(abs((x-39.5)/35.5),1.5)'
 s=s.replace(old,new)
 s=s.replace('p.mouth_purse*(4.0+8.0*radius*radius)-12.0*p.mouth_corner_lift_screen_right*pow(maxf((x-39.5)/35.5,0.0),3)','-4.0*p.mouth_spread*p.mouth_smile-(4.0+5.0*p.mouth_spread*p.mouth_smile)*p.mouth_smile*pow(radius,1.5)')
 s=s.replace('common-corner plus purse upper contour','symmetric smile upper contour').replace('timeline common upper contour','timeline symmetric smile upper contour')
 # Add measurement of effective internal channel plus actual tooth-support transforms; not independent dental control.
 marker='  var mouth_width=' if name=='check_and_capture.gd' else '  var actual_gap='
 insert='''  check(is_equal_approx(rig.face.mouth_spread,p.mouth_spread*p.mouth_smile),"effective spread includes smile product")
  for tooth in rig.face.spread_teeth:
   var left=tooth.name.ends_with("left")
   var spread=p.mouth_spread*p.mouth_smile
   var anchor=Vector2(553 if left else 577,619)
   var origin=Vector2(532 if left else 553,605)
   var angle=(1.0 if left else -1.0)*.12*spread
   var expected=anchor+(origin-anchor).rotated(angle)+Vector2((-20.0 if left else 20.0)*spread,9.0*spread)
   check(tooth.position.distance_to(expected)<.0001,"passively coupled upper tooth support position")
   check(is_equal_approx(tooth.rotation,angle),"passively coupled upper tooth support rotation")
   check(tooth.visible==(spread>0),"coupled tooth support visibility flag, not pixel exposure")
'''
 s=s.replace(marker,insert+marker)
 if name=='check_and_capture.gd':
  s=s.replace('Eight Triumphant Grin anchors with relaxed bilateral low brows, heavy ordinary partial lid closure and slight lip separation. No jaw or cheek anatomy is simulated.','Eight Triumphant Grin anchors with bilateral low inward-angled brows, equal ordinary focused lids and a centered tooth-bearing then more open smile. Existing tooth support is coupled to smile/spread; no independent dental control, clench or new anatomy.')
 else:
  a=s.index(' # One gradual sustained');b=s.index(' for i in range(1,records.size()):',a)
  s=s[:a]+''' # Reference-specific centered grin followed by a somewhat more open grin.
 var onset=records[18].pose;var peak=records[48].pose;var opened=records[72].pose
 check(onset.mouth_open==0 and onset.brow_screen_left<0 and onset.brow_tilt_screen_left>0,"brows and sealed smile precede opening")
 check(is_equal_approx(peak.brow_screen_left,-.32) and peak.brow_screen_left==peak.brow_screen_right,"equal low brows")
 check(is_equal_approx(peak.brow_tilt_screen_left,.42) and peak.brow_tilt_screen_right==-peak.brow_tilt_screen_left,"mirrored inward brow angles")
 check(is_equal_approx(peak.blink_R,.12) and peak.blink_R==peak.blink_L,"forward visibly open focused eyes")
 check(is_equal_approx(peak.mouth_open,.30) and is_equal_approx(peak.mouth_smile,.84) and is_equal_approx(peak.mouth_spread,.86),"shallow centered tooth-grin controls")
 check(is_equal_approx(records[48].central_lip_gap_native_px,8.91),"shallow peak aperture")
 check(is_equal_approx(opened.mouth_open,.46) and is_equal_approx(records[72].central_lip_gap_native_px,13.662),"later somewhat more open grin")
 for i in range(48,61):
  for key in ACTING_CHANNELS:check(is_equal_approx(records[48].pose[key],records[i].pose[key]),"held tooth grin "+str(i)+" "+key)
 for i in range(1,73):
  check(records[i].pose.mouth_open>=records[i-1].pose.mouth_open,"monotone grin opening "+str(i))
  check(records[i].pose.mouth_smile>=records[i-1].pose.mouth_smile,"monotone smile build "+str(i))
 for i in range(73,121):
  check(records[i].pose.mouth_open<=records[i-1].pose.mouth_open,"single gradual lip reseal "+str(i))
  check(records[i].pose.mouth_smile<=records[i-1].pose.mouth_smile,"gradual smile recovery "+str(i))
 check(records[96].pose.mouth_open==0 and records[96].pose.mouth_smile>.219,"lips seal before smile resolves")
 for record in records:
  if record.time<=.2 or record.time>=3.7:
   for value in record.pose.values():check(value==0,"neutral hold "+str(record.time))
  check(record.pose.brow_inner_lift_screen_left==0 and record.pose.brow_inner_lift_screen_right==0,"no inner-brow lift "+str(record.time))
  check(record.pose.brow_screen_left==record.pose.brow_screen_right and record.pose.brow_tilt_screen_left==-record.pose.brow_tilt_screen_right,"bilateral brow geometry "+str(record.time))
  check(record.pose.mouth_width_screen_left==0 and record.pose.mouth_width_screen_right==0,"no incompatible sealed-only width "+str(record.time))
  check(record.pose.eye_smile_R==0 and record.pose.eye_smile_L==0,"no smile-eye closing "+str(record.time))
''' +s[b:]
  s=s.replace('[.35,.6,1.0,1.6,2.4,2.8,3.2,3.5,3.7]','[.35,.6,1.0,1.6,2.0,2.4,2.8,3.2,3.7]')
 p.write_text(s)
# Correct launcher human-visible slug after broad name substitution.
p=W/'prepare_native_launcher.py';s=p.read_text().replace('TriumphantGrin104','TriumphantGrin104');p.write_text(s)
# Source verification; update comparisons to later current profiles, including sleepy.
p=W/'verify_preparation.py';s=p.read_text().replace('published39_runtime_artwork_parity','published41_runtime_artwork_parity')
s=s.replace("W.parent / 'mild_disgust_work/EXP-081.json']","W.parent / 'mild_disgust_work/EXP-081.json', W.parent / 'sleepy_work/EXP-161.json']")
a=s.index("    interpretation='");b=s.index('\n    limitations=',a)
s=s[:a]+"    interpretation='Bilateral low inward-angled brows and direct equal focused lids precede a centered tooth-bearing smile, followed by a modestly more open grin. EXP-114 is crooked with unequal lids/opposed brow heights; EXP-152 is downcast and sealed; EXP-001 raises brows and opens much wider. No independent dental or clench control is simulated.',"+s[b:]
p.write_text(s)
# Independent math: rederive effective spread product and symmetric smile aperture.
p=W/'independent_geometry.py';s=p.read_text();a=s.index('ACTING=');b=s.index('\n',a);s=s[:a]+'ACTING=set('+acting+')'+s[b:]
a=s.index('def upper(');b=s.index('def audit(',a)
s=s[:a]+'''def effective_spread(p):return p['mouth_spread']*p['mouth_smile']
def upper(p,x):
    radius=min(1,abs((x-39.5)/35.5));spread=effective_spread(p)
    return -4*spread-(4+5*spread)*p['mouth_smile']*radius**1.5
def gap(p,x):
    radius=min(1,abs((x-39.5)/35.5))
    curve=max(0,1-radius*radius)**.72
    return p['mouth_open']*.55*54*((1-p['mouth_smile'])+p['mouth_smile']*curve)
''' +s[b:]
s=s.replace("[14*p['mouth_purse'],-14*p['mouth_purse']]","[-20*effective_spread(p),20*effective_spread(p)]").replace("'purse width '","'effective spread width '")
s=s.replace(".570001,'bilateral heavy lids '",".120001,'bilateral focused lids '").replace("-.220001<=","-.320001<=").replace('relaxed equal low brows','equal low brows')
a=s.index("    p=motion['records'][48]['pose']");b=s.index('    return dict(',a)
s=s[:a]+'''    p=motion['records'][48]['pose'];opened=motion['records'][72]['pose']
    check(close(gap(p,39.5),8.91),'tooth-grin aperture')
    check(close(upper(p,75),-9.28368) and close(upper(p,4),-9.28368),'symmetric lifted grin corners')
    check(close(gap(opened,39.5),13.662),'later open-grin aperture')
    check(all(close(row['pose'][k],p[k]) for row in motion['records'][48:61] for k in controls),'held shallow tooth grin')
    onset=motion['records'][18]['pose']
    check(onset['brow_screen_left']<0 and onset['brow_tilt_screen_left']>0 and onset['mouth_open']==0,'brows precede opening')
    check(all(motion['records'][i]['pose']['mouth_open']>=motion['records'][i-1]['pose']['mouth_open'] for i in range(1,73)),'monotone opening build')
    check(all(motion['records'][i]['pose']['mouth_open']<=motion['records'][i-1]['pose']['mouth_open'] for i in range(73,121)),'single gradual reseal')
    check(motion['records'][96]['pose']['mouth_open']==0 and motion['records'][96]['pose']['mouth_smile']>.219,'reseal before smile recovery')
    check(motion['lifecycle_interruption_times']==[.35,.6,1,1.6,2,2.4,2.8,3.2,3.7] and motion['lifecycle_assertions']==36,'lifecycle evidence')
''' +s[b:]
s=s.replace('[1254,1254]','[1159,1358]')
# Add symmetry independently beyond profile matching.
s=s.replace("        if i<=6", "        check(close(p['brow_tilt_screen_left'],-p['brow_tilt_screen_right']) and 0<=p['brow_tilt_screen_left']<=.420001,'mirrored inward tilt '+str(i))\n        if i<=6")
p.write_text(s)
# Mutation test hardcoded expected analytic values.
p=W/'test_independent_geometry.py';s=p.read_text().replace('4.752','8.91').replace('test_smile_channel_rejected','test_smile_mismatch_rejected')
s=s.replace("audit.upper(p,75),0","audit.upper(p,75),-9.28368").replace("audit.upper(p,4),0","audit.upper(p,4),-9.28368")
p.write_text(s)
print('Author-only candidate scripts constructed.')

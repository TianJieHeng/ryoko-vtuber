"""Adapt established probe/launcher/encoder tooling; never run a native renderer."""
from pathlib import Path
W=Path(__file__).resolve().parent
T=W.parent/'open_sobbing_work'
acting='const ACTING_CHANNELS=["brow_screen_left","brow_screen_right","brow_tilt_screen_left","brow_tilt_screen_right","blink_L","blink_R","mouth_open","mouth_purse","mouth_corner_lift_screen_right"]'
for name in ['check_and_capture.gd','render_motion.gd','prepare_native_launcher.py','run_motion.sh','encode_preview.py','test_encode_preview.py','verify_preparation.py']:
 s=(T/name).read_text().replace('023','081').replace('Open Sobbing','Mild Disgust').replace('Open_sobbing','Mild_disgust').replace('open_sobbing','mild_disgust').replace('OpenSobbing','MildDisgust')
 if name.endswith('.gd'):
  lines=s.splitlines();lines=[acting if line.startswith('const ACTING_CHANNELS=') else line for line in lines];s='\n'.join(lines)+'\n'
 if name=='check_and_capture.gd':
  s=s.replace('plan.size()==9','plan.size()==8').replace('nine isolated study poses','eight isolated study poses').replace('BASELINE_COUNT+9','BASELINE_COUNT+8').replace('nine in-memory probes','eight in-memory probes').replace('"study_poses":9','"study_poses":8').replace('Nine Mild Disgust anchors with actual anchored-inner-brow, ordinary lid squeeze and symmetric opening/purse geometry checks.','Eight Mild Disgust anchors with unequal lowered/tilted brow geometry, ordinary lid narrowing and common-corner/purse opening checks.')
  s=s.replace('p.blink_R<=1.0 and p.blink_L<=1.0','p.blink_R<=.340001 and p.blink_L<=.180001').replace('ordinary distressed lids only','mild unequal ordinary lids only')
  s=s.replace(' and p.mouth_corner_lift_screen_right==0',' and p.mouth_corner_lift_screen_right<=.320001').replace('unsmiling split lips only','no smile control; bounded common corner lift only')
  s=s.replace('no claimed spatially uneven open mouth','symmetric horizontal mouth width, no translation')
  s=s.replace('p.mouth_purse*(4.0+8.0*pow(abs((x-39.5)/35.5),2))','p.mouth_purse*(4.0+8.0*pow(abs((x-39.5)/35.5),2))-12.0*p.mouth_corner_lift_screen_right*pow(maxf((x-39.5)/35.5,0.0),3)')
  s=s.replace('downward purse lip contour','common-corner plus purse upper contour')
  s=s.replace('check(is_equal_approx(rig.face._smile_lip_offset(4.0,false,false),rig.face._smile_lip_offset(75.0,false,false)),row.name+" open mouth remains spatially symmetric")','check(is_equal_approx(rig.face._smile_lip_offset(4.0,false,false)-rig.face._smile_lip_offset(75.0,false,false),12.0*p.mouth_corner_lift_screen_right),row.name+" corner lift moves both lip contours, not upper lip alone")')
 if name=='render_motion.gd':
  s=s.replace('p.blink_R<=1.0 and p.blink_L<=1.0','p.blink_R<=.340001 and p.blink_L<=.180001')
  s=s.replace('var angle=deg_to_rad((-26.0 if side=="screen_left" else 26.0)*p["brow_inner_lift_"+side])','var angle=deg_to_rad(8.0*p["brow_tilt_"+side])')
  s=s.replace('var expected=Vector2(0,-10.0*p["brow_"+side])+a-a.rotated(angle)','var expected=Vector2(0,-10.0*p["brow_"+side])')
  pos='  for key in p:\n'
  geom='''  for x in [4.0,39.5,75.0]:
   var radius=absf((x-39.5)/35.5)
   var expected_upper=p.mouth_purse*(4.0+8.0*radius*radius)-12.0*p.mouth_corner_lift_screen_right*pow(maxf((x-39.5)/35.5,0.0),3)
   var actual_upper=rig.face._smile_lip_offset(x,true,false)
   var actual_lower=rig.face._smile_lip_offset(x,false,false)
   check(is_equal_approx(actual_upper,expected_upper),"timeline common upper contour "+str(x)+" "+str(i))
   check(actual_lower>=actual_upper,"timeline nonnegative lip gap "+str(x)+" "+str(i))
  check(is_equal_approx(rig.face._smile_lip_offset(4.0,false,false)-rig.face._smile_lip_offset(75.0,false,false),12.0*p.mouth_corner_lift_screen_right),"timeline both lips share corner bias "+str(i))
'''
  s=s.replace(pos,geom+pos,1)
  a=s.index(' # Source-specific temporal checks');b=s.index(' for i in range(1,records.size()):',a)
  s=s[:a]+''' # Source-specific temporal relationships, distinct from taste or nausea.
 var detect=records[18].pose;var peak=records[42].pose;var sealed=records[65].pose
 check(detect.brow_screen_left<-.139 and detect.mouth_open==0 and detect.mouth_corner_lift_screen_right==0,"asymmetric detection leads mouth bias")
 check(peak.brow_screen_left<-.439 and peak.brow_screen_right>-.121,"one brow lowers more strongly")
 check(peak.blink_R>.339 and peak.blink_L<.181,"unequal mild narrowed eyes")
 check(peak.mouth_open>.179 and peak.mouth_corner_lift_screen_right>.319,"brief small parted common-corner lift")
 check(is_equal_approx(records[42].central_lip_gap_native_px,5.2164),"small peak central gap")
 for key in ACTING_CHANNELS:check(is_equal_approx(records[42].pose[key],records[52].pose[key]),"brief peak hold "+key)
 check(sealed.mouth_open==0 and sealed.brow_screen_left<-.37 and sealed.mouth_corner_lift_screen_right>.11,"mouth seals while objection persists")
 check(records[81].pose.mouth_corner_lift_screen_right==0 and records[81].pose.brow_screen_left<-.199,"mouth bias releases before brow tension")
 check(records[98].pose.mouth_purse==0,"purse releases before final brow settle")
 for record in records:
  if record.time<=.2 or record.time>=3.7:
   for value in record.pose.values():check(value==0,"neutral hold "+str(record.time))
  check(record.pose.brow_inner_lift_screen_left==0 and record.pose.brow_inner_lift_screen_right==0,"no queasy inner-brow lift "+str(record.time))
  check(record.pose.mouth_width_screen_left==0 and record.pose.mouth_width_screen_right==0,"no incompatible sealed-only width "+str(record.time))
  check(record.pose.eye_smile_R==0 and record.pose.eye_smile_L==0 and record.pose.mouth_smile==0,"no smile-eye or smile "+str(record.time))
'''+s[b:]
  s=s.replace('[.35,.55,.95,1.4,1.7,2.1,2.45,2.85,3.25,3.7]','[.35,.6,1.0,1.4,1.75,2.15,2.7,3.25,3.7]').replace('"lifecycle_assertions":40','"lifecycle_assertions":36')
 if name=='verify_preparation.py':
  s=s.replace('len(plan) == 9 and len(profile[\'keyframes\']) == 12','len(plan) == 8 and len(profile[\'keyframes\']) == 11')
  s=s.replace("motion['lifecycle_assertions'] == 40 and len(motion['lifecycle_interruption_times']) == 10","motion['lifecycle_assertions'] == 36 and len(motion['lifecycle_interruption_times']) == 9")
  s=s.replace("W.parent / 'puzzled_work/EXP-123.json']","W.parent / 'puzzled_work/EXP-123.json', W.parent / 'open_sobbing_work/EXP-023.json']")
  s=s.replace("interpretation='Bilateral strong inner lift with lowered outer brows, ordinary full lid squeeze/reopening, symmetric open/pursed mouth and a smaller second sob. Unlike Quiet sadness there is an open mouth and no downcast gaze; unlike Shocked gasp and Broad surprise there is lid closure rather than widening. No smile-eye or smile controls.'","interpretation='Asymmetric low brow and unequal partial lid closure lead a brief small parted common-corner lift, then mouth seals before brow release. Bitter taste uses stronger bilateral lowering and a longer symmetric open grimace; Queasy uses inner-brow lift and pressure rather than this side-biased common contour. Upper-lip-only lift and nose wrinkling are not implemented.'")
  s=s.replace('lifecycle_interruption_points=10, lifecycle_assertions=40','lifecycle_interruption_points=9, lifecycle_assertions=36')
  pos="assert len(f['source_files_sha256']) == 999"
  s=s.replace(pos,"for n,digest in f['published39_runtime_artwork_parity']['files_sha256'].items():\n    assert h(Path(f['published39_runtime_artwork_parity']['path'])/n) == digest, n\n"+pos)
 (W/name).write_text(s)

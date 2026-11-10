from pathlib import Path
W=Path(__file__).resolve().parent; M=W.parent/'mental_arithmetic_work'
s=(M/'prepare_candidate.py').read_text(); s=s[:s.index('def pose(')].replace('129','041').replace('mental-arithmetic','controlled-anger')
s+='''def pose(b,t,l,p):return dict(brow_screen_left=b,brow_screen_right=b,brow_tilt_screen_left=t,brow_tilt_screen_right=-t,blink_L=l,blink_R=l,mouth_lip_press=p)
poses={'neutral':{},'restrain':pose(-.18,.18,.06,.24),'gather':pose(-.42,.4,.16,.42),'controlled_anger':pose(-.7,.65,.26,.65),'ease_pressure':pose(-.7,.65,.26,.38),'soften':pose(-.3,.28,.12,.22),'settle':pose(-.08,.08,.03,.06),'neutral_return':{}}
(W/'plan.json').write_text(json.dumps([dict(name=k,pose=v) for k,v in poses.items()],indent=2)+'\\n')
keys=[(0,'neutral'),(.2,'neutral'),(.6,'restrain'),(.95,'gather'),(1.35,'controlled_anger'),(2.1,'controlled_anger'),(2.55,'ease_pressure'),(3,'soften'),(3.35,'settle'),(3.7,'neutral_return'),(4,'neutral_return')]
d=dict(id='EXP-041',title='Controlled anger',duration=4.0,status='UNAPPROVED shared-rig preparation v1; native visual review pending',intent='Brows draw inward and down by rigid approximation, eyes narrowly fixed, lips pressed straight and restrained.',scope='Existing symmetric brow lowering and opposing rigid tilt, ordinary symmetric lid closure and sealed lip pressure only. No horizontal brow convergence is available; no new anatomy, artwork, runtime, gaze, head or body movement.',timing_origin='New four-second interpretation of nine inspected static source panels, not recovered motion. Measured onset and held restrained peak, then lip pressure eases before the brow and lid release. Cold Glare has zero tilt and purse; Silent Fury has neutral lids and maximum tilt/press. This candidate instead combines moderate tilt and pressure with narrow fixed eyes.',interpolation='Unchanged shared smoothstep; eight static anchors, eleven timeline keys, exact neutral bookends, in-memory registration only.',source_catalogue_sha256=h(cat),keyframes=[dict(time=t,phase=p,values=poses[p]) for t,p in keys])
(W/'EXP-041.json').write_text(json.dumps(d,indent=2)+'\\n')
(W/'SOURCE_REFERENCE.json').write_text(json.dumps(dict(sheet=str(sheet),sha256=h(sheet),pixels_inspected=True,observations='Nine frontal panels: brows progressively angle down toward center, eyes narrow while maintaining forward gaze, lips remain thin and closed. Mid-row has strongest brow tension. Final row softens. No added body, head or gaze beat is warranted. Existing rigid brows approximate the inward/down cue without horizontal convergence.',approval='Historical approved sprite-composite art exists. It does not approve this new shared-rig animation.'),indent=2)+'\\n')
print('Prepared 999 pinned files, 184 PNGs; candidate outside production registry.')
'''
(W/'prepare_candidate.py').write_text(s)
for n in ['verify_preparation.py','prepare_native_launcher.py','encode_preview.py']:
 s=(M/n).read_text().replace('Mental arithmetic','Controlled anger').replace('Mental_arithmetic','Controlled_anger')
 if n=='prepare_native_launcher.py':s=s.replace("(D/'project.godot').write_text(p)","p=re.sub(r'config/name=.*','config/name=\\\"Ryoko EXP-041 Controlled Anger Review\\\"',p)\n(D/'project.godot').write_text(p)")
 (W/n).write_text(s)
s=(M/'check_and_capture.gd').read_text().replace('129','041').replace('"mouth_purse","gaze_y"','"mouth_lip_press"').replace('.080001','.260001').replace('subtle lids','narrow lids').replace('and p.mouth_lip_press==0','and p.mouth_purse==0').replace('sealed unsmiling purse only','sealed unsmiling pressed lips')
a=s.index('  for side in ["screen_left","screen_right"]:\n   var offset=');b=s.index('  for key in p:',a)
f=(W.parent/'silent_fury_work/check_and_capture.gd').read_text();c=f.index('  check(is_equal_approx(rig.face.mouth_lip_press');d=f.index('  for key in p:',c)
s=s[:a]+f[c:d]+s[b:];s=s.replace('Mental Arithmetic','Controlled Anger').replace('sealed-purse geometry','pressed-lip shader')
s=s.replace('is_equal_approx(delta.y,36.0*amount)','absf(delta.y-36.0*amount)<0.0001')
(W/'check_and_capture.gd').write_text(s)
s=(M/'render_motion.gd').read_text().replace('129','041').replace('"mouth_purse","gaze_y"','"mouth_lip_press"').replace('.080001','.260001').replace('subtle lids','narrow lids').replace('p.gaze_y<=0 and p.gaze_y>=-.800001','p.gaze_y==0 and p.gaze_x==0').replace('bounded upward gaze','fixed gaze')
a=s.index(' var left=records');b=s.index(' for record in records:',a)
s=s[:a]+''' var peak=records[45].pose;var easing=records[77].pose
 check(is_equal_approx(peak.brow_screen_left,-.7) and is_equal_approx(peak.brow_tilt_screen_left,.65),"moderate inward/down brow peak")
 check(is_equal_approx(peak.blink_L,.26) and is_equal_approx(peak.mouth_lip_press,.65),"narrow fixed eyes and restrained pressure")
 check(easing.mouth_lip_press<.4 and easing.brow_screen_left<-.69 and easing.blink_L>.259,"pressure eases before brows and eyes")
 for i in range(41,64):check(records[i].pose==peak,"still held peak "+str(i))
'''+s[b:]
s=s.replace('  if record.time>=1.45:check(record.pose.gaze_y==0,"glance finished "+str(record.time))','  check(record.pose.gaze_y==0 and record.pose.gaze_x==0,"fixed gaze "+str(record.time))')
s=s.replace('[.35,.65,1.1,1.45,1.95,2.2,2.65,3.15,3.7]','[.35,.6,.95,1.35,2.1,2.55,3.0,3.35,3.7]')
(W/'render_motion.gd').write_text(s)

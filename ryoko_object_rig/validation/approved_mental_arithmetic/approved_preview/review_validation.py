"""Independent read-only source/frame/decode review; never starts a renderer."""
from pathlib import Path
import hashlib,json,subprocess
import numpy as np
from PIL import Image,ImageDraw
w=Path(__file__).resolve().parent
out=w/'review_evidence';out.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rawsha=lambda im:hashlib.sha256(im.tobytes()).hexdigest()
freeze=json.loads((w/'BASELINE_FREEZE.json').read_text())
known=freeze['source_files_sha256'];rig=w/'rig';source=Path(freeze['source_rig'])
changed={str(root):[n for n,h in known.items() if not (root/n).is_file() or sha(root/n)!=h] for root in [rig,source]}
ids=[e['id'] for e in json.loads((rig/'expressions/registry.json').read_text())['entries']]
report={'scope':'Independent static pixels, all native frame hashes, source preservation, and MP4 decode/order review. No live pacing, whole-runtime, lip-sync, approval or integration claim.','baseline':freeze['baseline'],'baseline_commit':freeze.get('baseline_commit',freeze.get('published_baseline_commit')),'baseline_file_count':len(known),'baseline_png_count':sum(n.endswith('.png') for n in known),'frozen_source_changes':changed,'registry_ids':ids,'candidate_in_production_registry':'EXP-129' in ids}
ref=json.loads((w/'SOURCE_REFERENCE.json').read_text())
report['source_reference_hash_checks']={'sheet':sha(Path(ref['sheet']))==ref['sha256'],'catalogue':sha(Path(freeze['source_catalogue']))==freeze['catalogue_sha256']}
report['extra_manifest_hash_checks']={str(root):{n:sha(root/n)==h for n,h in freeze['extra_manifests_sha256'].items()} for root in [rig,source]}
rows=json.loads((w/'plan.json').read_text());names=[r['name'] for r in rows]
for view,size in [('full',(568,800)),('detail',(400,360))]:
 for path in (w/'motion'/view).glob('*.png'):assert Image.open(path).size==size, f'Invalid native dimensions: {path} {Image.open(path).size}, expected {size}'

# Contact sheet for visual evidence only, no retouching.
sheet=Image.new('RGB',(4*400,2*400),(32,34,36));d=ImageDraw.Draw(sheet)
for j,n in enumerate(names):
 im=Image.open(w/f'capture/{n}_detail.png').convert('RGB');x=(j%4)*400;y=(j//4)*400;sheet.paste(im,(x,y+30));d.text((x+10,y+8),n,fill='white')
sheet.save(out/'static_faces.png')
report['static']={}
for view in ['bust','detail']:
 n=np.asarray(Image.open(w/f'capture/neutral_{view}.png'))
 rec=[]
 for name in names:
  p=np.asarray(Image.open(w/f'capture/{name}_{view}.png'));m=np.any(n!=p,axis=2);ys,xs=np.nonzero(m)
  rec.append({'pose':name,'changed_pixels':int(m.sum()),'difference_bbox_xyxy':[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)] if len(xs) else None,'png_sha256':sha(w/f'capture/{name}_{view}.png')})
 report['static'][view]=rec
motion_path=w/'motion_checks.json';video=w/'Mental_arithmetic_review_v1.mp4'
if not motion_path.exists() or not video.exists():
 (out/'partial_review.json').write_text(json.dumps(report,indent=2)+'\n');raise SystemExit('Static and preservation evidence saved; motion/MP4 completion pending.')
motion=json.loads(motion_path.read_text());state=json.loads((w/'motion_state_checks.json').read_text())
report['native_motion']={k:v for k,v in motion.items() if k!='records'}
report['all_expected_121_frame_records']=len(motion['records'])==121 and all(r['frame']==i and abs(r['time']-i/30)<1e-12 for i,r in enumerate(motion['records']))
report['all_native_poses_match_headless']=[r['pose'] for r in motion['records']]==[r['pose'] for r in state['records']]
allrecs=[];frame_arrays={};diffs={};hash_ok=True
for vi,view in enumerate(['full','detail']):
 paths=sorted((w/'motion'/view).glob('*.png'));assert [p.name for p in paths]==[f'{i:04d}.png' for i in range(121)]
 arrays=[];neutral=np.asarray(Image.open(paths[0]));union=np.zeros(neutral.shape[:2],bool);drec=[]
 for i,p in enumerate(paths):
  im=Image.open(p);ar=np.asarray(im);rh=rawsha(im);expected=motion['records'][i]['hashes'][vi];hash_ok &= rh==expected
  arrays.append(ar[:,:,:3]);m=np.any(ar!=neutral,axis=2);union|=m
  allrecs.append({'view':view,'frame':i,'png_sha256':sha(p),'rgba_sha256':rh,'matches_capture_record':rh==expected})
  drec.append(int(m.sum()))
 ys,xs=np.nonzero(union);frame_arrays[view]=arrays
 diffs[view]={'changed_pixels_each_frame':drec,'union_difference_bbox_xyxy':[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],'neutral_bookends_identical':np.array_equal(arrays[0],arrays[-1]),'static_neutral_matches':np.array_equal(arrays[0],np.asarray(Image.open(w/f'capture/neutral_{"bust" if view=="full" else "detail"}.png'))[:,:,:3])}
 if view=='full':diffs[view]['all_pixels_outside_face_box_200_270_360_410_unchanged']=bool(not union[:270].any() and not union[410:].any() and not union[:,:200].any() and not union[:,360:].any())
report['native_motion_all_242_rgba_hashes_match']=bool(hash_ok);report['motion_pixel_changes']=diffs
(out/'native_frame_hashes.json').write_text(json.dumps(allrecs,indent=2)+'\n')
checks=json.loads((w/'capture/checks.json').read_text());report['static_native_checks']={'status':checks['status'],'checks':checks['checks'],'failures':checks['failures']}
report['static_vs_motion_exact']={}
for name,i in [('neutral',0),('left_lift_up',33),('right_lift',60),('neutral_return',120)]:
 report['static_vs_motion_exact'][name]={view:np.array_equal(np.asarray(Image.open(w/f'capture/{name}_{"bust" if view=="full" else "detail"}.png'))[:,:,:3],frame_arrays[view][i]) for view in ['full','detail']}
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_entries','stream=codec_name,width,height,pix_fmt,r_frame_rate,nb_frames,nb_read_frames:format=duration,size','-of','json',str(video)]))
report['video_probe']=probe;report['video_sha256']=sha(video)
pts=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','frame=best_effort_timestamp_time','-of','json',str(video)]))['frames']
report['mp4_monotonic_30fps_pts']=len(pts)==121 and all(abs(float(r['best_effort_timestamp_time'])-i/30)<1e-5 for i,r in enumerate(pts))
p=subprocess.Popen(['ffmpeg','-v','error','-i',str(video),'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
decoded=[];rbytes=968*800*3
while True:
 buf=p.stdout.read(rbytes)
 if not buf:break
 assert len(buf)==rbytes
 decoded.append(np.frombuffer(buf,np.uint8).reshape(800,968,3).copy())
err=p.stderr.read().decode();code=p.wait();report['mp4_full_decode']={'frames':len(decoded),'exit_code':code,'stderr':err};assert code==0 and len(decoded)==121
# Verify both visible native panels against their expected indexed source frames.
errors={'full':[],'detail':[]};nearest=[]
features=np.asarray([a[55:285,40:320].astype(np.float32)[::2,::2] for a in frame_arrays['detail']])
for i,ar in enumerate(decoded):
 for view,crop in [('full',ar[:800,:568]),('detail',ar[220:580,568:968])]:errors[view].append(float(np.abs(crop.astype(np.int16)-frame_arrays[view][i].astype(np.int16)).mean()))
 feat=ar[275:505,608:888].astype(np.float32)[::2,::2];dist=np.abs(features-feat).mean(axis=(1,2,3));best=float(dist.min());nearest.append({'frame':i,'expected_face_mae':float(dist[i]),'best_face_mae':best,'expected_minus_best':float(dist[i]-best),'best_matching_frame':int(dist.argmin())})
report['mp4_source_panel_mae']={k:{'mean':float(np.mean(v)),'max':max(v),'frames':len(v)} for k,v in errors.items()}
report['mp4_order_checks']={'method':'Every decoded RGB frame compared with same-index native full and detail panels; PTS inspected; nearest-frame face error exposes material reorder while acknowledging lossy compression and repeated/near-identical poses.','max_expected_face_mae':max(r['expected_face_mae'] for r in nearest),'max_expected_minus_best_face_mae':max(r['expected_minus_best'] for r in nearest),'selected': [nearest[i] for i in [0,20,33,44,60,66,80,111,120]],'all_frame_detail_file':'decoded_frame_order.json'}
(out/'decoded_frame_order.json').write_text(json.dumps(nearest,indent=2)+'\n')
# Selected decoded face strip preserves the shipped encoding for inspection.
sel=[0,20,33,44,60,66,80,111,120];sheet=Image.new('RGB',(400*3,390*3),(32,34,36));draw=ImageDraw.Draw(sheet)
for j,i in enumerate(sel):
 x=j%3*400;y=j//3*390;sheet.paste(Image.fromarray(decoded[i][220:580,568:968]),(x,y+30));draw.text((x+10,y+8),f'Encoded frame {i:03d} | {i/30:.3f} s',fill='white')
sheet.save(out/'encoded_keyframes.png')
# Four actual-size bust captures, not enlarged faces.
sheet=Image.new('RGB',(568*4,830),(32,34,36));draw=ImageDraw.Draw(sheet)
for j,i in enumerate([0,20,33,60]):
 sheet.paste(Image.fromarray(frame_arrays['full'][i]),(568*j,30));draw.text((568*j+12,9),f'Native frame {i:03d} | {i/30:.3f} s',fill='white')
sheet.save(out/'bust_progression.png')
poses=[r['pose'] for r in motion['records']]
candidate=json.loads((w/'EXP-129.json').read_text())
keys=candidate['keyframes'];errors=[]
for row in motion['records']:
 t=row['time'];a=keys[0];b=keys[-1]
 for left,right in zip(keys,keys[1:]):
  if left['time']<=t<=right['time']:a,b=left,right;break
 u=max(0.,min(1.,(t-a['time'])/(b['time']-a['time'])));q=u*u*(3-2*u)
 for channel,value in row['pose'].items():
  av=a['values'].get(channel,0.);bv=b['values'].get(channel,0.);expected=av+(bv-av)*q
  # Existing runtime applies a 0.30-second neutral-to-playing restart blend.
  if t<.30:
   v=t/.30;expected*=v*v*(3-2*v)
  errors.append(abs(value-expected))
report['independent_smoothstep_max_control_error']=max(errors)
report['mental_arithmetic_pose_assertions']={
 'independent_timeline_matches':max(errors)<1e-6,
 'initial_pinch_both_brows_lowered':poses[20]['brow_screen_left']<-.5 and poses[20]['brow_screen_right']<-.5,
 'first_lift_screen_left':poses[33]['brow_screen_left']>.6 and poses[33]['brow_screen_right']<-.3,
 'up_glance_with_first_lift':poses[33]['gaze_y']<-.79,
 'pinch_returns_between_lifts':poses[44]['brow_screen_left']<-.5 and poses[44]['brow_screen_right']<-.5,
 'second_lift_screen_right':poses[60]['brow_screen_right']>.6 and poses[60]['brow_screen_left']<-.3,
 'second_lift_gaze_centered':poses[60]['gaze_y']==0,
 'glance_finished_after_1_45_seconds':all(r['pose']['gaze_y']==0 for r in motion['records'] if r['time']>=1.45),
 'purse_released_by_frame80':all(p['mouth_purse']==0 for p in poses[80:]),
 'no_speech':all(p['mouth_open']==0 for p in poses),
 'bounded_symmetric_lids':all(p['blink_L']==p['blink_R'] and 0<=p['blink_L']<=.080001 for p in poses),
 'all_neutral_hold_pixels_exact':all(diffs[v]['changed_pixels_each_frame'][i]==0 for v in diffs for i in list(range(7))+list(range(111,121)))
}
report['independent_checks_pass']=bool(not any(changed.values()) and ids==freeze['baseline_profile_ids'] and 'EXP-129' not in ids and all(report['source_reference_hash_checks'].values()) and all(all(v.values()) for v in report['extra_manifest_hash_checks'].values()) and report['all_expected_121_frame_records'] and report['all_native_poses_match_headless'] and hash_ok and diffs['full']['all_pixels_outside_face_box_200_270_360_410_unchanged'] and all(v['neutral_bookends_identical'] and v['static_neutral_matches'] for v in diffs.values()) and report['mp4_monotonic_30fps_pts'] and max(r['expected_minus_best'] for r in nearest)<.10 and all(report['mental_arithmetic_pose_assertions'].values()) and all(all(v.values()) for v in report['static_vs_motion_exact'].values()))
report['normal_speed_continuous_observation']=False
report['approval']='UNAPPROVED; isolated review only'
(out/'review_checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['independent_checks_pass','mp4_full_decode','mp4_source_panel_mae','mp4_order_checks','mental_arithmetic_pose_assertions']},indent=2))

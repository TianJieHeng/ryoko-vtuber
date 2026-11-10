"""Independent read-only source/frame/decode review; never starts a renderer."""
from pathlib import Path
import hashlib,json,subprocess
import numpy as np
from PIL import Image,ImageDraw
w=Path(__file__).resolve().parent
# This script reads frozen inputs and writes derived evidence only. It never runs Godot.
# Native capture and MP4 encoding must finish before the review can pass.
out=w/'review_evidence';out.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rawsha=lambda im:hashlib.sha256(im.tobytes()).hexdigest()
freeze=json.loads((w/'BASELINE_FREEZE.json').read_text())
known=freeze['source_files_sha256'];rig=w/'rig';source=Path(freeze['source_rig'])
changed={str(root):[n for n,h in known.items() if not (root/n).is_file() or sha(root/n)!=h] for root in [rig,source]}
ids=[e['id'] for e in json.loads((rig/'expressions/registry.json').read_text())['entries']]
report={'scope':'Independent static pixels, all native frame hashes, source preservation, and MP4 decode/order review. No live pacing, whole-runtime, lip-sync, approval or integration claim.','baseline':freeze['baseline'],'baseline_commit':freeze.get('baseline_commit',freeze.get('published_baseline_commit')),'baseline_file_count':len(known),'baseline_png_count':sum(n.endswith('.png') for n in known),'frozen_source_changes':changed,'registry_ids':ids,'candidate_in_production_registry':'EXP-041' in ids}
ref=json.loads((w/'SOURCE_REFERENCE.json').read_text())
report['source_reference_hash_checks']={'sheet':sha(Path(ref['sheet']))==ref['sha256'],'catalogue':sha(Path(freeze['source_catalogue']))==freeze['catalogue_sha256'],'frozen_sheet':sha(Path(freeze['source_sheet']))==freeze['source_sheet_sha256'],'reference_identifies_frozen_sheet':Path(ref['sheet']).resolve()==Path(freeze['source_sheet']).resolve() and ref['sha256']==freeze['source_sheet_sha256']}
report['extra_manifest_hash_checks']={str(root):{n:sha(root/n)==h for n,h in freeze['extra_manifests_sha256'].items()} for root in [rig,source]}
rows=json.loads((w/'plan.json').read_text());names=[r['name'] for r in rows]
report['reviewed_input_sha256']={n:sha(w/n) for n in ['EXP-041.json','plan.json','SOURCE_REFERENCE.json','BASELINE_FREEZE.json','state_checks.json','motion_state_checks.json']}
required=[w/'capture/checks.json',w/'motion_checks.json',w/'Controlled_anger_review_v1.mp4']
required += [w/f'capture/{name}_{view}.png' for name in names for view in ['bust','detail']]
required += [w/f'motion/{view}/{i:04d}.png' for view in ['full','detail'] for i in range(121)]
missing=[str(p.relative_to(w)) for p in required if not p.is_file()]
if missing:
 report.update(status='PENDING',independent_checks_pass=False,missing_required_inputs=missing,approval='UNAPPROVED; isolated review only')
 (out/'partial_review.json').write_text(json.dumps(report,indent=2)+'\n')
 (out/'review_checks.json').write_text(json.dumps(report,indent=2)+'\n')
 raise SystemExit('PENDING: native capture/MP4 inputs incomplete. No renderer launched; see review_evidence/partial_review.json.')
report.update(status='RUNNING',independent_checks_pass=False)
(out/'review_checks.json').write_text(json.dumps(report,indent=2)+'\n')
# Never leave a prior PASS receipt behind after a failed rerun.
import sys
_original_excepthook=sys.excepthook
def _record_unhandled_failure(exc_type,exc_value,tb):
 report.update(status='FAIL',independent_checks_pass=False,failure=f'{exc_type.__name__}: {exc_value}')
 (out/'review_checks.json').write_text(json.dumps(report,indent=2)+'\n')
 _original_excepthook(exc_type,exc_value,tb)
sys.excepthook=_record_unhandled_failure
checks=json.loads((w/'capture/checks.json').read_text())
headless_static=json.loads((w/'state_checks.json').read_text())
report['static_receipt_pass']=bool(checks['status']=='PASS' and not checks['failures'] and checks['visual_capture'] is True and checks['baseline_profile_count']==freeze['baseline_profile_count'] and checks['study_poses']==8)
report['static_receipts_match_headless']=checks['records']==headless_static['records']
expected_static={f'{name}_{view}.png' for name in names for view in ['bust','detail']}
report['static_exact_membership']={p.name for p in (w/'capture').glob('*.png')}==expected_static
report['static_dimensions']={}
for name in names:
 for view,size in [('bust',(568,800)),('detail',(400,360))]:
  with Image.open(w/f'capture/{name}_{view}.png') as im:
   report['static_dimensions'][f'{name}_{view}']=im.size==size and im.mode=='RGBA'
assert report['static_exact_membership'], 'Unexpected static PNG membership'
assert all(report['static_dimensions'].values()), 'Invalid static image dimensions or mode'

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
motion_path=w/'motion_checks.json';video=w/'Controlled_anger_review_v1.mp4'
if not motion_path.exists() or not video.exists():
 (out/'partial_review.json').write_text(json.dumps(report,indent=2)+'\n');raise SystemExit('Static and preservation evidence saved; motion/MP4 completion pending.')
motion=json.loads(motion_path.read_text());state=json.loads((w/'motion_state_checks.json').read_text())
report['native_motion']={k:v for k,v in motion.items() if k!='records'}
report['native_motion_receipt_pass']=bool(motion['status']=='PASS' and not motion['failures'] and motion['visual_capture'] is True and motion['baseline_profile_count']==freeze['baseline_profile_count'] and motion['frames']==121 and motion['fps']==30 and motion['duration']==4.0 and motion['display']!='headless')
report['all_expected_121_frame_records']=len(motion['records'])==121 and all(r['frame']==i and abs(r['time']-i/30)<1e-12 for i,r in enumerate(motion['records']))
report['all_native_poses_match_headless']=[r['pose'] for r in motion['records']]==[r['pose'] for r in state['records']]
allrecs=[];frame_arrays={};rgba_arrays={};diffs={};hash_ok=True
for vi,view in enumerate(['full','detail']):
 paths=sorted((w/'motion'/view).glob('*.png'));assert [p.name for p in paths]==[f'{i:04d}.png' for i in range(121)]
 arrays=[];raw_arrays=[];neutral=np.asarray(Image.open(paths[0]));union=np.zeros(neutral.shape[:2],bool);drec=[]
 for i,p in enumerate(paths):
  im=Image.open(p);assert im.mode=='RGBA',f'Unexpected native mode: {p} {im.mode}';ar=np.asarray(im);rh=rawsha(im);expected=motion['records'][i]['hashes'][vi];hash_ok &= rh==expected
  arrays.append(ar[:,:,:3]);raw_arrays.append(ar);m=np.any(ar!=neutral,axis=2);union|=m
  allrecs.append({'view':view,'frame':i,'png_sha256':sha(p),'rgba_sha256':rh,'matches_capture_record':rh==expected})
  drec.append(int(m.sum()))
 ys,xs=np.nonzero(union);frame_arrays[view]=arrays;rgba_arrays[view]=raw_arrays
 diffs[view]={'changed_pixels_each_frame':drec,'union_difference_bbox_xyxy':([int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)] if len(xs) else None),'neutral_bookends_identical':np.array_equal(raw_arrays[0],raw_arrays[-1]),'static_neutral_matches':np.array_equal(raw_arrays[0],np.asarray(Image.open(w/f'capture/neutral_{"bust" if view=="full" else "detail"}.png')))}
 if view=='full':diffs[view]['all_pixels_outside_face_box_200_270_360_410_unchanged']=bool(not union[:270].any() and not union[410:].any() and not union[:,:200].any() and not union[:,360:].any())
report['native_motion_all_242_rgba_hashes_match']=bool(hash_ok);report['motion_pixel_changes']=diffs
(out/'native_frame_hashes.json').write_text(json.dumps(allrecs,indent=2)+'\n')
checks=json.loads((w/'capture/checks.json').read_text());report['static_native_checks']={'status':checks['status'],'checks':checks['checks'],'failures':checks['failures']}
report['static_vs_motion_exact']={}
for name,i in [('neutral',0),('restrain',18),('controlled_anger',45),('soften',90),('neutral_return',120)]:
 report['static_vs_motion_exact'][name]={view:np.array_equal(np.asarray(Image.open(w/f'capture/{name}_{"bust" if view=="full" else "detail"}.png')),rgba_arrays[view][i]) for view in ['full','detail']}
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_entries','stream=codec_name,width,height,pix_fmt,r_frame_rate,nb_frames,nb_read_frames:format=duration,size','-of','json',str(video)]))
report['video_probe']=probe;report['video_sha256']=sha(video)
stream=probe['streams'][0]
report['video_metadata_valid']=len(probe['streams'])==1 and stream['codec_name']=='h264' and stream['width']==968 and stream['height']==800 and stream['pix_fmt']=='yuv420p' and stream['r_frame_rate']=='30/1' and int(stream['nb_read_frames'])==121
assert report['video_metadata_valid'], 'Unexpected MP4 format or frame count'

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
report['mp4_order_checks']={'method':'Every decoded RGB frame compared with same-index native full and detail panels; PTS inspected; nearest-frame face error exposes material reorder while acknowledging lossy compression and repeated/near-identical poses.','max_expected_face_mae':max(r['expected_face_mae'] for r in nearest),'max_expected_minus_best_face_mae':max(r['expected_minus_best'] for r in nearest),'selected': [nearest[i] for i in [0,18,29,41,63,77,90,101,120]],'all_frame_detail_file':'decoded_frame_order.json'}
(out/'decoded_frame_order.json').write_text(json.dumps(nearest,indent=2)+'\n')
# Selected decoded face strip preserves the shipped encoding for inspection.
sel=[0,18,29,41,63,77,90,101,120];sheet=Image.new('RGB',(400*3,390*3),(32,34,36));draw=ImageDraw.Draw(sheet)
for j,i in enumerate(sel):
 x=j%3*400;y=j//3*390;sheet.paste(Image.fromarray(decoded[i][220:580,568:968]),(x,y+30));draw.text((x+10,y+8),f'Encoded frame {i:03d} | {i/30:.3f} s',fill='white')
sheet.save(out/'encoded_keyframes.png')
# Four actual-size bust captures, not enlarged faces.
sheet=Image.new('RGB',(568*4,830),(32,34,36));draw=ImageDraw.Draw(sheet)
for j,i in enumerate([0,18,41,77]):
 sheet.paste(Image.fromarray(frame_arrays['full'][i]),(568*j,30));draw.text((568*j+12,9),f'Native frame {i:03d} | {i/30:.3f} s',fill='white')
sheet.save(out/'bust_progression.png')
poses=[r['pose'] for r in motion['records']]
candidate=json.loads((w/'EXP-041.json').read_text())
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
allowed={'brow_screen_left','brow_screen_right','brow_tilt_screen_left','brow_tilt_screen_right','blink_L','blink_R','mouth_lip_press'}
peak=poses[45]
report['controlled_anger_pose_assertions']={
 'independent_timeline_matches':max(errors)<1e-6,
 'moderate_inward_downward_peak':abs(peak['brow_screen_left']+.7)<1e-6 and abs(peak['brow_tilt_screen_left']-.65)<1e-6,
 'restrained_peak_pressure':abs(peak['mouth_lip_press']-.65)<1e-6,
 'peak_lids_fixed_narrow':abs(peak['blink_L']-.26)<1e-6,
 'still_peak_frames41_through63':all(p==peak for p in poses[41:64]),
 'pressure_releases_before_eyes_brows':poses[77]['mouth_lip_press']<.4 and poses[77]['brow_screen_left']<-.69 and poses[77]['blink_L']>.259,
 'symmetric_brows':all(p['brow_screen_left']==p['brow_screen_right'] and p['brow_tilt_screen_left']==-p['brow_tilt_screen_right'] for p in poses),
 'bounded_symmetric_lids':all(p['blink_L']==p['blink_R'] and 0<=p['blink_L']<=.260001 for p in poses),
 'fixed_gaze':all(p['gaze_x']==0 and p['gaze_y']==0 for p in poses),
 'only_approved_acting_channels':all(v==0 for p in poses for k,v in p.items() if k not in allowed),
 'all_neutral_hold_controls_exact':all(all(v==0 for v in poses[i].values()) for i in list(range(7))+list(range(111,121))),
 'all_neutral_hold_pixels_exact':all(diffs[v]['changed_pixels_each_frame'][i]==0 for v in diffs for i in list(range(7))+list(range(111,121))),
 'peak_is_visibly_non_neutral':all(diffs[v]['changed_pixels_each_frame'][45]>0 for v in diffs),
 'maximum_frame_step_below_0_20':all(abs(poses[i][k]-poses[i-1][k])<.20 for i in range(1,len(poses)) for k in allowed)
}
report['static_plan_matches_receipts']=bool([r['name'] for r in checks['records']]==names and all(abs(record['pose'][k]-row['pose'].get(k,0))<1e-6 for row,record in zip(rows,checks['records']) for k in record['pose']))
report['mp4_lossy_panel_error_within_review_limits']=all(v['max']<3.0 for v in report['mp4_source_panel_mae'].values())
# The 3.0 RGB MAE ceiling catches corruption; the inherited 0.10 nearest-frame gap
# catches material reordering. Near-identical/repeated source poses are ambiguous.
report['independent_checks_pass']=bool(report['static_receipt_pass'] and report['static_receipts_match_headless'] and report['static_exact_membership'] and all(report['static_dimensions'].values()) and report['static_plan_matches_receipts'] and report['native_motion_receipt_pass'] and report['video_metadata_valid'] and report['mp4_lossy_panel_error_within_review_limits'] and not any(changed.values()) and ids==freeze['baseline_profile_ids'] and 'EXP-041' not in ids and all(report['source_reference_hash_checks'].values()) and all(all(v.values()) for v in report['extra_manifest_hash_checks'].values()) and report['all_expected_121_frame_records'] and report['all_native_poses_match_headless'] and hash_ok and diffs['full']['all_pixels_outside_face_box_200_270_360_410_unchanged'] and all(v['neutral_bookends_identical'] and v['static_neutral_matches'] for v in diffs.values()) and report['mp4_monotonic_30fps_pts'] and max(r['expected_minus_best'] for r in nearest)<.10 and all(report['controlled_anger_pose_assertions'].values()) and all(all(v.values()) for v in report['static_vs_motion_exact'].values()))
report['status']='PASS' if report['independent_checks_pass'] else 'FAIL'
report['normal_speed_continuous_observation']=False
report['approval']='UNAPPROVED; isolated review only'
(out/'review_checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['independent_checks_pass','mp4_full_decode','mp4_source_panel_mae','mp4_order_checks','controlled_anger_pose_assertions']},indent=2))

if not report['independent_checks_pass']:raise SystemExit('FAIL: independent native/MP4 checks; see review_evidence/review_checks.json.')

"""Independent review of captured v2 evidence. No renderer or GUI use."""
import hashlib,json,subprocess
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
W=Path(__file__).resolve().parents[1]; M=W/'motion_study'; O=W/'review'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rgb(p):return np.asarray(Image.open(p).convert('RGB'))
def bbox(mask):
 y,x=np.where(mask);return [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)] if len(x) else None
def differences(a,b):
 d=np.abs(a.astype(np.int16)-b.astype(np.int16)); mask=np.any(d,axis=2)
 return {'changed_pixels':int(mask.sum()),'bbox_exclusive':bbox(mask),'rgb_absolute_sum':int(d.sum())}
def verify_files(root,files):return [p for p,h in files.items() if not (root/p).is_file() or sha(root/p)!=h]
freeze=json.loads((W/'BASELINE_FREEZE.json').read_text());old=json.loads((W/'V1_PROVENANCE.json').read_text());sf=json.loads((W/'STATIC_ALTERNATIVES_FREEZE.json').read_text())
native=json.loads((M/'motion_checks.json').read_text());state=json.loads((M/'motion_state_checks.json').read_text());profile=json.loads((M/'EXP-139.json').read_text());registry=json.loads((W/'rig/expressions/registry.json').read_text())['entries']
channels={'brow_screen_left','brow_screen_right','brow_tilt_screen_left','brow_tilt_screen_right','mouth_lip_press','mouth_width_screen_left','mouth_width_screen_right','blink_L','blink_R'}
checks={}; result={'checks':checks,'approval':'UNAPPROVED','normal_speed_observed_by_this_reviewer':False}
checks['native_capture_success']=native['status']=='PASS' and not native['failures'] and native['visual_capture'] and native['frames']==121
checks['headless_state_success']=state['status']=='PASS' and not state['failures'] and not state['visual_capture']
checks['native_headless_pose_and_time_identity']=len(native['records'])==len(state['records'])==121 and all(all(a[k]==b[k] for k in ['frame','time','pose']) for a,b in zip(native['records'],state['records']))
checks['chronological_native_samples']=all(r['frame']==i and abs(r['time']-i/30)<1e-12 for i,r in enumerate(native['records']))
checks['only_nine_declared_acting_channels']=all(v==0 for r in native['records'] for k,v in r['pose'].items() if k not in channels)
checks['eyes_fully_open_from_070_through_recovery']=all(r['pose']['blink_L']==r['pose']['blink_R']==0 for r in native['records'] if r['time']>=.70)
checks['blink_symmetric_and_reaches_full_closure']=all(r['pose']['blink_L']==r['pose']['blink_R'] for r in native['records']) and max(r['pose']['blink_L'] for r in native['records'])==1
# Independent scalar smoothstep reconstruction of the declared control timeline.
errs=[]
for row in native['records']:
 t=row['time'];left=profile['keyframes'][0];right=left
 for l,r in zip(profile['keyframes'],profile['keyframes'][1:]):
  if l['time']<=t<=r['time']+1e-12:left,right=l,r;break
 if t>=profile['keyframes'][-1]['time']:left=right=profile['keyframes'][-1]
 u=0 if left==right else max(0,min(1,(t-left['time'])/(right['time']-left['time'])));s=u*u*(3-2*u)
 for key,val in row['pose'].items():
  a=left['values'].get(key,0);b=right['values'].get(key,0);expected=a+(b-a)*s
  # Existing initial/retrigger blend also applies before 0.30 seconds.
  if t<.30:
   q=max(0,min(1,t/.30));expected*=q*q*(3-2*q)
  errs.append(abs(val-expected))
checks['native_matches_independent_timeline_and_existing_restart_blend']=max(errs)<1e-6;result['maximum_control_reconstruction_error']=max(errs)
result['rig_mismatches']=verify_files(W/'rig',freeze['source_files_sha256']);checks['1112_frozen_rig_files_unchanged']=not result['rig_mismatches'] and len(freeze['source_files_sha256'])==1112
result['v1_mismatches']=verify_files(Path(old['source_work']),old['files']);checks['v1_frozen_evidence_preserved']=not result['v1_mismatches']
result['static_mismatches']=verify_files(W,sf['files']);checks['static_alternatives_preserved']=not result['static_mismatches']
checks['source_sheet_exact']=sha(Path(freeze['source_sheet']))==freeze['source_sheet_sha256']
checks['source_catalogue_exact']=sha(Path(freeze['source_catalogue']))==freeze['catalogue_sha256']
checks['registry_27_no_candidate']=[r['id'] for r in registry]==freeze['baseline_profile_ids'] and len(registry)==27 and all(r['id']!='EXP-139' for r in registry)
frames={};masks={};result['native_images']={};result['static_comparison']={}
for j,view in enumerate(['full','detail']):
 files=sorted((M/'motion'/view).glob('*.png'));checks[f'{view}_exact_complete_numbered_set']=[p.name for p in files]==[f'{i:04d}.png' for i in range(121)]
 arr=[];hashes=[]
 for p in files:
  im=Image.open(p);hashes.append(hashlib.sha256(im.tobytes()).hexdigest());arr.append(np.asarray(im.convert('RGB')))
 frames[view]=arr;a=arr[0];mask=np.zeros(a.shape[:2],bool)
 for b in arr:mask|=np.any(a!=b,axis=2)
 masks[view]=mask;suffix='bust' if view=='full' else 'detail'
 checks[f'{view}_all_121_native_hashes_exact']=all(h==r['hashes'][j] for h,r in zip(hashes,native['records']))
 checks[f'{view}_exact_native_neutral_bookends']=np.array_equal(a,arr[-1])
 checks[f'{view}_static_neutral_and_return_equal_native']=all(np.array_equal(a,rgb(W/f'capture/{name}_{suffix}.png')) for name in ['neutral','neutral_return'])
 checks[f'{view}_selected_peak_equals_static_C']=np.array_equal(arr[24],rgb(W/f'capture/c_strongest_open_{suffix}.png'))
 checks[f'{view}_reopened_matches_onset_static']=np.array_equal(arr[21],rgb(W/f'onset_study/capture/reopened_{suffix}.png'))
 checks[f'{view}_closed_matches_onset_static']=np.array_equal(arr[15],rgb(W/f'onset_study/capture/blink_closed_{suffix}.png'))
 checks[f'{view}_peak_held_exact_frames24_through72']=all(np.array_equal(b,arr[24]) for b in arr[24:73])
 checks[f'{view}_v1_reference_equals_v1_original']=np.array_equal(rgb(W/f'capture/v1_peak_reference_{suffix}.png'),rgb(Path(old['source_work'])/f'capture/focused_determination_{suffix}.png'))
 result['native_images'][view]={'size':[a.shape[1],a.shape[0]],'unique_decoded_hashes':len(set(hashes)),'all_frame_changed_pixels':int(mask.sum()),'changed_bbox_exclusive':bbox(mask),'neutral_frames':[i for i,b in enumerate(arr) if np.array_equal(a,b)],'exact_peak_frames':[i for i,b in enumerate(arr) if np.array_equal(arr[24],b)],'per_frame':[{'frame':i,**differences(a,b),'image_rgba_sha256':hashes[i]} for i,b in enumerate(arr)]}
 v1=rgb(W/f'capture/v1_peak_reference_{suffix}.png');v2=arr[24]
 result['static_comparison'][view]={'neutral_to_v1':differences(a,v1),'neutral_to_v2':differences(a,v2),'v1_to_v2':differences(v1,v2)}
 for n,b in [('v1',v1),('v2',v2)]:
  if view=='detail':result['static_comparison'][view][n+'_region_pixels']={'brows':differences(a[:113],b[:113])['changed_pixels'],'mouth':differences(a[240:275],b[240:275])['changed_pixels']}
checks['full_body_below_y400_unchanged']=not masks['full'][400:].any()
# Pixel-stability limits are explicit, not an automatic assertion that moving-eye seams are clean.
checks['detail_below_y280_unchanged']=not masks['detail'][280:].any()
checks['open_peak_eye_core_matches_neutral']=np.array_equal(frames['detail'][24][113:170],frames['detail'][0][113:170])
# y110..112 includes the newly lowered brow tip, not the eye.
checks['post_blink_eye_core_matches_neutral']=all(np.array_equal(b[113:170],frames['detail'][0][113:170]) for b in frames['detail'][21:])
for name,(x1,y1,x2,y2) in {'left_hair_lid_seam':(30,86,83,125),'right_hair_lid_seam':(275,85,337,125)}.items():
 checks[name+'_unchanged_when_reopened']=all(np.array_equal(b[y1:y2,x1:x2],frames['detail'][0][y1:y2,x1:x2]) for b in frames['detail'][21:])
result['corrected_initial_diagnostics']={'timeline':'The first reconstruction omitted the shared 0.30s initial/retrigger smoothstep. Only frame 8 differed, at most 0.001082. This was an independent test-model omission, not a runtime failure. The corrected model includes that unchanged runtime behavior, with the same 1e-6 threshold.','eye_roi':'The original y110:170 eye ROI included 25 pixels of the stronger brow tip at x144:154 y110:112. Visual inspection confirms these are brow pixels. Eye core is y113:170. Original results preserved in initial_review_diagnostics.json.'}
# Diagnostic native image panels, without scaling input captures.
canvas=Image.new('RGB',(1704,830),'#eeeeee');draw=ImageDraw.Draw(canvas)
for j,(label,path) in enumerate([('Neutral',W/'capture/neutral_bust.png'),('V1 peak (rejected as too subtle)',W/'capture/v1_peak_reference_bust.png'),('V2 selected C peak',W/'capture/c_strongest_open_bust.png')]):
 draw.text((j*568+10,10),label,fill='black');canvas.paste(Image.open(path).convert('RGB'),(j*568,30))
canvas.save(O/'full_bust_v1_v2_comparison.png')
inspect=[0,10,12,15,18,21,24,48,72,78,90,100,109,110,120];result['visually_inspected_motion_frames']=inspect
canvas=Image.new('RGB',(2000,1170),'#eeeeee');draw=ImageDraw.Draw(canvas)
for j,i in enumerate(inspect):
 x=j%5*400;y=j//5*390;draw.text((x+8,y+7),f'Native {i:04d} / {i/30:.3f}s',fill='black');canvas.paste(Image.fromarray(frames['detail'][i]),(x,y+30))
canvas.save(O/'native_motion_detail_contact_sheet.png')
video=M/'Focused_determination_review_v2.mp4'
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_streams','-show_format','-show_frames','-of','json',str(video)]));stream=probe['streams'][0];vf=probe['frames']
result['video']={'sha256':sha(video),'codec':stream['codec_name'],'size':[stream['width'],stream['height']],'frame_rate':stream['r_frame_rate'],'reported_frames':stream['nb_frames'],'duration':probe['format']['duration'],'bytes':video.stat().st_size}
checks['mp4_format_and_frame_count']=stream['codec_name']=='h264' and (stream['width'],stream['height'])==(968,800) and stream['r_frame_rate']=='30/1' and len(vf)==121 and stream['nb_frames']=='121'
checks['mp4_pts_exact_30hz_chronology']=all(abs(float(f['best_effort_timestamp_time'])-i/30)<1e-6 for i,f in enumerate(vf))
p=subprocess.Popen(['ffmpeg','-v','error','-i',str(video),'-map','0:v:0','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE);decode_errors=[];decoded=[]
for i in range(121):
 raw=p.stdout.read(968*800*3)
 if len(raw)!=968*800*3:raise RuntimeError(f'Short video decode frame {i}')
 a=np.frombuffer(raw,np.uint8).reshape((800,968,3));full=a[:,:568];detail=a[220:580,568:968]
 decode_errors.append({'frame':i,**{view:float(np.abs(val.astype(np.int16)-frames[view][i].astype(np.int16)).mean()) for view,val in [('full',full),('detail',detail)]}})
 if i in inspect:decoded.append((i,detail.copy()))
extra=p.stdout.read();stderr=p.stderr.read().decode();rc=p.wait();checks['full_mp4_decode_clean']=rc==0 and not stderr and not extra
result['video']['rgb_mean_absolute_errors']={v:{'mean':float(np.mean([r[v] for r in decode_errors])),'max':float(max(r[v] for r in decode_errors))} for v in ['full','detail']};result['video']['per_frame_rgb_error']=decode_errors
canvas=Image.new('RGB',(2000,1170),'#eeeeee');draw=ImageDraw.Draw(canvas)
for j,(i,a) in enumerate(decoded):
 x=j%5*400;y=j//5*390;draw.text((x+8,y+7),f'Decoded {i:04d} / {i/30:.3f}s',fill='black');canvas.paste(Image.fromarray(a),(x,y+30))
canvas.save(O/'decoded_motion_detail_contact_sheet.png')
# Independently compose the numeric native sequence; exact decoded YUV hashes and PTS prove ordering.
expected=O/'expected_chronological_sequence.mp4'
f='[1:v]pad=400:800:0:220:color=0x202224,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text=Focused determination:fontcolor=white:fontsize=22:x=(w-tw)/2:y=135,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text=Review candidate v2:fontcolor=0xbfc4ca:fontsize=16:x=(w-tw)/2:y=170[d];[0:v][d]hstack=inputs=2[v]'
cmd=['ffmpeg','-v','error','-nostdin','-y','-framerate','30','-start_number','0','-i',str(M/'motion/full/%04d.png'),'-framerate','30','-start_number','0','-i',str(M/'motion/detail/%04d.png'),'-filter_complex',f,'-map','[v]','-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart',str(expected)]
subprocess.run(cmd,check=True)
def hashes(p):return subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:v:0','-f','framemd5','-']).decode()
a=hashes(video);b=hashes(expected);(O/'delivered_video.framemd5').write_text(a);(O/'expected_chronological_sequence.framemd5').write_text(b)
rows=lambda s:[r for r in s.splitlines() if r and not r.startswith('#')]
checks['all_121_decoded_frames_and_pts_match_numeric_reconstruction']=len(rows(a))==121 and rows(a)==rows(b)
result['video']['chronological_reconstruction']={'decoded_frames':len(rows(a)),'exact_yuv_hashes_and_times':rows(a)==rows(b),'expected_mp4_sha256':sha(expected),'command':cmd,'limit':'Verifies delivered captured sequence, not continuous normal-speed viewing or live runtime pacing.'}
result['evidence_counts']={'native_static':json.loads((W/'capture/checks.json').read_text())['checks'],'native_onset':json.loads((W/'onset_study/capture/checks.json').read_text())['checks'],'native_motion':native['checks'],'headless_motion':state['checks'],'rig_files':len(freeze['source_files_sha256']),'rig_pngs':sum(p.endswith('.png') for p in freeze['source_files_sha256']),'v1_files':len(old['files']),'static_files':len(sf['files'])}
result['failed_checks']=[k for k,v in checks.items() if not v];result['status']='PASS' if not result['failed_checks'] else 'FAIL'
(O/'independent_review_metrics.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['native_images','video']},indent=2));print(json.dumps({k:v for k,v in result['video'].items() if k not in ['per_frame_rgb_error','chronological_reconstruction']},indent=2))

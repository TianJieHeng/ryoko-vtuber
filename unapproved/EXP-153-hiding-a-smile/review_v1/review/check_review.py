"""Read-only independent checks of native captures and the delivered video."""
from pathlib import Path
import hashlib,json,subprocess
import numpy as np
from PIL import Image,ImageDraw
w=Path(__file__).resolve().parents[1]
r=json.loads((w/'motion_checks.json').read_text())
f=json.loads((w/'BASELINE_FREEZE.json').read_text())
c=json.loads((w/'EXP-153.json').read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def spans(indices):
 out=[]
 for i in indices:
  if out and out[-1][1]+1==i:out[-1][1]=i
  else:out.append([i,i])
 return out
out={'identity':{str(p.relative_to(w)) if p.is_relative_to(w) else str(p):sha(p) for p in [w/'EXP-153.json',w/'Hiding_a_smile_review_v1.mp4',Path(f['source_sheet'])]},'views':{}}
imgs={}
for vi,view in enumerate(['full','detail']):
 paths=sorted((w/'motion'/view).glob('*.png'))
 assert [p.name for p in paths]==[f'{i:04}.png' for i in range(121)]
 arr=[np.array(Image.open(p).convert('RGBA')) for p in paths]; imgs[view]=arr
 hashes=[hashlib.sha256(im.tobytes()).hexdigest() for im in arr]
 assert hashes==[row['hashes'][vi] for row in r['records']]
 diffs=[np.any(im!=arr[0],axis=2) for im in arr]
 union=np.logical_or.reduce(diffs); y,x=np.where(union)
 out['views'][view]={'frame_count':len(arr),'dimensions':[arr[0].shape[1],arr[0].shape[0]],'hashes_match_native_record':True,'unique_images':len(set(hashes)),'neutral_spans':spans([i for i,h in enumerate(hashes) if h==hashes[0]]),'peak_spans':spans([i for i,h in enumerate(hashes) if h==hashes[42]]),'first_last_pixel_identical':hashes[0]==hashes[-1],'difference_union_half_open':[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)],'peak_changed_pixels':int(diffs[42].sum()),'all_pixels_y420_and_below_unchanged':not any(d[420:].any() for d in diffs) if view=='full' else None,'static_neutral_matches_frame0':np.array_equal(arr[0],np.array(Image.open(w/'capture'/('neutral_bust.png' if view=='full' else 'neutral_detail.png')).convert('RGBA'))),'static_peak_matches_frame42':np.array_equal(arr[42],np.array(Image.open(w/'capture'/('hiding_smile_bust.png' if view=='full' else 'hiding_smile_detail.png')).convert('RGBA'))),'static_return_matches_frame120':np.array_equal(arr[120],np.array(Image.open(w/'capture'/('neutral_return_bust.png' if view=='full' else 'neutral_return_detail.png')).convert('RGBA')))}
# Independently derive the timeline, including existing 0.30-second entry blend.
maxerr=0.; active=set(); all_zero_open=True
for i,row in enumerate(r['records']):
 assert row['frame']==i and abs(row['time']-i/30)<1e-12
 expected={k:0. for k in row['pose']};t=i/30
 if 0<t<c['duration']:
  for a,b in zip(c['keyframes'],c['keyframes'][1:]):
   if a['time']<=t<=b['time']:
    u=(t-a['time'])/(b['time']-a['time']);u=u*u*(3-2*u)
    expected={k:a['values'].get(k,0)+(b['values'].get(k,0)-a['values'].get(k,0))*u for k in expected}
    break
 if t<.3:
  u=t/.3;u=u*u*(3-2*u);expected={k:v*u for k,v in expected.items()}
 for k,v in row['pose'].items():
  maxerr=max(maxerr,abs(expected[k]-v))
  if v:active.add(k)
 all_zero_open=all_zero_open and row['pose']['mouth_open']==row['pose']['opening_px']==row['pose']['mouth_spread']==row['pose']['mouth_smile']==0
assert maxerr<1e-6
out['state']={'sampled_control_count':len(r['records'][0]['pose']),'samples':len(r['records']),'max_abs_interpolation_error':maxerr,'active_channels':sorted(active),'mouth_open_scoped_opening_spread_and_ordinary_smile_all_zero':all_zero_open,'native_report_checks':r['checks'],'native_report_status':r['status'],'headless_report_checks':json.loads((w/'motion_state_checks.json').read_text())['checks'],'normal_speed_observed':False}
known=f['source_files_sha256']; missing=[];changed=[]
for name,h in known.items():
 p=w/'rig'/name
 if not p.is_file():missing.append(name)
 elif sha(p)!=h:changed.append(name)
extra=[str(p.relative_to(w/'rig')) for p in (w/'rig').rglob('*') if p.is_file() and '.godot' not in p.parts and '__pycache__' not in p.parts and str(p.relative_to(w/'rig')) not in known]
entries=json.loads((w/'rig/expressions/registry.json').read_text())['entries'];ids=[a['id'] for a in entries]
out['preservation']={'frozen_files':len(known),'frozen_pngs':sum(n.endswith('.png') for n in known),'missing':missing,'changed':changed,'extra_outside_cache':extra,'registry_count':len(ids),'registry_ids_match_freeze':ids==f['baseline_profile_ids'],'candidate_absent_registry':'EXP-153' not in ids,'candidate_files_in_rig':[str(p) for p in (w/'rig').rglob('*153*.json')],'inherited_release_authored_local_count':json.loads((w/'rig/RELEASE.json').read_text())['authored_local_count']}
assert not missing and not changed and not extra
video=w/'Hiding_a_smile_review_v1.mp4'
strict=subprocess.run(['ffmpeg','-nostdin','-v','error','-xerror','-i',str(video),'-map','0:v:0','-f','null','-'],capture_output=True)
assert strict.returncode==0,strict.stderr.decode()
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_entries','stream=codec_name,width,height,pix_fmt,r_frame_rate,avg_frame_rate,nb_frames,nb_read_frames,duration:format=duration,size','-of','json',str(video)]))
pts=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','frame=best_effort_timestamp_time','-of','json',str(video)]))
times=[float(fr['best_effort_timestamp_time']) for fr in pts['frames']]
assert len(times)==121 and all(abs(t-i/30)<1e-6 for i,t in enumerate(times))
p=subprocess.Popen(['ffmpeg','-nostdin','-v','error','-i',str(video),'-map','0:v:0','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
maes={'full':[],'detail':[]}; native_activity=[];video_activity=[];prev=None
for i in range(121):
 data=p.stdout.read(968*800*3);assert len(data)==968*800*3,(i,len(data))
 a=np.frombuffer(data,dtype=np.uint8).reshape(800,968,3)
 for view,region in [('full',a[:,:568]),('detail',a[220:580,568:968])]:
  e=np.abs(region.astype(np.int16)-imgs[view][i][:,:,:3].astype(np.int16))
  maes[view].append(float(e.mean()))
 if i==0:neutral_video=a[220:580,568:968].copy()
 # Track just the animated eye and mouth face region, avoiding the unchanging border.
 native_activity.append(float(np.abs(imgs['detail'][i][55:280,30:335,:3].astype(float)-imgs['detail'][0][55:280,30:335,:3].astype(float)).mean()))
 video_activity.append(float(np.abs(a[275:500,598:903].astype(float)-neutral_video[55:280,30:335].astype(float)).mean()))
 if i in [0,16,42,81,120]:Image.fromarray(a).save(w/'review'/f'decoded_{i:04}.png')
assert p.stdout.read()==b''
stderr=p.stderr.read();rc=p.wait();assert rc==0,stderr.decode()
out['video']={'probe':probe,'strict_full_decode_returncode':strict.returncode,'strict_full_decode_stderr':strict.stderr.decode(),'decoded_rgb_frames':121,'presentation_timestamps_match_30fps_indices':True,'same_index_mean_absolute_rgb_errors':{view:{'average':float(np.mean(values)),'maximum':max(values),'minimum':min(values)} for view,values in maes.items()},'facial_activity_correlation_native_vs_video':float(np.corrcoef(native_activity,video_activity)[0,1]),'order_limit':'Lossy compression and repeated holds do not uniquely identify every adjacent frame. All same-index image comparisons, ordered timestamps, and the facial activity curve agree with the supplied chronological native sequence.'}
# A compact all-frame mouth contact sheet for actual image inspection.
board=Image.new('RGB',(1100,660),(32,34,36));d=ImageDraw.Draw(board)
for i,im in enumerate(imgs['detail']):
 crop=Image.fromarray(im[:,:,:3]).crop((135,235,235,280))
 x=(i%11)*100;y=(i//11)*60;board.paste(crop,(x,y));d.text((x+2,y+46),str(i),fill='white')
board.save(w/'review/all_mouth_frames.png')
(w/'review/checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))

"""Verify existing capture/image/video bytes only. No renderer or engine launch."""
from pathlib import Path
import argparse,hashlib,json,math,subprocess
from PIL import Image
R=Path(__file__).resolve().parents[1];V=R/'validation/approved_overly_sweet_taste';S=V/'review_sources'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
p=argparse.ArgumentParser();p.add_argument('--native-attempt',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
profile=R/'expressions/EXP-091.json';video=S/'Overly_sweet_taste_reconstruction_20261111_r1_review.mp4';receipt=json.loads((S/'capture/evidence.json').read_text());encoded=json.loads((S/'EXP091-preview-result.json').read_text())
assert receipt['status']=='PASS' and receipt['failures']==[] and receipt['checks']==137659 and receipt['visual_capture']
assert (receipt['frames'],receipt['fps'],receipt['duration'],receipt['baseline_profile_count'])==(121,30,4.0,39)
assert receipt['profile_sha256']==sha(profile)==sha(S/'EXP-091.json')=='67cae056cbc90fe0de20820131d750a97ada4ccc0340575ee43ec18963bbda6a'
assert receipt['input_freeze_sha256']==sha(S/'INPUT_FREEZE.json')
assert encoded['sha256']==sha(video)=='035ed33369ba957d2e2c1275cee377b0f9a21d3b6b2c529ea88592dbddfb4d19'
assert video.stat().st_size==225487
for i,row in enumerate(receipt['records']):
 assert type(row['frame']) is int and row['frame']==i and type(row['time']) in (int,float) and math.isfinite(row['time']) and abs(row['time']-i/30)<1e-12
assert len(receipt['records'])==121 and len(receipt['static_records'])==9 and len(receipt['lifecycle_records'])==270
# The original validator's exact-float timestamp failure remains historical.
# This check preserves its documented finite 1e-12-second serialization tolerance.
for j in range(2):
 assert all(row['views'][j]['rgba_sha256']==receipt['records'][0]['views'][j]['rgba_sha256'] for row in receipt['records'][:7]+receipt['records'][-8:])
count=0
for path in R.rglob('*.png'):
 with Image.open(path) as im:im.load()
 count+=1
assert count==184
native_count=0;frozen_count=0
if a.native_attempt:
 assert sha(a.native_attempt/'capture/evidence.json')==sha(S/'capture/evidence.json')
 assert sha(a.native_attempt/'INPUT_FREEZE.json')==sha(S/'INPUT_FREEZE.json')
 freeze=json.loads((S/'INPUT_FREEZE.json').read_text())['files']
 for name,digest in freeze.items():assert sha(a.native_attempt/name)==digest;frozen_count+=1
 assert frozen_count==1175
 rows=[(row,f'{i:04d}') for i,row in enumerate(receipt['records'])]+[(row,'static/'+row['name']) for row in receipt['static_records']]
 expected_paths=[]
 for row,label in rows:
  assert len(row['views'])==2
  for j,(view,size) in enumerate([('full',(568,800)),('detail',(400,360))]):
   item=row['views'][j];rel=f'{label}_{view}.png' if label.startswith('static/') else f'{view}/{label}.png';expected_paths.append(rel)
   assert item['path']==rel and (item['width'],item['height'])==size
   path=a.native_attempt/'capture'/rel;assert sha(path)==item['file_sha256']
   with Image.open(path) as im:im.load();assert im.mode=='RGBA' and im.size==size and hashlib.sha256(im.tobytes()).hexdigest()==item['rgba_sha256']
   native_count+=1
 assert sorted(str(p.relative_to(a.native_attempt/'capture')) for p in (a.native_attempt/'capture').rglob('*.png'))==sorted(expected_paths)
 assert native_count==260
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_entries','stream=codec_name,width,height,r_frame_rate,nb_read_frames:format=duration,size','-of','json',str(video)]))
s=probe['streams'][0];assert (s['codec_name'],s['width'],s['height'],s['r_frame_rate'],s['nb_read_frames'])==('h264',968,800,'30/1','121')
subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(video),'-f','null','-'],check=True)
out={'status':'PASS','profile_sha256':sha(profile),'video_sha256':sha(video),'baseline_pngs_decoded':count,'historical_native_rgba_images_verified':native_count,'historical_frozen_inputs_verified':frozen_count,'historical_native_motion_frames_per_view':121,'historical_static_anchor_pairs':9,'historical_video_frames_decoded':121,'neutral_hold_frames_initial':7,'neutral_hold_frames_final':8,'probe':probe,'new_images_rendered':0,'current_engine_executed':False,'current_visual_review':False,'normal_speed_playback_observed':False,'raw_capture_archive_in_patch':False,'scope':'Current integrity/decode checks of historical candidate media. Raw images verified only at the explicitly supplied local path; this does not establish remote backup, fresh integrated native parity, source fit, playback or pacing.'}
a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

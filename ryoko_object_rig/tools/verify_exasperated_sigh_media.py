"""Decode existing images/video only. Does not render or launch an editor/engine."""
from pathlib import Path
import argparse,hashlib,json,subprocess
from PIL import Image
R=Path(__file__).resolve().parents[1];V=R/'validation/approved_exasperated_sigh';S=V/'review_sources'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
p=argparse.ArgumentParser();p.add_argument('--native-dir',type=Path);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
profile=R/'expressions/EXP-046.json';video=S/'Exasperated_sigh_rebuild_v1_UNAPPROVED.mp4';receipt=json.loads((S/'native_capture/checks.json').read_text());encoded=json.loads((S/'ENCODE_RESULT.json').read_text())
assert receipt['status']=='PASS' and receipt['failures']==[] and receipt['checks']==68805 and receipt['visual_capture']
assert (receipt['frames'],receipt['fps'],receipt['duration'])==(145,30,4.8)
assert receipt['profile_sha256']==encoded['profile_sha256']==sha(profile)==sha(S/'EXP-046.json')
assert receipt['freeze_sha256']==sha(S/'CANDIDATE_FREEZE.json') and receipt['expected_sha256']==sha(S/'EXPECTED_TRAJECTORY.json')
assert encoded['native_receipt_sha256']==sha(S/'native_capture/checks.json') and encoded['mp4_sha256']==sha(video)
assert [r['frame'] for r in receipt['records']]==list(range(145))
for row in receipt['records']:assert abs(row['time']-row['frame']/30)<1e-10
assert all(r['hashes']==receipt['records'][0]['hashes'] for r in receipt['records'][:10]+receipt['records'][-10:])
expected=json.loads((S/'EXPECTED_TRAJECTORY.json').read_text())['records']
for actual,want in zip(receipt['records'],expected):assert actual['frame']==want['frame'] and all(abs(actual['pose'][k]-want['pose'][k])<1e-7 for k in want['pose'])
for row in receipt['lifecycle_records']:assert row['retrigger_steps']==145 and row['release_steps']==16 and row['reset_checked']
count=0
for path in R.rglob('*.png'):
 with Image.open(path) as im:im.load()
 count+=1
assert count==184
native_count=0
if args.native_dir:
 assert sha(args.native_dir/'checks.json')==sha(S/'native_capture/checks.json')
 for j,(view,size) in enumerate([('full',(568,800)),('detail',(400,360))]):
  assert {p.name for p in (args.native_dir/view).iterdir()}=={f'{i:04d}.png' for i in range(145)}
  pairs=[(args.native_dir/view/f'{row["frame"]:04d}.png',row['hashes'][j]) for row in receipt['records']]
  pairs += [(args.native_dir/'static'/f'{row["name"]}_{view}.png',row['hashes'][j]) for row in receipt['static_records']]
  for path,digest in pairs:
   with Image.open(path) as im:assert im.mode=='RGBA' and im.size==size and hashlib.sha256(im.tobytes()).hexdigest()==digest
   native_count+=1
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_entries','stream=codec_name,width,height,r_frame_rate,nb_read_frames:format=duration,size','-of','json',str(video)]))
s=probe['streams'][0];assert (s['codec_name'],s['width'],s['height'],s['r_frame_rate'],s['nb_read_frames'])==('h264',968,800,'30/1','145')
subprocess.run(['ffmpeg','-v','error','-i',str(video),'-f','null','-'],check=True)
out={'status':'PASS','profile_sha256':sha(profile),'video_sha256':sha(video),'baseline_pngs_decoded':count,'historical_native_rgba_images_verified':native_count,'historical_native_motion_frames_per_view':145,'historical_static_anchor_pairs':10,'historical_video_frames_decoded':145,'neutral_hold_frames_per_endpoint':10,'probe':probe,'new_images_rendered':0,'current_engine_executed':False,'current_visual_review':False,'normal_speed_playback_observed':False,'scope':'Existing historical capture identity/RGBA verification and media decode only. No fresh integrated engine/native run, perceptual review, or playback observation.'}
args.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

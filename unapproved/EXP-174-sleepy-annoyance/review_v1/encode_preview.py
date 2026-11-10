"""Encode only previously captured native frames; never starts a renderer."""
import json,subprocess
from pathlib import Path
w=Path(__file__).resolve().parent
if not (w/'motion_checks.json').exists():raise SystemExit('Native capture has not completed; run the native capture separately first.')
r=json.loads((w/'motion_checks.json').read_text());assert r['status']=='PASS',r['failures']
assert r['visual_capture'] is True and r['frames']==121 and r['baseline_profile_count']==json.loads((w/'BASELINE_FREEZE.json').read_text())['baseline_profile_count']
for view in ['full','detail']:
 assert {p.name for p in (w/'motion'/view).glob('*.png')}=={f'{i:04d}.png' for i in range(121)}
f='[1:v]pad=400:800:0:220:color=0x202224,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text=Sleepy annoyance:fontcolor=white:fontsize=22:x=(w-tw)/2:y=135,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text=Review candidate:fontcolor=0xbfc4ca:fontsize=16:x=(w-tw)/2:y=170[d];[0:v][d]hstack=inputs=2[v]'
cmd=['ffmpeg','-hide_banner','-nostdin','-n','-framerate','30','-i',str(w/'motion/full/%04d.png'),'-framerate','30','-i',str(w/'motion/detail/%04d.png'),'-filter_complex',f,'-map','[v]','-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart',str(w/'Sleepy_annoyance_review_v1.mp4')]
with (w/'encode.log').open('w') as log:subprocess.run(cmd,check=True,stdout=log,stderr=subprocess.STDOUT)
probe=subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_name,width,height,pix_fmt,r_frame_rate,nb_frames:format=duration,size','-of','json',str(w/'Sleepy_annoyance_review_v1.mp4')]);(w/'video_probe.json').write_bytes(probe)
subprocess.run(['ffmpeg','-v','error','-i',str(w/'Sleepy_annoyance_review_v1.mp4'),'-f','null','-'],check=True)
print(probe.decode())

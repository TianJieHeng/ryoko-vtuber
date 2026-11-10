import json,subprocess,time
from pathlib import Path
w=Path(__file__).resolve().parent
for _ in range(600):
 if (w/'motion_checks.json').exists():break
 time.sleep(1)
else:raise SystemExit('Native capture did not finish')
r=json.loads((w/'motion_checks.json').read_text());assert r['status']=='PASS',r['failures']
for view in ['full','detail']:assert len(list((w/'motion'/view).glob('*.png')))==187
f='[1:v]pad=400:800:0:220:color=0x202224,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text=Recovering composure:fontcolor=white:fontsize=22:x=(w-tw)/2:y=135,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text=Review candidate:fontcolor=0xbfc4ca:fontsize=16:x=(w-tw)/2:y=170[d];[0:v][d]hstack=inputs=2[v]'
cmd=['ffmpeg','-hide_banner','-nostdin','-n','-framerate','30','-i',str(w/'motion/full/%04d.png'),'-framerate','30','-i',str(w/'motion/detail/%04d.png'),'-filter_complex',f,'-map','[v]','-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart',str(w/'Recovering_Composure_review_v1.mp4')]
with (w/'encode.log').open('w') as log:subprocess.run(cmd,check=True,stdout=log,stderr=subprocess.STDOUT)
probe=subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_name,width,height,pix_fmt,r_frame_rate,nb_frames:format=duration,size','-of','json',str(w/'Recovering_Composure_review_v1.mp4')]);(w/'video_probe.json').write_bytes(probe)
subprocess.run(['ffmpeg','-v','error','-i',str(w/'Recovering_Composure_review_v1.mp4'),'-f','null','-'],check=True)
print(probe.decode())

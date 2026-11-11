#!/usr/bin/env python3
"""CPU cutout preview using actual Godot matrices; NOT a native Godot capture.
The head is an approved neutral source composite, not live shader output.
Run sample_wiring.gd before this. No external service or generated artwork.
"""
import json, math, subprocess, argparse
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'full_body'; OUT=BASE/'review'
manifest=json.loads((BASE/'registration.json').read_text())
samples=json.loads((OUT/'transform_samples.json').read_text())
assets={e['id']:Image.open(ROOT/e['file'][6:]).convert('RGBA') for e in manifest['layers']}
head=Image.open(BASE/'pieces_v2/head_audit/neutral_head_complete.png').convert('RGBA')
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',21)
small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)

def place(canvas,source,values):
 a,b,c,d,x,y=values
 corners=np.array([[0,0,1],[source.width,0,1],[0,source.height,1],[source.width,source.height,1]]).T
 m=np.array([[a,c,x],[b,d,y],[0,0,1]],dtype=float)
 pts=m@corners;left=math.floor(pts[0].min())-1;top=math.floor(pts[1].min())-1
 right=math.ceil(pts[0].max())+1;bottom=math.ceil(pts[1].max())+1
 inv=np.linalg.inv(m)@np.array([[1,0,left],[0,1,top],[0,0,1]])
 part=source.transform((right-left,bottom-top),Image.Transform.AFFINE,tuple(inv[:2].flatten()),Image.Resampling.BICUBIC)
 canvas.alpha_composite(part,(left,top))

movie=OUT/'ryoko_full_body_wiring_v1.mp4'
cmd=['ffmpeg','-hide_banner','-loglevel','warning','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1280x960','-r',str(samples['fps']),'-i','-','-an','-c:v','libx264','-preset','medium','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(movie)]
parser=argparse.ArgumentParser();parser.add_argument('--still-frame',type=int);args=parser.parse_args()
process=None if args.still_frame is not None else subprocess.Popen(cmd,stdin=subprocess.PIPE)
for i,frame in enumerate(samples['frames']):
 if args.still_frame is not None and i!=args.still_frame:continue
 canvas=Image.new('RGBA',tuple(manifest['canvas']),(237,235,229,255))
 for e in sorted(manifest['layers'],key=lambda e:e['z']):place(canvas,assets[e['id']],frame['layers'][e['id']])
 place(canvas,head,frame['head'])
 result=Image.new('RGB',(1280,960),(25,31,37));result.paste(canvas.convert('RGB').resize((568,852),Image.Resampling.LANCZOS),(24,76))
 # The bust is a crop from the very same composited full-body frame.
 result.paste(canvas.convert('RGB').crop((290,35,740,665)).resize((594,832),Image.Resampling.LANCZOS),(654,96))
 d=ImageDraw.Draw(result)
 d.text((24,14),'Ryoko / individual part assembly / UNAPPROVED',font=font,fill=(242,241,233))
 d.text((24,43),frame['phase'],font=small,fill=(132,224,203))
 d.text((654,76),'Same frame / bust detail',font=small,fill=(242,241,233))
 d.text((24,935),'CPU layer composite from Godot joint transforms. Neutral head source, not native-rendered facial controls.',font=small,fill=(216,218,220))
 if process is None:
  result.save(OUT/f'endpoint_review_{i:04}.jpg',quality=95);print(OUT/f'endpoint_review_{i:04}.jpg');break
 process.stdin.write(result.tobytes())
 if i in (0,60,90,150,180,210,270,300,330,390,420,450):
  result.save(OUT/f'preview_frame_{i:04}.jpg',quality=92)
 if i%60==0:print(f'{i}/{len(samples["frames"])}',flush=True)
if process is not None:
 process.stdin.close();code=process.wait()
 if code:raise SystemExit(code)
 print(movie)

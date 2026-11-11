"""CPU source-layer head-tilt seam diagnostic, not a Godot render."""
from PIL import Image,ImageDraw
from pathlib import Path
import json
r=Path(__file__).resolve().parents[2];j=json.loads((r/'full_body/registration.json').read_text());base=Image.new('RGBA',tuple(j['canvas']))
for e in sorted(j['layers'],key=lambda e:e['z']):
 im=Image.open(r/e['file'].replace('res://',''));im=im.resize(tuple(round(n*s) for n,s in zip(im.size,e['scale'])),Image.Resampling.LANCZOS);base.alpha_composite(im,tuple(round(v) for v in e['position']))
h=Image.open(r/'full_body/assets/neutral_head.png');h=h.resize((round(h.width*j['head_binding']['scale']),round(h.height*j['head_binding']['scale'])),Image.Resampling.LANCZOS);plane=Image.new('RGBA',base.size);plane.alpha_composite(h,tuple(j['head_binding']['position']));review=Image.new('RGB',(1050,620))
for i,a in enumerate([-3,0,3]):
 bg=Image.new('RGBA',base.size,(230,40,160,255));bg.alpha_composite(base);bg.alpha_composite(plane.rotate(a,Image.Resampling.BICUBIC,center=(510,234)));c=bg.crop((430,190,590,310)).resize((350,525));review.paste(c,(i*350,60));ImageDraw.Draw(review).text((i*350+20,20),f'CPU diagnostic head tilt {a} deg',fill='white')
review.save(r/'full_body/assets/head_tilt_seams_cpu.png')

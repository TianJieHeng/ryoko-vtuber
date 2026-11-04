from PIL import Image,ImageDraw,ImageFilter,ImageChops
import numpy as np
from pathlib import Path
import json
out=Path(__file__).resolve().parents[1]; p=out/'sources';art=out/'artwork'
a=Image.open(p/'neutral_restoration_candidate.png').convert('RGBA'); b=Image.open(p/'blink_blank_source.png').convert('RGBA')
# Normalize near-opaque generated alpha to prevent stacked facial tiles changing opacity.
for im in [a,b]: im.putalpha(im.getchannel('A').point(lambda v: 255 if v >= 240 else v))
a.save(art/'approved_neutral.png')
def mask(size,box,blur=7):
 m=Image.new('L',size);ImageDraw.Draw(m).ellipse(box,fill=255);return m.filter(ImageFilter.GaussianBlur(blur))
# Generated skin and blink artwork are cropped and registered, never repainted.
mb=(480,590,650,700); mm=mask(a.size,(505,610,623,674),7)
clip=Image.new("L",a.size);clip.paste(mm.crop(mb),mb[:2]);mm=clip
base=Image.composite(b,a,mm);base.save(art/'bust_base.png')
neutral=a.crop(mb);neutral.save(art/'mouth_neutral.png')
entries={'neutral':{'file':'mouth_neutral.png','xy':list(mb[:2])}}
for n in ['A','E','I','O','U']:
 im=Image.open(p/'source_mouths'/('mouth_'+n+'.png')).convert('RGBA')
 im=im.resize((round(im.width*1.45),round(im.height*1.45)),Image.Resampling.LANCZOS)
 im.save(art/('mouth_'+n+'.png'));entries[n]={'file':'mouth_'+n+'.png','xy':[round(564-im.width/2),622]}
# Blinks: independent left/right local replacement tiles, softly blended on skin.
blinks={}
for name,box in [('R',(395,450,550,552)),('L',(585,450,737,552))]:
 shifted=Image.new('RGBA',a.size);shifted.paste(b,(0,0))
 # Full-opacity center replaces both iris and eyelash; feather on skin boundaries.
 m=Image.new('L',a.size);d=ImageDraw.Draw(m);d.rounded_rectangle((box[0]+7,box[1]+10,box[2]-7,box[3]-7),radius=9,fill=255);m=m.filter(ImageFilter.GaussianBlur(2))
 im=shifted.crop(box);im.putalpha(m.crop(box));im.save(art/('blink_'+name+'.png'));blinks[name]={'file':'blink_'+name+'.png','xy':list(box[:2])}
manifest={'size':list(a.size),'mouths':entries,'blinks':blinks,'note':'Local facial-control preview. Flat bust base; independent mouth and eyelid sprites. No head/body deformation yet.'}
(out/'registration.json').write_text(json.dumps(manifest,indent=2))
def composite(mouth='neutral',blink=()):
 im=base.copy()
 for name in blink:
  e=blinks[name];im.alpha_composite(Image.open(art/e['file']),tuple(e['xy']))
 e=entries[mouth];im.alpha_composite(Image.open(art/e['file']),tuple(e['xy']))
 return im
for n in entries:
 im=composite(n);im.save(out/'previews'/('mouth_'+n+'.png'))
for n in [('L',),('R',),('L','R')]:composite(blink=n).save(out/'previews'/('blink_'+''.join(n)+'.png'))
# Contact sheet face crops, deterministic composites of actual registered sprites.
names=['mouth_neutral','blink_L','blink_R','blink_LR','mouth_A','mouth_E','mouth_I','mouth_O','mouth_U']
c=Image.new('RGB',(1800,1680),'#c9cdd1');d=ImageDraw.Draw(c)
from PIL import ImageFont
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',24)
for i,n in enumerate(names):
 im=Image.open(out/'previews'/(n+'.png')).crop((335,365,795,785));im=im.resize((552,504));x=(i%3)*600+24;y=(i//3)*560+44;c.paste(im,(x,y),im);d.text((x,y-34),n,font=f,fill='black')
c.save(out/'previews'/'facial_states_contact.jpg',quality=95)

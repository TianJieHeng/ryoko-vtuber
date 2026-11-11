#!/usr/bin/env python3
"""Assemble raw individual trouser/pump pieces only; never read full-body artwork."""
from pathlib import Path
from PIL import Image
import numpy as np
import json,hashlib
HERE=Path(__file__).resolve().parent;RIG=HERE.parents[2];REPO=RIG.parent
SRC=REPO/'avatar_build_assets/body/layers';layers=[]
def read(n):
 p=SRC/(n+'.png');im=Image.open(p).convert('RGBA');a=np.array(im);a[a[:,:,3]<32,3]=0;im=Image.fromarray(a);crop=im.getbbox();return im.crop(crop),list(crop),hashlib.sha256(p.read_bytes()).hexdigest()
def save(id,im,raw,crop,scale,xy,parent,pivot,z,overlap='',derivation='alpha<32 removed; crop to remaining foreground'):
 im.save(HERE/(id+'.png'));layers.append(dict(id=id,file='res://full_body/pieces_v2/lower/'+id+'.png',rawsource='avatar_build_assets/body/layers/'+raw+'.png',rawsource_sha256=hashlib.sha256((SRC/(raw+'.png')).read_bytes()).hexdigest(),raw_crop_xyxy=crop,scale=[scale,scale],position=list(xy),parent=parent,pivot=list(pivot),z=z,alpha_bounds=list(im.getbbox()),derivation=derivation,boundary_overlap=overlap))
for side,x in [('R',379),('L',525)]:
 raw='trousers_leg_front_character_'+side;im,crop,sha=read(raw);scale=660/im.height;y=685;knee=1010;cut=round((knee-y)/scale);overlap=round(14/scale)
 # Near-white external matte is not trouser pigment. Remove only outer boundary pixels.
 from PIL import ImageFilter
 a=np.array(im);rgb=a[:,:,:3].astype(int);edge=np.array(im.getchannel('A').filter(ImageFilter.MinFilter(5)))<128;white=(rgb.min(2)>125)&((rgb.max(2)-rgb.min(2))<65);a[edge&white,3]=0;im=Image.fromarray(a)
 for kind,start,end,z in [('thigh',0,cut+overlap,-30),('shin',cut-overlap,im.height,-31)]:
  part=im.crop((0,start,im.width,end));parent=('hip_' if kind=='thigh' else 'knee_')+side;pivot=[440 if side=='R' else 584,690] if kind=='thigh' else [434 if side=='R' else 590,1010]
  save(kind+'_'+side,part,raw,crop,scale,[x,y+start*scale],parent,pivot,z,'28 canvas px shared real source pixels at knee, bounded tiny motion',f'Alpha fringe cleanup; source cropped local y[{start},{end}) from foreground crop; no anisotropic resize')
 # Shoe center follows actual lower-trouser alpha center, not padded source bounds.
 a=np.array(im)[:,:,3];yy,xx=np.where(a[-100:]>128);ankle=x+(float(xx.min()+xx.max())/2)*scale
 rawshoe='pump_front_character_'+side;shoe,scrop,_=read(rawshoe);ss=140/shoe.height;shoe_y=1320
 save('shoe_'+side,shoe,rawshoe,scrop,ss,[ankle-shoe.width*ss/2,shoe_y],'ankle_'+side,[ankle,1334],-40,'Trouser hem overlaps real shoe opening by 25px; no added ankle artwork')
raw='trousers_pelvis_front';im,crop,sha=read(raw);s=.65;x=512-im.width*s/2;y=580
# Fade only the construction shorts hem into the real leg source below it.
a=np.array(im);global_y=y+np.arange(im.height)*s;fade=np.clip((790-global_y)/45,0,1);a[:,:,3]=(a[:,:,3]*fade[:,None]).astype('uint8');im=Image.fromarray(a)
save('pelvis',im,raw,crop,s,[x,y],'pelvis',[512,650],-20,'Leg tops start685; pelvis overlaps through790, hem fades745..790','Alpha<32 removed; uniform scale; construction lower hem alpha feather only, no paint')
# Independent raw belt accessory, anchored to actual gold buckle rather than padding.
belt_rel='avatar_build_assets/accessories/layers/RYO_ACC_belt_gold_buckle.png';bp=REPO/belt_rel
belt=Image.open(bp).convert('RGBA');ba=np.array(belt);ba[ba[:,:,3]<32,3]=0;belt=Image.fromarray(ba);bcrop=list(belt.getbbox());belt=belt.crop(tuple(bcrop));ba=np.array(belt);rgb=ba[:,:,:3].astype(int)
gold=(rgb[:,:,0]>rgb[:,:,1]+12)&(rgb[:,:,1]>rgb[:,:,2]+18)&(rgb[:,:,0]>120)&(ba[:,:,3]>128)
gy,gx=np.where(gold);gold_center=[(float(gx.min())+float(gx.max()))/2,(float(gy.min())+float(gy.max()))/2]
bs=265/belt.width;bxy=[512-gold_center[0]*bs,614-gold_center[1]*bs]
belt.save(HERE/'belt.png')
layers.append(dict(id='belt',file='res://full_body/pieces_v2/lower/belt.png',rawsource=belt_rel,rawsource_sha256=hashlib.sha256(bp.read_bytes()).hexdigest(),raw_crop_xyxy=bcrop,scale=[bs,bs],position=bxy,parent='pelvis',pivot=[512,614],z=-19,alpha_bounds=list(belt.getbbox()),gold_buckle_center_crop=gold_center,derivation='Alpha<32 removed; foreground crop; uniform scale to265px; actual gold buckle centered at [512,614]',boundary_overlap='Pelvis-mounted accessory; blouse/blazer integration may occlude belt sides, not buckle.'))
manifest=dict(canvas=[1024,1536],side_convention='L anatomical / screen-right; R anatomical / screen-left',layers=layers,source_policy='Only five raw individual body/layers PNGs plus individual raw gold-buckle belt; no canonical fullbody artwork or old registered artwork.',limitations=['Construction pelvis/leg shading differs; neutral assembly is for registration review, not approved final artwork.','No hidden anatomy generated; only cropped source overlap.','Knee and ankle pivots need integration against upper-body registration.'])
(HERE/'registration_fragment.json').write_text(json.dumps(manifest,indent=2)+'\n')
neutral=Image.new('RGBA',(1024,1536))
for e in sorted(layers,key=lambda e:e['z']):
 im=Image.open(HERE/(e['id']+'.png'));im=im.resize(tuple(round(n*s) for n,s in zip(im.size,e['scale'])),Image.Resampling.LANCZOS);neutral.alpha_composite(im,tuple(round(v) for v in e['position']))
neutral.save(HERE/'neutral_lower.png')
for n,c in [('light',(238,235,227,255)),('dark',(24,29,34,255))]:
 bg=Image.new('RGBA',neutral.size,c);bg.alpha_composite(neutral);bg.convert('RGB').save(HERE/('neutral_lower_'+n+'.png'))
print(HERE)

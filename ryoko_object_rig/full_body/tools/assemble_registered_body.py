#!/usr/bin/env python3
"""Reproducible, non-generative registration of retained Ryoko body artwork.
Original approved files are read-only. PIL only crops, masks and resamples pixels.
Run from anywhere: python ryoko_object_rig/full_body/tools/assemble_registered_body.py
"""
from pathlib import Path
import json, hashlib
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
ROOT=Path(__file__).resolve().parents[2]; REPO=ROOT.parent
OUT=ROOT/'full_body'; ASSET=OUT/'assets'; ASSET.mkdir(parents=True,exist_ok=True)
OLD=REPO/'ryoko_2d_update'; entries={e['name']:e for e in json.loads((OLD/'manifest/placement_manifest.json').read_text())['layers']}
canvas=(1024,1536); joints=[]; layers=[]
# Trace the actual empty torso/arm gap independently on each side; the source
# is not perfectly symmetric, so a mirrored polygon can cut into the jacket.
source_rel='avatar_build_assets/reference_library/assets/modeling/RYO_MOD_fullbody_front_v001.png'
source_rgb=np.array(Image.open(REPO/source_rel).convert('RGB')).astype(int)
separators={}
for side in ['L','R']:
 values=[]
 for y in range(1536):
  expect=float(np.interp(y,[280,350,400,450,500,550,600,650,700,739],[632,629,619,610,605,605,630,645,655,655]))
  if side=='R':expect=1024-expect
  if 450<=y<=739:
   lo,hi=max(0,int(expect)-40),min(1024,int(expect)+41);row=source_rgb[y,lo:hi];white=(row.min(1)>175)&((row.max(1)-row.min(1))<55)
   runs=[];start=None
   for ix,on in enumerate(list(white)+[False]):
    if on and start is None:start=ix
    if not on and start is not None:
     if ix-start>=2:runs.append((lo+(start+ix-1)/2,ix-start))
     start=None
   if runs:expect=min(runs,key=lambda v:abs(v[0]-expect))[0]
  values.append(expect)
 # Smooth the shoulder-to-empty-gap transition to avoid a horizontal cut step.
 from scipy.ndimage import gaussian_filter1d
 separators[side]=gaussian_filter1d(np.array(values),3.0)

def joint(id,parent,xy,control=None,limit=0):
 joints.append(dict(id=id,parent=parent,position=list(xy),control=(control or id) if limit else '',range_degrees=[-limit,limit]))
joint('pelvis','',[512,650],'pelvis_tilt',1)
joint('spine','pelvis',[512,540],'spine_tilt',1.5)
joint('chest','spine',[512,360],'chest_tilt',1)
joint('neck','chest',[512,246],'neck_tilt',0)
joint('head','neck',[510,234],'head_tilt',3)
for side in ['R','L']:
 s=side=='R'
 joint('shoulder_'+side,'chest',[372 if s else 652,302],'shoulder_'+side,2)
 joint('elbow_'+side,'shoulder_'+side,[374 if s else 650,535],'elbow_'+side,2)
 joint('wrist_'+side,'elbow_'+side,[315 if s else 709,724],'wrist_'+side,3)
 joint('hip_'+side,'pelvis',[440 if s else 584,690],'hip_'+side,.7)
 joint('knee_'+side,'hip_'+side,[434 if s else 590,1010],'knee_'+side,1)
 joint('ankle_'+side,'knee_'+side,[427 if s else 599,1334],'ankle_'+side,1)
def save(id,im,xy,parent,z,source,notes='',scale=(1,1)):
 im.save(ASSET/(id+'.png'))
 layers.append(dict(id=id,file='res://full_body/assets/'+id+'.png',parent=parent,position=list(xy),scale=list(scale),z=z-50,size=list(im.size),alpha_bounds=list(im.getchannel('A').getbbox()),source=source,sha256=hashlib.sha256((ASSET/(id+'.png')).read_bytes()).hexdigest(),notes=notes))
def retained(name,parent,z):
 e=entries[name]; im=Image.open(OLD/e['registered_png']).convert('RGBA'); xy=[v/2 for v in e['master_xy']]
 if name=='torso_garment':
  yy=np.clip((xy[1]+np.arange(im.height)/2).astype(int),0,1535);xx=xy[0]+np.arange(im.width)/2
  overlap=(6*np.clip((480-yy)/30,0,1))[:,None]
  keep=(xx[None,:]<=separators['L'][yy,None]+overlap)&(xx[None,:]>=separators['R'][yy,None]-overlap)
  aa=np.array(im);aa[:,:,3]=np.where(keep,aa[:,:,3],0);im=Image.fromarray(aa)
 if name.startswith('hand_'):
  a=np.array(im); rgb=a[:,:,:3].astype(int); alpha=im.getchannel('A'); inner=np.array(alpha.filter(ImageFilter.MinFilter(7))); edge=(a[:,:,3]>0)&(inner<128)
  # Remove only near-white exterior matte below cuff. Preserve warm skin and cuff.
  white=(rgb.min(2)>200)&((rgb.max(2)-rgb.min(2))<45); below=np.arange(im.height)[:,None]>45
  a[edge&white&below,3]=0;im=Image.fromarray(a)
 save(name,im,xy,parent,z,'ryoko_2d_update/'+e['registered_png'],'Retained registered canonical source cut; 2x source sampled at 0.5.',(.5,.5))
for side in ['R','L']:
 retained('shoe_'+side,'ankle_'+side,10)
 e=entries['leg_'+side]; im=Image.open(OLD/e['registered_png']).convert('RGBA'); x,y=[v/2 for v in e['master_xy']]
 # Knee overlap is duplicated real trouser pixels, never generated anatomy.
 cut=round((1010-y)*2); overlap=28
 save('thigh_'+side,im.crop((0,0,im.width,cut+overlap)),[x,y],'hip_'+side,20,'ryoko_2d_update/'+e['registered_png'],'56 source-pixel / 28 canvas-pixel knee overlap; bounded one-degree knee flexion.',(.5,.5))
 save('shin_'+side,im.crop((0,cut-overlap,im.width,im.height)),[x,y+(cut-overlap)/2],'knee_'+side,19,'ryoko_2d_update/'+e['registered_png'],'Same painted pixels overlap thigh by 56 source pixels / 28 canvas pixels; no hidden anatomy painted.',(.5,.5))
retained('canonical_pelvis','pelvis',25)
# Retained standalone canonical neck provides actual under-chin coverage from y216.
retained('neck','neck',30)
# Actual canonical collar/chest pixels underlap small holes in legacy garment mask.
collar_source=REPO/'avatar_build_assets/reference_library/assets/modeling/RYO_MOD_fullbody_front_v001.png'
collar=Image.open(collar_source).convert('RGBA').crop((460,250,566,395))
cm=Image.new('L',collar.size);ImageDraw.Draw(cm).polygon([(20,0),(84,0),(96,20),(106,50),(106,145),(0,145),(0,20),(10,10)],fill=255);collar.putalpha(cm)
save('collar_underlap',collar,[460,250],'neck',29,'avatar_build_assets/reference_library/assets/modeling/RYO_MOD_fullbody_front_v001.png','Unpainted interior collar/chest source crop behind garment and approved visible neck; closes inherited cut-mask holes.')
retained('torso_garment','chest',40)
# Re-cut each complete sleeve from the original frontal master. The retained
# forearm masks were incomplete and depended on torso-owned ghost sleeve pixels.
from scipy import ndimage
master=Image.open(collar_source).convert('RGBA'); a=np.array(master); rgb=a[:,:,:3].astype(int)
white=(rgb.min(2)>215)&((rgb.max(2)-rgb.min(2))<42); labels,_=ndimage.label(white)
border=np.unique(np.concatenate([labels[0],labels[-1],labels[:,0],labels[:,-1]]));a[np.isin(labels,border[border>0]),3]=0;master=Image.fromarray(a)
arm_inner=[(632,280),(629,340),(619,400),(604,450),(606,470),(611,490),(615,520),(615,550),(623,580),(631,610),(641,650),(648,680),(658,715),(660,739)]
arm_poly=arm_inner+[(740,739),(740,280)]
for side in ['R','L']:
 xx=np.arange(master.width)[None,:];yy=np.arange(master.height)[:,None];margin=6*np.clip((480-yy)/30,0,1);keep=(xx>=separators[side][:,None]-margin) if side=='L' else (xx<=separators[side][:,None]+margin);keep=keep&(yy>=280)&(yy<739)
 mask=Image.fromarray(np.where(keep,255,0).astype('uint8'))
 arm=master.copy();arm.putalpha(Image.fromarray(np.minimum(np.array(arm.getchannel('A')),np.array(mask))))
 aa=np.array(arm);rgb=aa[:,:,:3].astype(int);matte=(rgb.min(2)>175)&((rgb.max(2)-rgb.min(2))<55)&(np.arange(arm.height)[:,None]<710);aa[matte,3]=0;arm=Image.fromarray(aa)
 # Remove only neutral pale edge residue in the armpit source-background fringe.
 edge=(aa[:,:,3]>0)&(np.array(arm.getchannel('A').filter(ImageFilter.MinFilter(3)))<128)
 armpit=(np.arange(arm.height)[:,None]>=430)&(np.arange(arm.height)[:,None]<=480)
 fringe=edge&armpit&(rgb.min(2)>110)&((rgb.max(2)-rgb.min(2))<55);aa[fringe,3]=0;arm=Image.fromarray(aa)
 # Full artwork overlap 40px at actual source elbow (y535), rather than a gap.
 x0,x1=(600,740) if side=='L' else (284,424)
 for part,y0,y1,parent,z in [('upper_arm',280,555,'shoulder_',45),('forearm',515,739,'elbow_',44)]:
  piece=arm.crop((x0,y0,x1,y1))
  if part=='upper_arm':
   aa=np.array(piece);ramp=np.clip((555-(y0+np.arange(piece.height)))/25,0,1);aa[:,:,3]=(aa[:,:,3]*ramp[:,None]).astype('uint8');piece=Image.fromarray(aa)
  save(part+'_'+side,piece,[x0,y0],parent+side,z,'avatar_build_assets/reference_library/assets/modeling/RYO_MOD_fullbody_front_v001.png','Canonical sleeve-only cut, 40px elbow overlap. Exclusive arm ownership; no torso sleeve ghost.')
 retained('hand_'+side,'wrist_'+side,43)
# The approved neck/chest owns its original necklace. Mask at the existing garment opening.
fixed=Image.open(ROOT/'rig_assets/object_face/fixed_neck_torso.png').convert('RGBA')
# Map canonical garment opening into source coordinates with the exact head binding.
origin=(350,29); scale=.285
poly=[(478,234),(546,234),(546,240),(557,247),(555,261),(548,270),(550,291),(555,315),(548,330),(536,345),(526,360),(518,380),(511,389),(504,380),(497,360),(488,345),(476,330),(469,315),(474,290),(476,267),(468,260),(468,244)]
mask=Image.new('L',fixed.size); ImageDraw.Draw(mask).polygon([((x-origin[0])/scale,(y-origin[1])/scale) for x,y in poly],fill=255)
import numpy as np
fixed.putalpha(Image.fromarray(np.minimum(np.array(fixed.getchannel('A')),np.array(mask))))
b=fixed.getbbox(); fixed=fixed.crop(b)
save('approved_neck_chest',fixed,[origin[0]+b[0]*scale,origin[1]+b[1]*scale],'neck',41,'ryoko_object_rig/rig_assets/object_face/fixed_neck_torso.png','Only visible skin/necklace through existing blouse opening. No sleeves or replacement head.',(scale,scale))
# Match canonical full-body crown/chin and hair-width proportions, pivoting at the existing chin.
head_origin=(329,4); head_scale=.32
manifest=dict(version=2,canvas=list(canvas),side_convention='Anatomical L is screen-right; anatomical R is screen-left.',joints=joints,layers=layers,head_binding=dict(parent='head',position=list(head_origin),scale=head_scale,source_size=[1136,1384],hide_legacy=['FixedNeckTorso'],keep_objects=['stationary_backing','all existing dynamic head objects']),limitations=['Frontal-only bounded seam test, not a certified tracking/export rig.','Independent neck tilt is unsupported; neck follows chest and head tilt is bounded separately.','Retained source cuts supply existing overlap only; no invented occluded anatomy.','Knee, elbow and shoulder overlaps permit small local motion only. Larger motions require approved completion artwork.','Neck skin is a retained canonical underlap plus approved fixed-neck visible cut; no stretched chin or blouse.'])
(OUT/'registration.json').write_text(json.dumps(manifest,indent=2)+'\n')
# Neutral visual proof uses canonical source head only as a diagnostic stand-in for live objects.
im=Image.new('RGBA',canvas)
for e in sorted(layers,key=lambda e:e['z']):
 p=Image.open(ASSET/(e['id']+'.png')); p=p.resize(tuple(round(n*s) for n,s in zip(p.size,e['scale'])),Image.Resampling.LANCZOS); im.alpha_composite(p,tuple(round(v) for v in e['position']))
head=Image.open(ROOT/'canonical_sources/approved_neutral.png').convert('RGBA');
# Preserve actual hair tips below the neck split, rather than truncating the silhouette.
head.putalpha(Image.fromarray(np.where(np.arange(1384)[:,None]<720,np.array(head.getchannel('A')),0).astype('uint8')))
hm=json.loads((ROOT/'rig_assets/object_face/manifest.json').read_text())
for key,e in sorted(hm['objects'].items(),key=lambda item:item[1]['z']):
 if key.startswith('hair_') and 'hidden' not in key:
  part=Image.open(ROOT/'rig_assets/object_face'/e['file']).convert('RGBA');head.alpha_composite(part,tuple(e['xy']))
head.save(ASSET/'neutral_head.png')
head=head.resize((round(1136*head_scale),round(1384*head_scale)),Image.Resampling.LANCZOS);im.alpha_composite(head,head_origin)
im.save(ASSET/'neutral_composite.png')
for name,color in [('light',(242,239,232,255)),('dark',(24,29,34,255))]:
 bg=Image.new('RGBA',canvas,color);bg.alpha_composite(im);bg.convert('RGB').save(ASSET/('neutral_'+name+'.png'))
print(f'{len(joints)} joints; {len(layers)} layers; {OUT}/registration.json')

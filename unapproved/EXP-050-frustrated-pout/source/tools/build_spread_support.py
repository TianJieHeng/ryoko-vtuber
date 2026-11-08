#!/usr/bin/env python3
"""Deterministic fixed-UV oral support for rigid lateral lip articulation.
All source artwork remains byte-identical. New anatomical registration/mattes
are estimates, never recovered clean originals. This builds independent cavity,
posterior-enamel and lower-oral-surface owners, not a whole-mouth replacement.
"""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
P=Path(__file__).resolve().parents[1];O=P/'rig_assets/spread_support';O.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
M={'version':1,'status':'INTERNAL_CANDIDATE_NOT_USER_APPROVED','control':{'name':'mouth_spread','range':[0,1],'effective':'mouth_spread * mouth_smile','half_width_increment_px':20,'additional_corner_lift_px':5,'vertical_aperture_cap':.55,'maximum_per_column_aperture_px':30.8},'sources':{},'objects':{},'inference':[]}
def source(name):
 p=P/'assembly_sources/head'/name;M['sources'][str(p.relative_to(P))]=sha(p);return Image.open(p).convert('RGBA')
def save(name,im,source_name,crop,xy,kind,notes):
 im.save(O/(name+'.png'));mask=im.getchannel('A').point(lambda a:255 if a else 0);mask.save(O/(name+'_observed_support.png'))
 M['objects'][name]={'file':name+'.png','observed_mask':name+'_observed_support.png','xy':xy,'size':list(im.size),'source':source_name,'source_crop_xyxy':crop,'kind':kind,'pigment':'SOURCE_DERIVED_OBSERVED_ANATOMICAL_PIGMENT','registration':'INFERRED_CANONICAL_REGISTRATION_AND_HIDDEN_UNDERLAP','notes':notes,'sha256':sha(O/(name+'.png'))}
a=source('RYO_HEAD_mouth_cavity_v001.png')
for side,box,xy in [('left',(230,120,254,196),(501,620)),('right',(355,120,379,196),(605,620)),('top',(265,136,345,146),(525,619))]:
 save('cavity_'+side,a.crop(box),'assembly_sources/head/RYO_HEAD_mouth_cavity_v001.png',list(box),list(xy),'cavity_underlap','Native source crop, no color invention or runtime resampling. Registration and newly exposed cavity continuation are inferred. Central established cavity remains unchanged.')
a=source('RYO_HEAD_viseme_E_v001.png');mask=Image.new('L',a.size);d=ImageDraw.Draw(mask)
poly=[(264,159),(281,152),(309,150),(346,151),(377,149),(414,146),(447,147),(469,152),(479,158),(460,164),(428,168),(395,171),(361,172),(323,170),(290,166)]
d.polygon(poly,fill=255);mask=mask.filter(ImageFilter.GaussianBlur(.65));mask.save(O/'posterior_enamel_source_matte.png')
x=np.array(a);x[:,:,3]=np.minimum(x[:,:,3],np.array(mask));luma=x[:,:,:3]@np.array([.2126,.7152,.0722]);x[:,:,:3]=np.rint(np.clip(135+.5*luma,0,255))[:,:,None].astype('uint8')
b=Image.fromarray(x).crop((260,140,484,180)).resize((112,20),Image.Resampling.LANCZOS)
for side,box,xy in [('left',(0,0,37,20),(536,609)),('right',(75,0,112,20),(557,609))]:
 part=b.crop(box);padded=Image.new('RGBA',(part.width+8,part.height+8));padded.paste(part,(4,4));xy=(xy[0]-4,xy[1]-4)
 save('teeth_'+side,padded,'assembly_sources/head/RYO_HEAD_viseme_E_v001.png',[260,140,484,180],list(xy),'posterior_enamel','Only observed E-source enamel. Static uniform0.5 registration and approved white transform. Left/right crop '+str(box)+'. Entire independent wing starts above the closed upper aperture, then translates outward20px and downward9px with slight rigid rotation as spread increases. The aperture spatially uncovers its anatomical taper; there is no moving vertical enamel cut or UV/scale/color change. Front arch remains at533,626. Hidden anatomical correspondence and paths are inferred.')
# Source-backed hidden enamel-root underlap attaches to the fixed front arch.
# The tiny source enamel strip is cropped, not stretched. Its inferred static
# mask stops before each original crown's top boundary; zero-spread lip occlusion
# hides it completely. No original tooth color or alpha is changed.
front=np.array(Image.open(P/'rig_assets/yawn_mouth/upper_teeth.png'))
roots=np.array(b.crop((24,7,88,11)))
for x in range(64):
 ys=np.where(front[:,x,3]>=128)[0]
 top=626+int(ys[0]) if len(ys) else 626
 for y in range(4):
  if 629+y>=top:roots[y,x,3]=0
save('upper_enamel_roots',Image.fromarray(roots),'assembly_sources/head/RYO_HEAD_viseme_E_v001.png',[308,154,436,162],[533,629],'enamel_root_underlap','Actual observed E-source enamel, uniform0.5 registration, fixed at the approved front-arch attachment. Inferred static upper-root ownership ends before each original crown top. It is uncovered by upperlip-center lift and never translates, changes scale, or replaces the central arch. Baseline rendered invisibility must be verified.')
a=source('RYO_HEAD_tongue_v001.png');x=np.array(a);x[:,:,3]=np.rint(np.clip((x[:,:,3].astype(float)-16)/239,0,1)*255).astype('uint8');b=Image.fromarray(x).crop((83,25,467,219)).resize((100,50),Image.Resampling.LANCZOS)
padded=Image.new('RGBA',(108,58));padded.paste(b,(4,4))
save('tongue_surface',padded,'assembly_sources/head/RYO_HEAD_tongue_v001.png',[83,25,467,219],[510,667],'lower_oral_surface','Inferred lower oral/tongue top surface registration. Deep source owner rests fully behind aperture at spread0 and translates rigidly upward at spread>0; no whole-mouth patch. Existing tongue owner/texture/home remain unchanged and occluded below the bounded aperture.')
M['inference']=['Existing26 lip-joint sleeves are entirely inferred pigment; wider reveal increases their contribution. Their original full inferred-mask atlas remains authoritative. No claim of negligible contribution.','New enamel anatomical correspondence, cutout mattes, registration, tooth attachment rotations and reveal boundaries are inferred. Pigment is from actual assembly anatomy; no artificial colored geometry. Moving posterior enamel and tongue textures have4px transparent padding; retained source-derived RGBA remains unchanged inside it.','New cavity continuation and lower oral-surface placement are inferred unseen anatomy. Observed-support masks identify source-derived pigment, not a claim that its new placement was observed.','Current spread support does not implement inward/rounded lips, independent closed-smile corner lift, tongue articulation or phonemes.']
# Wider alpha-bearing joint gaps need separately owned inferred edge sleeves.
# Original twelve-pixel sleeves and all original157PNGs remain untouched.
old=json.loads((P/'rig_assets/smile_support/manifest.json').read_text())
source_atlas=Image.open(P/'rig_assets/smile_support/lip_continuations_atlas.png').convert('RGBA')
atlas=Image.new('RGBA',(168,265));inferred=Image.new('L',atlas.size);M['joint_extensions']=[]
for i,e in enumerate(old['lip_continuations']):
 x,y,w,h=e['atlas_rect'];a=np.array(source_atlas.crop((x,y,x+w,y+h)))
 b=np.pad(a,((0,0),(4,4),(0,0)),mode='edge');part=Image.fromarray(b)
 xy=(i%6*28+4,i//6*53+4);atlas.paste(part,xy);inferred.paste(Image.fromarray((b[:,:,3]>0).astype('uint8')*255),xy)
 M['joint_extensions'].append({'name':e['name']+'_outer_underlap','parent':e['name'],'edge':e['edge'],'upper':e['upper'],'file':'joint_edge_underlaps_atlas.png','inferred_mask':'joint_edge_underlaps_inferred_atlas.png','atlas_rect':[*xy,20,45],'pivot':[10,14],'classification':'ENTIRELY_INFERRED_HIDDEN_JOINT_PIGMENT','note':'Native old sleeve cross-section extended at its left/right edge. Fixed UV; only outside old sleeve support is spatially uncovered. Original owner remains unchanged.'})
atlas.save(O/'joint_edge_underlaps_atlas.png');inferred.save(O/'joint_edge_underlaps_inferred_atlas.png')
M['control']['center_lift_px']=4
M['sources']['rig_assets/smile_support/lip_continuations_atlas.png']=sha(P/'rig_assets/smile_support/lip_continuations_atlas.png')
M['inference'].append('26 new entirely inferred outer underlaps extend existing lip-joint cross-sections. Their full support is masked in a separate atlas. They appear only where rigid endpoint gaps extend beyond the original12px sleeve, not via opacity blending.')
(O/'manifest.json').write_text(json.dumps(M,indent=2)+'\n')
print('SPREAD_SUPPORT_BUILD_PASS',len(M['objects']))

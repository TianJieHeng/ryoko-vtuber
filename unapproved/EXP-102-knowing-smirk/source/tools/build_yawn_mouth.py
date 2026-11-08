#!/usr/bin/env python3
"""Recut the approved neutral lips; register oral interiors for continuous opening.
Alpha masks, static registrations and explicit tooth-only whitening. Input source bytes are immutable.
"""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy.ndimage import gaussian_filter1d
from PIL import Image,ImageDraw,ImageFilter
R=Path(__file__).resolve().parents[1];O=R/'rig_assets/yawn_mouth';F=R/'rig_assets/object_face';O.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest={'version':2,'mechanism':'Original approved neutral lip-color silhouette, upper/lower alpha ownership with static alpha-over correction; rigid lower-lip translation. Source-assembly oral interiors behind alpha-only aperture. Identity UV, no scale, no replacement or opacity crossfade.','sources':{},'objects':{},'estimates':{'neutral_lips':'Source-authored visible lip colors recut with a tight alpha silhouette including the under-lip shadow. Boundary coverage is estimated; no surrounding rectangular skin patch travels.','oral_interiors':'Previously registered source-assembly cavity, teeth and tongue reused; they are not claimed visible in the canonical neutral.'}}
source=R/'canonical_sources/approved_neutral.png';im=Image.open(source).convert('RGBA')
# Native approved mouth placement and shape. This is not the generic85x13 line.
box=(525,620,605,665);x0,y0,x1,y1=box;w=x1-x0;h=y1-y0
mask=Image.new('L',(w*4,h*4));d=ImageDraw.Draw(mask)
poly=[(527,632),(532,630),(543,627),(550,624),(558,625),(563,624),(570,624),(580,627),(591,630),(601,632),(603,635),(600,637),(591,639),(583,643),(576,647),(564,648),(552,647),(543,643),(536,639),(529,637),(527,636)]
d.polygon([((x-x0)*4,(y-y0)*4) for x,y in poly],fill=255)
d.ellipse(((549-x0)*4,(646-y0)*4,(581-x0)*4,(662-y0)*4),fill=255)
mask=mask.resize((w,h),Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(1.0))
a=np.array(im.crop(box));a[:,:,3]=np.array(mask)
Image.fromarray(a).save(F/'neutral_lips.png')
main=a.copy();shadow=a.copy();main[28:,:,3]=0;shadow[:28,:,3]=0
Image.fromarray(main).save(O/'upper_lip.png');Image.fromarray(main).save(O/'lower_lip.png');Image.fromarray(shadow).save(O/'underlip_shadow.png')
manifest['neutral_registration']={'xy':[x0,y0],'size':[w,h],'center_x':564.5,'upper_y':633.0,'opening_height':56.0,'lower_lip_travel':54.0,'seam_owner_x':[9.0,70.0],'lip_mask_polygon':poly}
# Dark original mouth seam, continuous across the visible mouth width.
lum=a[:,:,:3].mean(2);score=lum.copy();score[:10]=1000;score[18:]=1000;seam=np.argmin(score,axis=0)
seam[:4]=seam[4];seam[-4:]=seam[-5];seam=gaussian_filter1d(seam.astype(float),2.0)
sm=np.zeros((1,w,4),dtype=np.uint8);sm[0,:,0]=np.rint(seam*4);sm[0,:,3]=255;Image.fromarray(sm).save(O/'neutral_seam.png')
for name in ['upper_lip','lower_lip','underlip_shadow']:
 manifest['objects'][name]={'file':name+'.png','xy':[x0,y0],'size':[w,h],'z':53 if name=='underlip_shadow' else 58,'source':'canonical_sources/approved_neutral.png','source_visible_crop':list(box),'operation':'Original approved neutral lip colors inside traced alpha silhouette; static shader coverage divides upper and lower ownership.'}
manifest['sources'][str(source.relative_to(R))]=sha(source)
manifest['sources']['rig_assets/object_face/neutral_lips.png']=sha(F/'neutral_lips.png')
def part(name,fn,size,xy,z,center_crop=False):
 p=R/'assembly_sources/head'/fn;b=np.array(Image.open(p).convert('RGBA'));b[:,:,3]=np.rint(np.clip((b[:,:,3].astype(float)-16)/239,0,1)*255).astype('uint8')
 bounds=Image.fromarray(b[:,:,3]).point(lambda x:255 if x>=32 else 0).getbbox();im=Image.fromarray(b).crop(bounds)
 if center_crop:
  iw,ih=im.size;im=im.crop((round(iw*.25),round(ih*.35),round(iw*.75),round(ih*.65)))
 im=im.resize(size,Image.Resampling.LANCZOS)
 if name in ['upper_teeth','lower_teeth']:
  # Neutral-white enamel; retain source luminance boundaries and alpha.
  c=np.array(im);luma=c[:,:,:3].astype(float)@np.array([.2126,.7152,.0722])
  white=np.rint(np.clip(135.0+.5*luma,0,255)).astype('uint8')
  c[:,:,:3]=white[:,:,None];im=Image.fromarray(c)
 if name in ['tongue','lower_teeth']:
  padded=Image.new('RGBA',(size[0]+4,size[1]+4));padded.paste(im,(2,2));im=padded;xy=[xy[0]-2,xy[1]-2]
 im.save(O/(name+'.png'));manifest['sources'][str(p.relative_to(R))]=sha(p)
 manifest['objects'][name]={'file':name+'.png','xy':xy,'size':list(im.size),'z':z,'source':str(p.relative_to(R)),'source_visible_crop':bounds,'operation':'Static canonical-mouth registration of immutable source-assembly interior; transparent edge guard where moving. Identity UV at runtime.'}
part('cavity','RYO_HEAD_mouth_cavity_v001.png',(80,76),[525,629],54,True)
# The source arch has a scooped top: front crowns start 5–6 px below its
# crop origin. Place that top behind the stationary upper lip, not 7 px
# below it. The aperture hides the tooth roots/side tips, while the same
# whitened source crowns remain visible. This is one static registration;
# no animated scaling, redraw or yawn-dependent swap.
part('upper_teeth','RYO_HEAD_upper_teeth_v001.png',(64,14),[533,626],55)
manifest['version']=4
manifest['upper_teeth_correction']={'baseline_xy':[533,634],'corrected_xy':[533,626],'static_translation':[0,-8],'texture_bytes_unchanged':False,'reason':'Occlude the source arch top under the fixed upper lip; remove detached dark gap and side-first dental-outline reveal. Visible crown alpha and boundaries remain source-derived; tooth-only whitening is documented separately.','estimate':'Static registration is inferred because the canonical neutral does not expose teeth. No missing tooth pixels are generated.'}
part('lower_teeth','RYO_HEAD_lower_teeth_v001.png',(58,12),[535,687],55)
part('tongue','RYO_HEAD_tongue_v001.png',(53,25),[538,673],56)
manifest['mouth_limit']={'normalized_control_range':[0.0,1.0],'effective_aperture_cap':0.55,'max_aperture_source_px':30.8,'max_lower_lip_translation_source_px':29.7,'reference_sha256':'27251922a6834aaf65a7d1da787bba89621ea63643f8eea68627a64570cf9a77','reference_scale_estimate':0.792,'reason':'Conservative dark-opening bound measured against user screenshot at matching facial scale. Existing shape is evaluated at the capped control, never compressed or scaled.'}
manifest['tooth_whitening']={'objects':['upper_teeth','lower_teeth'],'operation':'Neutral RGB = round(clamp(135 + 0.5 * Rec709 source luminance, 0, 255)); alpha and source tooth boundaries retained. Static derivative only.','source_pixels_immutable':True,'upper_tooth_attachment_xy':[533,626]}
(O/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('CANONICAL_YAWN_MOUTH_BUILD_OK',len(manifest['objects']))

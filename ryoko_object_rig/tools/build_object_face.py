#!/usr/bin/env python3
"""Register clean original assembly parts into one common bust canvas.
Source PNGs are immutable. Derivatives clean faint alpha residue and receive a
fixed build-time registration. Runtime never warps or scales any face object.
"""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'rig_assets/object_face';OUT.mkdir(exist_ok=True)
W,H=1136,1384
base=np.array(Image.open(ROOT/'artwork/bust_base.png').convert('RGBA'))
manifest={'version':2,'canvas':[W,H],'coordinate_convention':'screen_left = source character R; screen_right = source character L','runtime_policy':'Rigid translation/rotation plus visibility clipping only. No scale animation, UV warp, baked face patch, or alpha emotion handover.','objects':{},'sources':{},'estimates':{'hidden_face':'None. The foundation is the original clean source face with no eyes, brows, lips or hair.','appearance':'Source pack shading, nose, eye drawing and hair silhouette differ from the former canonical composite. Fixed registration is newly authored, not claimed pixel-identical.','neck':'Fixed visible canonical neck/torso crop; no neck animation or hidden neck completion is claimed.'}}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def part(name,source,box,z,pivot=None,parent='head',clip=None):
 p=ROOT/'assembly_sources'/source;im=Image.open(p).convert('RGBA');a=np.array(im)
 a[:,:,3]=np.rint(np.clip((a[:,:,3].astype(float)-16)/239,0,1)*255).astype('uint8')
 bounds=Image.fromarray(a[:,:,3]).point(lambda x:255 if x>=32 else 0).getbbox();im=Image.fromarray(a).crop(bounds)
 x0,y0,x1,y1=box;im=im.resize((x1-x0,y1-y0),Image.Resampling.LANCZOS)
 if clip:
  arr=np.array(im);clip(arr,x0,y0);im=Image.fromarray(arr)
 im.save(OUT/(name+'.png'));manifest['sources'][str(p.relative_to(ROOT))]=sha(p)
 manifest['objects'][name]={'file':name+'.png','xy':[x0,y0],'size':list(im.size),'z':z,'pivot':pivot or [(x1+x0)/2,(y1+y0)/2],'parent':parent,'source':str(p.relative_to(ROOT)),'source_visible_crop':bounds,'alpha_cleanup':'Source alpha <=16/255 removed; retained alpha rescaled then visible-core crop at32/255. Original source bytes unchanged.','runtime_transforms':'translation, rotation, aperture clip only'}
 return im
# Full clean source face, not patched canonical skin.
part('stationary_backing','head/RYO_HEAD_face_base_v001.png',(398,316,739,726),20,[568,720])
part('ear_screen_left','head/RYO_HEAD_ear_R_v001.png',(382,532,430,615),18,[414,562])
part('ear_screen_right','head/RYO_HEAD_ear_L_v001.png',(706,532,754,615),18,[722,562])
part('hair_short_tail','hair/short_tail.png',(703,139,839,355),3,[731,174])
part('hair_rear_scalp','hair/rear_scalp_nape.png',(320,225,817,749),4,[568,390])
part('hair_bun','hair/bun.png',(516,82,763,264),5,[627,217])
# Temple roots render below the fringe to hide their attachment seam.
part('hair_temple_screen_left','hair/temple_lock_character_right.png',(318,467,411,792),60,[392,477])
part('hair_temple_screen_right','hair/temple_lock_character_left.png',(725,475,808,744),60,[736,489])
part('hair_front_fringe','hair/front_fringe.png',(282,190,855,687),70,[568,256])
# Fixed canonical neck and outfit: remove every old hair fragment above the
# collars, using skin-only source coverage. No replacement skin is painted.
body=base.copy();yy,xx=np.mgrid[:H,:W];rgb=base[:,:,:3].astype(float)
body[yy<700,3]=0
warm_skin=(rgb[:,:,0]-rgb[:,:,1]>20)&(rgb[:,:,1]-rgb[:,:,2]>5)
neck_width=np.interp(yy,[700,720,735,780,810],[48,70,84,90,115])
neck=(np.abs(xx-568)<=neck_width)&warm_skin
body[(yy>=700)&(yy<760)&~neck,3]=0
body[(yy>=760)&(yy<810)&warm_skin&~neck,3]=0
old_green=(rgb[:,:,1]-rgb[:,:,0]>-8)&(rgb[:,:,1]-rgb[:,:,2]>4)&(rgb[:,:,0]<245)
body[(yy>=760)&(yy<870)&old_green,3]=0
old_accessory=(rgb[:,:,0]-rgb[:,:,1]>15)&(rgb[:,:,1]-rgb[:,:,2]>25)&((xx<430)|(xx>710))
body[(yy>=760)&(yy<810)&old_accessory,3]=0
# Preserve the real curved gray collar tips, not a horizontal y760 cut.
collar=Image.new('L',(W,H));d=ImageDraw.Draw(collar)
d.polygon([(485,724),(475,730),(459,738),(448,748),(437,762),(431,779),(454,807),(480,788),(490,754)],fill=255)
d.polygon([(648,724),(662,731),(679,741),(692,756),(702,777),(681,807),(651,785),(642,753)],fill=255)
collar_mask=np.array(collar)>0
gray=(np.abs(rgb[:,:,0]-rgb[:,:,1])<18)&(rgb[:,:,2]>=rgb[:,:,1]-4)
restore=collar_mask&gray&(yy<810)
body[restore]=base[restore]
body[:,:,3][body[:,:,3]<16]=0
# Keep the connected neck/outfit component, removing isolated old matte dust.
labels,count=ndimage.label(body[:,:,3]>0,structure=np.ones((3,3)))
sizes=np.bincount(labels.ravel());sizes[0]=0;keep=labels==int(sizes.argmax())
removed_body_dust=int(((body[:,:,3]>0)&~keep).sum());body[:,:,3][~keep]=0
Image.fromarray(body).save(OUT/'fixed_neck_torso.png')
manifest['body']={'file':'fixed_neck_torso.png','xy':[0,0],'size':[W,H],'z':10,'source':'artwork/bust_base.png','method':'Visible source neck/outfit only, with source-traced curved collar tips. Old hair above collar excluded; largest connected component removes matte dust; no hidden-area synthesis.','removed_disconnected_dust_pixels':removed_body_dust}
manifest['sources']['artwork/bust_base.png']=sha(ROOT/'artwork/bust_base.png')
# Source-pixel accessories stay independent; no surrounding face or hair travels.
for side in ['screen_left','screen_right']:
 p=ROOT/'rig_assets'/('earring_'+side+'.png');im=Image.open(p);im.save(OUT/('earring_'+side+'.png'))
 manifest['sources'][str(p.relative_to(ROOT))]=sha(p)
 manifest['objects']['earring_'+side]={'file':'earring_'+side+'.png','xy':[0,0],'size':[W,H],'z':80,'pivot':[414,580] if side=='screen_left' else [726,580],'parent':'head','source':str(p.relative_to(ROOT)),'runtime_transforms':'rigid; source recut retained'}
# Two original canonical hairsticks plus hanging ornament, re-cut by their gold
# pixels on the existing isolated transparent background. No new accessory art.
for name,box,pivot in [('hairsticks',(575,86,810,228),(680,200)),('hanging_ornament',(780,184,804,315),(790.5,184))]:
 x0,y0,x1,y1=box;a=base[y0:y1,x0:x1].copy();r=a[:,:,:3].astype(float)
 gold=(r[:,:,0]-r[:,:,1]>7)&(r[:,:,1]-r[:,:,2]>12)
 a[:,:,3]=np.where(gold,a[:,:,3],0);Image.fromarray(a).save(OUT/(name+'.png'))
 manifest['objects'][name]={'file':name+'.png','xy':[x0,y0],'size':[x1-x0,y1-y0],'z':75,'pivot':list(pivot),'parent':'head','source':'artwork/bust_base.png','runtime_transforms':'rigid; canonical accessory recut'}
for side,char in [('screen_left','R'),('screen_right','L')]:
 left=side=='screen_left'
 part('sclera_'+side,'head/RYO_HEAD_sclera_'+char+'_v001.png',(420,483,532,518) if left else (605,483,717,518),30)
 # Place the complete original iris behind the upper lid, not fully exposed.
 part('iris_'+side,'head/RYO_HEAD_iris_pupil_'+char+'_v001.png',(455,470,496,510) if left else (629,470,670,510),32)
 part('lash_'+side,'head/RYO_HEAD_lash_lid_'+char+'_v001.png',(407,469,538,508) if left else (599,469,730,508),40)
 part('brow_'+side,'head/RYO_HEAD_brow_'+char+'_v001.png',(437,449,538,474) if left else (600,449,701,474),50)
 part('closed_reference_'+side,'head/RYO_HEAD_closed_lid_'+char+'_v001.png',(412,487,536,518) if left else (601,487,725,518),40)
# The authored neutral lips are the default drawable. A/E/I/O/U remain
# exclusive discrete source variants; no continuous oral timeline is shipped.
part('neutral_lips','head/RYO_HEAD_neutral_lips_v001.png',(526,635,611,648),55)
part('viseme_A','head/RYO_HEAD_viseme_A_v001.png',(529,614,609,704),55)
part('viseme_E','head/RYO_HEAD_viseme_E_v001.png',(516,626,622,671),55)
part('viseme_I','head/RYO_HEAD_viseme_I_v001.png',(515,630,623,658),55)
part('viseme_O','head/RYO_HEAD_viseme_O_v001.png',(539,614,598,704),55)
part('viseme_U','head/RYO_HEAD_viseme_U_v001.png',(544,631,593,668),55)
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
canvas=Image.new('RGBA',(W,H));stack=list(manifest['objects'].items())+[('body',manifest['body'])]
for name,e in sorted(stack,key=lambda p:p[1]['z']):
 if name.startswith(('closed_reference','viseme_')):continue
 canvas.alpha_composite(Image.open(OUT/e['file']).convert('RGBA'),tuple(e['xy']))
canvas.save(OUT/'neutral_registration_reference.png')
print('CLEAN_OBJECT_ASSETS_READY',len(manifest['objects']),'source_parts',len(manifest['sources']),'estimated_face_pixels=0')

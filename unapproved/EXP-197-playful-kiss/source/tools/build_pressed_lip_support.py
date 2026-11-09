#!/usr/bin/env python3
"""Inferred hidden inner-upper-lip pigment; original artwork is never modified."""
from pathlib import Path
import hashlib,json
from PIL import Image
import numpy as np
P=Path(__file__).resolve().parents[1];D=P/'rig_assets/pressed_lip_support';D.mkdir(exist_ok=True)
source=P/'rig_assets/yawn_mouth/upper_lip.png';seam_path=P/'rig_assets/yawn_mouth/neutral_seam.png'
a=np.array(Image.open(source).convert('RGBA'));seams=np.array(Image.open(seam_path).convert('RGBA'))[0,:,0].astype(float)/4
out=np.zeros_like(a);records=[]
for x in range(a.shape[1]):
 # A single immutable source pixel supplies the pigment for each hidden column.
 # Opaque dark contour is intentionally sampled; no visible pixels are repainted.
 ys=np.arange(max(0,int(seams[x])-2),min(a.shape[0],int(seams[x])+3))
 viable=ys[a[ys,x,3]>64]
 if not len(viable):continue
 luminance=a[viable,x,:3]@np.array([.2126,.7152,.0722]);sy=int(viable[np.argmin(luminance)])
 top=max(0,int(seams[x])-4);bottom=min(a.shape[0],int(seams[x])+14)
 out[top:bottom,x,:3]=a[sy,x,:3];out[top:bottom,x,3]=255
 records.append({'column':x,'sample_xy':[x,sy],'hidden_y_range':[top,bottom]})
Image.fromarray(out).save(D/'inner_upper_lip.png');Image.fromarray(np.where(out[:,:,3]>0,255,0).astype('uint8')).save(D/'inner_upper_lip_inferred_mask.png')
sha=lambda q:hashlib.sha256(q.read_bytes()).hexdigest()
m={'classification':'ENTIRELY_INFERRED_HIDDEN_INNER_UPPER_LIP_UNDERLAP','source':str(source.relative_to(P)),'source_sha256':sha(source),'seam':str(seam_path.relative_to(P)),'seam_sha256':sha(seam_path),'origin':[525,620],'size':[80,45],'pigment_file':'inner_upper_lip.png','pigment_sha256':sha(D/'inner_upper_lip.png'),'inferred_mask':'inner_upper_lip_inferred_mask.png','inferred_mask_sha256':sha(D/'inner_upper_lip_inferred_mask.png'),'operation':'Column-wise fixed pigment copied from each existing lip inner-edge darkest covered pixel near the registered seam. Vertical continuation is inferred hidden inner-lip tissue, not observed artwork. Each child is rigidly carried by an existing upper-lip joint. Only spatial aperture/depth clipping reveals it. No teeth tint, scale or UV change.','control':{'name':'mouth_lip_press','range':[0,1],'maximum_depth_source_px':4.0,'default':0.0,'outer_lip_translation':0,'teeth_translation':0},'source_samples':records}
(D/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
print('PRESSED_LIP_BUILD',sha(D/'inner_upper_lip.png'))

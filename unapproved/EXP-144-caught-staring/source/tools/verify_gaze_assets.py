#!/usr/bin/env python3
"""Immutable originals, clean iris evidence, masks and compositing algebra."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1];G=R/'rig_assets/gaze_eyes'
m=json.loads((G/'manifest.json').read_text());original=json.loads((R/'GAZE_SOURCE_ORIGINALS.json').read_text());checks=0
def check(value,label):
 global checks
 assert value,label;checks+=1
def im(name):return np.array(Image.open(G/name).convert('RGBA'))
for file,sha in original['original_pngs'].items():check(hashlib.sha256((R/file).read_bytes()).hexdigest()==sha,file)
check(len(original['original_pngs'])==103,'Original image count')
source=np.array(Image.open(R/'artwork/bust_base.png'))
for side,e in m['eyes'].items():
 a=im(f'iris_{side}.png');b=im(f'sclera_{side}.png');p=im(f'aperture_{side}.png')[:,:,0]>0
 observed=im(e['observed_iris_mask'])[:,:,0]>0;hidden=im(f'iris_hidden_estimate_{side}.png')[:,:,0]>0
 hmask=im(e['iris_under_hair_estimate_mask'])[:,:,0]>0;matte=im(f'iris_matte_estimate_{side}.png')[:,:,0]>0
 px,py=e['iris_padding'];w,h=e['size'];ox,oy=e['origin'];local=a[py:py+h,px:px+w];anchors=observed[py:py+h,px:px+w]
 check(not (anchors&hmask).any(),'Hair is not observed iris')
 # Observed support includes canonical iris edge evidence whose matte is inferred.
 # Only the fully opaque subset below claims exact original RGB.
 core=anchors&(local[:,:,3]==255)
 check(np.array_equal(local[:,:,:3][core],source[oy:oy+h,ox:ox+w,:3][core]),'Observed opaque RGB unchanged')
 check(np.array_equal(b[:,:,3]>0,p),'Stationary sclera covers entire fixed aperture')
 check((b[:,:,3][p]==255).all(),'Opaque sclera backing')
 check(int(hidden.sum())==e['hidden_iris_estimate_pixels'],'Inferred pixel count')
 check(int(observed.sum())==e['observed_iris_pixels'],'Observed pixel count')
 check(int(hmask.sum())==e['hair_transfer_pixels'],'Hair transfer count')
 check(int(matte.sum())==e['matte_estimate_pixels'],'Matte count')
 yy,xx=np.mgrid[:h,:w];cx,cy,rx,ry,tilt=e['ellipse_estimate'];rad=np.sqrt(((xx+ox-cx-tilt*(yy+oy-cy))/rx)**2+((yy+oy-cy)/ry)**2)
 pale=(rad>.88)&(local[:,:,3]>0)&(local[:,:,:3].min(axis=2)>125)&(np.ptp(local[:,:,:3].astype(float),axis=2)<60)
 check(not pale.any(),'No moving near-white perimeter texels')
 import_text=(G/f'iris_{side}.png.import').read_text()
 check('process/fix_alpha_border=false' in import_text,'Preserve unmatted RGB import')
 check('mipmaps/generate=false' in import_text,'No hidden footprint expansion from mipmaps')
for q in np.linspace(0,1,33):
 for alpha in np.linspace(0,1,33):
  ba=q*(1-alpha)/max(1-q*alpha,1e-6);fa=q*alpha
  check(abs(fa+ba*(1-fa)-q)<1e-9,'Single aperture opacity factored across two sprites')
print(json.dumps({'status':'pass','checks':checks,'original_pngs_unchanged':103,'gaze_px':m['calibrated_travel_source_pixels'],'visual_approval_required':True},indent=2))

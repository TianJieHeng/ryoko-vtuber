#!/usr/bin/env python3
"""Continuous conservative fixed-aperture/bilinear footprint proof; no foreground occlusion is assumed."""
from pathlib import Path
from PIL import Image
from scipy.ndimage import distance_transform_edt
import numpy as np,json,sys,os,hashlib
R=Path(__file__).resolve().parents[1];P=R;M=json.loads((P/'rig_assets/gaze_eyes/manifest.json').read_text())
XMAX,UP,DOWN=map(float,sys.argv[1:4]) if len(sys.argv)>1 else (4.,2.,1.)
def image(path):return np.array(Image.open(path).convert('RGBA'))
results={}
for side,e in M['eyes'].items():
 w,h=e['size'];px,py=e['iris_padding'];a=image(P/f'rig_assets/gaze_eyes/iris_{side}.png')[:,:,3]/255
 aperture=image(P/f'rig_assets/gaze_eyes/aperture_{side}.png')[:,:,0]>0
 hidden=image(P/f'rig_assets/gaze_eyes/iris_hidden_estimate_{side}.png')[:,:,0]>0
 known=np.zeros(a.shape,bool);known[py:py+h,px:px+w]=(a[py:py+h,px:px+w]>.05)&aperture
 if 'observed_iris_mask' in e:known=image(P/'rig_assets/gaze_eyes'/e['observed_iris_mask'])[:,:,0]>0
 dist=distance_transform_edt(~known)
 completed=image(P/f'rig_assets/gaze_eyes/completed_iris_{side}.png')[:,:,0]>0
 top=image(P/f'rig_assets/object_face/profile_{side}.png')[:,:,0];bot=image(P/f'rig_assets/object_face/lower_profile_{side}.png')[:,:,0]
 assert np.all(top==top[:1,:]) and np.all(bot==bot[:1,:]),'Profiles not column-constant'
 rect=[]
 # All breakpoints of linear-aperture support and nearest profile lookup
 # occur on integer or half-integer x. Within each open band, enumerate
 # exact nonzero-aperture y intervals and intersect fixed lid coverage.
 for lo in np.arange(-.5,w-.5,.5):
  hi=lo+.5;mid=(lo+hi)/2;col=int(np.clip(np.floor(mid+.5),0,w-1))
  support_cols=np.flatnonzero(abs(np.arange(w)-mid)<1)
  ys=np.flatnonzero(aperture[:,support_cols].any(axis=1))
  for y in ys:
   ya=max(float(y)-1,float(top[0,col])-.5,-.5);yb=min(float(y)+1,float(bot[0,col])+1.5,h-.5)
   if yb>ya:rect.append((lo,hi,ya,yb))
 rect=np.array(rect);bad=[];active=[];maxdist=0.;beyond_band=[]
 for sy,sx in zip(*np.where(hidden&(a>0))):
  sx0=sx-px;sy0=sy-py
  # Union of every possible bilinear footprint at every continuous allowed offset.
  reach=(sx0-XMAX-1,sx0+XMAX+1,sy0-UP-1,sy0+DOWN+1)
  overlap=(np.minimum(rect[:,1],reach[1])>np.maximum(rect[:,0],reach[0])+1e-12)&(np.minimum(rect[:,3],reach[3])>np.maximum(rect[:,2],reach[2])+1e-12)
  if overlap.any():
   active.append((sx,sy));maxdist=max(maxdist,float(dist[sy,sx]))
   if dist[sy,sx]>e.get('completion_band_pixels',3)+1e-12:beyond_band.append([int(sx),int(sy),float(dist[sy,sx])])
   if not completed[sy,sx]:
    rr=rect[np.flatnonzero(overlap)[0]];bad.append({'texel':[int(sx),int(sy)],'distance':float(dist[sy,sx]),'q_support_rect':rr.tolist(),'reachable_rect':list(reach)})
 results[side]={'continuous_x_range':[-XMAX,XMAX],'continuous_y_range':[-UP,DOWN],'reachable_hidden_texels':len(active),'max_hidden_distance':maxdist,'violating_hidden_texels':len(bad),'anchor_basis':e.get('observed_iris_mask','old_alpha_gt0.05'),'completion_band_pixels':e.get('completion_band_pixels',3),'texels_beyond_completion_band':beyond_band,'manifest_sha256':hashlib.sha256((P/'rig_assets/gaze_eyes/manifest.json').read_bytes()).hexdigest(),'iris_sha256':hashlib.sha256((P/f'rig_assets/gaze_eyes/iris_{side}.png').read_bytes()).hexdigest(),'observed_mask_sha256':hashlib.sha256((P/'rig_assets/gaze_eyes'/e['observed_iris_mask']).read_bytes()).hexdigest() if 'observed_iris_mask' in e else None,'examples':bad[:10]}
print(json.dumps({'status':'pass' if all(e['violating_hidden_texels']==0 for e in results.values()) else 'fail','eyes':results},indent=2))
assert all(e['violating_hidden_texels']==0 for e in results.values()), 'Visible bilinear footprint outside actually completed iris art'

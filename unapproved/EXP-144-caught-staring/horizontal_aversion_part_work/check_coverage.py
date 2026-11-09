"""Narrow positive-x part support check, adapted from existing fixed-aperture proof.
No general gaze range expansion is asserted. Uses actual approved completed/art masks.
"""
from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
W=Path(__file__).resolve().parent
R=W.parent/'approved_upper_iris_repair_integration/candidate/ryoko_object_rig'
M=json.loads((R/'rig_assets/gaze_eyes/manifest.json').read_text())
def image(path):return np.array(Image.open(path).convert('RGBA'))
results={}
for side,e in M['eyes'].items():
 w,h=e['size'];px,py=e['iris_padding'];a=image(R/f'rig_assets/gaze_eyes/iris_{side}.png')[:,:,3]/255
 aperture=image(R/f'rig_assets/gaze_eyes/aperture_{side}.png')[:,:,0]>0
 hidden=image(R/f'rig_assets/gaze_eyes/iris_hidden_estimate_{side}.png')[:,:,0]>0
 completed=image(R/f'rig_assets/gaze_eyes/completed_iris_{side}.png')[:,:,0]>0
 authored=image(W.parent/f'upper_iris_repair_proposal/authored_cap_mask_{side}.png')[:,:,0]>0
 top=image(R/f'rig_assets/object_face/profile_{side}.png')[:,:,0];bot=image(R/f'rig_assets/object_face/lower_profile_{side}.png')[:,:,0]
 rect=[]
 for lo in np.arange(-.5,w-.5,.5):
  hi=lo+.5;mid=(lo+hi)/2;col=int(np.clip(np.floor(mid+.5),0,w-1))
  cols=np.flatnonzero(abs(np.arange(w)-mid)<1)
  for y in np.flatnonzero(aperture[:,cols].any(axis=1)):
   ya=max(float(y)-1,float(top[0,col])+36*.18-.5,-.5);yb=min(float(y)+1,float(bot[0,col])+1.5,h-.5)
   if yb>ya:rect.append((lo,hi,ya,yb))
 rect=np.array(rect);bad=[];active=[]
 for sy,sx in zip(*np.where(hidden&(a>0))):
  sx0=sx-px;sy0=sy-py
  reach=(sx0-1,sx0+12+1,sy0-1,sy0+1)
  overlap=(np.minimum(rect[:,1],reach[1])>np.maximum(rect[:,0],reach[0])+1e-12)&(np.minimum(rect[:,3],reach[3])>np.maximum(rect[:,2],reach[2])+1e-12)
  if overlap.any():
   active.append((int(sx),int(sy)))
   if not completed[sy,sx] and not authored[sy,sx]:bad.append([int(sx),int(sy)])
 results[side]={'x_range':[0,12],'y':0,'minimum_lid_closure':.18,'reachable_hidden_texels':len(active),'uncovered_hidden_texels':len(bad),'uncovered_examples':bad[:15],'iris_sha256':hashlib.sha256((R/f'rig_assets/gaze_eyes/iris_{side}.png').read_bytes()).hexdigest()}
out={'scope':'continuous one-sided x0..12, y0, both lids >=.18; iris artwork footprint only, no extrapolation to onset or wider/unrestricted gaze','status':'PASS' if all(e['uncovered_hidden_texels']==0 for e in results.values()) else 'HOLD','eyes':results}
(W/'coverage.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

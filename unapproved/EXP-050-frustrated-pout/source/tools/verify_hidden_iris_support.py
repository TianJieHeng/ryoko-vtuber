#!/usr/bin/env python3
"""Full straight-RGBA old-domain lock + explicit directional support proof.

The frozen q rectangles include aperture linear support and nearest profile
breakpoints. Closure can only reduce q; smiling masks/foreground hair can only
occlude it. No foreground occlusion is needed by the proof.
"""
from pathlib import Path
import hashlib,json
import numpy as np
from scipy.ndimage import binary_dilation
from PIL import Image
R=Path(__file__).resolve().parents[1];G=R/'rig_assets/gaze_eyes';M=json.loads((G/'manifest.json').read_text());P=json.loads((R/'source_references/hidden_iris_cap_patch.json').read_text())
def im(p):return np.array(Image.open(p).convert('RGBA'))
def rectangles(e,side):
 w,h=e['size'];a=im(G/f'aperture_{side}.png')[:,:,0]>0;t=im(R/f'rig_assets/object_face/profile_{side}.png')[:,:,0];b=im(R/f'rig_assets/object_face/lower_profile_{side}.png')[:,:,0]
 assert np.all(t==t[:1,:]) and np.all(b==b[:1,:]);rect=[]
 for lo in np.arange(-.5,w-.5,.5):
  hi=lo+.5;mid=(lo+hi)/2;col=int(np.clip(np.floor(mid+.5),0,w-1));cols=np.flatnonzero(abs(np.arange(w)-mid)<1)
  for y in np.flatnonzero(a[:,cols].any(axis=1)):
   low=max(y-1.,float(t[0,col])-.5,-.5);high=min(y+1.,float(b[0,col])+1.5,h-.5)
   if high>low:rect.append((lo,hi,low,high))
 return np.array(rect)
def reachable(e,rect,down):
 iw,ih=e['iris_size'];px,py=e['iris_padding'];m=np.zeros((ih,iw),bool)
 for x in range(iw):
  rr=rect[(np.minimum(rect[:,1],x-px+5)>np.maximum(rect[:,0],x-px-5)+1e-12)]
  if len(rr):
   for y in range(ih):m[y,x]=np.any(np.minimum(rr[:,3],y-py+down+1)>np.maximum(rr[:,2],y-py-3)+1e-12)
 return m
results={}
for side,e in M['eyes'].items():
 p=P['eyes'][side];a=im(G/f'iris_{side}.png');old=reachable(e,rectangles(e,side),1);new=reachable(e,rectangles(e,side),6);completed=im(G/f'completed_iris_{side}.png')[:,:,0]>0
 assert int(old.sum())==p['old_reachable_count']
 assert hashlib.sha256(a[old].tobytes()).hexdigest()==p['old_reachable_rgba_sha256'],'All old reachable RGBA must remain exact, including alpha0 RGB'
 assert hashlib.sha256(a[:,:,3].tobytes()).hexdigest()==p['alpha_plane_sha256'],'Entire alpha plane must remain exact'
 assert not (new&(a[:,:,3]>0)&~completed).any(),'Uncompleted nonzero support'
 patch=np.zeros(old.shape,bool)
 for x,y,r,g,b in p['rgb_patch_xy_rgb']:
  assert list(a[y,x,:3])==[r,g,b];patch[y,x]=True
 assert not (old&patch).any(),'New art overlaps old footprint'
 assert np.all(new[patch]),'No excess artwork beyond selected domain'
 ring=np.zeros(old.shape,bool)
 for x,y in p['qualified_retained_ring_xy']:
  assert list(a[y,x,:3])==[55,29,17],'Canonical inferred dark perimeter only';ring[y,x]=True
 assert not (old&ring).any() and np.all(new[ring]) and not (ring&patch).any()
 completed_delta=np.zeros(old.shape,bool)
 for x,y in p['new_completed_xy']:completed_delta[y,x]=True
 assert np.array_equal(completed_delta,patch|ring),'Every new completion texel has disclosed ownership/provenance'
 observed=im(G/e['observed_iris_mask'])[:,:,0]>0
 assert not ((patch|ring)&observed).any(),'No observed pigment replacement'
 zero_edge=new&~old&(a[:,:,3]==0)&binary_dilation(a[:,:,3]>0,structure=np.ones((3,3)))
 assert np.all(a[zero_edge,:3]==np.array([55,29,17])),'New transparent edge RGB must be the unchanged canonical ring, not unverified cap color'
 imports=(G/f'iris_{side}.png.import').read_text();assert 'mipmaps/generate=false' in imports and 'process/fix_alpha_border=false' in imports and 'process/premult_alpha=false' in imports and 'compress/mode=0' in imports
 results[side]={'old_locked_rgba_texels':int(old.sum()),'locked_alpha_zero_texels':int((old&(a[:,:,3]==0)).sum()),'new_transparent_edge_texels':int(zero_edge.sum()),'transparent_edge_rgb':[55,29,17],'new_rgb_texels':int(patch.sum()),'retained_dark_ring_texels':int(ring.sum()),'old_domain_rgba_exact':True,'whole_alpha_exact':True,'new_domain_covered':True}
print(json.dumps({'status':'pass','old_domain':P['old_physical_domain'],'new_domain':P['new_physical_domain'],'eyes':results,'scope':'Continuous source/filter proof; final finite-render and visual gates required separately'},indent=2))

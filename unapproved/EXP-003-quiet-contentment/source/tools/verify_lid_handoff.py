#!/usr/bin/env python3
"""Source and spatial-mask checks for the ordinary near-closed lash correction.
Actual Godot dense trajectories and full-frame movie review remain required.
"""
from pathlib import Path
import hashlib,json
from welcome_source_guard import scoped_matches
import numpy as np
from scipy.ndimage import map_coordinates
from PIL import Image
R=Path(__file__).resolve().parents[1]
checks=0
def check(ok,message):
 global checks
 assert bool(ok),message
 checks+=1
def smooth(a,b,x):
 t=np.clip((x-a)/(b-a),0,1)
 return t*t*(3-2*t)
def seam(p,c):
 moving=p[2]-3+(p[0]-p[2]+5)*np.clip((c-.65)/.2,0,1)+36*c
 reveal=(p[3]-2)*(1-np.clip((c-.70)/.15,0,1))+(p[1]+2)*np.clip((c-.70)/.15,0,1)
 return np.minimum(moving,reveal)+4*smooth(.85,1.,c)
def coverage(role,p,lower,y,c,new):
 if role==1:
  threshold=seam(p,c)-36*c if new else p[2]-3+(p[0]-p[2]+5)*np.clip((c-.65)/.2,0,1)
  return smooth(-.5,.5,y-threshold)*(1-smooth(-.5,.5,y+36*c-(lower+1)))
 if role==2:
  old=1-smooth(0,1,y-(lower+7-max(0,(c-.65)/.35)*24))
  return old*smooth(-.5,.5,y-(p[0]+36*c-1.5)) if new else old
 if new:return np.maximum((1-smooth(-.5,.5,y-seam(p,c)))*smooth(-.5,.5,y-(p[3]-2)),smooth(-.5,.5,y-(p[1]+2)))
 threshold=p[1]+2-np.clip((c-.55)/.3,0,1)*(p[1]-p[3]+4)
 return smooth(-.5,.5,y-threshold)
base=json.loads((R/'validation/lid_handoff_baseline.json').read_text())
check(len(base['unchanged_pngs'])==126,'Expected all 126 delivered PNGs')
migration=json.loads((R/'validation/smile_lid_baseline_migration.json').read_text())['files']
for group in ['unchanged_pngs','unchanged_runtime']:
 for name,h in base[group].items():
  actual=hashlib.sha256((R/name).read_bytes()).hexdigest()
  if group=='unchanged_runtime' and name in migration:
   check(h==migration[name]['ordinary_lid_baseline_sha256'] and (actual==migration[name]['combined_smile_sha256'] or scoped_matches(name,migration[name]['combined_smile_sha256'])),name+' explicit shared smile migration')
  else:check(actual==h or (group=='unchanged_runtime' and scoped_matches(name,h)),name)
shader=(R/'canonical_eye_alpha.gdshader').read_text()
check(shader.count('lash_handoff_seam(p,c)')==2,'Both lash owners must call the same spatial seam')
check('float threshold=lash_handoff_seam(p,c)-36.0*c;' in shader,'Moving-lash local coordinate conversion')
check('float threshold=lash_handoff_seam(p,c);' in shader,'Closed-lash fixed coordinate')
check('coverage=max(handoff,original_boundary);' in shader,'Static original edge ownership plus complementary handoff')
for side in ['screen_left','screen_right']:
 folder=R/'rig_assets/object_face'
 profile=np.array(Image.open(folder/f'profile_{side}.png')).astype(float)
 p=np.moveaxis(profile,-1,0)
 lower=np.array(Image.open(folder/f'lower_profile_{side}.png'))[:,:,0].astype(float)
 y=np.indices(lower.shape)[0].astype(float)
 alpha={role:np.array(Image.open(folder/f'{name}_{side}.png'))[:,:,3]/255 for role,name in [(1,'upper_lash'),(2,'lower_contour'),(4,'closed_lash')]}
 for c in [0.,1.]:
  for role in [1,2,4]:check(np.array_equal(alpha[role]*coverage(role,p,lower,y,c,True),alpha[role]*coverage(role,p,lower,y,c,False)),f'{side}: endpoint {c}, role {role}')
 # Bilinear source support with nearest profile lookup, including quarter
 # phases. The closed owner's original static fringe is part of both endpoints.
 fy,fx=np.mgrid[-.25:lower.shape[0]-.5:.25,-.25:lower.shape[1]-.5:.25]
 col=np.clip(np.floor(fx+.5).astype(int),0,lower.shape[1]-1)
 fp=np.moveaxis(profile[0,col],-1,0)
 fl=lower[0,col]
 for c in [0.,1.]:
  for role in [1,2,4]:
   fa=map_coordinates(alpha[role],[fy,fx],order=1,mode='nearest')
   check(np.max(np.abs(fa*(coverage(role,fp,fl,fy,c,True)-coverage(role,fp,fl,fy,c,False))))<1e-12,f'{side}: bilinear endpoint {c}, role {role}')
 for c in np.linspace(0,1,401):
  cut=seam(p,c)
  for phase in [0.,.25,.5,.75]:
   fixed_y=y+phase
   before=smooth(-.5,.5,fixed_y-cut)
   after=1-smooth(-.5,.5,fixed_y-cut)
   check(np.max(np.abs(before+after-1))<1e-12,'Complementary masks must partition one boundary')
   check(not np.any((before>0)&(after>0)&(np.abs(fixed_y-cut)>=.5)),'Overlap only within one-pixel AA edge')
  lower_visible=alpha[2]*coverage(2,p,lower,y,c,True)
  check(not np.any(lower_visible[y<p[0]+36*c-2.0]>0),'Old lower contour cannot remain above approaching aperture')
  if c<=.70:check(not np.any(alpha[4]*coverage(4,p,lower,y,c,True)>0),'Closed-lash tip cannot appear before connected handoff')
print(json.dumps({'status':'pass','checks':checks,'unchanged_pngs':126,'closure_samples_per_eye':401,'subpixel_phases':4,'open_closed_source_alpha_identical':True,'note':'Source/algebra proof only; actual render and motion review are separate requirements.'},indent=2))

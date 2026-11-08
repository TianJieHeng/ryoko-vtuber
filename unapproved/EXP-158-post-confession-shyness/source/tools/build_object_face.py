#!/usr/bin/env python3
"""Assemble native canonical recuts. No generic head, face resize or neck wedge."""
from pathlib import Path
import json,hashlib,subprocess,sys,shutil
import numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage as ndi
R=Path(__file__).resolve().parents[1];O=R/'rig_assets/object_face';O.mkdir(parents=True,exist_ok=True)
H=R/'rig_assets/canonical_hair';E=R/'rig_assets/canonical_eyes'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
subprocess.run([sys.executable,str(R/'tools/build_canonical_hair.py')],check=True)
subprocess.run([sys.executable,str(R/'tools/build_hair_edge_mattes.py')],check=True)
subprocess.run([sys.executable,str(R/'tools/build_canonical_eyes.py'),'--source',str(R/'artwork/bust_base.png'),'--hair-mask',str(H/'full_hair_exclusion_mask.png'),'--hair-composite',str(H/'canonical_hair_matted_composite.png'),'--hair-matte-mask',str(H/'estimated_hair_matte_mask.png')],check=True)
subprocess.run([sys.executable,str(R/'tools/build_brow_d.py')],check=True)
subprocess.run([sys.executable,str(R/'tools/build_crossing_continuation.py')],check=True)
subprocess.run([sys.executable,str(R/'tools/build_yawn_mouth.py')],check=True)
hm=json.loads((H/'manifest.json').read_text());em=json.loads((E/'manifest.json').read_text())
B=R/'rig_assets/canonical_brows';C=B/'continuation_v2'
bm=json.loads((B/'manifest.json').read_text());cm=json.loads((C/'manifest.json').read_text())
cross_mask=np.array(Image.open(C/'crossing_correction_mask_full.png'))>0
hair_names=['temple_left','temple_right','crown_bun_rear','front_fringe']
owner_dist=[]
for name in hair_names:
 raw=np.array(Image.open(H/hm['layers'][name]['asset']))
 owner_dist.append(ndi.distance_transform_edt(~(raw[:,:,3]>0)))
cross_owner=np.argmin(owner_dist,axis=0)
cross_hair=Image.new('RGBA',(1136,1384))
for e in cm['patches'].values():cross_hair.alpha_composite(Image.open(C/e['hair_file']),tuple(e['xy']))
cross_hair=np.array(cross_hair)

m={'version':3,'canvas':[1136,1384],'coordinate_convention':'Native canonical source pixels. Screen side names. All source-visible head/hair/eye registration is unscaled.','runtime_policy':'Independent source cutouts; rigid movement and identity-UV alpha coverage only. No face warp, animated scale, emotion opacity crossfade or full face patch.','objects':{},'sources':{},'estimates':{'hair':hm['limitations'],'eyes':em['reconstruction'],'mouth':'Original approved lip color silhouette recut; alpha boundary estimated, preserved canonical lip shape. The separate static underlip shadow is occluded by the oral cavity, never dragged with lower lip.'},'gaze_supported':False}
m['estimates']['brow_hair_crossings']={'manifest':'rig_assets/canonical_brows/continuation_v2/manifest.json','method':'Explicit bounded same-strand continuation from source anchor rows where flattened brow and hair colors were mixed. Stationary skin and foreground hair have separate ownership. Neutral is not pixel-identical inside these masks.','validation':cm['validation']}
def add(name,path,xy,z,pivot=None,source='artwork/bust_base.png',**extra):
 im=Image.open(path).convert('RGBA')
 if name.startswith(('hair_','brow_')):
  ar=np.array(im);x,y=map(int,xy);hh,ww=ar.shape[:2];local=cross_mask[y:y+hh,x:x+ww]
  ar[local,3]=0
  if name in ['hair_'+n for n in hair_names]:
   owner=hair_names.index(name[5:]);take=local&(cross_owner[y:y+hh,x:x+ww]==owner)
   ar[take]=cross_hair[y:y+hh,x:x+ww][take]
  im=Image.fromarray(ar)
 target=O/(name+'.png');im.save(target)
 m['objects'][name]={'file':target.name,'xy':list(xy),'size':list(im.size),'z':z,'pivot':list(pivot or [xy[0]+im.width/2,xy[1]+im.height/2]),'source':source,'runtime_transforms':'rigid or alpha clip only',**extra}
# Erase baked eyes/brows through their complete owned masks, leaving stationary
# bounded hidden skin; these fills are never animated or faded.
back=Image.open(H/hm['backing']).convert('RGBA')
for key,e in em['objects'].items():
 if key.startswith('skin_'):back.alpha_composite(Image.open(E/e['file']),tuple(e['xy']))
for e in bm['objects'].values():back.alpha_composite(Image.open(B/e['skin']),tuple(e['xy']))
for e in cm['patches'].values():back.alpha_composite(Image.open(C/e['skin_file']),tuple(e['xy']))
a=np.array(back);body=a.copy();body[:720,:,3]=0;head=a.copy();head[720:,:,3]=0
Image.fromarray(head).save(O/'stationary_backing.png');Image.fromarray(body).save(O/'fixed_neck_torso.png')
m['objects']['stationary_backing']={'file':'stationary_backing.png','xy':[0,0],'size':[1136,1384],'z':20,'pivot':[568,720],'source':'artwork/bust_base.png','runtime_transforms':'stationary native source geometry; documented hidden backing only'}
m['body']={'file':'fixed_neck_torso.png','xy':[0,0],'size':[1136,1384],'z':10,'source':'artwork/bust_base.png','method':'Exact native canonical neck/torso. No width cap or reconstructed wedge. Static earrings remain source backing.'}
# True eye and brow owners. Skin is in the stationary backing above.
for key,e in em['objects'].items():
 if key.startswith(('skin_','brow_skin_')) or not e.get('enabled',True):continue
 extra={'estimated_pixels':e.get('estimated_pixels',False)}
 if key.startswith('hidden_hair_underlay_'):
  key='hair_'+key;extra.update(hair_angle=1.6,ownership='Estimated hidden continuation of '+e['owner'])
 for side,eye in em['eyes'].items():
  if key.endswith(side):
   prefix=key[:-(len(side)+1)]
   if prefix in eye['shader_roles']:
    extra.update(eye_role=eye['shader_roles'][prefix],eye_side=side,eye_profile=eye['profile'],eye_lower_profile=eye['lower_profile'],eye_taper_end=520 if side=='screen_left' else 713)
    for f in [eye['profile'],eye['lower_profile']]:shutil.copy2(E/f,O/f)
 add(key,(B if key.startswith('brow_') else E)/e['file'],e['xy'],e['z'],e['pivot'],**extra)
# Every seam guard follows its own hair rigid transform and sits behind all hair.
angles={'front_fringe':.6,'temple_left':1.6,'temple_right':1.6,'crown_bun_rear':.4}
for name,e in hm['layers'].items():
 if 'hidden_underlap' in e:
  u=e['hidden_underlap'];add('hair_'+name+'_underlap',H/u.get('rendered_asset',u['asset']),u['crop_origin'],60,u['pivot'],hair_angle=angles[name],estimated_pixels=True,ownership='hidden internal guard; hide together with matching visible hair')
for name,e in hm['layers'].items():
 key='hair_'+name if name in angles else name
 add(key,H/e.get('rendered_asset',e['cropped_asset']),e['crop_origin'],70 if name in angles else 80,e['pivot'],**({'hair_angle':angles[name]} if name in angles else {}))
# Original canonical neutral lips. The six oral subparts plus stationary shadow
# use their own sprites in continuous mode, never the discrete viseme renderer.
add('neutral_lips',O/'neutral_lips.png',[525,620],58,[564.5,634],source='canonical_sources/approved_neutral.png')
legacy=json.loads((R/'canonical_sources/legacy_object_face_manifest.json').read_text())
for key,e in legacy['objects'].items():
 if key.startswith('viseme_'):
  a=np.array(Image.open(R/e['source']).convert('RGBA'));a[:,:,3]=np.rint(np.clip((a[:,:,3].astype(float)-16)/239,0,1)*255).astype('uint8')
  Image.fromarray(a).crop(e['source_visible_crop']).resize(tuple(e['size']),Image.Resampling.LANCZOS).save(O/e['file'])
  m['objects'][key]=e
for folder in ['artwork','canonical_sources','assembly_sources']:
 for p in sorted((R/folder).rglob('*.png')):m['sources'][str(p.relative_to(R))]=sha(p)
m['derivation_inputs']={'hair_mask_sha256':sha(H/'full_hair_exclusion_mask.png'),'hair_manifest_sha256':sha(H/'manifest.json'),'eye_manifest_sha256':sha(E/'manifest.json')}
(O/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
def compose(hide=()):
 c=Image.new('RGBA',(1136,1384));stack=list(m['objects'].items())+[('body',m['body'])]
 for name,e in sorted(stack,key=lambda t:t[1]['z']):
  if name.startswith(('viseme_','closed_lash','lash_sweep')) or any(name.startswith(prefix) for prefix in hide):continue
  c.alpha_composite(Image.open(O/e['file']).convert('RGBA'),tuple(e['xy']))
 return c
neutral=compose();neutral.save(O/'neutral_registration_reference.png');compose(('hair_',)).save(O/'hair_hidden_reference.png');compose(('iris_','sclera_','upper_lash_','lower_contour_','brow_','neutral_lips')).save(O/'features_hidden_reference.png')
ref=np.array(Image.open(R/'canonical_sources/approved_neutral.png').convert('RGBA'));out=np.array(neutral);d=np.abs(out.astype(int)-ref.astype(int));excluded=np.zeros(d.shape[:2],bool);excluded[590:700,480:650]=True
report={'neutral_max_channel_error':int(d.max()),'neutral_changed_pixels':int(np.any(d,axis=2).sum()),'outside_mouth_max_error':int(d[~excluded].max()),'neck_roi_max_error':int(d[680:850,470:655].max()),'no_source_resize':True,'gaze_supported':False}
report['opaque_source_coverage_violations']=int(((ref[:,:,3]==255)&(out[:,:,3]<255)).sum())
assert report['opaque_source_coverage_violations']==0,'Source-opaque ownership holes'
(O/'neutral_metrics.json').write_text(json.dumps(report,indent=2)+'\n');print('CANONICAL_OBJECT_ASSETS_READY',len(m['objects']),json.dumps(report))

# Optional bounded-gaze derivatives do not replace or mutate the canonical inputs.
subprocess.run([sys.executable,str(R/"tools/build_gaze_eyes.py")],check=True)

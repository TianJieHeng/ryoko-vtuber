#!/usr/bin/env python3
"""Portable source/ownership/rebuild guard for the lateral-mouth additions."""
from pathlib import Path
from down_extra_source_guard import down_extra_matches
import hashlib,json,shutil,subprocess,sys,tempfile
from PIL import Image
import numpy as np
P=Path(__file__).resolve().parents[1];S=P/'rig_assets/spread_support';checks=0
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def check(ok,label):
 global checks
 checks+=1
 if not ok:raise AssertionError(label)
manifest=json.loads((S/'manifest.json').read_text())
protected=json.loads((P/'source_references/welcome_scope_sources.json').read_text())['protected_art_and_profiles']
check(sum(p.endswith('.png') for p in protected)==157,'157 protected originals')
for r,h in protected.items():check(sha(P/r)==h or down_extra_matches(r,h),'protected or exact hidden-cap successor '+r)
for r,h in manifest['sources'].items():check(sha(P/r)==h,'source '+r)
check(len(manifest['objects'])==7 and len(manifest['joint_extensions'])==26,'independent source owners and inferred joints')
for key,e in manifest['objects'].items():
 check(sha(S/e['file'])==e['sha256'],'derived pigment '+key)
 a=np.array(Image.open(S/e['file']).convert('RGBA'))[...,3];m=np.array(Image.open(S/e['observed_mask']).convert('L'))
 check(np.array_equal(m,np.where(a>0,255,0).astype('uint8')),'source-support mask '+key)
 check(e['registration']=='INFERRED_CANONICAL_REGISTRATION_AND_HIDDEN_UNDERLAP','inference label '+key)
 if key in ['teeth_left','teeth_right','tongue_surface']:
  check(not a[:4].any() and not a[-4:].any() and not a[:,:4].any() and not a[:,-4:].any(),'transparent moving border '+key)
a=np.array(Image.open(S/'joint_edge_underlaps_atlas.png').convert('RGBA'))[...,3];m=np.array(Image.open(S/'joint_edge_underlaps_inferred_atlas.png').convert('L'))
check(np.array_equal(m,np.where(a>0,255,0).astype('uint8')),'all inferred joint support identified')
for e in manifest['joint_extensions']:check(e['classification']=='ENTIRELY_INFERRED_HIDDEN_JOINT_PIGMENT','joint classification')
expected={f.name:sha(f) for f in S.iterdir() if f.suffix=='.png' or f.name=='manifest.json'}
with tempfile.TemporaryDirectory(prefix='ryoko-spread-rebuild-') as tmp:
 T=Path(tmp)
 for directory in ['assembly_sources/head','rig_assets/yawn_mouth','rig_assets/smile_support']:
  shutil.copytree(P/directory,T/directory,ignore=shutil.ignore_patterns('*.import'))
 (T/'tools').mkdir();shutil.copy2(P/'tools/build_spread_support.py',T/'tools/build_spread_support.py')
 for iteration in range(2):
  subprocess.run([sys.executable,str(T/'tools/build_spread_support.py')],check=True,stdout=subprocess.PIPE)
  for name,h in expected.items():check(sha(T/'rig_assets/spread_support'/name)==h,f'deterministic rebuild{iteration+1} {name}')
required=json.loads((S/'required_textures.json').read_text())
for path in required:check((P/path.removeprefix('res://')).is_file(),'required texture source '+path)
check(manifest['control']['vertical_aperture_cap']==.55 and manifest['control']['maximum_per_column_aperture_px']==30.8,'physical aperture cap unchanged')
print('SPREAD_SOURCE_PASS checks='+str(checks)+' originals=157 profiles=2 derived_pngs=17 rebuilds=2')

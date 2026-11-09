#!/usr/bin/env python3
"""Reproducible yawn source/ownership architecture gates, not visual approval."""
import json,hashlib,subprocess,sys
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1];m=json.loads((R/'rig_assets/yawn_mouth/manifest.json').read_text());checks=0
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for path,h in m['sources'].items():assert sha(R/path)==h,path;checks+=1
for name,e in m['objects'].items():
 im=Image.open(R/'rig_assets/yawn_mouth'/e['file']);assert im.mode=='RGBA' and list(im.size)==e['size'];checks+=1
for name in ['upper_lip','lower_lip','underlip_shadow']:
 import numpy as np
 a=np.array(Image.open(R/'rig_assets/yawn_mouth'/f'{name}.png'));source=np.array(Image.open(R/'rig_assets/object_face/neutral_lips.png'))
 assert np.array_equal(a[:,:,:3],source[:,:,:3]);checks+=1
 assert np.all(a[:,:,3]<=source[:,:,3]);checks+=1
before={p.name:sha(p) for p in (R/'rig_assets/yawn_mouth').glob('*') if p.suffix in ['.png','.json']}
subprocess.run([sys.executable,str(R/'tools/build_yawn_mouth.py')],check=True,capture_output=True)
after={p.name:sha(p) for p in (R/'rig_assets/yawn_mouth').glob('*') if p.suffix in ['.png','.json']};assert before==after;checks+=1
shader=(R/'object_mouth_clip.gdshader').read_text();assert 'texture(TEXTURE,UV)' in shader;checks+=1
for token in ['UV+=','UV +=','MeshInstance2D','AnimationPlayer','modulate.a=','scale=Vector2(']:
 assert token not in (R/'object_face.gd').read_text(),token;checks+=1
p=json.loads((R/'yawn_performance.json').read_text());assert p['id']=='EXP-163' and len(p['keyframes'])==13 and p['duration']==5.8;checks+=1
assert p['keyframes'][0]['values']==p['keyframes'][-1]['values'];checks+=1
print(json.dumps({'status':'pass','checks':checks,'oral_sources':len(m['sources']),'oral_objects':len(m['objects']),'deterministic_derivatives':len(before),'active_performances':['EXP-163'],'user_approval':'pending'},indent=2))

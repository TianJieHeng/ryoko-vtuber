#!/usr/bin/env python3
"""Focused reference-cap, tooth-white and unchanged-art regression checks."""
from pathlib import Path
import hashlib,json
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parents[1]
identity=json.loads((R/'validation/mouth_limit_baseline_identity.json').read_text());checks=0
# The only deliberate identity exception is the default application entry point.
# Historical baseline hashes remain intact; all artwork/rendering hashes still apply.
app_migrations=[]
for name,expected in identity['unchanged_files'].items():
 if name=='project.godot':
  config=(R/name).read_text()
  assert 'run/main_scene="res://expression_viewer.tscn"' in config
  app_migrations.append(name);checks+=1;continue
 assert hashlib.sha256((R/name).read_bytes()).hexdigest()==expected,name;checks+=1
m=json.loads((R/'rig_assets/yawn_mouth/manifest.json').read_text())
assert m['objects']['upper_teeth']['xy']==[533,626];checks+=1
assert m['objects']['upper_teeth']['size']==[64,14];checks+=1
assert m['mouth_limit']['effective_aperture_cap']==.55;checks+=1
assert m['mouth_limit']['max_aperture_source_px']==30.8;checks+=1
reports={}
for name in ['upper_teeth','lower_teeth']:
 old=np.array(Image.open(R/'source_references'/('pre_whitening_'+name+'.png')))
 a=np.array(Image.open(R/'rig_assets/yawn_mouth'/(name+'.png')))
 assert a.shape==old.shape;checks+=1
 assert np.array_equal(a[:,:,3],old[:,:,3]);checks+=1
 assert np.array_equal(a[:,:,0],a[:,:,1]) and np.array_equal(a[:,:,1],a[:,:,2]);checks+=1
 luma=old[:,:,:3].astype(float)@np.array([.2126,.7152,.0722]);expected=np.rint(np.clip(135+.5*luma,0,255)).astype('uint8')
 assert np.array_equal(a[:,:,0][a[:,:,3]>0],expected[a[:,:,3]>0]);checks+=1
 visible=a[:,:,0][a[:,:,3]>128];assert np.median(visible)>=245;checks+=1
 assert np.percentile(visible,5)<235 and visible.max()-visible.min()>30;checks+=1
 reports[name]={'opaque_rgb_median':[float(np.median(visible))]*3,'p05':float(np.percentile(visible,5)),'max':int(visible.max()),'alpha_identical':True}
print(json.dumps({'status':'pass','checks':checks,'unchanged_pngs':identity['unchanged_png_count'],'unchanged_runtime_and_art_files':len(identity['unchanged_files'])-len(app_migrations),'explicit_app_migrations':app_migrations,'static_upper_teeth_xy':[533,626],'effective_aperture_cap':.55,'tooth_whitening':reports},indent=2))

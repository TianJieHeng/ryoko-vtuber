#!/usr/bin/env python3
"""Deterministic base architecture/source gates; visual QA remains separate."""
from pathlib import Path
import json,hashlib
from PIL import Image
R=Path(__file__).resolve().parents[1]
m=json.loads((R/'rig_assets/object_face/manifest.json').read_text());p=json.loads((R/'SOURCE_PROVENANCE.json').read_text());checks=0
for path,entry in p['sources'].items():
 assert hashlib.sha256((R/path).read_bytes()).hexdigest()==entry['sha256'],path;checks+=1
for name,e in m['objects'].items():
 im=Image.open(R/'rig_assets/object_face'/e['file']);assert im.mode=='RGBA' and list(im.size)==e['size'],name;checks+=1
hair=[n for n in m['objects'] if n.startswith('hair_')];assert len(hair)==6;checks+=1
for name in ['stationary_backing','ear_screen_left','ear_screen_right','brow_screen_left','brow_screen_right','iris_screen_left','iris_screen_right','neutral_lips']:
 assert m['objects'][name]['source'].startswith('assembly_sources/'),name;checks+=1
main=(R/'project.godot').read_text();assert 'run/main_scene="res://object_rig.tscn"' in main;checks+=1
for file in ['object_rig.gd','object_face.gd','object_eye_clip.gdshader']:
 text=(R/file).read_text()
 for token in ['MeshInstance2D','SubViewport','expression_uv','motion_deform','facial_controller.gd','expression_performance.gd','expression_performances.json']:
  assert token not in text,(file,token);checks+=1
assert not (R/'expression_performances.json').exists();checks+=1
assert not (R/'motion_rig.gd').exists();checks+=1
assert len(json.loads((R/'legacy_expression_ids.json').read_text())['legacy_expression_ids'])==93;checks+=1
print(json.dumps({'status':'pass','checks':checks,'immutable_source_files':len(p['sources']),'clean_hair_objects':len(hair),'active_expression_timelines':0,'visual_review_required':True},indent=2))

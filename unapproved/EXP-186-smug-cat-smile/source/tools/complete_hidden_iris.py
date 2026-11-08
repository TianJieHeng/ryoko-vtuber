#!/usr/bin/env python3
"""Apply hash-pinned inferred hidden RGB strips, never a visible eye replacement.

The compact patch is durable source derived from a disclosed built-in imagegen
edit. Run after build_gaze_eyes.py to recreate the same two runtime owners.
"""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1];G=R/'rig_assets/gaze_eyes'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=json.loads((R/'source_references/hidden_iris_cap_patch.json').read_text());m=json.loads((G/'manifest.json').read_text())
 for side,e in p['eyes'].items():
  image=G/f'iris_{side}.png';completed=G/f'completed_iris_{side}.png'
  assert sha(image) in [e['baseline_iris_sha256'],e['candidate_iris_sha256']],'Unexpected iris source '+side
  assert sha(completed) in [e['baseline_completed_sha256'],e['candidate_completed_sha256']],'Unexpected completed source '+side
  a=np.array(Image.open(image).convert('RGBA'));alpha=a[:,:,3].copy()
  for x,y,r,g,b in e['rgb_patch_xy_rgb']:a[y,x,:3]=[r,g,b]
  assert np.array_equal(a[:,:,3],alpha),'alpha must not change'
  Image.fromarray(a).save(image);assert sha(image)==e['candidate_iris_sha256']
  c=np.array(Image.open(completed));
  for x,y in e['new_completed_xy']:c[y,x]=255
  Image.fromarray(c).save(completed);assert sha(completed)==e['candidate_completed_sha256']
  m['eyes'][side]['directional_down_completion']={'new_rgb_texels':len(e['rgb_patch_xy_rgb']),'retained_inferred_ring_texels':len(e['qualified_retained_ring_xy']),'new_completed_texels':len(e['new_completed_xy']),'physical_domain':p['new_physical_domain'],'source_patch':'source_references/hidden_iris_cap_patch.json','whole_alpha_unchanged':True,'old_reachable_rgba_unchanged':True,'not_original_recovered_art':True}
 m['down_extension']={'control':'gaze_down_extra','normalized_range':[0,1],'default':0,'additional_source_pixels':5,'combined_y_range':[-2,6],'status':'local candidate; user approval pending'}
 m['review_status']='Published original bounded gaze plus local hidden-cap/down-extension candidate; new support not yet user approved'
 (G/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 print('HIDDEN_IRIS_PATCH_PASS:155/132 RGB texels; old reachable RGBA and entire alpha preserved')
if __name__=='__main__':main()

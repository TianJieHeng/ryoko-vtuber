#!/usr/bin/env python3
"""Portable source/provenance guard. Does not imply visual acceptance."""
from pathlib import Path
import hashlib,json,re,shutil,subprocess,sys,tempfile
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
checks=0
def check(ok,label):
 global checks
 assert ok,label
 checks+=1
baseline=json.loads((P/'source_references/giggle_parent_inventory.json').read_text())['files']
original={p:h for p,h in baseline.items() if p.endswith('.png')}
check(len(original)==174,'174 parent PNG hashes')
check(len(list((P/'rig_assets/pressed_lip_support').glob('*.png')))==2,'two inferred pressed-lip PNGs')
for p,h in original.items():check(sha(P/p)==h,'original PNG: '+p)
for p in ['yawn_performance.json','expressions/EXP-005.json','expressions/EXP-001.json']:
 check(sha(P/p)==baseline[p],'unchanged parent profile '+p)
support=P/'rig_assets/pressed_lip_support';m=json.loads((support/'manifest.json').read_text())
check(m['classification']=='ENTIRELY_INFERRED_HIDDEN_INNER_UPPER_LIP_UNDERLAP','explicit inferred provenance')
check(m['control']['maximum_depth_source_px']==4 and m['control']['outer_lip_translation']==0 and m['control']['teeth_translation']==0,'bounded depth and fixed outer lip/enamel')
for name,key in [('source','source_sha256'),('seam','seam_sha256')]:check(sha(P/m[name])==m[key],name+' provenance')
for name,key in [('pigment_file','pigment_sha256'),('inferred_mask','inferred_mask_sha256')]:check(sha(support/m[name])==m[key],name+' provenance')
a=np.array(Image.open(P/m['source']).convert('RGBA'));p=np.array(Image.open(support/m['pigment_file']).convert('RGBA'));mask=np.array(Image.open(support/m['inferred_mask']).convert('L'))
check(np.array_equal(mask>0,p[:,:,3]>0),'mask covers every inferred pixel')
expected=np.zeros_like(p)
for record in m['source_samples']:
 x=record['column'];sx,sy=record['sample_xy'];top,bottom=record['hidden_y_range']
 check(a[sy,sx,3]>64 and sx==x,'covered same-column observed pigment')
 expected[top:bottom,x,:3]=a[sy,sx,:3];expected[top:bottom,x,3]=255
check(np.array_equal(p,expected),'all continuation pixels follow provenance samples')
original_hashes={f.name:sha(f) for f in support.iterdir() if f.suffix in {'.png','.json'}}
with tempfile.TemporaryDirectory(prefix='ryoko-closed-smile-') as tmp:
 root=Path(tmp);(root/'tools').mkdir();(root/'rig_assets/pressed_lip_support').mkdir(parents=True)
 shutil.copy2(P/'tools/build_pressed_lip_support.py',root/'tools/build_pressed_lip_support.py')
 for f in [m['source'],m['seam']]:
  (root/f).parent.mkdir(parents=True,exist_ok=True);shutil.copy2(P/f,root/f)
 for i in range(2):
  subprocess.run([sys.executable,str(root/'tools/build_pressed_lip_support.py')],check=True,capture_output=True)
  check({f.name:sha(f) for f in (root/'rig_assets/pressed_lip_support').iterdir()}==original_hashes,'deterministic rebuild '+str(i))
shader=(P/'pressed_lip_clip.gdshader').read_text()
check('texture(TEXTURE,UV)' in shader and not re.search(r'\b(?:VERTEX|UV)\s*[+*/-]?=',shader),'fixed pigment UV and no mesh deformation')
check(bool(re.search(r'float depth\s*=\s*4\.0\*lip_press',shader)),'4px shader bound')
check('lowering' not in (P/'object_face.gd').read_text().lower(),'rejected lowering absent')
print(f'CLOSED_SMILE_SOURCE_PASS checks={checks} original_pngs=174 pressed_lip_pngs=2 protected_profiles=3 deterministic_rebuilds=2 visual_approval=false')

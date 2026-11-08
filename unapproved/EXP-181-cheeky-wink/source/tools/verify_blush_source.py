#!/usr/bin/env python3
"""Rebuild fixed source FX and verify provenance. Not a visual-review substitute."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parents[1];F=P/'rig_assets/blush_support';checks=0
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def check(ok,label):
 global checks
 checks+=1;assert ok,label
m=json.loads((F/'manifest.json').read_text());check(len(m['objects'])==2,'two independent FX objects')
for name,h in m['source_originals_retained'].items():check(sha(F/'source_originals'/name)==h,'original FX '+name)
for key,e in m['objects'].items():
 check(e['runtime_scale']==[1,1] and e['runtime_rotation']==0 and e['z']==29,'fixed transform '+key)
 check(sha(F/e['file'])==e['sha256'],'texture '+key)
 check(sha(F/e['mask']['file'])==e['mask']['sha256'],'mask '+key)
 a=np.array(Image.open(F/e['file']).convert('RGBA'));mask=np.array(Image.open(F/e['mask']['file']))
 check(np.all((a[:,:,3]>0)<=(mask>0)),'mask confinement '+key)
 check(np.all(a[a[:,:,3]==0]==0),'transparent cleanup '+key)
check(sha(F/'build_registered_blush.py')==m['builder']['sha256'],'builder hash')
with tempfile.TemporaryDirectory(prefix='ryoko-blush-') as tmp:
 root=Path(tmp)/'rig';shutil.copytree(P,root,ignore=shutil.ignore_patterns('.godot','__pycache__'))
 f=root/'rig_assets/blush_support';expected={str(p.relative_to(F)):sha(p) for p in F.rglob('*.png')}
 for i in range(2):
  subprocess.run([sys.executable,str(f/'build_registered_blush.py')],cwd=root,check=True,capture_output=True)
  for name,h in expected.items():check(sha(f/name)==h,'repeat rebuild '+str(i)+' '+name)
print(f'BLUSH_SOURCE_PASS checks={checks} originals=2 runtime=2 masks=2 rebuilds=2')

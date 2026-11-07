#!/usr/bin/env python3
"""Portable source/ownership checks; visual and render checks remain separate."""
import hashlib,json,re,subprocess,sys
from pathlib import Path
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parents[1];checks=0
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def check(ok,label):
 global checks
 checks+=1
 if not ok:raise AssertionError(label)
g=json.loads((P/'validation/smile_source_guard.json').read_text())
for name,digest in g['original_pngs'].items():check(sha(P/name)==digest,'original PNG '+name)
check(sha(P/'yawn_performance.json')==g['yawn_performance_sha256'],'yawn values/timing unchanged')
for name,digest in g['original_smile_donor_sha256'].items():check(sha(P/name)==digest,'extracted source '+name)
face=(P/'object_face.gd').read_text()
for function,digest in g['mouth_functions'].items():
 block=re.search(rf'^func {function}\(.*?(?=^func |\Z)',face,re.M|re.S)
 check(block is not None,function)
 check(hashlib.sha256(block.group(0).encode()).hexdigest()==digest,'existing mouth function '+function)
check('const MAX_MOUTH_APERTURE=0.55' in face,'physical limit')
for f in ['object_face.gd','expression_rig.gd']:
 check('EXP-005' not in (P/f).read_text(),'no expression-specific dispatch '+f)
 check('Tween' not in (P/f).read_text(),'no stale tween owner '+f)
m=json.loads((P/'rig_assets/smile_support/manifest.json').read_text())
atlas=Image.open(P/'rig_assets/smile_support/lip_continuations_atlas.png').convert('RGBA')
mask=Image.open(P/'rig_assets/smile_support/lip_continuations_inferred_atlas.png').convert('L')
for e in m['lip_continuations']:
 x,y,w,h=e['atlas_rect'];part=atlas.crop((x,y,x+w,y+h));a=np.array(part)[:,:,3];support=np.array(mask.crop((x,y,x+w,y+h)))
 check(hashlib.sha256(part.tobytes()).hexdigest()==e['region_rgba_sha256'],'fixed native atlas region '+e['name'])
 check(int((a>0).sum())==e['nontransparent_pixels'],'quantized alpha count '+e['name'])
 check(np.all(support[a>0]>0),'inference mask covers all continuation '+e['name'])
 check(e['classification']=='ENTIRELY_INFERRED_HIDDEN_JOINT_PIGMENT','explicit inference '+e['name'])
check(len(m['lip_continuations'])==26,'separate join owner count')
check(m['fringe_reassignment']['core_pixels']==10 and m['fringe_reassignment']['retained_edge_pixels']==5,'fringe ownership bounds')
check(m['residue_review']['reassigned_source_core_pixels']==42,'backing ownership bounds')
check(sha(P/'rig_assets/yawn_mouth/upper_lip.png')==sha(P/'rig_assets/yawn_mouth/lower_lip.png'),'legacy shared full-lip source')
mouth=json.loads((P/'rig_assets/yawn_mouth/manifest.json').read_text())
check(mouth['objects']['upper_teeth']['xy']==[533,626],'tooth anchor')
reference=json.loads((P/'source_references/expression_catalogue_93.json').read_text())
check(len(reference['entries'])==93 and len({e['id'] for e in reference['entries']})==93,'93 reference IDs preserved')
registry=json.loads((P/'expressions/registry.json').read_text())
check({e['id'] for e in registry['entries']}=={'EXP-005','EXP-163'},'only two actual shared performances')
old=json.loads((P/'source_references/historical_EXP005_expression_performances.json').read_text())['profiles']['EXP-005']
new=json.loads((P/'expressions/EXP-005.json').read_text())
check([k['time'] for k in old['keyframes']]==[k['time'] for k in new['keyframes']],'fifteen semantic timing keys')
check(new['duration']==5.4,'duration')
# Rebuild only the derived smile outputs, twice, from immutable local sources.
def output_hashes():return {p.name:sha(p) for p in (P/'rig_assets/smile_support').iterdir() if p.suffix in ['.png','.json']}
before=output_hashes()
for i in range(2):
 subprocess.run([sys.executable,str(P/'tools/build_smile_support.py')],check=True,stdout=subprocess.DEVNULL)
 check(output_hashes()==before,'byte-identical smile rebuild '+str(i+1))
print(json.dumps({'status':'pass','checks':checks,'original_pngs':len(g['original_pngs']),'authored_performances':['EXP-163','EXP-005'],'historical_reference_ids':93,'separate_continuation_owners':26,'atlas_files':2,'visual_acceptance':'Separate actual-Godot frame/video review required.'},indent=2))

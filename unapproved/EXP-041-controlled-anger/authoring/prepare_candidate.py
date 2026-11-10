import hashlib,json,shutil
from pathlib import Path
W=Path(__file__).resolve().parent; ROOT=W.parent
source=ROOT/'approved36_integration_work/ryoko_object_rig'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((source/'APPROVED_SOURCE_MANIFEST.json').read_text()); files=m['files']
assert len(files)==999 and sum(n.endswith('.png') for n in files)==184
for n,v in files.items():
 assert h(source/n)==v,n
 dst=W/'rig'/n;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source/n,dst)
extra={}
for n in ['APPROVED_SOURCE_MANIFEST.json','PUBLICATION_SOURCE_MANIFEST.json']:
 if n not in files:shutil.copy2(source/n,W/'rig'/n);extra[n]=h(source/n)
ids=[r['id'] for r in json.loads((source/'expressions/registry.json').read_text())['entries']]
assert len(ids)==36 and 'EXP-041' not in ids
ref=ROOT/'insight_integration_work/avatar_build_assets/reference_library'; sheet=ref/'assets/expressions/EXP-041_controlled-anger/RYO_EXP-041_controlled-anger_sheet_v001.png';cat=ref/'metadata/expressions.json'
freeze=dict(baseline='approved36',baseline_profile_count=36,published_baseline_commit='3ce98774282ad6c20dfbd7018d20838ff861b762',source_rig=str(source),source_files=999,source_png_files=184,source_files_sha256=files,extra_manifests_sha256=extra,baseline_profile_ids=ids,source_sheet=str(sheet),source_sheet_sha256=h(sheet),source_catalogue=str(cat),catalogue_sha256=h(cat))
(W/'BASELINE_FREEZE.json').write_text(json.dumps(freeze,indent=2)+'\n')
def pose(b,t,l,p):return dict(brow_screen_left=b,brow_screen_right=b,brow_tilt_screen_left=t,brow_tilt_screen_right=-t,blink_L=l,blink_R=l,mouth_lip_press=p)
poses={'neutral':{},'restrain':pose(-.18,.18,.06,.24),'gather':pose(-.42,.4,.16,.42),'controlled_anger':pose(-.7,.65,.26,.65),'ease_pressure':pose(-.7,.65,.26,.38),'soften':pose(-.3,.28,.12,.22),'settle':pose(-.08,.08,.03,.06),'neutral_return':{}}
(W/'plan.json').write_text(json.dumps([dict(name=k,pose=v) for k,v in poses.items()],indent=2)+'\n')
keys=[(0,'neutral'),(.2,'neutral'),(.6,'restrain'),(.95,'gather'),(1.35,'controlled_anger'),(2.1,'controlled_anger'),(2.55,'ease_pressure'),(3,'soften'),(3.35,'settle'),(3.7,'neutral_return'),(4,'neutral_return')]
d=dict(id='EXP-041',title='Controlled anger',duration=4.0,status='UNAPPROVED shared-rig preparation v1; native visual review pending',intent='Brows draw inward and down by rigid approximation, eyes narrowly fixed, lips pressed straight and restrained.',scope='Existing symmetric brow lowering and opposing rigid tilt, ordinary symmetric lid closure and sealed lip pressure only. No horizontal brow convergence is available; no new anatomy, artwork, runtime, gaze, head or body movement.',timing_origin='New four-second interpretation of nine inspected static source panels, not recovered motion. Measured onset and held restrained peak, then lip pressure eases before the brow and lid release. Cold Glare has zero tilt and purse; Silent Fury has neutral lids and maximum tilt/press. This candidate instead combines moderate tilt and pressure with narrow fixed eyes.',interpolation='Unchanged shared smoothstep; eight static anchors, eleven timeline keys, exact neutral bookends, in-memory registration only.',source_catalogue_sha256=h(cat),keyframes=[dict(time=t,phase=p,values=poses[p]) for t,p in keys])
(W/'EXP-041.json').write_text(json.dumps(d,indent=2)+'\n')
(W/'SOURCE_REFERENCE.json').write_text(json.dumps(dict(sheet=str(sheet),sha256=h(sheet),pixels_inspected=True,observations='Nine frontal panels: brows progressively angle down toward center, eyes narrow while maintaining forward gaze, lips remain thin and closed. Mid-row has strongest brow tension. Final row softens. No added body, head or gaze beat is warranted. Existing rigid brows approximate the inward/down cue without horizontal convergence.',approval='Historical approved sprite-composite art exists. It does not approve this new shared-rig animation.'),indent=2)+'\n')
print('Prepared 999 pinned files, 184 PNGs; candidate outside production registry.')

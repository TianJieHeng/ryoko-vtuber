import hashlib,json,shutil
from pathlib import Path
W=Path(__file__).resolve().parent; ROOT=W.parent
source=ROOT/'approved36_integration_work/ryoko_object_rig';h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
files=json.loads((source/'APPROVED_SOURCE_MANIFEST.json').read_text())['files']
assert len(files)==999 and sum(n.endswith('.png') for n in files)==184
for n,v in files.items():
 assert h(source/n)==v,n
 dst=W/'rig'/n;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source/n,dst)
extra={}
for n in ['APPROVED_SOURCE_MANIFEST.json','PUBLICATION_SOURCE_MANIFEST.json']:
 if n not in files:shutil.copy2(source/n,W/'rig'/n);extra[n]=h(source/n)
ids=[r['id'] for r in json.loads((source/'expressions/registry.json').read_text())['entries']]
assert len(ids)==36 and 'EXP-061' not in ids
ref=ROOT/'insight_integration_work/avatar_build_assets/reference_library';cat=ref/'metadata/expressions.json'
catalogue=json.loads(cat.read_text()); rows=catalogue if isinstance(catalogue,list) else next(v for v in catalogue.values() if isinstance(v,list) and any(isinstance(r,dict) and r.get('id')=='EXP-061' for r in v))
entry=next(r for r in rows if r['id']=='EXP-061');sheet=ref/entry['asset_production']['actual_path'];assert h(sheet)==entry['asset_production']['sha256']
freeze=dict(baseline='approved36',baseline_profile_count=36,published_baseline_commit='3ce98774282ad6c20dfbd7018d20838ff861b762',source_rig=str(source),source_files=999,source_png_files=184,source_files_sha256=files,extra_manifests_sha256=extra,baseline_profile_ids=ids,source_sheet=str(sheet),source_sheet_sha256=h(sheet),source_catalogue=str(cat),catalogue_sha256=h(cat))
(W/'BASELINE_FREEZE.json').write_text(json.dumps(freeze,indent=2)+'\n')
def pose(b,e,m,p,press):return dict(brow_screen_left=b,brow_screen_right=b,opening_px=e,mouth_open=m,mouth_purse=p,mouth_lip_press=press)
poses={'neutral':{},'notice':pose(.2,.8,.08,.08,.08),'rise':pose(.55,2,.4,.18,.2),'broad_surprise':pose(1,4,.95,.32,.35),'held_surprise':pose(.9,3.7,.85,.28,.3),'release':pose(.35,1.5,.28,.1,.1),'soften':pose(.1,.4,.06,.03,.02),'neutral_return':{}}
(W/'plan.json').write_text(json.dumps([dict(name=k,pose=v) for k,v in poses.items()],indent=2)+'\n')
keys=[(0,'neutral'),(.2,'neutral'),(.5,'notice'),(.9,'rise'),(1.35,'broad_surprise'),(1.85,'broad_surprise'),(2.35,'held_surprise'),(2.85,'release'),(3.25,'soften'),(3.7,'neutral_return'),(4,'neutral_return')]
d=dict(id='EXP-061',title='Broad surprise',duration=4.0,status='UNAPPROVED preparation v1; native visual review pending',intent=entry['distinctive_facial_intent'],scope='Partial reference fit: existing symmetric whole-brow vertical lift, bounded four-source-pixel upper-eye opening, split-lip opening, purse and lip pressure only. No jaw rotation/drop, lower-eye expansion, pupil change or new anatomy. Broad rounded aperture is approximated with less purse than Shocked Gasp; no smile/spread or delight conversion. Head/body stay fixed; no runtime/art changes.',timing_origin='New four-second interpretation of inspected nine static reference panels, not recovered animation. Gradual whole-brow rise to held broad aperture 1.35-1.85, slowly eases to 2.35, then releases. Unlike EXP064 fast inner-brow intake and smaller residual gasp; unlike EXP004 round-to-spread smile.',interpolation='Unchanged smoothstep, eight static anchors, eleven timeline keys, exact neutral bookends, in-memory registration only.',source_catalogue_sha256=h(cat),keyframes=[dict(time=t,phase=p,values=poses[p]) for t,p in keys])
(W/'EXP-061.json').write_text(json.dumps(d,indent=2)+'\n')
(W/'SOURCE_REFERENCE.json').write_text(json.dumps(dict(sheet=str(sheet),sha256=h(sheet),pixels_inspected=True,catalogue_entry=entry,observations='Inspected 1254x1254 nine-panel sheet. Neutral first panels; bilateral whole brow rise and round opening build through panel 4, peak panel 5, soften panel 6, release panels 7-9. Current rig cannot reproduce jaw/chin silhouette or full eye expansion. New timing is authored, not reference animation.',comparison={'EXP-064':'Fast inner-brow rotation with fixed outer anchors, .9 mouth and .7 purse, .66 peak. This candidate uses whole-brow vertical travel, .95 mouth and .32 purse, 1.35 peak and sustained broad opening. Shared open-surprise vocabulary means distinctness remains visual-review pending.','EXP-004':'Round discovery becomes spread smile; this candidate has zero smile and spread throughout.'},approval='Accepted reference art does not approve the candidate'),indent=2)+'\n')
print('Prepared 999 pinned source files, 184 PNGs, 36 approved profiles; candidate unregistered.')

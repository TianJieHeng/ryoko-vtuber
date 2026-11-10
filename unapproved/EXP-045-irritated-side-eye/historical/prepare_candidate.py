"""Prepare EXP-045 outside the immutable approved36 runtime and registry."""
import hashlib,json,shutil
from pathlib import Path
W=Path(__file__).resolve().parent; ROOT=W.parent
source=ROOT/'approved36_integration_work/ryoko_object_rig'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
write=lambda p,d:p.write_text(json.dumps(d,indent=2)+'\n')
assert not (W/'rig').exists(),'Do not overwrite a prepared rig.'
files=json.loads((source/'APPROVED_SOURCE_MANIFEST.json').read_text())['files']
assert len(files)==999 and sum(n.endswith('.png') for n in files)==184
for n,v in files.items():
 assert h(source/n)==v,n
 dst=W/'rig'/n;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source/n,dst)
extra={}
for n in ['APPROVED_SOURCE_MANIFEST.json','PUBLICATION_SOURCE_MANIFEST.json']:
 if n not in files:shutil.copy2(source/n,W/'rig'/n);extra[n]=h(source/n)
ids=[r['id'] for r in json.loads((source/'expressions/registry.json').read_text())['entries']]
assert len(ids)==36 and 'EXP-045' not in ids
ref=ROOT/'insight_integration_work/avatar_build_assets/reference_library';cat=ref/'metadata/expressions.json'
entry=next(r for r in json.loads(cat.read_text())['expressions'] if r['id']=='EXP-045')
sheet=ref/entry['asset_production']['actual_path'];assert h(sheet)==entry['asset_production']['sha256']
for p in entry['key_pose_sequence']:assert h(ref/p['actual_panel_path'])==p['sha256']
excluded=['APPROVED_INTEGRATION_STATUS.json','APPROVED_INTEGRATION_TEST_RESULTS.json','README.md','RELEASE.json','expressions/registry.json','tools/verify_approved_integration.py']
parity={n:v for n,v in files.items() if n not in excluded};current=ROOT/'approved41_integration_work/ryoko_object_rig'
for n,d in parity.items():assert h(current/n)==d,n
freeze=dict(baseline='approved36',baseline_profile_count=36,published_baseline_commit='3ce98774282ad6c20dfbd7018d20838ff861b762',source_rig=str(source),source_files=999,source_png_files=184,source_files_sha256=files,extra_manifests_sha256=extra,baseline_profile_ids=ids,source_sheet=str(sheet),source_sheet_sha256=h(sheet),source_catalogue=str(cat),catalogue_sha256=h(cat),published41_runtime_artwork_parity=dict(path=str(current),files_sha256=parity,count=len(parity),excluded_changed_metadata_registry_and_aggregate_guard=excluded))
write(W/'BASELINE_FREEZE.json',freeze);write(W/'SOURCE_CATALOGUE_ENTRY.json',entry)
def pose(bl,br,tl,tr,ll,lr,av):
 return dict(brow_screen_left=bl,brow_screen_right=br,brow_tilt_screen_left=tl,brow_tilt_screen_right=tr,blink_R=ll,blink_L=lr,aversion_px=av)
poses={'neutral':{},'prepare_lids':pose(-.2,.05,.15,-.1,.24,.22,0),'glance':pose(-.4,.12,.3,-.2,.30,.28,6),'side_eye_peak':pose(-.65,.22,.5,-.28,.38,.30,12),'recover_gaze':pose(-.45,.14,.35,-.2,.32,.28,5),'center_gaze':pose(-.22,.06,.18,-.10,.24,.22,0),'settle':pose(-.05,.015,.04,-.02,.06,.05,0),'neutral_return':{}}
keys=[(0,'neutral'),(.2,'neutral'),(.6,'prepare_lids'),(1.,'glance'),(1.6,'side_eye_peak'),(2.4,'side_eye_peak'),(2.8,'recover_gaze'),(3.2,'center_gaze'),(3.5,'settle'),(3.7,'neutral_return'),(4.,'neutral_return')]
write(W/'plan.json',[dict(name=k,pose=v) for k,v in poses.items()])
write(W/'EXP-045.json',dict(id='EXP-045',title='Irritated Side-eye',duration=4.0,status='UNAPPROVED shared-rig preparation v1; independent source and native visual review pending',intent=entry['distinctive_facial_intent'],scope='Existing positive screen-right aversion, unequal ordinary upper-lid closure and unequal opposed rigid brow translation/tilt. Mouth remains sealed and unmodified: independent downturned corner is unavailable and is not faked by an upward sneer or symmetric purse. No new anatomy, art, runtime, shader, production registry, head/body motion, ordinary gaze, opening, smile-eye, smile, blush, speech or effects.',timing_origin='New four-second interpretation of the inspected static EXP-045 sheet, not recovered motion. Establish narrowed lids at .6 before the deliberate screen-right glance, build to an unequal-brow irritated hold at 1.6-2.4, then return gaze fully to center at 3.2 before releasing its supporting lids. Distinct from EXP-042 frontal cold glare, EXP-081 asymmetric mouth disgust and EXP-144 alert/embarrassed glance-away. Missing independent downturned mouth corner is disclosed rather than substituted.',interpolation='Unchanged shared smoothstep; eight static anchors, eleven timeline keys, exact neutral bookends. Candidate and static probes are registered only in memory. Every aversion-active adjoining segment keeps both lid endpoints at least .18; ordinary gaze, eye-smile and opening remain zero.',source_catalogue_sha256=h(cat),keyframes=[dict(time=t,phase=p,values=poses[p]) for t,p in keys]))
write(W/'SOURCE_REFERENCE.json',dict(sheet=str(sheet),sha256=h(sheet),dimensions=[1159,1358],pixels_inspected=True,observations='Actual full nine-panel sheet viewed before authoring. Panels 2-5 narrow the upper lids and deliberately shift both irises toward screen-right. The screen-left brow is lower with inward downward inclination while the screen-right brow is relatively raised with an opposing tilt. A sealed restrained mouth develops a downturned corner, then gaze and facial tension recover across panels 7-9. Sheet does not show the initial wide-eyed startle, blushing or downcast embarrassment of Caught staring.',left_right_convention='Brow names use screen sides. blink_R closes screen-left and blink_L closes screen-right. Positive aversion_px moves both original iris sprites and iris/sclera shader offsets toward screen-right in source pixels.',approximation='The independent downturned mouth corner cannot be represented by the frozen controls. All mouth channels stay exactly neutral and sealed; no upward sneer, symmetric purse or fake corner depression is introduced. Peak uses 12 source pixels of rightward aversion (5.88 bust pixels), .38/.30 lid closure (13.68/10.8 source-pixel lash travel), -0.65/+0.22 brow translation (6.5 pixels down/2.2 up) and +.50/-.28 tilt (+4/-2.24 degrees). Rigid brows cannot reproduce every drawn contour. Native fidelity and distinctness remain pending.',panel_hashes={p['actual_panel_path']:p['sha256'] for p in entry['key_pose_sequence']},approval='Accepted reference art does not approve this candidate or animation.'))
print('Prepared unapproved EXP-045 against frozen approved36: 999 files, 184 PNGs; 993 runtime/artwork files equal approved41.')

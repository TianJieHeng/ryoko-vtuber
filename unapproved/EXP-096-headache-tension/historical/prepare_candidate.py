"""Prepare an isolated EXP-096 candidate; never edit baseline or production files."""
import hashlib,json,shutil
from pathlib import Path
W=Path(__file__).resolve().parent;ROOT=W.parent
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
assert len(ids)==36 and 'EXP-096' not in ids
ref=ROOT/'insight_integration_work/avatar_build_assets/reference_library';cat=ref/'metadata/expressions.json'
entry=next(r for r in json.loads(cat.read_text())['expressions'] if r['id']=='EXP-096')
sheet=ref/entry['asset_production']['actual_path'];assert h(sheet)==entry['asset_production']['sha256']
for p in entry['key_pose_sequence']:assert h(ref/p['actual_panel_path'])==p['sha256']
excluded=['APPROVED_INTEGRATION_STATUS.json','APPROVED_INTEGRATION_TEST_RESULTS.json','README.md','RELEASE.json','expressions/registry.json','tools/verify_approved_integration.py']
parity={n:v for n,v in files.items() if n not in excluded};current=ROOT/'approved41_integration_work/ryoko_object_rig'
for n,d in parity.items():assert h(current/n)==d,n
freeze=dict(baseline='approved36',baseline_profile_count=36,published_baseline_commit='3ce98774282ad6c20dfbd7018d20838ff861b762',source_rig=str(source),source_files=999,source_png_files=184,source_files_sha256=files,extra_manifests_sha256=extra,baseline_profile_ids=ids,source_sheet=str(sheet),source_sheet_sha256=h(sheet),source_catalogue=str(cat),catalogue_sha256=h(cat),published41_runtime_artwork_parity=dict(path=str(current),files_sha256=parity,count=len(parity),excluded_changed_metadata_registry_and_aggregate_guard=excluded))
write(W/'BASELINE_FREEZE.json',freeze);write(W/'SOURCE_CATALOGUE_ENTRY.json',entry)
def pose(b,t,l,press,purse):
 return dict(brow_screen_left=b,brow_screen_right=b,brow_tilt_screen_left=t,brow_tilt_screen_right=-t,blink_R=l,blink_L=l,mouth_lip_press=press,mouth_purse=purse)
poses={'neutral':{},'tension_onset':pose(-.12,.20,.12,.12,.01),'heavy_build':pose(-.30,.40,.38,.32,.025),'close_build':pose(-.45,.55,.70,.50,.04),'headache_peak':pose(-.55,.65,1.,.65,.05),'soften_closed':pose(-.12,.12,1.,.08,0),'reopen':pose(-.04,.035,.18,0,0),'neutral_return':{}}
keys=[(0,'neutral'),(.2,'neutral'),(.6,'tension_onset'),(1.,'heavy_build'),(1.3,'close_build'),(1.6,'headache_peak'),(2.4,'headache_peak'),(2.8,'soften_closed'),(3.2,'reopen'),(3.7,'neutral_return'),(4.,'neutral_return')]
write(W/'plan.json',[dict(name=k,pose=v) for k,v in poses.items()])
write(W/'EXP-096.json',dict(id='EXP-096',title='Headache tension',duration=4.0,status='UNAPPROVED shared-rig preparation v1; independent source and native visual review pending',intent=entry['distinctive_facial_intent'],scope='Existing lowered/opposed-tilt rigid brows, ordinary bilateral blink_L/R, sealed lip pressure and tiny symmetric purse only. No central furrows, horizontal brow convergence or independent downturned corners are available. No art, anatomy, runtime, shader, production registry, head/body motion, mouth opening, smile/corners, eye_smile, opening_px, gaze, aversion, speech or effects.',timing_origin='New four-second interpretation of inspected static nine-panel source, not recovered motion. Central brow tension develops while both ordinary lids progressively close. KP5-6 map to the fully closed 1.6-2.4 peak. Brow and mouth tension soften at 2.8 (KP7) while lids stay fully closed, then eyes reopen. Reference catalogue proposed 1.9-second timing is not implemented animation.',interpolation='Unchanged shared smoothstep; eight static anchors, eleven timeline keys, exact neutral bookends. Candidate and probes exist only in memory. Full closure from 1.6 through 2.8 is deliberate, not smile-eye.',source_catalogue_sha256=h(cat),keyframes=[dict(time=t,phase=p,values=poses[p]) for t,p in keys]))
write(W/'SOURCE_REFERENCE.json',dict(sheet=str(sheet),sha256=h(sheet),dimensions=[1159,1358],pixels_inspected=True,observations='Actual full nine-panel sheet viewed before authoring. KP2 develops central brow tension; KP3-4 progressively narrow ordinary lids while brows incline downward toward the center and the lips press. KP5-6 have fully closed eyes and a small pressed/downturned line. KP7 softens brow and mouth tension with eyes still closed; KP8 reopens toward neutral, and KP9 returns neutral. The source does not show smiling eyes, a smile, an open mouth or sideways gaze.',left_right_convention='Brow names use screen sides. blink_R closes screen-left and blink_L closes screen-right. Positive screen-left and negative screen-right tilt oppose inward. All gaze and aversion channels remain zero.',approximation='Existing rigid brows translate down 5.5 source pixels and rotate +5.2/-5.2 degrees at peak. They cannot converge horizontally, deform or add true central furrows. blink_L=blink_R=1 uses ordinary lids with 36 source-pixel lash travel. Lip pressure .65 reuses existing pressed-lip owners. Tiny purse .05 shortens total contour width by 1.4 source pixels (.686 bust pixels); its center shifts down .2 and endpoints down .6 source pixels. This is a small symmetric purse contour approximation, not a genuine independent downturned corner. Mouth aperture stays zero. Reference fidelity and perceptual distinctness need native review.',panel_to_anchor={'1':'neutral','2':'tension_onset','3':'heavy_build','4':'close_build','5':'headache_peak','6':'headache_peak','7':'soften_closed','8':'reopen','9':'neutral_return'},panel_hashes={p['actual_panel_path']:p['sha256'] for p in entry['key_pose_sequence']},approval='Accepted reference art does not approve this candidate or animation.'))
print('Prepared UNAPPROVED EXP-096. Baseline: 999 pinned files, 184 PNGs; 993 common runtime/artwork files equal approved41.')

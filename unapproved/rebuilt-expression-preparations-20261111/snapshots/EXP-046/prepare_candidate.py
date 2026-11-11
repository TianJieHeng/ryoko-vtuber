"""New source-only EXP-046 rebuild. No external command or renderer is launched."""
import hashlib
import json
import shutil
from pathlib import Path
W = Path(__file__).resolve().parent
R = W.parent.parent
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
def write(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False)+'\n')
def main():
    if (W/'BASELINE_FREEZE.json').exists() or (W/'rig').exists():
        raise SystemExit('Already prepared; preserve this candidate and create a new directory for changes.')
    manifest = json.loads((R/'RECOVERY_MANIFEST.json').read_text())
    baseline = [r for r in manifest['files'] if r['destination'].startswith('main/ryoko_object_rig/')]
    assert len(baseline)==1124
    pinned = {}
    for row in baseline:
        source = R/row['destination']
        assert sha(source)==row['sha256'], source
        rel = source.relative_to(R/'main/ryoko_object_rig')
        dest = W/'rig'/rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source,dest)
        assert sha(dest)==row['sha256']
        pinned[str(rel)]=row['sha256']
    registry=json.loads((W/'rig/expressions/registry.json').read_text())
    ids=[e['id'] for e in registry['entries']]
    assert len(ids)==39 and 'EXP-046' not in ids
    catalogue=R/'main/avatar_build_assets/reference_library/metadata/expressions.json'
    data=json.loads((R/'metadata/target_catalogue_entries.json').read_text())
    entry=next(e for e in data['entries'] if e['id']=='EXP-046')
    assert sha(catalogue)==data['source_sha256']
    ref=R/'main/avatar_build_assets/reference_library'
    refs=[(entry['asset_production']['actual_path'],entry['asset_production']['sha256'])]+[(p['actual_panel_path'],p['sha256']) for p in entry['key_pose_sequence']]
    source_hashes={}
    for path,digest in refs:
        assert sha(ref/path)==digest
        dest=W/'reference'/Path(path).name;dest.parent.mkdir(exist_ok=True)
        shutil.copy2(ref/path,dest);source_hashes[dest.name]=digest
    headache=R/'headache_review_backup/EXP-096-headache-tension/historical/EXP-096.json'
    assert sha(headache)=='21ba5c4393ed672a5496ed28577068bd4b56e3b8ff5d7ac4f9674df03badf1fe'
    write(W/'BASELINE_FREEZE.json',dict(identity='NEW EXP046 rebuild 2026-11-11 v1',previous_local_candidate_restored=False,main_commit='419450d2302d471aa009557289ad509ffb413349',baseline_profile_count=39,baseline_profile_ids=ids,baseline_files_sha256=pinned,reference_files_sha256=source_hashes,source_catalogue_sha256=sha(catalogue),recovery_manifest_sha256=sha(R/'RECOVERY_MANIFEST.json'),headache_profile_sha256=sha(headache)))
    write(W/'SOURCE_CATALOGUE_ENTRY.json',entry)
    def pose(inner,lids,gaze,opening,purse,brow=0.0):
        return dict(brow_inner_lift_screen_left=inner,brow_inner_lift_screen_right=inner,brow_screen_left=brow,brow_screen_right=brow,blink_L=lids,blink_R=lids,gaze_y=gaze,mouth_open=opening,mouth_purse=purse)
    poses={'neutral':{},'weary_onset':pose(.24,.06,0,.06,.08), 'upward_glance':pose(.40,.13,-.7,.10,.12,-.04),'glance_crest':pose(.46,.18,-1.,.16,.16,-.05),'exhale_onset':pose(.50,.35,-.4,.34,.20,-.06),'exhale_peak':pose(.52,.50,0,.50,.26,-.07),'exhale_tail':pose(.44,.38,0,.28,.20,-.06),'tired_release':pose(.25,.24,0,.12,.12,-.03),'reseal':pose(.08,.05,0,0,0),'neutral_return':{}}
    keys=[(0,'neutral'),(.3,'neutral'),(.7,'weary_onset'),(1.15,'upward_glance'),(1.5,'glance_crest'),(1.85,'exhale_onset'),(2.25,'exhale_peak'),(2.7,'exhale_tail'),(3.15,'tired_release'),(3.7,'reseal'),(4.5,'neutral_return'),(4.8,'neutral_return')]
    write(W/'plan.json',[dict(name=k,pose=v) for k,v in poses.items()])
    write(W/'EXP-046.json',dict(id='EXP-046',title='Exasperated sigh',duration=4.8,status='UNAPPROVED new reconstruction v1; not a restored frozen implementation; native execution and review NOT RUN',intent='Weary inner brows, a bounded upward glance, then a prolonged unsmiling exhale and exact neutral return.',scope='Unchanged approved39 rigid outer-anchor inner-brow lift, small whole-brow lowering, ordinary bilateral lids, existing upward gaze (2 source pixels maximum), unsmiling mouth opening and symmetric purse only. Full source eye roll, brow deformation, jaw/shoulder motion, independent downturned corners and breathing anatomy are not implemented. No new art, runtime, shader, production registry entry or effect.',timing_origin='New 4.8-second interpretation after viewing the actual nine-panel sheet. Static source order retained; catalogue 1.9-second proposal is not recovered motion. Upward glance crests at 1.5s before half-closed unsmiling exhale at 2.25s. Mouth reseals by 3.7s; exact neutral from 4.5s. Old local-only implementation and captures remain lost.',interpolation='Unchanged shared cubic smoothstep, 0.30s same-expression retrigger and 0.45s release. Python numerical models are not native execution evidence. Candidate loading is prepared for memory only.',source_catalogue_sha256=sha(catalogue),keyframes=[dict(time=t,phase=k,values=poses[k]) for t,k in keys]))
    write(W/'SOURCE_MAP.json',dict(reference_sheet=entry['asset_production'],pixels_inspected=True,inspection_method='Viewed recovered 1159x1358 original sheet before authoring, not just catalogue prose.',observations='KP2 lifts the brow centers and parts the lips; KP3-4 look upward with increasingly heavy ordinary lids. KP5 has a larger unsmiling exhale and about half-closed eyes; KP6 tapers it; KP7 remains tired with a smaller opening; KP8 reseals and settles; KP9 is neutral. No smiling-eye substitution.',panel_to_anchor={'1':'neutral','2':'weary_onset','3':'upward_glance','4':'glance_crest','5':'exhale_peak','6':'exhale_tail','7':'tired_release','8':'reseal','9':'neutral_return'},intermediate_anchor='exhale_onset is an authored interpolation waypoint, not a tenth recovered source pose.',control_mapping={'brows':'Existing rigid outer-anchor rotation: -26*inner_lift degrees screen-left, +26*inner_lift screen-right; whole-brow y=-10*brow. No local hook deformation.','lids':'blink_R controls screen-left, blink_L screen-right; ordinary lash y=36*blink, max 18 source pixels. No full closure or smiling lids.','gaze':'gaze_y in [-1,0] gives [-2,0] source-pixel vertical offset. At 0.49 bust scale this is <=0.98 display pixels: a subtle glance, explicitly not a full eye roll.','mouth':'Existing split-lip aperture with MAX_MOUTH_APERTURE=0.55 and symmetric purse. At peak central gap=0.50*0.55*54-1.5*0.26=14.46 source pixels. No smile, spread, width, independent corners or lip press.'},limitations=['The source calls for an eye roll; current approved assets permit only a subtle upward glance. This partial fit must be made explicit at review.','Rigid whole brow strips cannot reproduce the painted inner hooks or localized furrows.','Purse is existing contour articulation, not independent downturned mouth anatomy.','No body/shoulder breath acting, actual airflow, new jaw action, lip sync or sound.','Native eye coverage, lip seams, appearance, perceptual distinctness and real-time pacing remain NOT RUN.','A numerically different trajectory does not establish visual success or user approval.'],approval='Unapproved. Accepted reference art is not animation approval.'))
    write(W/'LAUNCH_CLEARANCE.json',dict(state='DENIED_PENDING_RESOLUTION',cleared=False,reason='Parent reports outstanding project-launch denial. Do not launch Godot by CLI, editor, renderer, UI, headless, alternate environment or fallback route. This file is a guard, not authorization.',native_execution_performed=False))
    print('New source-only EXP046 candidate prepared; 1124 baseline files copied and verified; no native execution.')
if __name__=='__main__':main()

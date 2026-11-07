#!/usr/bin/env python3
"""Complete path/hash scope for the approved160 publication, preserving both parents."""
from pathlib import Path
import hashlib,json,sys
sys.dont_write_bytecode=True
from approved_shy_merge_source_guard import ROOT as P, RECEIPT, IDS, approved_shy_registry_matches
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
digest=lambda f:hashlib.sha256(json.dumps(f,sort_keys=True,separators=(',',':')).encode()).hexdigest()
ALLOWED_MERGE=['BROW_INNER_LIFT_STATUS.json', 'BROW_INNER_LIFT_VALIDATION.md', 'CONTROL_API.md', 'LOCAL_CONTROL_BRIDGE.md', 'PACKAGING.md', 'README.md', 'RELEASE.json', 'SHY_LAUGHTER_STATUS.json', 'SHY_LAUGHTER_VALIDATION.md', 'control_bridge.gd', 'control_limits.gd', 'expression_registry.gd', 'expression_rig.gd', 'expression_viewer.gd', 'expressions/registry.json', 'object_face.gd', 'object_rig.gd', 'rig_assets/gaze_eyes/completed_iris_screen_left.png', 'rig_assets/gaze_eyes/completed_iris_screen_right.png', 'rig_assets/gaze_eyes/iris_screen_left.png', 'rig_assets/gaze_eyes/iris_screen_right.png', 'rig_assets/gaze_eyes/manifest.json', 'test_expression_backbone.gd', 'test_yawn.gd', 'tests/test_affection_runtime.gd', 'tests/test_auto_blink_lifecycle.gd', 'tests/test_blush_controls.gd', 'tests/test_brow_inner_lift_contract.gd', 'tests/test_down_extra_runtime.gd', 'tests/test_giggle_runtime.gd', 'tests/test_oral_lift_contract.gd', 'tests/test_private_pride_runtime.gd', 'tests/test_purse_contract.gd', 'tests/test_purse_transport.gd', 'tests/test_reassurance_runtime.gd', 'tests/test_relief_runtime.gd', 'tests/test_shy_laughter_runtime.gd', 'tests/test_spread_runtime.gd', 'tools/approved_merge_source_guard.py', 'tools/autoblink_source_guard.py', 'tools/build_gaze_eyes.py', 'tools/shy_source_guard.py', 'tools/test_control_bridge.py', 'tools/verify_affection_scope.py', 'tools/verify_autoblink_scope.py', 'tools/verify_closed_smile_support.py', 'tools/verify_down_extra_scope.py', 'tools/verify_gaze_coverage.py', 'tools/verify_giggle_scope.py', 'tools/verify_lid_handoff.py', 'tools/verify_private_pride_scope.py', 'tools/verify_reassurance_scope.py', 'tools/verify_relief_scope.py', 'tools/verify_shy_scope.py', 'tools/verify_smile_support.py', 'tools/verify_spread_support.py', 'tools/verify_welcome_scope.py']
NEW_PATHS=['BROW_INNER_LIFT_STATUS.json', 'BROW_INNER_LIFT_VALIDATION.md', 'SHY_LAUGHTER_STATUS.json', 'SHY_LAUGHTER_VALIDATION.md', 'SHY_MERGED_PUBLICATION_VALIDATION.md', 'expressions/EXP-160.json', 'source_references/approved152_publication_inventory.json', 'source_references/approved160_review_inventory.json', 'source_references/brow_inner_lift_parent_inventory.json', 'source_references/brow_inner_lift_predecessor_RELEASE.json', 'source_references/brow_outer_anchor_geometry.json', 'source_references/shy_laughter_parent_inventory.json', 'source_references/shy_laughter_predecessor_RELEASE.json', 'source_references/shy_laughter_source_manifest.json', 'tests/test_brow_inner_lift_contract.gd', 'tests/test_shy_laughter_runtime.gd', 'tools/approved_shy_merge_source_guard.py', 'tools/brow_source_guard.py', 'tools/review_brow_extension.gd', 'tools/review_brow_parity.gd', 'tools/review_shy_trajectory.gd', 'tools/shy_source_guard.py', 'tools/test_outer_anchor_preflight.gd', 'tools/verify_approved_shy_merge.py', 'tools/verify_brow_inner_lift_scope.py', 'tools/verify_shy_scope.py', 'validation/approved_shy_merge_migration.json', 'validation/brow_inner_lift_runtime_migration.json', 'validation/shy_laughter_runtime_migration.json']
def verify(clean=False):
    m=json.loads((P/RECEIPT).read_text());a=json.loads((P/'source_references/approved152_publication_inventory.json').read_text());s=json.loads((P/'source_references/approved160_review_inventory.json').read_text())
    assert len(a['files'])==495 and digest(a['files'])==a['inventory_sha256']=='acbac9aaef5e03b6487e3306850c80c21eedecfd8a133a401c808f58ba2188a6'
    assert len(s['files'])==473 and digest(s['files'])==s['inventory_sha256']=='9978d0cd18212e104355ca6e06ba9c6b969011c6041a755e74b414adb3700418'
    assert not any(x.is_symlink() for x in P.rglob('*'))
    assert set(m['files'])==set(ALLOWED_MERGE) and set(m['new_paths_from_152'])==set(NEW_PATHS),'fixed exact successor scope'
    actual={str(x.relative_to(P)) for x in P.rglob('*') if x.is_file() and (clean or not set(x.parts)&{'.godot','__pycache__'})}
    expected=set(a['files'])|set(m['new_paths_from_152']);assert actual==expected,'exact successor paths'
    assert set(s['files'])<=expected and set(m['new_paths_from_152'])==expected-set(a['files'])
    for n in expected-{'SOURCE_FILES.sha256',RECEIPT}:
        h=sha(P/n);record=m['files'].get(n)
        if record:
            assert h==record['candidate_sha256'] and set(record['predecessor_sha256'])=={q['files'][n] for q in [a,s] if n in q['files']},'pinned merge '+n
        else:
            parents={q['files'][n] for q in [a,s] if n in q['files']}
            if parents:assert parents=={h},'unchanged '+n
            else:assert h==m['new_files'][n],'new support '+n
    assert set(m['new_files'])==expected-set(a['files'])-set(s['files'])-{RECEIPT}
    assert all(sha(P/n)==h for n,h in a['files'].items() if n.endswith(('.png','.gdshader','.tscn','.import')) or n=='project.godot' or n=='yawn_performance.json' or n.startswith('expressions/EXP-')),'all prior profiles/art/shaders/scenes/config unchanged'
    assert sha(P/'expressions/EXP-160.json')==s['files']['expressions/EXP-160.json']=='f30c64314d59fa368781eb5e098a12fb6582f845b0d4fa43e40a4a4cd77838c2'
    assert {n for n in expected if n.endswith('.png')}=={n for n in a['files'] if n.endswith('.png')} and len([n for n in expected if n.endswith('.png')])==182
    for n in set(a['files'])|set(s['files']):
        if (n.startswith('source_references/') or n.startswith('validation/')) and n not in {RECEIPT}:assert sha(P/n)==(a['files'].get(n) or s['files'][n]),'historical receipt/provenance unchanged '+n
    assert approved_shy_registry_matches(),'all nine exact approved profiles and aliases'
    manifest={}
    for row in (P/'SOURCE_FILES.sha256').read_text().splitlines():
        h,sep,n=row.partition('  ');assert sep=='  ' and n not in manifest;manifest[n]=h
    assert set(manifest)==expected-{'SOURCE_FILES.sha256'} and all(sha(P/n)==h for n,h in manifest.items())
    release=json.loads((P/'RELEASE.json').read_text());assert release['user_approved'] and release['approved_registry']==IDS
    assert not any(n.endswith(('.zip','.mp4','.pyc')) or set(n.split('/'))&{'.git','.godot','__pycache__'} for n in expected)
    print('APPROVED_SHY_MERGE_SCOPE_PASS files='+str(len(expected))+' pngs=182 registry=9 frozen160=473 published152=495')
if __name__=='__main__':verify(clean='--clean' in sys.argv)

#!/usr/bin/env python3
"""Exact local additive-brow scope; no widening of historical hash receipts."""
from pathlib import Path
from shy_source_guard import shy_matches, shy_registry_matches
import hashlib,json
P=Path(__file__).resolve().parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
base=json.loads((P/'source_references/brow_inner_lift_parent_inventory.json').read_text())
m=json.loads((P/'validation/brow_inner_lift_runtime_migration.json').read_text())
allowed={'object_face.gd','object_rig.gd','expression_rig.gd','expression_registry.gd','expression_viewer.gd','control_limits.gd','control_bridge.gd','CONTROL_API.md','LOCAL_CONTROL_BRIDGE.md','README.md','PACKAGING.md','RELEASE.json','tools/autoblink_source_guard.py','tools/verify_autoblink_scope.py','tools/verify_relief_scope.py'}
checks=0
def check(ok,label):
 global checks
 checks+=1
 assert ok,label
check(base['commit']=='8c349e29fb1e742231918260d7db56026492a6c9','published baseline')
check(base['inventory_sha256']=='70e8593da87a240bfa024c58677f53560f4ff7afc6d6fa07f7f54665d1072cf6','exact parent inventory')
check(len(base['files'])==450 and set(m['files'])==allowed,'narrow450-file source delta')
for name,h in base['files'].items():
 check((P/name).is_file(),'retained '+name)
 if name=='SOURCE_FILES.sha256':continue
 if name in m['files']:
  check(m['files'][name]['baseline_sha256']==h,'old hash '+name)
  check(sha(P/name)==m['files'][name]['candidate_sha256'] or shy_matches(name,m['files'][name]['candidate_sha256']),'pinned candidate or exact EXP-160 support migration '+name)
 else:check(sha(P/name)==h or shy_matches(name,h),'unchanged or exact EXP-160 support migration '+name)
check(set(m['new_files'])=={'tests/test_brow_inner_lift_contract.gd','tools/review_brow_extension.gd','tools/review_brow_parity.gd','tools/verify_brow_inner_lift_scope.py','tools/brow_source_guard.py','BROW_INNER_LIFT_VALIDATION.md','BROW_INNER_LIFT_STATUS.json','source_references/brow_inner_lift_parent_inventory.json','source_references/brow_inner_lift_predecessor_RELEASE.json','source_references/brow_outer_anchor_geometry.json','tools/test_outer_anchor_preflight.gd'},'only exact new capability/support files')
for name,h in m['new_files'].items():check(sha(P/name)==h or shy_matches(name,h),'pinned new file or exact EXP-160 support migration '+name)
check({f.relative_to(P).as_posix() for f in P.rglob('*.png')}=={n for n in base['files'] if n.endswith('.png')},'no new art')
check(sum(n.endswith('.png') for n in base['files'])==182,'all182PNG preserved')
check(len(json.loads((P/'expressions/registry.json').read_text())['entries'])==6 or shy_registry_matches(),'six approved profiles or exact local EXP-160 migration')
check(not any(n.endswith('.gdshader') for n in m['files']),'all shaders preserved')
print(f'BROW_INNER_LIFT_SCOPE_PASS checks={checks} parent_files=450 protected_pngs=182 changed_parent_files={len(allowed)}')

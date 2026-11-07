#!/usr/bin/env python3
"""Verify exact local correction against e436972, without weakening frozen receipts."""
from pathlib import Path
import hashlib,json
from affection_source_guard import affection_matches
P=Path(__file__).resolve().parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
base=json.loads((P/'source_references/autoblink_parent_inventory.json').read_text())
m=json.loads((P/'validation/autoblink_runtime_migration.json').read_text())
checks=0
def check(ok,label):
 global checks
 checks+=1
 assert ok,label
check(base['commit']=='e4369727e7597894d6c2747d06e3cb7ff5b119ca','exact parent')
check(base['inventory_sha256']=='dfe5c6023d09215812561c6ae52a30949c7d64c5cfae8f8ad166f5ee454dd9fd','exact parent inventory')
check(len(base['files'])==442,'all 442 parent files')
allowed={'expression_rig.gd','expression_viewer.gd','control_bridge.gd','tests/test_relief_runtime.gd','tests/test_purse_contract.gd','tools/relief_source_guard.py','tools/verify_relief_scope.py','CONTROL_API.md','LOCAL_CONTROL_BRIDGE.md','README.md'}
check(set(m['files'])==allowed,'narrow exact delta')
for name,h in base['files'].items():
 check((P/name).is_file(),'retained '+name)
 if name=='SOURCE_FILES.sha256':continue
 if name in m['files']:
  record=m['files'][name]
  check(record['baseline_sha256']==h,'migration parent '+name)
  check(sha(P/name)==record['candidate_sha256'] or affection_matches(name,record['candidate_sha256']),'pinned correction '+name)
 else:check(sha(P/name)==h or affection_matches(name,h),'unchanged or pinned descendant '+name)
# All facial renderer, baseline blink timing, artwork, registry/profile, shader and
# geometry paths are covered by unchanged hashes above, not a broad exclusion.
check(sum(name.endswith('.png') for name in base['files'])==182,'all 182 approved PNGs unchanged')
check({p.relative_to(P).as_posix() for p in P.rglob('*.png')}=={n for n in base['files'] if n.endswith('.png')},'no additional art')
for name,h in m['new_files'].items():check(sha(P/name)==h or affection_matches(name,h),'pinned new test/harness '+name)
print(f'AUTO_BLINK_SCOPE_PASS checks={checks} parent_files=442 protected_pngs=182 changed_parent_files={len(allowed)}')

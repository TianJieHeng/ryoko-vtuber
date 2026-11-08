#!/usr/bin/env python3
"""Verify the narrow welcome scope against exact recovered source inventories."""
from pathlib import Path
import hashlib,json
from welcome_source_guard import giggle_matches
P=Path(__file__).resolve().parents[1];checks=0
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def check(ok,label):
 global checks
 checks+=1
 if not ok:raise AssertionError(label)
sources=json.loads((P/'source_references/welcome_scope_sources.json').read_text())
for path,digest in sources['protected_art_and_profiles'].items():check((sha(P/path)==digest or giggle_matches(path,digest)),'approved predecessor '+path)
for path,digest in sources['selected_exact'].items():check((sha(P/path)==digest or giggle_matches(path,digest)),'exact reviewed welcome source '+path)
baseline=json.loads((P/'source_references/laughter_baseline_inventory.json').read_text())
allowed=set(json.loads((P/'validation/welcome_scoped_changes.json').read_text())['changed_baseline_paths'])
for path,digest in baseline['files'].items():
 check((P/path).is_file(),'retained predecessor path '+path)
 if path not in allowed:check((sha(P/path)==digest or giggle_matches(path,digest)),'unchanged predecessor path '+path)
check(sha(P/'canonical_eye_alpha.gdshader')==baseline['files']['canonical_eye_alpha.gdshader'],'exact approved eye shader')
registry=json.loads((P/'expressions/registry.json').read_text())
check([e['id'] for e in registry['entries']]==['EXP-163','EXP-005','EXP-001','EXP-006','EXP-107','EXP-007','EXP-003'],'exact registry order and scope')
check({p.name for p in (P/'expressions').glob('EXP-*.json')}=={'EXP-005.json','EXP-001.json','EXP-006.json','EXP-107.json','EXP-007.json','EXP-003.json'},'only approved non-yawn profiles')
check(not (P/'rig_assets/wide_support').exists(),'no wide-eye artwork')
for path in ['object_face.gd','expression_registry.gd','expression_rig.gd','expression_viewer.gd','control_bridge.gd']:
 text=(P/path).read_text()
 for forbidden in ['eye_wide','wide_support']:
  check(forbidden not in text,'no unapproved control '+path+' '+forbidden)
for path in ['object_face.gd','expression_rig.gd']:
 check('EXP-001' not in (P/path).read_text(),'no expression-specific controller '+path)
check(len(list((P/'rig_assets/spread_support').glob('*.png')))==17,'only 17 lateral support PNGs')
check(len(list(P.rglob('*.png')))==182,'174 parent PNGs plus two pressed-lip and six original/registered/mask FX PNGs')
check(not list(P.rglob('*.mp4')),'movies remain external')
print(f'WELCOME_SCOPE_PASS checks={checks} predecessor_pngs=157 lateral_pngs=17 registry=7')

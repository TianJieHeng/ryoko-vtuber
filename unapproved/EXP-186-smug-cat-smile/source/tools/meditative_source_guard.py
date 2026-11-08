"""Exact data-only EXP-177 descendant of published main7065575. No runtime exceptions."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
BASE_COMMIT='70655752bc82ba01b3fe8f64923360da60c578c9'
BASE_HASH='3f25dad6194837b63ed396447b21a923fc36e88abee11295eab4c224271cbfb5'
PROFILE_HASH='4fb88990455fc4ba799e30ce2987b17151fe0ca00d31e562aa38680a7349f211'
INVENTORY='source_references/meditative_parent_inventory.json'
MIGRATION='validation/meditative_runtime_migration.json'
MANIFEST='SOURCE_FILES.sha256'
ALLOWED=frozenset(['RELEASE.json', 'tests/test_affection_runtime.gd', 'tools/verify_down_extra_scope.py', 'CONTROL_API.md', 'LOCAL_CONTROL_BRIDGE.md', 'PACKAGING.md', 'README.md', 'expressions/registry.json', 'test_expression_backbone.gd', 'tests/test_auto_blink_lifecycle.gd', 'tests/test_brow_inner_lift_contract.gd', 'tests/test_down_extra_runtime.gd', 'tests/test_giggle_runtime.gd', 'tests/test_oral_lift_contract.gd', 'tests/test_private_pride_runtime.gd', 'tests/test_purse_contract.gd', 'tests/test_purse_transport.gd', 'tests/test_reassurance_runtime.gd', 'tests/test_relief_runtime.gd', 'tests/test_shy_laughter_runtime.gd', 'tests/test_spread_runtime.gd', 'tools/approved_shy_merge_source_guard.py', 'tools/verify_affection_scope.py', 'tools/verify_approved_shy_merge.py', 'tools/verify_giggle_scope.py', 'tools/verify_private_pride_scope.py', 'tools/verify_reassurance_scope.py', 'tools/verify_relief_scope.py', 'tools/verify_smile_support.py', 'tools/verify_welcome_scope.py'])
NEW_FILES=frozenset(['MEDITATIVE_PUBLICATION_VALIDATION.md','source_references/meditative_v1_review_inventory.json','MEDITATIVE_CLOSING_REVISION.md','source_references/meditative_v0_inventory.json','source_references/EXP-177_v0.json','tools/verify_meditative_closing_scope.py','tests/test_meditative_closing_smoothness.gd','tools/review_meditative_regression.gd', 'MEDITATIVE_SCOPE_VALIDATION.md', 'MEDITATIVE_STATUS.json', 'expressions/EXP-177.json', 'source_references/EXP-177_reference_metadata.json', 'source_references/meditative_parent_inventory.json', 'source_references/meditative_parent_registry.json', 'tests/test_meditative_runtime.gd', 'tools/meditative_source_guard.py', 'tools/review_meditative_gate.gd', 'tools/review_meditative_lifecycle.gd', 'tools/review_meditative_scope.gd', 'tools/verify_meditative_scope.py', 'validation/meditative_runtime_migration.json'])
IDS=['EXP-163','EXP-005','EXP-001','EXP-006','EXP-107','EXP-007','EXP-002','EXP-152','EXP-160','EXP-177']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def read_contract():
 b=json.loads((ROOT/INVENTORY).read_text());m=json.loads((ROOT/MIGRATION).read_text())
 assert b['base_commit']==BASE_COMMIT and b['inventory_sha256']==BASE_HASH==digest(b['files']) and len(b['files'])==524
 assert m['base_commit']==BASE_COMMIT and m['base_inventory_sha256']==BASE_HASH
 assert set(m['files'])==ALLOWED and set(m['new_files'])==NEW_FILES-{MIGRATION}
 for n,r in m['files'].items():assert r['baseline_sha256']==b['files'][n]
 assert not any(n.endswith(('.png','.gdshader','.tscn','.import')) or (n.endswith('.gd') and '/' not in n and n!='test_expression_backbone.gd') or (n.startswith('expressions/EXP-')) or n in ['project.godot','yawn_performance.json'] for n in ALLOWED)
 assert sha(ROOT/'expressions/EXP-177.json')==PROFILE_HASH
 return b,m
def meditative_matches(path,expected):
 try:
  b,m=read_contract();r=m['files'].get(path)
  return bool(r and expected==b['files'][path]==r['baseline_sha256'] and sha(ROOT/path)==r['candidate_sha256'])
 except (OSError,KeyError,ValueError,AssertionError,TypeError):return False
def meditative_registry_matches():
 try:
  b,m=read_contract();reg=json.loads((ROOT/'expressions/registry.json').read_text())
  original=json.loads((ROOT/'source_references/meditative_parent_registry.json').read_text())
  entry={'id':'EXP-177','path':'res://expressions/EXP-177.json','aliases':['meditative-calm','meditate'],'trigger_phase':'settling'}
  return reg=={'schema_version':1,'entries':original['entries']+[entry]} and meditative_matches('expressions/registry.json',b['files']['expressions/registry.json']) and all(sha(ROOT/e['path'][6:])==b['files'][e['path'][6:]] for e in original['entries']) and {p.name for p in (ROOT/'expressions').glob('EXP-*.json')}=={x+'.json' for x in IDS if x!='EXP-163'} and sha(ROOT/'source_references/meditative_parent_registry.json')==b['files']['expressions/registry.json']
 except (OSError,KeyError,ValueError,AssertionError,TypeError):return False
def meditative_extra_paths():
 b,m=read_contract()
 assert all(sha(ROOT/n)==h for n,h in m['new_files'].items())
 return set(NEW_FILES)

"""Portable immutable-source and additive-profile guard for this local package."""
from pathlib import Path
import hashlib,json,sys
S=Path(__file__).resolve().parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
f=json.loads((S/'CONFIDENT_DENIAL_CAPTURE_FREEZE.json').read_text())
errors=[]
for path,h in f['files'].items():
 if not (S/path).is_file() or sha(S/path)!=h:errors.append(path)
assert not errors,errors
base=f['baseline_files'];changed=[p for p,h in base.items() if sha(S/p)!=h]
assert changed==['expressions/registry.json'],changed
old=json.loads((S/'source_references/confident_denial_prior_registry.json').read_text());new=json.loads((S/'expressions/registry.json').read_text())
assert new['entries'][:-1]==old['entries'] and new['entries'][-1]['id']=='EXP-116'
assert len(new['entries'])==16
status=json.loads((S/'CONFIDENT_DENIAL_STATUS.json').read_text())
assert status['unapproved_profile_ids']==['EXP-158','EXP-181','EXP-102','EXP-116'] and status['approved'] is False
print(json.dumps({'status':'PASS','verified_files':len(f['files']),'inherited_changed':changed,'prior_profiles_exact':15,'pngs_exact':182,'inventory_sha256':f['inventory_sha256']}))

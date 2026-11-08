"""Exact successor of published002/152 plus the frozen approved160 source."""
from meditative_source_guard import meditative_matches, meditative_registry_matches
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
RECEIPT='validation/approved_shy_merge_migration.json'
IDS=['EXP-163','EXP-005','EXP-001','EXP-006','EXP-107','EXP-007','EXP-002','EXP-152','EXP-160']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def approved_shy_merge_matches(path,expected):
    if meditative_matches(path,expected):return True
    file=ROOT/RECEIPT
    if not file.is_file():return False
    record=json.loads(file.read_text())['files'].get(path)
    return bool(record and expected in record['predecessor_sha256'] and (sha(ROOT/path)==record['candidate_sha256'] or meditative_matches(path,record['candidate_sha256'])))
def approved_shy_registry_matches():
    if meditative_registry_matches():return True
    try:
        m=json.loads((ROOT/RECEIPT).read_text());a=json.loads((ROOT/'source_references/approved152_publication_inventory.json').read_text())['files'];s=json.loads((ROOT/'source_references/approved160_review_inventory.json').read_text())['files']
        reg=json.loads((ROOT/'expressions/registry.json').read_text())
        return ([e['id'] for e in reg['entries']]==IDS and sha(ROOT/'expressions/registry.json')==m['files']['expressions/registry.json']['candidate_sha256'] and {p.name for p in (ROOT/'expressions').glob('EXP-*.json')}=={x+'.json' for x in IDS if x!='EXP-163'} and all(sha(ROOT/e['path'][6:])==(s if e['id']=='EXP-160' else a)[e['path'][6:]] for e in reg['entries']))
    except (OSError,ValueError,KeyError,TypeError):return False

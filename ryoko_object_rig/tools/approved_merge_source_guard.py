"""Exact hash-pinned merge of approved002 and approved152, without broad exceptions."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
def approved_merge_matches(path,expected):
    file=ROOT/'validation/approved_merge_migration.json'
    if not file.is_file():return False
    record=json.loads(file.read_text())['files'].get(path)
    return bool(record and expected in record['predecessor_sha256'] and hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==record['candidate_sha256'])

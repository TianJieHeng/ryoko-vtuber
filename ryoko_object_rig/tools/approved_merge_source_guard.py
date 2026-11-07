"""Exact hash-pinned merge of approved002 and approved152, without broad exceptions."""
from pathlib import Path
import hashlib,json
from approved_shy_merge_source_guard import approved_shy_merge_matches
ROOT=Path(__file__).resolve().parents[1]
def approved_merge_matches(path,expected):
    if approved_shy_merge_matches(path,expected):return True
    file=ROOT/'validation/approved_merge_migration.json'
    if not file.is_file():return False
    record=json.loads(file.read_text())['files'].get(path)
    return bool(record and expected in record['predecessor_sha256'] and (hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==record['candidate_sha256'] or approved_shy_merge_matches(path,record['candidate_sha256'])))

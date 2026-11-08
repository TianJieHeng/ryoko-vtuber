"""Accept only the exact pinned EXP-152 data/test/documentation extension."""
from pathlib import Path
import hashlib,json
from approved_merge_source_guard import approved_merge_matches
ROOT=Path(__file__).resolve().parents[1]
def private_pride_matches(path,expected):
    file=ROOT/'validation/private_pride_runtime_migration.json'
    if not file.exists():return False
    if approved_merge_matches(path,expected):return True
    record=json.loads(file.read_text())['files'].get(path)
    return bool(record and expected==record['baseline_sha256'] and (hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==record['candidate_sha256'] or approved_merge_matches(path,record['candidate_sha256'])))

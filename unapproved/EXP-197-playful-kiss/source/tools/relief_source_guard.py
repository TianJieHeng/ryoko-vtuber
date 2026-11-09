"""Accept only the exact pinned EXP-007 and generic rigid-purse extension."""
from pathlib import Path
import hashlib,json
from autoblink_source_guard import autoblink_matches
ROOT=Path(__file__).resolve().parents[1]
def relief_matches(path,expected):
    file=ROOT/'validation/relief_runtime_migration.json'
    if not file.exists():return False
    record=json.loads(file.read_text())['files'].get(path)
    return bool(record and expected==record['baseline_sha256'] and (hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==record['candidate_sha256'] or autoblink_matches(path,record['candidate_sha256']))) or autoblink_matches(path,expected)

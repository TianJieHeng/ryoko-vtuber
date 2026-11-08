"""Accept only the hash-pinned auto-blink lifecycle correction on e436972."""
from pathlib import Path
import hashlib,json
from down_extra_source_guard import down_extra_matches
ROOT=Path(__file__).resolve().parents[1]
def autoblink_matches(path,expected):
    file=ROOT/'validation/autoblink_runtime_migration.json'
    if not file.exists():return False
    record=json.loads(file.read_text())['files'].get(path)
    return bool(record and expected==record['baseline_sha256'] and (hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==record['candidate_sha256'] or down_extra_matches(path,record['candidate_sha256']))) or down_extra_matches(path,expected)

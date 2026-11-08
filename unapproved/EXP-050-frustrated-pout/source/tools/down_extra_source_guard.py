"""Accept only the explicitly hash-pinned hidden-cap/down-extension migration."""
from pathlib import Path
import hashlib,json
from private_pride_source_guard import private_pride_matches
ROOT=Path(__file__).resolve().parents[1]
def down_extra_matches(path,expected):
    file=ROOT/'validation/down_extra_runtime_migration.json'
    if not file.exists():return False
    record=json.loads(file.read_text())['files'].get(path)
    return bool(record and expected==record['baseline_sha256'] and (hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==record['candidate_sha256'] or private_pride_matches(path,record['candidate_sha256']))) or private_pride_matches(path,expected)

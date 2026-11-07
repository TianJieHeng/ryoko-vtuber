"""Accept only the exact pinned EXP-107 extension of the published EXP-006 source."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
def reassurance_matches(path,expected):
    file=ROOT/'validation/reassurance_runtime_migration.json'
    if not file.exists():return False
    record=json.loads(file.read_text())['files'].get(path)
    return bool(record and expected==record['baseline_sha256'] and hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==record['candidate_sha256'])

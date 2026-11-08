"""Accept only pinned blink correction and its exact EXP-003 descendant."""
from pathlib import Path
import hashlib,json
from contentment_source_guard import contentment_matches
ROOT=Path(__file__).resolve().parents[1]
def autoblink_matches(path,expected):
    file=ROOT/'validation/autoblink_runtime_migration.json'
    if not file.exists():return False
    record=json.loads(file.read_text())['files'].get(path)
    if record and expected==record['baseline_sha256']:
        target=record['candidate_sha256']
        return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==target or contentment_matches(path,target)
    return contentment_matches(path,expected)

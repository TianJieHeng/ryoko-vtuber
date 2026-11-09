"""Accept exact welcome migration or its explicitly pinned scoped giggle descendant."""
from pathlib import Path
import hashlib,json
from reassurance_source_guard import reassurance_matches
ROOT=Path(__file__).resolve().parents[1]
def giggle_matches(path,expected):
 file=ROOT/'validation/giggle_runtime_migration.json'
 if not file.exists():return False
 record=json.loads(file.read_text())['files'].get(path)
 return bool(record and expected==record['baseline_sha256'] and (hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==record['candidate_sha256'] or reassurance_matches(path,record['candidate_sha256']))) or reassurance_matches(path,expected)
def scoped_matches(path,expected):
 record=json.loads((ROOT/'validation/welcome_runtime_migration.json').read_text())['files'].get(path)
 return bool(record and expected==record['baseline_sha256'] and (hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==record['candidate_sha256'] or giggle_matches(path,record['candidate_sha256']))) or giggle_matches(path,expected)

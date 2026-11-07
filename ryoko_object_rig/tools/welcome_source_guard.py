"""Accept only the explicit, exact scoped descendant of an exact v9 file."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
def scoped_matches(path,expected):
 record=json.loads((ROOT/'validation/welcome_runtime_migration.json').read_text())['files'].get(path)
 return bool(record and expected==record['baseline_sha256'] and hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==record['candidate_sha256'])

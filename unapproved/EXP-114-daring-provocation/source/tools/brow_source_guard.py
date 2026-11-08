"""Recognize only the exact additive-brow migration from the450-file parent."""
from pathlib import Path
from shy_source_guard import shy_matches
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
ALLOWED={'object_face.gd','object_rig.gd','expression_rig.gd','expression_registry.gd','expression_viewer.gd','control_limits.gd','control_bridge.gd','CONTROL_API.md','LOCAL_CONTROL_BRIDGE.md','README.md','PACKAGING.md','RELEASE.json','tools/autoblink_source_guard.py','tools/verify_autoblink_scope.py','tools/verify_relief_scope.py'}
def brow_matches(path,expected):
    if path not in ALLOWED:return shy_matches(path,expected)
    inventory=ROOT/'source_references/brow_inner_lift_parent_inventory.json'
    migration=ROOT/'validation/brow_inner_lift_runtime_migration.json'
    if not inventory.is_file() or not migration.is_file():return False
    parent=json.loads(inventory.read_text());records=json.loads(migration.read_text())['files']
    if parent.get('commit')!='8c349e29fb1e742231918260d7db56026492a6c9' or len(parent.get('files',{}))!=450:return False
    if set(records)!=ALLOWED:return False
    record=records.get(path)
    return bool(record and parent['files'].get(path)==expected==record['baseline_sha256'] and (hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==record['candidate_sha256'] or shy_matches(path,record['candidate_sha256']))) or shy_matches(path,expected)

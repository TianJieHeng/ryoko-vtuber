"""Recognize only the exact EXP-160 descendant of the frozen outer-anchor rig.

The migration pins this guard, all changed support files, and every added file.
It excludes itself and SOURCE_FILES.sha256 to avoid recursive hash cycles; the
final source manifest covers the migration, and verify_shy_scope checks both.
No runtime, artwork, prior profile, or historical receipt is migratable here.
"""
from pathlib import Path
import hashlib
import json
import re
from approved_shy_merge_source_guard import approved_shy_merge_matches, approved_shy_registry_matches

ROOT = Path(__file__).resolve().parents[1]
BASELINE_INVENTORY_SHA256 = 'd3d32cea21da2973c711779f201676c8344b409fba966b48ab22832381fae49f'
PUBLISHED_BASELINE_COMMIT = '8c349e29fb1e742231918260d7db56026492a6c9'
BASELINE_KIND = 'outer_anchor_v1_local_candidate'
SHY_KEYFRAMES_SHA256 = '6f2a08d69d70e20156f75051f1300444f401a54e0961e25c05bf2528dbfbb35d'
INVENTORY_PATH = 'source_references/shy_laughter_parent_inventory.json'
PREDECESSOR_RELEASE_PATH = 'source_references/shy_laughter_predecessor_RELEASE.json'
MIGRATION_PATH = 'validation/shy_laughter_runtime_migration.json'
MANIFEST_PATH = 'SOURCE_FILES.sha256'
ALLOWED = frozenset({
    'expressions/registry.json', 'README.md', 'PACKAGING.md', 'RELEASE.json',
    'test_expression_backbone.gd', 'tests/test_brow_inner_lift_contract.gd',
    'tests/test_purse_contract.gd', 'tests/test_oral_lift_contract.gd',
    'tests/test_purse_transport.gd', 'tests/test_relief_runtime.gd',
    'tests/test_reassurance_runtime.gd', 'tests/test_giggle_runtime.gd',
    'tests/test_spread_runtime.gd', 'tests/test_blush_controls.gd',
    'tools/brow_source_guard.py',
    'tools/verify_brow_inner_lift_scope.py', 'tools/verify_relief_scope.py',
    'tools/verify_welcome_scope.py', 'tools/verify_giggle_scope.py',
    'tools/verify_reassurance_scope.py',
})
NEW_FILES = frozenset({
    'expressions/EXP-160.json', 'tools/review_shy_trajectory.gd',
    'tests/test_shy_laughter_runtime.gd', 'SHY_LAUGHTER_VALIDATION.md',
    'SHY_LAUGHTER_STATUS.json', 'source_references/shy_laughter_source_manifest.json',
    'tools/shy_source_guard.py', 'tools/verify_shy_scope.py', INVENTORY_PATH,
    PREDECESSOR_RELEASE_PATH, MIGRATION_PATH,
})
PRIOR_IDS = ['EXP-163', 'EXP-005', 'EXP-001', 'EXP-006', 'EXP-107', 'EXP-007']
PRIOR_PROFILE_PATHS = frozenset({
    'yawn_performance.json', 'expressions/EXP-005.json', 'expressions/EXP-001.json',
    'expressions/EXP-006.json', 'expressions/EXP-107.json', 'expressions/EXP-007.json',
})
PRIOR_ENTRIES = [
    {'id': 'EXP-163', 'path': 'res://yawn_performance.json', 'aliases': ['yawn'], 'trigger_phase': 'anticipation'},
    {'id': 'EXP-005', 'path': 'res://expressions/EXP-005.json', 'aliases': ['hearty-laughter', 'laugh'], 'trigger_phase': 'anticipation'},
    {'id': 'EXP-001', 'path': 'res://expressions/EXP-001.json', 'aliases': ['bright_welcome'], 'trigger_phase': 'recognition'},
    {'id': 'EXP-006', 'path': 'res://expressions/EXP-006.json', 'aliases': ['suppressed-giggle', 'giggle'], 'trigger_phase': 'anticipation'},
    {'id': 'EXP-107', 'path': 'res://expressions/EXP-107.json', 'aliases': ['confident-reassurance', 'reassure'], 'trigger_phase': 'anticipation'},
    {'id': 'EXP-007', 'path': 'res://expressions/EXP-007.json', 'aliases': ['relieved-smile', 'relief'], 'trigger_phase': 'inward_tension'},
]
SHY_ENTRY = {'id': 'EXP-160', 'path': 'res://expressions/EXP-160.json', 'aliases': ['shy-laughter', 'shy_laughter'], 'trigger_phase': 'tender_closed_onset'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory_sha(files):
    return hashlib.sha256(json.dumps(files, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def _require(condition, label):
    if not condition:
        raise ValueError(label)


def _digest(value):
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value) is not None


def read_contract():
    """Load a narrow hash receipt, rejecting malformed or widened contracts."""
    base = json.loads((ROOT / INVENTORY_PATH).read_text())
    _require(set(base) == {'schema_version', 'published_baseline_commit', 'baseline_kind', 'inventory_sha256', 'files'}, 'parent inventory schema')
    _require(base['schema_version'] == 1 and base['baseline_kind'] == BASELINE_KIND, 'parent identity')
    _require(base['published_baseline_commit'] == PUBLISHED_BASELINE_COMMIT, 'published parent')
    files = base['files']
    _require(len(files) == 462 and all(_digest(h) for h in files.values()), '462 exact parent hashes')
    _require(base['inventory_sha256'] == BASELINE_INVENTORY_SHA256 == inventory_sha(files), 'immutable outer-anchor inventory')
    _require(ALLOWED <= set(files) and not NEW_FILES.intersection(files), 'disjoint exact scope')
    _require(sha(ROOT / PREDECESSOR_RELEASE_PATH) == files['RELEASE.json'], 'immutable predecessor release')
    migration = json.loads((ROOT / MIGRATION_PATH).read_text())
    _require(set(migration) == {'schema_version', 'expression_id', 'baseline_kind', 'baseline_inventory_sha256', 'published_baseline_commit', 'files', 'new_files', 'hash_exclusions'}, 'migration schema')
    _require(migration['schema_version'] == 1 and migration['expression_id'] == 'EXP-160', 'migration identity')
    _require(migration['baseline_kind'] == BASELINE_KIND and migration['baseline_inventory_sha256'] == BASELINE_INVENTORY_SHA256, 'migration parent')
    _require(migration['published_baseline_commit'] == PUBLISHED_BASELINE_COMMIT, 'migration published parent')
    _require(migration['hash_exclusions'] == [MANIFEST_PATH, MIGRATION_PATH], 'only nonrecursive hash exclusions')
    _require(set(migration['files']) == ALLOWED, 'exact changed support paths')
    _require(set(migration['new_files']) == NEW_FILES - {MIGRATION_PATH}, 'exact new profile/support paths')
    for path, record in migration['files'].items():
        _require(set(record) == {'baseline_sha256', 'candidate_sha256'}, 'record schema: ' + path)
        _require(record['baseline_sha256'] == files[path] and _digest(record['candidate_sha256']), 'pinned migration: ' + path)
    _require(all(_digest(h) for h in migration['new_files'].values()), 'pinned new files')
    return base, migration


def shy_matches(path, expected):
    """Accept a final hash only from that path's exact frozen brow-parent hash."""
    if approved_shy_merge_matches(path,expected):
        return True
    if path not in ALLOWED:
        return False
    try:
        base, migration = read_contract()
        record = migration['files'][path]
        return expected == base['files'][path] == record['baseline_sha256'] and (sha(ROOT / path) == record['candidate_sha256'] or approved_shy_merge_matches(path,record['candidate_sha256']))
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        return False


def shy_registry_matches():
    """Permit precisely six unchanged definitions plus the pinned EXP-160 only."""
    if approved_shy_registry_matches():
        return True
    try:
        base, migration = read_contract()
        record = migration['files']['expressions/registry.json']
        if sha(ROOT / 'expressions/registry.json') != record['candidate_sha256']:
            return False
        if sha(ROOT / 'expressions/EXP-160.json') != migration['new_files']['expressions/EXP-160.json']:
            return False
        profile = json.loads((ROOT / 'expressions/EXP-160.json').read_text())
        if profile['id'] != 'EXP-160' or profile['duration'] != 3.4 or inventory_sha(profile['keyframes']) != SHY_KEYFRAMES_SHA256:
            return False
        registry = json.loads((ROOT / 'expressions/registry.json').read_text())
        if registry != {'schema_version': 1, 'entries': PRIOR_ENTRIES + [SHY_ENTRY]}:
            return False
        profile_paths = {p.relative_to(ROOT).as_posix() for p in (ROOT / 'expressions').glob('EXP-*.json')}
        if profile_paths != (PRIOR_PROFILE_PATHS - {'yawn_performance.json'}) | {'expressions/EXP-160.json'}:
            return False
        return all(sha(ROOT / path) == base['files'][path] for path in PRIOR_PROFILE_PATHS)
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        return False


def source_paths(clean=False):
    """List source paths; clean mode rejects every extra file, including caches."""
    base = json.loads((ROOT / INVENTORY_PATH).read_text())['files']
    paths = set()
    for file in ROOT.rglob('*'):
        if not file.is_file():
            continue
        path = file.relative_to(ROOT)
        if not clean and ('.godot' in path.parts or '__pycache__' in path.parts or file.suffix == '.pyc'):
            continue
        name = path.as_posix()
        if not clean and file.suffix == '.import' and name not in base:
            continue
        paths.add(name)
    return paths

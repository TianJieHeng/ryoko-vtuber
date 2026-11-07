#!/usr/bin/env python3
"""Authoritative exact EXP-160 source scope on the immutable 462-file brow rig."""
import argparse
import json
import sys

# A strict clean-source check must not create an unlisted cache while importing.
sys.dont_write_bytecode = True
from shy_source_guard import (
    ROOT as P, ALLOWED, NEW_FILES, MANIFEST_PATH, MIGRATION_PATH,
    PRIOR_PROFILE_PATHS, read_contract, sha, shy_matches,
    shy_registry_matches, source_paths,
)

checks = 0


def check(ok, label):
    global checks
    checks += 1
    assert ok, label


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--clean', action='store_true', help='Reject every unlisted file, including generated caches/imports.')
args = parser.parse_args()
if (P / 'validation/approved_shy_merge_migration.json').is_file():
    from verify_approved_shy_merge import verify
    verify(clean=args.clean)
    sys.exit(0)
base, migration = read_contract()
check(len(base['files']) == 462, 'all frozen outer-anchor parent files')
check(not any(path.is_symlink() for path in P.rglob('*')), 'no source file or directory symlinks')
check(source_paths(clean=args.clean) == set(base['files']) | NEW_FILES, 'exact 473 packaged source paths; no generated UIDs or out-of-scope files')
for name, digest in base['files'].items():
    check((P / name).is_file() and not (P / name).is_symlink(), 'retained regular source ' + name)
    if name == MANIFEST_PATH:
        continue
    if name in ALLOWED:
        check(shy_matches(name, digest), 'exact scoped migration ' + name)
    else:
        check(sha(P / name) == digest, 'immutable parent source ' + name)
for name, digest in migration['new_files'].items():
    check((P / name).is_file() and not (P / name).is_symlink() and sha(P / name) == digest, 'pinned new source ' + name)
# Redundant explicit guards document the boundaries that must never be migrated.
core = {name for name in base['files'] if ('/' not in name and name.endswith(('.gd', '.gdshader'))) and name != 'test_expression_backbone.gd'}
check(not core.intersection(ALLOWED), 'no core runtime or shader migration')
for name in core | PRIOR_PROFILE_PATHS:
    check(sha(P / name) == base['files'][name], 'unchanged runtime/shader/prior profile ' + name)
pngs = {name for name in base['files'] if name.endswith('.png')}
check(len(pngs) == 182, '182 frozen artwork files')
check({p.relative_to(P).as_posix() for p in P.rglob('*.png')} == pngs, 'no new artwork')
for name in pngs:
    check(sha(P / name) == base['files'][name], 'byte-exact artwork ' + name)
check(shy_registry_matches(), 'exact six prior definitions plus EXP-160 registry and profile only')
profile = json.loads((P / 'expressions/EXP-160.json').read_text())
check(profile['id'] == 'EXP-160' and profile['duration'] == 3.4 and len(profile['keyframes']) == 12, 'authored 3.4-second twelve-key performance')
check(profile['source_catalogue_sha256'] == 'ded1b313c36b66daf46f3426288ef4670b04703497323314754bba18e872b2bf', 'exact EXP-160 source catalogue')
check([f['time'] for f in profile['keyframes']] == [0.0, 0.3, 0.5, 0.65, 1.0, 1.35, 1.6, 1.85, 2.2, 2.4, 2.8, 3.4], 'exact authored key timing')
check(all(value == 0 for frame in [profile['keyframes'][0], profile['keyframes'][-1]] for value in frame['values'].values()), 'neutral endpoints')
check(all(frame['values'][axis] == 0 for frame in profile['keyframes'] for axis in ['gaze_x', 'gaze_y', 'hair_sway', 'brow_screen_left', 'brow_screen_right']), 'no gaze, hair, or legacy brow translation acting')
manifest = {}
for line in (P / MANIFEST_PATH).read_text().splitlines():
    digest, separator, name = line.partition('  ')
    check(separator == '  ' and name not in manifest and len(digest) == 64, 'manifest row ' + name)
    manifest[name] = digest
check(set(manifest) == (set(base['files']) | NEW_FILES) - {MANIFEST_PATH}, 'complete nonrecursive final manifest')
check(MIGRATION_PATH in manifest, 'manifest pins migration receipt')
for name, digest in manifest.items():
    check(sha(P / name) == digest, 'final manifest hash ' + name)
print(f'SHY_SCOPE_PASS checks={checks} parent_files=462 candidate_files=473 protected_pngs=182 prior_profiles=6 registry=7 changed_parent_files={len(ALLOWED)} new_files={len(NEW_FILES)}')

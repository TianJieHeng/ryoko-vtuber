"""Create a fresh source identity once. Never run from a validator."""
from numeric_model import W,canonical,sha

EXCLUDED={'INPUT_FREEZE.json','INPUT_FREEZE.sha256'}

def main():
    if any((W/name).exists() for name in EXCLUDED):
        raise SystemExit('Frozen identity already exists. Refusing to rewrite or repin.')
    files={p.relative_to(W).as_posix():sha(p) for p in sorted(W.rglob('*')) if p.is_file()}
    if any('__pycache__' in name or '/.godot/' in name for name in files):
        raise SystemExit('Remove generated caches in a separate authorized authoring step before freezing.')
    for required in ['comparators/EXP-091.json','COMPARATOR_091_BINDING.json','NUMERIC_COMPARATOR_091.json','RESULT.json']:
        if required not in files: raise SystemExit('Required final artifact missing: '+required)
    manifest={'identity':'EXP-092 recovery reconstruction r1, 2026-11-11; fresh UNAPPROVED identity',
        'status':'NUMERIC_AND_STATIC_PREPARATION_ONLY','previous_lost_freeze_restored':False,
        'approval':'UNAPPROVED','native_execution':False,'mp4_generated':False,
        'file_count':len(files),'files_sha256':files,
        'policy':'Read-only validators must never overwrite sources, receipts or this manifest. Any authorized later source/native-gate change needs a distinct new freeze with explicit lineage.'}
    with (W/'INPUT_FREEZE.json').open('x') as f: f.write(canonical(manifest))
    with (W/'INPUT_FREEZE.sha256').open('x') as f: f.write(sha(W/'INPUT_FREEZE.json')+'  INPUT_FREEZE.json\n')
    print('Created fresh immutable preparation freeze: '+sha(W/'INPUT_FREEZE.json'))

if __name__=='__main__': main()

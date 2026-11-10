"""Export a pinned local Git baseline. No network, rendering, or source checkout writes."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

w = Path(__file__).resolve().parent
source = Path(sys.argv[1]).resolve()
f = json.loads((w / 'BASELINE_REFERENCE.json').read_text())
commit = f['published_baseline_commit']
git = ['git', '-c', 'protocol.allow=never', '-C', str(source)]
env = dict(os.environ, GIT_NO_LAZY_FETCH='1')
assert subprocess.check_output(git + ['rev-parse', commit + '^{commit}'], text=True, env=env).strip() == commit
assert not (w / 'baseline').exists() and not (w / 'rig').exists(), 'Use a fresh package copy'
paths = ['ryoko_object_rig', str(Path(f['source_sheet'].removeprefix('baseline/')).parent), f['source_catalogue'].removeprefix('baseline/')]
(w / 'baseline').mkdir()
p = subprocess.Popen(git + ['archive', commit, '--', *paths], stdout=subprocess.PIPE, env=env)
try:
    subprocess.run(['tar', '-x', '-C', str(w / 'baseline')], stdin=p.stdout, check=True)
finally:
    p.stdout.close()
assert p.wait() == 0
root = w / 'baseline/ryoko_object_rig'
m = json.loads((root / 'APPROVED_SOURCE_MANIFEST.json').read_text())['files']
assert len(m) == f['source_files'] == 999
assert sum(n.endswith('.png') for n in m) == f['source_png_files'] == 184
for n, h in (m | f['extra_manifests_sha256']).items():
    src = root / n
    assert hashlib.sha256(src.read_bytes()).hexdigest() == h, n
    dst = w / 'rig' / n
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
ids = [r['id'] for r in json.loads((root / 'expressions/registry.json').read_text())['entries']]
assert ids == f['baseline_profile_ids'] and len(ids) == 36 and 'EXP-123' not in ids
f['source_files_sha256'] = m
f['source_rig'] = str(root)
for key, hashkey in [('source_sheet', 'source_sheet_sha256'), ('source_catalogue', 'catalogue_sha256')]:
    f[key] = str(w / f[key])
    assert hashlib.sha256(Path(f[key]).read_bytes()).hexdigest() == f[hashkey]
(w / 'BASELINE_FREEZE.json').write_text(json.dumps(f, indent=2) + '\n')
r = json.loads((w / 'SOURCE_REFERENCE.json').read_text())
r['sheet'] = f['source_sheet']
(w / 'SOURCE_REFERENCE.json').write_text(json.dumps(r, indent=2) + '\n')
print('Pinned approved36 baseline verified: 999 files, 184 PNGs, 36 profiles. Candidate profile and video untouched.')

for name,digest in r['panel_hashes'].items():
    p=Path(f['source_catalogue']).parent.parent/name
    assert hashlib.sha256(p.read_bytes()).hexdigest()==digest, name
print('All nine reference panels also verified.')

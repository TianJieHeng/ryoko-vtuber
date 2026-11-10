"""Freeze a fresh reproduction's relocated inputs; preserve historical evidence."""
import hashlib, json
from pathlib import Path

w = Path(__file__).resolve().parent
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
f = json.loads((w/'review_input_freeze.json').read_text())
relocatable = {'BASELINE_FREEZE.json','SOURCE_REFERENCE.json',
               'native_launcher/static.gd','native_launcher/motion.gd',
               'native_launcher/launcher.gd'}
changes = []
for n, old in f['sha256'].items():
    h = sha(w/n)
    if old != h:
        assert n in relocatable, f'Unexpected non-path input change: {n}'
        changes.append({'path':n,'historical_sha256':old,'reproduction_sha256':h})
archive = w/'historical_review_input_freeze.json'
assert not archive.exists(), 'Use a fresh reproduction copy'
archive.write_bytes((w/'review_input_freeze.json').read_bytes())
f['scope'] = 'New local reproduction inputs frozen before native capture, not the historical reviewed inputs or a new approval.'
f['historical_freeze_sha256'] = sha(archive)
f['path_relocations'] = changes
f['sha256'] = {n:sha(w/n) for n in f['sha256']}
(w/'review_input_freeze.json').write_text(json.dumps(f,indent=2)+'\n')
print('Fresh reproduction freeze recorded; historical input freeze preserved.')

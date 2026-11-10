"""Verify shipped hashes and all historical frozen inputs without fetching/rendering."""
from pathlib import Path
import hashlib,json
W=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
files=json.loads((W/'FILES.json').read_text())['files']
actual={str(p.relative_to(W)) for p in W.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='FILES.json'}
assert actual==set(files),'Unexpected or missing package files; validate pristine package before reproduction.'
for n,r in files.items():assert (W/n).stat().st_size==r['bytes'] and sha(W/n)==r['sha256'],n
sources=json.loads((W/'SOURCE_PACKAGE_PROVENANCE.json').read_text())['sources']
for n,r in sources.items():assert sha(W/n)==r['sha256'],n
freeze=json.loads((W/'review_input_freeze.json').read_text())
for n,digest in freeze['files'].items():
 p=W/n
 if n in ['README.md','BASELINE_FREEZE.json'] or n.startswith('native_launcher/'):p=W/'historical_inputs'/n
 assert sha(p)==digest,n
approval=json.loads((W/'APPROVAL_STATUS.json').read_text())
assert sha(W/'EXP-081.json')==approval['review_profile_sha256']
assert sha(W/approval['review_video'])==approval['review_video_sha256']
print(f'PASS: {len(files)} package files, {len(sources)} exact source artifacts, all {len(freeze["files"])} historical frozen inputs, exact approved profile/video.')

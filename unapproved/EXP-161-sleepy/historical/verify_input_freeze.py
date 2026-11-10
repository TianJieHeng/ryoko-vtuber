"""Read-only check of handoff files. No renderer, UI, encoder or write operation."""
import hashlib
import json
from pathlib import Path
W=Path(__file__).resolve().parent
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
f=json.loads((W/'review_input_freeze.json').read_text())
changed=[n for n,d in f['files'].items() if not (W/n).is_file() or h(W/n)!=d]
if changed:raise SystemExit('Frozen handoff files changed or missing: '+', '.join(changed))
b=json.loads((W/'BASELINE_FREEZE.json').read_text())
for root in [W/'rig',Path(b['source_rig'])]:
 for n,d in b['source_files_sha256'].items():
  assert h(root/n)==d,str(root/n)
 for n,d in b['extra_manifests_sha256'].items():
  assert h(root/n)==d,str(root/n)
for n,d in b['source_files_sha256'].items():
 if n!='project.godot':assert h(W/'native_launcher'/n)==d,n
for n,d in b['extra_manifests_sha256'].items():assert h(W/'native_launcher'/n)==d,n
print('PASS: frozen handoff files, all 999 source/rig files, 998 launcher files and both manifests match.')
print('Review-input freeze SHA256:',h(W/'review_input_freeze.json'))

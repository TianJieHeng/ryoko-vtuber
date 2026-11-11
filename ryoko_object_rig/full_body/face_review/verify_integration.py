#!/usr/bin/env python3
"""Exact source preservation for this integrated-face review, not native validation."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
m=json.loads((HERE/'publication_manifest.json').read_text())
assert sha(R/'APPROVED_SOURCE_MANIFEST.json')==m['baseline_manifest_sha256']
base=json.loads((R/'APPROVED_SOURCE_MANIFEST.json').read_text())
for name,digest in base['files'].items():
    expected=m['intended_existing_edits'].get(name,{}).get('after_sha256',digest)
    assert sha(R/name)==expected,'Unexpected source change: '+name
for name,edit in m['intended_existing_edits'].items():
    assert base['files'][name]==edit['before_sha256'],'Unexpected predecessor: '+name
for name,digest in m['candidate_files'].items():
    assert sha(R/name)==digest,'Changed candidate file: '+name
registry=json.loads((R/'expressions/registry.json').read_text())['entries']
assert len(registry)==47
report=json.loads((HERE/'all47_full_body_live_faces_15fps.json').read_text())
assert report['all_faces_changed'] and report['all_returned_to_exact_neutral']
assert set(report['expressions'])=={e['id'] for e in registry}
assert report['native_godot_capture'] is False
assert json.loads((HERE/'viewer_controls.json').read_text())['status']=='PASS'
print('FULL_BODY_EXPRESSION_REVIEW PASS: 47 original profiles/artwork preserved; exact intended integration changes; all47 reconstructed face-change/neutral evidence. Native capture and live pacing unverified.')

#!/usr/bin/env python3
"""Verify this portable unapproved backup without Git or network access."""
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'BACKUP_MANIFEST.json').read_text())
assert manifest['user_approved'] is False
assert manifest['approved_integration'] is False
expected = manifest['files']
actual_paths = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
assert actual_paths == set(expected) | {'BACKUP_MANIFEST.json'}, 'Missing or unexpected backup paths'
for name, expected_file in expected.items():
    path = root / name
    assert not path.is_symlink(), name
    data = path.read_bytes()
    assert len(data) == expected_file['size'], name
    assert hashlib.sha256(data).hexdigest() == expected_file['sha256'], name
    git_sha = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert git_sha == expected_file['git_blob_sha'], name
status = json.loads((root/'source/CHEEKY_WINK_STATUS.json').read_text())
assert status['approved_integration'] is False
if 'user_approved' in status:
    assert status['user_approved'] is False
profile = json.loads((root/'source/expressions/EXP-181.json').read_text())
assert profile['status'].startswith('Local'), profile['status']
registry = json.loads((root/'source/expressions/registry.json').read_text())
assert len(registry['entries']) == 13
assert registry['entries'][-1]['id'] == 'EXP-181'
source_files = {n.removeprefix('source/'):v['sha256'] for n,v in expected.items() if n.startswith('source/')}
digest = hashlib.sha256(json.dumps(source_files,sort_keys=True,separators=(',',':')).encode()).hexdigest()
assert digest == manifest['source_inventory_sha256']
print(json.dumps({'status':'PASS','files':len(expected)+1,'source_files':len(source_files),
                  'source_inventory_sha256':digest,'user_approved':False,'approved_integration':False}))

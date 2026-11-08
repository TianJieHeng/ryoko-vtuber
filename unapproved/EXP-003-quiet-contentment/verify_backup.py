#!/usr/bin/env python3
"""Offline exact historical-source and reference recovery verification."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
m=json.loads((root/'BACKUP_MANIFEST.json').read_text())
assert m['user_approved'] is False and m['approved_integration'] is False
expected=m['files']
assert {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}==set(expected)|{'BACKUP_MANIFEST.json'}
for name,row in expected.items():
 p=root/name;assert not p.is_symlink(),name;b=p.read_bytes()
 assert len(b)==row['size'] and hashlib.sha256(b).hexdigest()==row['sha256'],name
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob_sha'],name
source={n[7:]:r['sha256'] for n,r in expected.items() if n.startswith('source/')}
freeze=json.loads((root/'HISTORICAL_FREEZE.json').read_text())
assert source==freeze['files'] and len(source)==467
assert hashlib.sha256(json.dumps(source,sort_keys=True,separators=(',',':')).encode()).hexdigest()==m['source_inventory_sha256']=='caf000a386cc7bda0bce4c8e0c32a4923ee057726b3e406185cb436779f3bf10'
assert sum(p.endswith('.png') for p in source)==182
registry=json.loads((root/'source/expressions/registry.json').read_text())
assert [x['id'] for x in registry['entries']]==['EXP-163','EXP-005','EXP-001','EXP-006','EXP-107','EXP-007','EXP-003']
profile=json.loads((root/'source/expressions/EXP-003.json').read_text())
assert profile['duration']==1.9 and len(profile['keyframes'])==9
assert profile['source_catalogue_sha256']=='4636be0c5bf2df17302b9ea131aa498a74100a7d81062beb1c73d1f6d19e5007'
refs=json.loads((root/'original_reference/INDEX.json').read_text())
assert len(refs['files'])==10
for row in refs['files']:
 entry=expected['original_reference/'+row['name']]
 assert entry['sha256']==row['sha256'] and entry['git_blob_sha']==row['git_blob_sha']
summary=json.loads((root/'VALIDATION_SUMMARY.json').read_text())
assert summary['user_approved'] is False and summary['user_rejected'] is False
assert summary['current_visual_compatibility']=='NOT_REPLAYED'
print(json.dumps({'status':'PASS','files':len(expected)+1,'source_files':len(source),'source_inventory_sha256':m['source_inventory_sha256'],'exact_historical_source':True,'user_approved':False,'approved_integration':False}))

#!/usr/bin/env python3
"""Offline exact source, reference and unapproved-status recovery verification."""
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
assert len(source)==605
assert hashlib.sha256(json.dumps(source,sort_keys=True,separators=(',',':')).encode()).hexdigest()==m['source_inventory_sha256']
freeze=json.loads((root/'source/CONFIDENT_DENIAL_CAPTURE_FREEZE.json').read_text())
assert len(freeze['files'])==604 and freeze['files']=={n:h for n,h in source.items() if n!='CONFIDENT_DENIAL_CAPTURE_FREEZE.json'}
status=json.loads((root/'source/CONFIDENT_DENIAL_STATUS.json').read_text())
assert status['approved'] is False and status['approved_integration'] is False
assert len(status['approved_profile_ids'])==12
assert status['unapproved_profile_ids']==['EXP-158','EXP-181','EXP-102','EXP-116']
registry=json.loads((root/'source/expressions/registry.json').read_text())
assert len(registry['entries'])==16 and registry['entries'][-1]['id']=='EXP-116'
plan=json.loads((root/'capture_plan.json').read_text())
assert plan['source_freeze_sha256']==source['CONFIDENT_DENIAL_CAPTURE_FREEZE.json'] and plan['profile_sha256']==source['expressions/EXP-116.json']
assert plan['checkpoints']==330
for id in status['unapproved_profile_ids']:
 p=json.loads((root/f'source/expressions/{id}.json').read_text());assert 'unapproved' in p['status'].lower() or 'user approval pending' in p['status'].lower(),id
print(json.dumps({'status':'PASS','files':len(expected)+1,'source_files':len(source),'source_inventory_sha256':m['source_inventory_sha256'],'frozen_source_inventory_sha256':freeze['inventory_sha256'],'source_is_exact_capture':True,'user_approved':False,'approved_integration':False}))

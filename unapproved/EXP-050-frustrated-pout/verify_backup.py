#!/usr/bin/env python3
"""Verify a relocated exact-source recovery snapshot without network or Godot."""
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
assert len(source)==617
assert hashlib.sha256(json.dumps(source,sort_keys=True,separators=(',',':')).encode()).hexdigest()==m['source_inventory_sha256']
freeze=json.loads((root/'source/FRUSTRATED_POUT_CAPTURE_FREEZE.json').read_text())
assert len(freeze['files'])==616 and freeze['files']=={n:h for n,h in source.items() if n!='FRUSTRATED_POUT_CAPTURE_FREEZE.json'}
assert hashlib.sha256(json.dumps(freeze['files'],sort_keys=True,separators=(',',':')).encode()).hexdigest()==freeze['inventory_sha256']
status=json.loads((root/'source/FRUSTRATED_POUT_STATUS.json').read_text())
assert status['approved'] is False and status['approved_integration'] is False
assert status['approved_profile_ids']==['EXP-163','EXP-005','EXP-001','EXP-006','EXP-107','EXP-007','EXP-002','EXP-152','EXP-160','EXP-177','EXP-164','EXP-021']
assert status['unapproved_profile_ids']==['EXP-158','EXP-181','EXP-102','EXP-116','EXP-050']
registry=json.loads((root/'source/expressions/registry.json').read_text())
assert len(registry['entries'])==17 and registry['entries'][-1]['id']=='EXP-050'
plan=json.loads((root/'capture_plan.json').read_text())
assert plan['source_freeze_sha256']==source['FRUSTRATED_POUT_CAPTURE_FREEZE.json'] and plan['profile_sha256']==source['expressions/EXP-050.json']
assert plan['source_inventory_sha256']==freeze['inventory_sha256'] and plan['checkpoints']==541
for id in status['unapproved_profile_ids']:
 p=json.loads((root/f'source/expressions/{id}.json').read_text());assert 'unapproved' in p['status'].lower() or 'user approval pending' in p['status'].lower(),id
refs=json.loads((root/'original_reference/INDEX.json').read_text())
assert len(refs['files'])==10
for r in refs['files']:
 assert expected['original_reference/'+r['name']]['git_blob_sha']==r['git_blob_sha']
 assert expected['original_reference/'+r['name']]['sha256']==r['sha256']
gates=json.loads((root/'gate_records/INDEX.json').read_text())
for r in gates['records']:
 assert expected['gate_records/'+r['backup_name']]['sha256']==r['sha256']
summary=json.loads((root/'VALIDATION_SUMMARY.json').read_text())
assert summary['user_approved'] is False and summary['approved_integration'] is False
assert summary['normal_speed_playback_observed'] is False and summary['source_is_exact_capture'] is True
actual=json.loads((root/'gate_records/ACTUAL_REVIEW_FREEZE.json').read_text())
assert actual['source_freeze_sha256']==plan['source_freeze_sha256']
assert actual['capture_plan_sha256']==expected['capture_plan.json']['sha256']
assert actual['files']['REPORT_ACTUAL.md']==expected['gate_records/REPORT_ACTUAL.md']['sha256']
assert actual['prior_review_freeze_sha256']==expected['gate_records/PRE_CAPTURE_REVIEW_FREEZE.json']['sha256']
print(json.dumps({'status':'PASS','files':len(expected)+1,'source_files':len(source),'source_inventory_sha256':m['source_inventory_sha256'],'frozen_source_inventory_sha256':freeze['inventory_sha256'],'source_is_exact_capture':True,'user_approved':False,'approved_integration':False}))

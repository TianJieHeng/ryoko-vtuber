from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((R/'CURRENT_SOURCE_MANIFEST.json').read_text());frozen=json.loads((R/'QUIET_SADNESS_CAPTURE_FREEZE.json').read_text())
assert sha(R/'QUIET_SADNESS_CAPTURE_FREEZE.json')==m['capture_source_manifest_sha256']
for f,h in m['files'].items():assert sha(R/f)==h,f
allowed=set(m['metadata_overlay_allowed_paths'])
for f,h in frozen['files'].items():
 if f not in allowed:assert sha(R/f)==h,('captured implementation changed',f)
 else:assert sha(R/'historical_capture_metadata'/f)==h,('captured metadata not preserved',f)
reg=json.loads((R/'expressions/registry.json').read_text());status=json.loads((R/'RELEASE.json').read_text())
assert len(reg['entries'])==12 and status['approved_published_count']==11 and not status['published'] and not status['user_approved']
assert [e['id'] for e in reg['entries']]==status['authored_registry'] and status['pending_review']==['EXP-021']
lines=(R/'SOURCE_FILES.sha256').read_text().splitlines()
for line in lines:
 h,f=line.split('  ',1);assert sha(R/f)==h,f
expected=set(m['files'])|{'CURRENT_SOURCE_MANIFEST.json'}
assert {line.split('  ',1)[1] for line in lines}==expected
seen={str(p.relative_to(R)) for p in R.rglob('*') if p.is_file() and '.godot' not in p.relative_to(R).parts}
allowed_generated_uids={f for f in seen if f.endswith(('.uid','.import')) and f not in expected}
assert seen-allowed_generated_uids==expected|{'SOURCE_FILES.sha256'},'unexpected package files'
print(json.dumps({'status':'PASS','files':len(m['files'])+2,'authored_local':12,'approved_published':11,'all_captured_implementation_preserved':True,'metadata_overlay_only':True}))

from pathlib import Path
import hashlib,json,sys
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((R/'POST_CONFESSION_SHYNESS_SOURCE_MANIFEST.json').read_text());frozen=json.loads((R/'POST_CONFESSION_SHYNESS_CAPTURE_FREEZE.json').read_text())
assert sha(R/'POST_CONFESSION_SHYNESS_CAPTURE_FREEZE.json')==m['capture_source_manifest_sha256']
for f,h in m['files'].items():assert sha(R/f)==h,f
allowed=set(m['metadata_overlay_allowed_paths'])
for f,h in frozen['files'].items():
 if f not in allowed:assert sha(R/f)==h,('captured implementation changed',f)
 else:assert sha(R/'post_confession_shyness_capture_metadata'/f)==h,('captured metadata not preserved',f)
reg=json.loads((R/'expressions/registry.json').read_text());status=json.loads((R/'RELEASE.json').read_text())
assert len(reg['entries'])==13 and status['approved_published_count']==12 and not status['approved_integration'] and not status['user_approved']
assert [e['id'] for e in reg['entries']]==status['authored_registry'] and status['pending_review']==['EXP-158'] and status['backup_is_not_approval']
assert sha(R/'expressions/EXP-158.json')==m['profile_sha256']
old_profile=json.loads((R/'post_confession_shyness_capture_metadata/expressions/EXP-158.json').read_text());new_profile=json.loads((R/'expressions/EXP-158.json').read_text())
assert sha(R/'post_confession_shyness_capture_metadata/expressions/EXP-158.json')==m['captured_profile_sha256']
assert new_profile['interpolation']==old_profile['interpolation'].replace('neutral at4.20','neutral at 4.20')
new_profile['interpolation']=old_profile['interpolation'];assert new_profile==old_profile,'profile timing/control metadata changed'
lines=(R/'POST_CONFESSION_SHYNESS_FILES.sha256').read_text().splitlines()
for line in lines:
 h,f=line.split('  ',1);assert sha(R/f)==h,f
expected=set(m['files'])|{'POST_CONFESSION_SHYNESS_SOURCE_MANIFEST.json'}
assert {line.split('  ',1)[1] for line in lines}==expected
seen={str(p.relative_to(R)) for p in R.rglob('*') if p.is_file() and '.godot' not in p.relative_to(R).parts}
generated={f for f in seen-expected if (f.endswith('.gd.uid') and f[:-4] in expected) or (f.endswith('.import') and f[:-7] in expected)}
assert seen-generated==expected|{'POST_CONFESSION_SHYNESS_FILES.sha256'},'unexpected package files'
proof=json.loads((R/'source_references/post_confession_shyness_original_proof.json').read_text());assert len(proof['files'])==10
verified_originals=0
for item in proof['files']:
 assert 'local_path' not in item and item['relative_reference_path']=='../original_reference/'+item['filename']
 ref=R/item['relative_reference_path']
 if '--require-originals' in sys.argv:assert ref.exists(),('required original missing',item['filename'])
 if ref.exists():
  assert sha(ref)==item['sha256'],('original source mismatch',item['filename']);verified_originals+=1
print(json.dumps({'status':'PASS','files':len(m['files'])+2,'authored_local':13,'approved_published':12,'pending_approval':['EXP-158'],'all_captured_implementation_preserved':True,'metadata_overlay_only':True,'original_reference_files_verified':verified_originals}))

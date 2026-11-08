from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
digest=lambda d:hashlib.sha256(json.dumps(d,sort_keys=True,separators=(',',':')).encode()).hexdigest()
read=lambda n:json.loads((P/n).read_text())
actual={p.relative_to(P).as_posix():sha(p) for p in P.rglob('*') if p.is_file()}
review=read('source_references/quiet_sadness_approved_review.json');frozen=review['files'];base=review['parent_files']
assert len(frozen)==581 and digest(frozen)==review['inventory_sha256']=='2ffdd7fd8fdad85deb3d7a1e9ac3524958686bae3a1f9b6d3a987e3d78e597aa'
assert len(base)==564 and digest(base)==review['parent_inventory_sha256']=='49069126653f1d7c1596e6ff92db3337f84fb0f8585d5346ebf09921879553e2'
overlay={'README.md','CONTROL_API.md','PACKAGING.md','LOCAL_CONTROL_BRIDGE.md','RELEASE.json','QUIET_SADNESS_STATUS.json','QUIET_SADNESS_SCOPE.md','expressions/EXP-021.json','SOURCE_FILES.sha256'}
added={'QUIET_SADNESS_PUBLICATION_VALIDATION.md','PUBLICATION_SOURCE_MANIFEST.json','source_references/quiet_sadness_approved_review.json','tools/verify_quiet_sadness_publication.py'}
assert set(actual)==set(frozen)|added and len(actual)==585
assert {n for n,h in frozen.items() if actual[n]!=h}==overlay
assert set(base)<=set(actual)
profile=read('expressions/EXP-021.json');old=json.loads(review['profile_text']);oldhash=hashlib.sha256(review['profile_text'].encode()).hexdigest()
assert oldhash==frozen['expressions/EXP-021.json']=='80d960bf10b64c3df7617533d5ba8f6c868d9df5506c56ba14a368791d749571'
assert set(profile)==set(old) and {k for k in profile if profile[k]!=old[k]}=={'status'}
assert profile['status']=='User-approved Quiet sadness; published with the containing repository commit'
prior=['EXP-163','EXP-005','EXP-001','EXP-006','EXP-107','EXP-007','EXP-002','EXP-152','EXP-160','EXP-177','EXP-164'];ids=prior+['EXP-021']
assert [e['id'] for e in read('expressions/registry.json')['entries']]==ids
assert {p.stem for p in (P/'expressions').glob('EXP-*.json')}==set(ids)-{'EXP-163'}
for entry in read('expressions/registry.json')['entries']:
 if entry['id'] in prior:
  n=entry['path'].removeprefix('res://');assert actual[n]==base[n],n
for n,h in base.items():
 if n.endswith(('.gd','.gdshader','.png','.tscn','.uid','.import','.py')):assert actual[n]==h,n
assert sum(n.endswith('.png') for n in actual)==182
release=read('RELEASE.json');status=read('QUIET_SADNESS_STATUS.json');manifest=read('PUBLICATION_SOURCE_MANIFEST.json')
assert release['user_approved'] is release['published'] is True and release['approved_published_count']==12
assert release['authored_registry']==release['approved_registry']==ids and release['approved_predecessors']==prior and release['pending_review']==[]
assert status['published'] is status['user_approved'] is True and status['approved_count']==12 and status['user_approval_pending'] is False
assert release['reviewed_profile_sha256']==manifest['reviewed_profile_sha256']==oldhash
assert release['published_profile_sha256']==manifest['published_profile_sha256']==actual['expressions/EXP-021.json']
assert release['approved_review_inventory_sha256']==manifest['review_inventory_sha256']==review['inventory_sha256']
assert review['parent_commit']==release['base_main']==status['main_base']==manifest['base_commit']=='2d46f72704ddf2a329b44a87cd24c66d5fe92568'
assert manifest['approved_published']==12 and manifest['files']=={n:h for n,h in actual.items() if n not in {'PUBLICATION_SOURCE_MANIFEST.json','SOURCE_FILES.sha256'}}
lines=(P/'SOURCE_FILES.sha256').read_text().splitlines();checks={}
for line in lines:
 h,n=line.split('  ',1);assert n not in checks;checks[n]=h
assert checks=={n:h for n,h in actual.items() if n!='SOURCE_FILES.sha256'}
print(json.dumps({'status':'PASS','files':len(actual),'pngs':182,'approved_published':12,'unchanged_predecessor_profiles':11,'review_inventory_sha256':review['inventory_sha256'],'publication_inventory_sha256':digest(actual),'profile_status_only':True,'all_historical_receipts_guards_tests_and_runtime_preserved':True}))

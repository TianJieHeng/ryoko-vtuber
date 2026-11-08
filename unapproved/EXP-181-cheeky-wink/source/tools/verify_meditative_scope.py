#!/usr/bin/env python3
import sys,json
sys.dont_write_bytecode=True
from meditative_source_guard import ROOT as P,ALLOWED,NEW_FILES,MIGRATION,MANIFEST,PROFILE_HASH,read_contract,sha,meditative_registry_matches
b,m=read_contract();expected=set(b['files'])|NEW_FILES
actual={p.relative_to(P).as_posix() for p in P.rglob('*') if p.is_file() and not ('.godot' in p.parts or '__pycache__' in p.parts)}
assert actual==expected,'exact source paths'
assert not any(p.is_symlink() for p in P.rglob('*'))
for n,h in b['files'].items():
 if n==MANIFEST:continue
 assert sha(P/n)==(m['files'][n]['candidate_sha256'] if n in ALLOWED else h),'immutable or exact support '+n
for n,h in m['new_files'].items():assert sha(P/n)==h,'new exact '+n
assert meditative_registry_matches(),'exact ten approved profiles'
assert {p.relative_to(P).as_posix() for p in P.rglob('*.png')}=={n for n in b['files'] if n.endswith('.png')}
p=json.loads((P/'expressions/EXP-177.json').read_text());assert sha(P/'expressions/EXP-177.json')==PROFILE_HASH
assert p['duration']==3.9 and [k['time'] for k in p['keyframes']]==[0,1.2,1.75,2.35,2.85,3.35,3.9]
assert [k['values']['blink_R'] for k in p['keyframes']]==[0,1,1,1,.64,.42,0]
for k in p['keyframes']:
 assert k['values']['blink_R']==k['values']['blink_L']
 assert all(v==0 for key,v in k['values'].items() if key not in ['blink_R','blink_L'])
assert p['source_catalogue_sha256']=='793f57f3bdfb9974dcd076d5e84af20c356e15d0c98db0b2985e3ab65eeb731b'
manifest={}
for row in (P/MANIFEST).read_text().splitlines():
 h,sep,n=row.partition('  ');assert sep=='  ' and n not in manifest;manifest[n]=h
assert set(manifest)==expected-{MANIFEST} and all(sha(P/n)==h for n,h in manifest.items())
status=json.loads((P/'MEDITATIVE_STATUS.json').read_text());assert status['published'] is True and status['user_approved'] is True and status['approved_registry']==[e['id'] for e in json.loads((P/'expressions/registry.json').read_text())['entries']]
release=json.loads((P/'RELEASE.json').read_text());assert release['published'] is True and release['user_approved'] is True and release['authored_registry']==release['approved_registry']==status['approved_registry'] and release['approved_predecessors']==status['approved_registry'][:-1], 'ten approved with exact predecessor list'
print('MEDITATIVE_REBASED_SCOPE_PASS parent=524 files='+str(len(expected))+' pngs=182 registry=10 runtime_art_prior_profiles_unchanged=true')

#!/usr/bin/env python3
"""Portable, read-only exact candidate/predecessor/cache guard. Run with python -B."""
from pathlib import Path
import argparse,hashlib,json,math
P=Path(__file__).resolve().parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
digest=lambda value:hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def inv(root):
 assert root.is_dir(),('missing tree',str(root))
 assert not any(p.is_symlink() for p in root.rglob('*')),'symlinks forbidden'
 return {p.relative_to(root).as_posix():sha(p) for p in sorted(root.rglob('*')) if p.is_file()}
def verify(predecessor,runtime=False):
 contract=json.loads((P/'source_references/daring_provocation_guard_contract.json').read_text());manifest=json.loads((P/'DARING_PROVOCATION_SOURCE_MANIFEST.json').read_text())
 base=contract['approved_files'];cache=contract['cache'];files=manifest['files']
 assert len(base)==646 and digest(base)==contract['approved_inventory_sha256']=='37d2ac563100386fdc40be0cc4f7595dfb40cff16fed57f1a7b25a6e7f8aa043'
 assert predecessor.resolve()!=P.resolve() and inv(predecessor)==base,'distinct immutable approved predecessor must be exact'
 assert digest(files)==manifest['inventory_sha256']
 expected=files|{'DARING_PROVOCATION_SOURCE_MANIFEST.json':sha(P/'DARING_PROVOCATION_SOURCE_MANIFEST.json'),'DARING_PROVOCATION_SOURCE_FILES.sha256':sha(P/'DARING_PROVOCATION_SOURCE_FILES.sha256')}
 if runtime:expected|=cache['generated_sidecars']|{'.godot/imported/'+p:h for p,h in cache['imported_resources'].items()}|{'.godot/'+p:h for p,h in cache['cache_metadata'].items()}
 assert inv(P)==expected,'extra/missing/changed candidate file rejected, including arbitrary sidecars or cache'
 checksum={line[66:]:line[:64] for line in (P/'DARING_PROVOCATION_SOURCE_FILES.sha256').read_text().splitlines()}
 assert checksum==files|{'DARING_PROVOCATION_SOURCE_MANIFEST.json':sha(P/'DARING_PROVOCATION_SOURCE_MANIFEST.json')}
 assert [p for p in base if files.get(p)!=base[p]]==['expressions/registry.json'],'only inherited registry may change'
 assert set(files)-set(base)==set(manifest['added_paths']),'explicit additional support files only'
 assert len([p for p in files if p.endswith('.png')])==182 and all(files[p]==base[p] for p in files if p.endswith('.png'))
 approved=json.loads((predecessor/'expressions/registry.json').read_text());reg=json.loads((P/'expressions/registry.json').read_text())
 assert reg['entries'][:-1]==approved['entries'] and reg['entries'][-1]=={'id':'EXP-114','path':'res://expressions/EXP-114.json','aliases':['daring-provocation','daring_provocation'],'trigger_phase':'quiet_composure'} and len(reg['entries'])==19
 assert len(list((P/'expressions').glob('EXP-*.json')))==18
 status=json.loads((P/'DARING_PROVOCATION_STATUS.json').read_text());assert not status['approved'] and not status['approved_integration'] and status['approved_profile_count']==18 and status['pending_profile_ids']==['EXP-114']
 assert status['approved_profile_ids']==[e['id'] for e in approved['entries']]
 profile=json.loads((P/'expressions/EXP-114.json').read_text());anchors=json.loads((P/'source_references/daring_provocation_source_anchor_map.json').read_text());static=json.loads((P/'source_references/daring_provocation_accepted_static_plan.json').read_text());timing=json.loads((P/'source_references/daring_provocation_timing.json').read_text())
 cases={int(x['source_key']):x for x in static['candidate_cases']};assert list(cases)==[1,3,4,5,6,7,9]
 assert profile['duration']==3.8 and len(profile['keyframes'])==14
 for frame,anchor,key in zip(profile['keyframes'],anchors['anchors'],timing['keys'],strict=True):
  t,phase,kp=key
  assert frame=={'time':t,'phase':phase,'values':cases[kp]['values']} and anchor['values']==frame['values'] and anchor['key_pose']==kp
  assert set(frame['values'])==set(cases[1]['values']) and all(type(v) in [int,float] and math.isfinite(v) for v in frame['values'].values())
  assert frame['values']['mouth_width_screen_left']==frame['values']['mouth_width_screen_right']==0
 assert manifest['profile_sha256']==sha(P/'expressions/EXP-114.json')
 if runtime:
  for png,row in cache['png_to_resource'].items():
   assert sha(P/png)==row['source_sha256']==base[png]
   for path_key,hash_key in [('sidecar_path','sidecar_sha256'),('resource_path','resource_sha256'),('md5_path','md5_sha256')]:assert sha(P/row[path_key])==row[hash_key]
   assert 'source_file="res://'+png+'"' in (P/row['sidecar_path']).read_text()
 return {'status':'PASS','source_files':len(files)+2,'approved_profiles':18,'pending_profile_ids':['EXP-114'],'pngs_exact':182,'immutable_predecessor_files':646,'source_inventory_sha256':manifest['inventory_sha256'],'profile_sha256':manifest['profile_sha256'],'runtime_cache_exact':runtime}
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--predecessor',type=Path,required=True);parser.add_argument('--runtime',action='store_true');args=parser.parse_args()
 print(json.dumps(verify(args.predecessor,args.runtime)))

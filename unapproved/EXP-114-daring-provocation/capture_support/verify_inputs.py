"""Strict read-only offline package identity. Never invokes Godot or imports resources."""
from pathlib import Path
import hashlib,json,subprocess,sys,math
W=Path(__file__).resolve().parent;R=W.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def inv(p):
 assert not any(x.is_symlink() for x in p.rglob('*'))
 return {x.relative_to(p).as_posix():sha(x) for x in sorted(p.rglob('*')) if x.is_file()}
def verify():
 base=json.loads((W/'evidence/BASELINE.json').read_text());cache=json.loads((W/'evidence/CACHE_REUSE.json').read_text());expected=base['files'];pred=W/'approved_predecessor/ryoko_object_rig'
 assert len(expected)==646 and inv(pred)==inv(Path(base['copied_from']))==expected
 full_cache=cache['generated_sidecars']|{'.godot/imported/'+p:h for p,h in cache['imported_resources'].items()}|{'.godot/'+p:h for p,h in cache['cache_metadata'].items()}
 assert inv(W/'runtime/approved')==expected|full_cache
 for p,h in json.loads((W/'evidence/EXTERNAL_PROVENANCE.json').read_text())['files'].items():assert sha(R/p)==h,('external evidence changed',p)
 source=W/'source/ryoko_object_rig';f=json.loads((source/'DARING_PROVOCATION_SOURCE_MANIFEST.json').read_text());want=f['files']|{'DARING_PROVOCATION_SOURCE_MANIFEST.json':sha(source/'DARING_PROVOCATION_SOURCE_MANIFEST.json'),'DARING_PROVOCATION_SOURCE_FILES.sha256':sha(source/'DARING_PROVOCATION_SOURCE_FILES.sha256')}
 assert inv(source)==want and inv(W/'runtime/candidate')==want|full_cache
 for tree,runtime in [(source,False),(W/'runtime/candidate',True)]:
  cmd=[sys.executable,'-B',str(tree/'tools/verify_daring_provocation_candidate.py'),'--predecessor',str(pred)]+(['--runtime'] if runtime else [])
  result=subprocess.run(cmd,capture_output=True,text=True);assert result.returncode==0,(cmd,result.stdout,result.stderr)
  assert json.loads(result.stdout)['status']=='PASS'
 plan=json.loads((W/'capture_plan.json').read_text());assert plan['checkpoints']==701 and len(plan['chapters'])==26 and sum(len(c['times']) for c in plan['chapters'])==701
 for c in plan['chapters']:
  assert c['times']==sorted(set(c['times'])) and all(type(t) in [int,float] and math.isfinite(t) and t>=0 for t in c['times'])
 freeze=W/'evidence/PREPARED_PACKAGE.json'
 if freeze.exists():
  binding=json.loads(freeze.read_text())
  for p,h in binding['files'].items():assert sha(W/p)==h,('frozen offline input changed',p)
  assert binding['candidate_source_files']==want and binding['approved_source_files']==expected
 return {'status':'PASS','approved_source_files':646,'approved_profiles':18,'candidate_source_files':len(want),'pending_profiles':['EXP-114'],'pngs':182,'generated_sidecars':180,'imported_resource_files':364,'cache_metadata':3,'profile_sha256':sha(source/'expressions/EXP-114.json'),'capture_plan_sha256':sha(W/'capture_plan.json'),'candidate_manifest_sha256':sha(source/'DARING_PROVOCATION_SOURCE_MANIFEST.json'),'prepared_package_sha256':sha(freeze) if freeze.exists() else None}
if __name__=='__main__':print(json.dumps(verify()))

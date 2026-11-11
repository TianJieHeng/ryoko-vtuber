"""Run inventory and semantic tamper probes only in a disposable copy."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,sys
p=argparse.ArgumentParser();p.add_argument('output',type=Path);args=p.parse_args()
R=Path(__file__).resolve().parents[1];W=args.output.resolve();T=W/'guard_negative_copy';guard=R/'tools/verify_approved_integration.py';V='validation/approved_batch39/'
assert not W.is_relative_to(R),'Use an output directory outside production'
assert not W.exists() or not any(W.iterdir()),'Output must be new or empty'
W.mkdir(parents=True,exist_ok=True)
shutil.copytree(R,T,ignore=shutil.ignore_patterns('.godot','__pycache__'))
def read(n):return json.loads((T/n).read_text())
def put(n,d):(T/n).write_text(json.dumps(d,indent=2)+'\n')
def sha(n):return hashlib.sha256((T/n).read_bytes()).hexdigest()
def repin():
 m=read('APPROVED_SOURCE_MANIFEST.json');m['files']={n:sha(n) for n in m['files']};put('APPROVED_SOURCE_MANIFEST.json',m)
 (T/'APPROVED_SOURCE_FILES.sha256').write_text(''.join(f'{h}  {n}\n' for n,h in sorted(m['files'].items())))
cases=[]
def run(label,mutate,files,semantic=False):
 files=list(set(files+['APPROVED_SOURCE_MANIFEST.json','APPROVED_SOURCE_FILES.sha256']));before={n:(T/n).read_bytes() if (T/n).exists() else None for n in files}
 try:
  mutate()
  if semantic:repin()
  p=subprocess.run([sys.executable,str(guard),str(T)],capture_output=True,text=True)
  assert p.returncode!=0,label+' corruption was accepted'
  cases.append({'name':label,'expected_rejection_observed':True,'exit_code':p.returncode,'diagnostic':p.stderr[-1400:]})
 finally:
  for n,b in before.items():
   if b is None:(T/n).unlink(missing_ok=True)
   else:(T/n).write_bytes(b)
  p=subprocess.run([sys.executable,str(guard),str(T)],capture_output=True,text=True)
  assert p.returncode==0,label+' restore failed '+p.stderr
run('new approved profile byte corruption',lambda:(T/'expressions/EXP-129.json').write_text('{}\n'),['expressions/EXP-129.json'])
png=next(n for n in read('APPROVED_SOURCE_MANIFEST.json')['files'] if n.endswith('.png'))
run('protected PNG byte corruption',lambda:(T/png).write_bytes(b'corrupt'),[png])
run('unexpected source file',lambda:(T/'unexpected_guard_test.txt').write_text('extra\n'),['unexpected_guard_test.txt'])
run('missing registry file',lambda:(T/'expressions/registry.json').unlink(),['expressions/registry.json'])
prior_profile=read('historical_capture_metadata/approved36_before_mental_arithmetic/expressions/registry.json')['entries'][0]['path'][6:]
def bad_prior_profile():
 d=read(prior_profile);d['title']+=' tampered';put(prior_profile,d)
run('prior profile corruption with manifest repinned',bad_prior_profile,[prior_profile],True)
def bad_native():
 n=V+'native_parity/RESULT.json';d=read(n);d['records'][0]['hashes'][0]='0'*64;d['records'][0]['expected_hashes'][0]='0'*64;put(n,d)
 n=V+'native_parity/independent_png_verification.json';d=read(n);d['records'][0]['sha256_rgba']='0'*64;d['records'][0]['expected']='0'*64;put(n,d)
 d=read('APPROVED_INTEGRATION_TEST_RESULTS.json')
 for name in ['native_parity/RESULT.json','native_parity/independent_png_verification.json']:d['receipts'][name]['sha256']=sha(V+name)
 put('APPROVED_INTEGRATION_TEST_RESULTS.json',d)
run('self-consistent forged parity fails approved-capture linkage',bad_native,[V+'native_parity/RESULT.json',V+'native_parity/independent_png_verification.json','APPROVED_INTEGRATION_TEST_RESULTS.json'],True)
def bad_preservation():
 n=V+'native_parity/source_preservation.json';d=read(n);d['production_differences']=[{'path':'expression_rig.gd','changed':True}];put(n,d)
run('source preservation difference rejected after repin',bad_preservation,[V+'native_parity/source_preservation.json'],True)
report={'status':'PASS','cases':len(cases),'failures':[],'results':cases,'scope':'Disposable-copy negative probes only. Each tamper rejected and pristine restored guard passed; semantic probes update checksums to test actual preservation and approved-capture linkage.'}
(W/'guard_negative_tests.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='results'}));shutil.rmtree(T)

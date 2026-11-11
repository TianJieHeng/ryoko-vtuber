"""Tamper disposable copies only; never modifies the source integration."""
from pathlib import Path
import json,shutil,subprocess,sys,tempfile
R=Path(__file__).resolve().parents[1]
out=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else None
if out is None or out.exists() or out.is_relative_to(R):raise SystemExit('Provide a new external output directory')
out.mkdir(parents=True)
def call(r):return subprocess.run([sys.executable,'-B',str(r/'tools/verify_approved_integration.py'),str(r)],capture_output=True,text=True)
base=call(R);assert base.returncode==0,base.stderr
identity=json.loads((R/'validation/approved_exasperated_sigh/approved_review_identity.json').read_text())['profiles']
probes=[('prior_profile','yawn_performance.json','append'),('new_profile','expressions/EXP-046.json','append'),('registry','expressions/registry.json','append'),('runtime','expression_rig.gd','append'),('png',str(next(R.rglob('*.png')).relative_to(R)),'append'),('approved_video',identity[0]['video_path'],'append'),('review_receipt',identity[0]['motion_path'],'append'),('approval','validation/approved_exasperated_sigh/current_user_approvals.json','append'),('predecessor_manifest','historical_capture_metadata/approved45_before_exasperated_sigh/APPROVED_SOURCE_MANIFEST.json','append'),('missing_profile','expressions/EXP-046.json','delete'),('unexpected_file','unregistered_extra.txt','append'),('python_receipt','validation/approved_exasperated_sigh/python_model_checks.json','append')]
records=[]
with tempfile.TemporaryDirectory(prefix='approved46_guard_',dir=out) as tmp:
 root=Path(tmp)/'rig';shutil.copytree(R,root,ignore=shutil.ignore_patterns('.godot','__pycache__','*.pyc'))
 for name,path,action in probes:
  p=root/path;original=p.read_bytes() if p.exists() else None
  if action=='delete':p.unlink()
  else:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((original or b'')+b'\nTAMPER\n')
  res=call(root);assert res.returncode!=0,'Tamper escaped guard: '+name
  records.append({'probe':name,'path':path,'guard_exit':res.returncode,'rejected':True})
  if original is None:p.unlink()
  else:p.write_bytes(original)
  restored=call(root);assert restored.returncode==0,restored.stderr
result={'status':'PASS','tamper_cases':len(records),'all_rejected':True,'clean_source_passed':True,'restored_copy_passes':len(records),'records':records,'scope':'Disposable-copy source/identity guard probes. No engine execution.'}
(out/'guard_negative_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

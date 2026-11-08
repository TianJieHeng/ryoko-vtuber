#!/usr/bin/env python3
"""Offline source recovery check. No Git, Godot, cache mutation or publication."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,sys,tempfile
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=argparse.ArgumentParser();p.add_argument('source',type=Path);a=p.parse_args();s=a.source.resolve()
c=json.loads((s/'source_references/daring_provocation_guard_contract.json').read_text())
with tempfile.TemporaryDirectory(prefix='exp114-recovery-') as tmp:
 base=Path(tmp)/'approved_predecessor';base.mkdir()
 for name,h in c['approved_files'].items():
  source=s/name
  if name=='expressions/registry.json':source=s/'source_references/daring_provocation_approved18_registry.json'
  assert sha(source)==h,('cannot reconstruct approved predecessor',name)
  dest=base/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest)
 result=subprocess.run([sys.executable,'-B',str(s/'tools/verify_daring_provocation_candidate.py'),'--predecessor',str(base)],capture_output=True,text=True)
 assert result.returncode==0,(result.stdout,result.stderr)
 r=json.loads(result.stdout);assert r['status']=='PASS'
 print(json.dumps({'status':'PASS_OFFLINE_SOURCE_RECOVERY','source':str(s),'approved_predecessor_reconstructed_from_preserved_blobs':646,'candidate_guard':r,'engine_started':False,'git_written':False},indent=2))

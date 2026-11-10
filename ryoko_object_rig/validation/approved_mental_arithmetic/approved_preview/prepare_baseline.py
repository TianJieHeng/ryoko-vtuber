"""Materialize only a local, already checked-out approved36 baseline; no network or rendering."""
import json,hashlib,shutil,subprocess,sys
from pathlib import Path
w=Path(__file__).resolve().parent
source=Path(sys.argv[1]).resolve()
f=json.loads((w/'BASELINE_REFERENCE.json').read_text())
assert subprocess.check_output(['git','-C',str(source),'rev-parse','HEAD'],text=True).strip()==f['published_baseline_commit']
assert not (w/'baseline').exists() and not (w/'rig').exists(), 'Use a fresh package copy'
# Export the exact pinned commit rather than mutable working-tree bytes.
p=subprocess.Popen(['git','-C',str(source),'archive',f['published_baseline_commit']],stdout=subprocess.PIPE)
(w/'baseline').mkdir()
subprocess.run(['tar','-x','-C',str(w/'baseline')],stdin=p.stdout,check=True)
p.stdout.close();assert p.wait()==0
root=w/'baseline/ryoko_object_rig'
m=json.loads((root/'APPROVED_SOURCE_MANIFEST.json').read_text())['files']
assert len(m)==999 and sum(n.endswith('.png') for n in m)==184
f['source_files_sha256']=m
f['source_rig']=str(root)
f['source_sheet']=str(w/f['source_sheet']);f['source_catalogue']=str(w/f['source_catalogue'])
for n,h in (m|f['extra_manifests_sha256']).items():
 src=root/n;assert hashlib.sha256(src.read_bytes()).hexdigest()==h,n
 dst=w/'rig'/n;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
(w/'BASELINE_FREEZE.json').write_text(json.dumps(f,indent=2)+'\n')
r=json.loads((w/'SOURCE_REFERENCE.json').read_text());r['sheet']=f['source_sheet'];(w/'SOURCE_REFERENCE.json').write_text(json.dumps(r,indent=2)+'\n')
print('Pinned approved36 baseline materialized; candidate profile and video untouched.')

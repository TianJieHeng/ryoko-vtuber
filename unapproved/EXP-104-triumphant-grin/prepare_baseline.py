#!/usr/bin/env python3
"""Offline, hash-checked materialization only. Never launches a renderer or UI.

Use --git REPOSITORY for a local clone containing the fixed baseline commit,
or supply --rig-source and --reference-source directories. Output must not exist.
The immutable snapshot is reconstructed separately from a path-relocated replay.
"""
import argparse,hashlib,json,os,shutil,subprocess
from pathlib import Path
P=Path(__file__).resolve().parent
H=lambda data:hashlib.sha256(data).hexdigest()
a=argparse.ArgumentParser()
a.add_argument('--git',type=Path)
a.add_argument('--rig-source',type=Path)
a.add_argument('--reference-source',type=Path)
a.add_argument('--output',type=Path,required=True)
args=a.parse_args()
assert bool(args.git) != bool(args.rig_source),'Choose --git or --rig-source plus --reference-source'
assert args.git or args.reference_source,'Provide the reference_library directory'
out=args.output.resolve();assert not out.exists(),'Output must be new; never overwrite evidence'
manifest=json.loads((P/'SOURCE_MAP.json').read_text())['files']
base=json.loads((P/'historical/BASELINE_FREEZE.json').read_text())
commit='3ce98774282ad6c20dfbd7018d20838ff861b762'
assert base['published_baseline_commit']==commit
if args.git:
 git=['git','-c','protocol.allow=never','-C',str(args.git.resolve())]
 env=dict(os.environ,GIT_NO_LAZY_FETCH='1',GIT_TERMINAL_PROMPT='0')
 assert subprocess.check_output(git+['rev-parse',commit+'^{commit}'],env=env,text=True).strip()==commit
 def read_source(path):return subprocess.check_output(git+['cat-file','blob',commit+':'+path],env=env)
else:
 def read_source(path):
  if path.startswith('ryoko_object_rig/'):return (args.rig_source/path.removeprefix('ryoko_object_rig/')).read_bytes()
  return (args.reference_source/path.removeprefix('avatar_build_assets/reference_library/')).read_bytes()
# Validate all inputs before creating the output.
blobs={}
for name,digest in (base['source_files_sha256']|base['extra_manifests_sha256']).items():
 data=read_source('ryoko_object_rig/'+name);assert H(data)==digest,name;blobs['baseline/ryoko_object_rig/'+name]=data
assert len(base['source_files_sha256'])==999
assert sum(n.endswith('.png') for n in base['source_files_sha256'])==184
ref=json.loads((P/'historical/SOURCE_REFERENCE.json').read_text())
references={base['source_sheet'].split('/reference_library/',1)[1]:base['source_sheet_sha256'],'metadata/expressions.json':base['catalogue_sha256'],**ref['panel_hashes']}
for name,digest in references.items():
 data=read_source('avatar_build_assets/reference_library/'+name);assert H(data)==digest,name;blobs['baseline/avatar_build_assets/reference_library/'+name]=data
for name,record in manifest.items():
 data=(P/record['stored_path']).read_bytes();assert H(data)==record['sha256'],name;blobs['snapshot/'+name]=data
video=(P/'TriumphantGrin_review_v1.mp4').read_bytes()
assert H(video)=='caa4914959146c87fa371a17e829ca3c5d85b4db4a273b341f62781a8b33d17b'
blobs['snapshot/TriumphantGrin_review_v1.mp4']=video
for name,data in blobs.items():
 dst=out/name;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(data)
for root in ['snapshot/rig','snapshot/native_launcher','reproduction/triumphant_grin_work/rig']:
 for name in base['source_files_sha256']|base['extra_manifests_sha256']:
  dst=out/root/name
  if dst.exists():continue # exact historical launcher override remains intact
  dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(out/'baseline/ryoko_object_rig'/name,dst)
# Verify all frozen original inputs, including aliases. No old absolute paths used.
freeze=json.loads((out/'snapshot/review_input_freeze.json').read_text())
assert H((out/'snapshot/review_input_freeze.json').read_bytes())=='40f54ee01529ef96d18404cd2f3ebb1e2bf3004662cf2c45055434fb063aef7a'
for name,digest in freeze['files'].items():assert H((out/'snapshot'/name).read_bytes())==digest,name
# A separate replay changes paths, never the historical contract or its validators.
w=out/'reproduction/triumphant_grin_work'
for name in ['SOURCE_CATALOGUE_ENTRY.json','EXP-104.json','plan.json','check_and_capture.gd','render_motion.gd','run_motion.sh','prepare_native_launcher.py','independent_geometry.py','test_independent_geometry.py','encode_preview.py','test_encode_preview.py']:
 shutil.copyfile(out/'snapshot'/name,w/name)
base['source_rig']=str(out/'baseline/ryoko_object_rig')
for key in ['source_sheet','source_catalogue']:base[key]=str(out/'baseline/avatar_build_assets/reference_library'/base[key].split('/reference_library/',1)[1])
base['reproduction_note']='Paths relocated. Prior approved40/41 parity is historical evidence, not revalidated here. This is not the historical input freeze.'
(w/'BASELINE_FREEZE.json').write_text(json.dumps(base,indent=2)+'\n')
ref['sheet']=base['source_sheet'];(w/'SOURCE_REFERENCE.json').write_text(json.dumps(ref,indent=2)+'\n')
receipt={'status':'PASS','baseline_commit':commit,'baseline_files':999,'baseline_pngs':184,'reference_files':len(references),'historical_frozen_files':len(freeze['files']),'native_renderer_run':False,'historical_inputs_modified':False,'reproduction_only_path_changes':True}
(out/'BOOTSTRAP_RESULT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))

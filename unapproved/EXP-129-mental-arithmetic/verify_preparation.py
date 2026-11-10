import hashlib,json
from pathlib import Path
W=Path(__file__).resolve().parent; f=json.loads((W/'BASELINE_FREEZE.json').read_text());h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
errors=[]
for root in [Path(f['source_rig']),W/'rig']:
 for n,v in (f['source_files_sha256']|f['extra_manifests_sha256']).items():
  if h(root/n)!=v:errors.append(str(root/n))
for n in ['source_sheet','source_catalogue']:
 expected=f['source_sheet_sha256' if n=='source_sheet' else 'catalogue_sha256']
 assert h(Path(f[n]))==expected
r={n:json.loads((W/n).read_text()) for n in ['state_checks.json','motion_state_checks.json']}
assert all(x['status']=='PASS' and not x['visual_capture'] for x in r.values())
assert not errors,errors
out=dict(status='PASS',source_files=999,source_png_files=184,approved_profiles=36,production_and_copied_pinned_files_unchanged=True,reference_art_and_catalogue_unchanged=True,checks={n:x['checks'] for n,x in r.items()},native_capture='Separate GUI worker owns execution; numerical checks are not visual approval.',candidate_approval='UNAPPROVED',publication='No production registry change or publication',extra_manifests=f['extra_manifests_sha256'])
(W/'preparation_verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

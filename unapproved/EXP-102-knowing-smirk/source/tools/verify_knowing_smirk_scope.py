#!/usr/bin/env python3
"""Portable exact-source and actual-capture guard. It is not a visual oracle."""
import argparse,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--capture-root',type=Path);args=ap.parse_args();checks=0
 def require(ok,label):
  nonlocal checks
  checks+=1
  if not ok:raise AssertionError(label)
 freeze=json.loads((ROOT/'KNOWING_SMIRK_CAPTURE_FREEZE.json').read_text())
 for name,h in freeze['files'].items():require((ROOT/name).is_file() and sha(ROOT/name)==h,'frozen source '+name)
 baseline=json.loads((ROOT/'source_references/knowing_smirk_capability_inventory.json').read_text())
 modified=json.loads((ROOT/'source_references/knowing_smirk_declared_metadata_changes.json').read_text())['modified_inherited_metadata']
 require(len(baseline)==587 and sum(x.endswith('.png') for x in baseline)==182,'verified inherited scope')
 for name,h in baseline.items():
  if name=='expressions/registry.json':continue
  path=ROOT/'source_references/exp102_baseline_metadata'/name if name in modified else ROOT/name
  require(sha(path)==h,'exact inherited source or archived metadata '+name)
 reg=json.loads((ROOT/'expressions/registry.json').read_text());prior=json.loads((ROOT/'source_references/knowing_smirk_prior_registry.json').read_text())
 require(reg['entries'][:-1]==prior['entries'] and len(reg['entries'])==13,'append-only thirteen-entry registry')
 require(reg['entries'][-1]['id']=='EXP-102','only requested new profile')
 p=json.loads((ROOT/'expressions/EXP-102.json').read_text());require(p['duration']==3.8 and len(p['keyframes'])==10,'authored timing')
 require('unapproved' in p['status'] and 'unimplemented reference proposal' in p['timing_origin'],'honest candidate and static-source status')
 require(all(v==0 for v in p['keyframes'][0]['values'].values()) and all(v==0 for v in p['keyframes'][-1]['values'].values()),'neutral endpoints')
 anchors=json.loads((ROOT/'source_references/knowing_smirk_source_anchor_map.json').read_text())['anchors'];static=json.loads((ROOT/'source_references/knowing_smirk_accepted_static_plan.json').read_text())['candidate_cases']
 for a in anchors:
  matches=[k for k in p['keyframes'] if k['time']==a['time']];require(len(matches)==1 and matches[0]['values']==a['values'],'authored source anchor')
  for e in static:
   if e['source_key']==a['key_pose']:require(all(a['values'].get(k,0)==e['values'].get(k,0) for k in set(a['values'])|set(e['values'])),'exact accepted static controls')
 zero_channels=json.loads((ROOT/'source_references/knowing_smirk_accepted_static_plan.json').read_text())['required_zero_channels']
 for key in p['keyframes']:
  for name in zero_channels:require(key['values'][name]==0,'unused natural channel '+name)
 status=json.loads((ROOT/'KNOWING_SMIRK_STATUS.json').read_text());release=json.loads((ROOT/'RELEASE.json').read_text())
 require(status['user_approved'] is False and status['approved_count']==12 and status['local_registered_count']==13,'unapproved status')
 require(release['user_approved'] is False and release['published'] is False and release['authored_local_count']==13,'unapproved release')
 plan=json.loads((ROOT/'source_references/knowing_smirk_capture_plan.json').read_text());require(sha(ROOT/'source_references/knowing_smirk_capture_plan.json')==freeze['capture_plan_sha256'],'portable capture plan exact')
 if args.capture_root:
  from PIL import Image
  ev=json.loads((args.capture_root/'evidence.json').read_text());require(not ev['validate_only'] and not ev['failures'],'actual graphical capture passed')
  require(ev['profile_sha256']==sha(ROOT/'expressions/EXP-102.json'),'captured exact profile')
  require(ev['source_manifest_sha256']==sha(ROOT/'KNOWING_SMIRK_CAPTURE_FREEZE.json'),'captured exact source manifest')
  require(ev['plan_sha256']==freeze['capture_plan_sha256'],'captured exact plan')
  require(len(ev['records'])==sum(len(c['times']) for c in plan['chapters']),'all planned checkpoints')
  for rec in ev['records']:
   for kind,key in [('full','full_rgba_sha256'),('native','native_rgba_sha256')]:
    path=args.capture_root/kind/(rec['label']+'.png');require(path.is_file(),'actual frame exists')
    with Image.open(path) as im:require(hashlib.sha256(im.convert('RGBA').tobytes()).hexdigest()==rec[key],'frame pixels match receipt')
 print(json.dumps({'status':'PASS','checks':checks,'source_manifest_sha256':sha(ROOT/'KNOWING_SMIRK_CAPTURE_FREEZE.json'),'profile_sha256':sha(ROOT/'expressions/EXP-102.json'),'captures_checked':bool(args.capture_root),'normal_speed_playback_observed':False}))
if __name__=='__main__':main()

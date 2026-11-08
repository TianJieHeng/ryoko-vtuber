#!/usr/bin/env python3
"""Portable frozen-source and optional actual-capture guard; never a visual oracle."""
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
 freeze=json.loads((ROOT/'CHEEKY_WINK_CAPTURE_FREEZE.json').read_text())
 overlay_path=ROOT/'CHEEKY_WINK_DELIVERY_OVERLAY.json'
 overlay=json.loads(overlay_path.read_text()) if overlay_path.exists() else {'overrides':{}}
 allowed={'expressions/EXP-181.json','README.md','RELEASE.json','CHEEKY_WINK_STATUS.json','INDEPENDENT_CORNERS_LOCAL.md','CONTROL_API.md','LOCAL_CONTROL_BRIDGE.md','tools/verify_cheeky_wink_scope.py'}
 require(set(overlay['overrides'])<=allowed,'only declared metadata/documentation/verifier overrides')
 if overlay_path.exists():
  require(overlay['captured_source_manifest_sha256']==sha(ROOT/'CHEEKY_WINK_CAPTURE_FREEZE.json'),'delivery preserves captured source manifest')
  inventory=json.loads((ROOT/'DELIVERY_SOURCE_MANIFEST.json').read_text())
  require(inventory['file_count_including_this_manifest']==len(inventory['files'])+1,'delivery inventory count')
  for name,h in inventory['files'].items():require((ROOT/name).is_file() and sha(ROOT/name)==h,'delivery inventory exact '+name)
  release=json.loads((ROOT/'RELEASE.json').read_text())
  require(release['user_approved'] is False and release['published'] is False and release['approved_published_count']==12 and release['authored_local_count']==13,'current unapproved release scope')
 def captured_path(name):
  if name not in overlay['overrides']:return ROOT/name
  e=overlay['overrides'][name];require(e['captured_path']=='source_references/captured_source/'+name,'bounded captured path')
  require(sha(ROOT/name)==e['delivery_sha256'],'declared live overlay '+name)
  require(e['captured_sha256']==freeze['files'][name],'override original identity')
  return ROOT/e['captured_path']
 for name,h in freeze['files'].items():
  path=captured_path(name);require(path.is_file() and sha(path)==h,'frozen source or exact archived metadata '+name)
 for name,h in overlay.get('added_files',{}).items():require((ROOT/name).is_file() and sha(ROOT/name)==h,'declared delivery addition '+name)
 captured_profile=json.loads(captured_path('expressions/EXP-181.json').read_text())
 live_profile=json.loads((ROOT/'expressions/EXP-181.json').read_text())
 prose={'status','intent','timing_origin','scope','interpolation'}
 require({k:v for k,v in captured_profile.items() if k not in prose}=={k:v for k,v in live_profile.items() if k not in prose},'profile motion and all non-prose fields exact')
 old=json.loads((ROOT/'source_references/corner_approved_parent_inventory.json').read_text());cap=json.loads((ROOT/'source_references/corner_capability_v1_inventory.json').read_text())
 require(len(old)==585,'approved baseline file count')
 require(sum(x.endswith('.png') for x in old)==182,'approved artwork count')
 for name,h in old.items():
  if name.endswith('.png') or (name.startswith('expressions/') and name!='expressions/registry.json') or name=='yawn_performance.json':require(sha(ROOT/name)==h,'approved artwork/profile exact '+name)
 for name,h in cap.items():
  if name not in ['README.md','expressions/registry.json']:require(sha(captured_path(name))==h,'reviewed capability exact '+name)
 reg=json.loads((ROOT/'expressions/registry.json').read_text());prior=json.loads((ROOT/'source_references/corner_approved_registry.json').read_text())
 require(reg['entries'][:-1]==prior['entries'] and len(reg['entries'])==13,'append-only thirteen-entry registry')
 require(reg['entries'][-1]['id']=='EXP-181','only requested new profile')
 p=json.loads((ROOT/'expressions/EXP-181.json').read_text());require(p['duration']==3.10 and len(p['keyframes'])==10,'authored timing')
 require(p['status'].startswith('Local') and 'unimplemented reference proposal' in p['timing_origin'],'honest unapproved/static status')
 require(all(v==0 for v in p['keyframes'][0]['values'].values()) and all(v==0 for v in p['keyframes'][-1]['values'].values()),'neutral endpoints')
 anchors=json.loads((ROOT/'source_references/cheeky_wink_source_anchor_map.json').read_text())['anchors'];static=json.loads((ROOT/'source_references/cheeky_wink_accepted_static_plan.json').read_text())['candidate_cases']
 for a in anchors:
  matches=[k for k in p['keyframes'] if k['time']==a['time']];require(len(matches)==1 and matches[0]['values']==a['values'],'authored anchor')
  for e in static:
   if e['source_key']==a['key_pose']:
    require(all(a['values'].get(k,0)==e['values'].get(k,0) for k in set(a['values'])|set(e['values'])),'exact accepted static values')
 status=json.loads((ROOT/'CHEEKY_WINK_STATUS.json').read_text());require(status['approved_integration'] is False and status['approved_count']==12 and status['local_registered_count']==13,'unapproved scope')
 if args.capture_root:
  from PIL import Image
  ev=json.loads((args.capture_root/'evidence.json').read_text());require(not ev['validate_only'] and not ev['failures'],'actual graphical capture passed')
  require(ev['profile_sha256']==sha(captured_path('expressions/EXP-181.json')),'captured exact profile')
  require(ev['source_manifest_sha256']==sha(ROOT/'CHEEKY_WINK_CAPTURE_FREEZE.json'),'captured exact source manifest')
  require(ev['plan_sha256']==freeze['capture_plan_sha256'],'captured exact plan')
  require(len(ev['records'])==305,'all planned checkpoints')
  for rec in ev['records']:
   for kind,key in [('full','full_rgba_sha256'),('native','native_rgba_sha256')]:
    path=args.capture_root/kind/(rec['label']+'.png');require(path.is_file(),'actual frame exists')
    with Image.open(path) as im:require(hashlib.sha256(im.convert('RGBA').tobytes()).hexdigest()==rec[key],'frame pixels match receipt')
 print(json.dumps({'status':'PASS','checks':checks,'source_manifest_sha256':sha(ROOT/'CHEEKY_WINK_CAPTURE_FREEZE.json'),'profile_sha256':sha(ROOT/'expressions/EXP-181.json'),'captures_checked':bool(args.capture_root),'normal_speed_playback_observed':False}))
if __name__=='__main__':main()

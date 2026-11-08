from pathlib import Path
import json,hashlib
S=Path(__file__).resolve().parent.parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();f=json.loads((S/'SMUG_CAT_SMILE_CAPTURE_FREEZE.json').read_text())
for p,h in f['files'].items():assert sha(S/p)==h,p
for p,h in f['baseline_files'].items():
 if p!='expressions/registry.json':assert sha(S/p)==h,p
old=json.loads((S/'source_references/smug_cat_smile_prior_registry.json').read_text());new=json.loads((S/'expressions/registry.json').read_text());assert new['entries'][:-1]==old['entries'] and len(new['entries'])==18
plan=json.loads((S/'source_references/smug_cat_smile_accepted_static_plan.json').read_text());cases={e['source_key']:e['values'] for e in plan['candidate_cases']};profile=json.loads((S/'expressions/EXP-186.json').read_text());maps=json.loads((S/'source_references/smug_cat_smile_source_anchor_map.json').read_text())['anchors'];assert profile['duration']==3.4 and len(profile['keyframes'])==len(maps)==10
for frame,anchor in zip(profile['keyframes'],maps):
 assert frame['time']==anchor['time'] and frame['phase']==anchor['phase'] and frame['values']==anchor['values']
 for k,v in frame['values'].items():assert v==cases[anchor['key_pose']].get(k,0),(frame['time'],k)
status=json.loads((S/'SMUG_CAT_SMILE_STATUS.json').read_text());assert len(status['approved_profile_ids'])==12 and len(status['unapproved_profile_ids'])==6 and not status['approved'];assert sum(p.endswith('.png') for p in f['files'])==182
print('SMUG_CAT_SMILE_SCOPE_PASS:18local profiles,17 predecessor profiles/runtime/art/statuses exact,12 approvals, accepted anchor values only')

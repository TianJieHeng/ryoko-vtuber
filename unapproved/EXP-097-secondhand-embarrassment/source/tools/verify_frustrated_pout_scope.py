from pathlib import Path
import json,hashlib
S=Path(__file__).resolve().parent.parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
f=json.loads((S/'FRUSTRATED_POUT_CAPTURE_FREEZE.json').read_text())
for p,h in f['files'].items():assert sha(S/p)==h,p
for p,h in f['baseline_files'].items():
 if p!='expressions/registry.json':assert sha(S/p)==h,p
old=json.loads((S/'source_references/frustrated_pout_prior_registry.json').read_text());new=json.loads((S/'expressions/registry.json').read_text());assert new['entries'][:-1]==old['entries'] and len(new['entries'])==17
plan=json.loads((S/'source_references/frustrated_pout_accepted_static_plan.json').read_text());cases={e['source_key']:e['combined_values'] for e in plan['candidate_cases']};profile=json.loads((S/'expressions/EXP-050.json').read_text());maps=json.loads((S/'source_references/frustrated_pout_source_anchor_map.json').read_text())['anchors']
assert profile['duration']==4.13 and len(profile['keyframes'])==len(maps)==9
for frame,anchor in zip(profile['keyframes'],maps):
 assert frame['time']==anchor['time'] and frame['phase']==anchor['phase'] and frame['values']==anchor['values']
 for k,v in frame['values'].items():assert v==cases[anchor['key_pose']].get(k,0),(frame['time'],k)
assert sum(p.endswith('.png') for p in f['files'])==182
print('FRUSTRATED_POUT_SCOPE_PASS: 17 profiles, sixteen predecessor profiles and inherited runtime/art exact, only accepted anchor values')

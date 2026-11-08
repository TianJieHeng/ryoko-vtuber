from pathlib import Path
import hashlib,json
S=Path(__file__).resolve().parent.parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();f=json.loads((S/'SECONDHAND_EMBARRASSMENT_CAPTURE_FREEZE.json').read_text())
# Clean source contract only. Runtime caches require their separate exact external inventory.
assert not S.is_symlink(), 'Symlink source root'
paths=list(S.rglob('*'))
assert not any(p.is_symlink() for p in paths), 'Symlinks are not allowed in clean source'
expected=set(f['files'])|{'SECONDHAND_EMBARRASSMENT_CAPTURE_FREEZE.json'}
actual={str(p.relative_to(S)) for p in paths if p.is_file()}
assert actual==expected, {'missing':sorted(expected-actual),'unexpected':sorted(actual-expected)}
for p,h in f['files'].items():assert sha(S/p)==h,p
for p,h in f['approved_base_files'].items():
 if p!='expressions/registry.json':assert sha(S/p)==h,p
old=json.loads((S/'source_references/secondhand_embarrassment_prior_registry.json').read_text());reg=json.loads((S/'expressions/registry.json').read_text());approved=json.loads((S/'APPROVED_INTEGRATION_STATUS.json').read_text());status=json.loads((S/'SECONDHAND_EMBARRASSMENT_STATUS.json').read_text())
assert len(old['entries'])==19 and reg['entries'][:-1]==old['entries'] and len(reg['entries'])==20
assert approved['approved_profile_ids']==status['approved_profile_ids']==[e['id'] for e in old['entries']] and approved['approved_profile_count']==status['approved_profile_count']==19
assert status['pending_profile_ids']==['EXP-097'] and not status['approved'] and not status['approved_integration']
# Inherited approved manifests are pinned predecessor evidence, not candidate inventory validators.
assert f['published_manifest_scope']=='exact_approved_predecessor_only'
profile=json.loads((S/'expressions/EXP-097.json').read_text());static=json.loads((S/'source_references/secondhand_embarrassment_accepted_static_plan.json').read_text());cases={c['source_key']:c['values'] for c in static['candidate_cases']};mapping=json.loads((S/'source_references/secondhand_embarrassment_source_anchor_map.json').read_text())['anchors'];assert len(profile['keyframes'])==len(mapping)==12 and profile['duration']==3.3
for frame,anchor in zip(profile['keyframes'],mapping):assert frame['time']==anchor['time'] and frame['phase']==anchor['phase'] and frame['values']==anchor['values']==cases[anchor['key_pose']]
assert sum(p.endswith('.png') for p in f['files'])==182
print('EXP097_REBASED_SCOPE_PASS registered=20 approved=19 pending=EXP-097; exact accepted anchors and approved predecessor bytes preserved')

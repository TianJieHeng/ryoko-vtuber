#!/usr/bin/env python3
"""Map all retained expression/body references to named presets on the shared rig."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
META=ROOT.parent/'ryoko-vtuber'/'avatar_build_assets'/'reference_library'/'metadata'
expressions=json.loads((META/'expressions.json').read_text())['expressions']
gestures=json.loads((META/'body_gestures.json').read_text())['assets']
def expression_controls(e):
 text=(e['slug']+' '+e['family']+' '+e['distinctive_facial_intent']).lower()
 c={'mouth':'neutral','brow_raise':0.0,'brow_lower':0.0,'gaze_x':0.0,'gaze_y':0.0,'head_tilt':0.0,'effects':[]}
 if any(k in text for k in ['brow arches','brows rise','raised brow','eyebrows lift','surprise','startle','wide-eyed']):c['brow_raise']=.75
 if any(k in text for k in ['brow lower','brows lower','knit','stern','angry','anger','scold','frown','glare','annoy']):c['brow_lower']=.8
 if any(k in text for k in ['side-eye','side eye','look left','gaze left']):c['gaze_x']=-.7
 if any(k in text for k in ['look right','gaze right']):c['gaze_x']=.7
 if any(k in text for k in ['look up','gaze up','upward']):c['gaze_y']=-.65
 if any(k in text for k in ['look down','gaze down','downcast','eyes down']):c['gaze_y']=.65
 if any(k in text for k in ['pucker','funnel','rounded mouth','oo '] ):c['mouth']='O'
 elif any(k in text for k in ['broad','upper-teeth','upper teeth','open smile','laugh','grin','teeth smile']):c['mouth']='A'
 elif any(k in text for k in ['smile','smirk','grin','ee '] ):c['mouth']='E'
 elif any(k in text for k in ['jaw open','mouth open','gasp','shout','outburst']):c['mouth']='A'
 if 'blush' in text:c['effects']+=['blush_R','blush_L']
 if any(k in text for k in ['tear','crying','weep']):c['effects']+=['tear_R','tear_L']
 if 'sweat' in text or 'nervous' in text:c['effects']+=['sweat']
 if 'anger mark' in text or 'angry' in text or 'furious' in text:c['effects']+=['anger']
 if 'sparkle' in text or 'starry' in text:c['effects']+=['sparkle']
 if 'tilt' in text:c['head_tilt']=.25 if any(k in text for k in ['left','quizzical','question']) else -.25
 c['effects']=list(dict.fromkeys(c['effects']))
 return c
exp=[]
for e in expressions:
 exp.append({'id':e['id'],'slug':e['slug'],'family':e['family'],'source_sheet':e['asset_production']['actual_path'],'source_peak':e['asset_production']['peak_actual_path'],'intent':e['distinctive_facial_intent'],'duration_seconds':e['timing']['duration_seconds'],'peak_hold_seconds':e['timing']['peak_hold_seconds'],'key_pose_times':[p['time_seconds'] for p in e['key_pose_sequence']],'controls':expression_controls(e),'body_reference_ids':e['body_gesture']['reference_ids'],'implementation':'parameterized_shared_rig_preset','source_usage':'acting guide; no raw sheet crop is used as a runtime frame'})
(ROOT/'manifest/expression_map.json').write_text(json.dumps({'version':1,'count':len(exp),'neutral_effects_off':True,'expressions':exp},indent=2))
registered={'BOD-001':'gesture_crossed_arms','BOD-002':'gesture_finger_wag','BOD-011':'gesture_wave'}
actions=[]
for g in gestures:
 text=(g['slug']+' '+g['intent']).lower();gid=g['id']
 controls={'head_tilt':0.0,'brow_lower':0.0,'brow_raise':0.0,'sway':.25,'arm_proxy':0.0}
 if any(k in text for k in ['stern','scold','stern','admonish','glare']):controls['brow_lower']=.75
 if any(k in text for k in ['surprise','startle','question','shrug']):controls['brow_raise']=.65
 if 'tilt' in text or 'question' in text:controls['head_tilt']=.3
 if gid not in registered:controls['arm_proxy']=.6
 actions.append({'id':gid,'slug':g['slug'],'intent':g['intent'],'source_sheet':g['path'],'key_poses':g['key_poses'],'timestamps_seconds':g['timestamps_seconds'],'duration_seconds':g['duration_seconds'],'loop':g['loop'],'gesture':registered.get(gid,''),'implementation':'registered_alternate_drawing' if gid in registered else 'parameterized_deformation_proxy','controls':controls,'source_usage':'acting guide on the same rig; raw panels are not playback frames'})
(ROOT/'manifest/body_action_map.json').write_text(json.dumps({'version':1,'count':len(actions),'registered_swap_count':len(registered),'actions':actions},indent=2))
print(json.dumps({'expressions':len(exp),'actions':len(actions),'registered_gestures':list(registered.values())},indent=2))

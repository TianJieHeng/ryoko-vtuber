"""Build the unapproved EXP-093 profile outside the unchanged production rig."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent
poses={row['name']:row['pose'] for row in json.loads((W/'plan.json').read_text())}
freeze=json.loads((W/'BASELINE_FREEZE.json').read_text())
keys=[(0,'neutral'),(.2,'neutral'),(.65,'tasting_onset'),(1.15,'souring_build'),(1.85,'bitter_peak'),(2.25,'bitter_peak'),(2.65,'aftertaste'),(3.2,'soften'),(3.75,'neutral_return'),(4,'neutral_return')]
definition={
 'id':'EXP-093','title':'Bitter taste','duration':4.0,
 'status':'UNAPPROVED review v1; data-only candidate against '+freeze['baseline'],
 'intent':'Brows lower as the bitter taste registers; ordinary lids narrow slowly over 1.65 seconds while a downturned open grimace develops. A closed aftertaste follows before exact neutral return.',
 'scope':'Existing symmetric ordinary lid closure, symmetric vertical brow lowering, opposing rigid brow tilt, continuous mouth opening and purse only. No independent upper-lip lift or curl is supported. The upper lip actually moves down with the common purse contour while the lower lip descends farther through existing opening. This is a partial approximation, not reproduction of the source upper-up/lower-down anatomy. No unilateral sneer or left-right lip asymmetry is authored. No new artwork, anatomy, shader, runtime, control or range. Smile, corner lift, lip pressure, oral lift, side width, kiss, uneasy part, gaze, blush, hair, head and body acting remain zero.',
 'timing_origin':'New four-second interpretation of nine static EXP-093 panels; the catalogue 1.9-second timing is proposed and numeric rig weights are null. Neutral holds to 0.20, onset at 0.65, build at 1.15, peak at 1.85 through 2.25, closed aftertaste at 2.65, soften at 3.20 and exact neutral from 3.75 through 4.00. Lids narrow gradually across onset and build; no automatic or full blink is added.',
 'interpolation':'Unchanged shared cubic smoothstep and displayed-pose restart/release. Seven static anchors, ten timeline keys, exact neutral bookends. Candidate loaded only into memory.',
 'source_catalogue_sha256':freeze['catalogue_sha256'],
 'keyframes':[{'time':t,'phase':name,'values':poses[name]} for t,name in keys]}
assert len(poses)==7
assert definition['keyframes'][0]['values']==definition['keyframes'][-1]['values']=={}
(W/'EXP-093.json').write_text(json.dumps(definition,indent=2)+'\n')
print('Built UNAPPROVED EXP-093: 4 seconds, ten keys, seven static anchors; production unchanged.')

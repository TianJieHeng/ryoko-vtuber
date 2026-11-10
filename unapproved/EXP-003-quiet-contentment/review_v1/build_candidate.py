"""Build only an external, unapproved data profile; no production writes."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent
poses={row['name']:row['pose'] for row in json.loads((W/'plan.json').read_text())}
freeze=json.loads((W/'BASELINE_FREEZE.json').read_text())
keys=[(0.0,'neutral'),(.25,'neutral'),(.70,'eyes_soften'),(1.15,'settling'),(1.65,'quiet_contentment'),(2.80,'quiet_contentment'),(3.60,'lingering_smile'),(4.25,'neutral_return'),(4.60,'neutral_return')]
d={
'id':'EXP-003','title':'Quiet contentment','duration':4.6,
'status':'UNAPPROVED review v1; isolated data-only preparation against '+freeze['baseline'],
'intent':'Low level brows and soft eyes settle into a gentle held closed-eye smile, then reopen with a lingering small smile before exact neutral.',
'scope':'Existing symmetric vertical brow lowering, symmetric smile-eye closure and sealed symmetric mouth smile/corner lift only. Peak brow pivots lower 2.8 source pixels without rotation; the existing smile-eye control closes the canonical aperture and uses 0.32 of its existing curved closed-eye shape. Peak mouth corners lift 2.36 source pixels with no widening, opening or purse. No new anatomy, artwork, shader, runtime, range, head/body motion, gaze, blush, hair or automatic blink. Low and level means no additional tilt; existing source brow shape remains. The v002 sheet peak closes its eyes despite catalogue wording eyes half relax. The existing smiling eye geometry is an approximation, not the exact sheet contour; a separate static half-relaxed alternative is not used by this timeline.',
'source_catalogue_sha256':freeze['catalogue_sha256'],
' timing_origin':'',
'interpolation':'Unchanged shared cubic smoothstep, displayed-pose restart and release. Exact neutral bookends. Six timeline anchors and nine keys; one additional static half-relaxed alternative. Candidate loads only into memory.'}
d.pop(' timing_origin')
d['timing_origin']='New 4.6-second interpretation, not recovered animation. Source proposes 1.9 seconds and has no numeric rig weights. Neutral holds through 0.25 seconds; lids soften by 0.70, settle by 1.15 and reach a gentle closed-eye pose at 1.65. The exact quiet peak holds through 2.80. Eyes reopen with a lingering smile by 3.60 and reach exact neutral at 4.25 through 4.60. Readability comes from the continuous eye-settling transition and clear hold, not a larger smile or extra head/body motion.'
d['keyframes']=[{'time':t,'phase':p,'values':poses[p]} for t,p in keys]
(W/'EXP-003.json').write_text(json.dumps(d,indent=2)+'\n')
print('Built UNAPPROVED EXP-003: 4.6 seconds, nine keys; production untouched.')

"""Deterministic generic timeline comparison, not a render or visual-fit test."""
import json
import math
from numeric_model import W,CHANNELS,canonical,playback_from_neutral,rounded,sha

def expected(w=W):
    sour=json.loads((w/'EXP-092.json').read_text())
    sweet=json.loads((w/'comparators/EXP-091.json').read_text())
    if sweet.get('id')!='EXP-091' or sweet.get('duration')!=4.0:
        raise ValueError('Expected the fresh four-second EXP-091 comparator')
    a=playback_from_neutral(sour,1.6)
    b=playback_from_neutral(sweet,1.6)
    deltas={key:math.fsum(abs(playback_from_neutral(sour,i/240)[key]-playback_from_neutral(sweet,i/240)[key]) for i in range(961))/961 for key in sorted(CHANNELS)}
    return rounded({'scope':'Pure-Python control trajectories. No actual rendered or perceptual comparison.',
        'status':'NUMERIC_DIFFERENCE_ONLY','sour_sha256':sha(w/'EXP-092.json'),'sweet_sha256':sha(w/'comparators/EXP-091.json'),
        'dense_samples':961,'at_1_6_seconds':{'sour':a,'sweet':b},'mean_absolute_control_differences':deltas,
        'rms_of_mean_absolute_control_differences':math.sqrt(math.fsum(deltas[k]**2 for k in sorted(deltas))/len(deltas)),
        'required_native_comparison':'PENDING. Verify actual source fit and visible distinctness from both EXP-096 and fresh EXP-091 at bust/detail size across chronological frames.'})

if __name__=='__main__':
    target=W/'NUMERIC_COMPARATOR_091.json'
    if target.exists(): raise SystemExit('Existing comparator receipt preserved; refusing overwrite.')
    with target.open('x') as f: f.write(canonical(expected()))

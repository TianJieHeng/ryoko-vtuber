"""Freeze fresh inputs only. Never recreates an old identity or authorizes launch."""
import hashlib,json
from pathlib import Path
W=Path(__file__).resolve().parent
INPUTS=['prepare_candidate.py','trajectory_model.py','test_candidate.py','freeze_candidate.py','native_capture.gd','encode_preview.py','README.md','EXP-046.json','plan.json','SOURCE_MAP.json','SOURCE_CATALOGUE_ENTRY.json','BASELINE_FREEZE.json','EXPECTED_TRAJECTORY.json']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def verify(w=W):
    freeze=json.loads((w/'CANDIDATE_FREEZE.json').read_text())
    for rel,digest in freeze['files_sha256'].items():
        if sha(w/rel)!=digest:raise ValueError('Candidate input changed: '+rel)
    baseline=json.loads((w/'BASELINE_FREEZE.json').read_text())
    for rel,digest in baseline['baseline_files_sha256'].items():
        if sha(w/'rig'/rel)!=digest:raise ValueError('Baseline changed: '+rel)
    for rel,digest in baseline['reference_files_sha256'].items():
        if sha(w/'reference'/rel)!=digest:raise ValueError('Reference changed: '+rel)
    return freeze
if __name__=='__main__':
    target=W/'CANDIDATE_FREEZE.json'
    if target.exists():
        verify();print('Existing new freeze verified without rewrite.')
    else:
        data={'identity':'NEW EXP046 rebuild 2026-11-11 v1','old_candidate_restored':False,'approval':'UNAPPROVED','native_execution':'NOT RUN','files_sha256':{n:sha(W/n) for n in INPUTS}}
        target.write_text(json.dumps(data,indent=2)+'\n');verify();print('New source-only input identity frozen.')

"""Read-only final verifier. Emits deterministic JSON to stdout; writes nothing."""
import io
import json
from pathlib import Path
import unittest
from numeric_model import W,sha,canonical,build_receipts,validate_profile
from comparator_091 import expected
import test_candidate

def inventory():
    return {p.relative_to(W).as_posix():sha(p) for p in sorted(W.rglob('*')) if p.is_file()}

def validate():
    before=inventory()
    errors=[]
    checked=[]
    def check(value,label):
        checked.append(label)
        if not value: errors.append(label)
    manifest=json.loads((W/'INPUT_FREEZE.json').read_text())
    check((W/'INPUT_FREEZE.sha256').read_text()==sha(W/'INPUT_FREEZE.json')+'  INPUT_FREEZE.json\n','freeze sidecar')
    declared=manifest['files_sha256']
    check(len(declared)==manifest['file_count'],'freeze file count')
    actual={k:v for k,v in before.items() if k not in {'INPUT_FREEZE.json','INPUT_FREEZE.sha256'}}
    check(actual==declared,'exact frozen file set and bytes')
    baseline=json.loads((W/'BASELINE_FREEZE.json').read_text())
    check(len(baseline['files_sha256'])==1124,'1124 baseline files')
    check(sum(n.endswith('.png') for n in baseline['files_sha256'])==184,'184 baseline PNGs')
    for name,digest in sorted(baseline['files_sha256'].items()):
        check(sha(W/'rig'/name)==digest,'baseline '+name)
    recovery=W.parent/'ryoko_expression_recovery_20261111'
    for row in sorted(json.loads((recovery/'RECOVERY_MANIFEST.json').read_text())['files'],key=lambda r:r['destination']):
        check(sha(recovery/row['destination'])==row['sha256'],'preserved recovery '+row['destination'])
    registry=json.loads((W/'rig/expressions/registry.json').read_text())
    ids=[r['id'] for r in registry['entries']]
    check(ids==baseline['baseline_profile_ids'] and len(ids)==39,'approved39 registry unchanged')
    check(not set(ids)&{'EXP-091','EXP-092','EXP-096'},'candidates not production integrated')
    check(sha(W/'comparators/EXP-096.json')=='21ba5c4393ed672a5496ed28577068bd4b56e3b8ff5d7ac4f9674df03badf1fe','exact approved096 comparator bytes')
    for name,digest in sorted(baseline['reference_files_sha256'].items()):
        check(sha(W/name)==digest,'source reference '+name)
    profile=json.loads((W/'EXP-092.json').read_text())
    check(validate_profile(profile),'candidate restricted schema')
    for name,result in zip(['NUMERIC_TRAJECTORY.json','NUMERIC_LIFECYCLE.json'],build_receipts()):
        check((W/name).read_text()==canonical(result),'immutable deterministic '+name)
    binding=json.loads((W/'COMPARATOR_091_BINDING.json').read_text())
    check(sha(W/'comparators/EXP-091.json')==binding['profile_sha256'],'fresh091 comparator binding')
    check((W/'NUMERIC_COMPARATOR_091.json').read_text()==canonical(expected()),'immutable deterministic091 comparison')
    check(json.loads((W/'NATIVE_GATE.json').read_text())['allowed'] is False,'native execution blocked')
    check(not (W/'native_capture').exists(),'no new native capture claimed')
    check(not list(W.glob('*.mp4')),'no approval MP4 claimed')
    check(manifest['previous_lost_freeze_restored'] is False,'fresh identity not false restoration')
    tests=unittest.defaultTestLoader.loadTestsFromModule(test_candidate)
    test_result=unittest.TextTestRunner(stream=io.StringIO(),verbosity=0).run(tests)
    check(test_result.wasSuccessful(),'pure Python unit tests')
    check(before==inventory(),'validator made no file or receipt changes')
    return {'status':'PASS' if not errors else 'FAIL','scope':'Read-only static and pure-Python numeric model verification only',
        'checks':len(checked),'unit_tests':test_result.testsRun,'unit_failures':len(test_result.failures),'unit_errors':len(test_result.errors),
        'errors':errors,'freeze_sha256':sha(W/'INPUT_FREEZE.json'),'profile_sha256':sha(W/'EXP-092.json'),
        'native_render':'NOT RUN; blocked','native_lifecycle':'NOT RUN; model tests only','native_parse_check':'NOT RUN',
        'normal_speed_visual_review':'NOT RUN','native_distinctness_096_091':'NOT RUN','mp4':'NOT GENERATED','pushed':False,
        'approval':'UNAPPROVED','read_only':True}

if __name__=='__main__':
    result=validate()
    print(canonical(result),end='')
    raise SystemExit(0 if result['status']=='PASS' else 1)

"""Explicit author action. Refuse to repin an existing input identity."""
import hashlib
import json
from pathlib import Path
W=Path(__file__).resolve().parent
if __name__=='__main__':
    if (W/'INPUT_FREEZE.json').exists() or (W/'INPUT_FREEZE.sha256').exists():
        raise SystemExit('Existing freeze preserved. Create a separately named revision.')
    excluded={'STATIC_VALIDATION.json','TEST_RESULTS.log','MULTISEED_CHECK.json','RESULT.json','FILES.sha256'}
    files={str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(W.rglob('*'))
       if p.is_file() and '__pycache__' not in p.parts and p.name not in excluded}
    freeze={'reconstruction':'NEW 20261111 r1; not restored old v2','files':files,
            'native_execution':'BLOCKED; disabled source is preparation only','approval':'UNAPPROVED',
            'excluded_outputs':sorted(excluded),'freeze_writes_during_validation':False}
    data=(json.dumps(freeze,sort_keys=True,indent=2)+'\n').encode()
    with (W/'INPUT_FREEZE.json').open('xb') as f:f.write(data)
    with (W/'INPUT_FREEZE.sha256').open('x') as f:f.write(hashlib.sha256(data).hexdigest()+'  INPUT_FREEZE.json\n')
    print('New frozen inputs:',len(files))

#!/usr/bin/env python3
"""Read-only, standard-library exact source and predecessor recovery verification."""
from pathlib import Path
import hashlib, json

P=Path(__file__).resolve().parent
def digest(v):
    return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def obj(kind,b):return hashlib.sha1(kind.encode()+b' '+str(len(b)).encode()+b'\0'+b).hexdigest()
def tree(rows):
    children={}; direct=[]
    for n,value in rows.items():
        if '/' in n:
            head,tail=n.split('/',1);children.setdefault(head,{})[tail]=value
        else:direct.append((n,value[1],value[0]))
    for n,child in children.items():direct.append((n,'40000',tree(child)))
    direct.sort(key=lambda r:r[0]+('/' if r[1]=='40000' else ''))
    return obj('tree',b''.join((mode+' '+n).encode()+b'\0'+bytes.fromhex(h) for n,mode,h in direct))

def verify(root=P):
    assert not root.is_symlink(),'symlink package root'
    allpaths=list(root.rglob('*'))
    assert not any(p.is_symlink() for p in allpaths),'symlinks forbidden'
    m=json.loads((root/'RECOVERY.json').read_text())
    assert m['schema']=='EXP097_SOURCE_RECOVERY_V1'
    assert m['source_tree']=='938072165f3cf206228b6cd6c3c6e6a6785b4aaf'
    assert m['source_full_inventory_sha256']=='ac9b2de61cd85bd5e705f9519a0beaa9adfab19290e6284a8344fb0cfc8972d3'
    s=root/'source';fpath=s/'SECONDHAND_EMBARRASSMENT_CAPTURE_FREEZE.json'
    assert sha(fpath)==m['freeze_sha256']=='b0c3295e4da79699a2b390ddcfb2fb02112c8b241ecef3ad1ac87ba427beae08'
    f=json.loads(fpath.read_text());expected=set(f['files'])|{fpath.name}
    files={p.relative_to(root).as_posix():p for p in allpaths if p.is_file()}
    assert set(files)=={'source/'+n for n in expected}|{'README.md','RECOVERY.json','verify_recovery.py'},'missing/extra file'
    inv={n:sha(s/n) for n in sorted(expected)}
    assert len(inv)==673 and digest(inv)==m['source_full_inventory_sha256']
    assert {n:h for n,h in inv.items() if n!=fpath.name}==f['files']
    assert digest(f['files'])==m['payload_inventory_sha256']
    assert tree({n:(obj('blob',(s/n).read_bytes()),'100755' if n in m['executable_paths'] else '100644') for n in expected})==m['source_tree']
    assert inv['expressions/EXP-097.json']==m['profile_sha256']=='2717ea8ee1d42fbd8fb312efaa0f37466da5c0b42097f65737e04cb2d9afb342'
    old=json.loads((s/'source_references/secondhand_embarrassment_prior_registry.json').read_text())
    reg=json.loads((s/'expressions/registry.json').read_text())
    assert len(old['entries'])==19 and reg['entries'][:-1]==old['entries'] and reg['entries'][-1]['id']=='EXP-097'
    base={n:sha(s/('source_references/secondhand_embarrassment_prior_registry.json' if n=='expressions/registry.json' else n)) for n in f['approved_base_files']}
    assert len(base)==661 and base==f['approved_base_files'] and digest(base)==m['approved_inventory_sha256']
    assert sum(n.endswith('.png') for n in inv)==182
    for n,h in m['recovery_files_sha256'].items():assert sha(root/n)==h,n
    assert not m['user_approved'] and not m['approved_integration'] and m['pending']==['EXP-097']
    assert m['normal_realtime_pacing']=='HOLD' and not m['full815_accepted'] and not m['media_accepted']
    return {'status':'PASS_EXACT_SOURCE_RECOVERY','source_files':673,'package_files':len(files),'approved_predecessor_files_recoverable':661,'source_tree':m['source_tree'],'visual_evidence_replayed':False,'engine_started':False,'files_written':False}
if __name__=='__main__':print(json.dumps(verify(),indent=2))

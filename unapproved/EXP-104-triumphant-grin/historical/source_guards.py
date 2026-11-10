"""Read-only author source guards; no runtime execution or reviewer artifact access."""
import hashlib
import json
import re
from pathlib import Path
W=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_text())

def verify_manifest(root,files):
    failures=[]
    for name,digest in files.items():
        # Refuse escaping paths even when the manifest itself is malformed.
        rel=Path(name)
        if rel.is_absolute() or '..' in rel.parts:
            failures.append('unsafe manifest path: '+name);continue
        p=root/rel
        if not p.is_file():failures.append('missing: '+name)
        elif sha(p)!=digest:failures.append('changed: '+name)
    return failures

def expected_wrapper(source,w):
    s=source.replace('extends SceneTree','extends Node\nvar root\nvar exit_code=0')
    s=s.replace('var w=get_script().resource_path.get_base_dir()','var w='+json.dumps(str(w)))
    s=s.replace('func _initialize():\n visual="--capture" in OS.get_cmdline_user_args()\n call_deferred("run")','func _ready():\n root=get_tree().root\n visual=true\n call_deferred("run")')
    s=s.replace('await process_frame','await get_tree().process_frame').replace('quit(','finish(')
    return s+'\nfunc finish(code):\n exit_code=code\n if is_instance_valid(rig):rig.queue_free()\n queue_free()\n'

def audit_sources(w=W):
    f=load(w/'BASELINE_FREEZE.json');errors=[];files=f['source_files_sha256']|f['extra_manifests_sha256']
    for root in [Path(f['source_rig']),w/'rig']:
        errors.extend(str(root)+': '+e for e in verify_manifest(root,files))
    errors.extend('launcher: '+e for e in verify_manifest(w/'native_launcher',{n:d for n,d in files.items() if n!='project.godot'}))
    for release in [40,41]:
        p=f[f'published{release}_runtime_artwork_parity']
        errors.extend('runtime parity: '+e for e in verify_manifest(Path(p['path']),p['files_sha256']))
    base=(w/'rig/project.godot').read_text()
    base=re.sub(r'run/main_scene=.*','run/main_scene="res://launcher.tscn"',base)
    base=re.sub(r'config/name=.*','config/name="Ryoko EXP104 Triumphant Grin PREVIEW ONLY"',base)
    if (w/'native_launcher/project.godot').read_text()!=base:errors.append('unexpected launcher configuration change')
    for target,src in [('static','check_and_capture.gd'),('motion','render_motion.gd')]:
        if (w/f'native_launcher/{target}.gd').read_text()!=expected_wrapper((w/src).read_text(),w):errors.append('launcher wrapper differs: '+target)
    for key,digest in [('source_sheet','source_sheet_sha256'),('source_catalogue','catalogue_sha256')]:
        if sha(Path(f[key]))!=f[digest]:errors.append('reference changed: '+key)
    ref=load(w/'SOURCE_REFERENCE.json');root=Path(f['source_catalogue']).parent.parent
    errors.extend('reference panel: '+e for e in verify_manifest(root,ref['panel_hashes']))
    if len(f['source_files_sha256'])!=999 or sum(n.endswith('.png') for n in f['source_files_sha256'])!=184:errors.append('incorrect baseline counts')
    for root in [w/'rig',w/'native_launcher',Path(f['source_rig'])]:
        ids=[x['id'] for x in load(root/'expressions/registry.json')['entries']]
        if ids!=f['baseline_profile_ids'] or len(ids)!=36 or 'EXP-104' in ids:errors.append('disk registry changed')
    return dict(status='FAIL' if errors else 'PASS',failures=errors,baseline_files=999,baseline_png_files=184,common_runtime_files=993,baseline_profiles=36,artwork_changes=False,runtime_changes=False)

if __name__=='__main__':
    result=audit_sources();print(json.dumps(result,indent=2))
    raise SystemExit(result['status']!='PASS')

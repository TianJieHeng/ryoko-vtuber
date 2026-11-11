"""Offline byte restoration only. Never run a candidate, renderer, UI, or encoder."""
import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess

PACKAGE = Path(__file__).resolve().parent
SHA = lambda b: hashlib.sha256(b).hexdigest()
BLOB = lambda b: hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()

def safe_path(root, relative):
    p = PurePosixPath(relative)
    if p.is_absolute() or '..' in p.parts or not p.parts:
        raise ValueError('Unsafe relative path: '+relative)
    target = root.joinpath(*p.parts)
    if not target.resolve().is_relative_to(root.resolve()):
        raise ValueError('Path escapes root: '+relative)
    return target

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--git-dir', type=Path, required=True, help='Existing local Git object database containing both pinned commits and required blobs. No network fetch is performed.')
    ap.add_argument('--output', type=Path, required=True, help='New, nonexistent destination workspace root.')
    ap.add_argument('--verify-only', action='store_true', help='Check the existing output snapshot without writing any files.')
    args = ap.parse_args()
    data = gzip.decompress((PACKAGE/'RECONSTRUCTION_MANIFEST.json.gz').read_bytes())
    scope = json.loads((PACKAGE/'BACKUP_SCOPE.json').read_text())
    if SHA(data) != scope['manifest_uncompressed_sha256']:
        raise ValueError('Manifest hash mismatch')
    manifest = json.loads(data)
    root = args.output.resolve()
    if args.verify_only:
        if not root.is_dir(): raise ValueError('Existing output directory required')
    elif root.exists():
        raise FileExistsError('Refusing to alter existing output: '+str(root))
    env = dict(os.environ, GIT_NO_LAZY_FETCH='1', GIT_TERMINAL_PROMPT='0')
    git = ['git', '--git-dir='+str(args.git_dir.resolve())]
    trees = {}
    for commit in [manifest['main_commit'], manifest['headache_review_commit']]:
        raw = subprocess.check_output(git+['ls-tree','-r','-z',commit], env=env)
        tree = {}
        for entry in raw.split(b'\0'):
            if entry:
                head,path = entry.split(b'\t',1)
                mode,kind,oid = head.decode().split()
                if kind == 'blob': tree[path.decode()] = oid
        trees[commit] = tree
    # Validate every path and every pinned commit/path before creating output.
    for row in manifest['files']:
        safe_path(root,row['destination'])
        src = row['source']
        if src['kind'] == 'pinned_git':
            if trees[src['commit']].get(src['repository_path']) != src['git_blob']:
                raise ValueError('Pinned tree mismatch: '+row['destination'])
        elif src['kind'] == 'package': safe_path(PACKAGE,src['path'])
        else: raise ValueError('Unknown source kind')
    proc = subprocess.Popen(git+['cat-file','--batch'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, env=env)
    cache = {}
    total = 0
    try:
        for row in manifest['files']:
            src = row['source']
            if src['kind'] == 'pinned_git':
                oid = src['git_blob']
                if oid not in cache:
                    proc.stdin.write((oid+'\n').encode()); proc.stdin.flush()
                    header = proc.stdout.readline().decode().strip().split()
                    if len(header)!=3 or header[1]!='blob': raise ValueError('Missing local Git object: '+oid)
                    b = proc.stdout.read(int(header[2]))
                    if proc.stdout.read(1)!=b'\n' or BLOB(b)!=oid: raise ValueError('Git blob integrity failure')
                    cache[oid] = b
                b = cache[oid]
            else:
                stored = safe_path(PACKAGE,src['path']).read_bytes()
                if SHA(stored)!=src['stored_sha256']: raise ValueError('Stored artifact hash mismatch')
                if src['encoding']=='gzip': b=gzip.decompress(stored)
                elif src['encoding']=='identity': b=stored
                else: raise ValueError('Unknown encoding')
            if len(b)!=row['size'] or SHA(b)!=row['sha256']: raise ValueError('Restored input hash mismatch: '+row['destination'])
            dst = safe_path(root,row['destination'])
            if args.verify_only:
                if dst.read_bytes()!=b: raise ValueError('Existing byte mismatch: '+str(dst))
            else:
                dst.parent.mkdir(parents=True,exist_ok=True)
                with dst.open('xb') as f: f.write(b)
            total += len(b)
    finally:
        proc.stdin.close()
        proc.wait()
    print(json.dumps(dict(status='PASS',scope='Offline exact-byte source restoration only',files=len(manifest['files']),bytes=total,pinned_blobs_verified=len(cache),verify_only=args.verify_only,native_execution=False,mp4_generated=False),sort_keys=True))

if __name__=='__main__': main()

"""Restore exact saved bytes offline. No native execution, rendering, encoding or network."""
import argparse,gzip,hashlib,io,json,os,subprocess,tarfile
from pathlib import Path,PurePosixPath
P=Path(__file__).resolve().parent
H=lambda b:hashlib.sha256(b).hexdigest()
B=lambda b:hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def safe(root,rel):
 p=PurePosixPath(rel)
 if p.is_absolute() or '..' in p.parts or not p.parts:raise ValueError('Unsafe path')
 q=root.joinpath(*p.parts)
 if not q.resolve().is_relative_to(root.resolve()):raise ValueError('Path escapes root')
 return q
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--git-dir',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--verify-only',action='store_true');a=ap.parse_args()
 raw=gzip.decompress((P/'RECONSTRUCTION_MANIFEST.json.gz').read_bytes());scope=json.loads((P/'BACKUP_SCOPE.json').read_text());assert H(raw)==scope['manifest_uncompressed_sha256'];m=json.loads(raw)
 out=a.output.resolve()
 if a.verify_only:assert out.is_dir()
 elif out.exists():raise FileExistsError('Output must not already exist')
 env=dict(os.environ,GIT_NO_LAZY_FETCH='1',GIT_TERMINAL_PROMPT='0');git=['git','--git-dir='+str(a.git_dir.resolve())];trees={};cache={};archives={}
 for commit in sorted({r['source']['commit'] for r in m['files'] if r['source']['kind']=='pinned_git'}):
  raw=subprocess.check_output(git+['ls-tree','-r','-z',commit],env=env);tree={}
  for e in raw.split(b'\0'):
   if e:
    h,p=e.split(b'\t',1);mode,kind,oid=h.decode().split()
    if kind=='blob':tree[p.decode()]=oid
  trees[commit]=tree
 for row in m['files']:
  safe(out,row['destination']);s=row['source']
  if s['kind']=='pinned_git':assert trees[s['commit']].get(s['repository_path'])==s['git_blob']
 for name,arc in m['archives'].items():
  parts=[]
  for part in arc['parts']:
   b=safe(P,part['path']).read_bytes();assert len(b)==part['size'] and H(b)==part['sha256'];parts.append(b)
  b=b''.join(parts);assert len(b)==arc['size'] and H(b)==arc['sha256'];members={}
  with tarfile.open(fileobj=io.BytesIO(b),mode='r:xz') as t:
   for member in t.getmembers():
    assert member.isfile();safe(out,member.name);assert member.name not in members;members[member.name]=t.extractfile(member).read()
  assert len(members)==arc['members'];archives[name]=members
 proc=subprocess.Popen(git+['cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,env=env)
 try:
  total=0
  for row in m['files']:
   s=row['source'];kind=s['kind']
   if kind=='pinned_git':
    oid=s['git_blob']
    if oid not in cache:
     proc.stdin.write((oid+'\n').encode());proc.stdin.flush();header=proc.stdout.readline().decode().strip().split();assert len(header)==3 and header[1]=='blob'
     b=proc.stdout.read(int(header[2]));assert proc.stdout.read(1)==b'\n' and B(b)==oid;cache[oid]=b
    b=cache[oid]
    if s['encoding']=='gzip':b=gzip.decompress(b)
    else:assert s['encoding']=='identity'
   elif kind=='package':
    b=safe(P,s['path']).read_bytes();assert H(b)==s['stored_sha256']
    if s['encoding']=='gzip':b=gzip.decompress(b)
    else:assert s['encoding']=='identity'
   elif kind=='archive':b=archives[s['archive']][s['member']]
   else:raise ValueError('Unknown source kind')
   assert len(b)==row['size'] and H(b)==row['sha256'],row['destination'];dst=safe(out,row['destination'])
   if a.verify_only:assert dst.read_bytes()==b
   else:
    dst.parent.mkdir(parents=True,exist_ok=True)
    with dst.open('xb') as f:f.write(b)
   total+=len(b)
 finally:
  proc.stdin.close();proc.wait()
 print(json.dumps(dict(status='PASS',files=len(m['files']),bytes=total,pinned_blobs=len(cache),native_pngs=m['archives']['native_frames']['members'],verify_only=a.verify_only,native_execution=False,mp4_generated=False)))
if __name__=='__main__':main()

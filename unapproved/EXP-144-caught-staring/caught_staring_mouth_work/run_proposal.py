from pathlib import Path
import hashlib,json,os,subprocess,time,traceback
W=Path(__file__).resolve().parent;R=W.parent/'interested_skepticism_work/candidate/ryoko_object_rig';OUT=W/'proposal_01'
def engines():return [s for s in subprocess.check_output(['/bin/ps','-eo','pid=,comm='],text=True).splitlines() if s.split()[-1].lower().startswith('godot')]
def digest(root):
 h=hashlib.sha256()
 for p in sorted(root.rglob('*')):
  if p.is_file() and '.godot' not in p.parts:h.update(str(p.relative_to(root)).encode());h.update(hashlib.sha256(p.read_bytes()).digest())
 return h.hexdigest()
assert not OUT.exists(),'One attempt only; inspect before any retry.'
assert not engines(),'Another engine is active.'
free=os.statvfs(W).f_bavail*os.statvfs(W).f_frsize
memory=int(dict(x.split(':',1) for x in Path('/proc/meminfo').read_text().splitlines())['MemAvailable'].split()[0])*1024
assert free>100*1024**2 and memory>700*1024**2,(free,memory)
OUT.mkdir();before=digest(R);protected=W.parent/'approved_upper_iris_repair_integration/candidate/ryoko_object_rig';protected_before=digest(protected)
env=os.environ.copy()
env["LP_NUM_THREADS"]="2"
for key,folder in [('HOME','home'),('XDG_CACHE_HOME','cache'),('XDG_CONFIG_HOME','config'),('XDG_DATA_HOME','data')]:
 p=W/'native_environment'/folder;p.mkdir(parents=True,exist_ok=True);env[key]=str(p)
env['XDG_CACHE_HOME']=str(W/'cache')
argv=['/usr/local/bin/godot','--rendering-method','gl_compatibility','--audio-driver','Dummy','--path',str(R),'--script',str(W/'capture_proposal.gd'),'--',str(W),str(OUT)]
(OUT/'run.json').write_text(json.dumps({'argv':argv,'free_bytes':free,'available_memory':memory,'timeout_seconds':120,'LP_NUM_THREADS':'2','retry':'one whole warmed-cache attempt'},indent=2))
start=time.time();result={'status':'FAIL'};proc=None
try:
 with (OUT/'console.log').open('w') as log:
  proc=subprocess.Popen(argv,stdout=log,stderr=subprocess.STDOUT,env=env)
  proc.wait(timeout=120)
 assert proc.returncode==0,proc.returncode
 result['capture']=json.loads((OUT/'result.json').read_text())
 result['status']='CAPTURED'
except Exception as e:result['error']=repr(e)
finally:
 if proc and proc.poll() is None:
  proc.terminate()
  try:proc.wait(timeout=5)
  except subprocess.TimeoutExpired:proc.kill();proc.wait()
 result.update({'elapsed_seconds':time.time()-start,'candidate_base_unchanged':before==digest(R),'approved20_unchanged':protected_before==digest(protected),'remaining_engines':engines()})
 (OUT/'launch_result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))

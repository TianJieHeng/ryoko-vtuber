"""One leased native render. PNG frames stream to FFmpeg; only seven stills are kept."""
from pathlib import Path
import hashlib,json,os,socket,struct,subprocess,time,traceback
import sys
VIEW=sys.argv[1];assert VIEW in ['full','detail']
W=Path(__file__).resolve().parent;R=W.parent/'playful_kiss_performance_work/candidate/ryoko_object_rig';OUT=W/('preview_native_'+VIEW)
PLAN=json.loads((W/'capture_plan.json').read_text())
def digest_tree(root,skip_cache=False):
 h=hashlib.sha256()
 for f in sorted(root.rglob('*')):
  if f.is_file() and (not skip_cache or '.godot' not in f.relative_to(root).parts):h.update(str(f.relative_to(root)).encode());h.update(hashlib.sha256(f.read_bytes()).digest())
 return h.hexdigest()
def engines():return [s for s in subprocess.check_output(['/bin/ps','-eo','pid=,comm='],text=True).splitlines() if s.split()[-1].lower().startswith('godot')]
assert not OUT.exists(),'Prior attempt exists; inspect before considering another launch.'
assert not engines(),'Godot already active.'
free=os.statvfs(W).f_bavail*os.statvfs(W).f_frsize
mem=int(dict(x.split(':',1) for x in Path('/proc/meminfo').read_text().splitlines())['MemAvailable'].split()[0])*1024
assert free>64*1024**2 and mem>700*1024**2,(free,mem)
OUT.mkdir();(OUT/'stills').mkdir();before=digest_tree(R,True)
B=W.parent/'approved_upper_iris_repair_integration/candidate/ryoko_object_rig';base_before=digest_tree(B)
env=os.environ.copy();env["LP_NUM_THREADS"]="2"
for key,folder in [('HOME','home'),('XDG_CACHE_HOME','cache'),('XDG_CONFIG_HOME','config'),('XDG_DATA_HOME','data')]:
 p=W/'native_environment'/folder;p.mkdir(parents=True,exist_ok=True);env[key]=str(p)
env['XDG_CACHE_HOME']=str(W.parent/'caught_staring_onset_work/cache')
server=socket.socket();server.bind(('127.0.0.1',0));server.listen(1);server.settimeout(1);port=server.getsockname()[1]
argv=['/usr/local/bin/godot','--audio-driver','Dummy','--path',str(R),'--script',str(W/'capture_cycle_native.gd'),'--','--output='+str(OUT),'--port='+str(port),'--view='+VIEW]
ff=['/usr/bin/ffmpeg','-v','error','-threads','1','-filter_threads','1','-f','image2pipe','-framerate','30','-vcodec','png','-i','pipe:0','-an','-c:v','libx264','-threads','1','-preset','fast','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart','-metadata','title=EXP-144 Caught staring | One 30 fps cycle | Unapproved',str(OUT/f'EXP144_caught_staring_{VIEW}.mp4')]
(OUT/'run.json').write_text(json.dumps({'godot':argv,'ffmpeg':ff,'free_bytes':free,'available_memory_bytes':mem,'source_sha256':before,'started_unix':time.time()},indent=2))
result={'status':'FAIL'};proc=None;encoder=None;conn=None;received=0;start=time.time()
try:
 with (OUT/'console.log').open('w') as log,(OUT/'encoder.log').open('w') as enc_log:
  encoder=subprocess.Popen(ff,stdin=subprocess.PIPE,stderr=enc_log)
  proc=subprocess.Popen(argv,stdout=log,stderr=subprocess.STDOUT,env=env)
  while conn is None:
   try:conn,_=server.accept()
   except socket.timeout:
    if proc.poll() is not None:raise RuntimeError('Engine ended before stream: '+log.name)
    if time.time()-start>60:raise TimeoutError('No encoder connection within 60 seconds')
  conn.settimeout(60)
  def read_exact(n):
   chunks=[]
   while n:
    chunk=conn.recv(min(n,1024*1024))
    if not chunk:raise EOFError('Incomplete frame stream')
    chunks.append(chunk);n-=len(chunk)
   return b''.join(chunks)
  for i in range(PLAN['frames']):
   if time.time()-start>240:raise TimeoutError('Capture exceeded 240 seconds')
   size=struct.unpack('!I',read_exact(4))[0];assert 0<size<10*1024*1024,size
   data=read_exact(size);encoder.stdin.write(data);received+=1
   if i in PLAN['saved_frames']:(OUT/'stills'/f'{i:03d}.png').write_bytes(data)
  encoder.stdin.close();encoder.wait(timeout=60);proc.wait(timeout=30)
  assert encoder.returncode==0 and proc.returncode==0,(encoder.returncode,proc.returncode)
  actual=json.loads((OUT/'capture_result.json').read_text());assert actual['status']=='PASS' and len(actual['frames'])==157,actual.get('failures')
  videos={}
  for label in [VIEW]:
   path=OUT/f'EXP144_caught_staring_{label}.mp4'
   p=json.loads(subprocess.check_output(['/usr/bin/ffprobe','-v','error','-count_frames','-show_entries','stream=width,height,r_frame_rate,nb_read_frames,duration','-of','json',str(path)]))['streams'][0]
   assert p['nb_read_frames']=='157' and p['r_frame_rate']=='30/1',p
   videos[label]=p|{'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
  result={'status':'PASS','videos':videos,'frames':157,'profile_seconds':5.2,'video_seconds':157/30,'live_engine_pacing_measured':False}
except Exception as exc:result['error']=repr(exc);result['traceback']=traceback.format_exc()
finally:
 if conn:conn.close()
 server.close()
 for p in (proc,encoder):
  if p and p.poll() is None:
   p.terminate()
   try:p.wait(timeout=5)
   except subprocess.TimeoutExpired:p.kill();p.wait()
 result|={'received_frames':received,'engine_returncode':proc.poll() if proc else None,'encoder_returncode':encoder.poll() if encoder else None,'candidate_source_unchanged':before==digest_tree(R,True),'approved20_unchanged':base_before==digest_tree(B),'remaining_engines':engines(),'elapsed_seconds':time.time()-start}
 if not result['candidate_source_unchanged'] or not result['approved20_unchanged'] or result['remaining_engines']:result['status']='FAIL'
 (OUT/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))

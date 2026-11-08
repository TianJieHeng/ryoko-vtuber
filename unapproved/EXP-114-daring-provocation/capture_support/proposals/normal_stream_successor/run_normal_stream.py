"""One leased frozen stage, no import/retry/refit. Native stages require supported CUA wrapper launch."""
from pathlib import Path
import datetime,json,os,subprocess,sys,time,traceback
from verify_normal_inputs import W,sha,verify,BINDING
assert len(sys.argv)>=3;stage=sys.argv[1];assert stage=='normal'
flags=['--coordinator-godot-slot-granted']+([] if stage=='headless' else ['--coordinator-display-lease-granted','--independent-pre-render-review-approved'])
assert sys.argv[2:]==flags
binding=sha(BINDING);guard_path=W/'evidence/NORMAL_STREAM_PRE_GUARD.json';guard=json.loads(guard_path.read_text())
assert guard['status']=='PASS' and guard['stage']==stage and guard['binding_sha256']==binding
assert 0<=(datetime.datetime.now(datetime.timezone.utc)-datetime.datetime.fromisoformat(guard['time_utc'])).total_seconds()<600
assert guard['review_sha256']==sha(W/'evidence'/('NORMAL_STREAM_REVIEW_APPROVAL.json')) and guard['lease_sha256']==sha(W/'evidence'/('NORMAL_STREAM_LEASE.json'))
def active():return [s.strip() for s in subprocess.check_output(['/bin/ps','-eo','pid=,comm='],text=True).splitlines() if len(s.split())>1 and s.split()[1].lower().startswith('godot')]
assert not active(),'Godot occupied'
pre=verify();out=W/(stage+'_01');assert not out.exists(),'Attempt exists; never retry';out.mkdir();(out/'PRE_RUN_IDENTITY.json').write_text(json.dumps(pre,indent=2)+'\n')
env=os.environ.copy();env['GODOT_SILENCE_ROOT_WARNING']='1'
for key,folder in [('HOME','home'),('XDG_CACHE_HOME','cache'),('XDG_CONFIG_HOME','config'),('XDG_DATA_HOME','data')]:
 p=W/'runtime_environment'/folder;p.mkdir(parents=True,exist_ok=True);env[key]=str(p)
if stage=='headless':jobs=json.loads((W/'plan/HEADLESS_JOBS.json').read_text())['jobs']
else:
 script='review_daring_provocation_trajectory.gd' if stage=='native' else 'review_daring_provocation_normal_playback.gd'
 args=flags+['--output={output}']+(['--plan='+str(W/'capture_plan.json')] if stage=='native' else [])
 jobs=[{'name':stage,'tree':'candidate','script':'res://tools/'+script,'args':args,'timeout_seconds':1200 if stage=='native' else 180}]
rows=[];code=1
try:
 for job in jobs:
  assert not active(),'Godot occupied between serial jobs';verify()
  argv=['/usr/local/bin/godot']+(['--headless'] if stage=='headless' else [])+['--audio-driver','Dummy','--path',str(W/'runtime'/job['tree']),'--script',job['script'],'--']+[x.replace('{output}',str(out)) for x in job['args']]
  log=out/(job['name']+'.log');started=time.time();row={'name':job['name'],'argv':argv,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'binding_sha256':binding,'guard_sha256':sha(guard_path)}
  (out/'CURRENT_STARTED.json').write_text(json.dumps(row,indent=2)+'\n')
  with log.open('w') as stream:
   proc=subprocess.Popen(argv,stdout=stream,stderr=subprocess.STDOUT,env=env)
   while proc.poll() is None:
    time.sleep(.25)
    errors=[line for line in log.read_text().splitlines() if line.startswith(('SCRIPT ERROR','ERROR:'))]
    if errors or time.time()-started>job['timeout_seconds']:
     proc.terminate()
     try:proc.wait(timeout=10)
     except subprocess.TimeoutExpired:proc.kill();proc.wait()
     row['stopped_on_error_or_timeout']=True;break
  row|={'returncode':proc.returncode,'seconds':time.time()-started,'log_sha256':sha(log)};rows.append(row)
  (out/'RUN_ROWS.json').write_text(json.dumps(rows,indent=2)+'\n')
  verify();text=log.read_text();assert proc.returncode==0 and not row.get('stopped_on_error_or_timeout') and 'SCRIPT ERROR' not in text and '\nERROR:' not in text,(job['name'],'STOP_FIRST_UNEXPECTED_FAILURE')
  print(json.dumps(row),flush=True)
 if stage=='headless':
  a=json.loads((out/'prior18_approved.json').read_text());b=json.loads((out/'prior18_candidate.json').read_text());assert a==b and not a['failures'],'old18 exact parity failed'
  from verify_records import verify_run
  trajectory=verify_run(out/'trajectory',False)
  result={'status':'PASS','binding_sha256':binding,'jobs':rows,'prior18_exact_samples':a['samples'],'trajectory':trajectory}
  target=W/'evidence/HEADLESS_VERIFICATION.json';assert not target.exists();target.write_text(json.dumps(result,indent=2)+'\n')
 elif stage=='native':
  from verify_records import verify_run
  result=verify_run(out,True);result['binding_sha256']=binding
  target=W/'evidence/NATIVE_VERIFICATION.json';assert not target.exists();target.write_text(json.dumps(result,indent=2)+'\n')
 else:
  result=json.loads((out/'evidence.json').read_text());assert result['status']=='PASS' and len(result['cycles'])==4 and not result['failures']
  assert [(c['view'],c['cycle']) for c in result['cycles']]==[('bust',0),('bust',1),('native',0),('native',1)]
  for cycle in result['cycles']:
   assert cycle['samples'] and cycle['samples'][-1]['state']['active_expression']=='' and all(v==0 for v in cycle['samples'][-1]['state']['controls'].values())
  # A review must assess timing/dropouts and actual CUA observation before calling playback visually accepted.
 code=0
except Exception as exc:
 (out/'FAILURE.json').write_text(json.dumps({'status':'FAIL','exception':repr(exc),'traceback':traceback.format_exc()},indent=2)+'\n');print(traceback.format_exc(),flush=True)
finally:
 result={'status':'PASS' if code==0 else 'FAIL','returncode':code,'binding_sha256':binding,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'remaining_godot_processes':active()}
 result['lease_released']=not result['remaining_godot_processes']
 try:result['post_identity']=verify()
 except Exception as exc:result['post_identity_error']=repr(exc);result['status']='FAIL';code=1
 if not result['lease_released']:code=1
 result['status']='PASS' if code==0 else 'FAIL';result['returncode']=code
 (out/'RUN_RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
raise SystemExit(code)

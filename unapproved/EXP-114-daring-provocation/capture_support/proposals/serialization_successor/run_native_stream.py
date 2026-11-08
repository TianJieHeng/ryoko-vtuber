"""One supported-CUA-launched combined native trajectory/pixel attempt. No import or retry."""
import datetime,json,os,subprocess,sys,time,traceback
from verify_native_stream_inputs import W,P,BINDING,sha,verify,require_review_and_lease
flags=['--coordinator-godot-slot-granted','--coordinator-display-lease-granted','--independent-pre-render-review-approved'];assert sys.argv[1:]==flags
review,lease=require_review_and_lease();binding=sha(BINDING);gp=W/'evidence/NATIVE_STREAM_PRE_GUARD.json';guard=json.loads(gp.read_text())
assert guard['status']=='PASS' and guard['stage']=='native_stream_01' and guard['binding_sha256']==binding
assert 0<=(datetime.datetime.now(datetime.timezone.utc)-datetime.datetime.fromisoformat(guard['time_utc'])).total_seconds()<600
assert guard['review_sha256']==sha(W/'evidence/NATIVE_STREAM_REVIEW_APPROVAL.json') and guard['lease_sha256']==sha(W/'evidence/NATIVE_STREAM_LEASE.json')
def active():return [s.strip() for s in subprocess.check_output(['/bin/ps','-eo','pid=,comm='],text=True).splitlines() if len(s.split())>1 and s.split()[1].lower().startswith('godot')]
assert not active();pre=verify();out=W/'native_stream_01';assert not out.exists();out.mkdir();(out/'PRE_RUN_IDENTITY.json').write_text(json.dumps(pre,indent=2)+'\n')
env=os.environ.copy();env['GODOT_SILENCE_ROOT_WARNING']='1'
for key,folder in [('HOME','home'),('XDG_CACHE_HOME','cache'),('XDG_CONFIG_HOME','config'),('XDG_DATA_HOME','data')]:
 path=W/'runtime_environment'/folder;path.mkdir(parents=True,exist_ok=True);env[key]=str(path)
argv=['/usr/local/bin/godot','--audio-driver','Dummy','--path',str(W/'runtime/candidate'),'--script',str(P/'trajectory_record_files.gd'),'--',*flags,'--plan='+str(W/'capture_plan.json'),'--output='+str(out)]
started={'argv':argv,'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'binding_sha256':binding,'guard_sha256':sha(gp),'route':'One supported Sky/CUA Thunar Open With custom /bin/sh, Use as default OFF','cold_import':False,'headless':False,'combined_native_trajectory_pixel_gate':True,'old_failed_trajectory_not_reused':True};(out/'RUN_STARTED.json').write_text(json.dumps(started,indent=2)+'\n')
code=1;proof=None;process_receipt={};proc=None
try:
 t=time.time();log=out/'console.log'
 with log.open('w') as stream:
  proc=subprocess.Popen(argv,stdout=stream,stderr=subprocess.STDOUT,env=env)
  while proc.poll() is None:
   time.sleep(.25)
   errors=[line for line in log.read_text().splitlines() if line.startswith(('SCRIPT ERROR','ERROR:'))]
   if errors or time.time()-t>1800:
    proc.terminate()
    try:proc.wait(timeout=10)
    except subprocess.TimeoutExpired:proc.kill();proc.wait()
    process_receipt['stopped_on_error_or_timeout']=True;break
 process_receipt|={'returncode':proc.returncode,'seconds':time.time()-t,'log_sha256':sha(log)};assert proc.returncode==0 and not process_receipt.get('stopped_on_error_or_timeout'),'STOP_FIRST_UNEXPECTED_FAILURE'
 text=log.read_text();assert 'SCRIPT ERROR' not in text and not any(s.startswith('ERROR:') for s in text.splitlines())
 verify()
 from verify_native_record_files import verify_run
 proof=verify_run(out);assert proof['status']=='PASS' and not proof['headless_native_cross_run_comparison_performed'] and proof['render_invariance_captures_verified']==1402
 proof|={'binding_sha256':binding,'accepted_runtime_checks':5380806,'accepted_prior18_parity_samples':3230,'independent_runtime_review_sha256':sha(W.parent/'daring_provocation_independent_review/PERFORMANCE_HEADLESS_02_FAILURE_REVIEW.json'),'old_failed_job21_not_pass':True};code=0
except Exception as exc:
 (out/'FAILURE.json').write_text(json.dumps({'status':'FAIL','exception':repr(exc),'traceback':traceback.format_exc()},indent=2)+'\n');print(traceback.format_exc(),flush=True)
finally:
 if proc is not None and proc.poll() is None:
  proc.terminate()
  try:proc.wait(timeout=10)
  except subprocess.TimeoutExpired:proc.kill();proc.wait()
 result={'binding_sha256':binding,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'engine':process_receipt,'remaining_godot_processes':active()};result['lease_released']=not result['remaining_godot_processes']
 try:result['post_identity']=verify()
 except Exception as exc:result['post_identity_error']=repr(exc);code=1
 if not result['lease_released']:code=1
 result['status']='PASS' if code==0 else 'FAIL';result['returncode']=code
 if code==0:
  target=W/'evidence/NATIVE_STREAM_VERIFICATION.json';assert not target.exists();target.write_text(json.dumps(proof,indent=2)+'\n');result['verification_sha256']=sha(target)
 (out/'RUN_RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
raise SystemExit(code)

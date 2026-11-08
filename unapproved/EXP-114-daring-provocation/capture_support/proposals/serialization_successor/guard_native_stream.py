"""Fresh separately awaited native-only guard. No engine launch."""
import datetime,json,subprocess
from verify_native_stream_inputs import W,P,BINDING,sha,verify,require_review_and_lease
assert not (W/'native_stream_01').exists(),'Preserve prior attempt; no retry'
target=W/'evidence/NATIVE_STREAM_PRE_GUARD.json';assert not target.exists()
review,lease=require_review_and_lease();identity=verify()
active=[s.strip() for s in subprocess.check_output(['/bin/ps','-eo','pid=,comm='],text=True).splitlines() if len(s.split())>1 and s.split()[1].lower().startswith('godot')];assert not active,active
result={'status':'PASS','stage':'native_stream_01','time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'binding_sha256':sha(BINDING),'review_sha256':sha(W/'evidence/NATIVE_STREAM_REVIEW_APPROVAL.json'),'lease_sha256':sha(W/'evidence/NATIVE_STREAM_LEASE.json'),'identity':identity,'godot_processes':active}
target.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))

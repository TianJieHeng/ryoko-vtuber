"""Run as a separate awaited call; this guard never launches an engine."""
import datetime,json,subprocess,sys
from pathlib import Path
from verify_normal_inputs import W,sha,verify,BINDING
assert sys.argv[1:]==['normal']
stage=sys.argv[1];binding=sha(BINDING);output=W/(stage+'_01');target=W/'evidence'/'NORMAL_STREAM_PRE_GUARD.json'
assert not output.exists() and not target.exists(),'Preserve every attempt and prior guard; no automatic retry'
review_path=W/'evidence'/'NORMAL_STREAM_REVIEW_APPROVAL.json';lease_path=W/'evidence'/'NORMAL_STREAM_LEASE.json'
review=json.loads(review_path.read_text());lease=json.loads(lease_path.read_text())
assert review['approved'] is True and review['stage']==stage and review['binding_sha256']==binding
assert sha(Path(review['review_path']))==review['review_sha256']
assert lease['exclusive_godot_lease'] is True and lease['binding_sha256']==binding and lease['stage']==stage
assert lease['display_lease']==(stage!='headless')
# Successful combined native-stream receipts replace the unavailable failed headless trajectory.
# verify() binds and validates the new successful run and all its immutable artifacts.
identity=verify()
active=[s.strip() for s in subprocess.check_output(['/bin/ps','-eo','pid=,comm='],text=True).splitlines() if len(s.split())>1 and s.split()[1].lower().startswith('godot')]
assert not active,('engine occupied',active)
result={'status':'PASS','stage':stage,'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'binding_sha256':binding,'review_sha256':sha(review_path),'lease_sha256':sha(lease_path),'identity':identity,'godot_processes':active}
target.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))

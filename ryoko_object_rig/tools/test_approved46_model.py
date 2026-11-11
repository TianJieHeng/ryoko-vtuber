"""Dense, deterministic pure-Python model checks. Never launches Godot."""
import copy,hashlib,json,math,sys
from pathlib import Path
from approved45_model import *
R=Path(__file__).resolve().parents[1];V=R/'validation/approved_exasperated_sigh'
checks=0;failures=[];counts={};maximum_review_error=0.
def check(ok,label):
 global checks
 checks+=1
 if not ok:
  if len(failures)<30:failures.append(label)
  if len(failures)==30:raise AssertionError(failures)
def valid(p,label):
 check(scoped_valid(p),label+' scope');check(mouth_valid(p),label+' mouth')
 for k,(lo,hi) in BOUNDS.items():check(math.isfinite(p[k]) and lo<=p[k]<=hi,label+' bounds '+k)
def timed(d,hz):return sorted({min(i/hz,d['duration']) for i in range(math.ceil(d['duration']*hz)+1)}|{f['time'] for f in d['keyframes']})
def schema(d):
 check(set(d)<=set(['id','title','duration','keyframes','status','intent','source_catalogue_sha256','timing_origin','scope','interpolation']),'definition keys')
 check(type(d['duration']) in (int,float) and math.isfinite(d['duration']) and d['duration']>0,'duration')
 check(d['keyframes'][0]['time']==0 and d['keyframes'][-1]['time']==d['duration'],'timeline span')
 last=-1
 for f in d['keyframes']:
  check(set(f)=={'time','phase','values'},'keyframe keys');check(type(f['time']) in (int,float) and math.isfinite(f['time']) and last<f['time']<=d['duration'],'time');last=f['time']
  check(type(f['phase'])==str and bool(f['phase']),'phase');check(set(f['values'])<=set(CHANNELS),'channels')
  for k,v in f['values'].items():check(type(v) in (int,float) and math.isfinite(v) and BOUNDS[k][0]<=v<=BOUNDS[k][1],'finite value')
  p=neutral();p.update(f['values']);valid(p,d['id'])
 for f in [d['keyframes'][0],d['keyframes'][-1]]:check(all(v==0 for v in f['values'].values()),'neutral endpoints')
 for a,b in zip(d['keyframes'],d['keyframes'][1:]):
  x,y=a['values'],b['values']
  check(not(max(x.get('mouth_open',0),y.get('mouth_open',0))>0 and(width(x) or width(y))),'whole segment mouth')
  if max(x.get('opening_px',0),y.get('opening_px',0))>0:check(all(x.get(k,0)==y.get(k,0)==0 for k in CONFLICTS),'whole opening segment')
  if max(x.get('aversion_px',0),y.get('aversion_px',0))>0:
   check(all(min(x.get(k,0),y.get(k,0))>=.18 for k in ['blink_L','blink_R']),'whole aversion support')
   check(all(x.get(k,0)==y.get(k,0)==0 for k in ['gaze_x','gaze_y','gaze_down_extra','eye_smile_L','eye_smile_R']),'whole aversion segment')
  if max(x.get('uneasy_weight',0),y.get('uneasy_weight',0))>0:check(all(x.get(k,0)==y.get(k,0)==0 for k in ['mouth_open','mouth_kiss']),'whole uneasy segment')
defs={};entries=json.loads((R/'expressions/registry.json').read_text())['entries'];old=json.loads((R/'historical_capture_metadata/approved45_before_exasperated_sigh/expressions/registry.json').read_text())['entries'];identities=json.loads((V/'approved_review_identity.json').read_text())['profiles'];new=[i['id'] for i in identities]
check(len(entries)==46 and entries[:45]==old and [e['id'] for e in entries[45:]]==new,'registry exact extension')
names={}
for e in entries:
 d=json.loads((R/e['path'][6:]).read_text());schema(d);check(e['id']==d['id'],'profile ID');defs[e['id']]=d
 for name in [e['id']]+e.get('aliases',[]):check(name not in names,'alias unique');names[name]=e['id']
counts['validated_profiles']=len(defs);counts['registered_aliases']=len(names)-len(defs)
# Comparison uses exact old definitions and same unchanged mathematical controller.
prior={e['id']:copy.deepcopy(defs[e['id']]) for e in old};counts['prior45_samples_at_60hz']=0
for id,d in prior.items():
 a=Model(defs);b=Model(prior);a.play(id);b.play(id);last=0
 for t in timed(d,60):
  a.advance(t-last);b.advance(t-last);last=t;check(a.pose==b.pose,'prior45 exact model '+id);valid(a.pose,id);counts['prior45_samples_at_60hz']+=1
counts['approved_review_pose_samples']=0
for item in identities:
 r=json.loads((R/item['motion_path']).read_text());check(r['profile_sha256']==item['profile_sha256'],'historical exact profile');check([x['frame'] for x in r['records']]==list(range(145)),'review record order');m=Model(defs);m.play(item['id']);last=0
 for frame in r['records']:
  t=frame['time'];m.advance(t-last);last=t
  for k in CHANNELS:
   err=abs(m.pose[k]-frame['pose'][k]);maximum_review_error=max(maximum_review_error,err);check(err<1e-7,'review pose '+item['id']+' '+str(frame['frame'])+' '+k)
  valid(m.pose,'review');counts['approved_review_pose_samples']+=1
counts['all46_samples_at_240hz']=0
for id,d in defs.items():
 m=Model(defs);m.play(id);last=0
 for t in timed(d,240):m.advance(t-last);last=t;valid(m.pose,'standalone');counts['all46_samples_at_240hz']+=1
 check(m.pose==neutral() and not m.active,'standalone exact neutral')
counts.update(directed_pairs=0,cross_key_midpoint_cases=0,cross_boundary_samples=0,interrupted_lifecycle_cases=0)
boundaries=sorted({i/200 for i in range(61)}|{.000001,.099999,.100001,.149999,.150001,.199999,.200001,.299999,.300001,.45,.61})
for source,d in defs.items():
 times=sorted({f['time'] for f in d['keyframes']}|{(a['time']+b['time'])/2 for a,b in zip(d['keyframes'],d['keyframes'][1:])})
 for target in defs:
  if source not in new and target not in new:continue
  counts['directed_pairs']+=1
  for st in times:
   m=Model(defs);m.auto_blink=True;m.play(source);m.advance(st);before=m.pose.copy();check(m.play(target),'play');check(m.pose==before,'cross C0');last=0
   for t in boundaries:m.advance(t-last);last=t;valid(m.pose,'cross');counts['cross_boundary_samples']+=1
   m.advance(20);check(m.pose==neutral() and not m.active and m.release_time<0 and m.auto_blink and not m.pending,'cross end+blink');counts['cross_key_midpoint_cases']+=1
   for action in ['release','restart','repeated_release','reset','manual_takeover']:
    m=Model(defs);m.auto_blink=True;m.play(source);m.advance(st);m.play(target);m.advance(.15);before=m.pose.copy()
    if action in ['release','repeated_release']:m.release()
    elif action=='restart':m.play(target)
    elif action=='reset':m.reset()
    else:m.manual_takeover()
    if action not in ['reset','manual_takeover']:check(m.pose==before,'lifecycle C0')
    m.advance(.15);valid(m.pose,'lifecycle')
    if action=='repeated_release':before=m.pose.copy();m.release();check(m.pose==before,'second release C0')
    if action=='manual_takeover':check(not m.pending and not m.auto_blink and not m.active,'manual cancels blink intent');m.reset()
    m.advance(20);check(m.pose==neutral() and not m.active and m.release_time<0,'lifecycle neutral')
    check((not m.auto_blink and not m.pending) if action in ['reset','manual_takeover'] else (m.auto_blink and not m.pending),'lifecycle blink');counts['interrupted_lifecycle_cases']+=1
# Invalid API inputs are transactional in the model; these do not test Godot's API.
m=Model(defs);m.play(new[0]);m.advance(1);before=copy.deepcopy(m.__dict__)
for bad in [-1,float('nan'),float('inf'),True,'0',None]:check(not m.advance(bad) and m.__dict__==before,'invalid delta is transactional')
check(not m.play('EXP-091') and m.__dict__==before,'unregistered ID is transactional')
out={'status':'PASS' if not failures else 'FAIL','checks':checks,'failures':failures,**counts,'maximum_review_pose_error':maximum_review_error,'runtime_sha256':hashlib.sha256((R/'expression_rig.gd').read_bytes()).hexdigest(),'scope':'Pure-Python mathematical model of byte-unchanged GDScript. Compared all 45 old profiles and all 145 historical EXP-046 native pose records; densely sampled all46 and all directed transitions involving the single EXP-046 addition. No engine, scene, rendering setter, actual auto-blink display, or native pixel execution.','godot_executed':False,'native_rendering_executed':False,'historical_tests_rerun':False,'ci_run':False}
output=Path(sys.argv[1]) if len(sys.argv)>1 else V/'python_model_checks.json';output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));sys.exit(bool(failures))

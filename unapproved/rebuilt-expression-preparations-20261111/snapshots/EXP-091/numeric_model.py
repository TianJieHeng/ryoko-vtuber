"""Read-only stdlib numeric model of unchanged runtime equations, not a Godot test."""
import hashlib
import json
import math
import re
from pathlib import Path
W=Path(__file__).resolve().parent

def load(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(obj): return (json.dumps(obj,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def contract(root=W):
    src=(root/'rig/expression_registry.gd').read_text()
    text=re.search(r'const CHANNEL_BOUNDS=(\{.*\})',src).group(1)
    bounds=json.loads(text.replace('Limits.GAZE_MIN','-1.0').replace('Limits.GAZE_MAX','1.0'))
    return dict(sorted(bounds.items()))
BOUNDS=contract()
CHANNELS=tuple(sorted(BOUNDS))
ACTING=tuple(sorted(('brow_screen_left','brow_screen_right','brow_tilt_screen_left',
    'brow_tilt_screen_right','brow_inner_lift_screen_left','brow_inner_lift_screen_right',
    'blink_L','blink_R','eye_smile_L','eye_smile_R','mouth_open','mouth_purse',
    'mouth_lip_press','mouth_corner_lift','mouth_smile','blush_intensity')))
INTERRUPTIONS=(.35,.55,.9,1.25,1.65,2.25,2.75,3.3,3.75)

def neutral(): return dict.fromkeys(CHANNELS,0.0)
def smooth(u):
    u=min(1.0,max(0.0,u)); return u*u*(3.0-2.0*u)
def mix(a,b,u): return {k:a.get(k,0.0)+(b.get(k,0.0)-a.get(k,0.0))*u for k in CHANNELS}
def sample(profile,t):
    if t<=0 or t>=profile['duration']: return neutral()
    for a,b in zip(profile['keyframes'],profile['keyframes'][1:]):
        if a['time']<=t<=b['time']:
            return mix(a['values'],b['values'],smooth((t-a['time'])/(b['time']-a['time'])))
    raise ValueError('Timeline gap')
def independent_sample(profile,t):
    """Alternate evaluation for numerical comparison, no shared interpolation helper."""
    out=neutral()
    if not 0<t<profile['duration']: return out
    a,b=next((a,b) for a,b in zip(profile['keyframes'],profile['keyframes'][1:]) if a['time']<=t<=b['time'])
    u=(t-a['time'])/(b['time']-a['time']); w=3*u*u-2*u*u*u
    for k in CHANNELS: out[k]=(1-w)*a['values'].get(k,0)+w*b['values'].get(k,0)
    return out

def playing(profile,t,source=None):
    target=sample(profile,t)
    return mix(source or neutral(),target,smooth(t/.30)) if t<.30 else target

def release_pose(source,t): return mix(source,neutral(),smooth(t/.45))

def valid_definition(p):
    allowed={'id','title','duration','keyframes','status','intent','source_catalogue_sha256','timing_origin','scope','interpolation'}
    if set(p)-allowed: raise ValueError('Unknown definition metadata')
    number=lambda v:type(v) in (int,float) and math.isfinite(v)
    if not number(p['duration']) or p['duration']<=0: raise ValueError('Duration')
    frames=p['keyframes']
    if len(frames)<2 or frames[0]['time']!=0 or frames[-1]['time']!=p['duration']: raise ValueError('Timeline endpoints')
    previous=-1
    for f in frames:
        if set(f)!= {'time','phase','values'} or not isinstance(f['phase'],str) or not f['phase']: raise ValueError('Key schema')
        t=f['time']
        if not number(t) or not previous<t<=p['duration']: raise ValueError('Key order')
        previous=t
        for k,v in f['values'].items():
            if k not in BOUNDS or not number(v) or not BOUNDS[k][0]<=v<=BOUNDS[k][1]: raise ValueError('Control '+k)
    if any(v!=0 for f in (frames[0],frames[-1]) for v in f['values'].values()): raise ValueError('Nonneutral endpoints')
    # EXP091 does not use scoped parts or independent width/kiss; their bridges
    # are deliberately not modeled. Guard the model's domain explicitly.
    for f in frames:
        if any(v!=0 for k,v in f['values'].items() if k not in ACTING): raise ValueError('Outside reconstruction model scope')
    return True

def in_scope(p):
    return (set(p)==set(CHANNELS) and all(math.isfinite(v) and BOUNDS[k][0]<=v<=BOUNDS[k][1] for k,v in p.items())
        and all(p[k]==0 for k in CHANNELS if k not in ACTING)
        and all(p[a]==p[b] for a,b in [('blink_L','blink_R'),('eye_smile_L','eye_smile_R'),
          ('brow_screen_left','brow_screen_right'),('brow_inner_lift_screen_left','brow_inner_lift_screen_right')])
        and p['brow_tilt_screen_left']==-p['brow_tilt_screen_right'])

def geometry(p):
    """Analytic source-space predictions only, not observed transforms or pixels."""
    spread=p['mouth_spread']*p['mouth_smile']
    purse=p['mouth_purse']; smile=p['mouth_smile']; corner=p['mouth_corner_lift']
    def lip(x):
        radius=min(1,abs((x-39.5)/35.5))
        upper=-4*spread-(4+5*spread)*smile*radius**1.5-12*corner*radius**3+purse*(4+8*radius**2)
        curve=max(0,1-radius*radius)**.72
        aperture=(1-smile)+smile*curve
        if purse:
            signed_width=1+20*spread/35.5-14*purse/35.5
            cavity=(38-12*p['mouth_open']*.55)*(1-smile)+35.5*smile+20*spread-14*purse
            h=min(1,abs((x-39.5)*signed_width)/cavity)
            aperture=(1-purse)*aperture+purse*math.sqrt(max(0,1-h*h))
        gap=max(0,p['mouth_open']*.55*54*aperture-1.5*purse*min(p['mouth_open']*4,1))
        return {'x':x,'upper_y':upper,'lower_y':upper+gap,'gap':gap}
    return {'mouth_width_source_px':71+40*spread-28*purse,
        'lip_samples':[lip(x) for x in (4.,39.5,75.)],
        'eye_effective_closure':max(p['blink_L'],min(p['eye_smile_L']*2,1)),
        'eye_curved_shape':min(1,max(0,(p['eye_smile_L']-.5)*2)),
        'brow_angle_degrees':{'screen_left':8*p['brow_tilt_screen_left']-26*p['brow_inner_lift_screen_left'],
                              'screen_right':8*p['brow_tilt_screen_right']+26*p['brow_inner_lift_screen_right']},
        'brow_vertical_source_px':-10*p['brow_screen_left']}

class Lifecycle:
    """Restricted analytic lifecycle; no claim to execute actual controller."""
    def __init__(self,profile):
        valid_definition(profile); self.profile=profile; self.reset()
    def reset(self): self.pose=neutral(); self.source=neutral(); self.t=0.; self.mode='manual'
    def trigger(self): self.source=dict(self.pose); self.t=0.; self.mode='playing'
    def release(self): self.source=dict(self.pose); self.t=0.; self.mode='release'
    def manual(self,values):
        if set(values)-set(ACTING): raise ValueError('manual outside model scope')
        p=dict(self.pose); p.update(values)
        if not all(math.isfinite(v) and BOUNDS[k][0]<=v<=BOUNDS[k][1] for k,v in p.items()): raise ValueError('manual invalid')
        self.pose=p; self.mode='manual'; self.t=0.
    def advance(self,dt):
        if type(dt) not in (int,float) or not math.isfinite(dt) or dt<0: raise ValueError('delta')
        if self.mode=='manual': return
        self.t+=dt
        if self.mode=='playing':
            self.pose=playing(self.profile,self.t,self.source)
            if self.t>=self.profile['duration']: self.pose=neutral(); self.mode='manual'
        else:
            self.pose=release_pose(self.source,self.t)
            if self.t>=.45: self.pose=neutral(); self.mode='manual'

def numerical_distance(a,b):
    # Stable ordered accumulation. NEVER iterate a set while reducing floats.
    channels=tuple(sorted(set(CHANNELS)|{k for p in (a,b) for f in p['keyframes'] for k in f['values']}))
    deltas=[playing(a,a['duration']*i/120).get(k,0)-playing(b,b['duration']*i/120).get(k,0)
            for i in range(121) for k in channels]
    return {'rms':math.sqrt(math.fsum(d*d for d in deltas)/len(deltas)), 'max_abs':max(map(abs,deltas)),
            'samples':121,'channels':len(channels),'perceptual_distinctness':'PENDING'}

def verify_freeze(root=W):
    freeze=load(root/'INPUT_FREEZE.json')
    for rel,expected in sorted(freeze['files'].items()):
        if sha(root/rel)!=expected: raise ValueError('Frozen input mismatch: '+rel)
    return len(freeze['files'])

def validate(root=W):
    checks=0
    def check(ok,label):
        nonlocal checks
        checks+=1
        if not ok: raise ValueError(label)
    frozen=verify_freeze(root)
    p=load(root/'EXP-091.json'); valid_definition(p)
    baseline=load(root/'BASELINE_FREEZE.json'); reg=load(root/'rig/expressions/registry.json')
    check(len(reg['entries'])==39,'approved39 count')
    check('EXP-091' not in [r['id'] for r in reg['entries']],'production registration changed')
    for name,digest in sorted(baseline['source_files_sha256'].items()): check(sha(root/'rig'/name)==digest,'baseline '+name)
    check(sha(root/'comparators/EXP-096.json')==baseline['headache_profile_sha256'],'Headache comparator changed')
    source=load(root/'SOURCE_MAP.json')
    for name,digest in sorted(source['input_files'].items()): check(sha(root/'reference'/name)==digest,'source '+name)
    records=[{'frame':i,'time':i/30,'pose':playing(p,i/30),'predicted_geometry':geometry(playing(p,i/30))} for i in range(121)]
    max_error=0.; max_step=0.
    for row in records:
        i=row['frame']; t=row['time']; pose=row['pose']
        check(in_scope(pose),'timeline scope '+str(i))
        expected=independent_sample(p,t)
        if t<.30: expected={k:v*(3*(t/.3)**2-2*(t/.3)**3) for k,v in expected.items()}
        for k in CHANNELS:
            error=abs(pose[k]-expected[k]); max_error=max(max_error,error)
            check(error<1e-12,'alternate timeline math')
            if i: max_step=max(max_step,abs(pose[k]-records[i-1]['pose'][k]))
        if t<=.2 or t>=3.75: check(pose==neutral(),'neutral holds')
        if t>=.9: check(pose['mouth_open']==0,'sealed after intake')
        check(all(q['gap']>=0 for q in row['predicted_geometry']['lip_samples']),'nonnegative lip gap')
    check(max_step<.20,'max frame step')
    peak=sample(p,1.65); g=geometry(peak)
    check(peak==sample(p,2.25),'sustained KP5-6 peak')
    check(g['eye_effective_closure']==g['eye_curved_shape']==1,'closed curved smile-eyes')
    check(peak['blink_L']==peak['blink_R']==0,'not headache ordinary closure')
    check(peak['blush_intensity']==.92 and peak['mouth_lip_press']==.70,'blush and pressed peak')
    check(abs(g['mouth_width_source_px']-49.16)<1e-12,'purse width prediction')
    check(all(x['gap']==0 for x in g['lip_samples']),'sealed peak')
    check(abs(g['lip_samples'][0]['upper_y']-g['lip_samples'][1]['upper_y']+.84)<1e-12,'small smile corner prediction')
    check(g['brow_angle_degrees']=={'screen_left':-8.,'screen_right':8.},'rigid raised-inner-brow strain')
    check(geometry(sample(p,2.75))['eye_effective_closure']<.5,'KP7 reopened with residual tension')
    dense=0
    for a,b in zip(p['keyframes'],p['keyframes'][1:]):
        for fraction in (0,1e-9,.001,.01,.1,.25,.5,.75,.9,.99,.999,1-1e-9,1):
            q=sample(p,a['time']+(b['time']-a['time'])*fraction); dense+=1
            check(in_scope(q),'dense segment scope')
    life=[]
    for t in INTERRUPTIONS:
        source=playing(p,t)
        for stage,steps in [('restart',12),('release',16)]:
            player=Lifecycle(p);player.trigger();player.advance(t)
            player.trigger() if stage=='restart' else player.release()
            check(player.pose==source,'trigger continuity')
            for i in range(steps+1):
                if i: player.advance(1/30)
                elapsed=i/30
                target=sample(p,elapsed) if stage=='restart' else neutral()
                u=min(1,elapsed/(.3 if stage=='restart' else .45)); w=3*u*u-2*u*u*u
                expected={k:(1-w)*source[k]+w*target[k] for k in CHANNELS}
                check(in_scope(player.pose),'lifecycle scope')
                check(max(abs(player.pose[k]-expected[k]) for k in CHANNELS)<1e-12,'lifecycle alternate math')
                life.append({'interruption_time':t,'stage':stage,'step':i,'pose':dict(player.pose)})
            if stage=='release': check(player.pose==neutral(),'release neutral')
            player.reset(); check(player.pose==neutral(),'reset neutral')
    comparisons={}
    definitions={r['id']:load(root/'rig'/r['path'].removeprefix('res://')) for r in reg['entries']}
    definitions['EXP-096']=load(root/'comparators/EXP-096.json')
    for key in sorted(definitions):
        result=numerical_distance(p,definitions[key]); check(result['rms']>0,'numeric duplicate '+key);comparisons[key]=result
    return {'status':'PASS_STATIC_NUMERIC_ONLY','reconstruction':'NEW 20261111 r1; not restored old v2',
        'approval':'UNAPPROVED','checks':checks,'frozen_inputs_verified':frozen,
        'baseline_files_verified':len(baseline['source_files_sha256']),'baseline_profiles':39,
        'timeline_samples':121,'dense_segment_samples':dense,'lifecycle_samples':len(life),
        'maximum_independent_control_error':max_error,'maximum_30hz_step':max_step,
        'trajectory_sha256':hashlib.sha256(canonical(records)).hexdigest(),
        'lifecycle_sha256':hashlib.sha256(canonical(life)).hexdigest(),
        'peak_analytic_prediction':g,'numerical_comparisons':comparisons,
        'native_runtime':'NOT RUN','native_capture':'PENDING_BLOCKED','source_fidelity':'PENDING_NATIVE_REVIEW',
        'normal_speed_review':'PENDING','mp4':'PENDING','remote_publication':'NOT_ATTEMPTED'}

if __name__=='__main__':
    print(canonical(validate()).decode(),end='')

"""Read-only, pure-Python oracle for this candidate's restricted control subspace.

Mirrors shared smoothstep/restart/release arithmetic, NOT Godot execution or
shader/pixel validation. Broader scoped/width/opening bridge flows are excluded.
"""
from pathlib import Path
import ast
import copy
import hashlib
import json
import math
import re

W = Path(__file__).resolve().parent
CHANNELS = tuple(ast.literal_eval(re.search(r'const CHANNELS=(\[.*?\])',
    (W/'rig/expression_rig.gd').read_text()).group(1)))
ACTING = tuple(sorted(('brow_screen_left','brow_screen_right','brow_tilt_screen_left',
                      'brow_tilt_screen_right','blink_L','blink_R','mouth_lip_press','mouth_purse')))
DEFINITION_KEYS = {'id','title','duration','keyframes','status','intent',
                   'source_catalogue_sha256','timing_origin','scope','interpolation'}

def canonical(data):
    return json.dumps(data, sort_keys=True, indent=2, allow_nan=False) + '\n'

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def finite_number(value):
    return type(value) in (int,float) and math.isfinite(value)

def neutral():
    return {key:0.0 for key in CHANNELS}

def smooth(u):
    u=max(0.0,min(1.0,u))
    return u*u*(3.0-2.0*u)

def blend(a,b,u):
    return {key:float(a.get(key,0.0))+(float(b.get(key,0.0))-float(a.get(key,0.0)))*u for key in CHANNELS}

def validate_profile(p, expected_id='EXP-092'):
    if not isinstance(p,dict) or set(p)-DEFINITION_KEYS: raise ValueError('Unknown profile fields')
    if p.get('id') != expected_id: raise ValueError('Wrong expression ID')
    if not isinstance(p.get('title'),str) or not p['title']: raise ValueError('Title required')
    for k in sorted(set(p)-{'duration','keyframes'}):
        if not isinstance(p[k],str): raise ValueError('String metadata required')
    if not finite_number(p.get('duration')) or p['duration']<=0: raise ValueError('Duration invalid')
    keys=p.get('keyframes')
    if not isinstance(keys,list) or len(keys)<2: raise ValueError('Keyframes missing')
    previous=-1.0
    for row in keys:
        if not isinstance(row,dict) or set(row)!={'time','phase','values'}: raise ValueError('Frame schema')
        t=row['time']
        if not finite_number(t) or t<=previous or not 0<=t<=p['duration']: raise ValueError('Timeline invalid')
        previous=t
        if not isinstance(row['phase'],str) or not row['phase']: raise ValueError('Phase required')
        if not isinstance(row['values'],dict): raise ValueError('Controls required')
        for k,v in sorted(row['values'].items()):
            if k not in ACTING: raise ValueError('Outside restricted Sour/Headache subspace')
            lo=-1.0 if k.startswith('brow_') else 0.0
            if not finite_number(v) or not lo<=v<=1.0: raise ValueError('Nonfinite or unbounded control')
        if row['values'].get('blink_L',0)!=row['values'].get('blink_R',0): raise ValueError('Asymmetric lids')
        if row['values'].get('brow_screen_left',0)!=row['values'].get('brow_screen_right',0): raise ValueError('Asymmetric brow height')
        if row['values'].get('brow_tilt_screen_left',0)!=-row['values'].get('brow_tilt_screen_right',0): raise ValueError('Brow opposition lost')
    if keys[0]['time']!=0 or keys[-1]['time']!=p['duration']: raise ValueError('Timeline endpoints')
    if any(v!=0 for row in (keys[0],keys[-1]) for v in row['values'].values()): raise ValueError('Nonneutral endpoint')
    return True

def sample(p,t):
    if not finite_number(t): raise ValueError('Nonfinite time')
    if t<=0 or t>=p['duration']: return neutral()
    for a,b in zip(p['keyframes'],p['keyframes'][1:]):
        if a['time']<=t<=b['time']:
            return blend(a['values'],b['values'],smooth((t-a['time'])/(b['time']-a['time'])))
    raise ValueError('Uncovered timeline')

def geometry(p):
    """Formula coordinates, not actual nodes/shader output or visible pixels."""
    purse=p['mouth_purse']
    return {
        'mouth_contour_width_source_px':71.0-28.0*purse,
        'central_contour_drop_source_px':4.0*purse,
        'endpoint_contour_drop_source_px':12.0*purse,
        'central_aperture_source_px':0.0,
        'brow_down_source_px':[-10.0*p['brow_screen_left'],-10.0*p['brow_screen_right']],
        'brow_rotations_degrees':[8.0*p['brow_tilt_screen_left'],8.0*p['brow_tilt_screen_right']],
        'ordinary_lash_travel_source_px':[36.0*p['blink_R'],36.0*p['blink_L']],
    }

def playback_from_neutral(p,t):
    """Includes the real player's 0.30 s restart envelope on initial trigger."""
    target=sample(p,t)
    return blend(neutral(),target,smooth(t/.30)) if 0<t<.30 else target

class RestrictedLifecycle:
    """Numeric model only. Does not pretend to test the actual rig controller."""
    def __init__(self,p):
        validate_profile(p)
        self.profile=copy.deepcopy(p)
        self.pose=neutral(); self.mode='manual'; self.t=0.0
        self.restart=neutral(); self.release_pose=neutral()
        self.auto_blink=False; self.pending=False

    def trigger(self):
        self.restart=self.pose.copy(); self.mode='performance'; self.t=0.0
        self.pending=self.pending or self.auto_blink; self.auto_blink=False

    def release(self):
        self.release_pose=self.pose.copy(); self.mode='release'; self.t=0.0
        self.pending=self.pending or self.auto_blink; self.auto_blink=False

    def reset(self):
        self.pose=neutral(); self.mode='manual'; self.t=0.0
        self.restart=neutral(); self.release_pose=neutral()
        self.auto_blink=False; self.pending=False

    def manual(self,controls):
        for key,value in sorted(controls.items()):
            if key not in ACTING or not finite_number(value): raise ValueError('Invalid manual control')
            if not (-1 if key.startswith('brow_') else 0)<=value<=1: raise ValueError('Manual range')
        self.pose.update({key:float(value) for key,value in controls.items()})
        self.mode='manual'; self.pending=False

    def advance(self,delta):
        if not finite_number(delta) or delta<0: raise ValueError('Invalid delta')
        if self.mode=='performance':
            self.t=min(self.profile['duration'],self.t+delta)
            self.pose=sample(self.profile,self.t)
            if self.t<.30: self.pose=blend(self.restart,self.pose,smooth(self.t/.30))
            if self.t>=self.profile['duration']: self.finish()
        elif self.mode=='release':
            self.t+=delta
            self.pose=blend(self.release_pose,neutral(),smooth(self.t/.45))
            if self.t>=.45: self.finish()

    def finish(self):
        self.pose=neutral(); self.mode='manual'
        if self.pending: self.pending=False; self.auto_blink=True

def rounded(value):
    if isinstance(value,float): return round(value,12)
    if isinstance(value,dict): return {k:rounded(v) for k,v in sorted(value.items())}
    if isinstance(value,list): return [rounded(v) for v in value]
    return value

def build_receipts(w=W):
    p=json.loads((w/'EXP-092.json').read_text())
    headache=json.loads((w/'comparators/EXP-096.json').read_text())
    validate_profile(p); validate_profile(headache,'EXP-096')
    frames=[{'frame':i,'time':i/30.0,'pose':playback_from_neutral(p,i/30.0),'formula_geometry':geometry(playback_from_neutral(p,i/30.0))} for i in range(121)]
    # All reductions use explicit ordering. Never iterate a set for floating sums.
    differences={key:math.fsum(abs(playback_from_neutral(p,i/240.0)[key]-playback_from_neutral(headache,i/240.0)[key]) for i in range(961))/961 for key in sorted(ACTING)}
    rms=math.sqrt(math.fsum(differences[k]**2 for k in sorted(differences))/len(differences))
    trajectory={
        'status':'PASS_NUMERIC_ONLY','approval':'UNAPPROVED','native_execution':False,
        'profile_sha256':sha(w/'EXP-092.json'),'headache_profile_sha256':sha(w/'comparators/EXP-096.json'),
        'sampling':'Pure Python mirror of restricted shared smoothstep and initial 0.30-second restart envelope, not Godot or pixel evidence',
        'fps':30,'duration':4.0,'frame_count':121,'dense_sample_count':961,
        'records':frames,
        'max_adjacent_30fps_step':{k:max(abs(frames[i]['pose'][k]-frames[i-1]['pose'][k]) for i in range(1,121)) for k in sorted(ACTING)},
        'headache_mean_absolute_control_difference':differences,
        'headache_rms_of_mean_absolute_control_difference':rms,
        'peak_purse_difference':.85,'peak_formula_width_contraction_source_px':23.8,
        'native_distinctness_from_096_and_091':'NOT RUN; required independently of numeric separation',
    }
    lifecycles=[]
    for interruption in [.35,.6,1.0,1.3,1.6,2.0,2.4,2.8,3.2,3.7]:
        for event in ['retrigger','release','reset','manual_takeover','release_then_retrigger']:
            player=RestrictedLifecycle(p); player.auto_blink=True; player.trigger(); player.advance(interruption)
            before=player.pose.copy()
            if event=='retrigger': player.trigger()
            elif event=='release': player.release()
            elif event=='reset': player.reset()
            elif event=='manual_takeover': player.manual({'mouth_purse':.2})
            else: player.release(); player.advance(.15); before=player.pose.copy(); player.trigger()
            after=player.pose.copy()
            continuity=(before==after) if event in ['retrigger','release','release_then_retrigger'] else None
            samples=[]
            for i in range(16):
                player.advance(1/30)
                samples.append({'step':i+1,'pose':player.pose.copy(),'auto_blink':player.auto_blink,'pending_restore':player.pending})
            player.advance(4.0)
            lifecycles.append({'interruption_time':interruption,'event':event,'continuous_on_trigger':continuity,
                'immediate_pose':after,'samples':samples,'final_pose':player.pose.copy(),
                'final_auto_blink':player.auto_blink,'final_pending_restore':player.pending})
    lifecycle={'status':'PASS_NUMERIC_MODEL_ONLY','native_execution':False,
        'scope':'Sour self-retrigger, release, reset, manual takeover, release-to-retrigger and auto-blink bookkeeping in a restricted pure-Python model. Not native lifecycle coverage or cross-profile handoff validation.',
        'scenarios':lifecycles,'scenario_count':len(lifecycles),'sample_count':len(lifecycles)*16}
    return rounded(trajectory),rounded(lifecycle)

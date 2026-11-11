"""Numerical mirror of the pinned shared sampler, same-candidate retrigger and release.
Not an engine, renderer, image generator, runtime parity test or perceptual review.
"""
import hashlib
import json
import math
import re
from pathlib import Path
W=Path(__file__).resolve().parent
PROFILE=json.loads((W/'EXP-046.json').read_text())
SOURCE=(W/'rig/expression_registry.gd').read_text()
BOUNDS=json.loads(re.search(r'const CHANNEL_BOUNDS=(\{[^\n]+\})',SOURCE).group(1).replace('Limits.GAZE_MIN','-1.0').replace('Limits.GAZE_MAX','1.0'))
CHANNELS=list(BOUNDS)
ACTING={'brow_inner_lift_screen_left','brow_inner_lift_screen_right','brow_screen_left','brow_screen_right','blink_L','blink_R','gaze_y','mouth_open','mouth_purse'}
INTERRUPTIONS=[.35,.7,1.15,1.5,1.85,2.25,2.7,3.15,3.7,4.5]
FPS=30
FRAMES=145

def finite(v):return type(v) in (int,float) and math.isfinite(v)
def neutral():return dict.fromkeys(CHANNELS,0.)
def smooth(u):
    u=max(0.,min(1.,u));return u*u*(3.-2.*u)
def blend(a,b,u):return {k:a.get(k,0.)+(b.get(k,0.)-a.get(k,0.))*u for k in CHANNELS}
def valid_pose(p):
    if set(p)-set(CHANNELS):return False
    if any(not finite(v) or not BOUNDS[k][0]<=v<=BOUNDS[k][1] for k,v in p.items()):return False
    v=lambda k:p.get(k,0.)
    if v('mouth_open')>0 and any(v(k)>0 for k in ['mouth_width_screen_left','mouth_width_screen_right','mouth_kiss']):return False
    if v('opening_px')>0 and any(v(k)!=0 for k in ['blink_L','blink_R','gaze_x','gaze_y','gaze_down_extra','eye_smile_L','eye_smile_R','aversion_px']):return False
    if v('aversion_px')>0 and (min(v('blink_L'),v('blink_R'))<.18 or any(v(k)!=0 for k in ['gaze_x','gaze_y','gaze_down_extra','eye_smile_L','eye_smile_R'])):return False
    if v('uneasy_weight')>0 and (v('mouth_open')>0 or v('mouth_kiss')>0):return False
    return True

def validate_profile(p):
    allowed={'id','title','duration','keyframes','status','intent','source_catalogue_sha256','timing_origin','scope','interpolation'}
    assert not set(p)-allowed
    assert p['id']=='EXP-046' and finite(p['duration']) and p['duration']==4.8
    assert isinstance(p['title'],str) and p['title']
    last=-1
    for row in p['keyframes']:
        assert set(row)=={'time','phase','values'}
        assert finite(row['time']) and last<row['time']<=p['duration']
        assert isinstance(row['phase'],str) and row['phase']
        assert valid_pose(row['values']) and not set(row['values'])-ACTING
        last=row['time']
    assert p['keyframes'][0]['time']==0 and last==p['duration']
    assert all(v==0 for row in [p['keyframes'][0],p['keyframes'][-1]] for v in row['values'].values())
    return True

def sample(t,profile=PROFILE):
    if not finite(t):raise ValueError('Finite sample time required')
    if t<=0 or t>=profile['duration']:return neutral()
    for a,b in zip(profile['keyframes'],profile['keyframes'][1:]):
        if a['time']<=t<=b['time']:
            return blend(a['values'],b['values'],smooth((t-a['time'])/(b['time']-a['time'])))
    return neutral()

class Player:
    """Candidate-only control-coordinate lifecycle; no cross-expression/scoped bridge claims."""
    def __init__(self):self.reset()
    def reset(self):
        self.pose=neutral();self.time=0.;self.release_time=-1.;self.active=False;self.origin=neutral()
    def play(self):
        self.origin=self.pose.copy();self.time=0.;self.release_time=-1.;self.active=True
    def release(self):
        self.origin=self.pose.copy();self.active=False;self.release_time=0.
    def advance(self,delta):
        if not finite(delta) or delta<0:raise ValueError('Nonnegative finite delta required')
        if self.active:
            self.time=min(PROFILE['duration'],self.time+delta)
            self.pose=sample(self.time)
            if self.time<.30:self.pose=blend(self.origin,self.pose,smooth(self.time/.30))
            if self.time>=PROFILE['duration']:self.active=False;self.pose=neutral()
        elif self.release_time>=0:
            self.release_time+=delta
            self.pose=blend(self.origin,neutral(),smooth(self.release_time/.45))
            if self.release_time>=.45:self.release_time=-1.;self.pose=neutral()
        return self.pose.copy()

def rotate(v,angle):
    c,s=math.cos(angle),math.sin(angle);return (v[0]*c-v[1]*s,v[0]*s+v[1]*c)
def geometry(p):
    result={'gaze_source_px':[4*p['gaze_x'],p['gaze_y']*(2 if p['gaze_y']<0 else 1)+5*p['gaze_down_extra']], 'lash_source_px':{'screen_left':36*p['blink_R'],'screen_right':36*p['blink_L']},'central_gap_source_px':max(0,p['mouth_open']*.55*54-1.5*p['mouth_purse']*min(4*p['mouth_open'],1)),'brows':{}}
    manifest=json.loads((W/'rig/rig_assets/object_face/manifest.json').read_text())
    anchors={'screen_left':(466.550,452.350),'screen_right':(646.227,453.773)}
    for side,sign in [('screen_left',-1),('screen_right',1)]:
        pivot=manifest['objects']['brow_'+side]['pivot'];anchor=anchors[side]
        a=(anchor[0]-pivot[0],anchor[1]-pivot[1]);theta=math.radians(26*sign*p['brow_inner_lift_'+side]);legacy=math.radians(8*p['brow_tilt_'+side])
        rotated=rotate(a,theta);offset=rotate((a[0]-rotated[0],a[1]-rotated[1]),legacy)
        result['brows'][side]={'pivot_delta_source_px':[offset[0],offset[1]-10*p['brow_'+side]],'angle_degrees':math.degrees(legacy+theta)}
    return result

def expected_frames():
    player=Player();player.play();rows=[]
    for i in range(FRAMES):
        if i:player.advance(max(0,i/FPS-player.time))
        rows.append({'frame':i,'time':i/FPS,'pose':player.pose.copy(),'geometry_model':geometry(player.pose)})
    return rows

def write_expected():
    data={'scope':'PURE PYTHON NUMERICAL EXPECTATIONS, NOT NATIVE EVIDENCE','profile_sha256':hashlib.sha256((W/'EXP-046.json').read_bytes()).hexdigest(),'fps':FPS,'frames':FRAMES,'duration':PROFILE['duration'],'records':expected_frames()}
    (W/'EXPECTED_TRAJECTORY.json').write_text(json.dumps(data,indent=2)+'\n')
if __name__=='__main__':
    validate_profile(PROFILE);write_expected();print('Wrote 145 numerical expectations only; no capture or engine execution.')

"""Explicit Python numerical model of the unchanged GDScript timeline controller.

This is NOT engine execution, scene validation, native rendering, or pacing evidence.
Its source contract is pinned by verify_approved_integration.py. Only authored
pose/lifecycle mathematics is modeled; rendering setters and geometry are not.
"""
import ast,copy,json,math,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
source=(R/'expression_rig.gd').read_text()
def constant(name):return ast.literal_eval(re.search(r'^const '+name+r'=(.+)$',source,re.M)[1])
CHANNELS=constant('CHANNELS');SCOPED=constant('SCOPED_CHANNELS');TRIO=constant('MOUTH_TRIO');CONFLICTS=constant('OPENING_CONFLICTS')
bounds=re.search(r'^const CHANNEL_BOUNDS=(.+)$',(R/'expression_registry.gd').read_text(),re.M)[1]
BOUNDS=json.loads(bounds.replace('Limits.GAZE_MIN','-1.0').replace('Limits.GAZE_MAX','1.0'))
RESTART=constant('RESTART_SECONDS');RELEASE=constant('RELEASE_SECONDS')
def neutral():return dict.fromkeys(CHANNELS,0.0)
def smooth(a,b,t):u=max(0.0,min(1.0,(t-a)/(b-a)));return u*u*(3-2*u)
def mix(a,b,w):return a+(b-a)*w
def sample(d,t):
 p=neutral()
 if t<=0 or t>=d['duration']:return p
 for a,b in zip(d['keyframes'],d['keyframes'][1:]):
  if a['time']<=t<=b['time']:
   u=smooth(a['time'],b['time'],t)
   return {k:mix(float(a['values'].get(k,0)),float(b['values'].get(k,0)),u) for k in CHANNELS}
 return p
def width(p):return any(p.get(k,0)>0 for k in TRIO[1:])
def has_scoped(p):return any(p.get(k,0)>0 for k in SCOPED)
def scoped_valid(p):
 if p.get('opening_px',0)>0 and any(p.get(k,0)!=0 for k in CONFLICTS):return False
 if p.get('aversion_px',0)>0:
  if min(p.get('blink_L',0),p.get('blink_R',0))<.18:return False
  if any(p.get(k,0)!=0 for k in ['gaze_x','gaze_y','gaze_down_extra','eye_smile_L','eye_smile_R']):return False
 return not (p.get('uneasy_weight',0)>0 and (p.get('mouth_kiss',0)>0 or p.get('mouth_open',0)>0))
def mouth_valid(p):return not(p.get('mouth_open',0)>0 and width(p))
def scoped_handoff(s,t,u):
 p=s.copy()
 if u<.5:
  w=1-smooth(0,.5,u)
  for k in SCOPED:p[k]=s.get(k,0)*w
 else:
  w=smooth(.5,1,u);p={k:mix(s.get(k,0),t.get(k,0),w) for k in CHANNELS}
  for k in SCOPED:p[k]=t.get(k,0)*w
 return p
class Model:
 def __init__(self,definitions):self.definitions=definitions;self.reset()
 def reset(self):
  self.pose=neutral();self.active='';self.time=0.;self.release_time=-1.;self.restart=neutral();self.release_pose=neutral();self.performance={};self.mode='none';self.bridge_duration=0.;self.opening_bridge=False;self.auto_blink=False;self.pending=False
 def play(self,id):
  if id not in self.definitions:return False
  self.restart=self.pose.copy();self.active=id;self.performance=copy.deepcopy(self.definitions[id]);self.time=0.;self.release_time=-1.;self.pending=self.pending or self.auto_blink;self.auto_blink=False
  sw=width(self.restart);tw=any(width(f['values']) for f in self.performance['keyframes']);to=any(f['values'].get('mouth_open',0)>0 for f in self.performance['keyframes'])
  self.mode='legacy'
  if sw or tw:self.mode='staged' if (sw and to) or (self.restart['mouth_open']>0 and tw) else 'bounded_direct'
  self.bridge_duration=RESTART if self.mode=='legacy' else min(RESTART,self.performance['duration'])
  self.opening_bridge=any(self.restart[k]!=0 for k in CONFLICTS) and (sample(self.performance,RESTART)['opening_px']>0 or any(0<f['time']<RESTART and f['values'].get('opening_px',0)>0 for f in self.performance['keyframes']))
  return True
 def release(self):
  self.release_pose=self.pose.copy();self.active='';self.release_time=0.;self.pending=self.pending or self.auto_blink;self.auto_blink=False;self.mode='none';self.opening_bridge=False
 def restore(self):
  if self.pending and not self.active and self.release_time<0 and self.pose==neutral():self.pending=False;self.auto_blink=True
 def manual_takeover(self):
  # Test the documented ownership effect only, not the full manual-control API.
  self.active='';self.release_time=-1.;self.pending=False;self.mode='none';self.opening_bridge=False
  for k in SCOPED:self.pose[k]=0.
 def advance(self,delta):
  if type(delta) not in (int,float) or not math.isfinite(delta) or delta<0:return False
  if self.active:
   self.time=min(self.performance['duration'],self.time+delta);t=sample(self.performance,self.time);p=t.copy()
   if self.time<RESTART:p={k:mix(self.restart[k],p[k],smooth(0,RESTART,self.time)) for k in CHANNELS}
   if has_scoped(self.restart) and self.time<RESTART:p=scoped_handoff(self.restart,t,self.time/RESTART)
   if self.opening_bridge and self.time<RESTART:
    u=self.time/RESTART;p['opening_px']=0.;p['aversion_px']=self.restart['aversion_px']*(1-smooth(0,1/3,u))
    for k in CONFLICTS:
     if k!='aversion_px':p[k]=self.restart[k]*(1-smooth(1/3,2/3,u))
    if u>=2/3:
     w=smooth(2/3,1,u);p['opening_px']=t['opening_px']*w
     for k in CONFLICTS:p[k]=t[k]*w
   if self.mode not in ('none','legacy'):
    if self.time>=self.bridge_duration:
     for k in TRIO:p[k]=t[k]
    else:
     u=self.time/self.bridge_duration
     if self.mode=='bounded_direct':
      for k in TRIO:p[k]=mix(self.restart[k],t[k],smooth(0,1,u))
     elif u<=.5:
      for k in TRIO:p[k]=self.restart[k]*(1-smooth(0,.5,u))
     else:
      for k in TRIO:p[k]=t[k]*smooth(.5,1,u)
   self.pose=p
   if self.time>=self.performance['duration']:self.active='';self.mode='none';self.opening_bridge=False;self.pose=neutral();self.restore()
  elif self.release_time>=0:
   self.release_time+=delta;self.pose={k:mix(self.release_pose[k],0,smooth(0,RELEASE,self.release_time)) for k in CHANNELS}
   if has_scoped(self.release_pose):self.pose=scoped_handoff(self.release_pose,neutral(),self.release_time/RELEASE)
   if self.release_time>=RELEASE:self.release_time=-1.;self.pose=neutral();self.restore()
  return True

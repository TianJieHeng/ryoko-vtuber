"""Run the five-state gate on an existing imported approved24 rig."""
import argparse, os, subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--rig',type=Path,required=True);p.add_argument('--capture',action='store_true');p.add_argument('--godot',default='godot');a=p.parse_args()
w=Path(__file__).resolve().parent
if a.capture and (w/'capture').exists():raise SystemExit('Inspect the existing capture before another run.')
env=os.environ.copy();env['LP_NUM_THREADS']='2'
for k,d in [('HOME','home'),('XDG_CACHE_HOME','cache'),('XDG_CONFIG_HOME','config'),('XDG_DATA_HOME','data')]:
 q=w/'local_environment'/d;q.mkdir(parents=True,exist_ok=True);env[k]=str(q)
cmd=[a.godot,*(['--rendering-method','gl_compatibility','--audio-driver','Dummy'] if a.capture else ['--headless']),'--path',str(a.rig.resolve()),'--script',str(w/'check_and_capture.gd')]
if a.capture:cmd+=['--','--capture']
with (w/('capture.log' if a.capture else 'state.log')).open('w') as log:
 result=subprocess.run(cmd,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=120)
raise SystemExit(result.returncode)

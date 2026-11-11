"""Validate native evidence before encoding. No renderer, editor or launcher calls.
Default/preflight never invokes any subprocess. Missing capture must be a hard failure.
"""
import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path
from PIL import Image
from freeze_candidate import verify, sha
from trajectory_model import INTERRUPTIONS, neutral
W=Path(__file__).resolve().parent
SIZES={'full':(568,800),'detail':(400,360)}
def require(condition,message):
    if not condition:raise ValueError(message)
def load(path):return json.loads(path.read_text())
def pose_equal(actual,expected):
    return isinstance(actual,dict) and set(actual)==set(neutral()) and all(type(actual[k]) in (int,float) and math.isfinite(actual[k]) and abs(actual[k]-expected.get(k,0))<1e-5 for k in actual)
def validate_metadata(receipt,w=W):
    require(receipt.get('status')=='PASS' and receipt.get('failures')==[] and receipt.get('visual_capture') is True,'Native capture did not pass.')
    require(type(receipt.get('checks')) is int and receipt['checks']>0,'No native checks reported.')
    require(receipt.get('display') not in (None,'','headless') and isinstance(receipt.get('renderer'),str) and receipt['renderer'].strip(),'Native rendered capture required, not headless state checks.')
    for key,path in [('profile_sha256','EXP-046.json'),('freeze_sha256','CANDIDATE_FREEZE.json'),('expected_sha256','EXPECTED_TRAJECTORY.json')]:
        require(receipt.get(key)==sha(w/path),'Receipt input identity mismatch: '+key)
    require(receipt.get('baseline_profile_count')==39 and receipt.get('production_registry_unchanged') is True,'Wrong or altered baseline.')
    require((receipt.get('frames'),receipt.get('fps'),receipt.get('duration'))==(145,30,4.8),'Expected 145 samples at 30 Hz through t=4.8.')
    require(receipt.get('approval')=='UNAPPROVED','Encoding must not imply approval.')
    expected=load(w/'EXPECTED_TRAJECTORY.json')['records'];records=receipt.get('records',[])
    require(len(records)==145,'Missing or extra motion records.')
    for i,(row,want) in enumerate(zip(records,expected)):
        require(row.get('frame')==i and type(row.get('time')) in (int,float) and abs(row['time']-i/30)<1e-10,'Wrong frame order or time.')
        require(pose_equal(row.get('pose'),want['pose']),'Motion pose mismatch at '+str(i))
        require(isinstance(row.get('hashes'),list) and len(row['hashes'])==2 and all(isinstance(h,str) and len(h)==64 and all(c in '0123456789abcdef' for c in h) for h in row['hashes']),'Bad RGBA hash receipt.')
    require(records[0]['hashes']==records[-1]['hashes'],'Neutral endpoint pixels differ.')
    plans=load(w/'plan.json');static=receipt.get('static_records',[])
    require(len(static)==len(plans),'Missing static anchors.')
    for got,want in zip(static,plans):
        require(got.get('name')==want['name'] and pose_equal(got.get('pose'),want['pose']),'Wrong static anchor name/pose.')
        require(isinstance(got.get('hashes'),list) and len(got['hashes'])==2,'Missing static hashes.')
    lifecycle=receipt.get('lifecycle_records',[])
    require([r.get('interruption_time') for r in lifecycle]==INTERRUPTIONS,'Incomplete native lifecycle coverage.')
    require(all(r.get('retrigger_steps')==145 and r.get('release_steps')==16 and r.get('reset_checked') is True for r in lifecycle),'Incomplete lifecycle stages.')
    return receipt

def check_image(path,size,digest):
    with Image.open(path) as im:
        require(im.mode=='RGBA' and im.size==size,'Wrong native image mode/size: '+str(path))
        require(hashlib.sha256(im.tobytes()).hexdigest()==digest,'Raw native RGBA identity mismatch: '+str(path))
def validate_capture(w=W):
    verify(w)
    path=w/'native_capture/checks.json'
    require(path.is_file(),'Native capture NOT RUN. No MP4 may be encoded from numerical data or reference panels.')
    receipt=validate_metadata(load(path),w)
    for j,(view,size) in enumerate(SIZES.items()):
        directory=w/'native_capture'/view
        require({p.name for p in directory.iterdir()}=={f'{i:04d}.png' for i in range(145)},'Incomplete or extra native '+view+' frame set.')
        for row in receipt['records']:check_image(directory/f'{row["frame"]:04d}.png',size,row['hashes'][j])
    directory=w/'native_capture/static'
    require({p.name for p in directory.iterdir()}=={f'{r["name"]}_{view}.png' for r in receipt['static_records'] for view in SIZES},'Incomplete or extra static frame set.')
    for row in receipt['static_records']:
        for j,(view,size) in enumerate(SIZES.items()):check_image(directory/f'{row["name"]}_{view}.png',size,row['hashes'][j])
    return receipt

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--encode',action='store_true');parser.add_argument('--preflight',action='store_true');args=parser.parse_args()
    validate_capture()
    if not args.encode:
        print('Native input evidence passed; encoder was not invoked.');return
    clearance=load(W/'LAUNCH_CLEARANCE.json')
    require(clearance.get('cleared') is True and clearance.get('state')=='CLEARED_FOR_THIS_NATIVE_CAPTURE','Outstanding launch restriction has not been resolved; no encode.')
    out=W/'Exasperated_sigh_rebuild_v1_UNAPPROVED.mp4'
    require(not out.exists(),'Preserving existing MP4; refusing overwrite.')
    filter_text='[1:v]pad=400:800:0:220:color=0x202224,drawtext=text=Exasperated sigh:fontcolor=white:fontsize=22:x=(w-tw)/2:y=130,drawtext=text=UNAPPROVED new candidate:fontcolor=white:fontsize=16:x=(w-tw)/2:y=165,drawtext=text=Bounded upward glance only:fontcolor=white:fontsize=14:x=(w-tw)/2:y=190[d];[0:v][d]hstack=inputs=2[v]'
    command=['ffmpeg','-hide_banner','-nostdin','-n','-framerate','30','-i',str(W/'native_capture/full/%04d.png'),'-framerate','30','-i',str(W/'native_capture/detail/%04d.png'),'-filter_complex',filter_text,'-map','[v]','-frames:v','145','-c:v','libx264','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart',str(out)]
    with (W/'encode.log').open('x') as log:subprocess.run(command,check=True,stdout=log,stderr=subprocess.STDOUT)
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_name,width,height,pix_fmt,r_frame_rate,nb_frames:format=duration,size','-of','json',str(out)]))
    s=probe['streams'][0];require((s['width'],s['height'],s['nb_frames'],s['r_frame_rate'],s['pix_fmt'])==(968,800,'145','30/1','yuv420p'),'Encoded output dimensions/count/rate mismatch.')
    require(abs(float(probe['format']['duration'])-145/30)<.002,'Encoded duration mismatch.')
    subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True)
    (W/'ENCODE_RESULT.json').write_text(json.dumps({'status':'PASS','approval':'UNAPPROVED','profile_sha256':sha(W/'EXP-046.json'),'native_receipt_sha256':sha(W/'native_capture/checks.json'),'mp4_sha256':sha(out),'probe':probe,'decoded_frame_visual_review':'PENDING','normal_speed_observed':False},indent=2)+'\n')
    print('Encoded UNAPPROVED preview; perceptual and decoded-frame review still required.')
if __name__=='__main__':
    try:main()
    except (ValueError,OSError,KeyError,TypeError) as error:raise SystemExit(str(error))

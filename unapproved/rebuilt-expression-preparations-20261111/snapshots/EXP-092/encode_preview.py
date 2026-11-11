"""Guarded native-frame encoder preparation. Default is read-only preflight.

No renderer is launched here. The current native gate is BLOCKED, so even an
explicit --encode stops before ffmpeg. This task never ran an encoder.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess

W=Path(__file__).resolve().parent
IDS=('EXP-092','EXP-096','EXP-091')
VIEWS=(('full',(568,800)),('detail',(400,360)))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
load=lambda p:json.loads(Path(p).read_text())

def require_native_gate(w):
    gate_path=w/'NATIVE_GATE.json'
    if not gate_path.is_file() or load(gate_path).get('allowed') is not True:
        raise ValueError('Native access is blocked; no capture or encode may be launched by this preparation.')

def validate_capture(w=W):
    require_native_gate(w)
    path=w/'native_capture/motion_checks.json'
    if not path.is_file(): raise ValueError('Fresh native capture is missing; no MP4 can be encoded.')
    freeze=load(w/'INPUT_FREEZE.json')
    for name,digest in sorted(freeze['files_sha256'].items()):
        if sha(w/name)!=digest: raise ValueError('Frozen source changed: '+name)
    result=load(path)
    if result.get('status')!='PASS' or result.get('failures')!=[] or result.get('visual_capture') is not True:
        raise ValueError('Capture must pass actual native checks.')
    if result.get('display') in (None,'','headless') or not result.get('renderer'):
        raise ValueError('State-only/headless receipts are not native rendering evidence.')
    if result.get('input_freeze_sha256')!=sha(w/'INPUT_FREEZE.json'):
        raise ValueError('Capture belongs to another input freeze.')
    if result.get('baseline_freeze_sha256')!=sha(w/'BASELINE_FREEZE.json'):
        raise ValueError('Capture belongs to another baseline freeze.')
    if (result.get('frames_per_profile'),result.get('fps'),result.get('duration'))!=(121,30,4.0):
        raise ValueError('Expected 121 chronological frames at 30 Hz per profile.')
    if set(result.get('records',{}))!=set(IDS) or set(result.get('profile_hashes',{}))!=set(IDS):
        raise ValueError('Both EXP-096 and fresh EXP-091 comparators are required.')
    from PIL import Image
    for id in IDS:
        profile=w/('EXP-092.json' if id=='EXP-092' else 'comparators/'+id+'.json')
        if result['profile_hashes'][id]!=sha(profile): raise ValueError('Profile hash mismatch: '+id)
        rows=result['records'][id]
        if len(rows)!=121: raise ValueError('Incomplete frame receipts: '+id)
        for view_index,(view,size) in enumerate(VIEWS):
            directory=w/'native_capture'/id/view
            if sorted(p.name for p in directory.glob('*.png'))!=[f'{i:04d}.png' for i in range(121)]:
                raise ValueError('Missing or extra native frames: '+id+'/'+view)
            for i,row in enumerate(rows):
                if row['frame']!=i or abs(row['time']-i/30)>1e-12: raise ValueError('Frame order/time mismatch')
                if len(row['hashes'])!=2: raise ValueError('Both native views required')
                with Image.open(directory/f'{i:04d}.png') as im:
                    if im.size!=size or im.mode!='RGBA': raise ValueError('Native RGBA dimensions differ')
                    if hashlib.sha256(im.tobytes()).hexdigest()!=row['hashes'][view_index]:
                        raise ValueError('Native pixel receipt mismatch')
            if rows[0]['hashes'][view_index]!=rows[-1]['hashes'][view_index]:
                raise ValueError('Neutral pixel endpoints differ')
    review_path=w/'native_capture/INDEPENDENT_VISUAL_REVIEW.json'
    if not review_path.is_file(): raise ValueError('Independent Sour-versus-096/091 native review is pending.')
    review=load(review_path)
    if review.get('capture_sha256')!=sha(path) or review.get('profile_sha256')!=sha(w/'EXP-092.json'):
        raise ValueError('Visual review belongs to another capture/profile')
    for field in ('source_fit','distinct_from_096','distinct_from_091','no_kiss_or_smile_eye','full_and_detail_inspected','chronological_frames_inspected'):
        if review.get(field) is not True: raise ValueError('Visual review incomplete: '+field)
    if not review.get('reviewer') or not review.get('observations'):
        raise ValueError('Independent review needs attributed observations, not numeric metrics alone')
    return result

def command(w=W):
    target=w/'Sour_taste_rebuild_UNAPPROVED.mp4'
    if target.exists(): raise ValueError('Existing MP4 preserved; refusing overwrite.')
    filters='[1:v]pad=400:800:0:220:color=0x202224[d];[0:v][d]hstack=inputs=2[v]'
    return ['ffmpeg','-hide_banner','-nostdin','-n','-framerate','30','-i',str(w/'native_capture/EXP-092/full/%04d.png'),
            '-framerate','30','-i',str(w/'native_capture/EXP-092/detail/%04d.png'),'-filter_complex',filters,
            '-map','[v]','-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart',str(target)]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--encode',action='store_true',help='Only for a later explicitly authorized native task')
    args=parser.parse_args()
    validate_capture()
    cmd=command()
    if not args.encode:
        print(json.dumps({'preflight':'PASS','encoded':False,'command':cmd},sort_keys=True))
        return
    target=Path(cmd[-1])
    with (W/'encode.log').open('x') as log:
        subprocess.run(cmd,check=True,stdout=log,stderr=subprocess.STDOUT)
    raw=subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_name,width,height,pix_fmt,r_frame_rate,nb_frames:format=duration,size','-of','json',str(target)])
    probe=json.loads(raw)
    stream=probe['streams'][0]
    if (stream['width'],stream['height'],stream['nb_frames'],stream['r_frame_rate'],stream['codec_name'],stream['pix_fmt'])!=(968,800,'121','30/1','h264','yuv420p'):
        raise ValueError('Encoded video does not satisfy review contract; preserve failed output separately.')
    if abs(float(probe['format']['duration'])-121/30)>.002: raise ValueError('Encoded duration differs')
    subprocess.run(['ffmpeg','-v','error','-i',str(target),'-f','null','-'],check=True)
    with (W/'VIDEO_PROBE.json').open('x') as f:
        json.dump({'probe':probe,'video_sha256':sha(target),'approval':'UNAPPROVED','normal_speed_observed':False},f,sort_keys=True,indent=2)

if __name__=='__main__':
    try: main()
    except (ValueError,FileNotFoundError,KeyError) as exc: raise SystemExit(str(exc))

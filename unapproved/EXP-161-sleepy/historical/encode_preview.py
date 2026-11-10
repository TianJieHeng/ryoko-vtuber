"""Encode already captured native frames only. Never invokes a renderer."""
import hashlib
import json
import subprocess
from pathlib import Path
from PIL import Image

W = Path(__file__).resolve().parent
SIZES = {'full': (568, 800), 'detail': (400, 360)}
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
load = lambda p: json.loads(p.read_text())

def validate_capture(w):
    if not (w / 'motion_checks.json').is_file() or not (w / 'capture/checks.json').is_file():
        raise ValueError('Native static and motion captures are pending. No preview can be encoded.')
    motion = load(w / 'motion_checks.json')
    static = load(w / 'capture/checks.json')
    for result in [static, motion]:
        if result['status'] != 'PASS' or result['failures'] or result['visual_capture'] is not True:
            raise ValueError('Native capture must pass before encoding.')
        if result['baseline_freeze_sha256'] != sha(w / 'BASELINE_FREEZE.json'):
            raise ValueError('Native receipt belongs to another baseline freeze.')
    if motion['display'] == 'headless' or not motion['renderer']:
        raise ValueError('Headless state checks are not native capture evidence.')
    if motion['profile_sha256'] != sha(w / 'EXP-161.json') or static['plan_sha256'] != sha(w / 'plan.json'):
        raise ValueError('Candidate changed after capture; preserve the evidence and recapture separately.')
    if motion['frames'] != 121 or motion['fps'] != 30 or motion['duration'] != 4.0:
        raise ValueError('Expected 121 frames at 30 Hz, ending exactly at 4 seconds.')
    if motion['baseline_profile_count'] != load(w / 'BASELINE_FREEZE.json')['baseline_profile_count']:
        raise ValueError('Incorrect baseline profile count.')
    if len(motion['records']) != 121:
        raise ValueError('Expected 121 frame receipts.')
    for view_index, (view, expected) in enumerate(SIZES.items()):
        directory = w / 'motion' / view
        if {p.name for p in directory.glob('*.png')} != {f'{i:04d}.png' for i in range(121)}:
            raise ValueError(f'{view}: incomplete or extra frame set.')
        for i, row in enumerate(motion['records']):
            if row['frame'] != i or abs(row['time'] - i/30) > 1e-12:
                raise ValueError(f'Frame receipt order/time differs at {i}.')
            with Image.open(directory / f'{i:04d}.png') as im:
                if im.size != expected or im.mode != 'RGBA':
                    raise ValueError(f'{view} {i}: native RGBA {expected} required, found {im.mode} {im.size}.')
                if hashlib.sha256(im.tobytes()).hexdigest() != row['hashes'][view_index]:
                    raise ValueError(f'{view} {i}: native pixel receipt does not match.')
        if motion['records'][0]['hashes'][view_index] != motion['records'][-1]['hashes'][view_index]:
            raise ValueError(f'{view}: neutral return pixels differ.')
    for row in load(w / 'plan.json'):
        for suffix, expected in [('bust', (568, 800)), ('detail', (400, 360))]:
            with Image.open(w / 'capture' / f'{row["name"]}_{suffix}.png') as im:
                if im.size != expected or im.mode != 'RGBA':
                    raise ValueError('Static capture has incorrect native dimensions or pixel mode.')
    return motion

def main():
    validate_capture(W)
    target = W / 'Sleepy_review_v1.mp4'
    if target.exists():
        raise ValueError('Existing video is preserved; refusing overwrite.')
    filters = '[1:v]pad=400:800:0:220:color=0x202224,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text=Sleepy:fontcolor=white:fontsize=22:x=(w-tw)/2:y=135,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text=Review candidate:fontcolor=0xbfc4ca:fontsize=16:x=(w-tw)/2:y=170[d];[0:v][d]hstack=inputs=2[v]'
    cmd = ['ffmpeg', '-hide_banner', '-nostdin', '-n', '-framerate', '30', '-i', str(W/'motion/full/%04d.png'), '-framerate', '30', '-i', str(W/'motion/detail/%04d.png'), '-filter_complex', filters, '-map', '[v]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(target)]
    with (W/'encode.log').open('w') as log:
        subprocess.run(cmd, check=True, stdout=log, stderr=subprocess.STDOUT)
    probe = subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_name,width,height,pix_fmt,r_frame_rate,nb_frames:format=duration,size', '-of', 'json', str(target)])
    (W/'video_probe.json').write_bytes(probe)
    p = json.loads(probe)
    stream = p['streams'][0]
    assert stream['width'] == 968 and stream['height'] == 800 and stream['nb_frames'] == '121'
    assert stream['r_frame_rate'] == '30/1' and abs(float(p['format']['duration']) - 121/30) < .002
    subprocess.run(['ffmpeg', '-v', 'error', '-i', str(target), '-f', 'null', '-'], check=True)
    print(probe.decode())

if __name__ == '__main__':
    try:
        main()
    except ValueError as e:
        raise SystemExit(str(e))

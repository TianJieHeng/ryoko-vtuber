"""Read-only preparation. Validate fresh native evidence; emit a command, never execute it."""
import binascii
import hashlib
import json
import struct
import zlib
from pathlib import Path
from numeric_model import W, load, sha, verify_freeze, playing, neutral, release_pose, INTERRUPTIONS
OUTPUT='Overly_sweet_taste_reconstruction_20261111_r1_review.mp4'

def read_rgba(path):
    """Decode only noninterlaced RGBA8 PNG with CRC checks; no rendering/editing."""
    data=path.read_bytes()
    if data[:8]!=b'\x89PNG\r\n\x1a\n':raise ValueError('PNG signature')
    pos=8;parts=[];size=None;ended=False
    while pos<len(data):
        n=struct.unpack('>I',data[pos:pos+4])[0];kind=data[pos+4:pos+8];body=data[pos+8:pos+8+n]
        if len(body)!=n or pos+12+n>len(data):raise ValueError('Truncated PNG')
        crc=struct.unpack('>I',data[pos+8+n:pos+12+n])[0]
        if binascii.crc32(kind+body)&0xffffffff!=crc:raise ValueError('PNG CRC')
        if kind==b'IHDR':
            if size is not None or n!=13:raise ValueError('PNG IHDR')
            width,height,depth,color,compression,filter_method,interlace=struct.unpack('>IIBBBBB',body)
            if (depth,color,compression,filter_method,interlace)!=(8,6,0,0,0):raise ValueError('Native RGBA8 PNG required')
            if (width,height) not in ((568,800),(400,360)):raise ValueError('Wrong native dimensions')
            size=(width,height)
        elif kind==b'IDAT':parts.append(body)
        elif kind==b'IEND':ended=True;pos+=12+n;break
        pos+=12+n
    if not ended or pos!=len(data) or size is None:raise ValueError('PNG structure')
    width,height=size;stride=width*4;raw=zlib.decompress(b''.join(parts))
    if len(raw)!=(stride+1)*height:raise ValueError('PNG scanlines')
    previous=bytearray(stride);out=bytearray()
    for y in range(height):
        kind=raw[y*(stride+1)];row=bytearray(raw[y*(stride+1)+1:(y+1)*(stride+1)])
        if kind not in range(5):raise ValueError('PNG filter')
        for x in range(stride):
            a=row[x-4] if x>=4 else 0;b=previous[x];c=previous[x-4] if x>=4 else 0
            p=a+b-c;pa,pb,pc=abs(p-a),abs(p-b),abs(p-c)
            predictor=(0,a,b,(a+b)//2,a if pa<=pb and pa<=pc else b if pb<=pc else c)[kind]
            row[x]=(row[x]+predictor)&255
        out.extend(row);previous=row
    return size,hashlib.sha256(out).hexdigest()

def validate_metadata(w,receipt):
    if receipt.get('status')!='PASS' or receipt.get('failures')!=[] or receipt.get('visual_capture') is not True:raise ValueError('Passing actual native capture required')
    if receipt.get('display') in (None,'','headless') or not receipt.get('renderer'):raise ValueError('Native display and renderer required')
    if receipt.get('input_freeze_sha256')!=sha(w/'INPUT_FREEZE.json') or receipt.get('profile_sha256')!=sha(w/'EXP-091.json'):raise ValueError('Stale native evidence')
    if [receipt.get(k) for k in ('frames','fps','duration','baseline_profile_count')]!=[121,30,4.0,39]:raise ValueError('Capture protocol differs')
    if len(receipt.get('records',[]))!=121 or len(receipt.get('static_records',[]))!=9 or len(receipt.get('lifecycle_records',[]))!=270:raise ValueError('Incomplete native evidence')
    profile=load(w/'EXP-091.json')
    def pose_matches(actual,expected):
        return set(actual)==set(expected) and all(type(actual[k]) in (float,int) and abs(actual[k]-expected[k])<1e-5 for k in expected)
    for i,row in enumerate(receipt['records']):
        if row.get('frame')!=i or row.get('time')!=i/30:raise ValueError('Frame order/time mismatch')
        if not pose_matches(row['pose'],playing(profile,i/30)):raise ValueError('Native trajectory mismatch')
    plan=load(w/'plan.json')
    for anchor,row in zip(plan,receipt['static_records']):
        expected=neutral();expected.update(anchor['pose'])
        if row['name']!=anchor['name'] or not pose_matches(row['pose'],expected):raise ValueError('Static anchor mismatch')
    expected_life=[(t,stage,step) for t in INTERRUPTIONS for stage,count in [('restart',13),('release',17)] for step in range(count)]
    for row,(t,stage,step) in zip(receipt['lifecycle_records'],expected_life):
        if (row.get('interruption_time'),row.get('stage'),row.get('step'))!=(t,stage,step):raise ValueError('Lifecycle order mismatch')
        source=playing(profile,t)
        expected=playing(profile,step/30,source) if stage=='restart' else release_pose(source,step/30)
        if not pose_matches(row['pose'],expected):raise ValueError('Lifecycle mismatch')
    return receipt

def validate_capture(w=W):
    verify_freeze(w)
    path=w/'capture/evidence.json'
    if not path.is_file():raise ValueError('PENDING_BLOCKED: fresh native captures absent. No encode is permitted.')
    receipt=validate_metadata(w,load(path));expected_paths=[]
    rows=[(row,f'{i:04d}') for i,row in enumerate(receipt['records'])]
    rows += [(row,'static/'+row['name']) for row in receipt['static_records']]
    for row,label in rows:
        if len(row.get('views',[]))!=2:raise ValueError('Two native views required')
        for index,(view,size) in enumerate((('full',(568,800)),('detail',(400,360)))):
            item=row['views'][index]
            rel=f'{label}_{view}.png' if label.startswith('static/') else f'{view}/{label}.png'
            if item.get('path')!=rel or (item.get('width'),item.get('height'))!=size:raise ValueError('View path/dimensions mismatch')
            file=w/'capture'/rel;expected_paths.append(rel)
            if sha(file)!=item.get('file_sha256'):raise ValueError('Frame file hash mismatch')
            actual_size,digest=read_rgba(file)
            if actual_size!=size or digest!=item.get('rgba_sha256'):raise ValueError('Frame RGBA hash mismatch')
    if sorted(str(p.relative_to(w/'capture')) for p in (w/'capture').rglob('*.png'))!=sorted(expected_paths):raise ValueError('Missing/extra PNGs')
    for i in range(2):
        if receipt['records'][0]['views'][i]['rgba_sha256']!=receipt['records'][-1]['views'][i]['rgba_sha256']:raise ValueError('Neutral pixels differ')
    return receipt

def prepare_command(w=W):
    validate_capture(w)
    if (w/OUTPUT).exists():raise ValueError('Existing video preserved; refusing overwrite')
    return ['ffmpeg','-hide_banner','-nostdin','-n','-framerate','30','-i',str(w/'capture/full/%04d.png'),
      '-framerate','30','-i',str(w/'capture/detail/%04d.png'),'-filter_complex',
      '[1:v]pad=400:800:0:220:color=0x202224[d];[0:v][d]hstack=inputs=2[v]',
      '-map','[v]','-frames:v','121','-c:v','libx264','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart',str(w/OUTPUT)]

if __name__=='__main__':
    try:print(json.dumps({'status':'PREPARED_ONLY_NOT_EXECUTED','command':prepare_command()},indent=2))
    except (ValueError,KeyError,OSError) as e:
        print(json.dumps({'status':'PENDING_BLOCKED','reason':str(e)}));raise SystemExit(2)

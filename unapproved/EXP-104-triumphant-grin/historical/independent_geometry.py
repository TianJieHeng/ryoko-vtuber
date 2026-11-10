"""Read-only independent source/geometry/timeline validation. No Godot or renderer."""
import hashlib
import json
import math
from pathlib import Path
from PIL import Image
W=Path(__file__).resolve().parent
ACTING=set(["brow_screen_left","brow_screen_right","brow_tilt_screen_left","brow_tilt_screen_right","blink_L","blink_R","mouth_smile","mouth_spread","mouth_open"])
load=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def close(a,b,eps=1e-5):
    return math.isfinite(a) and math.isfinite(b) and abs(a-b)<eps
def sample(keys,t,channels):
    for a,b in zip(keys,keys[1:]):
        if a['time']<=t<=b['time']:break
    x=min(1,max(0,(t-a['time'])/(b['time']-a['time'])))
    blend=3*x*x-2*x*x*x
    join=1 if t>=.3 else 3*(t/.3)**2-2*(t/.3)**3
    return {k:join*(a['values'].get(k,0)*(1-blend)+b['values'].get(k,0)*blend) for k in channels}
def effective_spread(p):return p['mouth_spread']*p['mouth_smile']
def upper(p,x):
    radius=min(1,abs((x-39.5)/35.5));spread=effective_spread(p)
    return -4*spread-(4+5*spread)*p['mouth_smile']*radius**1.5
def gap(p,x):
    radius=min(1,abs((x-39.5)/35.5))
    curve=max(0,1-radius*radius)**.72
    return p['mouth_open']*.55*54*((1-p['mouth_smile'])+p['mouth_smile']*curve)
def audit(plan,static,motion,profile):
    errors=[];checks=0
    def check(ok,label):
        nonlocal checks
        checks+=1
        if not ok:errors.append(label)
    check(len(plan)==len(static['records'])==8,'eight static records')
    check(len(motion['records'])==121,'121 timeline records')
    check(static['status']==motion['status']=='PASS','passing receipts')
    check(static['failures']==motion['failures']==[],'no probe failures')
    controls=set(motion['records'][0]['pose'])
    for anchor,row in zip(plan,static['records']):
        p=row['pose'];name=row['name']
        check(anchor['name']==name,'static name '+name)
        for k,v in p.items():check(close(v,anchor['pose'].get(k,0)),f'static pose {name} {k}')
        for side in ['screen_left','screen_right']:
            b=row['brow_geometry'][side]
            check(close(b['pivot_delta_source_px'][0],0) and close(b['pivot_delta_source_px'][1],-10*p['brow_'+side],1e-4),'brow translation '+name+side)
            check(close(b['rotation_degrees'],8*p['brow_tilt_'+side]),'brow rotation '+name+side)
            check(b['inner_lift']==0,'no inner-brow lift '+name+side)
            lash=row['lash_geometry'][side];blink=p['blink_R' if side=='screen_left' else 'blink_L']
            check(close(lash['closure'],blink) and close(lash['pivot_delta_source_px'][0],0) and close(lash['pivot_delta_source_px'][1],36*blink,1e-4),'lid closure side/travel '+name+side)
        for actual,expected in zip(row['actual_mouth_side_delta_source_px'],[-20*effective_spread(p),20*effective_spread(p)]):check(close(actual,expected),'effective spread width '+name)
        check([o['x'] for o in row['lip_contour_offsets']]==[4,39.5,75],'lip sample x values '+name)
        for lip in row['lip_contour_offsets']:
            x=lip['x'];u=upper(p,x);g=gap(p,x)
            check(close(lip['upper_y'],u),'independent upper lip '+name+str(x))
            check(close(lip['lower_y'],u+g),'independent lower lip '+name+str(x))
        check(close(row['central_lip_gap_native_px'],gap(p,39.5)),'static central aperture '+name)
        check(close(row['central_lip_gap_bust_px'],.49*gap(p,39.5)),'scaled central aperture '+name)
        check(close(upper(p,4)-upper(p,75),12*p['mouth_corner_lift_screen_right']),'common corner bias '+name)
    maximum=0
    for i,row in enumerate(motion['records']):
        check(row['frame']==i and close(row['time'],i/30,1e-12),'timeline frame/time '+str(i))
        p=row['pose'];expected=sample(profile['keyframes'],i/30,controls)
        check(set(p)==controls,'stable pose keys '+str(i))
        for k,v in p.items():
            maximum=max(maximum,abs(v-expected[k]))
            check(close(v,expected[k],1e-6),f'timeline math {i} {k}')
            check(v==0 if k not in ACTING else -1<=v<=1 if k.startswith('brow_') else 0<=v<=1,f'excluded/bounded {i} {k}')
        check(close(row['central_lip_gap_native_px'],gap(expected,39.5)),'timeline gap '+str(i))
        check(0<=p['blink_L']==p['blink_R']<=.120001,'bilateral focused lids '+str(i))
        check(-.320001<=p['brow_screen_left']==p['brow_screen_right']<=0,'equal low brows '+str(i))
        check(close(p['brow_tilt_screen_left'],-p['brow_tilt_screen_right']) and 0<=p['brow_tilt_screen_left']<=.420001,'mirrored inward tilt '+str(i))
        if i<=6 or i>=111:check(all(v==0 for v in p.values()),'neutral endpoint hold '+str(i))
        if i:
            previous=motion['records'][i-1]['pose']
            check(all(abs(p[k]-previous[k])<.20 for k in ACTING),'frame-step bound '+str(i))
    p=motion['records'][48]['pose'];opened=motion['records'][72]['pose']
    check(close(gap(p,39.5),8.91),'tooth-grin aperture')
    check(close(upper(p,75),-9.28368) and close(upper(p,4),-9.28368),'symmetric lifted grin corners')
    check(close(gap(opened,39.5),13.662),'later open-grin aperture')
    check(all(close(row['pose'][k],p[k]) for row in motion['records'][48:61] for k in controls),'held shallow tooth grin')
    onset=motion['records'][18]['pose']
    check(onset['brow_screen_left']<0 and onset['brow_tilt_screen_left']>0 and onset['mouth_open']==0,'brows precede opening')
    check(all(motion['records'][i]['pose']['mouth_open']>=motion['records'][i-1]['pose']['mouth_open'] for i in range(1,73)),'monotone opening build')
    check(all(motion['records'][i]['pose']['mouth_open']<=motion['records'][i-1]['pose']['mouth_open'] for i in range(73,121)),'single gradual reseal')
    check(motion['records'][96]['pose']['mouth_open']==0 and motion['records'][96]['pose']['mouth_smile']>.219,'reseal before smile recovery')
    check(motion['lifecycle_interruption_times']==[.35,.6,1,1.6,2,2.4,2.8,3.2,3.7] and motion['lifecycle_assertions']==36,'lifecycle evidence')
    return dict(status='FAIL' if errors else 'PASS',checks=checks,failures=errors,max_control_error=maximum,independent_timeline_samples=121)
def main():
    result=audit(load(W/'plan.json'),load(W/'state_checks.json'),load(W/'motion_state_checks.json'),load(W/'EXP-104.json'))
    f=load(W/'BASELINE_FREEZE.json');entry=load(W/'SOURCE_CATALOGUE_ENTRY.json');ref=load(W/'SOURCE_REFERENCE.json')
    catalogue=load(Path(f['source_catalogue']));root=Path(f['source_catalogue']).parent.parent
    assert next(x for x in catalogue['expressions'] if x['id']=='EXP-104')==entry
    assert sha(Path(ref['sheet']))==ref['sha256']==entry['asset_production']['sha256']
    crops={}
    with Image.open(ref['sheet']) as sheet:
        assert list(sheet.size)==ref['dimensions']==[1159,1358]
        for p in entry['key_pose_sequence']:
            name=p['actual_panel_path']
            assert sha(root/name)==ref['panel_hashes'][name]==p['sha256']
            with Image.open(root/name) as panel:
                extracted=sheet.crop(p['crop_bounds_xyxy']).convert('RGBA')
                crops[name]=extracted.size==panel.size and extracted.tobytes()==panel.convert('RGBA').tobytes()
    assert len(crops)==9 and all(crops.values())
    result['source_panels_exact_lossless_crops']=crops
    result['native_capture']='PENDING; no renderer or UI invoked'
    result['approval']='UNAPPROVED'
    (W/'independent_geometry_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='source_panels_exact_lossless_crops'},indent=2))
    return 0 if result['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())

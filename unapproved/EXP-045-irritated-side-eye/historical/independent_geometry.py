"""Read-only independent source/geometry/timeline validation. No Godot or renderer."""
import hashlib
import json
import math
from pathlib import Path
from PIL import Image
W=Path(__file__).resolve().parent
ACTING={'brow_screen_left','brow_screen_right','brow_tilt_screen_left','brow_tilt_screen_right','blink_L','blink_R','aversion_px'}
load=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def close(a,b,eps=1e-5):
    return math.isfinite(a) and math.isfinite(b) and abs(a-b)<eps
def sample(keys,t,channels,initial_blend=True):
    for a,b in zip(keys,keys[1:]):
        if a['time']<=t<=b['time']:break
    x=min(1,max(0,(t-a['time'])/(b['time']-a['time'])))
    blend=3*x*x-2*x*x*x
    join=1 if t>=.3 or not initial_blend else 3*(t/.3)**2-2*(t/.3)**3
    return {k:join*(a['values'].get(k,0)*(1-blend)+b['values'].get(k,0)*blend) for k in channels}
def upper(p,x):
    radius=min(1,abs((x-39.5)/35.5))
    corner=12*p['mouth_corner_lift_screen_right']*radius**3 if x>=39.5 else 0
    return p['mouth_purse']*(4+8*radius**2)-corner
def gap(p,x):
    opening,purse=p['mouth_open'],p['mouth_purse']
    aperture=1
    if purse:
        mapped=(x-39.5)*(1-14*purse/35.5)
        cavity=38-12*opening*.55-14*purse
        r=min(1,abs(mapped)/cavity)
        aperture=(1-purse)+purse*math.sqrt(max(0,1-r*r))
    return max(0,opening*.55*54*aperture-1.5*purse*min(1,4*opening))
def scoped_valid(p):
    if not all(math.isfinite(v) for v in p.values()):return False
    if not 0<=p.get('aversion_px',0)<=12:return False
    if p.get('aversion_px',0)>0:
        if min(p.get('blink_R',0),p.get('blink_L',0))<.18:return False
        if any(p.get(k,0)!=0 for k in ['gaze_x','gaze_y','gaze_down_extra','opening_px','eye_smile_L','eye_smile_R']):return False
    return True
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
        for side in ['screen_left','screen_right']:
            for field in ['sprite_delta_source_px','iris_shader_offset_source_px']:
                check(close(row['iris_geometry'][side][field][0],p['aversion_px'],1e-4) and row['iris_geometry'][side][field][1]==0,'actual static iris displacement '+name+side+field)
        for actual,expected in zip(row['actual_mouth_side_delta_source_px'],[14*p['mouth_purse'],-14*p['mouth_purse']]):check(close(actual,expected),'purse width '+name)
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
            check(v==0 if k not in ACTING else -1<=v<=1 if k.startswith('brow_') else 0<=v<=12 if k=='aversion_px' else 0<=v<=1,f'excluded/bounded {i} {k}')
        check(close(row['central_lip_gap_native_px'],gap(expected,39.5)),'timeline gap '+str(i))
        check(0<=p['blink_R']<=.380001 and 0<=p['blink_L']<=.300001,'narrowed unequal lids '+str(i))
        check(-.650001<=p['brow_screen_left']<=0 and 0<=p['brow_screen_right']<=.220001,'unequal opposed brows '+str(i))
        check(scoped_valid(p),'aversion invariant '+str(i))
        for side in ['screen_left','screen_right']:
            for field in ['sprite_delta_source_px','iris_shader_offset_source_px']:
                check(close(row['iris_geometry'][side][field][0],p['aversion_px'],1e-4) and row['iris_geometry'][side][field][1]==0,'actual timeline iris displacement '+str(i)+side+field)
        if i<=6 or i>=111:check(all(v==0 for v in p.values()),'neutral endpoint hold '+str(i))
        if i:
            previous=motion['records'][i-1]['pose']
            check(all(abs(p[k]-previous[k])<(.9 if k=='aversion_px' else .20) for k in ACTING),'frame-step bound '+str(i))
    p=motion['records'][48]['pose']
    check(close(p['aversion_px'],12),'peak source-pixel aversion')
    check(close(gap(p,39.5),0) and upper(p,75)==upper(p,4)==0,'sealed neutral mouth')
    check(close(p['brow_screen_left'],-.65) and close(p['brow_screen_right'],.22),'unequal opposed peak brows')
    check(close(p['brow_tilt_screen_left'],.5) and close(p['brow_tilt_screen_right'],-.28),'unequal opposed peak tilts')
    check(all(close(row['pose'][k],p[k]) for row in motion['records'][48:73] for k in controls),'sustained held peak')
    onset=motion['records'][18]['pose'];center=motion['records'][96]['pose']
    check(min(onset['blink_R'],onset['blink_L'])>=.18 and onset['aversion_px']==0,'lids established before glance')
    check(min(center['blink_R'],center['blink_L'])>=.18 and center['aversion_px']==0,'gaze centers before lid release')
    check(all(motion['records'][i]['pose']['aversion_px']>=motion['records'][i-1]['pose']['aversion_px'] for i in range(1,49)),'monotone gaze onset')
    check(all(motion['records'][i]['pose']['aversion_px']<=motion['records'][i-1]['pose']['aversion_px'] for i in range(73,121)),'monotone return gaze')
    for j,(a,b) in enumerate(zip(profile['keyframes'],profile['keyframes'][1:])):
        if max(a['values'].get('aversion_px',0),b['values'].get('aversion_px',0))>0:
            for lid in ['blink_R','blink_L']:check(min(a['values'].get(lid,0),b['values'].get(lid,0))>=.18,'all adjoining aversion segment endpoints support lids '+str(j)+lid)
            for k in ['gaze_x','gaze_y','gaze_down_extra','opening_px','eye_smile_L','eye_smile_R']:check(a['values'].get(k,0)==b['values'].get(k,0)==0,'no adjoining segment conflict '+str(j)+k)
        for fraction in [0,1e-9,.001,.01,.1,.25,.5,.75,.9,.99,.999,1-1e-9,1]:
            q=sample(profile['keyframes'],a['time']+(b['time']-a['time'])*fraction,controls)
            check(scoped_valid(q),'dense adjoining segment invariant '+str(j)+str(fraction))
    life=motion['lifecycle_scoped_samples']
    check(len(life)==252,'all restart and release trajectory samples')
    expected_order=[(t,stage,j+1) for t in [.35,.6,1,1.6,2.4,2.8,3.2,3.5,3.7] for stage,n in [('restart',12),('release',16)] for j in range(n)]
    check([(r['interruption_time'],r['stage'],r['step']) for r in life]==expected_order,'lifecycle sample order')
    max_lifecycle_error=0
    for row in life:
        source=sample(profile['keyframes'],row['interruption_time'],controls)
        elapsed=row['step']/30
        target=sample(profile['keyframes'],elapsed,controls,False) if row['stage']=='restart' else {k:0. for k in controls}
        duration=.3 if row['stage']=='restart' else .45
        u=min(1.,elapsed/duration)
        smooth=lambda x:max(0.,min(1.,x))**2*(3-2*max(0.,min(1.,x)))
        if source['aversion_px']>0 and u<.5:
            expected=dict(source);expected['aversion_px']*=1-smooth(2*u)
        elif source['aversion_px']>0:
            blend=smooth(2*u-1);expected={k:source[k]*(1-blend)+target[k]*blend for k in controls}
            expected['aversion_px']=target['aversion_px']*blend
        else:
            blend=smooth(u);expected={k:source[k]*(1-blend)+target[k]*blend for k in controls}
        max_lifecycle_error=max(max_lifecycle_error,max(abs(row['pose'][k]-expected[k]) for k in controls))
        check(all(close(row['pose'][k],expected[k],1e-5) for k in controls),'independent lifecycle full pose '+str(row['interruption_time'])+row['stage']+str(row['step']))
        check(scoped_valid(row['pose']),'lifecycle aversion invariant')
        check(all(v==0 for k,v in row['pose'].items() if k not in ACTING),'lifecycle excluded controls')
    check(all(all(v==0 for v in r['pose'].values()) for r in life if r['stage']=='release' and r['step']==16),'all releases recover exact neutral')
    check(motion['lifecycle_interruption_times']==[.35,.6,1,1.6,2.4,2.8,3.2,3.5,3.7] and motion['lifecycle_assertions']==36,'lifecycle evidence')
    return dict(status='FAIL' if errors else 'PASS',checks=checks,failures=errors,max_control_error=maximum,max_lifecycle_error=max_lifecycle_error,independent_timeline_samples=121,independent_lifecycle_samples=252)
def main():
    result=audit(load(W/'plan.json'),load(W/'state_checks.json'),load(W/'motion_state_checks.json'),load(W/'EXP-045.json'))
    f=load(W/'BASELINE_FREEZE.json');entry=load(W/'SOURCE_CATALOGUE_ENTRY.json');ref=load(W/'SOURCE_REFERENCE.json')
    catalogue=load(Path(f['source_catalogue']));root=Path(f['source_catalogue']).parent.parent
    assert next(x for x in catalogue['expressions'] if x['id']=='EXP-045')==entry
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

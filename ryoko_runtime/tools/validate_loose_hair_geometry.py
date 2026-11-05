"""Read-only source/mesh audit; writes evidence to the sibling output directory.

Evaluate piecewise-linear weights on the actual 32x40 mesh, including all four
corners and the center of every source-pixel footprint. No project files change.
Color checks are a conservative hair-color heuristic, not a semantic mask or
substitute for runtime visual review. Existing source RGB under faint alpha is
reported separately rather than silently treated as opaque artwork.
"""
from pathlib import Path
import hashlib, json
import numpy as np
from PIL import Image

PROJECT=Path(__file__).resolve().parents[1]
OUT=PROJECT.parent/'output';OUT.mkdir(exist_ok=True)
SOURCE=PROJECT/'artwork/bust_base.png'
src=np.asarray(Image.open(SOURCE).convert('RGBA'))
h,w=src.shape[:2]
assert (w,h)==(1136,1384)
vx,vy=np.meshgrid(np.arange(33)*w/32,np.arange(41)*h/40)
y,x=np.indices((h,w),dtype=float)

def smoothstep(a,b,z):
    t=np.clip((z-a)/(b-a),0,1)
    return t*t*(3-2*t)

def vertex_fields(params):
    y0,y1,y2,y3,left0,left1,right0,right1=params
    v=smoothstep(y0,y1,vy)*(1-smoothstep(y2,y3,vy))
    return [v*(1-smoothstep(left0,left1,vx)),v*smoothstep(right0,right1,vx)]

def interpolate(a,X,Y):
    cx=np.minimum((X/(w/32)).astype(int),31)
    cy=np.minimum((Y/(h/40)).astype(int),39)
    u=X/(w/32)-cx
    v=Y/(h/40)-cy
    aa=a[cy,cx];bb=a[cy,cx+1];cc=a[cy+1,cx];dd=a[cy+1,cx+1]
    # Matches _build_grid(): [a,c,b] and [b,c,d], diagonal from b to c.
    return np.where(u+v<=1,aa*(1-u-v)+bb*u+cc*v,
                    bb*(1-v)+cc*(1-u)+dd*(u+v-1))

def footprint(a):
    return np.maximum.reduce([interpolate(a,x+ox,y+oy) for ox,oy in
                              [(0,0),(1,0),(0,1),(1,1),(.5,.5)]])

def bbox(sel):
    yy,xx=np.where(sel)
    return [int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max())] if len(xx) else None

rgb=src[:,:,:3].astype(int)
r,g,b=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
visible=src[:,:,3]>76  # alpha > about .3
nonhair=(g<=r)|(b-g>3)|((np.max(rgb,2)-np.min(rgb,2)<10)&(g>160))
report={
    'source':'artwork/bust_base.png',
    'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    'mesh_columns_rows':[32,40],
    'mesh_stride':[w/32,h/40],
    'pixel_samples':'Four footprint corners and center; max piecewise-linear weight.',
    'nonhair_color_test':'G<=R OR B-G>3 OR (RGB range<10 AND G>160)',
    'color_threshold':'Source alpha >76/255',
    'variants':{},
}
params_by_name={
    'corrected':[600,690,750,795,335,390,746,790],
}
for name,params in params_by_name.items():
    verts=vertex_fields(params)
    weights=[footprint(a) for a in verts]
    results={'parameters':params,'sides':{}}
    for side,ww,a in zip(['screen_left','screen_right'],weights,verts):
        active=(ww>1e-12)&visible
        bad=active&nonhair
        faint=(ww>1e-12)&(src[:,:,3]>0)&(src[:,:,3]<=76)&(r-g>2)
        yy,xx=np.where(faint)
        samples=[{'xy':[int(xx[i]),int(yy[i])],
                  'rgba':src[yy[i],xx[i]].tolist(),
                  'max_weight':float(ww[yy[i],xx[i]])}
                 for i in np.argsort(-src[yy,xx,3].astype(int))[:8]]
        aa=a[:-1,:-1];bb=a[:-1,1:];cc=a[1:,:-1];dd=a[1:,1:]
        gx1=(bb-aa)/(w/32);gy1=(cc-aa)/(h/40)
        gx2=(dd-cc)/(w/32);gy2=(dd-bb)/(h/40)
        jacobian=min((1-10*np.sqrt(gx1*gx1+gy1*gy1)).min(),
                     (1-10*np.sqrt(gx2*gx2+gy2*gy2)).min())
        results['sides'][side]={
            'affected_visible_source_pixels':int(active.sum()),
            'affected_visible_bbox_inclusive':bbox(active),
            'nonhair_color_visible_pixels':int(bad.sum()),
            'nonhair_color_bbox_inclusive':bbox(bad),
            'nonhair_color_max_weight':float(ww[bad].max()) if bad.any() else 0,
            'minimum_G_minus_R_affected_visible':int((g-r)[active].min()),
            'minimum_G_minus_B_affected_visible':int((g-b)[active].min()),
            'faint_warm_fringe_pixel_count':int(faint.sum()),
            'faint_warm_fringe_max_alpha':int(src[:,:,3][faint].max()) if faint.any() else 0,
            'faint_warm_fringe_highest_alpha_examples':samples,
            'conservative_Jacobian_lower_bound_offset_length10':float(jacobian),
        }
    report['variants'][name]=results
    if name=='corrected':
        allw=np.maximum.reduce(weights)
        corrected_verts=verts

manifest=json.loads((PROJECT/'registration.json').read_text())
entries=[]
for kind in ['mouths','blinks']:entries.extend(manifest[kind].values())
for e in manifest['expressions'].values():
    entries.extend(e['eyes'].values());entries.extend(e['blinks'].values())
    entries.append(e['mouth']);entries.extend(e.get('effects',[]))
checked=0;violations=[]
for e in entries:
    im=np.asarray(Image.open(PROJECT/'artwork'/e['file']).convert('RGBA'))
    x0,y0=e['xy'];hh,ww=im.shape[:2]
    weights=allw[y0:y0+hh,x0:x0+ww]
    selected=im[:,:,3]>0
    checked+=int(selected.sum())
    if np.any(weights[selected]>1e-12):
        violations.append({'file':e['file'],'max_weight':float(weights[selected].max())})
report['corrected_overlay_checks']={
    'entries':len(entries),'alpha_bearing_pixel_footprints':checked,'violations':violations}
report['corrected_protected_masks']={}
for name in ['earring_clear_masks.png','brow_allow_screen_left.png',
             'brow_allow_screen_right.png','aperture_screen_left.png',
             'aperture_screen_right.png']:
    a=np.asarray(Image.open(PROJECT/'rig_assets'/name))
    selected=((a[:,:,0]>0)|(a[:,:,1]>0)) if name=='earring_clear_masks.png' else (
        a[:,:,0]>0 if a.ndim==3 else a>0)
    report['corrected_protected_masks'][name]={
        'selected_pixels':int(selected.sum()),'maximum_weight':float(allw[selected].max())}
report['corrected_protected_boxes']={}
for name,box in [
    ('left_exposed_ear',(379,540,421,580)),
    ('right_exposed_ear',(708,540,745,610)),
    ('left_fixed_stud',(395,570,423,600)),
    ('right_fixed_stud',(702,570,732,598)),
    ('central_face_neck',(391,340,745,795)),
    ('clothing_from_y796',(0,796,1136,1384)),
]:
    x0,y0,x1,y1=box
    region=allw[y0:y1,x0:x1];selected=visible[y0:y1,x0:x1]
    report['corrected_protected_boxes'][name]={
        'box_exclusive':list(box),'selected_visible_pixels':int(selected.sum()),
        'max_visible_weight':float(region[selected].max()) if selected.any() else 0,
        'affected_visible_pixels':int(((region>1e-12)&selected).sum())}
report['corrected_support']={
    'y_open_interval':[588.2,795.8],
    'left_x_less_than':390.5,
    'right_x_greater_than':745.5,
    'nonzero_grid_rows':[float(v) for v in vy[:,0][np.any(corrected_verts[0]>0,axis=1)]]}
report['limitations']=[
    'Color classification is a source-pixel heuristic, not a hair semantic mask.',
    'The listed ear/stud/central-face rectangles are conservative visual landmarks, not authored masks.',
    'The support proof uses current mesh topology and source alpha; re-run if either changes.',
    'No runtime screenshot, motion, boundary antialiasing, or simultaneous-deformation visual QA is claimed here.',
    'Jacobian estimate covers this additional local weight displacement alone, not all pre-existing transforms.',
    'Faint warm fringe pixels already exist in the source; their RGB can move with the hair silhouette.'
]
assert not violations
assert all(d['nonhair_color_visible_pixels']==0 for d in report['variants']['corrected']['sides'].values())
assert all(d['maximum_weight']==0 for d in report['corrected_protected_masks'].values())
assert all(d['max_visible_weight']==0 for d in report['corrected_protected_boxes'].values())
assert all(d['conservative_Jacobian_lower_bound_offset_length10']>0 for d in report['variants']['corrected']['sides'].values())
report['status']='passed_source_support_audit'
(OUT/'side_lock_weight_audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))

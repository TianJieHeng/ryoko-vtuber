#!/usr/bin/env python3
"""Deterministic separate-part smile support. No face patch or runtime texture warp.
Eye source extraction is upstream and immutable. Canonical lips are source-native
with static upper/lower ownership and 14 independent rigid contour joints.
"""
import json,hashlib,shutil
from pathlib import Path
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parents[1]
S=P/'source_references/smile_preparation'; O=P/'rig_assets/smile_support'; O.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest={'version':1,'status':'LOCAL_REVIEW_CANDIDATE','objects':{},'sources':{},'inference':[]}
for side in ['screen_left','screen_right']:
    origin=(410,469) if side=='screen_left' else (607,468)
    for kind in ['lash','lower_contour','hidden_continuation']:
        name=f'laugh_{kind}_{side}';src=S/(name+'.png');shutil.copyfile(src,O/src.name)
        manifest['sources'][str(src.relative_to(P))]=sha(src)
        manifest['objects'][name]={'file':src.name,'xy':origin,'z':36 if kind=='lash' else 35,'side':side,'kind':kind,'inferred':kind=='hidden_continuation'}
    low=np.array(Image.open(S/f'laugh_lower_contour_{side}.png'))[:,:,3]
    upp=np.array(Image.open(S/f'laugh_lash_{side}.png'))[:,:,3]
    h,w=low.shape;xx=np.arange(w); valid=[];vals=[]
    for x in xx:
        yy=np.where(low[:,x]>16)[0]
        if len(yy):valid.append(x);vals.append(float(yy[0]))
    mid=np.interp(xx,valid,vals)
    pr=np.zeros((h,w,4),np.uint8);pr[:,:,0]=np.rint(mid)[None,:];pr[:,:,3]=255
    for x in xx:
        yy=np.where(upp[:,x]>0)[0];pr[:,x,1]=min(yy) if len(yy) else mid[x];pr[:,x,2]=max(yy) if len(yy) else mid[x]
    old=np.array(Image.open(P/'rig_assets/object_face'/f'closed_lash_{side}.png'))[:,:,3].astype(float)
    new=np.maximum(low,upp).astype(float)
    hidden=np.array(Image.open(S/f'laugh_hidden_continuation_{side}.png'))[:,:,3]
    new=np.maximum(new,hidden)
    def centers(a):
        weight=a.sum(axis=0); valid=weight>0
        c=(a*np.arange(a.shape[0])[:,None]).sum(axis=0)/np.maximum(weight,1)
        from scipy.ndimage import gaussian_filter1d
        return gaussian_filter1d(np.interp(np.arange(a.shape[1]),np.where(valid)[0],c[valid]),2.0).tolist()
    manifest.setdefault('eye_joints',{})[side]={'origin':origin,'size':[w,h], 'old_centers':centers(old),'new_centers':centers(new),'edges':list(range(0,w,8))+[w]}

# Original lip RGBA is not warped/repainted. Each runtime joint shares this
# immutable source and clips a static native strip. New articulation is inferred.
manifest['lips']={'texture':'../yawn_mouth/upper_lip.png','origin':[525,620], 'size':[80,45], 'segment_edges':[0,9,14,19,24,29,34,40,46,51,56,61,66,71,80], 'corner_lift_pixels':4.0,'max_opening':0.55,'max_aperture_pixels':30.8,'note':'Inferred rigid-joint contour articulation of canonical native lip pigment; no painted expression replacement. Outer strips are independent corner owners.'}
# Hidden joint material is an explicit reconstruction, not native pigment.
# Cross-sections interpolate the two native columns beside each joint, while
# dynamic geometry only reveals a bounded width of the fixed 12px owner.
lip=np.array(Image.open(P/'rig_assets/yawn_mouth/upper_lip.png')).astype(float)/255
seam=np.array(Image.open(P/'rig_assets/yawn_mouth/neutral_seam.png'))[0,:,0].astype(float)/255*63.75
manifest['lip_continuations']=[]
def smooth(a,b,x):
    t=np.clip((x-a)/(b-a),0,1);return t*t*(3-2*t)
for edge in manifest['lips']['segment_edges'][1:-1]:
    patch=np.zeros((45,12,4),float)
    for x in range(12):
        u=x/11;patch[:,x]=lip[:,max(0,edge-1)]*(1-u)+lip[:,min(79,edge)]*u
    for upper in [False,True]:
        out=patch.copy();y=np.arange(45)+.5
        lower=smooth(seam[min(edge,79)]+.45,seam[min(edge,79)]+1.55,y)*smooth(8.5,9.5,edge)*(1-smooth(69.5,70.5,edge))
        la=out[:,:,3]*lower[:,None]
        out[:,:,3]=(out[:,:,3]-la)/np.maximum(1-la,1e-8) if upper else la
        name=('upper' if upper else 'lower')+f'_joint_continuation_{edge}'
        Image.fromarray(np.rint(np.clip(out,0,1)*255).astype('uint8')).save(O/(name+'.png'))
        Image.fromarray((out[:,:,3]>0).astype('uint8')*255).save(O/(name+'_inferred_mask.png'))
        manifest['lip_continuations'].append({'name':name,'file':name+'.png','edge':edge,'upper':upper,'size':[12,45],'pivot':[6,14], 'classification':'ENTIRELY_INFERRED_HIDDEN_JOINT_PIGMENT','source_columns':[edge-1,edge],'nontransparent_pixels':int((np.rint(out[:,:,3]*255)>0).sum()),'inferred_support_pixels':int((out[:,:,3]>0).sum()),'inferred_mask':name+'_inferred_mask.png'})
# Pack tiny continuations without combining their logical owners or UV motion.
# Every owner retains its fixed native12x45 region and an independent transform.
atlas=Image.new('RGBA',(120,265));mask_atlas=Image.new('L',(120,265))
for i,e in enumerate(manifest['lip_continuations']):
    xy=(i%6*20+4,i//6*53+4)
    part=Image.open(O/e['file']).convert('RGBA');mask=Image.open(O/e['inferred_mask']).convert('L')
    atlas.paste(part,xy);mask_atlas.paste(mask,xy)
    (O/e['file']).unlink();(O/e['inferred_mask']).unlink()
    e['file']='lip_continuations_atlas.png';e['inferred_mask']='lip_continuations_inferred_atlas.png'
    e['atlas_rect']=[*xy,12,45]
    e['region_rgba_sha256']=hashlib.sha256(part.tobytes()).hexdigest()
atlas.save(O/'lip_continuations_atlas.png');mask_atlas.save(O/'lip_continuations_inferred_atlas.png')
manifest['inference'].append('Lip joint sleeves contain inferred pigment across material absent from the rigid native strips. Their full alpha support is separately masked; runtime reveals only geometric endpoint gaps. Peak contribution must be measured, not described as negligible.')
manifest['inference'] += ['Laugh eye upper/lower ownership and mattes are inherited estimates. Hidden continuation is entirely inferred.', 'Rigid lip joint divisions, pivots and smile paths are inferred. Runtime UV and each joint scale remain unchanged.']
# Source-backed residue ownership: original pixel layer + inferred stationary
# skin behind it. The fringe candidates are reviewed separately below.
# Five semitransparent edge samples are retained; ten opaque crossing mixtures
# require distinct inferred hair continuation and neutral eye pigment owners.
back=np.array(Image.open(P/'rig_assets/object_face/stationary_backing.png')).astype(float)
clean=back.copy(); allmask=np.zeros(back.shape[:2],bool); residue=[]
for name in ['backing_detached_upper_lash_tip','backing_orphan_crease_flecks']:
    core=np.array(Image.open(S/'residue_masks'/(name+'_source_core_global.png')))>0
    halo=np.array(Image.open(S/'residue_masks'/(name+'_matte_review_global.png')))>0
    mask=core|halo; allmask|=mask
    ys,xs=np.where(mask);x0,x1=xs.min()-6,xs.max()+7;y0,y1=ys.min()-6,ys.max()+7
    YY,XX=np.mgrid[y0:y1,x0:x1];rgb=back[y0:y1,x0:x1,:3]
    known=(~mask[y0:y1,x0:x1])&(rgb[:,:,0]>220)&(rgb[:,:,1]>155)&(rgb[:,:,0]-rgb[:,:,1]>25)
    features=np.stack([np.ones_like(XX),XX-xs.mean(),YY-ys.mean()],axis=-1)
    fit=np.linalg.lstsq(features[known],rgb[known],rcond=None)[0]
    estimate=rgb.copy()
    selected=mask[y0:y1,x0:x1]
    estimate[selected]=np.clip((features@fit)[selected],[180,120,95],[255,230,215])
    for _ in range(400):
        padded=np.pad(estimate,((1,1),(1,1),(0,0)),mode='edge')
        mean=(padded[:-2,1:-1]+padded[2:,1:-1]+padded[1:-1,:-2]+padded[1:-1,2:])*.25
        estimate[selected]=mean[selected]
    clean[y0:y1,x0:x1,:3][mask[y0:y1,x0:x1]]=estimate[mask[y0:y1,x0:x1]]
    box=[int(xs.min()-2),int(ys.min()-2),int(xs.max()+3),int(ys.max()+3)]
    residue.append({'name':name,'box':box,'core_pixels':int(core.sum()),'inferred_skin_pixels':int(mask.sum()),'z':21,'classification':'REASSIGNED_NEUTRAL_EYE_PIGMENT_WITH_INFERRED_SKIN_BEHIND'})
Image.fromarray(np.rint(clean).astype('uint8')).save(O/'stationary_backing_eye_reassigned.png')
manifest['residue_objects']=[]
for e in residue:
    x0,y0,x1,y1=e['box']; crop=np.s_[y0:y1,x0:x1]
    for suffix,a in [('original',back[crop]),('skin',clean[crop])]:Image.fromarray(np.rint(a).astype('uint8')).save(O/(e['name']+'_'+suffix+'.png'))
    mask=np.array(Image.open(S/'residue_masks'/(e['name']+'_source_core_global.png')))>0
    mask|=np.array(Image.open(S/'residue_masks'/(e['name']+'_matte_review_global.png')))>0
    Image.fromarray((mask[crop]*255).astype('uint8')).save(O/(e['name']+'_ownership.png'))
    e['xy']=[x0,y0]; e['size']=[x1-x0,y1-y0];manifest['residue_objects'].append(e)
manifest['residue_review']={'backing_original_sha256':sha(P/'rig_assets/object_face/stationary_backing.png'),'reassigned_source_core_pixels':42,'inferred_skin_pixels':int(allmask.sum()),'fringe_pixels_removed':0,'fringe_decision':'Retained all15 review cores: green-biased values and continuity along the actual hair strand/edge, not detached brown lash pigment. Existing foreground ownership, source alpha and distal gaze-phase hair tip are unchanged.','neutral_reconstruction':'Separate residue shader uses fixed original/skin/ownership samples to preserve the original filtered composite. Rendered parity must be measured.'}

# The ten opaque dark crossing cores need separate ownership. Five translucent
# edge samples are retained, not erased. Dark cores are a flattened hair/lash
# mixture: split their native color into a green foreground + dark eye owner,
# with a separately labeled hidden green continuation behind the neutral ink.
fringe=np.array(Image.open(P/'rig_assets/object_face/hair_front_fringe.png')).astype(float)/255
mask_global=np.array(Image.open(S/'residue_masks/fringe_dark_eye_crossing_source_core_global.png'))>0
mask=mask_global[55:805,41:1112]&(fringe[:,:,3]>.999)
fg=fringe.copy();neutral=np.zeros_like(fringe);hidden=np.zeros_like(fringe)
for y,x in zip(*np.where(mask)):
    patch=fringe[max(0,y-5):y+6,max(0,x-5):x+6]
    good=(patch[:,:,1]>patch[:,:,0])&(patch[:,:,0]>.30)&(patch[:,:,3]>.8)
    green=np.median(patch[:,:,:3][good],axis=0)
    old=fringe[y,x,:3]
    hair_alpha=min(.65,float(np.min(old/np.maximum(green,1e-5)))*.8)
    ink=(old-green*hair_alpha)/(1-hair_alpha)
    fg[y,x,3]=hair_alpha
    neutral[y,x,:3]=ink;neutral[y,x,3]=1
    hidden[y,x,:3]=green;hidden[y,x,3]=1
Image.fromarray(np.rint(np.clip(fg,0,1)*255).astype('uint8')).save(O/'hair_front_fringe_eye_reassigned.png')
box=[672,475,684,485];x0,y0,x1,y1=box;sl=np.s_[y0-55:y1-55,x0-41:x1-41]
for name,arr in [('neutral_fringe_eye_pigment',fringe),('fringe_reassigned_alpha',fg),('hidden_fringe_continuation',hidden)]:
    Image.fromarray(np.rint(np.clip(arr[sl],0,1)*255).astype('uint8')).save(O/(name+'.png'))
Image.fromarray((mask[sl]*255).astype('uint8')).save(O/'hidden_fringe_continuation_inferred_mask.png')
manifest['fringe_reassignment']={'xy':[x0,y0],'size':[x1-x0,y1-y0],'pivot':[529,218],'core_pixels':int(mask.sum()),'retained_edge_pixels':5,'inference':'All ten opaque mixture cores use inferred foreground hair coverage and hidden green continuation. Original foreground RGB is unchanged; source-over alpha factorization assigns the remaining neutral pigment behind it. Five semitransparent hair-edge candidates remain original. These are inferred layer ownerships, not recovered originals.','original_sha256':sha(P/'rig_assets/object_face/hair_front_fringe.png')}
manifest['residue_review']['fringe_pixels_removed']=0
manifest['residue_review']['fringe_decision']='Ten opaque mixed eye/hair cores split into explicit inferred green foreground, dark neutral eye pigment behind it, and hidden green continuation; all five semitransparent edge candidates remain original. Hair outline, pivot, and distal gaze-phase hair-tip ownership are retained.'

(O/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('SMILE_SUPPORT_BUILD_PASS')

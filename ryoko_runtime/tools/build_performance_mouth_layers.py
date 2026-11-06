#!/usr/bin/env python3
"""Separate authored oral features from fixed skin/jaw for expression performance.

Artwork is read-only. Derivatives have explicit per-pixel estimate masks. Cleared RGB
uses a discrete harmonic extension from adjacent source skin. Feature RGB is source
RGB, hard alpha inside the reviewed mask, nearest-source bleed outside.

IMPORTANT: source mouth features cross the source patch feather. Composite cleared
RGB + feature in an opaque patch-sized intermediate, then restore source patch alpha.
This recovers original RGBA bytes at rest, including partially transparent lips.
Ordinary alpha-over on the already feathered cleared patch does NOT do that.
The bust_base is NOT an acceptable skin substitute: the source mouth patch covers
a nose tip and uses different skin shading, exposed by a simple alpha-hole approach.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage, sparse
from scipy.sparse.linalg import spsolve

ROOT=Path(__file__).resolve().parents[1]
REVIEW_IDS=['EXP-005']
# Reviewed in original pixel coordinates. The mask surrounds oral contour, lips,
# highlights and the small lip cast shadow. Jaw and nose lines are excluded.
REVIEWED_POLYGONS={
 'EXP-005':[(27,23),(45,17),(69,11),(101,10),(130,15),(154,21),(153,38),(146,58),(133,80),(116,97),(103,110),(91,114),(77,110),(66,101),(49,83),(37,64),(29,44)],

}

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def mask_for(size,poly):
 im=Image.new('L',size); ImageDraw.Draw(im).polygon(poly,fill=255)
 return np.asarray(im)>0

def harmonic(rgb,mask):
 """Solve Laplace u=0 within mask, Dirichlet source pixels on its boundary."""
 h,w=mask.shape; yy,xx=np.where(mask); n=len(yy)
 index=np.full((h,w),-1,dtype=np.int32); index[yy,xx]=np.arange(n)
 rows=list(range(n));cols=list(range(n));data=[4.0]*n
 rhs=np.zeros((n,3),np.float64)
 for dy,dx in [(0,1),(0,-1),(1,0),(-1,0)]:
  y=yy+dy;x=xx+dx
  if np.any((y<0)|(y>=h)|(x<0)|(x>=w)):raise ValueError('Mask touches patch edge')
  neighbor=index[y,x]; inside=neighbor>=0
  rows.extend(np.flatnonzero(inside).tolist());cols.extend(neighbor[inside].tolist());data.extend([-1.0]*int(inside.sum()))
  rhs[~inside]+=rgb[y[~inside],x[~inside]]
 mat=sparse.csr_matrix((data,(rows,cols)),shape=(n,n))
 out=rgb.copy();out[mask]=np.rint(np.clip(spsolve(mat,rhs),0,255)).astype(np.uint8)
 return out

def feature_at(feature,pivot,scale,width=1.0):
 if scale==1 and width==1:return feature.copy()
 px,py=map(float,pivot); mat=(1/width,0,px-px/width,0,1/scale,py-py/scale)
 return np.asarray(Image.fromarray(feature).transform((feature.shape[1],feature.shape[0]),Image.Transform.AFFINE,mat,Image.Resampling.BILINEAR))

def source_over(bg,fg):
 return np.asarray(Image.alpha_composite(Image.fromarray(bg),Image.fromarray(fg)))

def combine(clear,feature,coverage):
 a=feature[:,:,3:4].astype(np.float64)/255
 rgb=np.rint(feature[:,:,:3]*a+clear[:,:,:3]*(1-a)).astype(np.uint8)
 return np.dstack((rgb,coverage))

def checker(im,size=None):
 a=np.asarray(im);h,w=a.shape[:2];y,x=np.mgrid[:h,:w];v=np.where(((x//8+y//8)%2)==0,50,65).astype(np.uint8)
 bg=np.stack([v]*3,-1);alpha=a[:,:,3:4]/255;out=Image.fromarray(np.rint(a[:,:,:3]*alpha+bg*(1-alpha)).astype(np.uint8))
 if size:out=out.resize(size,Image.Resampling.NEAREST)
 return out

def geometry_guards(out,src,clear,feature,pivot,base,xy):
 """Independent image-space exclusion tests, not a claim of runtime GPU QA."""
 h,w=src.shape[:2]; yy,xx=np.mgrid[:h,:w];xx+=xy[0];yy+=xy[1]
 guards={
  'nose':(xx>=530)&(xx<606)&(yy>=540)&(yy<586),
  'jaw':yy>=700,
  'outside_oral_roi':~((xx>=492)&(xx<644)&(yy>=578)&(yy<700)),
 }
 reference=source_over(base,src);trials=[]
 sheet=Image.new('RGB',(1080,870),'#242424');draw=ImageDraw.Draw(sheet)
 for row,scale_y in enumerate([.235,.6,1.]):
  for col,scale_x in enumerate([.82,1.,1.18]):
   result=source_over(base,combine(clear,feature_at(feature,pivot,scale_y,scale_x),src[:,:,3]))
   changed=np.any(result!=reference,axis=2)
   record={'scale_y':scale_y,'scale_x':scale_x}
   record.update({name+'_changed_pixels':int(np.count_nonzero(changed&guard)) for name,guard in guards.items()})
   assert all(record[name+'_changed_pixels']==0 for name in guards),record
   trials.append(record)
   draw.text((col*360+5,row*290+5),f'EXP-005 Y={scale_y} X={scale_x}',fill='white')
   sheet.paste(Image.fromarray(result).convert('RGB').resize((356,260),Image.Resampling.NEAREST),(col*360+2,row*290+25))
 report={'passed':True,'nose_guard_global':[530,540,606,586],
         'jaw_guard_global_y_min':700,'oral_roi_global':[492,578,644,700],
         'reference':'Original source RGBA over actual bust_base, bilinear image-space feature sampling; GPU shader needs separate runtime QA.',
         'trials':trials}
 (out/'geometry_guard_checks.json').write_text(json.dumps(report,indent=2)+'\n')
 sheet.save(out/'geometry_guard_contact.png')

def build(ids):
 reg=json.loads((ROOT/'registration.json').read_text());out=ROOT/'rig_assets/expression_mouths';out.mkdir(parents=True,exist_ok=True)
 profiles={};test=[];visual=[]
 for id in ids:
  source=ROOT/'artwork'/reg['expressions'][id]['mouth']['file'];before=sha(source);src=np.asarray(Image.open(source).convert('RGBA'));h,w=src.shape[:2]
  poly=REVIEWED_POLYGONS[id];mask=mask_for((w,h),poly)
  clear=src.copy();clear[:,:,:3]=harmonic(src[:,:,:3],mask)
  feature=src.copy();feature[:,:,3]=mask.astype(np.uint8)*255
  # Transparent RGB bleed prevents dark fringes under filtering, never black-fill.
  indices=ndimage.distance_transform_edt(~mask,return_distances=False,return_indices=True)
  feature[~mask,:3]=src[indices[0][~mask],indices[1][~mask],:3]
  yy,xx=np.where(mask); pivot=[round(float(xx.min()+xx.max())/2,2),round(float(yy.min()+yy.max())/2,2)]
  paths={kind:f'{id}_{kind}.png' for kind in ['cleared','feature','estimated_mask','coverage']}
  for kind,arr in [('cleared',clear),('feature',feature),('estimated_mask',mask.astype(np.uint8)*255),('coverage',src[:,:,3])]:Image.fromarray(arr).save(out/paths[kind])
  rest=combine(clear,feature,src[:,:,3]);closed=combine(clear,feature_at(feature,pivot,.235),src[:,:,3]);half=combine(clear,feature_at(feature,pivot,.6),src[:,:,3]); base_full=np.asarray(Image.open(ROOT/'artwork/bust_base.png').convert('RGBA')); xy=reg['expressions'][id]['mouth']['xy']; base=base_full[xy[1]:xy[1]+h,xy[0]:xy[0]+w]
  Image.fromarray(base).save(out/f'{id}_base_reference.png')
  geometry_guards(out,src,clear,feature,pivot,base,xy)
  checks={'id':id,'outside_mask_byte_exact':bool(np.array_equal(clear[~mask],src[~mask])),'rest_rgba_byte_exact':bool(np.array_equal(rest,src)), 'rest_composite_base_byte_exact':bool(np.array_equal(source_over(base,rest),source_over(base,src))),'feature_rgb_byte_exact_in_mask':bool(np.array_equal(feature[mask,:3],src[mask,:3])),'original_file_unchanged':before==sha(source),'mask_pixel_count':int(mask.sum()),'partial_alpha_mask_pixels':int(np.count_nonzero(mask&(src[:,:,3]<255))),'closed_outside_mask_byte_exact':bool(np.array_equal(closed[~mask],src[~mask])), 'outside_mask_motion_note':'Moving the feature can cover different oral skin pixels outside the original concave mask. Nose/jaw and complete swept-region exclusion are checked separately.'}
  # A scaled feature is permitted to cover some fixed skin inside its own swept
  # bounds, but cannot move any original jaw/nose pixels. outside_mask closure
  # check can fail for concave masks under resampling; source clearing still exact.
  assert all(checks[k] for k in ['outside_mask_byte_exact','rest_rgba_byte_exact','feature_rgb_byte_exact_in_mask','original_file_unchanged'])
  profiles[id]={**paths,'pivot':pivot,'xy':reg['expressions'][id]['mouth']['xy'],'size':[w,h],'source':'artwork/'+source.name,'source_sha256':before,'estimated_pixels':int(mask.sum()),'cleared_pixels':int(mask.sum()),'mask_polygon':poly,'closed_scale':.235,'open_scale':1.0,'review_status':'user_approved_EXP005','runtime_enabled':True,'requires_fixed_patch_coverage':True,'feature_method':'original RGB with hard binary alpha and nearest oral RGB filter bleed','underpaint_method':'discrete harmonic neighboring-skin extension; estimated pixels are explicitly masked','base_reference':f'{id}_base_reference.png','clearing_method':'Only RGB inside mask is estimated; original patch alpha unchanged. Final combined patch MUST reuse original alpha coverage.'}
  test.append(checks);visual.append((id,[source_over(base,src),source_over(base,clear),feature,source_over(base,closed),source_over(base,half),source_over(base,rest)]))
 manifest={'version':1,'composition':'Compose cleared RGB and transformed hard-alpha feature in an opaque patch-sized intermediate, then restore original source alpha from coverage. This recovers original RGBA byte-exactly at rest. A CanvasItem shader may do this directly using texture samples, without a SubViewport. Ordinary alpha-over on the feathered cleared patch is not sufficient.','review_scope':'Approved EXP-005 performance only. Static artwork remains unchanged.','profiles':profiles}
 (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');(out/'validation.json').write_text(json.dumps({'passed':all(all(t[k] for k in ['outside_mask_byte_exact','rest_rgba_byte_exact','feature_rgb_byte_exact_in_mask','original_file_unchanged'])for t in test),'profiles':test},indent=2)+'\n')
 cellw=220;cellh=185
 c=Image.new('RGB',(cellw*6,cellh*len(visual)+32),'#242424');d=ImageDraw.Draw(c)
 for j,label in enumerate(['original','cleared (estimated skin)','isolated feature','closed 0.235','half 0.60','rest 1.00 exact']):d.text((j*cellw+5,5),label,fill='white')
 for i,(id,arrays) in enumerate(visual):
  for j,a in enumerate(arrays):
   d.text((j*cellw+5,i*cellh+25),id,fill='white');im=checker(a);im.thumbnail((cellw-10,cellh-25));c.paste(im,(j*cellw+(cellw-im.width)//2,i*cellh+45))
 c.save(out/'contact_sheet.png');print(json.dumps({'output':str(out),'ids':ids,'checks':test},indent=2))

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--ids',nargs='+',choices=REVIEW_IDS,default=REVIEW_IDS);args=parser.parse_args();build(args.ids)

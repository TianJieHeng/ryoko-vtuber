#!/usr/bin/env python3
"""Derive bounded-travel eye owners from canonical flattened pixels.

Original object_face PNGs remain immutable inputs. Hidden colors and the matte
are estimates, not recovered source layers. All outputs are deterministic.
"""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt, gaussian_filter, map_coordinates
R=Path(__file__).resolve().parents[1]
I=R/'rig_assets/object_face';O=R/'rig_assets/gaze_eyes'
CFG={
 'screen_left':dict(origin=[410,469],ellipse=[476.6,488.7,24.0,28.8,0.10]),
 'screen_right':dict(origin=[607,468],ellipse=[646.6,489.5,23.0,26.4,-0.04]),
}
PADDING=[12,16]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,rgb,alpha):
 alpha=np.rint(np.clip(alpha,0,1)*255).astype(np.uint8)
 rgb=np.rint(np.clip(rgb,0,255)).astype(np.uint8)
 known=alpha>0
 if known.any():
  ids=distance_transform_edt(~known,return_distances=False,return_indices=True)
  rgb[~known]=rgb[ids[0][~known],ids[1][~known]]
 Image.fromarray(np.dstack((rgb,alpha))).save(O/name)
def main():
 O.mkdir(parents=True,exist_ok=True)
 source=np.array(Image.open(R/'artwork/bust_base.png').convert('RGBA'))
 manifest={'version':1,'source':'artwork/bust_base.png','source_sha256':sha(R/'artwork/bust_base.png'),
  'source_commit':'d8d9d20542f8b636890145709d0c1228f83fd7cb',
  'original_pngs_unchanged':True,'foreground_objects':{},'eyes':{},'limits_provisional':False,'review_status':'local candidate; user approval pending','calibrated_travel_source_pixels':{'left':4,'right':4,'up':2,'down':1},
  'derivation':'Visible canonical pixels with inferred subpixel iris matte. Hidden sclera is row interpolation of canonical exposed whites; hidden iris cap/boundary colors are local continuation of this same iris. No assembly-source eye donor, new highlight, UV warp or gaze-zero special case.',
  'limitations':'Flattened hair/iris and lower-lid antialias crossings are not clean original layers. New exposed inferred pixels require visual approval. Full hidden eye art is not claimed recovered.'}
 for side,cfg in CFG.items():
  original_iris=np.array(Image.open(I/f'iris_{side}.png').convert('RGBA'))
  original_sclera=np.array(Image.open(I/f'sclera_{side}.png').convert('RGBA'))
  h,w=original_iris.shape[:2];ox,oy=cfg['origin'];yy,xx=np.mgrid[:h,:w];X=xx+ox;Y=yy+oy
  C=source[oy:oy+h,ox:ox+w,:3].astype(float)
  aperture=((original_iris[:,:,3]>0)|(original_sclera[:,:,3]>0))
  original_aperture=aperture.copy()
  hair_transfer=np.zeros((h,w),bool)
  if side=='screen_left':
   # The pale distal diagonal is a HAIR strand, not an iris highlight. Its
   # ownership is now excluded from every observed-iris/provenance anchor.
   points=np.array([[459.5,488.0],[461.2,491.0],[463.8,495.0],[467.0,498.3],[469.2,500.0]])
   strand_dist=np.full((h,w),1e9)
   for aa,bb in zip(points[:-1],points[1:]):
    vx,vy=bb-aa;t=np.clip(((X-aa[0])*vx+(Y-aa[1])*vy)/(vx*vx+vy*vy),0,1)
    strand_dist=np.minimum(strand_dist,np.hypot(X-aa[0]-t*vx,Y-aa[1]-t*vy))
   top=np.array(Image.open(I/f'profile_{side}.png')).astype(float)[:,:,0]+oy
   bottom=np.array(Image.open(I/f'lower_profile_{side}.png')).astype(float)[:,:,0]+oy
   hair_transfer=(strand_dist<=2.3)&(Y>top)&(Y<=bottom-2)
   aperture |= hair_transfer

  cx,cy,rx,ry,tilt=cfg['ellipse']
  rad=np.sqrt(((X-cx-tilt*(Y-cy))/rx)**2+((Y-cy)/ry)**2)
  # The full unseen disk is only a geometric continuation. Visible support is
  # estimated from actual ring/sclera contrast inside this conservative band.
  possible=(rad<1.075)&aperture
  whites=aperture&(rad>1.04)&(C.min(axis=2)>125)&((C.max(axis=2)-C.min(axis=2))<42)
  B=np.zeros_like(C)
  valid_rows=[]
  for y in range(h):
   ids=np.flatnonzero(whites[y])
   if len(ids)>=2:
    for ch in range(3):B[y,:,ch]=np.interp(np.arange(w),ids,C[y,ids,ch])
    valid_rows.append(y)
  assert valid_rows
  for x in range(w):
   for ch in range(3):B[:,x,ch]=np.interp(np.arange(h),valid_rows,B[valid_rows,x,ch])
  B=gaussian_filter(B,sigma=(1.0,0.65,0));B=np.rint(B);sclera_estimate=B.copy()
  ring=np.array([55.,29.,17.])
  delta=B-ring;alpha=np.sum((B-C)*delta,axis=2)/np.maximum(np.sum(delta*delta,axis=2),1)
  alpha=np.clip(alpha,0,1);alpha[rad<.88]=1;alpha[~possible]=0
  # An unmixing alpha must admit finite in-gamut foreground RGB. Round upward
  # to preserve that condition in RGBA8. Near-white opaque highlights remain.
  amin=np.maximum(np.max(np.maximum(B-C,0)/np.maximum(B,1),axis=2),np.max(np.maximum(C-B,0)/np.maximum(255-B,1),axis=2))
  alpha=np.maximum(alpha,amin)*possible
  alpha=np.ceil(alpha*255)/255
  alpha[(alpha<.035)&(rad>.975)]=0
  # Preserve the approved stationary visible whites exactly. This includes
  # the source's tiny naturally warm lower-rim antialias samples.
  B[alpha==0]=C[alpha==0]
  F=np.clip(np.rint((C-B*(1-alpha[:,:,None]))/np.maximum(alpha[:,:,None],1/255)),0,255)
  F[alpha>=1]=C[alpha>=1]
  # Pale edge RGB belongs to the background mixture, never a moving white
  # fringe. Refit those mixtures with measured dark-ring foreground and a
  # minimally adjusted stationary background, preserving canonical composites.
  pale=(rad>.88)&(((F.min(axis=2)>125)&((F.max(axis=2)-F.min(axis=2))<60))|(F[:,:,1]>F[:,:,0]+3)|(F[:,:,2]>F[:,:,1]+3))&(alpha>0)
  # Exact neutral color and clean layers cannot both be inferred at several
  # flattened white/iris antialias samples. Keep the smooth sclera and bound
  # the foreground to measured ring color instead of baking a stationary rim.
  # These few visible matte differences are quantified below, not hidden.
  alpha[pale]=np.rint(np.clip(np.sum((B-C)*delta,axis=2)/np.maximum(np.sum(delta*delta,axis=2),1),0,1)[pale]*255)/255
  F[pale]=ring
  if hair_transfer.any():
   # Infer only the newly uncovered iris behind the strand, from clean local
   # iris neighbors. There is no face patch and no moving strand in this disk.
   known=(alpha>.75)&original_aperture&~hair_transfer
   ii=distance_transform_edt(~known,return_distances=False,return_indices=True)
   filled=F.copy();filled[hair_transfer]=F[ii[0][hair_transfer],ii[1][hair_transfer]]
   for _ in range(400):
    z=np.pad(filled,((1,1),(1,1),(0,0)),mode='edge')
    mean=(z[:-2,1:-1]+z[2:,1:-1]+z[1:-1,:-2]+z[1:-1,2:])/4
    filled[hair_transfer]=mean[hair_transfer]
   F[hair_transfer]=np.rint(filled[hair_transfer]);alpha[hair_transfer]=1;B[hair_transfer]=sclera_estimate[hair_transfer]
   # The original registered blink exposes the real distal strand against
   # skin. Recut that tiny contour and follow the existing front-fringe pivot.
   closed=Image.fromarray(source.copy());closed.alpha_composite(Image.open(R/'artwork/blink_R.png').convert('RGBA'),(395,450))
   closed=np.array(closed)[oy:oy+h,ox:ox+w,:3].astype(float)
   local=(X>=453)&(X<=476)&(Y>=482)&(Y<=505)
   support=local&(strand_dist<=3.0)
   skin_known=local&~support&(closed[:,:,0]>220)&(closed[:,:,0]-closed[:,:,1]>22)
   si=distance_transform_edt(~skin_known,return_distances=False,return_indices=True)
   skin=gaussian_filter(closed[si[0],si[1]],sigma=(1.5,1.5,0))
   hair_color=np.array([104.,125.,108.])
   axis=skin-hair_color
   ta=np.clip(np.sum((skin-closed)*axis,axis=2)/np.maximum(np.sum(axis*axis,axis=2),1),0,1)*support
   ta[ta<.025]=0
   old=json.loads((I/'manifest.json').read_text())['objects']['hair_front_fringe']
   old_im=np.array(Image.open(I/old['file']))[:,:,3]/255
   old_a=np.zeros((h,w))
   for yy0 in range(h):
    for xx0 in range(w):
     hx=ox+xx0-old['xy'][0];hy=oy+yy0-old['xy'][1]
     if 0<=hy<old_im.shape[0] and 0<=hx<old_im.shape[1]:old_a[yy0,xx0]=old_im[hy,hx]
   ta=np.clip((ta-old_a)/np.maximum(1-old_a,1/255),0,1)
   ta[~support]=0
   save('hair_iris_crossing_screen_left.png',np.broadcast_to(hair_color,(h,w,3)).copy(),ta)
   manifest['foreground_objects']['hair_iris_crossing_screen_left']={'file':'../gaze_eyes/hair_iris_crossing_screen_left.png','xy':[ox,oy],'size':[w,h],'z':71,'pivot':old['pivot'],'hair_angle':old['hair_angle'],'source':'artwork/blink_R.png registered at (395,450)','source_sha256':sha(R/'artwork/blink_R.png'),'matte_rgb_is_inferred':True,'matte_color_estimate':[104,125,108],'estimated_pixels':True,'ownership':'Distal front-fringe strand recut from registered closed-source contour, inferred alpha against skin. Independent foreground hair, never gaze or eyelid owned.'}
  # Padding holds a complete inferred disk rather than a lash-truncated cap.
  px,py=PADDING;HH=h+2*py;WW=w+2*px;y2,x2=np.mgrid[:HH,:WW];AX=x2+ox-px;AY=y2+oy-py
  rr=np.sqrt(((AX-cx-tilt*(AY-cy))/rx)**2+((AY-cy)/ry)**2)
  full_alpha=np.clip((1-rr)*min(rx,ry)+.5,0,1)
  visible=np.zeros((HH,WW),bool);visible[py:py+h,px:px+w]=aperture
  observed=(alpha>.05)&original_aperture&~hair_transfer&~pale
  existing=np.zeros((HH,WW),bool);existing[py:py+h,px:px+w]=observed
  Image.fromarray((existing*255).astype(np.uint8)).save(O/f'observed_iris_{side}.png')
  Image.fromarray((hair_transfer*255).astype(np.uint8)).save(O/f'iris_under_hair_estimate_{side}.png')
  rgba=np.zeros((HH,WW,3));rgba[py:py+h,px:px+w]=F
  dist,ids=distance_transform_edt(~existing,return_distances=True,return_indices=True)
  nearest=rgba[ids[0],ids[1]].copy()
  # A compact inferred upper iris cap, with no extruded highlight or pupil.
  # Palette is measured from canonical dark amber, then darkened toward its
  # unseen upper rim. The completed <=4px band is the conservative filter footprint for local candidate gaze.
  safe=aperture&(alpha>.9)&(C[:,:,0]-C[:,:,1]>22)&(C[:,:,1]-C[:,:,2]>22)&(C[:,:,0]<180)
  palette=np.median(C[safe],axis=0)
  shade=np.clip((AY-(cy-ry))/ry,.20,1.0)
  inferred=palette[None,None,:]*shade[:,:,None]
  rgba[~existing]=inferred[~existing]
  near=(~existing)&(dist<=3)
  rgba[near]=nearest[near]
  # Complete the extra band that fractional GPU filtering actually reaches at
  # horizontal +/-4, up2/down1. This is NEW inferred artwork, not a wider mask.
  # Extrapolate the same iris's inward color slope, bounded to +/-24 levels,
  # and never brighten an unseen upper cap into a new highlight.
  vy=(y2-ids[0])/np.maximum(dist,1);vx=(x2-ids[1])/np.maximum(dist,1)
  inward=np.stack([map_coordinates(nearest[:,:,ch],[ids[0]-vy*2,ids[1]-vx*2],order=1,mode='nearest') for ch in range(3)],axis=2)
  slope=(nearest-inward)/2.0
  continued=np.clip(nearest+np.clip(slope*dist[:,:,None],-24,24),0,255)
  upward=AY<ids[0]+oy-py
  continued[upward]=np.minimum(continued[upward],nearest[upward])
  weight=np.clip(dist-3,0,1);weight=weight*weight*(3-2*weight)
  extra=(~visible)&(dist>3)&(dist<=4)&(full_alpha>0)
  blended=nearest*(1-weight[:,:,None])+continued*weight[:,:,None]
  rgba[extra]=blended[extra]
  annulus=(rr>.89)&~visible
  rgba[annulus]=ring
  full_alpha[py:py+h,px:px+w][aperture]=alpha[aperture]
  rgba[py:py+h,px:px+w][aperture]=F[aperture]
  full_alpha=np.rint(full_alpha*255)/255
  completed=(existing|((dist<=4)&(full_alpha>0)))
  completed[py:py+h,px:px+w] |= hair_transfer|pale
  Image.fromarray((completed*255).astype(np.uint8)).save(O/f'completed_iris_{side}.png')
  save(f'iris_{side}.png',rgba,full_alpha)
  save(f'sclera_{side}.png',B,aperture)
  Image.fromarray((aperture*255).astype(np.uint8)).save(O/f'aperture_{side}.png')
  Image.fromarray(((full_alpha>0)&~existing).astype(np.uint8)*255).save(O/f'iris_hidden_estimate_{side}.png')
  Image.fromarray((((alpha>0)&(alpha<1))|pale).astype(np.uint8)*255).save(O/f'iris_matte_estimate_{side}.png')
  Image.fromarray((((alpha>0)|pale)&aperture).astype(np.uint8)*255).save(O/f'sclera_hidden_estimate_{side}.png')
  Image.fromarray((extra*255).astype(np.uint8)).save(O/f'iris_extra_completion_{side}.png')
  comp=np.rint(F*alpha[:,:,None]+B*(1-alpha[:,:,None]));d=np.abs(comp-C)
  changed=np.any(d>0,axis=2)&aperture
  Image.fromarray((changed*255).astype(np.uint8)).save(O/f'visible_matte_change_{side}.png')
  assert np.array_equal(F[(alpha==1)&aperture&~hair_transfer],C[(alpha==1)&aperture&~hair_transfer]),"Opaque canonical iris core changed"
  manifest['eyes'][side]={'origin':[ox,oy],'size':[w,h], 'iris_origin':[ox-px,oy-py],'iris_size':[WW,HH],
   'ellipse_estimate':cfg['ellipse'],'iris_padding':PADDING,'completion_band_pixels':4,'extra_completion_pixels':int(extra.sum()),'extra_completion_method':'Bounded inward canonical color-slope extrapolation across the additionally required 3–4px hidden band; upward continuation cannot introduce a brighter highlight.','input_sha256':{f'{n}_{side}.png':sha(I/f'{n}_{side}.png') for n in ['iris','sclera','profile','lower_profile']},
   'observed_iris_mask':f'observed_iris_{side}.png','iris_under_hair_estimate_mask':f'iris_under_hair_estimate_{side}.png','hair_transfer_pixels':int(hair_transfer.sum()),'visible_iris_pixels':int((alpha>0).sum()),'matte_estimate_pixels':int((((alpha>0)&(alpha<1))|pale).sum()),
   'hidden_iris_estimate_pixels':int(((full_alpha>0)&~existing).sum()),'concealed_cap_estimate_pixels':int(((full_alpha>0)&~visible).sum()),'visible_inferred_iris_pixels':int(((full_alpha>0)&~existing&visible).sum()),'observed_iris_pixels':int(existing.sum()),'hidden_sclera_estimate_pixels':int((((alpha>0)|pale)&aperture).sum()),
   'comparison_scope':'Eye interior before foreground hair, against flattened source. Not whole rendered neutral; see GAZE_VALIDATION.md for actual GPU metrics.','interior_source_changed_pixels':int(changed.sum()),'interior_source_max_channel_error':int(d[aperture].max()),
   'estimated_files':[f'iris_hidden_estimate_{side}.png',f'iris_matte_estimate_{side}.png',f'sclera_hidden_estimate_{side}.png',f'iris_extra_completion_{side}.png',f'visible_matte_change_{side}.png']}
 (O/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(json.dumps({s:{k:v for k,v in e.items() if k.startswith('interior_') or k.endswith('_pixels')} for s,e in manifest['eyes'].items()},indent=2))
if __name__=='__main__':main()

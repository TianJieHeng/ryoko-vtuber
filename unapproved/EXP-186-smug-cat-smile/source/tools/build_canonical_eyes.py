#!/usr/bin/env python3
"""Local canonical pixel recut + alpha-only lid closure proof. Never edits source."""
from pathlib import Path
import argparse,json,hashlib
import numpy as np
from scipy.ndimage import distance_transform_edt
from PIL import Image,ImageDraw,ImageFilter
PROJECT=Path(__file__).resolve().parents[1]
P=PROJECT/'rig_assets/canonical_eyes';P.mkdir(parents=True,exist_ok=True)
DEFAULT=str(PROJECT/'artwork/bust_base.png')
CFG={
'screen_left':dict(rect=[410,469,533,529],pivot=[477,497],top=[(410,483),(424,480),(440,476),(452,477),(467,478),(480,480),(495,484),(510,491),(522,502),(533,511)],upper=[(410,485),(425,495),(432,491),(445,488),(460,487),(475,488),(490,490),(505,496),(520,505),(533,511)],lower=[(410,485),(425,497),(433,505),(448,513),(462,517),(477,519),(495,516),(508,511),(520,505),(533,511)]),
'screen_right':dict(rect=[607,468,719,526],pivot=[648,496],top=[(607,491),(620,485),(635,480),(650,477),(667,475),(680,476),(697,476),(711,481),(719,482)],upper=[(607,497),(619,494),(632,489),(648,487),(664,487),(680,489),(693,494),(704,494),(719,482)],lower=[(607,497),(619,504),(631,513),(648,517),(665,515),(680,509),(693,499),(704,494),(719,482)])}
def smooth(a,b,x):
 t=np.clip((x-a)/max(b-a,1e-8),0,1);return t*t*(3-2*t)
def save_rgba(name,rgb,alpha):
 rgb=np.array(rgb).astype('uint8').copy();alpha=np.asarray(alpha)
 # Nearest valid foreground RGB under zero alpha prevents bilinear/mipmap bleed.
 valid=alpha>0.1
 if valid.any():
  idx=distance_transform_edt(~valid,return_distances=False,return_indices=True);empty=alpha<=0;rgb[empty]=rgb[idx[0][empty],idx[1][empty]]
 out=np.dstack((rgb,np.clip(alpha*255,0,255).astype('uint8'))).astype('uint8');Image.fromarray(out).save(P/(name+'.png'))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source',default=DEFAULT);ap.add_argument('--hair-mask');ap.add_argument('--hair-composite');ap.add_argument('--hair-matte-mask');args=ap.parse_args()
 src=Image.open(args.source).convert('RGBA');a=np.array(src);H,W=a.shape[:2];yy,xx=np.mgrid[:H,:W]
 hair=np.array(Image.open(args.hair_mask).convert('L'))/255 if args.hair_mask else ((a[:,:,1].astype(float)>a[:,:,0]-3)&(a[:,:,2]>a[:,:,0]-20)).astype(float)
 hair_matte=np.array(Image.open(args.hair_matte_mask).convert('L'))>0 if args.hair_matte_mask else np.zeros((H,W),bool)
 eye_rect_mask=np.zeros((H,W),bool)
 for cfg in CFG.values():
  bx0,by0,bx1,by1=cfg['rect'];eye_rect_mask[by0:by1,bx0:bx1]=True
 hair_matte &= eye_rect_mask
 hair_composite=Image.open(args.hair_composite).convert('RGBA') if args.hair_composite else None
 # Conservative color-derived fallback identifies green hair only; replace with supplied ownership mask.
 if hair.shape!=(H,W):raise ValueError('hair mask must match source canvas')
 manifest={'canvas':[W,H],'source':'artwork/bust_base.png','source_sha256':hashlib.sha256(Path(args.source).read_bytes()).hexdigest(),'hair_mask_sha256':hashlib.sha256(Path(args.hair_mask).read_bytes()).hexdigest() if args.hair_mask else None,'objects':{},'eyes':{},'reconstruction':{'skin':'One coherent harmonic skin extension within the removed eye ownership and hair-matte mask. Hidden skin is estimated, never claimed original. Registered blink artwork supplies the closed lash, not disjoint skin patches.','lash_sweep':'Disabled rejected prototype. Active closure translates ONLY upper lash rigidly36px at full control, then spatially clips it against fixed lower aperture and reveals separately matted canonical closed lash. Core source RGB preserved; alpha edge matting and hidden strand-covered lash completion explicitly estimated.','iris':'Visible immutable source disk; hidden cap is not reconstructed and gaze is limited to zero until a verified hidden extension is supplied.','hair':'External mask' if args.hair_mask else 'Conservative RGB green-hair classifier, review before integration.'}}
 closed=src.copy()
 for fn,xy in [('blink_R.png',(395,450)),('blink_L.png',(585,450))]:closed.alpha_composite(Image.open(Path(args.source).parent/fn).convert('RGBA'),xy)
 closed=np.array(closed)
 manifest['closed_lash_sources']=[{'file':fn,'xy':list(xy),'sha256':hashlib.sha256((Path(args.source).parent/fn).read_bytes()).hexdigest()} for fn,xy in [('blink_R.png',(395,450)),('blink_L.png',(585,450))]]
 base=a.copy();allremove=np.zeros((H,W),bool);layers={};profiles={}
 for side,cfg in CFG.items():
  x0,y0,x1,y1=cfg['rect'];xs=np.arange(x0,x1);Y,X=np.mgrid[y0:y1,x0:x1];sh=Y.shape
  top=np.interp(xs,*np.array(cfg['top']).T)[None,:];up=np.interp(xs,*np.array(cfg['upper']).T)[None,:];lo=np.maximum(up,np.interp(xs,*np.array(cfg['lower']).T)[None,:]);
  # Skin/color estimate is fit only to visible warm skin, excluding hair, whites, iris, creases.
  sx0=max(0,x0-10);sx1=min(W,x1+10);sy0=y0-20;sy1=y1+28
  sy,sx=np.mgrid[sy0:sy1,sx0:sx1];sample=a[sy0:sy1,sx0:sx1,:3].astype(float)
  valid=(sample[:,:,0]>225)&(sample[:,:,1]>165)&(sample[:,:,1]<225)&(sample[:,:,2]>140)&(sample[:,:,0]-sample[:,:,1]>18)&(hair[sy0:sy1,sx0:sx1]<.1)
  valid &= ((sy<y0)|(sy>y1+1)|((sx>x1-1)&(sy>505)))
  def feats(x,y):
   x=(x-cfg['pivot'][0])/60;y=(y-500)/50;return np.stack([np.ones_like(x),x,y,x*x,x*y,y*y],axis=-1)
  coef=np.linalg.lstsq(feats(sx,sy)[valid],sample[valid],rcond=None)[0]
  skin=np.clip(feats(X,Y)@coef,[210,145,120],[255,230,215]).astype('uint8')
  rgb=a[y0:y1,x0:x1,:3]
  dark=(rgb[:,:,0].astype(float)<190)&(rgb[:,:,1].astype(float)<130)
  region=(Y>=top-2)&(Y<=lo+7)&(hair[y0:y1,x0:x1]<.5)
  fillregion=region|hair_matte[y0:y1,x0:x1]
  # All cuts own disjoint source pixels. This preserves exact compositing at neutral.
  upper=region&(Y<=up)
  lower=region&(Y>lo-2)&~upper
  interior=region&~upper&~lower
  cx,cy=cfg['pivot'];iris=interior&(((X-cx)/24)**2+((Y-(cy-5))/25)**2<=1)
  sclera=interior&~iris
  rgb=a[y0:y1,x0:x1,:3]
  crgb=closed[y0:y1,x0:x1,:3]
  close_top=np.interp(xs,*np.array(([(410,504),(430,502),(445,506),(465,511),(480,513),(495,510),(510,508),(529,514)] if side=='screen_left' else [(607,509),(620,508),(640,511),(660,512),(680,507),(697,501),(719,503)])).T)[None,:]
  close_bottom=np.interp(xs,*np.array(([(410,507),(430,511),(445,516),(465,521),(480,521),(495,519),(510,515),(529,515)] if side=='screen_left' else [(607,513),(620,516),(640,520),(660,522),(680,518),(697,511),(719,506)])).T)[None,:]
  closed_mask=(Y>=close_top-2)&(Y<=close_bottom+2)&(crgb[:,:,0]<185)&(crgb[:,:,1]<130)&(hair[y0:y1,x0:x1]<.5)
  closed_core=closed_mask.copy()
  closed_mask=(np.array(Image.fromarray((closed_mask*255).astype('uint8')).filter(ImageFilter.MaxFilter(5)))>0)&(hair[y0:y1,x0:x1]<.5)
  for col in range(x1-x0):
   ys=np.flatnonzero(closed_mask[:,col])
   if len(ys):close_top[0,col]=ys.min()+y0;close_bottom[0,col]=ys.max()+y0+1
  # Closed lash is matted against the reconstructed lid below, after skin exists.
  lash_core=upper&(rgb[:,:,0]<170)&(rgb[:,:,1]<115)
  upper_feature=upper&(rgb[:,:,0]<205)&(rgb[:,:,1]<155)
  upper_surround=upper&~upper_feature
  hidden_upper=(hair[y0:y1,x0:x1]>.5)&(Y>=top+1)&(Y<=up)
  upper_rgb=rgb.copy()
  for row in range(y1-y0):
   good=np.flatnonzero(upper_feature[row]&(rgb[row,:,0]<120)&(rgb[row,:,0].astype(float)>rgb[row,:,1].astype(float)+5))
   if len(good)>1:
    for ch in range(3):upper_rgb[row,:,ch][hidden_upper[row]]=np.interp(np.flatnonzero(hidden_upper[row]),good,rgb[row,good,ch])
   else:upper_rgb[row][hidden_upper[row]]=[20,11,7]
  local={'upper_lash':upper_feature,'upper_surround':upper_surround,'lower_contour':lower,'iris':iris,'sclera':sclera}
  # Harmonic extension from surrounding true skin, excluding the whole source eye.
  known=(sample[:,:,0]>170)&(sample[:,:,1]>110)&(sample[:,:,0]-sample[:,:,1]>18)&(hair[sy0:sy1,sx0:sx1]<.1)
  known[y0-sy0:y1-sy0,x0-sx0:x1-sx0][region]=False
  colors=np.clip(feats(sx,sy)@coef,[210,145,120],[255,230,215]);colors[known]=sample[known]
  for _ in range(600):
   q=np.pad(colors,((1,1),(1,1),(0,0)),mode='edge');mean=(q[:-2,1:-1]+q[2:,1:-1]+q[1:-1,:-2]+q[1:-1,2:])/4;colors[~known]=mean[~known]
  skin=colors[y0-sy0:y1-sy0,x0-sx0:x1-sx0].astype('uint8')
  clean_closed_skin=(crgb[:,:,0]>170)&(crgb[:,:,0].astype(float)-crgb[:,:,1].astype(float)>18)&~(np.array(Image.fromarray((closed_core*255).astype('uint8')).filter(ImageFilter.MaxFilter(7)))>0)
  closed_green=(crgb[:,:,1].astype(float)>crgb[:,:,0].astype(float)-5)&(crgb[:,:,2].astype(float)>crgb[:,:,0].astype(float)-15)&(crgb[:,:,1]>40)&(crgb[:,:,0]<230)
  clean_closed_skin &= ~(np.array(Image.fromarray((closed_green*255).astype('uint8')).filter(ImageFilter.MaxFilter(9)))>0)
  weight=smooth(20,45,crgb[:,:,0].astype(float)-crgb[:,:,1].astype(float))*smooth(170,220,crgb[:,:,0].astype(float))*clean_closed_skin
  # One harmonic skin field, no disjoint registered-skin islands.
  # The field is visible only within the existing removed-feature ownership mask.
  def matte(fg,bg,shape,core):
   sf=fg.astype(float);bf=bg.astype(float);ink=np.array([12.,6.,3.]);ratio=np.max((bf-sf)/np.maximum(bf-ink,1),axis=2)
   alpha=np.clip(ratio,0,1)*shape;alpha[core]=1
   alpha=np.rint(alpha*255)/255
   color=np.clip(np.rint((sf-bf*(1-alpha[:,:,None]))/np.maximum(alpha[:,:,None],1/255)),0,255).astype('uint8')
   return color,alpha
  outer=(X<=421) if side=='screen_left' else (X>=713)
  near_outer=(X<435) if side=='screen_left' else (X>705)
  closed_hair=(crgb[:,:,1].astype(float)>crgb[:,:,0].astype(float)+2)&(crgb[:,:,1]>45)
  hair_under_mask=fillregion&(outer|(near_outer&closed_hair))
  hair_under_rgb=crgb.copy()
  for col,xabs in enumerate(xs):
   line=a[max(0,y0-25):min(H,y1+25),xabs,:3].astype(float);yline=np.arange(max(0,y0-25),min(H,y1+25))
   known_green=(line[:,1]>line[:,0]+2)&(line[:,1]>line[:,2]+3)&(line[:,1]>45)
   if known_green.sum()>1:
    for ch in range(3):hair_under_rgb[:,col,ch]=np.interp(np.arange(y0,y1),yline[known_green],line[known_green,ch])
  hair_under_rgb[closed_hair]=crgb[closed_hair]
  save_rgba('hidden_hair_underlay_'+side,hair_under_rgb,hair_under_mask)
  Image.fromarray((hair_under_mask*255).astype('uint8')).save(P/('hidden_hair_underlay_'+side+'_estimate_mask.png'))
  matte_bg=skin.copy();matte_bg[hair_under_mask]=hair_under_rgb[hair_under_mask]
  incompatible=upper_feature&np.any(rgb.astype(float)>matte_bg.astype(float)+5,axis=2)&(rgb[:,:,0]>=100)
  upper_feature &= ~incompatible;upper_surround |= incompatible;local['upper_lash']=upper_feature;local['upper_surround']=upper_surround
  upper_rgb,upper_alpha=matte(upper_rgb,matte_bg,upper_feature|hidden_upper,(upper_feature&(rgb[:,:,0]<100))|hidden_upper)
  closed_rgb,closed_alpha=matte(crgb,skin,closed_mask,closed_mask&(crgb[:,:,0]<120))
  def constrain_ink(fg,alpha,original,bg,label):
   bad=(alpha>0)&((fg[:,:,1].astype(int)>fg[:,:,0].astype(int))|(fg[:,:,2].astype(int)>fg[:,:,1].astype(int)))
   ink=np.array([18.,9.,5.]);bf=bg.astype(float);sf=original.astype(float);axis=ink-bf
   fit=np.clip(np.sum((sf-bf)*axis,axis=2)/np.maximum(np.sum(axis*axis,axis=2),1),0,1)
   fg[bad]=ink.astype('uint8');alpha[bad]=np.rint(fit[bad]*255)/255
   Image.fromarray((bad*255).astype('uint8')).save(P/(label+'_'+side+'_inferred_ink_mask.png'))
   return fg,alpha
  upper_rgb,upper_alpha=constrain_ink(upper_rgb,upper_alpha,rgb,matte_bg,'upper_lash')
  closed_rgb,closed_alpha=constrain_ink(closed_rgb,closed_alpha,crgb,skin,'closed_lash')
  save_rgba('closed_lash_'+side,closed_rgb,closed_alpha)
  Image.fromarray((hidden_upper*255).astype('uint8')).save(P/('upper_lash_'+side+'_hidden_estimate_mask.png'))
  Image.fromarray(((upper_feature&(upper_alpha<1))*255).astype('uint8')).save(P/('upper_lash_'+side+'_estimated_matte.png'))
  Image.fromarray(((closed_mask&(closed_alpha<1))*255).astype('uint8')).save(P/('closed_lash_'+side+'_estimated_matte.png'))
  base[y0:y1,x0:x1,:3][fillregion]=skin[fillregion];allremove[y0:y1,x0:x1]|=fillregion
  # Source ownership/estimate masks stay alongside exported art.
  save_rgba('skin_'+side,skin,fillregion)
  sweep_rgb=np.zeros_like(rgb)
  for col in range(x1-x0):
   dk=(rgb[:,col,0]<75)&(rgb[:,col,1]<50)&upper[:,col]
   color=np.median(rgb[dk,col],axis=0) if dk.any() else np.array([20,11,7])
   sweep_rgb[:,col]=color
  save_rgba('lash_sweep_'+side,sweep_rgb,region)
  for name,m in local.items():
   save_rgba(name+'_'+side,upper_rgb if name=='upper_lash' else rgb,upper_alpha if name=='upper_lash' else m);Image.fromarray((m*255).astype('uint8')).save(P/(name+'_'+side+'_source_mask.png'))
  # R/G/B encode native y coordinates relative to crop; use nearest filtering.
  pro=np.zeros((*sh,4),'uint8');pro[:,:,0]=np.floor(up-y0);pro[:,:,1]=np.rint(close_bottom-y0);pro[:,:,2]=np.rint(top-y0);pro[:,:,3]=np.rint(close_top-y0)
  Image.fromarray(pro).save(P/('profile_'+side+'.png'))
  lp=np.zeros((*sh,4),'uint8');lp[:,:,0]=np.rint(lo-y0);lp[:,:,3]=255;Image.fromarray(lp).save(P/('lower_profile_'+side+'.png'))
  for name in [*local,'skin','lash_sweep','closed_lash','hidden_hair_underlay']:
   key=name+'_'+side;manifest['objects'][key]={'file':key+'.png','xy':[x0,y0],'rect':[x0,y0,x1-x0,y1-y0],'size':[x1-x0,y1-y0],'pivot':cfg['pivot'],'z':{'skin':30,'sclera':31,'iris':32,'lower_contour':33,'lash_sweep':34,'upper_lash':35,'upper_surround':34,'closed_lash':36,'hidden_hair_underlay':31}[name],'source_pixels':name in local or name=='closed_lash','estimated_pixels':name in ['skin','lash_sweep','upper_lash','closed_lash','hidden_hair_underlay'],'enabled':name!='lash_sweep'}
  manifest['objects']['hidden_hair_underlay_'+side]['owner']='temple_left' if side=='screen_left' else 'temple_right'
  manifest['objects']['hidden_hair_underlay_'+side]['pivot']=[425,407] if side=='screen_left' else [721,420]
  manifest['eyes'][side]={'profile':'profile_'+side+'.png','lower_profile':'lower_profile_'+side+'.png','origin':[x0,y0],'size':[x1-x0,y1-y0],'upper':cfg['upper'],'lower':cfg['lower'],'top':cfg['top'],'shader_roles':{'sclera':0,'iris':0,'upper_lash':1,'lower_contour':2,'lash_sweep':3,'closed_lash':4,'upper_surround':5},'gaze_supported':False,'upper_rigid_travel_y':36,'upper_surround_static':True}
  layers[side]=(rgb,skin,region,local,upper_rgb,hidden_upper,upper_alpha,hair_under_rgb,hair_under_mask);profiles[side]=(np.rint(top),np.floor(up),np.rint(lo),Y,np.rint(close_top),np.rint(close_bottom),closed_rgb,closed_alpha,sweep_rgb)
 Image.fromarray(base).save(P/'eye_clean_base.png');Image.fromarray((allremove*255).astype('uint8')).save(P/'eye_removal_mask.png');Image.fromarray((hair*255).astype('uint8')).save(P/'hair_exclusion_used.png')
 # Canonical brows: green feature pixels only, never a rectangular skin crop.
 brows=[]
 browcfg=[('screen_left',(460,442,540,479),[(463,448),(482,450),(505,457),(520,466),(537,477),(520,473),(497,466),(477,460),(463,457)]),('screen_right',(601,440,658,474),[(605,460),(618,453),(637,447),(651,445),(654,454),(638,458),(620,466),(605,472)])]
 browremove=np.zeros((H,W),bool);browbase=base.copy()
 for side,(x0,y0,x1,y1),points in browcfg:
  rgb=a[y0:y1,x0:x1,:3];bh,bw=rgb.shape[:2]
  pm=Image.new('L',(bw,bh));ImageDraw.Draw(pm).polygon([(x-x0,y-y0) for x,y in points],fill=255)
  rf=rgb.astype(float)
  broad=np.array(pm.filter(ImageFilter.MaxFilter(9)))>0
  seed=broad&(rf[:,:,0]-rf[:,:,1]<30)&(rf[:,:,0]-rf[:,:,2]<60)&(hair[y0:y1,x0:x1]<.5)
  vicinity=np.array(Image.fromarray((seed*255).astype('uint8')).filter(ImageFilter.MaxFilter(5)))>0
  mask=broad&vicinity&(rf[:,:,0]-rf[:,:,1]<44)&(rf[:,:,0]-rf[:,:,2]<80)&(hair[y0:y1,x0:x1]<.5)
  colors=rgb.astype(float);known=~mask&(rf[:,:,0]>rf[:,:,1]+25)&(rf[:,:,0]>215)&(hair[y0:y1,x0:x1]<.5);colors[~known]=[250,203,180]
  for _ in range(700):
   q=np.pad(colors,((1,1),(1,1),(0,0)),mode='edge');mean=(q[:-2,1:-1]+q[2:,1:-1]+q[1:-1,:-2]+q[1:-1,2:])/4;colors[~known]=mean[~known]
  colors=np.rint(colors).astype('uint8');bf=colors.astype(float)
  core=mask&(rf[:,:,0]-rf[:,:,1]<15)
  ink=np.median(rf[core],axis=0) if core.any() else np.array([145,170,150])
  alpha=np.clip(np.max((bf-rf)/np.maximum(bf-ink,1),axis=2),0,1)*mask
  alpha=np.maximum(alpha,np.clip(np.max((rf-bf)/np.maximum(255-bf,1),axis=2),0,1)*mask)
  alpha[core]=1;alpha=np.rint(alpha*255)/255
  fg=np.clip(np.rint((rf-bf*(1-alpha[:,:,None]))/np.maximum(alpha[:,:,None],1/255)),0,255).astype('uint8')
  key='brow_'+side;save_rgba(key,fg,alpha);save_rgba('brow_skin_'+side,colors,mask)
  Image.fromarray((mask*255).astype('uint8')).save(P/(key+'_ownership_mask.png'))
  Image.fromarray(((mask&~core)*255).astype('uint8')).save(P/(key+'_estimated_matte_mask.png'))
  browremove[y0:y1,x0:x1]|=mask;browbase[y0:y1,x0:x1,:3][mask]=colors[mask]
  manifest['objects'][key]={'file':key+'.png','xy':[x0,y0],'size':[bw,bh],'rect':[x0,y0,bw,bh],'pivot':[(x0+x1)/2,(y0+y1)/2],'z':40,'source_pixels':True,'estimated_pixels':True}
  manifest['objects']['brow_skin_'+side]={'file':'brow_skin_'+side+'.png','xy':[x0,y0],'size':[bw,bh],'rect':[x0,y0,bw,bh],'pivot':[(x0+x1)/2,(y0+y1)/2],'z':30,'source_pixels':False,'estimated_pixels':True}
 Image.fromarray(browbase).save(P/'eye_brow_clean_base.png');Image.fromarray((browremove*255).astype('uint8')).save(P/'brow_removal_mask.png')
 # CPU mirror of shader, source-over; preview only, not replacement facial art.
 def render(c,use_matte=True):
  out=base.copy()
  for side,cfg in CFG.items():
   x0,y0,x1,y1=cfg['rect'];rgb,skin,region,local,urgb,hupper,ualpha,hair_under_rgb,hair_under_mask=layers[side];top,up,lo,Y,ct,cb,crgb,cm,srgb=profiles[side]
   edge=up+36*c
   view=out[y0:y1,x0:x1,:3].astype(float)
   view[hair_under_mask]=hair_under_rgb[hair_under_mask]
   interior=smooth(-.5,.5,Y-(np.floor(up)+36*c))
   for key in ['upper_surround','sclera','iris','lower_contour','upper_lash','closed_lash']:
    if key=='upper_surround':
     threshold=top-3+(up-top+4)*min(c/.15,1)
     mask=local[key]*smooth(-.5,.5,Y-threshold);color=rgb
    elif key in ['sclera','iris']:mask=local[key]*interior;color=rgb
    elif key=='lower_contour':mask=local[key]*(1-smooth(0,1,Y-(np.rint(lo)+7-max(0,(c-.65)/.35)*24)));color=rgb
    elif key=='lash_sweep':
     xt=np.arange(x0,x1)[None,:]
     tip=(1-smooth(495,523,xt)) if side=='screen_left' else smooth(607,632,xt)
     thick=(6.0*(1-c)+(cb-ct)*c)*tip
     end=520 if side=='screen_left' else 713
     taper=1-smooth(end-4,end,np.arange(x0,x1)[None,:])
     mask=region*taper*(1-smooth(-.5,.5,Y-ct))*smooth(-.5,.5,Y-(edge-thick))*(1-smooth(-.5,.5,Y-edge))*(Y<=up if c==0 else 1);color=srgb
    elif key=='closed_lash':
     xt=np.arange(x0,x1)[None,:]
     tip=(1-smooth(495,523,xt)) if side=='screen_left' else smooth(607,632,xt)
     thick=(6.0*(1-c)+(cb-ct)*c)*tip
     threshold=cb+2-min(1,max(0,(c-.55)/.3))*(cb-ct+4)
     mask=cm*smooth(-.5,.5,Y-threshold);color=crgb
    else:
     # Spatial top-down removal. At 20% closure original upper lash has gone.
     threshold=top-3+(up-top+5)*min(1,max(0,(c-.65)/.2))
     am=ualpha*smooth(-.5,.5,Y-threshold)
     sprite=Image.fromarray(np.dstack((urgb,(am*255).astype('uint8'))))
     sprite=sprite.transform(sprite.size,Image.Transform.AFFINE,(1,0,0,0,1,-c*36),Image.Resampling.BILINEAR)
     moved=np.array(sprite);mask=moved[:,:,3]/255.0;color=moved[:,:,:3]
     mask*=1-smooth(-.5,.5,Y-(lo+1))
    view=view*(1-mask[:,:,None])+color*mask[:,:,None]
   out[y0:y1,x0:x1,:3]=np.rint(view).astype('uint8')
  if use_matte and hair_composite is not None:
   keep=(hair>.5)&~hair_matte;out[keep]=a[keep]
   composite=np.array(Image.alpha_composite(Image.fromarray(out),hair_composite));out[hair_matte]=composite[hair_matte]
   return Image.fromarray(out)
  out[hair>.5]=a[hair>.5]
  return Image.fromarray(out)
 frames=[]
 for name,c in [('neutral',0),('quarter',.25),('mid',.5),('three_quarter',.75),('closed',1),('reopen',0)]:
  im=render(c);im.save(P/(name+'.png'));crop=im.crop((400,460,730,535)).resize((990,225));panel=Image.new('RGB',(990,250),'#dddddd');panel.paste(crop,(0,25));ImageDraw.Draw(panel).text((8,6),name+' closure='+str(c),fill='black');frames.append(panel)
 sheet=Image.new('RGB',(990,250*len(frames)));[sheet.paste(im,(0,250*i)) for i,im in enumerate(frames)];sheet.save(P/'closure_comparison.png')
 native=Image.new('RGB',(660,95*3),'#dddddd')
 for j,name in enumerate(['neutral','quarter','mid','three_quarter','closed','reopen']):
  crop=Image.open(P/(name+'.png')).crop((400,460,730,535));x=(j%2)*330;y=(j//2)*95;native.paste(crop,(x,y+20));ImageDraw.Draw(native).text((x+4,y+4),name,fill='black')
 native.save(P/'closure_native_scale.png')
 rawneutral=np.array(render(0,False));rawdiff=np.abs(rawneutral.astype(int)-a.astype(int));Image.fromarray(rawneutral).save(P/'eye_only_neutral_raw_hair.png')
 neutral=np.array(render(0));diff=np.abs(neutral.astype(int)-a.astype(int));manifest['validation']={'eye_only_neutral_max_error':int(rawdiff.max()),'eye_only_neutral_changed_pixels':int(np.any(rawdiff,axis=2).sum()),'neutral_changed_pixels':int(np.any(diff,axis=2).sum()),'neutral_max_channel_error':int(diff.max()),'reopen_exact':bool(np.array_equal(np.array(render(0)),neutral)),'neutral_region_ownership_exact':bool(all(np.array_equal(sum(m.astype(int) for m in z[3].values()),z[2].astype(int)) for z in layers.values()))}
 (P/'manifest.json').write_text(json.dumps(manifest,indent=2));print(json.dumps(manifest['validation']))
if __name__=='__main__':main()

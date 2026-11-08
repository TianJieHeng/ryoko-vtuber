#!/usr/bin/env python3
"""Replace ambiguous flattened brow/hair crossing pixels with bounded continuation.
This is estimated artwork, not recovered clean source. Does not modify shared inputs.
"""
from pathlib import Path
import json,argparse
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import map_coordinates,distance_transform_edt
from build_brow_d import reconstruct_brow_skin,SRC,HAIR,EYES,P
O=P/'continuation_v2'
CONFIG={'screen_left': {'box': (418, 440, 468, 466), 'polygon': [(423, 444), (463, 444), (465, 461), (424, 461)], 'anchor_y': [442, 464], 'dx_per_y': 0.12, 'top_landmarks': [418, 434, 440, 444, 448, 454, 458, 460, 462, 468], 'bottom_landmarks': [418, 430, 436, 446, 450, 456, 460, 462, 464, 468]}, 'screen_right': {'box': (635, 435, 666, 464), 'polygon': [(640, 441), (652, 441), (661, 455), (655, 460), (644, 449)], 'anchor_y': [438, 462], 'dx_per_y': 0.8}, 'screen_right_inner': {'box': (598, 452, 614, 477), 'polygon': [(600, 454), (614, 454), (614, 475), (604, 475)], 'anchor_y': [450, 478], 'dx_per_y': 0.3}}
def smooth(a,b,x):
 t=np.clip((x-a)/(b-a),0,1);return t*t*(3-2*t)
def save_rgba(path,rgb,alpha):
 rgb=np.clip(np.rint(rgb),0,255).astype('uint8');al=np.clip(np.rint(alpha*255),0,255).astype('uint8')
 valid=al>25
 if valid.any():
  inds=distance_transform_edt(~valid,return_distances=False,return_indices=True);zero=al==0;rgb[zero]=rgb[inds[0][zero],inds[1][zero]]
 Image.fromarray(np.dstack((rgb,al))).save(path)
def main():
 global P,O,SRC,HAIR
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--source',type=Path,default=SRC)
 parser.add_argument('--hair-mask',type=Path,default=HAIR)
 parser.add_argument('--brow-dir',type=Path,default=P,help='Brow D output directory including manifest and matte assets.')
 parser.add_argument('--output-dir',type=Path,default=None)
 args=parser.parse_args();SRC=args.source;HAIR=args.hair_mask;P=args.brow_dir;O=args.output_dir or P/'continuation_v2';O.mkdir(parents=True,exist_ok=True)
 src=np.array(Image.open(SRC).convert('RGBA'));H,W=src.shape[:2];hair=np.array(Image.open(HAIR).convert('L'))>0
 dm=json.loads((P/'manifest.json').read_text());fullbrow=np.zeros((H,W),bool)
 for side,e in dm['objects'].items():
  x,y=e['xy'];w,h=e['size'];fullbrow[y:y+h,x:x+w]|=np.array(Image.open(P/e['full_feature_ownership']))>0
 patch_union=np.zeros((H,W),bool);layers={};report={'status':'Estimated same-strand continuation; previous97 source transfers are superseded. Original source contains mixed/baked brow pixels in these intervals, not clean hair.','source':'artwork/bust_base.png','patches':{},'ownership_rule':'For every correction-mask pixel: remove old raw source from hair/brow/backing; stationary_skin is face-owned backing, hair_continuation is front_fringe-owned foreground with pivot529,218. Do not redraw old97 source transfer assets or original hair within these masks.'}
 for side,c in CONFIG.items():
  x0,y0,x1,y1=c['box'];Y,X=np.mgrid[y0:y1,x0:x1];raw=src[y0:y1,x0:x1,:3].astype(float)
  maskim=Image.new('L',(x1-x0,y1-y0));ImageDraw.Draw(maskim).polygon([(x-x0,y-y0) for x,y in c['polygon']],fill=255);mask=np.array(maskim)>0
  unknown=fullbrow.copy();unknown[y0:y1,x0:x1]|=mask
  skin,_,_,_=reconstruct_brow_skin(src,unknown,hair,c['box'],side,margin=30);skin=skin.astype(float)
  ya,yb=c['anchor_y'];flow=c['dx_per_y'];samples=[]
  for anchor in [ya,yb]:
   row_samples=[]
   for offset in [-1,0,1]:
    sy=np.full(Y.shape,float(anchor+offset))
    if 'top_landmarks' in c:
     ta=np.array(c['top_landmarks']);ba=np.array(c['bottom_landmarks']);sx=np.zeros(X.shape,float)
     for row in range(Y.shape[0]):
      ty=np.clip((Y[row,0]-ya)/(yb-ya),0,1);mid=ta*(1-ty)+ba*ty
      sx[row]=np.interp(X[row],mid,ta if anchor==ya else ba)+offset*(ba-ta).mean()/(yb-ya)
    else:sx=X+flow*(sy-Y)
    row_samples.append(np.stack([map_coordinates(src[:,:,ch].astype(float),[sy,sx],order=1,mode='nearest') for ch in range(3)],axis=2))
   samples.append(np.median(row_samples,axis=0))
  t=np.clip((Y-ya)/(yb-ya),0,1)[:,:,None];continued=samples[0]*(1-t)+samples[1]*t
  feather=np.minimum(distance_transform_edt(mask)/2,1)[:,:,None]
  reconstructed=continued*feather+raw*(1-feather)
  # Explicitly split clean background gaps from green foreground strands.
  delta_rg=reconstructed[:,:,0]-reconstructed[:,:,1];delta_rb=reconstructed[:,:,0]-reconstructed[:,:,2]
  alpha=(1-smooth(8,32,delta_rg))*(1-smooth(25,62,delta_rb))*mask
  pure_skin=mask&(alpha<0.02)
  skin[pure_skin]=reconstructed[pure_skin]
  fg=np.clip((reconstructed-skin*(1-alpha[:,:,None]))/np.maximum(alpha[:,:,None],1/255),0,255)
  # No warm gap pixels can become opaque foreground hair.
  save_rgba(O/f'hair_continuation_{side}.png',fg,alpha)
  save_rgba(O/f'stationary_skin_{side}.png',skin,mask.astype(float))
  Image.fromarray((mask*255).astype('uint8')).save(O/f'crossing_correction_mask_{side}.png')
  Image.fromarray(np.clip(np.rint(continued),0,255).astype('uint8')).save(O/f'same_strand_estimate_{side}.png')
  patch_union[y0:y1,x0:x1]|=mask;layers[side]=(c['box'],skin,mask,fg,alpha)
  report['patches'][side]={'xy':[x0,y0],'size':[x1-x0,y1-y0],'missing_clean_art_polygon':c['polygon'],'missing_clean_art_y_interval':[min(y for x,y in c['polygon']),max(y for x,y in c['polygon'])],'missing_clean_art_pixels':int(mask.sum()),'sampling':'Median of3 source rows at each anchor, bilinear along the traced strand direction; linear continuation between anchors;2px boundary feather only outside contaminated core.','anchor_rows':[[ya-1,ya,ya+1],[yb-1,yb,yb+1]],'dx_per_y':flow,'same_strand_landmarks_top':c.get('top_landmarks'),'same_strand_landmarks_bottom':c.get('bottom_landmarks'),'hair_file':f'hair_continuation_{side}.png','skin_file':f'stationary_skin_{side}.png','mask':f'crossing_correction_mask_{side}.png','hair_owner':'front_fringe','hair_pivot':[529,218],'hair_z':90,'pixels_hair_alpha_gt_0':int((alpha>0).sum()),'pixels_pure_skin':int(pure_skin.sum())}
 # Proof makes transfer order explicit. Original mixed pixels never render over estimates.
 base=Image.fromarray(src)
 for side,e in dm['objects'].items():base.alpha_composite(Image.open(P/e['skin']),e['xy'])
 for side,(box,skin,mask,fg,alpha) in layers.items():base.alpha_composite(Image.open(O/f'stationary_skin_{side}.png'),box[:2])
 states={}
 for name,show_brow,offset,show_hair in [('hidden_brows',False,0,True),('raised_brows',True,-10,True),('neutral_estimated',True,0,True),('both_hidden_in_correction',False,0,False)]:
  im=base.copy()
  if show_brow:
   for side,e in dm['objects'].items():
    brow=np.array(Image.open(P/e['brow']));bx,by=e['xy'];bh,bw=brow.shape[:2]
    brow[patch_union[by:by+bh,bx:bx+bw],3]=0
    im.alpha_composite(Image.fromarray(brow),(bx,by+offset))
  ar=np.array(im);restore=hair&~patch_union;ar[restore]=src[restore];im=Image.fromarray(ar)
  if show_hair:
   for side,(box,skin,mask,fg,alpha) in layers.items():im.alpha_composite(Image.open(O/f'hair_continuation_{side}.png'),box[:2])
  im.save(O/f'{name}.png');states[name]=im
 # Canonical reference + clear ownership proofs.
 panels=[('canonical reference',Image.fromarray(src)),('brows hidden; estimated clean strand continuation',states['hidden_brows']),('brows raised10px; foreground hair remains',states['raised_brows']),('brows and hair hidden INSIDE correction mask',states['both_hidden_in_correction']),('estimated neutral (not exact-source claim)',states['neutral_estimated'])]
 sheet=Image.new('RGB',(1050,750),'#ddd');draw=ImageDraw.Draw(sheet)
 for i,(label,im) in enumerate(panels):sheet.paste(im.crop((400,430,750,473)).resize((1050,129)),(0,i*150+21));draw.text((5,i*150+4),label,fill='black')
 sheet.save(O/'ownership_hide_proof_3x.png')
 d=np.abs(np.array(states['neutral_estimated']).astype(int)-src.astype(int));changed=np.any(d,axis=2)
 report['validation']={'estimated_neutral_changed_pixels':int(changed.sum()),'estimated_neutral_max_channel_error':int(d.max()),'estimated_neutral_changes_outside_correction_mask':int((changed&~patch_union).sum()),'source_art_claim':'No clean original source pixels exist for the flattened mixed crossing intervals. Continuation is explicitly estimated, not original recovered artwork.'}
 Image.fromarray((patch_union*255).astype('uint8')).save(O/'crossing_correction_mask_full.png');(O/'manifest.json').write_text(json.dumps(report,indent=2));print(json.dumps(report['validation']))
if __name__=='__main__':main()

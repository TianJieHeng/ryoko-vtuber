"""Separate only the two rigid hanging earrings; never overwrite source artwork.

Coordinates are source pixels, screen sides, positive y down. The first hanging
link is the pivot; upper stud and connecting stem stay baked into the face.
Underpaint carries real RGBA. Packed red/green clear channels control replacement.
"""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage as ndi
ROOT=Path(__file__).resolve().parents[1]; REPO=ROOT.parent
OUT=ROOT/'rig_assets'; REVIEW=REPO/'review'; VALID=REPO/'output'
for d in (OUT,REVIEW,VALID): d.mkdir(exist_ok=True)
originals=sorted(p for p in ROOT.rglob('*.png') if not p.name.startswith('earring_'))
def hashes(): return {str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest() for p in originals}
before=hashes(); src=np.array(Image.open(ROOT/'artwork/bust_base.png').convert('RGBA'))
h,w=src.shape[:2]
configs=[('screen_left',(395,600,424,737),(409,602)),('screen_right',(702,598,731,737),(716,600))]
manifest={'canvas':[w,h],'coordinate_system':'source pixels; screen sides; x right, y down','pivot_contract':'Rotate each full-canvas earring about pivot; fixed stud above source_rect remains in base. Clear base with the packed red/green mask then insert RGBA underpaint before transformed cutout. Neutral may bypass derivatives for exact source.','layers':{}}
stats={}; masks={}; underpaints={}
for side,box,pivot in configs:
 x0,y0,x1,y1=box; rgb=src[y0:y1,x0:x1,:3].astype(float)
 seed=(rgb[:,:,0]-rgb[:,:,1]>8)&(rgb[:,:,0]-rgb[:,:,2]>20)
 # Keep the largest connected gold object, excluding nearby skin flecks.
 labs,n=ndi.label(seed); sizes=np.bincount(labs.ravel());sizes[0]=0
 seed=labs==sizes.argmax()
 # Two source pixel margin captures dark ink/antialiasing without broad hair cuts.
 local=ndi.distance_transform_edt(~seed)<=2.5
 # No upward expansion into fixed studs.
 mask=np.zeros((h,w),np.uint8);mask[y0:y1,x0:x1]=local*255
 # Initialize the harmonic fill from adjacent original hair / transparent air.
 # Work premultiplied so transparent source RGB never creates colored fringes.
 bg=src.astype(float); pm=bg[:,:,:3]*(bg[:,:,3:4]/255)
 filled=bg.copy();filled[:,:,:3]=pm
 for y in range(y0,y1):
  xs=np.flatnonzero(mask[y]);
  if not len(xs):continue
  a,b=xs[0],xs[-1]
  # Two-pixel samples outside the clearing silhouette retain original hair tones.
  l=np.mean(filled[y,max(0,a-3):a-1],axis=0);r=np.mean(filled[y,b+2:min(w,b+4)],axis=0)
  for x in xs:
   t=(x-a+1)/(b-a+2);filled[y,x]=l*(1-t)+r*t
 # Harmonic relaxation removes row interpolation bands while respecting each
 # neighboring source pixel. RGBA remains premultiplied during reconstruction.
 z=filled[y0:y1,x0:x1].copy()
 for _ in range(1100):
  padded=np.pad(z,((1,1),(1,1),(0,0)),mode='edge')
  avg=(padded[:-2,1:-1]+padded[2:,1:-1]+padded[1:-1,:-2]+padded[1:-1,2:])/4
  z[local]=avg[local]
 filled[y0:y1,x0:x1]=z
 alpha=filled[:,:,3:4]/255
 filled[:,:,:3]=np.divide(filled[:,:,:3],alpha,out=np.zeros_like(filled[:,:,:3]),where=alpha>0)
 under=np.zeros_like(src);under[mask>0]=np.clip(np.rint(filled[mask>0]),0,255).astype(np.uint8)
 cut=np.zeros_like(src);cut[mask>0]=src[mask>0]
 Image.fromarray(cut).save(OUT/f'earring_{side}.png')
 underpaints[side]=under; masks[side]=mask
 cleared=src.copy();cleared[mask>0]=under[mask>0]
 restored=np.array(Image.alpha_composite(Image.fromarray(cleared),Image.fromarray(cut)))
 delta=np.abs(restored.astype(int)-src.astype(int));active=mask>0
 yy,xx=np.nonzero(mask);rect=[int(xx.min()),int(yy.min()),int(xx.max()-xx.min()+1),int(yy.max()-yy.min()+1)]
 manifest['layers'][side]={'source_rect':rect,'pivot':list(pivot),'cutout':f'earring_{side}.png','mask_channel':'r' if side=='screen_left' else 'g'}
 premul=lambda a: a[:,:,:3].astype(float)*(a[:,:,3:4]/255)
 visible_delta=np.abs(premul(restored)-premul(src))
 stats[side]={'neutral_premultiplied_rgb_max_error':float(visible_delta.max()),'neutral_premultiplied_rgb_mean_error_in_mask':float(visible_delta[active].mean()),'source_pixels_outside_mask_unchanged':bool(np.array_equal(cleared[~active],src[~active])),'mask_pixels':int(active.sum()),'source_rect':rect,'pivot':list(pivot),'neutral_rgba_max_error':int(delta.max()),'neutral_rgba_changed_pixels':int(np.any(delta>0,axis=2).sum()),'neutral_rgba_mean_absolute_error_in_mask':float(delta[active].mean()),'original_nonopaque_pixels_in_mask':int(np.sum(src[:,:,3][active]<255)),'fixed_stud_pixels_modified':0}
 crop=(x0-15,570,x1+15,755);scale=3
 sheet=Image.new('RGB',(5*(crop[2]-crop[0])*scale, (crop[3]-crop[1])*scale+25),(58,62,65));draw=ImageDraw.Draw(sheet)
 variants=[('source',Image.fromarray(src)),('cleared',Image.fromarray(cleared)),('restored',Image.fromarray(restored))]
 for deg in [-6,6]:
  moved=Image.fromarray(cut).rotate(deg,Image.Resampling.BICUBIC,center=pivot)
  variants.append((f'{deg:+} deg',Image.alpha_composite(Image.fromarray(cleared),moved)))
 for i,(label,im) in enumerate(variants):
  small=Image.new('RGBA',(crop[2]-crop[0],crop[3]-crop[1]),(58,62,65,255));small.alpha_composite(im.crop(crop));sheet.paste(small.convert('RGB').resize((small.width*scale,small.height*scale)),(i*small.width*scale,25));draw.text((i*small.width*scale+4,5),label,fill='white')
 sheet.save(REVIEW/f'earring_{side}_review.png')
 maskim=Image.fromarray(mask).crop(crop).resize(((crop[2]-crop[0])*3,(crop[3]-crop[1])*3));maskim.save(REVIEW/f'earring_{side}_mask.png')
assert before==hashes(), 'Original PNG changed during layer generation'
assert len(before)==606, f'Expected 606 original PNGs; got {len(before)}'
left=masks['screen_left'];right=masks['screen_right']
assert not np.any((left>0)&(right>0)), 'Left/right masks overlap'
assert not np.any(left[:600]) and not np.any(right[:598]), 'Fixed upper studs changed'
packed_under=underpaints['screen_left']+underpaints['screen_right']
packed_masks=np.zeros((h,w,3),np.uint8);packed_masks[:,:,0]=left;packed_masks[:,:,1]=right
Image.fromarray(packed_under).save(OUT/'earring_underpaint.png')
Image.fromarray(packed_masks).save(OUT/'earring_clear_masks.png')
manifest['underpaint']='earring_underpaint.png';manifest['clear_masks']='earring_clear_masks.png'
(OUT/'earring_layers.json').write_text(json.dumps(manifest,indent=2)+'\n')
after=hashes();report={'source_png_count_checked':len(before),'original_png_hashes_unchanged':before==after,'source_sha256':before['project/artwork/bust_base.png'],'layers':stats,'limitations':['Underpaint is local premultiplied RGBA harmonic interpolation, not recovered original hidden hair. Small smooth fill regions can be seen in enlarged cleared crops.','Cutouts retain a restrained two-pixel source fringe and tiny original hair islands within links. At large enlargement these can move with the rigid earring.','Neutral derivative composition is not guaranteed source-exact where original edge alpha is fractional; runtime should bypass derivatives at zero relative sway.'],'original_png_sha256':before}
(VALID/'earring_asset_validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='original_png_sha256'},indent=2))

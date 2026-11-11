#!/usr/bin/env python3
"""Independent source-part jacket study. No reference pixels are used as artwork."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.interpolate import PchipInterpolator
from scipy.ndimage import map_coordinates
HERE=Path(__file__).resolve().parent;RIG=HERE.parents[1];REPO=RIG.parent
CANVAS=(1024,1536)
manifest=json.loads((RIG/'full_body/registration.json').read_text())
frame=json.loads((RIG/'full_body/review/transform_samples.json').read_text())['frames'][0]

def place(c,src,v):
 a,b,cc,d,x,y=v;m=np.array([[a,cc,x],[b,d,y],[0,0,1.]])
 inv=np.linalg.inv(m);c.alpha_composite(src.transform(c.size,Image.Transform.AFFINE,tuple(inv[:2].flatten()),Image.Resampling.BICUBIC))

def clean(path):
 a=np.array(Image.open(path).convert('RGBA'));a[a[:,:,3]<=10,3]=0;return a
# Existing painted fold seam defines exterior front / interior facing ownership.
fold_R=np.array([[20,345],[60,340],[120,343],[175,344],[235,349],[285,357],[345,371],[409,392],[465,419],[541,451],[584,446],[650,430],[722,406],[798,381],[863,365]])
fold_L=np.array([[20,245],[60,249],[120,244],[175,242],[235,233],[285,221],[345,204],[409,180],[465,150],[541,117],[584,122],[650,139],[722,163],[798,188],[863,209]])
# Front silhouette landmarks derived by visual registration, in canvas pixels.
# The L/R mirror preserves the two independently painted sources, not mirrored art.
ty=np.array([265,273,281,289,320,360,400,440,480,516,540,570,600,630,660,674,689.])
outer=np.array([454,434,407,363,368,379,385,400,411,423,418,407,390,378,364,400,455.])+8
inner=np.array([454,454,453,452,450,448,452,467,489,511,502,493,483,474,464,459,455.])+8
# Keep the actual button inside the join, rather than forcing both painted edges to coincide.
inner[9]=517
srcy=np.array([24,116,200,300,400,546,650,770,861.]);dsty=np.array([265,289,332,382,437,516,590,660,689.])
art={};records=[]
for side,fold in [('R',fold_R),('L',fold_L)]:
 path=REPO/f'avatar_build_assets/body/layers/blazer_front_character_{side}.png';a=clean(path);h,w=a.shape[:2]
 yy,xx=np.indices((h,w));edge=PchipInterpolator(fold[:,0],fold[:,1])(np.clip(yy,20,863))
 visible=(xx<=edge) if side=='R' else (xx>=edge)
 exterior=a.copy();exterior[~visible,3]=0
 if side=='R':
  button_mask=(xx-450)**2+(yy-546)**2<=19**2
  button_source=a.copy();button_source[~button_mask,3]=0
  button_im=Image.fromarray(button_source).crop((431,527,470,566));button_im.save(HERE/'blazer_button_candidate.png')
  exterior[button_mask,3]=0
  art['blazer_button']=(button_im,[.48,0,0,.48,499,507])
 facing=a.copy();facing[visible,3]=0
 Image.fromarray(exterior).save(HERE/f'blazer_{side}_exterior_source.png');Image.fromarray(facing).save(HERE/f'blazer_{side}_facing_not_instantiated.png')
 # Exact alpha contour on cleaned source. Smooth only near subpixel top/bottom tips.
 opaque=exterior[:,:,3]>10; valid=np.flatnonzero(opaque.any(axis=1))
 outside=np.array([np.flatnonzero(opaque[y])[0 if side=='R' else -1] for y in valid])
 y,x=np.indices((470,350),dtype=float); y+=250;x+=337 if side=='R' else 512
 sy=PchipInterpolator(dsty,srcy,extrapolate=False)(np.clip(y,265,689))
 src_outer=np.interp(sy,valid,outside);src_inner=PchipInterpolator(fold[:,0],fold[:,1])(sy)
 dst_outer=PchipInterpolator(ty,outer)(np.clip(y,265,689));dst_inner=PchipInterpolator(ty,inner)(np.clip(y,265,689))
 if side=='L':dst_outer=1024-dst_outer;dst_inner=1024-dst_inner
 denom=dst_inner-dst_outer
 u=np.divide(x-dst_outer,denom,out=np.zeros_like(x),where=abs(denom)>0.1)
 sx=src_outer+u*(src_inner-src_outer)
 out=np.stack([map_coordinates(exterior[:,:,c],[sy,sx],order=1,mode='constant',cval=0) for c in range(4)],2).astype('uint8')
 out[(y<265)|(y>689)|(u<0)|(u>1)|(abs(denom)<.1),3]=0
 im=Image.fromarray(out);box=im.getbbox();im=im.crop(box); pos=[(337 if side=='R' else 512)+box[0],250+box[1]]
 im.save(HERE/f'blazer_{side}_candidate.png');art['blazer_'+side]=(im,[1,0,0,1,*pos])
 records.append({'id':'blazer_'+side,'source':str(path.relative_to(REPO)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'file':str((HERE/f'blazer_{side}_candidate.png').relative_to(RIG)),'position':pos,'scale':[1,1],'parent':'chest','z':-180 if side=='R' else -179,'fold_seam_source_yx':fold.tolist(),'excluded_part':str((HERE/f'blazer_{side}_facing_not_instantiated.png').relative_to(RIG))})
# Isolate collar tabs from the same registered blouse with complementary masks.
blouse_source=REPO/'avatar_build_assets/body/layers/blouse_front.png'
blouse_clean=Image.fromarray(clean(blouse_source));crop=list(blouse_clean.getbbox());blouse=blouse_clean.crop(crop);a=np.array(blouse)
blouse_position=[512-blouse.width*.38/2,245];blouse_v=[.38,0,0,.38,*blouse_position]
rear=a.copy();collars={};collar_masks=[]
for side,poly,srcanchors,dstanchors in [
 ('R',[(267,204),(277,372),(141,391),(238,319)],[(267,204),(141,390),(277,374)],[(478,246),(440,302),(482,303)]),
 ('L',[(425,204),(419,374),(557,392),(458,319)],[(425,204),(557,392),(419,374)],[(546,246),(584,302),(542,303)])]:
 mask=Image.new('L',blouse.size);ImageDraw.Draw(mask).polygon([(x-crop[0],y-crop[1]) for x,y in poly],fill=255)
 m=np.array(mask)>0;collar_masks.append(m);front=a.copy();front[~m,3]=0;rear[m,3]=0
 im=Image.fromarray(front);box=im.getbbox();im=im.crop(box);im.save(HERE/f'blouse_collar_{side}_source.png')
 v=[.38,0,0,.38,403.51+box[0]*.38,245+box[1]*.38]
 dstanchors=[[403.51+(x-crop[0])*.38,245+(y-crop[1])*.38] for x,y in srcanchors]
 baked=Image.new('RGBA',CANVAS);place(baked,im,v);baked_box=baked.getbbox();baked=baked.crop(baked_box);baked.save(HERE/f'blouse_collar_{side}_candidate.png')
 collars[side]=(baked,[1,0,0,1,baked_box[0],baked_box[1]])
 records.append({'id':'blouse_collar_'+side,'source':'avatar_build_assets/body/layers/blouse_front.png','file':str((HERE/f'blouse_collar_{side}_candidate.png').relative_to(RIG)),'source_polygon_xy':poly,'source_landmarks_xy':srcanchors,'target_landmarks_xy':dstanchors,'canvas_affine_abcdxy':v,'crop':crop,'source_crop_within_cleaned_blouse':list(box),'position':list(baked_box[:2]),'scale':[1,1],'rotation_degrees':0,'parent':'chest','z':-178,'ownership':'Pixels removed from rear blouse; not an overlapping duplicate.'})
# The detached shirt has an untucked flared hem. Keep its center behind the jacket;
# hide only lower side excess outside the assembled fitted torso, not visible shirt details.
by,bx=np.indices(rear.shape[:2]);cx=403.51+bx*.38;cy=245+by*.38
limit_left=PchipInterpolator(ty,outer)(np.clip(cy,265,689))+3;limit_right=1024-limit_left
hide=(cy>=480)&((cx<limit_left)|(cx>limit_right));rear[hide,3]=0
Image.fromarray(rear).save(HERE/'blouse_body_candidate.png')
art['blouse']=(Image.fromarray(rear),blouse_v)
records.append({'id':'blouse','source':str(blouse_source.relative_to(REPO)),'source_sha256':hashlib.sha256(blouse_source.read_bytes()).hexdigest(),'file':str((HERE/'blouse_body_candidate.png').relative_to(RIG)),'crop':crop,'position':blouse_position,'scale':[.38,.38],'rotation_degrees':0,'parent':'chest','z':-190,'derivation':'Alpha <=10 cleanup; original crop; collar tabs cut into two front owners; untucked lower side excess alpha-masked inside registered jacket exterior at y>=480.'})
records.append({'id':'blazer_button','source':'avatar_build_assets/body/layers/blazer_front_character_R.png','file':str((HERE/'blazer_button_candidate.png').relative_to(RIG)),'crop':[431,527,470,566],'source_circle_xy_radius':[450,546,19],'position':[499,507],'scale':[.48,.48],'rotation_degrees':0,'parent':'chest','z':-177,'ownership':'Full original button cut from source panel; same pixels removed from visible exterior panel.'})
# Clip only surplus belt strap against the actual existing trouser-pelvis alpha.
belt_source=REPO/'avatar_build_assets/accessories/layers/RYO_ACC_belt_gold_buckle.png'
ba=np.array(Image.open(belt_source).convert('RGBA'));ba[ba[:,:,3]<32,3]=0
belt=Image.fromarray(ba);belt_crop=list(belt.getbbox());belt=belt.crop(belt_crop);ba=np.array(belt)
rgb=ba[:,:,:3].astype(int);gold=(rgb[:,:,0]>rgb[:,:,1]+12)&(rgb[:,:,1]>rgb[:,:,2]+18)&(rgb[:,:,0]>120)&(ba[:,:,3]>128)
gy,gx=np.where(gold);gold_center=[(float(gx.min())+float(gx.max()))/2,(float(gy.min())+float(gy.max()))/2]
bs=265/belt.width;bpos=[512-gold_center[0]*bs,614-gold_center[1]*bs];bv=[bs,0,0,bs,*bpos]
pa=np.array(Image.open(REPO/'avatar_build_assets/body/layers/trousers_pelvis_front.png').convert('RGBA'));pa[pa[:,:,3]<32,3]=0
pelvis=Image.fromarray(pa);pelvis=pelvis.crop(pelvis.getbbox());pa=np.array(pelvis)[:,:,3]
pv=[.65,0,0,.65,512-pelvis.width*.65/2,580]
by,bx=np.indices(ba.shape[:2],dtype=float);cx=bv[0]*bx+bv[4];cy=bv[3]*by+bv[5];px=(cx-pv[4])/pv[0];py=(cy-pv[5])/pv[3]
pa_sample=map_coordinates(pa,[py,px],order=1,mode='constant',cval=0)
before_belt_alpha=ba[:,:,3].copy();ba[(pa_sample<32)&(~gold),3]=0;Image.fromarray(ba).save(HERE/'belt_candidate.png')
art['belt']=(Image.fromarray(ba),bv)
records.append({'id':'belt','source':str(belt_source.relative_to(REPO)),'source_sha256':hashlib.sha256(belt_source.read_bytes()).hexdigest(),'file':str((HERE/'belt_candidate.png').relative_to(RIG)),'crop':belt_crop,'position':bpos,'scale':[bs,bs],'rotation_degrees':0,'parent':'pelvis','z':-319,'gold_buckle_center_crop':gold_center,'mask':'Only surplus strap outside the existing registered pelvis alpha removed; centered buckle unchanged.'})
# Preserve the current body, sleeves, head transform and neutral artwork.
for side,values in collars.items():art['blouse_collar_'+side]=values
c=Image.new('RGBA',CANVAS)
# Overrides are drawn once. This remains repeatable after the candidate is installed.
for e in sorted([e for e in manifest['layers'] if e['id'] not in art]+records,key=lambda e:e['z']):
 if e['id'] in art:im,v=art[e['id']]
 else:im=Image.open(RIG/e['file'][6:]).convert('RGBA');v=frame['layers'][e['id']]
 place(c,im,v)
place(c,Image.open(RIG/'full_body/pieces_v2/head_audit/neutral_head_complete.png').convert('RGBA'),frame['head'])
c.save(HERE/'integrated_candidate_transparent.png')
for filename,bg in [('integrated_candidate.png','#eeece5'),('integrated_candidate_dark.png','#20252b')]:
 out=Image.new('RGBA',CANVAS,bg);out.alpha_composite(c);out.save(HERE/filename)
out=Image.new('RGBA',CANVAS,'#eeece5');out.alpha_composite(c);out.crop((290,220,740,730)).resize((900,1020)).save(HERE/'jacket_detail.png')
for rec in records:
 im=Image.open(RIG/rec['file']);rec['size']=list(im.size);rec['alpha_bounds']=list(im.getbbox());rec.setdefault('rotation_degrees',0)
 src=REPO/rec['source'];rec.setdefault('source_sha256',hashlib.sha256(src.read_bytes()).hexdigest())
validation={'owners':len(records),'owner_ids':[e['id'] for e in records],'unique_owner_ids':len({e['id'] for e in records})==len(records),'collar_masks_disjoint':not np.any(collar_masks[0]&collar_masks[1]),'gold_buckle_alpha_unchanged':bool(np.array_equal(before_belt_alpha[gold],ba[:,:,3][gold])),'unchanged_head_transform':frame['head'],'reference_used_as_texture':False,'runtime_files_written':False,'native_render_verified':False}
assert validation['unique_owner_ids'] and validation['collar_masks_disjoint'] and validation['gold_buckle_alpha_unchanged']
(HERE/'validation.json').write_text(json.dumps(validation,indent=2)+'\n')
(HERE/'registration_candidate.json').write_text(json.dumps({'status':'Local jacket fit study, not integrated or approved','layers':records,'reference':'avatar_build_assets/reference_library/assets/modeling/RYO_MOD_fullbody_front_v001.png','reference_use':'Landmark/silhouette inspection only; no reference pixels used.','method':'Exterior panel isolated at existing painted lapel fold seam; documented contour landmark registration. Source RGB and alpha resampled, no generated art.','destination_y':ty.tolist(),'outer_R_x':outer.tolist(),'inner_R_x':inner.tolist(),'source_y':srcy.tolist(),'destination_source_y':dsty.tolist()},indent=2)+'\n')
print(HERE/'integrated_candidate.png')

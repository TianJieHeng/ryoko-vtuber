#!/usr/bin/env python3
"""Register cleaned full-body gesture drawings to the approved 1024x1536 reference."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter,ImageFont
import numpy as np
from scipy import ndimage
import json
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT.parent/'avatar_build_assets'
if not ASSETS.exists():
 ASSETS=ROOT.parent/'ryoko-vtuber'/'avatar_build_assets'
SRC=ASSETS/'reference_library/assets/body'
OUT=ROOT/'artwork'/'gestures';OUT.mkdir(parents=True,exist_ok=True)
PRE=ROOT/'previews';MAN=ROOT/'manifest'
S=2
routes={
 'gesture_finger_wag':{
  'file':'RYO_BOD-002_finger-wag_kp03_v001.png','crop':(280,100,760,910),'bottom':690,'action':'BOD-002',
  'hands':[(335,165,420,345),(650,710,742,895)],
  'lower_arm':[(640,500),(690,510),(710,600),(720,700),(730,910),(640,910),(638,700)],
  'neck_x':512,'torso_shift_ref':[0,-40],
  'hand_lines':[[(133,94),(132,68),3],[(126,89),(138,89),2],[(125,95),(136,95),2],[(126,101),(134,101),2],[(235,250),(235,264),2],[(247,254),(245,267),(238,278),3]],
  'hand_polys':[[(125,87),(139,84),(143,96),(137,110),(134,118),(124,117),(122,103)],[(236,239),(246,239),(248,253),(244,256),(241,250),(237,251),(233,258),(232,249)]],
  'pocket':(615,372,645,405),'raised_cuff':(345,330,390,370),'lowered_cuff':(675,690,715,735)},
 'gesture_crossed_arms':{
  'file':'RYO_BOD-001_arms-crossed-stern_kp05_v001.png','crop':(320,240,705,720),'bottom':690,'action':'BOD-001',
  'hands':[(345,385,485,495),(535,360,660,485)],
  'neck_x':512,'torso_shift_ref':[0,-40],
  'pocket':(600,365,635,400),'raised_cuff':(0,0,0,0),'lowered_cuff':(0,0,0,0)},
 'gesture_wave':{
  'file':'RYO_BOD-011_greeting-wave_kp04_v001.png','crop':(210,100,760,910),'bottom':690,'action':'BOD-011',
  'hands':[(210,145,370,345),(650,710,742,895)],
  'lower_arm':[(674,520),(710,540),(724,620),(738,700),(748,910),(700,910),(695,720),(670,620)],
  'neck_x':541,'torso_shift_ref':[-29,-40],
  'hand_lines':[[(99,113),(86,101),3],[(103,109),(90,92),3],[(109,106),(96,85),3],[(114,104),(105,83),3],[(118,114),(120,96),3],[(235,250),(235,264),2],[(247,254),(245,267),(238,278),3]],
  'hand_polys':[[(98,103),(113,101),(124,113),(124,130),(116,139),(105,130),(94,115)],[(236,239),(246,239),(248,253),(244,256),(241,250),(237,251),(233,258),(232,249)]],
  'pocket':(628,370,655,405),'raised_cuff':(320,375,355,415),'lowered_cuff':(695,690,735,735)}
}
def remove_background(im):
 """Remove only the border-connected sheet background here; anatomy is protected after registration."""
 a=np.array(im.convert('RGBA'));rgb=a[:,:,:3].astype(np.int16)
 # The sheet is a neutral warm grey. A broad near-white chroma threshold also
 # classifies pale skin as background, so keep the matte test genuinely neutral.
 candidate=(rgb.min(2)>215)&((rgb.max(2)-rgb.min(2))<16)
 labels,_=ndimage.label(candidate);border=np.unique(np.concatenate([labels[0,:],labels[-1,:],labels[:,0],labels[:,-1]]))
 a[np.isin(labels,border[border>0]),3]=0
 return Image.fromarray(a,'RGBA')
def hand_protection(full,rois):
 """Preserve every foreground pixel inside tight hand boxes, including pale finger interiors."""
 a=np.array(full);protected=np.zeros(a.shape[:2],bool)
 for x0,y0,x1,y1 in rois:
  x0,y0,x1,y1=[round(v*S) for v in (x0,y0,x1,y1)]
  protected[y0:y1,x0:x1]|=a[y0:y1,x0:x1,3]>0
 return protected
def register_torso_to_neutral_head(full,cfg):
 """Move the upper torso to the fixed approved head; taper to zero before the pelvis."""
 a=np.array(full)
 yy,xx=np.mgrid[0:a.shape[0],0:a.shape[1]].astype(np.float32)
 weight=np.clip((700-yy/S)/400.0,0,1)
 dx=cfg['torso_shift_ref'][0]*S*weight
 dy=cfg['torso_shift_ref'][1]*S*weight
 coords=[yy-dy,xx-dx]
 out=np.zeros_like(a)
 for channel in range(4):
  out[:,:,channel]=ndimage.map_coordinates(a[:,:,channel],coords,order=1,mode='constant',cval=0,prefilter=False)
 return Image.fromarray(out,'RGBA')
entries=[]
for name,cfg in routes.items():
 src=Image.open(SRC/cfg['file']).convert('RGB');clean=remove_background(src);alpha=np.array(clean.getchannel('A'))
 ys,xs=np.where(alpha>0);top=int(ys.min());bottom=int(ys.max())
 scale=(1497-26)/(bottom-top);tx=512-src.width/2*scale;ty=26-top*scale
 # Restore pale skin removed with the sheet background inside registered hand ROIs.
 # Skin chroma distinguishes fingers from the neutral white gaps between them.
 clean_array=np.array(clean);source_array=np.array(src.convert('RGBA'));srgb=source_array[:,:,:3].astype(np.int16)
 skin_source=(srgb[:,:,0]>120)&(srgb[:,:,0]>srgb[:,:,1]+4)&(srgb[:,:,1]>srgb[:,:,2]+3)
 for hx0,hy0,hx1,hy1 in cfg['hands']:
  sx0=max(0,int((hx0-tx)/scale));sx1=min(src.width,int((hx1-tx)/scale)+1)
  sy0=max(0,int((hy0-ty)/scale));sy1=min(src.height,int((hy1-ty)/scale)+1)
  restore=np.zeros(clean_array.shape[:2],bool);restore[sy0:sy1,sx0:sx1]=True;restore&=skin_source
  clean_array[restore]=source_array[restore]
 # Restore chromatic skin on the chest, legs and ankles as well. The neutral
 # sheet remains excluded by the red/green and green/blue chroma guards.
 lower_skin=np.zeros(clean_array.shape[:2],bool)
 lower_skin[max(0,int((285-ty)/scale)):min(src.height,int((1520-ty)/scale)+1),:]=True
 lower_skin&=skin_source
 clean_array[lower_skin]=source_array[lower_skin]
 # Reveal only the original interiors of the drawn fingers and palms. These
 # interior strokes never cross the true background gaps between fingers.
 interior=Image.new('L',src.size,0);draw=ImageDraw.Draw(interior)
 for line in cfg.get('hand_lines',[]):
  draw.line(line[:-1],fill=255,width=line[-1],joint='curve')
 for polygon in cfg.get('hand_polys',[]):
  draw.polygon(polygon,fill=255)
 interior_mask=(np.array(interior)>0)&(srgb[:,:,0]>srgb[:,:,1]+2)&(srgb[:,:,0]>srgb[:,:,2]+7)
 clean_array[interior_mask]=source_array[interior_mask]
 clean=Image.fromarray(clean_array,'RGBA')
 size=(round(src.width*scale*S),round(src.height*scale*S));im=clean.resize(size,Image.Resampling.LANCZOS)
 full=Image.new('RGBA',(2048,3072));full.alpha_composite(im,(round(tx*S),round(ty*S)))
 a=np.array(full);rgb=a[:,:,:3].astype(np.int16);white=(rgb.min(2)>205)&((rgb.max(2)-rgb.min(2))<30)
 protect=Image.new('L',full.size,0);pd=ImageDraw.Draw(protect)
 pd.polygon([(415*S,235*S),(605*S,235*S),(610*S,430*S),(575*S,650*S),(450*S,650*S),(415*S,430*S)],fill=255)
 pd.rectangle((370*S,1330*S,480*S,1520*S),fill=255)
 pd.rectangle((545*S,1330*S,655*S,1520*S),fill=255)
 for key in ('pocket','raised_cuff','lowered_cuff'):
  box=cfg.get(key,(0,0,0,0))
  if box[2]>box[0] and box[3]>box[1]:
   pd.rectangle(tuple(round(v*S) for v in box),fill=255)
 hand_foreground=hand_protection(full,cfg['hands'])
 protected=(np.array(protect)>0)|hand_foreground
 a[white&~protected,3]=0
 # Remove residual neutral matte at outside boundaries without cutting pale hands or garments.
 solid=a[:,:,3]>8;edge=solid&~ndimage.binary_erosion(solid,iterations=3)
 neutral=(rgb.min(2)>65)&((rgb.max(2)-rgb.min(2))<80)
 near_dark=ndimage.binary_dilation(rgb.max(2)<90,iterations=5)
 a[edge&neutral&near_dark&~protected,3]=0;full=Image.fromarray(a,'RGBA')
 # Retain the complete upper body and hands, but replace the alternate head AND neck.
 mask=Image.new('L',full.size,0);d=ImageDraw.Draw(mask);x0,y0,x1,y1=[round(v*S) for v in cfg['crop']]
 d.rectangle((x0,y0,x1,y1),fill=255)
 yy=np.arange(3072,dtype=np.float32)[:,None]/S
 ramp=np.clip((cfg['bottom']+35-yy)/35,0,1)
 mask_array=(np.array(mask).astype(np.float32)*ramp).astype(np.uint8)
 # The lowered arm and hand extend below the torso overlap; never fade through them.
 if name in ('gesture_finger_wag','gesture_wave'):
  arm=Image.new('L',full.size,0);ad=ImageDraw.Draw(arm)
  ad.polygon([(x*S,y*S) for x,y in cfg['lower_arm']],fill=255)
  mask_array=np.maximum(mask_array,np.array(arm))
 mask=Image.fromarray(mask_array,'L')
 d=ImageDraw.Draw(mask)
 # Replace only the alternate head and central neck. Preserve the reference's
 # shoulders, jacket and centered blouse; the former deep rectangle cut them off.
 neck_x=cfg['neck_x']
 d.rectangle((380*S,0,680*S,285*S),fill=0)
 if name=='gesture_wave':
  # Remove the alternate lower-body fragment outside the viewer-left jacket hem.
  d.rectangle((350*S,760*S,425*S,810*S),fill=0)
 # Trim detached alternate hip/leg fragments outside the jacket silhouette.
 # The approved neutral pelvis remains underneath; lowered arms are protected below.
 if name=='gesture_crossed_arms':
  d.rectangle((300*S,610*S,379*S,810*S),fill=0)
  d.rectangle((646*S,610*S,705*S,810*S),fill=0)
 elif name=='gesture_finger_wag':
  d.rectangle((280*S,610*S,374*S,810*S),fill=0)
 mask_array=np.array(mask)
 # Keep the original smooth collar fabric, but remove residual alternate hair.
 original_alpha=np.array(full.getchannel('A'))
 fabric=(rgb.min(2)>105)&((rgb.max(2)-rgb.min(2))<48)
 collar_transition=(yy>=235)&(yy<285)&fabric
 collar_weight=np.clip((yy-235)/35.0,0,1)
 collar_alpha=(original_alpha.astype(np.float32)*collar_weight).astype(np.uint8)
 mask_array[collar_transition]=np.maximum(mask_array[collar_transition],collar_alpha[collar_transition])
 hair=(rgb[:,:,1]>rgb[:,:,0]+7)&(rgb[:,:,1]>rgb[:,:,2]+4)&(rgb.max(2)<235)
 residual_zone=(yy>=235)&(yy<=345)
 mask_array[residual_zone&hair]=0
 head_hand_restore=hand_foreground.copy();head_hand_restore[345*S:,:]=False;mask_array[head_hand_restore]=255;mask=Image.fromarray(mask_array,'L')
 mask=mask.filter(ImageFilter.GaussianBlur(.6))
 lower_source=full.copy()
 full.putalpha(Image.fromarray(np.minimum(np.array(full.getchannel('A')),np.array(mask)).astype(np.uint8),'L'))
 # The alternate head is now detached from the torso. Keep the main body and all
 # hand-connected components; discard detached head fragments and isolated matte.
 a=np.array(full);labels,n=ndimage.label(a[:,:,3]>10);sizes=np.bincount(labels.ravel());sizes[0]=0
 main=int(sizes.argmax());keep=labels==main
 # All cleaned hands remain attached through their wrists and arms. Keeping
 # every detached component inside a hand box also preserved isolated matte.
 a[~keep,3]=0;full=Image.fromarray(a,'RGBA')
 full=register_torso_to_neutral_head(full,cfg)
 lower_full=register_torso_to_neutral_head(lower_source,cfg)
 # The upward torso registration can pull residual alternate head pixels into
 # the fixed-head region. Clean them after warping too, without cutting the
 # raised finger-wag hand or the continuous jacket and collar below y=225.
 wa=np.array(full);wrgb=wa[:,:,:3].astype(np.int16)
 post=Image.new('L',full.size,255);post_draw=ImageDraw.Draw(post)
 post_draw.rectangle((420*S,0,680*S,225*S),fill=0)
 wa[:,:,3]=np.minimum(wa[:,:,3],np.array(post))
 wskin=(wrgb[:,:,0]>120)&(wrgb[:,:,0]>wrgb[:,:,1]+7)&(wrgb[:,:,1]>wrgb[:,:,2]+4)
 whair=(wrgb[:,:,1]>wrgb[:,:,0]+7)&(wrgb[:,:,1]>wrgb[:,:,2]+4)&(wrgb.max(2)<235)
 wyy=np.arange(3072,dtype=np.float32)[:,None]/S
 wxx=np.arange(2048,dtype=np.float32)[None,:]/S
 neck_residue=(wyy>=225)&(wyy<285)&(wxx>=430)&(wxx<=610)
 wa[neck_residue&(wskin|whair),3]=0
 full=Image.fromarray(wa,'RGBA')
 # Warping can detach tiny matte/collar specks at a crop boundary. The registered
 # upper body is one connected drawing; discard only detached residue.
 fa=np.array(full);fl,fn=ndimage.label(fa[:,:,3]>10);fs=np.bincount(fl.ravel());fs[0]=0
 fa[fl!=int(fs.argmax()),3]=0;full=Image.fromarray(fa,'RGBA')
 crop=full.crop((x0,y0,x1,y1))
 ca=np.array(crop);cl,cn=ndimage.label(ca[:,:,3]>0);cs=np.bincount(cl.ravel());cs[0]=0
 ca[cl!=int(cs.argmax()),3]=0;crop=Image.fromarray(ca,'RGBA');crop.save(OUT/f'{name}.png')
 # Build the authoritative single-body derivative from the same complete registered
 # drawing. No second upper/lower copy is composited, so hems, arms, pelvis, legs
 # and heels retain their source alignment.
 la=np.array(lower_full);ll,ln=ndimage.label(la[:,:,3]>10);ls=np.bincount(ll.ravel());ls[0]=0
 la[ll!=int(ls.argmax()),3]=0
 body_alpha=la[:,:,3].copy()
 lrgb=la[:,:,:3].astype(np.int16)
 lhair=(lrgb[:,:,1]>lrgb[:,:,0]+7)&(lrgb[:,:,1]>lrgb[:,:,2]+4)&(lrgb.max(2)<235)
 lyy=np.arange(3072,dtype=np.float32)[:,None]/S
 underlay_transition=(lyy>=235)&(lyy<285)
 la[underlay_transition&lhair,3]=0
 underlay_ramp=np.clip((lyy-235)/40.0,0,1)
 la[:,:,3]=(la[:,:,3].astype(np.float32)*underlay_ramp).astype(np.uint8)
 if name in ('gesture_finger_wag','gesture_wave'):
  hx0,hy0,hx1,hy1=cfg['hands'][0]
  hand_restore=np.zeros(la.shape[:2],bool)
  hand_restore[hy0*S:hy1*S,hx0*S:hx1*S]=True
  la[hand_restore,3]=body_alpha[hand_restore]
 fl,fn=ndimage.label(la[:,:,3]>10);fs=np.bincount(fl.ravel());fs[0]=0
 la[fl!=int(fs.argmax()),3]=0
 registered=Image.fromarray(la,'RGBA')
 registered_box=(x0,y0,x1,1520*S);registered=registered.crop(registered_box);registered.save(OUT/f'{name}_registered.png')
 # Replace the experimental split upper/lower entries with one coherent body.
 entries=[e for e in entries if e['name'] not in (name,f'{name}_lower_body')]
 entries.append({'name':name,'source':f'reference_library/assets/body/{cfg["file"]}','registered_png':f'artwork/gestures/{name}_registered.png','enabled_neutral':False,'z':20.0,'parent':'torso','master_xy':[registered_box[0],registered_box[1]],'master_size':list(registered.size),'pivot_ref':[512,280],'pivot_master':[1024,560],'action_id':cfg['action'],'registration':{'source_scale_to_reference':scale,'source_translation_ref':[tx,ty],'source_foreground_top_bottom':[top,bottom],'head_and_alternate_neck_excluded':True,'shoulders_and_original_blouse_preserved':True,'torso_shift_ref':cfg['torso_shift_ref'],'head_offset_ref':[0,0],'background_removed':True,'complete_hand_protection_ref':cfg['hands'],'single_registered_body':True},'role':'single coherent registered full-body alternate; fixed canonical head composites above'})
# A narrow canonical neck bridge joins the approved head to each original torso.
# The alternate drawing keeps its own collar, blouse, jewelry, shoulders and jacket.
placement=json.loads((MAN/'placement_manifest.json').read_text());base_entries=placement['layers']
# The neutral rear-hair cut includes covered neck/collar/jacket pixels. Gesture
# swaps expose them, so use a hair-only derivative while leaving neutral intact.
rear_base=next(e for e in base_entries if e['name']=='rear_hair')
rear=Image.open(ROOT/rear_base['registered_png']).convert('RGBA');ra=np.array(rear);rrgb=ra[:,:,:3].astype(np.int16)
hair_core=(rrgb[:,:,1]>rrgb[:,:,0]+2)&(rrgb[:,:,1]>rrgb[:,:,2]+1)
hair_support=ndimage.binary_dilation(hair_core,iterations=2)
hair_tint=(rrgb[:,:,1]>=rrgb[:,:,0]-3)&(rrgb[:,:,1]>=rrgb[:,:,2]-3)
rear_mask=Image.fromarray(np.where(hair_support&hair_tint,255,0).astype(np.uint8),'L').filter(ImageFilter.GaussianBlur(.5))
rear.putalpha(Image.fromarray(np.minimum(ra[:,:,3],np.array(rear_mask)).astype(np.uint8),'L'))
ra=np.array(rear);ra[max(0,250*S-rear_base['master_xy'][1]):,:,3]=0
rl,rn=ndimage.label(ra[:,:,3]>10);rs=np.bincount(rl.ravel());rs[0]=0
ra[~np.isin(rl,np.where(rs>=24)[0]),3]=0;rear=Image.fromarray(ra,'RGBA')
rear.save(OUT/'gesture_rear_hair.png')
entries.append({'name':'gesture_rear_hair','source':'approved canonical rear-hair layer; non-hair overlap removed for gesture swaps','registered_png':'artwork/gestures/gesture_rear_hair.png','enabled_neutral':False,'z':10.0,'parent':'head','master_xy':rear_base['master_xy'],'master_size':list(rear.size),'pivot_ref':[512,250],'pivot_master':[1024,500],'role':'hair-only rear layer; prevents neck, collar and jacket duplication above gesture torsos'})
bridge=Image.new('RGBA',(2048,3072))
for e in sorted(base_entries,key=lambda item:item['z']):
 if e['name'] in ('neck',):
  bridge.alpha_composite(Image.open(ROOT/e['registered_png']).convert('RGBA'),tuple(e['master_xy']))
bridge_mask=Image.new('L',bridge.size,0);bd=ImageDraw.Draw(bridge_mask)
bd.polygon([(465*S,208*S),(550*S,208*S),(552*S,250*S),(545*S,315*S),(535*S,340*S),(480*S,340*S),(465*S,315*S)],fill=255)
by=np.arange(3072,dtype=np.float32)[:,None]/S
bridge_ramp=np.clip((340-by)/25,0,1)
bridge_mask=Image.fromarray((np.array(bridge_mask).astype(np.float32)*bridge_ramp).astype(np.uint8),'L').filter(ImageFilter.GaussianBlur(1.0))
bridge_alpha=np.minimum(np.array(bridge.getchannel('A')),np.array(bridge_mask)).astype(np.float32)
# The canonical neck derivative includes collar-edge pixels that the neutral torso
# normally covers. Keep only skin here so the original gesture collar stays single.
ba=np.array(bridge)[:,:,:3].astype(np.int16)
bridge_skin=(ba[:,:,0]>105)&(ba[:,:,0]>ba[:,:,1]+5)&(ba[:,:,1]>ba[:,:,2]+3)
skin_mask=Image.fromarray(np.where(bridge_skin,255,0).astype(np.uint8),'L').filter(ImageFilter.GaussianBlur(.7))
bridge_alpha*=np.array(skin_mask).astype(np.float32)/255.0
bridge.putalpha(Image.fromarray(bridge_alpha.astype(np.uint8),'L'))
bridge_box=(455*S,205*S,565*S,340*S);bridge=bridge.crop(bridge_box);bridge.save(OUT/'gesture_neck_bridge.png')
entries.append({'name':'gesture_neck_bridge','source':'approved canonical neck layer only; original gesture collar, blouse and jewelry preserved','registered_png':'artwork/gestures/gesture_neck_bridge.png','enabled_neutral':False,'z':37.0,'parent':'torso','master_xy':[bridge_box[0],bridge_box[1]],'master_size':list(bridge.size),'pivot_ref':[512,280],'pivot_master':[1024,560],'role':'narrow registered canonical neck join; no torso, shoulder, face or blouse replacement'})
(MAN/'gesture_layers.json').write_text(json.dumps({'canvas_reference':[1024,1536],'canvas_master':[2048,3072],'gesture_hide':['torso_garment','upper_arm_R','upper_arm_L','forearm_R','forearm_L','hand_R','hand_L','registration_underlap','canonical_pelvis','trousers_leg_front_R','trousers_leg_front_L','shoe_R','shoe_L','neck','belt_gold_buckle','necklace_chain','green_pendant'],'layers':entries},indent=2))
# Assemble real gesture previews on the approved neutral head, hair, jewelry and lower body.
hide=set(json.loads((MAN/'gesture_layers.json').read_text())['gesture_hide'])
clean_rear_entry=next(x for x in entries if x['name']=='gesture_rear_hair')
def composite(gesture=None,bg=(24,29,34,255)):
 can=Image.new('RGBA',(2048,3072))
 for e in base_entries:
  if not e['enabled_neutral'] or e['name'] in hide:continue
  if gesture and e['parent']=='head' and e['z']>=32:continue  # redraw the face and front head once, above the swap
  if gesture and e['name']=='rear_hair':
   can.alpha_composite(Image.open(ROOT/clean_rear_entry['registered_png']).convert('RGBA'),tuple(clean_rear_entry['master_xy']));continue
  can.alpha_composite(Image.open(ROOT/e['registered_png']).convert('RGBA'),tuple(e['master_xy']))
 if gesture:
  gesture_entry=next(x for x in entries if x['name']==gesture);can.alpha_composite(Image.open(ROOT/gesture_entry['registered_png']).convert('RGBA'),tuple(gesture_entry['master_xy']))
  offset=[0,0]
  bridge_entry=next(x for x in entries if x['name']=='gesture_neck_bridge');can.alpha_composite(Image.open(ROOT/bridge_entry['registered_png']).convert('RGBA'),(bridge_entry['master_xy'][0]+offset[0],bridge_entry['master_xy'][1]+offset[1]))
  for e in base_entries:
   if e['enabled_neutral'] and e['parent']=='head' and e['z']>=32 and e['name'] not in hide:
    can.alpha_composite(Image.open(ROOT/e['registered_png']).convert('RGBA'),(e['master_xy'][0]+offset[0],e['master_xy'][1]+offset[1]))
 out=Image.new('RGBA',can.size,bg);out.alpha_composite(can);return out.convert('RGB')
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',26)
sheet=Image.new('RGB',(1800,1100),(27,32,37));d=ImageDraw.Draw(sheet)
for i,name in enumerate(routes):
 im=composite(name);im.save(PRE/f'{name}_dark.png');im.thumbnail((560,840));sheet.paste(im,(30+i*590,90));d.text((30+i*590,35),name.replace('gesture_','').replace('_',' ').upper(),font=font,fill=(240,240,240))
d.text((30,980),'REGISTERED ALTERNATE DRAWINGS / CONTINUOUS CANONICAL NECK + COMPLETE HANDS',font=font,fill=(210,220,215));sheet.save(PRE/'ryoko_gesture_registration_review.png')
print(json.dumps({'gestures':len(routes),'shared_neck_bridge':True,'output':str(MAN/'gesture_layers.json')},indent=2))

#!/usr/bin/env python3
"""Register cleaned upper-body alternate drawings to the approved 1024x1536 master."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter,ImageFont
import numpy as np
from scipy import ndimage
import json
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT.parent/'ryoko-vtuber'/'avatar_build_assets'/'reference_library/assets/body'
OUT=ROOT/'artwork'/'gestures';OUT.mkdir(parents=True,exist_ok=True)
PRE=ROOT/'previews';MAN=ROOT/'manifest'
S=2
routes={
 'gesture_finger_wag':{
  'file':'RYO_BOD-002_finger-wag_kp03_v001.png','crop':(280,100,760,910),'bottom':690,'action':'BOD-002',
  'hands':[(335,165,420,345),(650,710,742,895)],
  'lower_arm':[(640,500),(690,510),(710,600),(720,700),(730,910),(640,910),(638,700)],
  'neck_x':512,'torso_shift_ref':[0,-40]},
 'gesture_crossed_arms':{
  'file':'RYO_BOD-001_arms-crossed-stern_kp05_v001.png','crop':(320,240,705,720),'bottom':690,'action':'BOD-001',
  'hands':[(345,385,485,495),(535,360,660,485)],
  'neck_x':512,'torso_shift_ref':[0,-40]},
 'gesture_wave':{
  'file':'RYO_BOD-011_greeting-wave_kp04_v001.png','crop':(250,100,760,910),'bottom':690,'action':'BOD-011',
  'hands':[(250,155,370,345),(650,710,742,895)],
  'lower_arm':[(674,520),(710,540),(724,620),(738,700),(748,910),(700,910),(695,720),(670,620)],
  'neck_x':541,'torso_shift_ref':[-29,-40]}
}
def remove_background(im):
 """Remove only the border-connected sheet background here; anatomy is protected after registration."""
 a=np.array(im.convert('RGBA'));rgb=a[:,:,:3].astype(np.int16)
 candidate=(rgb.min(2)>215)&((rgb.max(2)-rgb.min(2))<42)
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
 size=(round(src.width*scale*S),round(src.height*scale*S));im=clean.resize(size,Image.Resampling.LANCZOS)
 full=Image.new('RGBA',(2048,3072));full.alpha_composite(im,(round(tx*S),round(ty*S)))
 a=np.array(full);rgb=a[:,:,:3].astype(np.int16);white=(rgb.min(2)>205)&((rgb.max(2)-rgb.min(2))<30)
 protect=Image.new('L',full.size,0);pd=ImageDraw.Draw(protect)
 pd.polygon([(415*S,235*S),(605*S,235*S),(610*S,430*S),(575*S,650*S),(450*S,650*S),(415*S,430*S)],fill=255)
 pd.rectangle((590*S,345*S,650*S,420*S),fill=255)  # pocket square
 pd.rectangle((340*S,255*S,415*S,345*S),fill=255)  # raised-wrist cuff
 pd.rectangle((640*S,675*S,725*S,760*S),fill=255)  # lowered-wrist cuff
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
  d.rectangle((350*S,615*S,425*S,810*S),fill=0)
 mask_array=np.array(mask)
 # Keep the original smooth collar fabric, but remove residual alternate skin/hair.
 original_alpha=np.array(full.getchannel('A'))
 fabric=(rgb.min(2)>105)&((rgb.max(2)-rgb.min(2))<48)
 fabric_restore=(yy>=285)&(yy<=345)&fabric
 mask_array[fabric_restore]=original_alpha[fabric_restore]
 skin=(rgb[:,:,0]>120)&(rgb[:,:,0]>rgb[:,:,1]+7)&(rgb[:,:,1]>rgb[:,:,2]+4)
 hair=(rgb[:,:,1]>rgb[:,:,0]+7)&(rgb[:,:,1]>rgb[:,:,2]+4)&(rgb.max(2)<235)
 residual_zone=(yy>=282)&(yy<=345)
 mask_array[residual_zone&hair]=0
 head_hand_restore=hand_foreground.copy();head_hand_restore[345*S:,:]=False;mask_array[head_hand_restore]=255;mask=Image.fromarray(mask_array,'L')
 mask=mask.filter(ImageFilter.GaussianBlur(.6))
 full.putalpha(Image.fromarray(np.minimum(np.array(full.getchannel('A')),np.array(mask)).astype(np.uint8),'L'))
 # The alternate head is now detached from the torso. Keep the main body and all
 # hand-connected components; discard detached head fragments and isolated matte.
 a=np.array(full);labels,n=ndimage.label(a[:,:,3]>10);sizes=np.bincount(labels.ravel());sizes[0]=0
 main=int(sizes.argmax());keep=labels==main
 hand_pixels=np.zeros(a.shape[:2],bool)
 for hx0,hy0,hx1,hy1 in cfg['hands']:
  hx0,hy0,hx1,hy1=[round(v*S) for v in (hx0,hy0,hx1,hy1)];hand_pixels[hy0:hy1,hx0:hx1]=True
 hand_labels=np.unique(labels[hand_pixels&(labels>0)])
 for component in hand_labels:
  if int(sizes[component])>=8:keep|=labels==component
 a[~keep,3]=0;full=Image.fromarray(a,'RGBA')
 full=register_torso_to_neutral_head(full,cfg)
 crop=full.crop((x0,y0,x1,y1));crop.save(OUT/f'{name}.png')
 entries.append({'name':name,'source':f'reference_library/assets/body/{cfg["file"]}','registered_png':f'artwork/gestures/{name}.png','enabled_neutral':False,'z':36.5,'parent':'torso','master_xy':[x0,y0],'master_size':list(crop.size),'pivot_ref':[512,280],'pivot_master':[1024,560],'action_id':cfg['action'],'registration':{'source_scale_to_reference':scale,'source_translation_ref':[tx,ty],'source_foreground_top_bottom':[top,bottom],'head_and_alternate_neck_excluded':True,'shoulders_and_original_blouse_preserved':True,'torso_shift_ref':cfg['torso_shift_ref'],'head_offset_ref':[0,0],'background_removed':True,'complete_hand_protection_ref':cfg['hands'],'lowered_hand_preserved_below_torso_overlap':name in ('gesture_finger_wag','gesture_wave')},'role':'registered cleaned upper-body alternate drawing for the shared cutout rig'})
# A narrow canonical neck bridge joins the approved head to each original torso.
# The alternate drawing keeps its own collar, blouse, jewelry, shoulders and jacket.
placement=json.loads((MAN/'placement_manifest.json').read_text());base_entries=placement['layers']
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
(MAN/'gesture_layers.json').write_text(json.dumps({'canvas_reference':[1024,1536],'canvas_master':[2048,3072],'gesture_hide':['torso_garment','upper_arm_R','upper_arm_L','forearm_R','forearm_L','hand_R','hand_L'],'layers':entries},indent=2))
# Assemble real gesture previews on the approved neutral head, hair, jewelry and lower body.
hide=set(json.loads((MAN/'gesture_layers.json').read_text())['gesture_hide'])
def composite(gesture=None,bg=(24,29,34,255)):
 can=Image.new('RGBA',(2048,3072))
 for e in base_entries:
  if not e['enabled_neutral'] or e['name'] in hide:continue
  can.alpha_composite(Image.open(ROOT/e['registered_png']).convert('RGBA'),tuple(e['master_xy']))
 if gesture:
  gesture_entry=next(x for x in entries if x['name']==gesture);can.alpha_composite(Image.open(ROOT/gesture_entry['registered_png']).convert('RGBA'),tuple(gesture_entry['master_xy']))
  offset=[0,0]
  bridge_entry=next(x for x in entries if x['name']=='gesture_neck_bridge');can.alpha_composite(Image.open(ROOT/bridge_entry['registered_png']).convert('RGBA'),(bridge_entry['master_xy'][0]+offset[0],bridge_entry['master_xy'][1]+offset[1]))
  for e in base_entries:
   if e['enabled_neutral'] and e['z']>=40:
    can.alpha_composite(Image.open(ROOT/e['registered_png']).convert('RGBA'),(e['master_xy'][0]+offset[0],e['master_xy'][1]+offset[1]))
 out=Image.new('RGBA',can.size,bg);out.alpha_composite(can);return out.convert('RGB')
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',26)
sheet=Image.new('RGB',(1800,1100),(27,32,37));d=ImageDraw.Draw(sheet)
for i,name in enumerate(routes):
 im=composite(name);im.save(PRE/f'{name}_dark.png');im.thumbnail((560,840));sheet.paste(im,(30+i*590,90));d.text((30+i*590,35),name.replace('gesture_','').replace('_',' ').upper(),font=font,fill=(240,240,240))
d.text((30,980),'REGISTERED ALTERNATE DRAWINGS / CONTINUOUS CANONICAL NECK + COMPLETE HANDS',font=font,fill=(210,220,215));sheet.save(PRE/'ryoko_gesture_registration_review.png')
print(json.dumps({'gestures':len(routes),'shared_neck_bridge':True,'output':str(MAN/'gesture_layers.json')},indent=2))

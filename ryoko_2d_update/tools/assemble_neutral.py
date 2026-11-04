#!/usr/bin/env python3
"""Register Ryoko's supplied 2D artwork on one frontal master and export editable layers."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from scipy import ndimage
import cv2
import json, zipfile, shutil
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT.parent/'ryoko-vtuber'/'avatar_build_assets'
OUT=ROOT/'artwork';MAN=ROOT/'manifest';PRE=ROOT/'previews'
for p in [OUT/'layers',OUT/'registered',OUT/'derivatives',MAN,PRE]:p.mkdir(parents=True,exist_ok=True)
S=2;W,H=1024*S,1536*S
entries=[];cleaned={}
def clean(im,rel=''):
 im=im.convert('RGBA');a=np.array(im);alpha=a[:,:,3].astype(np.float32)
 a[:,:,3]=np.where(alpha<12,0,np.where(alpha<32,(alpha-12)*255/20,alpha)).astype(np.uint8)
 if 'trousers_leg_front' in rel:
  # The supplied leg cuts carry a pale outer matte; remove only that exterior fringe.
  rgb=a[:,:,:3].astype(np.int16);solid=a[:,:,3]>0;edge=solid&~ndimage.binary_erosion(solid,iterations=3)
  pale=(rgb.min(axis=2)>125)&((rgb.max(axis=2)-rgb.min(axis=2))<65);a[edge&pale,3]=0
 im=Image.fromarray(a,'RGBA');b=im.getchannel('A').getbbox()
 if not b:raise ValueError('empty artwork')
 return im.crop(b)
def load_source(rel):
 if rel not in cleaned:
  cleaned[rel]=clean(Image.open(SRC/rel),rel);cleaned[rel].save(OUT/'derivatives'/(rel.replace('/','__')))
 return cleaned[rel].copy()
def add(name,rel,bbox=None,z=0,parent='root',pivot=None,enabled=True,role='',center=None,size=None,angle=0,source=None,top_shift=0):
 im=load_source(rel)
 if bbox is not None:
  x0,y0,x1,y1=bbox;tw,th=round((x1-x0)*S),round((y1-y0)*S);cx,cy=(x0+x1)*S/2,(y0+y1)*S/2
 else:tw,th=round(size[0]*S),round(size[1]*S);cx,cy=center[0]*S,center[1]*S
 im=im.resize((max(1,tw),max(1,th)),Image.Resampling.LANCZOS)
 if top_shift:
  shift=round(top_shift*S);anchor=round(im.height*.60);warped=Image.new('RGBA',im.size)
  warped.paste(im.crop((0,0,im.width,anchor)).resize((im.width,anchor-shift),Image.Resampling.LANCZOS),(0,shift));warped.paste(im.crop((0,anchor,im.width,im.height)),(0,anchor));im=warped
 if angle:im=im.rotate(angle,Image.Resampling.BICUBIC,expand=True)
 x,y=round(cx-im.width/2),round(cy-im.height/2);reg=OUT/'registered'/f'{name}.png';im.save(reg)
 if pivot is None:pivot=(cx/S,cy/S)
 entries.append({'name':name,'source':source or rel,'derivative':str((OUT/'derivatives'/(rel.replace('/','__'))).relative_to(ROOT)),'registered_png':str(reg.relative_to(ROOT)),'enabled_neutral':enabled,'z':z,'parent':parent,'bbox_ref_xyxy':[round(x/S,3),round(y/S,3),round((x+im.width)/S,3),round((y+im.height)/S,3)],'master_xy':[x,y],'master_size':[im.width,im.height],'rotation_degrees':angle,'shoulder_compression_ref':top_shift,'pivot_ref':list(pivot),'pivot_master':[pivot[0]*S,pivot[1]*S],'role':role,'character_side_convention':'L is character-left (viewer-right); R is character-right (viewer-left)'})
_CANONICAL=None
def get_canonical():
 global _CANONICAL
 if _CANONICAL is None:
  base=Image.open(SRC/'reference_library/assets/modeling/RYO_MOD_fullbody_front_v001.png').convert('RGBA');a=np.array(base);rgb=a[:,:,:3].astype(np.int16)
  candidate=(rgb.min(axis=2)>215)&((rgb.max(axis=2)-rgb.min(axis=2))<42);labels,_=ndimage.label(candidate)
  border=np.unique(np.concatenate([labels[0,:],labels[-1,:],labels[:,0],labels[:,-1]]));a[np.isin(labels,border[border>0]),3]=0
  _CANONICAL=Image.fromarray(a,'RGBA')
 return _CANONICAL
def canonical_part(name,polygon,bbox,z,parent,pivot,role,remove_skin=False,mirror=False,remove_white=False,fade_bottom=None):
 im=get_canonical().copy()
 if remove_skin:
  a=np.array(im);r=a[:,:,0].astype(int);g=a[:,:,1].astype(int);b=a[:,:,2].astype(int);skin=(r>130)&(g>80)&(b>65)&(r>g+12)&(g>b+4)&((r-b)<120)
  region=np.zeros(skin.shape,bool);region[220:560,420:604]=True;a[skin&region,3]=0;im=Image.fromarray(a,'RGBA')
 if remove_white:
  a=np.array(im);rgb=a[:,:,:3].astype(np.int16);white=(rgb.min(axis=2)>205)&((rgb.max(axis=2)-rgb.min(axis=2))<48);region=np.ones(white.shape,bool)
  if remove_white=='arms':region[715:,:]=False
  elif remove_white=='torso':region[:,425:580]=False;region[350:375,600:632]=False
  a[white&region,3]=0;im=Image.fromarray(a,'RGBA')
 im=im.resize((W,H),Image.Resampling.LANCZOS)
 if remove_white:
  a=np.array(im);rgb=a[:,:,:3].astype(np.int16);white=(rgb.min(axis=2)>205)&((rgb.max(axis=2)-rgb.min(axis=2))<48);region=np.ones(white.shape,bool)
  if remove_white=='arms':region[715*S:,:]=False
  elif remove_white=='torso':region[:,425*S:580*S]=False;region[350*S:375*S,600*S:632*S]=False
  a[white&region,3]=0;im=Image.fromarray(a,'RGBA')
 points=[((1024-x if mirror else x)*S,y*S) for x,y in polygon];mask=Image.new('L',(W,H));ImageDraw.Draw(mask).polygon(points,fill=255)
 if fade_bottom:
  start,end=fade_bottom;yy=np.arange(H,dtype=np.float32)[:,None]/S;ramp=np.clip((end-yy)/max(end-start,.001),0,1);mask=Image.fromarray((np.array(mask).astype(np.float32)*ramp).astype(np.uint8),'L')
 mask=mask.filter(ImageFilter.GaussianBlur(.35));im.putalpha(Image.fromarray(np.minimum(np.array(im.getchannel('A')),np.array(mask)).astype(np.uint8),'L'))
 x0,y0,x1,y1=[round(v*S) for v in bbox];im=im.crop((x0,y0,x1,y1))
 if remove_white:
  # Cut away the white-matte fringe itself; recoloring leaves a visible dotted edge.
  a=np.array(im);rgb=a[:,:,:3].astype(np.int16);alpha=a[:,:,3];solid=alpha>8
  edge=solid&~ndimage.binary_erosion(solid,iterations=4)
  neutral=((rgb.max(axis=2)-rgb.min(axis=2))<70)&(rgb.min(axis=2)>45)
  region=np.ones(solid.shape,bool);yy=y0+np.arange(im.height)[:,None];xx=x0+np.arange(im.width)[None,:]
  if remove_white=='arms':region[np.broadcast_to(yy>=715*S,region.shape)]=False
  elif remove_white=='torso':
   region[np.broadcast_to((xx>=425*S)&(xx<580*S),region.shape)]=False;region[(yy>=350*S)&(yy<375*S)&(xx>=600*S)&(xx<632*S)]=False
  a[edge&neutral&region,3]=0;im=Image.fromarray(a,'RGBA')
 im.save(OUT/'registered'/f'{name}.png');im.save(OUT/'derivatives'/f'CANONICAL_{name}.png')
 entries.append({'name':name,'source':'reference_library/assets/modeling/RYO_MOD_fullbody_front_v001.png','derivative':f'artwork/derivatives/CANONICAL_{name}.png','registered_png':f'artwork/registered/{name}.png','enabled_neutral':True,'z':z,'parent':parent,'bbox_ref_xyxy':list(bbox),'master_xy':[x0,y0],'master_size':list(im.size),'rotation_degrees':0,'shoulder_compression_ref':0,'pivot_ref':list(pivot),'pivot_master':[pivot[0]*S,pivot[1]*S],'role':role,'source_polygon_ref':points,'character_side_convention':'L is character-left (viewer-right); R is character-right (viewer-left)'})
def canonical_custom(name,polygon,bbox,z,parent,pivot,role,kind='patch',feather=1.0):
 base=get_canonical().copy()
 if kind=='neck':
  a=np.array(base);mask=np.zeros((1536,1024),np.uint8);chain=np.array([(468,266),(477,278),(493,290),(510,301),(528,290),(544,277),(555,264)],np.int32)
  cv2.polylines(mask,[chain],False,255,5,cv2.LINE_AA);cv2.circle(mask,(511,306),11,255,-1,cv2.LINE_AA);a[:,:,:3]=cv2.inpaint(a[:,:,:3],mask,4,cv2.INPAINT_TELEA);base=Image.fromarray(a,'RGBA')
 im=base.resize((W,H),Image.Resampling.LANCZOS);points=[(x*S,y*S) for x,y in polygon];mask=Image.new('L',(W,H));ImageDraw.Draw(mask).polygon(points,fill=255)
 if kind=='eye_surround':
  outer=Image.new('L',(W,H));ImageDraw.Draw(outer).rectangle((bbox[0]*S,bbox[1]*S,bbox[2]*S,bbox[3]*S),fill=255);mask=Image.fromarray(np.maximum(np.array(outer).astype(int)-np.array(mask).astype(int),0).astype(np.uint8),'L')
 if kind in ('gold','jewelry'):
  a=np.array(im);r=a[:,:,0].astype(int);g=a[:,:,1].astype(int);b=a[:,:,2].astype(int)
  if kind=='gold':color=(r>g+4)&(g>b+4)&(r>65)
  else:gold=(r<238)&(r>g+4)&(g>b+4)&(r>65);green=(g>r+3)&(g>b+3)&(r<190);color=gold|green
  m=np.minimum(np.array(mask),np.where(color,255,0).astype(np.uint8));m=cv2.dilate(m,np.ones((2,2),np.uint8),iterations=1);mask=Image.fromarray(np.minimum(m,np.array(mask)),'L')
 mask=mask.filter(ImageFilter.GaussianBlur(feather*S));im.putalpha(Image.fromarray(np.minimum(np.array(im.getchannel('A')),np.array(mask)).astype(np.uint8),'L'))
 x0,y0,x1,y1=[round(v*S) for v in bbox];im=im.crop((x0,y0,x1,y1));im.save(OUT/'registered'/f'{name}.png');im.save(OUT/'derivatives'/f'CANONICAL_{name}.png')
 entries.append({'name':name,'source':'reference_library/assets/modeling/RYO_MOD_fullbody_front_v001.png','derivative':f'artwork/derivatives/CANONICAL_{name}.png','registered_png':f'artwork/registered/{name}.png','enabled_neutral':True,'z':z,'parent':parent,'bbox_ref_xyxy':list(bbox),'master_xy':[x0,y0],'master_size':list(im.size),'rotation_degrees':0,'shoulder_compression_ref':0,'pivot_ref':list(pivot),'pivot_master':[pivot[0]*S,pivot[1]*S],'role':role,'source_polygon_ref':points,'canonical_mask_kind':kind,'character_side_convention':'L is character-left (viewer-right); R is character-right (viewer-left)'})
# Rear hair and exact canonical hair accessories.
add('short_tail','hair/short_tail.png',(505,154,580,267),4,'head',pivot=(529,157),role='rear short hair tail with independent sway')
add('rear_scalp','hair/rear_scalp_nape.png',(420,54,592,205),5,'head',pivot=(512,76),role='rear scalp behind frontal face')
add('bun','hair/bun.png',(462,24,578,108),6,'head',pivot=(520,75),role='hair bun')
add('construction_hairstick_01','accessories/layers/RYO_ACC_hairstick_01.png',z=7,parent='head',center=(558,49),size=(8,91),angle=55,pivot=(535,72),enabled=False,role='hidden construction hairstick')
add('construction_hairstick_02','accessories/layers/RYO_ACC_hairstick_02.png',z=8,parent='head',center=(556,67),size=(8,91),angle=55,pivot=(535,83),enabled=False,role='hidden construction hairstick')
add('construction_hair_dangler','accessories/layers/RYO_ACC_hair_dangler_01.png',(576,57,586,105),9,'head',pivot=(581,59),enabled=False,role='hidden construction dangler')
canonical_custom('hairstick_01',[(538,60),(545,68),(571,43),(583,40),(584,31),(578,26),(571,30),(569,36)],(536,25,586,72),7,'head',(542,64),'canonical upper gold hairstick inserted into bun',kind='gold',feather=.18)
canonical_custom('hairstick_02',[(548,65),(553,73),(583,61),(595,59),(597,51),(591,47),(584,49),(581,55)],(546,45,599,77),8,'head',(552,69),'canonical lower gold hairstick inserted straight into hair',kind='gold',feather=.18)
canonical_custom('hair_dangler',[(583,57),(594,57),(594,103),(583,103)],(581,55,596,105),9,'head',(589,59),'canonical single dangling hair ornament',kind='gold',feather=.18)
# Feet, legs, construction pieces, and separate canonical neck/chest.
add('shoe_R','body/layers/pump_front_character_R.png',(391,1327,463,1497),18,'leg_R',pivot=(427,1334),role='front pump')
add('shoe_L','body/layers/pump_front_character_L.png',(563,1327,635,1497),19,'leg_L',pivot=(599,1334),role='front pump')
add('construction_pelvis','body/layers/trousers_pelvis_front.png',(382,566,642,735),21.5,'torso',pivot=(512,590),enabled=False,role='hidden construction pelvis')
add('leg_R','body/layers/trousers_leg_front_character_R.png',(370,681,493,1341),22,'pelvis',pivot=(440,690),role='character-right front trouser leg')
add('leg_L','body/layers/trousers_leg_front_character_L.png',(530,681,653,1341),23,'pelvis',pivot=(584,690),role='character-left front trouser leg')
add('construction_forearm_R','body/layers/sleeve_forearm_character_R.png',(306,433,374,731),24,'upper_arm_R',pivot=(352,449),enabled=False,role='hidden construction forearm')
add('construction_forearm_L','body/layers/sleeve_forearm_character_L.png',(650,433,718,731),24.5,'upper_arm_L',pivot=(672,449),enabled=False,role='hidden construction forearm')
add('construction_upper_arm_R','body/layers/sleeve_upper_character_R.png',z=25,parent='torso',center=(359,420),size=(76,240),angle=-4,pivot=(372,302),enabled=False,role='hidden construction upper sleeve')
add('construction_upper_arm_L','body/layers/sleeve_upper_character_L.png',z=26,parent='torso',center=(665,420),size=(76,240),angle=4,pivot=(652,302),enabled=False,role='hidden construction upper sleeve')
add('construction_hand_R','body/layers/hand_dorsal_character_R.png',(298,716,354,859),27,'forearm_R',pivot=(326,724),enabled=False,role='hidden construction hand')
add('construction_hand_L','body/layers/hand_dorsal_character_L.png',(670,716,726,859),28,'forearm_L',pivot=(698,724),enabled=False,role='hidden construction hand')
add('construction_blouse_front','body/layers/blouse_front.png',(401,235,623,608),30,'torso',pivot=(512,260),enabled=False,role='hidden construction blouse')
add('belt','accessories/layers/RYO_ACC_belt_gold_buckle.png',(302,584,722,614),20.5,'pelvis',pivot=(512,599),enabled=False,role='hidden construction belt')
neck_skin=[(478,216),(546,216),(546,239),(556,244),(555,260),(548,267),(550,290),(555,315),(548,330),(536,345),(526,360),(518,380),(511,389),(504,380),(497,360),(488,345),(476,330),(469,315),(474,290),(476,267),(468,260),(468,244),(478,239)]
canonical_custom('neck',neck_skin,(458,210,566,395),31,'torso',(512,225),'standalone canonical neck/chest derivative; jewelry removed; no face or blouse stretching',kind='neck',feather=.25)
add('construction_blazer_R','body/layers/blazer_front_character_R.png',(345,254,500,690),32,'torso',pivot=(490,282),enabled=False,role='hidden construction blazer',top_shift=26)
add('construction_blazer_L','body/layers/blazer_front_character_L.png',(524,254,679,690),33,'torso',pivot=(534,282),enabled=False,role='hidden construction blazer',top_shift=26)
# Visible canonical suit cuts.
arm_upper=[(361,289),(384,292),(392,326),(388,367),(383,409),(399,460),(391,500),(387,525),(329,525),(329,474),(337,430),(344,385),(348,340)]
arm_fore=[(339,470),(397,470),(391,500),(387,520),(384,540),(381,560),(380,580),(377,600),(372,620),(367,640),(362,660),(357,680),(353,700),(349,730),(328,730),(298,730),(295,695),(302,643),(310,590),(318,535),(329,480)]
hand=[(300,716),(330,716),(337,743),(344,774),(350,813),(344,837),(332,858),(319,850),(307,828),(301,803),(298,770)]
torso=[(470,237),(459,246),(447,272),(420,278),(384,286),(362,291),(351,318),(348,360),(357,408),(366,449),(378,477),(373,506),(362,557),(365,657),(402,674),(444,684),(481,683),(512,668),(543,684),(585,681),(627,670),(659,658),(655,566),(646,518),(650,478),(661,442),(670,382),(673,330),(661,291),(637,286),(601,278),(575,268),(563,243),(552,237)]
pelvis_poly=[(390,640),(634,640),(642,655),(645,665),(642,700),(627,752),(556,735),(512,716),(468,735),(397,752),(382,700),(379,665),(382,655)]
canonical_part('canonical_pelvis',pelvis_poly,(360,635,665,760),23.5,'torso',(512,650),'canonical trouser-only hip overlap',remove_white=True)
canonical_part('forearm_R',arm_fore,(288,460,402,738),33.0,'upper_arm_R',(350,480),'canonical character-right forearm',remove_white='arms')
canonical_part('forearm_L',arm_fore,(622,460,736,738),33.05,'upper_arm_L',(674,480),'canonical character-left forearm',mirror=True,remove_white='arms')
canonical_part('upper_arm_R',arm_upper,(320,280,404,535),33.1,'torso',(372,302),'canonical character-right upper sleeve with feathered elbow overlap',remove_white='arms',fade_bottom=(490,525))
canonical_part('upper_arm_L',arm_upper,(620,280,704,535),33.15,'torso',(652,302),'canonical character-left upper sleeve with feathered elbow overlap',mirror=True,remove_white='arms',fade_bottom=(490,525))
canonical_part('hand_R',hand,(292,710,358,866),33.2,'forearm_R',(315,724),'canonical character-right dorsal hand')
canonical_part('hand_L',hand,(666,710,732,866),33.25,'forearm_L',(709,724),'canonical character-left dorsal hand',mirror=True)
canonical_part('torso_garment',torso,(340,228,684,700),32.5,'torso',(512,280),'canonical blazer and blouse with matte-free armpit-to-hip edges',remove_skin=True,remove_white='torso')
canonical_custom('necklace_chain',[(466,263),(471,261),(481,275),(495,286),(510,296),(526,286),(541,274),(552,261),(557,264),(546,280),(529,294),(511,305),(492,294),(477,282)],(464,258,559,307),34,'torso',(512,264),'canonical necklace chain',kind='patch',feather=.12)
canonical_custom('green_pendant',[(502,297),(520,297),(521,316),(501,316)],(500,296,522,317),35,'necklace_chain',(511,301),'canonical green pendant and gold setting',kind='patch',feather=.12)
# Approved canonical face, eyes, mouth, and accessories.
add('face','head/layers/RYO_HEAD_face_base_v001.png',(451,94,565,234),40,'head',pivot=(512,214),role='canonical adult face base')
canonical_custom('nose_detail',[(499,177),(516,177),(516,198),(499,198)],(498,176,517,199),40.5,'head',(507,190),'canonical nose-tip patch',kind='patch',feather=1.0)
add('ear_R','head/layers/RYO_HEAD_ear_R_v001.png',(438,145,462,198),41,'head',pivot=(456,156),role='character-right ear')
add('ear_L','head/layers/RYO_HEAD_ear_L_v001.png',(555,145,580,198),42,'head',pivot=(562,156),role='character-left ear')
canonical_custom('earring_R',[(446,179),(460,179),(460,241),(446,241)],(445,178,461,242),63,'head',(451,183),'canonical character-right slim gold earring',kind='patch',feather=.25)
canonical_custom('earring_L',[(551,179),(566,179),(566,241),(551,241)],(550,178,567,242),64,'head',(560,183),'canonical character-left slim gold earring',kind='patch',feather=.25)
add('sclera_R','head/layers/RYO_HEAD_sclera_R_v001.png',(456,153,500,169),45,'head',pivot=(478,161),role='character-right sclera')
add('sclera_L','head/layers/RYO_HEAD_sclera_L_v001.png',(519,153,561,169),45.5,'head',pivot=(537,161),role='character-left sclera')
iris_shape_R=[(472,153),(485,153),(489,158),(488,166),(484,171),(476,171),(470,167),(468,160)]
iris_shape_L=[(530,153),(542,153),(547,159),(546,166),(542,171),(534,171),(529,167),(527,160)]
canonical_custom('iris_R',iris_shape_R,(450,148,498,177),46,'head',(479,163),'canonical character-right amber iris',kind='eye_iris',feather=.12)
canonical_custom('iris_L',iris_shape_L,(521,148,566,177),46.5,'head',(537,163),'canonical character-left amber iris',kind='eye_iris',feather=.12)
canonical_custom('lash_R',iris_shape_R,(450,148,498,177),47,'head',(478,157),'canonical character-right eye surround',kind='eye_surround',feather=.35)
canonical_custom('lash_L',iris_shape_L,(521,148,566,177),47.5,'head',(537,157),'canonical character-left eye surround',kind='eye_surround',feather=.35)
add('closed_R','head/layers/RYO_HEAD_closed_lid_R_v001.png',(454,148,502,169),48,'head',pivot=(478,157),enabled=False,role='character-right blink swap')
add('closed_L','head/layers/RYO_HEAD_closed_lid_L_v001.png',(518,148,565,169),48.5,'head',pivot=(538,157),enabled=False,role='character-left blink swap')
canonical_custom('brow_R',[(454,137),(498,137),(498,155),(454,155)],(453,136,499,156),49,'head',(479,147),'canonical character-right brow',kind='patch',feather=.8)
canonical_custom('brow_L',[(521,137),(564,137),(564,155),(521,155)],(520,136,565,156),49.5,'head',(538,147),'canonical character-left brow',kind='patch',feather=.8)
canonical_custom('mouth_neutral',[(488,197),(529,197),(529,218),(488,218)],(487,196,530,219),50,'head',(508,206),'exclusive canonical neutral mouth',kind='patch',feather=1.1)
for v,b in {'A':(489,196,525,224),'E':(489,199,525,214),'I':(489,200,525,213),'O':(496,197,518,223),'U':(495,201,519,216)}.items():add('mouth_'+v,f'head/layers/RYO_HEAD_viseme_{v}_v001.png',b,51,'head',pivot=(506.5,205),enabled=False,role=f'exclusive viseme {v} mouth swap')
add('front_fringe','hair/front_fringe.png',(409,48,593,239),60,'head',pivot=(512,64),role='front fringe')
add('temple_R','hair/temple_lock_character_right.png',(418,104,453,253),61,'head',pivot=(443,109),role='character-right temple lock')
add('temple_L','hair/temple_lock_character_left.png',(551,112,581,238),62,'head',pivot=(558,115),role='character-left temple lock')
# Optional effects remain separate and off in neutral.
add('blush_R','effects/layers/RYO_FX_blush_character_R.png',(459,171,495,188),70,'head',pivot=(477,179),enabled=False,role='optional blush')
add('blush_L','effects/layers/RYO_FX_blush_character_L.png',(529,171,565,188),71,'head',pivot=(547,179),enabled=False,role='optional blush')
add('sweat','effects/layers/RYO_FX_sweatdrop.png',(554,121,570,153),72,'head',pivot=(562,123),enabled=False,role='optional sweat')
add('anger','effects/layers/RYO_FX_anger_mark.png',(551,103,580,130),73,'head',pivot=(565,116),enabled=False,role='optional anger')
add('tear_R','effects/layers/RYO_FX_tear_character_R.png',(473,163,483,213),74,'head',pivot=(478,165),enabled=False,role='optional tear')
add('tear_L','effects/layers/RYO_FX_tear_character_L.png',(541,163,551,213),75,'head',pivot=(546,165),enabled=False,role='optional tear')
add('sparkle','effects/layers/RYO_FX_sparkle_cluster.png',(544,88,584,130),76,'head',pivot=(564,108),enabled=False,role='optional sparkle')
entries.sort(key=lambda e:e['z'])
canvas=Image.new('RGBA',(W,H))
for e in entries:
 if e['enabled_neutral']:canvas.alpha_composite(Image.open(ROOT/e['registered_png']).convert('RGBA'),tuple(e['master_xy']))
canvas.save(PRE/'ryoko_neutral_transparent.png')
for e in entries:shutil.copy2(ROOT/e['registered_png'],OUT/'layers'/f"{e['name']}.png")
def on_bg(color):
 bg=Image.new('RGBA',(W,H),color);bg.alpha_composite(canvas);return bg.convert('RGB')
light=on_bg((242,239,232,255));dark=on_bg((24,29,34,255));light.save(PRE/'ryoko_neutral_light.png');dark.save(PRE/'ryoko_neutral_dark.png')
bustbox=(650,20,1390,920);light.crop(bustbox).save(PRE/'ryoko_neutral_bust_light.png');dark.crop(bustbox).save(PRE/'ryoko_neutral_bust_dark.png')
manifest={'canvas_reference':[1024,1536],'canvas_master':[W,H],'scale':2,'side_convention':'L is character-left (viewer-right); R is character-right (viewer-left)','layers':entries}
(MAN/'placement_manifest.json').write_text(json.dumps(manifest,indent=2))
# Genuine OpenRaster package with individual layer images, offsets, visibility and stack order.
ora=OUT/'Ryoko_Neutral_Layered.ora'
with zipfile.ZipFile(ora,'w') as z:
 z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
 for i,e in enumerate(entries):z.write(ROOT/e['registered_png'],f'data/layer{i:03d}.png')
 # ORA's topmost XML layer is drawn first; reverse ascending z order.
 body=[]
 for i in reversed(range(len(entries))):
  e=entries[i];x,y=e['master_xy'];vis='visible' if e['enabled_neutral'] else 'hidden'
  body.append(f'<layer name="{e["name"]}" src="data/layer{i:03d}.png" x="{x}" y="{y}" visibility="{vis}"/>')
 stack=f'<image w="{W}" h="{H}" name="Ryoko Neutral"><stack name="Ryoko">'+''.join(body)+'</stack></image>'
 z.writestr('stack.xml',stack);z.write(PRE/'ryoko_neutral_transparent.png','mergedimage.png')
 thumb=canvas.copy();thumb.thumbnail((256,384));from io import BytesIO
 b=BytesIO();thumb.save(b,'PNG');z.writestr('Thumbnails/thumbnail.png',b.getvalue())
review=Image.new('RGB',(1920,1320),(30,34,38));d=ImageDraw.Draw(review)
try:font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',26)
except:font=ImageFont.load_default()
review.paste(light.resize((660,990)),(35,90));review.paste(dark.resize((660,990)),(725,90));review.paste(light.crop(bustbox).resize((475,575)),(1400,90))
d.text((35,30),'RYOKO — REGISTERED 2D NEUTRAL / LIGHT',font=font,fill=(240,240,240));d.text((725,30),'DARK BACKGROUND',font=font,fill=(240,240,240));d.text((1400,30),'FACE / NECK DETAIL',font=font,fill=(240,240,240));d.text((1400,710),f'{sum(e["enabled_neutral"] for e in entries)} enabled layers / {len(entries)} registered',font=font,fill=(210,220,215))
review.save(PRE/'ryoko_neutral_review.png')
print(json.dumps({'layers':len(entries),'enabled':sum(e['enabled_neutral'] for e in entries),'ora':str(ora),'previews':str(PRE)},indent=2))

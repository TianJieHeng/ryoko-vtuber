#!/usr/bin/env python3
"""Rebuild Ryoko's canonical neutral as genuine registered 2D cutout layers."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage
import numpy as np
import json, shutil, zipfile

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT.parent/'ryoko-vtuber'/'avatar_build_assets'
REF=ASSETS/'reference_library/assets/modeling/RYO_MOD_fullbody_front_v001.png'
ART=ROOT/'artwork'; REG=ART/'registered'; LAY=ART/'layers'; DER=ART/'derivatives'
PRE=ROOT/'previews'; MAN=ROOT/'manifest'
for p in (REG,LAY,DER,PRE,MAN): p.mkdir(parents=True,exist_ok=True)
S=2; SIZE=(2048,3072)
entries=[]; coverage=np.zeros((3072,2048),bool)

def remove_background(im):
    a=np.array(im.convert('RGBA')); rgb=a[:,:,:3].astype(np.int16)
    candidate=(rgb.min(2)>232)&((rgb.max(2)-rgb.min(2))<24)
    labels,_=ndimage.label(candidate)
    border=np.unique(np.concatenate([labels[0,:],labels[-1,:],labels[:,0],labels[:,-1]]))
    background_labels=set(border[border>0].tolist())
    # These two enclosed near-white components are background wedges between
    # the sleeves and jacket, not blouse artwork. Seed well inside each wedge
    # so only those connected components are removed.
    for x,y in ((397,500),(615,500)):
        label=int(labels[y,x])
        if label>0: background_labels.add(label)
    a[np.isin(labels,list(background_labels)),3]=0
    a[:,:,3]=np.where(a[:,:,3]<10,0,a[:,:,3]).astype(np.uint8)
    return Image.fromarray(a,'RGBA')

canonical=remove_background(Image.open(REF).convert('RGB')).resize(SIZE,Image.Resampling.LANCZOS)
# Remove subvisible resampling residue inside fully transparent cutouts.
canonical.putalpha(canonical.getchannel('A').point(lambda v: 0 if v<16 else v))
canonical.save(DER/'canonical_fullbody_background_removed.png')
ca=np.array(canonical.getchannel('A'))

def mask_rect(box):
    m=Image.new('L',SIZE,0); ImageDraw.Draw(m).rectangle(tuple(v*S for v in box),fill=255); return m

def mask_poly(points):
    m=Image.new('L',SIZE,0); ImageDraw.Draw(m).polygon([(x*S,y*S) for x,y in points],fill=255); return m

def subtract(mask,*cuts):
    a=np.array(mask).astype(np.int16)
    for cut in cuts: a-=np.array(cut).astype(np.int16)
    return Image.fromarray(np.clip(a,0,255).astype(np.uint8),'L')

def ellipse(box):
    m=Image.new('L',SIZE,0); ImageDraw.Draw(m).ellipse(tuple(v*S for v in box),fill=255); return m

def pivots(parent,pivot):
    defaults={'root':(0,0),'torso':(512,280),'head':(512,250),'pelvis':(512,650)}
    px,py=pivot; bx,by=defaults[parent]
    return {'parent':parent,'pivot_ref':[px,py],'pivot_master':[px*S,py*S]}

def add_image(name,im,z,parent='torso',pivot=(512,280),enabled=True,role='',source=''):
    a=np.array(im.getchannel('A')); enabled=bool(enabled and np.any(a>0))
    if not enabled and not np.any(a>0):
        # Keep disabled alternate entries with a valid 1-pixel transparent image.
        im=Image.new('RGBA',(2,2)); box=(0,0,2,2)
    else:
        b=im.getchannel('A').getbbox(); box=b; im=im.crop(b)
    path=REG/f'{name}.png'; im.save(path); shutil.copy2(path,LAY/f'{name}.png')
    e={'name':name,'source':source or str(REF.relative_to(ASSETS)),'registered_png':f'artwork/registered/{name}.png',
       'enabled_neutral':enabled,'z':z,'master_xy':[box[0],box[1]],'master_size':list(im.size),
       'role':role,**pivots(parent,pivot)}
    entries.append(e)
    return e

def add_canonical(name,mask,z,parent='torso',pivot=(512,280),enabled=True,role='',holes=()):
    global coverage
    m=subtract(mask,*holes) if holes else mask
    a=np.minimum(ca,np.array(m)).astype(np.uint8)
    im=canonical.copy(); im.putalpha(Image.fromarray(a,'L'))
    if enabled: coverage|=a>0
    return add_image(name,im,z,parent,pivot,enabled,role)

def add_alternate(name,path,target,z,parent='head',pivot=(512,250),max_size=None):
    im=Image.open(ASSETS/path).convert('RGBA'); b=im.getchannel('A').getbbox(); im=im.crop(b)
    if max_size: im.thumbnail(max_size,Image.Resampling.LANCZOS)
    x,y,w,h=target
    scale=min(w*S/im.width,h*S/im.height)
    im=im.resize((max(1,round(im.width*scale)),max(1,round(im.height*scale))),Image.Resampling.LANCZOS)
    full=Image.new('RGBA',SIZE); full.alpha_composite(im,(round((x+w/2)*S-im.width/2),round((y+h/2)*S-im.height/2)))
    return add_image(name,full,z,parent,pivot,False,'registered alternate control drawing',str(path))

head_rect=mask_rect((390,15,620,285))
face_poly=mask_poly([(468,91),(551,91),(568,137),(557,197),(512,239),(468,207),(447,157)])
eye_r=mask_rect((447,137,501,177)); eye_l=mask_rect((519,137,573,177))
iris_r=ellipse((461,142,489,174)); iris_l=ellipse((527,142,555,174))
mouth_box=mask_rect((484,191,539,221))

# Rear head and accessories.
bun=mask_rect((445,20,578,102))
fringe=mask_poly([(417,52),(577,43),(596,135),(567,207),(544,183),(512,105),(480,183),(444,231),(408,180)])
temple_r=mask_poly([(408,89),(466,96),(457,241),(428,263),(404,181)])
temple_l=mask_poly([(548,91),(592,84),(602,190),(566,257),(543,220)])
short_tail=mask_poly([(540,173),(585,165),(589,244),(556,274),(540,235)])
rear=subtract(head_rect,face_poly,bun,fringe,temple_r,temple_l,short_tail)
add_canonical('rear_hair',rear,10,'head',(512,220),role='canonical rear hair and scalp')
add_canonical('bun',bun,11,'head',(512,70),role='canonical bun')
add_canonical('short_tail',short_tail,12,'head',(560,185),role='canonical short rear tail')
add_canonical('neck',mask_rect((458,210,566,395)),31,'torso',(512,225),role='standalone canonical neck/chest derivative; no face or blouse stretching')
add_canonical('face',face_poly,32,'head',(512,250),role='canonical adult face with independent eye and mouth openings',holes=(eye_r,eye_l,mouth_box))
add_canonical('ear_R',mask_rect((431,145,466,207)),33,'head',(451,176),role='character-right ear')
add_canonical('ear_L',mask_rect((551,145,578,207)),33,'head',(562,176),role='character-left ear')

# Eyes: exact canonical patches; iris openings prevent double pupils during gaze.
add_canonical('sclera_R',eye_r,34,'head',(474,157),holes=(iris_r,),role='canonical character-right eye surround')
add_canonical('sclera_L',eye_l,34,'head',(546,157),holes=(iris_l,),role='canonical character-left eye surround')
add_canonical('iris_R',iris_r,35,'head',(475,158),role='canonical amber character-right iris')
add_canonical('iris_L',iris_l,35,'head',(541,158),role='canonical amber character-left iris')
add_canonical('lash_R',eye_r,36,'head',(474,157),holes=(iris_r,),role='canonical character-right lash and eyelid')
add_canonical('lash_L',eye_l,36,'head',(546,157),holes=(iris_l,),role='canonical character-left lash and eyelid')
add_canonical('brow_R',mask_rect((449,127,501,148)),43,'head',(475,137),role='canonical character-right brow')
add_canonical('brow_L',mask_rect((520,127,568,148)),43,'head',(544,137),role='canonical character-left brow')
add_alternate('closed_R','head/layers/RYO_HEAD_closed_lid_R_v001.png',(447,137,54,40),38,max_size=(160,120))
add_alternate('closed_L','head/layers/RYO_HEAD_closed_lid_L_v001.png',(519,137,54,40),38,max_size=(160,120))

# Mouths are exclusive alternates; only canonical neutral lips are enabled at rest.
add_canonical('mouth_neutral',mouth_box,39,'head',(512,206),role='exact canonical neutral mouth')
for v in 'AEIOU':
    add_alternate(f'mouth_{v}',f'head/layers/RYO_HEAD_viseme_{v}_v001.png',(485,187,54,39),39,max_size=(180,135))

# Front hair and exact canonical accessories.
add_canonical('front_fringe',fringe,45,'head',(512,100),role='canonical front fringe')
add_canonical('temple_R',temple_r,46,'head',(438,105),role='character-right temple lock')
add_canonical('temple_L',temple_l,46,'head',(570,105),role='character-left longer temple lock')
add_canonical('hairstick_01',mask_poly([(529,63),(566,27),(578,25),(581,37),(544,76)]),48,'head',(541,67),role='canonical gold hairstick 1')
add_canonical('hairstick_02',mask_poly([(544,77),(578,46),(590,44),(593,56),(555,88)]),48,'head',(552,77),role='canonical gold hairstick 2')
add_canonical('hair_dangler',mask_rect((570,45,596,112)),49,'head',(583,55),role='canonical hair ornament dangler')
add_canonical('earring_R',mask_rect((435,169,466,245)),47,'head',(451,181),role='canonical character-right slim earring')
add_canonical('earring_L',mask_rect((545,166,572,245)),47,'head',(558,181),role='canonical character-left slim earring')

# Body and clothing, all cut from the same registered frontal master.
torso=mask_poly([(357,231),(666,231),(691,360),(674,548),(651,690),(563,711),(512,690),(460,711),(363,690),(343,548),(330,360)])
add_canonical('torso_garment',torso,30,'torso',(512,300),role='canonical black trouser suit and centered white blouse')
add_canonical('canonical_pelvis',mask_rect((350,650,670,790)),24,'pelvis',(512,680),role='canonical trouser pelvis and clean hip coverage')
add_canonical('belt_gold_buckle',mask_rect((480,580,540,625)),38,'torso',(510,603),role='canonical belt and gold buckle')
add_canonical('necklace_chain',mask_rect((460,265,560,315)),40,'torso',(512,285),role='canonical gold necklace chain')
add_canonical('green_pendant',mask_rect((494,286,526,322)),41,'torso',(510,298),role='canonical green pendant')

upper_r=mask_poly([(350,278),(392,285),(392,472),(372,574),(333,555),(326,410)])
upper_l=mask_poly([(632,285),(674,278),(698,410),(691,555),(652,574),(632,472)])
fore_r=mask_poly([(330,500),(381,515),(365,697),(350,747),(292,736),(300,624)])
fore_l=mask_poly([(643,515),(694,500),(724,624),(732,736),(674,747),(659,697)])
hand_r=mask_poly([(294,716),(351,716),(355,816),(337,866),(305,842),(292,781)])
hand_l=mask_poly([(673,716),(730,716),(732,781),(719,842),(687,866),(669,816)])
add_canonical('upper_arm_R',upper_r,34,'torso',(370,305),role='full canonical character-right upper sleeve')
add_canonical('upper_arm_L',upper_l,34,'torso',(654,305),role='full canonical character-left upper sleeve')
add_canonical('forearm_R',fore_r,35,'torso',(354,535),role='full canonical character-right forearm and cuff')
add_canonical('forearm_L',fore_l,35,'torso',(670,535),role='full canonical character-left forearm and cuff')
add_canonical('hand_R',hand_r,37,'torso',(326,735),role='canonical character-right complete hand')
add_canonical('hand_L',hand_l,37,'torso',(698,735),role='canonical character-left complete hand')

leg_r=mask_poly([(356,702),(510,702),(500,925),(476,1130),(462,1342),(393,1342),(376,1130),(365,925)])
leg_l=mask_poly([(514,702),(668,702),(659,925),(648,1130),(631,1342),(562,1342),(548,1130),(524,925)])
add_canonical('trousers_leg_front_R',leg_r,22,'pelvis',(450,710),role='canonical character-right trouser leg')
add_canonical('trousers_leg_front_L',leg_l,22,'pelvis',(574,710),role='canonical character-left trouser leg')
add_canonical('shoe_R',mask_rect((385,1315,470,1510)),26,'pelvis',(430,1335),role='canonical character-right ankle and black heel')
add_canonical('shoe_L',mask_rect((554,1315,640,1510)),26,'pelvis',(594,1335),role='canonical character-left ankle and black heel')

# Any source foreground not explicitly partitioned becomes a hidden registered underlap.
missing=(ca>0)&~coverage
if np.any(missing):
    im=canonical.copy(); im.putalpha(Image.fromarray(np.where(missing,ca,0).astype(np.uint8),'L'))
    add_image('registration_underlap',im,5,'root',(0,0),True,'hidden canonical overlap completion for unmatched edge pixels')

# Optional effects remain independent and off in neutral.
fx=[('blush_R','RYO_FX_blush_character_R.png',(449,169,38,24)),('blush_L','RYO_FX_blush_character_L.png',(536,169,38,24)),
    ('tear_R','RYO_FX_tear_character_R.png',(464,164,22,54)),('tear_L','RYO_FX_tear_character_L.png',(538,164,22,54)),
    ('sweat','RYO_FX_sweatdrop.png',(566,105,25,42)),('anger','RYO_FX_anger_mark.png',(548,91,34,32)),
    ('sparkle','RYO_FX_sparkle_cluster.png',(575,125,55,55))]
for name,file,target in fx: add_alternate(name,'effects/layers/'+file,target,60,max_size=(150,150))

entries.sort(key=lambda e:e['z'])
manifest={'canvas_reference':[1024,1536],'canvas_master':[2048,3072],'scale':2,'character_left':'viewer-right',
          'source_reference':'reference_library/assets/modeling/RYO_MOD_fullbody_front_v001.png',
          'source_preserved':True,'derivatives_separate':True,'neck_resolution':'standalone canonical neck derivative; no stretching',
          'layers':entries}
(MAN/'placement_manifest.json').write_text(json.dumps(manifest,indent=2))

# Composite in real layer order.
def composite(bg=None):
    can=Image.new('RGBA',SIZE)
    for e in entries:
        if not e['enabled_neutral']: continue
        can.alpha_composite(Image.open(ROOT/e['registered_png']).convert('RGBA'),tuple(e['master_xy']))
    if bg is None: return can
    out=Image.new('RGBA',SIZE,bg); out.alpha_composite(can); return out.convert('RGB')

transparent=composite(); transparent.save(PRE/'ryoko_neutral_transparent.png')
composite((242,239,232,255)).save(PRE/'ryoko_neutral_light.png')
composite((24,29,34,255)).save(PRE/'ryoko_neutral_dark.png')
transparent.resize((1024,1536),Image.Resampling.LANCZOS).save(PRE/'ryoko_neutral_transparent_1024.png')

# Genuine OpenRaster document with individual layer PNGs and offsets.
merged=PRE/'ryoko_neutral_transparent.png'; thumb=transparent.copy(); thumb.thumbnail((256,256),Image.Resampling.LANCZOS)
stack=['<?xml version="1.0" encoding="UTF-8"?>','<image version="0.0.3" w="2048" h="3072" name="Ryoko Neutral Layered">','<stack name="Ryoko">']
for i,e in enumerate(reversed(entries)):
    vis='visible' if e['enabled_neutral'] else 'hidden'
    stack.append(f'<layer name="{e["name"]}" src="data/layer{i:03d}.png" x="{e["master_xy"][0]}" y="{e["master_xy"][1]}" visibility="{vis}" composite-op="svg:src-over"/>')
stack+=['</stack>','</image>']
with zipfile.ZipFile(ART/'Ryoko_Neutral_Layered.ora','w') as z:
    z.writestr(zipfile.ZipInfo('mimetype'),'image/openraster',compress_type=zipfile.ZIP_STORED)
    z.writestr('stack.xml',''.join(stack)); z.write(merged,'merged_image.png')
    import io
    b=io.BytesIO(); thumb.save(b,'PNG'); z.writestr('Thumbnails/thumbnail.png',b.getvalue())
    for i,e in enumerate(reversed(entries)): z.write(ROOT/e['registered_png'],f'data/layer{i:03d}.png')

# Registration proof: the layered composite must reproduce the canonical foreground.
base=np.array(canonical)[:,:,:3].astype(np.int16); out=np.array(transparent)[:,:,:3].astype(np.int16)
alpha=np.array(transparent.getchannel('A')); both=(ca>0)&(alpha>0)
report={'layers_total':len(entries),'layers_enabled_neutral':sum(e['enabled_neutral'] for e in entries),
        'canonical_foreground_pixels':int((ca>0).sum()),'missing_foreground_pixels':int(((ca>0)&(alpha==0)).sum()),
        'extra_foreground_pixels':int(((ca==0)&(alpha>0)).sum()),
        'mean_abs_rgb_difference_shared_pixels':float(np.abs(base-out).mean(axis=2)[both].mean()) if both.any() else None,
        'ora':'artwork/Ryoko_Neutral_Layered.ora'}
(MAN/'neutral_validation.json').write_text(json.dumps(report,indent=2)); print(json.dumps(report,indent=2))

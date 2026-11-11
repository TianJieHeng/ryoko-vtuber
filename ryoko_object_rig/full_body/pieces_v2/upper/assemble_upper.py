#!/usr/bin/env python3
"""Individual artwork assembly study. Never uses a full-body composite as art."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,math
HERE=Path(__file__).resolve().parent; REPO=HERE.parents[3]; RAW=REPO/'avatar_build_assets'; ASSETS=HERE/'assets';ASSETS.mkdir(exist_ok=True)
records=[]
old=ASSETS/'neck_skin_partial.png'
if old.exists():old.unlink()
def add(name,source,scale,pivot,target,parent,z,angle=0,mask=None):
 im=Image.open(REPO/source).convert('RGBA');a=np.array(im); a[a[:,:,3]<=10,3]=0
 if mask is not None:
  m=Image.new('L',im.size);ImageDraw.Draw(m).polygon(mask,fill=255);a[:,:,3]=np.minimum(a[:,:,3],np.array(m))
 im=Image.fromarray(a);box=im.getbbox();im=im.crop(box)
 deformation=None
 if name.startswith('blazer_'):
  # Fit the independent open jacket panel; no rotation of its shoulder edge.
  # Narrow the collar end gradually to the waist while retaining all art.
  from scipy.ndimage import map_coordinates
  src=np.array(im);h,w=src.shape[:2];ow=round(w*.94)
  yy,xx=np.indices((h,ow),dtype=float);taper=.25*np.clip(1-yy/(h*.60),0,1)
  dest_x=xx/.94; offset=w*taper if name.endswith('_L') else 0
  source_x=(dest_x-offset)/(1-taper)
  warped=np.stack([map_coordinates(src[:,:,c],[yy,source_x],order=1,mode='constant',cval=0) for c in range(4)],2).astype('uint8')
  im=Image.fromarray(warped);deformation={'method':'rowwise horizontal panel fit','base_width_ratio':.94,'collar_width_ratio':.75,'fade_to_full_width_at_height_fraction':.60,'anchored_outer_edge':'left' if name.endswith('_R') else 'right'}
 im.save(ASSETS/(name+'.png'))
 size=[im.width*scale,im.height*scale]; pv=[size[0]*pivot[0],size[1]*pivot[1]]
 records.append(dict(id=name,file=str((ASSETS/(name+'.png')).relative_to(REPO/'ryoko_object_rig')),source=source,source_sha256=hashlib.sha256((REPO/source).read_bytes()).hexdigest(),crop=list(box),size=list(im.size),scale=[scale,scale],position=[target[0]-pv[0],target[1]-pv[1]],pivot=pv,pivot_space='scaled cropped pixels',target_pivot=target,parent=parent,z=z,rotation_degrees=angle,deformation=deformation,alpha_cleanup='Discard alpha <=10 outliers; preserve other alpha and RGB.'))
b='avatar_build_assets/body/layers/'
add('blouse',b+'blouse_front.png',.38,[.5,0],[512,245],'chest',10)
add('blazer_R',b+'blazer_front_character_R.png',.477,[1,0],[513,250],'chest',20)
add('blazer_L',b+'blazer_front_character_L.png',.477,[0,0],[513,250],'chest',21)
for side,sign,x in [('R',1,372),('L',-1,652)]:
 add('upper_arm_'+side,b+'sleeve_upper_character_'+side+'.png',.30,[.32 if side=='R' else .68,.06],[x,302],'shoulder_'+side,15)
 add('forearm_'+side,b+'sleeve_forearm_character_'+side+'.png',.24,[.5,.03],[374 if side=='R' else 650,530],'elbow_'+side,16,sign*14)
 add('hand_'+side,b+'hand_dorsal_character_'+side+'.png',.21,[.5,.02],[325 if side=='R' else 699,725],'wrist_'+side,14,sign*10)
a='avatar_build_assets/accessories/layers/'
add('necklace_chain',a+'RYO_ACC_necklace_chain.png',.065,[.5,0],[512,268],'chest',30)
add('necklace_pendant',a+'RYO_ACC_green_pendant.png',.04,[.5,0],[512,318],'chest',31)
# Complete only the hidden upper edge of the SAME skin part. Repeat its
# existing top shadow/skin scanline upward 36 source pixels (12.24 canvas px).
# Original pixels at y>=720 are untouched; this is not another covering sprite.
skin_source=HERE/'sources/neck_skin_working_source.png'
skin=Image.open(skin_source).convert('RGBA');skin_array=np.array(skin)
skin_array[684:720,484:649]=skin_array[720:721,484:649]
completed_source=HERE/'sources/neck_skin_completed_source.png'
Image.fromarray(skin_array).save(completed_source)
add('neck_skin','ryoko_object_rig/full_body/pieces_v2/upper/sources/neck_skin_completed_source.png',.34,[.5,0],[510,221.76],'neck',11,mask=[(484,684),(648,684),(648,720),(650,790),(670,840),(670,900),(651,936),(664,960),(648,1000),(630,1040),(604,1100),(580,1160),(562,1188),(548,1160),(522,1100),(496,1040),(478,1000),(466,960),(478,936),(451,900),(451,840),(478,790),(484,720)])
records[-1]['hidden_area_completion']={'source_rows':[684,720],'method':'Extend original top skin/shadow scanline y720 upward 36 source pixels within x484..648; no original visible pixels replaced.','canvas_extension_px':12.24,'original_visible_top_y':234,'status':'New unapproved completion; verify live head tilt endpoints.'}
records[-1]['ownership_note']='Skin overlays the rear collar band from the blouse, without importing collar pixels; front opening remains separate blouse artwork.'
records[-1]['provenance']='sources/provenance.json: new compatible edited skin, not original approved artwork.'
manifest=dict(canvas=[1024,1536],status='registration study with new compatible edited skin; not user-approved or motion-certified',layers=records,limitations=['Neck skin uses a new jewelry-removed compatible edit plus original lower skin, explicitly masked to exclude clothing. Requires user visual approval.','Inspect neck-to-head and lower chest joins in the integrated assembly before claiming completion.','Independent pieces are registered approximately. Blazer panels use a documented rowwise fitting deformation rather than rotated shoulder flare; fitting still needs integrated review. Elbow/wrist overlaps need bounded motion verification.','Head is not in this fragment; preserve existing approved live head.','Front/back and alternate hand/shoe views are not stacked.'])
(HERE/'registration_fragment.json').write_text(json.dumps(manifest,indent=2)+'\n')
# Draw each piece using its own transform; no surrogate portrait or body.
canvas=Image.new('RGBA',(1024,1536))
for e in sorted(records,key=lambda e:e['z']):
 im=Image.open(REPO/'ryoko_object_rig'/e['file']);sc=e['scale'][0];im=im.resize((round(im.width*sc),round(im.height*sc)),Image.Resampling.LANCZOS)
 # Place on full canvas then rotate around the declared canvas pivot.
 layer=Image.new('RGBA',canvas.size);layer.alpha_composite(im,tuple(round(n) for n in e['position']))
 layer=layer.rotate(-e['rotation_degrees'],Image.Resampling.BICUBIC,center=tuple(e['target_pivot']));canvas.alpha_composite(layer)
canvas.save(HERE/'upper_assembly_incomplete.png')
for name,bg in [('light','#eeece5'),('dark','#20252b')]:
 out=Image.new('RGBA',canvas.size,bg);out.alpha_composite(canvas);out.save(HERE/('upper_'+name+'.png'))
# Isolated true cuts for ownership review.
out=Image.new('RGB',(1200,900),'#888888');draw=ImageDraw.Draw(out)
for i,e in enumerate(records):
 im=Image.open(REPO/'ryoko_object_rig'/e['file']);im.thumbnail((180,250));x=(i%6)*200;y=(i//6)*300;out.paste(im,(x,y+30),im);draw.text((x+3,y+3),e['id'],fill='white')
out.save(HERE/'isolated_parts.png')
print('Wrote',len(records),'individual parts, registration and INCOMPLETE study.')

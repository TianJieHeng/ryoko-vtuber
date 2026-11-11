#!/usr/bin/env python3
"""Static neutral sleeve registration from four raw source cutouts; no new pixels painted."""
from pathlib import Path
import json, hashlib, math
import numpy as np
from PIL import Image, ImageDraw
from scipy.interpolate import PchipInterpolator
from scipy.ndimage import map_coordinates
HERE=Path(__file__).resolve().parent; BODY=HERE.parent; RIG=BODY.parent; REPO=RIG.parent
C=(1024,1536)
manifest=json.loads((BODY/'registration.json').read_text()); frame=json.loads((BODY/'review/transform_samples.json').read_text())['frames'][0]
records=[];parts={}
def place(canvas,im,v):
 a,b,c,d,x,y=v; inv=np.linalg.inv([[a,c,x],[b,d,y],[0,0,1]])
 canvas.alpha_composite(im.transform(canvas.size,Image.Transform.AFFINE,tuple(inv[:2].flatten()),Image.Resampling.BICUBIC))
def load(name):
 p=REPO/'avatar_build_assets/body/layers'/name; a=np.array(Image.open(p).convert('RGBA'));a[a[:,:,3]<=10,3]=0
 return p,a

def record(id,source,im,pos,parent,z,extra):
 file=HERE/(id+'_candidate.png'); im.save(file)
 e=dict(id=id,file=str(file.relative_to(RIG)),source=str(source.relative_to(REPO)),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),position=pos,scale=[1,1],rotation_degrees=0,parent=parent,z=z,size=list(im.size),alpha_bounds=list(im.getbbox()),**extra)
 records.append(e);parts[id]=(im,[1,0,0,1,*pos])

# Reference elbow center R ~354,535 (outer332, inner381); wrist ~323,725.
# Keep shoulders and wrist/hand assembly fixed; correct the elbow between them.
source_y=np.array([76,400,700,780,850.]);target_y=np.array([286.7,386,500,530,553.])
shifts=np.array([0,-4,-20,-26,-29.]);widths=np.array([1,1,.97,.96,.95])
for side in ['R','L']:
 p,a=load('sleeve_upper_character_'+side+'.png');h,w=a.shape[:2]
 # Only this source's construction opening is excluded. No substitute cover sprite.
 # Across the source, the lower fold edge is diagonal; use that seam as the join.
 syy,sxx=np.indices((h,w));rx=sxx if side=='R' else 413-sxx
 seam=np.interp(rx,[70,110,165,215,260,310,350],[806,810,820,833,846,850,850])
 weight=np.clip((seam-syy)/8,0,1)
 cut=a.copy();cut[:,:,3]=(cut[:,:,3]*weight).astype('uint8');Image.fromarray(cut).save(HERE/('upper_'+side+'_source_cut.png'))
 yy,xx=np.indices(C[::-1],dtype=float)
 sy=PchipInterpolator(target_y,source_y,extrapolate=False)(np.clip(yy,target_y[0],target_y[-1]))
 dx=PchipInterpolator(source_y,shifts)(sy);ws=PchipInterpolator(source_y,widths)(sy)
 # Original shoulder alignment is unchanged. Left is its own source artwork.
 center=190 if side=='R' else 223
 original_left=346.944 if side=='R' else 598.756;crop_left=79 if side=='R' else 73
 basecenter=original_left+(center-crop_left)*.30
 targetcenter=basecenter+(dx if side=='R' else -dx)
 sx=center+(xx-targetcenter)/(.30*ws)
 out=np.stack([map_coordinates(cut[:,:,c],[sy,sx],order=1,mode='constant',cval=0) for c in range(4)],2).astype('uint8')
 out[(yy<target_y[0])|(yy>target_y[-1]),3]=0
 im=Image.fromarray(out);box=im.getbbox();im=im.crop(box)
 record('upper_arm_'+side,p,im,list(box[:2]),'shoulder_'+side,-185,dict(alpha_cleanup='Discard alpha <=10 outliers.',source_cut=str((HERE/('upper_'+side+'_source_cut.png')).relative_to(RIG)),source_cut_seam_R_xy=[[70,806],[110,810],[165,820],[215,833],[260,846],[310,850],[350,850]],source_cut_mirror='x_L=413-x_R' if side=='L' else None,source_y=source_y.tolist(),target_y=target_y.tolist(),source_x_scale=.30,lower_shift_R=shifts.tolist(),width_ratio=widths.tolist(),method='Source alpha cut at last painted fold, excluding artificial open tube; rowwise register original RGB/alpha from shoulder to real elbow.'))

 # Register actual forearm fold, not the top construction cut, to the elbow.
 p,a=load('sleeve_forearm_character_'+side+'.png')
 # Discard surplus construction overlap above the elbow and retain a rounded
 # hidden tab. This avoids a long extra outer edge peeking beside the upper arm.
 fy,fx=np.indices(a.shape[:2]); fc=190 if side=='R' else 176
 top_seam=330+70*np.clip(abs(fx-fc)/110,0,1)**2
 a[:,:,3]=(a[:,:,3]*np.clip((fy-top_seam)/8,0,1)).astype('uint8')
 # Open the cuff at its existing painted inner rim. The gray closed ellipse
 # and its bottom construction rim are excluded, never painted over.
 cuff_center=190 if side=='R' else 198
 cuff_edge=(899 if side=='R' else 901)+17*((fx-cuff_center)/77)**2
 a[:,:,3]=(a[:,:,3]*np.clip(cuff_edge-fy,0,1)).astype('uint8')
 source_elbow=np.array([185.,400.]) if side=='R' else np.array([179.,400.])
 source_wrist=np.array([188.,925.]) if side=='R' else np.array([200.,925.])
 elbow=np.array([354.,532.]) if side=='R' else np.array([670.,532.])
 wrist=np.array([325.,725.]) if side=='R' else np.array([699.,725.])
 v=wrist-elbow;delta=source_wrist-source_elbow;scale_x=.30
 scale_y=float(math.sqrt(float(v@v)-(delta[0]*scale_x)**2)/delta[1])
 angle=math.atan2(v[1],v[0])-math.atan2(delta[1]*scale_y,delta[0]*scale_x)
 rot=np.array([[math.cos(angle),-math.sin(angle)],[math.sin(angle),math.cos(angle)]])
 mat=rot@np.diag([scale_x,scale_y]);origin=elbow-mat@source_elbow
 affine=[float(mat[0,0]),float(mat[1,0]),float(mat[0,1]),float(mat[1,1]),*origin.tolist()]
 source_im=Image.fromarray(a);source_im.save(HERE/('forearm_'+side+'_source_cut.png'))
 temp=Image.new('RGBA',C);place(temp,source_im,affine);box=temp.getbbox();im=temp.crop(box)
 record('forearm_'+side,p,im,list(box[:2]),'elbow_'+side,-186,dict(cuff_opening_cut={'center_x':cuff_center,'edge_center_y':899 if side=='R' else 901,'edge_formula':'center_y+17*((x-center_x)/77)^2','method':'Discard gray inner ellipse and lower construction rim at painted opening. Wrist enters behind white cuff.'},source_cut_top='Rounded overlap tab: y=330+70*min(abs(x-center)/110,1)^2; 8px source feather.',source_landmarks_xy=[source_elbow.tolist(),source_wrist.tolist()],target_landmarks_xy=[elbow.tolist(),wrist.tolist()],source_affine_abcdxy=affine,source_scale=[scale_x,scale_y],source_rotation_degrees=math.degrees(angle),method='Register painted elbow fold y400 and original cuff-end landmark y925 to elbow and wrist; source opening is cut at its painted inner rim. Retain top construction overlap below upper sleeve owner; forearm drawn behind upper sleeve.'))

# Re-derive original hands directly from raw sources, never a prior candidate.
# Apply the inspected absolute 10px underlap to the original measured bind; never to a prior candidate.
for side in ['R','L']:
 p,a=load('hand_dorsal_character_'+side+'.png')
 source_im=Image.fromarray(a);source_crop=list(source_im.getbbox());im=source_im.crop(source_crop)
 angle=math.radians(10 if side=='R' else -10);sc=.21
 px,py=im.width*sc*.5,im.height*sc*.02;tx=325 if side=='R' else 699;ty=725
 v=[sc*math.cos(angle),sc*math.sin(angle),-sc*math.sin(angle),sc*math.cos(angle),tx-math.cos(angle)*px+math.sin(angle)*py,ty-math.sin(angle)*px-math.cos(angle)*py-10]
 v=([0.206809610128403,0.0364661179482937,-0.0364661179482937,0.206809610128403,297.790588378906,707.865112304688] if side=='R' else [0.206809610128403,-0.0364661179482937,0.0364661179482937,0.206809610128403,670.991271972656,717.601623535156])
 temp=Image.new('RGBA',C);place(temp,im,v);box=temp.getbbox();im=temp.crop(box)
 record('hand_'+side,p,im,list(box[:2]),'wrist_'+side,-187,dict(source_crop=source_crop,source_affine_on_cropped_abcdxy=v,source_scale=[sc,sc],source_rotation_degrees=math.degrees(angle),method='Original cleaned raw hand translated upward 10px from its measured neutral bind into the opened cuff; unchanged proportions, fingers and neutral angle.'))

# Original pre-correction sleeve/hand registrations define the before proof,
# independently of any subsequently integrated candidate runtime manifest.
original=json.loads((BODY/'pieces_v2/upper/registration_fragment.json').read_text())
baseline_records=[];baseline_parts={}
for old in original['layers']:
 if old['id'] not in parts:continue
 e=dict(old);e['z']-=200;baseline_records.append(e)
 a=math.radians(e['rotation_degrees']);sx,sy=e['scale'];px,py=e['pivot'];tx,ty=e['target_pivot']
 v=[sx*math.cos(a),sx*math.sin(a),-sy*math.sin(a),sy*math.cos(a),tx-math.cos(a)*px+math.sin(a)*py,ty-math.sin(a)*px-math.cos(a)*py]
 baseline_parts[e['id']]=(Image.open(RIG/e['file']).convert('RGBA'),v)
# Static CPU composite uses unchanged final transforms for all other owners and head.
before=Image.new('RGBA',C);after=Image.new('RGBA',C)
for canvas,use_new in [(before,False),(after,True)]:
 entries=[e for e in manifest['layers'] if e['id'] not in parts]+(records if use_new else baseline_records)
 for e in sorted(entries,key=lambda e:e['z']):
  if use_new and e['id'] in parts: im,v=parts[e['id']]
  elif not use_new and e['id'] in baseline_parts:im,v=baseline_parts[e['id']]
  else:im=Image.open(RIG/e['file'][6:]).convert('RGBA');v=frame['layers'][e['id']]
  place(canvas,im,v)
 place(canvas,Image.open(BODY/'pieces_v2/head_audit/neutral_head_complete.png').convert('RGBA'),frame['head'])
for name,canvas in [('before',before),('candidate',after)]:
 canvas.save(HERE/(name+'_transparent.png'))
 bg=Image.new('RGBA',C,'#eeece5');bg.alpha_composite(canvas);bg.save(HERE/('integrated_'+name+'.png'))
 bg.crop((280,275,744,750)).resize((928,950)).save(HERE/(name+'_elbow_detail.png'))
pair=Image.new('RGB',(1856,995),'#eeece5');d=ImageDraw.Draw(pair)
for i,(name,label) in enumerate([('before','CURRENT: duplicated bend / open upper tube'),('candidate','CANDIDATE: aligned fold / continuous arm')]):
 pair.paste(Image.open(HERE/(name+'_elbow_detail.png')),(i*928,45));d.text((i*928+10,12),label,fill='#222')
pair.save(HERE/'before_after_elbows.jpg',quality=94)
(HERE/'registration_candidate.json').write_text(json.dumps(dict(status='Unapproved local static sleeve fit, not integrated',canvas=list(C),reference='avatar_build_assets/reference_library/assets/modeling/RYO_MOD_fullbody_front_v001.png',reference_use='Visual landmarks only. No reference pixels are used in candidate artwork.',layers=records,joint_replacements=[{'id':'elbow_R','position':[354,532]},{'id':'elbow_L','position':[670,532]}],unchanged_wrist_bind_points=[[325,725],[699,725]],unchanged_shoulder_bind_points=[[372,302],[652,302]],notes=['Four independent sleeve owners and two independently re-registered original hand owners retained. No composite body/bust texture is instantiated.','Head, neck, jacket, blouse, jewelry and lower body are unchanged. Hands retain proportions and angle with an absolute 10px underlap translation from their original neutral bind.','Upper open-tube cap excluded along fold. Forearm top now overlaps beneath upper sleeve; the painted fold is located at the elbow rather than below it.','Static CPU proof only. No native render, motion, or user approval is claimed.']),indent=2)+'\n')
print(HERE/'before_after_elbows.jpg')

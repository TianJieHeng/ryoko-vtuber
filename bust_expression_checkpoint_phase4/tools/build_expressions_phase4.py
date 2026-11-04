from PIL import Image,ImageDraw,ImageFilter,ImageFont
from pathlib import Path
import json
p=Path(__file__).resolve().parents[1];q=p;art=q/'artwork';out=q/'previews';size=(1136,1384)
manifest=json.loads((q/'registration.json').read_text());manifest.setdefault('expressions',{})
def read(path):
 im=Image.open(path).convert('RGBA').resize(size,Image.Resampling.LANCZOS);im.putalpha(im.getchannel('A').point(lambda x:255 if x>=240 else x));return im
def extract(im,box,fn):
 m=Image.new('L',size);d=ImageDraw.Draw(m);d.rounded_rectangle((box[0]+7,box[1]+10,box[2]-7,box[3]-7),radius=25,fill=255) if box[1]<500 else d.ellipse((box[0]+8,box[1]+8,box[2]-8,box[3]-8),fill=255);m=m.filter(ImageFilter.GaussianBlur(5 if box[1]<500 else 4));tile=im.crop(box);tile.putalpha(m.crop(box));tile.save(art/fn);return {'file':fn,'xy':list(box[:2])}
for id in ['023','081','192']:
 name='EXP-'+id;rest=read(p/'sources'/(name+'.png'));blink=rest if id=='023' else read(p/'sources'/(name+'-blink.png'))
 e={'eyes':{},'blinks':{},'eyes_closed_at_rest':id=='023'}
 for side,box in [('R',(394,350,550,551)),('L',(590,350,735,551))]:
  e['eyes'][side]=extract(rest,box,name+'_eye_'+side+'.png');e['blinks'][side]=extract(blink,box,name+'_blink_'+side+'.png')
 e['mouth']=extract(rest,(484,594,648,690),name+'_rest_mouth.png');e['effects']=[]
 if id=='023':
  for side,box in [('R',(406,521,542,600)),('L',(581,521,723,600))]:e['effects'].append(extract(rest,box,name+'_blush_'+side+'.png'))
 if id=='081': e['effects'].append(extract(rest,(526,480,604,605),name+'_nose_scrunch.png'))
 if id=='192':
  import numpy as np
  from scipy import ndimage
  arr=np.asarray(rest).astype('int16');skin=(arr[:,:,0]-arr[:,:,1]>15)&(arr[:,:,1]-arr[:,:,2]>4)
  envelope=Image.new('L',size);ImageDraw.Draw(envelope).polygon([(425,520),(700,520),(720,555),(727,606),(714,650),(686,671),(641,684),(604,706),(565,727),(528,706),(486,685),(443,671),(414,650),(402,606),(410,558)],fill=255)
  skin &= np.asarray(envelope)>0
  labels,_=ndimage.label(skin);part=labels==labels[600,565];part=ndimage.binary_fill_holes(part);part=ndimage.binary_dilation(part,iterations=2)
  m=Image.fromarray((part*255).astype('uint8')).filter(ImageFilter.GaussianBlur(0.6));ma=np.asarray(m).copy();ma=(ma*np.clip((np.arange(size[1])[:,None]-520)/20,0,1)).astype('uint8');m=Image.fromarray(ma)
  tile=rest.copy();tile.putalpha(m);tile=tile.crop((390,520,740,735));fn=name+'_puffed_contour.png';tile.save(art/fn);e['effects'].append({'file':fn,'xy':[390,520],'rest_only':True})
 manifest['expressions'][name]=e
(q/'registration.json').write_text(json.dumps(manifest,indent=2))
def add(im,e):im.alpha_composite(Image.open(art/e['file']),tuple(e['xy']))
def comp(name,speech=None,blink=False):
 im=Image.open(art/'bust_base.png').convert('RGBA');e=manifest['expressions'][name]
 for fx in e.get('effects',[]):
  if not fx.get('rest_only',False) or speech is None:add(im,fx)
 for side in ['L','R']:add(im,e['blinks' if blink else 'eyes'][side])
 add(im,manifest['mouths'][speech] if speech else e['mouth']);return im
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',23)
for name in ['EXP-023','EXP-081','EXP-192']:
 c=Image.new('RGB',(2200,660),'#c9cdd1');d=ImageDraw.Draw(c)
 ref=Image.open(p/'references'/(name+'_peak.png')).convert('RGB');ref=ref.crop({'EXP-023':(86,127,311,342),'EXP-081':(90,110,315,325),'EXP-192':(94,109,319,324)}[name]).resize((420,402));c.paste(ref,(10,95));d.text((10,40),'EXACT '+name+' REF CROP',font=f,fill='black')
 for i,(label,speech,blink) in enumerate([('ASSEMBLED REST',None,False),('SPEAKING A','A',False),('BLINK',None,True),('SPEAK + BLINK','A',True)]):
  im=comp(name,speech,blink);im.save(out/(name+'_'+label.lower().replace(' ','_').replace('+','and')+'.png'));crop=im.crop((335,360,795,800)).resize((420,402));c.paste(crop,(450+i*440,95),crop);d.text((450+i*440,40),label,font=f,fill='black')
 d.text((15,570),'Actual sprite composites, not a graphical runtime capture. Speech overrides mouth; rest mouth returns after speech.',font=f,fill='black')
 if name=='EXP-192':d.text((15,610),'Actual puffed cheek contour at rest; cheeks deflate during speech and restore after speech release.',font=f,fill='black')
 c.save(out/(name+'_approval_comparison.jpg'),quality=96)

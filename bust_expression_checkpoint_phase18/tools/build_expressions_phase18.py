from PIL import Image,ImageDraw,ImageFilter,ImageFont
from pathlib import Path
import json
p=Path(__file__).resolve().parents[1];q=p;art=q/'artwork';out=q/'previews';size=(1136,1384)
manifest=json.loads((q/'registration.json').read_text());manifest.setdefault('expressions',{})
def read(path):
 im=Image.open(path).convert('RGBA').resize(size,Image.Resampling.LANCZOS);im.putalpha(im.getchannel('A').point(lambda x:255 if x>=240 else x));return im
def extract(im,box,fn):
 m=Image.new('L',size);d=ImageDraw.Draw(m);d.rounded_rectangle((box[0]+7,box[1]+10,box[2]-7,box[3]-7),radius=25,fill=255) if box[1]<500 else d.ellipse((box[0]+8,box[1]+8,box[2]-8,box[3]-8),fill=255);m=m.filter(ImageFilter.GaussianBlur(5 if box[1]<500 else 4));tile=im.crop(box);tile.putalpha(m.crop(box));tile.save(art/fn);return {'file':fn,'xy':list(box[:2])}
for id in ['097','107','194']:
 name='EXP-'+id;rest=read(p/'sources'/(name+'.png'));blink=read(p/'sources'/(name+'-blink.png'))
 e={'eyes':{},'blinks':{},'eyes_closed_at_rest':id=='194','effects':[]}
 for side,box in [('R',(394,350,550,531)),('L',(590,350,735,531))]:
  e['eyes'][side]=extract(rest,box,name+'_eye_'+side+'.png');e['blinks'][side]=extract(rest if id=='097' and side=='L' else blink,box,name+'_blink_'+side+'.png')
 if id in ['097','107','194']:
  box=(477,588,655,706);m=Image.new('L',size);d=ImageDraw.Draw(m);d.rounded_rectangle((485,594,647,698),radius=22,fill=255);m=m.filter(ImageFilter.GaussianBlur(4));tile=rest.crop(box);tile.putalpha(m.crop(box));fn=name+'_rest_mouth.png';tile.save(art/fn);e['mouth']={'file':fn,'xy':list(box[:2])}
 else:e['mouth']=extract(rest,(484,594,648,690),name+'_rest_mouth.png')
 if id=='097':e['wink_closed_side']='L'
 clean=read(p/'sources'/(name+'-cheek-cleanup.png'))
 for side,box,poly in [('R',(418,507,550,615),[(427,514),(540,514),(541,582),(484,607),(443,586)]),('L',(585,507,706,615),[(596,514),(697,514),(689,581),(644,607),(594,583)])]:
  m=Image.new('L',size);d=ImageDraw.Draw(m);d.polygon(poly,fill=255);m=m.filter(ImageFilter.GaussianBlur(4));tile=clean.crop(box);tile.putalpha(m.crop(box));fn=name+'_cheek_clean_'+side+'.png';tile.save(art/fn);e['effects'].append({'file':fn,'xy':list(box[:2])})
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
for name in ['EXP-097','EXP-107','EXP-194']:
 c=Image.new('RGB',(2200,660),'#c9cdd1');d=ImageDraw.Draw(c)
 ref=Image.open(p/'references'/(name+'_peak.png')).convert('RGB');ref=ref.crop({'EXP-097':(85,100,310,315),'EXP-107':(80,85,305,300),'EXP-194':(90,95,315,310)}[name]).resize((420,402));c.paste(ref,(10,95));d.text((10,40),'EXACT '+name+' REF CROP',font=f,fill='black')
 for i,(label,speech,blink) in enumerate([('ASSEMBLED REST',None,False),('SPEAKING A','A',False),('BLINK',None,True),('SPEAK + BLINK','A',True)]):
  im=comp(name,speech,blink);im.save(out/(name+'_'+label.lower().replace(' ','_').replace('+','and')+'.png'));crop=im.crop((335,360,795,800)).resize((420,402));c.paste(crop,(450+i*440,95),crop);d.text((450+i*440,40),label,font=f,fill='black')
 d.text((15,570),'Actual sprite composites, not a graphical runtime capture. Speech overrides mouth; rest mouth returns after speech.',font=f,fill='black')

 c.save(out/(name+'_approval_comparison.jpg'),quality=96)

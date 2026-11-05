from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import numpy as np
root=Path(__file__).resolve().parents[1]
p=root;src=np.array(Image.open(p/'artwork/bust_base.png').convert('RGBA'));out=p/'rig_assets'
configs=[('screen_left',[(463,449),(480,451),(500,456),(516,463),(535,476),(518,471),(497,465),(477,459),(463,456)],(460,437,541,482)),('screen_right',[(605,460),(618,454),(636,448),(651,446),(653,453),(640,457),(621,465),(607,470)],(600,435,660,481))]
for name,points,box in configs:
 x0,y0,x1,y1=box;patch=src[y0:y1,x0:x1,:3].astype(float)
 yy,xx=np.mgrid[y0:y1,x0:x1]
 green=(patch[:,:,1]>patch[:,:,0]-35)&(patch[:,:,2]>patch[:,:,0]-65)
 if name=='screen_left':region=(xx>=463)&(xx<=536)&(yy>=446)&(yy<=477);foreground=(xx<463)
 else:region=(xx>=605)&(xx<=655)&(yy>=443)&(yy<=472);foreground=(xx>=632+(yy-430)*.8-1)|(xx<605)
 shape=Image.new('L',(1136*4,1384*4));ImageDraw.Draw(shape).polygon([(x*4,y*4) for x,y in points],fill=255)
 shape=shape.resize((1136,1384),Image.Resampling.LANCZOS).filter(ImageFilter.MaxFilter(7))
 local=np.array(shape)[y0:y1,x0:x1].copy();local[foreground]=0
 mask=np.zeros(src.shape[:2],dtype='uint8');mask[y0:y1,x0:x1]=local
 unknown=(local>0)|green
 # Reconstruct skin only where the baked-in visible brow used to be.
 filled=patch.copy();filled[unknown]=[239,185,161]
 for i in range(450):
  a=np.pad(filled,((1,1),(1,1),(0,0)),mode='edge');mean=(a[:-2,1:-1]+a[2:,1:-1]+a[1:-1,:-2]+a[1:-1,2:])/4;filled[unknown]=mean[unknown]
 mask=np.array(Image.fromarray(mask).filter(ImageFilter.GaussianBlur(.8)))
 mask[y0:y1,x0:x1][foreground]=0
 bg=np.zeros_like(src);bg[y0:y1,x0:x1,:3]=filled.astype('uint8');bg[:,:,3]=mask
 brow=np.zeros_like(src);brow[y0:y1,x0:x1,:3]=src[y0:y1,x0:x1,:3];brow[:,:,3]=mask
 # Original skin or the original brow is an allowed destination. Hair pixels
 # outside the extraction remain foreground and cannot be covered by the brow.
 allow=np.zeros(src.shape[:2],dtype='uint8');region=src[y0:y1,x0:x1,:3].astype(float)
 skin=(region[:,:,0]>region[:,:,1]+12)&(region[:,:,0]>region[:,:,2]+20)
 allow[y0:y1,x0:x1]=np.maximum(skin.astype('uint8')*255,mask[y0:y1,x0:x1])
 allow[y0:y1,x0:x1][foreground]=0
 Image.fromarray(brow).save(out/f'brow_{name}.png');Image.fromarray(bg).save(out/f'brow_skin_{name}.png');Image.fromarray(allow).save(out/f'brow_allow_{name}.png')
print('Separated neutral brow derivatives; source unchanged')

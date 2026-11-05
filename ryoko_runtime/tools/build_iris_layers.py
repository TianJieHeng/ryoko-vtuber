from PIL import Image,ImageDraw,ImageFilter
import numpy as np, json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
src=Image.open(root/'artwork/bust_base.png').convert('RGBA');a=np.array(src)
out=root/'rig_assets';out.mkdir(exist_ok=True)
# Fixed aperture follows the visible sclera beneath the existing eyelash edge.
def polygon(points):
 m=Image.new('L',(1136*4,1384*4));ImageDraw.Draw(m).polygon([(int(x*4),int(y*4)) for x,y in points],fill=255);return m.resize((1136,1384),Image.Resampling.LANCZOS)
configs=[('screen_left',(477,491),[(436,497),(448,493),(460,487),(476,486),(490,489),(503,495),(516,503),(518,507),(503,512),(487,517),(474,517),(461,513),(449,507),(440,501)],[(454,482),(458,485),(460,491),(465,497),(462,498),(457,493),(452,487)]),('screen_right',(646,490),[(618,497),(629,490),(644,485),(660,484),(676,486),(690,491),(690,499),(681,506),(667,512),(651,515),(638,513),(627,507),(621,501)],[])]
for name,(cx,cy),poly,hair in configs:
 aperture=polygon(poly)
 if hair:aperture=Image.fromarray(np.minimum(np.array(aperture),255-np.array(polygon(hair))))
 # Preserve source lower iris outline. Complete only the hidden upper cap and
 # small strand-covered area, so they can move behind the fixed upper lid.
 mask=Image.new('L',(1136*4,1384*4));d=ImageDraw.Draw(mask)
 d.ellipse(((cx-24)*4,(cy-24)*4,(cx+24)*4,(cy+24)*4),fill=255)
 mask=mask.resize((1136,1384),Image.Resampling.LANCZOS)
 iris=a.copy();iris[:,:,3]=np.array(mask)
 # Reconstruct only occluded texels by harmonic extension from visible iris.
 # Visible lower iris/pupil pixels are held fixed, never stretched or resampled.
 patch=a[cy-32:cy+32,cx-32:cx+32,:3].astype(float)
 yy,xx=np.mgrid[-32:32,-32:32]
 disk=xx*xx+yy*yy<23*23
 known=disk & (((yy+cy)>=498) | ((np.abs(xx)<=14)&((yy+cy)>=489)))
 if name=='screen_left':known &= ~(((xx+cx)<466)&((yy+cy)<501))
 colors=patch.copy();colors[~known]=[134,87,28]
 for iteration in range(450):
  padded=np.pad(colors,((1,1),(1,1),(0,0)),mode='edge')
  mean=(padded[:-2,1:-1]+padded[2:,1:-1]+padded[1:-1,:-2]+padded[1:-1,2:])/4
  colors[~known]=mean[~known]
 iris[cy-32:cy+32,cx-32:cx+32,:3]=np.clip(colors,0,255).astype('uint8')
 # Neutral sclera gradient reconstructed from source sclera samples, not an
 # invented expression. Only the fixed aperture is rendered over the source.
 bg=a.copy()
 for y in range(cy-20,cy+28):
  for x in range(cx-48,cx+48):
   # Upper-lid shadow fades into the existing off-white sclera.
   k=np.clip((y-(cy-5))/15,0,1)
   color=(1-k)*np.array([192,181,181])+k*np.array([251,248,247])
   bg[y,x,:3]=color.astype('uint8')
 bg[:,:,3]=np.array(aperture)
 # Full-canvas textures keep canonical registration without per-eye offsets.
 Image.fromarray(iris).save(out/f'iris_{name}.png')
 Image.fromarray(bg).save(out/f'sclera_{name}.png')
 aperture.save(out/f'aperture_{name}.png')
print('Built rigid iris layers from unchanged canonical source')

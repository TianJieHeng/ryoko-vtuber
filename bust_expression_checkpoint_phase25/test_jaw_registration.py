from pathlib import Path
from PIL import Image
import json
p=Path(__file__).parent
m=json.loads((p/'registration.json').read_text())
def add(im,e):im.alpha_composite(Image.open(p/'artwork'/e['file']),tuple(e['xy']))
def assemble(id,state):
 im=base.copy();e=m['expressions']['EXP-'+id]
 for fx in e['effects']:add(im,fx)
 for side in ['L','R']:add(im,e['blinks' if 'blink' in state else 'eyes'][side])
 add(im,m['mouths']['A'] if state in ['speaking_a','speak_and_blink'] else e['mouth'])
 return im
base=Image.open(p/'artwork/bust_base.png').convert('RGBA');n=0
for id in ['007','092','128']:
 for state in ['assembled_rest','speaking_a','blink','speak_and_blink']:
  im=assemble(id,state)
  for box in [(0,704,1136,1384),(0,676,512,704),(616,676,1136,704)]:
   assert im.crop(box).tobytes()==base.crop(box).tobytes(),(id,state,box)
  n+=1
print(f'PASS: {n} displayed states retain original jaw/chin/neck/body outside shared speech mouth bounds. Emotion mouth tiles end at y675.')

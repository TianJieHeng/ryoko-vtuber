from pathlib import Path
from PIL import Image
import numpy as np, hashlib, io, json
W=Path(__file__).resolve().parent/'caught_staring_mouth_work'
results=[]
for meta,rawname,target in [('provenance.json','raw_generated.png','uneasy_authored.png'),('parting_provenance.json','parting_raw_generated.png','uneasy_clear_parting.png')]:
 p=json.loads((W/meta).read_text());raw=W/rawname
 assert hashlib.sha256(raw.read_bytes()).hexdigest()==p['raw_sha256']
 a=np.array(Image.open(raw));a[:,:,3][a[:,:,3]<=8]=0
 im=Image.fromarray(a).crop(p['crop']).resize(p['native_size'],Image.Resampling.LANCZOS)
 b=io.BytesIO();im.save(b,format='PNG');out=b.getvalue()
 assert out==(W/target).read_bytes(), target+' differs'
 results.append({'file':target,'sha256':hashlib.sha256(out).hexdigest(),'native_size':list(im.size)})
print(json.dumps({'status':'PASS','outputs':results,'scope':'Exact included processing only; no generation or native rendering'}))

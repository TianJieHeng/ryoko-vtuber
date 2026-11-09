from PIL import Image,ImageDraw
from pathlib import Path
import numpy as np,json,hashlib
W=Path(__file__).resolve().parent;D=W/'proposal_01'
board=Image.new('RGB',(1200,420),'#eeeeee');d=ImageDraw.Draw(board)
source=Image.open(W.parent/'flirty_blushing_set_source_audit/source_reference/RYO_EXP-144_caught-staring_kp03_v001.png').crop((105,130,305,310)).resize((400,360),Image.Resampling.NEAREST)
for i,(im,title) in enumerate([(source,'Original KP3 reference (enlarged crop)'),(Image.open(D/'KP3_uneasy_old.png'),'Existing native mouth'),(Image.open(D/'KP3_uneasy_proposal.png'),'One authored mouth proposal, unapproved')]):
 board.paste(im.convert('RGB'),(i*400,30));d.text((i*400+8,8),title,fill='black')
d.text((8,400),'Static art proposal only. Surprised eye opening is still unresolved. Neutral face remains unchanged.',fill='black');board.save(W/'UNEASY_MOUTH_REVIEW.png')
checks={}
for label in ['KP3_uneasy','KP4_aversion']:
 a=np.array(Image.open(D/(label+'_old.png')));b=np.array(Image.open(D/(label+'_proposal.png')));diff=np.any(a!=b,axis=2);y,x=np.where(diff)
 checks[label]={'changed_pixels':int(diff.sum()),'bbox_half_open':[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]}
a=np.array(Image.open(D/'neutral_old.png'));b=np.array(Image.open(D/'neutral_restored_old.png'));checks['neutral_changed_pixels']=int(np.any(a!=b,axis=2).sum())
checks['snapshot_restored']=json.loads((D/'result.json').read_text())['snapshot_restored']
P=W.parent/'approved_upper_iris_repair_integration/candidate/ryoko_object_rig';old=json.loads((W.parent/'interested_skepticism_work/approved_before.json').read_text());new={str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in P.rglob('*') if p.is_file()};checks['protected666_unchanged']=old==new
(W/'checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(checks))

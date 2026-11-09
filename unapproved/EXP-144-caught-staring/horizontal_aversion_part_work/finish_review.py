from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
W=Path(__file__).resolve().parent;D=W/'gate_01'
def arr(n):return np.array(Image.open(D/f'{n}.png').convert('RGBA'))
checks={'neutral_changed_pixels':int(np.any(arr('neutral')!=arr('neutral_restored'),axis=2).sum())}
a=arr('bounded_4');b=arr('aversion_12');diff=np.any(a!=b,axis=2);ys,xs=np.where(diff)
checks['gaze_4_to_12_changed_pixels']=int(diff.sum());checks['difference_bbox_half_open']=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
allowed=np.zeros(diff.shape,bool);allowed[89:150,30:153]=True;allowed[89:150,230:360]=True
checks['changed_pixels_outside_eye_boxes']=int((diff&~allowed).sum())
# Recheck all protected files against the established preflight record.
protected=W.parent/'approved_upper_iris_repair_integration/candidate/ryoko_object_rig'
prior=json.loads((W.parent/'interested_skepticism_work/approved_before.json').read_text())
actual={str(p.relative_to(protected)):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected.rglob('*') if p.is_file()}
checks['protected_before_record_type']=type(prior).__name__
checks['protected666_exact']=prior==actual
checks['protected_file_count']=len(actual)
(W/'pixel_checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(checks)
labels=[('bounded_4','Existing 4px bound; 18% lids'),('aversion_12','Proposed 12px; 18% lids'),('caught_peak','Caught-staring peak study only')]
board=Image.new('RGB',(1200,390),'#eeeeee');d=ImageDraw.Draw(board)
for i,(n,label) in enumerate(labels):
 d.text((i*400+8,8),label,fill='black');board.paste(Image.open(D/f'{n}.png').convert('RGB'),(i*400,30))
board.save(W/'AVERSION_PART_REVIEW.png')

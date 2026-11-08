from pathlib import Path
from collections import Counter
from itertools import zip_longest
import json,hashlib
D=Path(__file__).resolve().parent
counts=Counter();added=Counter();missing=Counter();examples={};added_values={};n=0;exact=0;natural=0;natural_affected=0
def compare(a,b,path,case):
 if isinstance(a,dict) and isinstance(b,dict):
  for k in a:
   if k not in b:missing[path+'/'+k]+=1
   else:compare(a[k],b[k],path+'/'+k,case)
  for k in b.keys()-a.keys():
   p=path+'/'+k;added[p]+=1
   values=added_values.setdefault(p,[])
   if b[k] not in values and len(values)<6:values.append(b[k])
 elif isinstance(a,list) and isinstance(b,list):
  if len(a)!=len(b):counts[path+'/length']+=1;examples.setdefault(path+'/length',{'case':case,'historical':len(a),'current':len(b)})
  for i,(x,y) in enumerate(zip(a,b)):compare(x,y,path+'/'+str(i),case)
 elif a!=b:
  counts[path]+=1;examples.setdefault(path,{'case':case,'historical':a,'current':b})
with (D/'historical_samples.jsonl').open() as af,(D/'current_samples.jsonl').open() as bf:
 for al,bl in zip_longest(af,bf):
  assert al and bl,'mismatched sample count'
  a=json.loads(al);b=json.loads(bl);assert a['case']==b['case'];n+=1
  before=sum(counts.values());compare(a,b,'',a['case']);same=sum(counts.values())==before
  exact+=same
  if a['case'].startswith('natural/'):
   natural+=1;natural_affected+=not same
report={'samples':n,'natural_samples':natural,'natural_samples_with_shared_field_differences':natural_affected,'all_shared_fields_equal_samples':exact,'shared_difference_count':sum(counts.values()),'shared_differing_paths':dict(counts),'shared_difference_examples':examples,'missing_fields':dict(missing),'added_fields':dict(added),'added_field_values':added_values,'historical_samples_sha256':hashlib.sha256((D/'historical_samples.jsonl').read_bytes()).hexdigest(),'current_samples_sha256':hashlib.sha256((D/'current_samples.jsonl').read_bytes()).hexdigest(),'comparison':'Exact recursive comparison of every historical state, face, object transform, material uniform, texture/UV and head/body field. Current-only fields are reported separately, not silently normalized.'}
(D/'SAMPLED_COMPATIBILITY.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['shared_difference_examples','added_fields','added_field_values']},indent=2))
print('EXAMPLES',json.dumps(dict(list(examples.items())[:10]),indent=2))

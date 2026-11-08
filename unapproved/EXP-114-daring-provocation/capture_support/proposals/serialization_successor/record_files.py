"""Strict bounded reader for complete checkpoint files and final completion manifest.
No value normalization, float tolerance, field filtering, renderer, or reconstruction of missing evidence.
"""
from pathlib import Path
import hashlib,json,re
SCHEMA='EXP114_RECORD_FILES_V1'
TRANSPORT={'serialization_schema','serialization_complete','record_count','expected_record_count','record_files'}
DESCRIPTOR={'ordinal','label','chapter','checkpoint','chapter_elapsed','path','sha256','bytes'}
sha=lambda b:hashlib.sha256(b).hexdigest()
def unique_object(pairs):
 result={}
 for key,value in pairs:
  assert key not in result,('duplicate JSON key',key)
  result[key]=value
 return result
def loads(data):return json.loads(data,object_pairs_hook=unique_object,parse_constant=lambda s:(_ for _ in ()).throw(AssertionError('nonfinite JSON '+s)))
def ordered_plan(plan):
 return [{'label':c['name']+'_%03d'%i,'chapter':c['name'],'checkpoint':i,'chapter_elapsed':t} for c in plan['chapters'] for i,t in enumerate(c['times'])]
class CompleteRecords:
 def __init__(self,output,index,expected):self.output=Path(output);self.index=index;self.expected=expected
 def __len__(self):return len(self.index)
 def __iter__(self):
  for n,(entry,expected) in enumerate(zip(self.index,self.expected,strict=True)):
   path=self.output/entry['path'];assert path.is_file() and not path.is_symlink()
   data=path.read_bytes();assert len(data)==entry['bytes'] and sha(data)==entry['sha256'],('record size/hash',n)
   row=loads(data);assert isinstance(row,dict)
   for key,value in expected.items():assert row.get(key)==value and not isinstance(row.get(key),bool),(n,key,'record identity')
   yield row

def read_evidence(output,expected,plan_sha256):
 output=Path(output);manifest=output/'evidence.json';assert manifest.is_file() and not manifest.is_symlink()
 header=loads(manifest.read_bytes());assert isinstance(header,dict)
 assert header['status']=='PASS' and header['failures']==[] and header['serialization_schema']==SCHEMA and header['serialization_complete'] is True
 assert header['plan_sha256']==plan_sha256
 assert type(header['record_count']) is int and type(header['expected_record_count']) is int
 assert header['record_count']==header['expected_record_count']==len(expected)
 index=header['record_files'];assert isinstance(index,list) and len(index)==len(expected)
 paths=[];labels=[]
 for n,(entry,wanted) in enumerate(zip(index,expected,strict=True)):
  assert isinstance(entry,dict) and set(entry)==DESCRIPTOR
  assert type(entry['ordinal']) is int and entry['ordinal']==n and type(entry['checkpoint']) is int
  assert entry['path']=='records/%04d.json'%n
  assert type(entry['bytes']) is int and entry['bytes']>0 and isinstance(entry['sha256'],str) and re.fullmatch('[0-9a-f]{64}',entry['sha256'])
  for key,value in wanted.items():assert entry[key]==value and not isinstance(entry[key],bool),(n,key,'descriptor identity')
  paths.append(entry['path']);labels.append(entry['label'])
 assert len(set(paths))==len(paths) and len(set(labels))==len(labels),'duplicate path or label'
 directory=output/'records';assert directory.is_dir() and not directory.is_symlink()
 actual=list(directory.iterdir());assert all(p.is_file() and not p.is_symlink() for p in actual)
 assert sorted(p.relative_to(output).as_posix() for p in actual)==sorted(paths),'missing or extra record file'
 records=CompleteRecords(output,index,expected)
 # Validate every file before returning a reusable bounded stream. No aggregate array retained.
 for _ in records:pass
 result={k:v for k,v in header.items() if k not in TRANSPORT};assert 'records' not in result
 result['records']=records
 return result

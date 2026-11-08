"""Disposable offline transport fixtures. Not engine execution, trajectory evidence, or visual acceptance."""
from pathlib import Path
import ast,copy,hashlib,json,shutil,tempfile
from record_files import SCHEMA,read_evidence,ordered_plan,sha
P=Path(__file__).resolve().parent;W=P.parents[1];R=W.parent
for p in P.glob('*.py'):ast.parse(p.read_text(),filename=str(p))
static_path=R/'daring_provocation_fit_work/native_capture_01/evidence.json';static=json.loads(static_path.read_text());plan=json.loads((W/'capture_plan.json').read_text());plan_hash=sha((W/'capture_plan.json').read_bytes())
report={'status':'RUNNING','scope':'Offline serialization equivalence and fail-closed negatives only; no Godot or visual-performance claim','real_record_source':str(static_path),'real_record_source_sha256':sha(static_path.read_bytes()),'tests':[]}
def write_dataset(root,original,rows,expected,ph):
 root.mkdir();(root/'records').mkdir();index=[]
 for n,(row,wanted) in enumerate(zip(rows,expected,strict=True)):
  data=(json.dumps(row,indent=2,allow_nan=False)+'\n').encode();rel='records/%04d.json'%n;(root/rel).write_bytes(data)
  index.append({'ordinal':n,**wanted,'path':rel,'sha256':sha(data),'bytes':len(data)})
 h={k:copy.deepcopy(v) for k,v in original.items() if k!='records'}
 h.update(serialization_schema=SCHEMA,serialization_complete=True,record_count=len(rows),expected_record_count=len(rows),record_files=index,plan_sha256=ph)
 (root/'evidence.json').write_text(json.dumps(h,indent=2,allow_nan=False)+'\n')
 return h
with tempfile.TemporaryDirectory(prefix='exp114_record_files_') as tmp:
 T=Path(tmp);rows=[]
 for n,row in enumerate(static['records']):
  row=copy.deepcopy(row);row.update(chapter='offline_real_static_fixture',checkpoint=n,chapter_elapsed=float(n));rows.append(row)
 expected=[{k:r[k] for k in ['label','chapter','checkpoint','chapter_elapsed']} for r in rows]
 original={k:copy.deepcopy(v) for k,v in static.items() if k!='records'};original.update(records=rows,plan_sha256=plan_hash,fixture_only=True)
 write_dataset(T/'real',original,rows,expected,plan_hash);decoded=read_evidence(T/'real',expected,plan_hash);decoded['records']=list(decoded['records']);assert decoded==original
 for before,after in zip(static['records'],decoded['records'],strict=True):
  assert {k:after[k] for k in before}==before
 report['tests'].append({'name':'Seven complete actual native static records, all recursive fields and header round trip exactly','status':'PASS','real_records':7,'new_performance_evidence':False,'original_row_content_sha256':[sha(json.dumps(r,sort_keys=True,separators=(',',':')).encode()) for r in static['records']]})
 expected=ordered_plan(plan);rows=[{**wanted,'fixture_only':True,'real_public_controls':copy.deepcopy(static['records'][n%7]['public_controls']),'synthetic_order_fixture_index':n} for n,wanted in enumerate(expected)]
 header={'status':'PASS','failures':[],'checks':0,'fixture_only':True,'plan_sha256':plan_hash,'records':rows}
 clean=T/'clean701';write_dataset(clean,header,rows,expected,plan_hash);decoded=read_evidence(clean,expected,plan_hash);assert len(decoded['records'])==701 and list(decoded['records'])==rows
 report['tests'].append({'name':'701 ordered synthetic transport records preserve exact real control values','status':'PASS','checkpoints':701,'not_actual_trajectory':True})
 def rejection(name,mutate):
  d=T/'negative';shutil.copytree(clean,d);h=json.loads((d/'evidence.json').read_text());mutate(d,h)
  if (d/'evidence.json').exists() and not name.startswith(('truncated_manifest','duplicate_manifest_key')):(d/'evidence.json').write_text(json.dumps(h,indent=2)+'\n')
  caught=None
  try:read_evidence(d,expected,plan_hash)
  except (AssertionError,ValueError,KeyError,TypeError,OSError) as e:caught=type(e).__name__+': '+str(e)
  assert caught is not None,('negative silently passed',name)
  report['tests'].append({'name':name,'status':'PASS_EXPECTED_REJECTION','reason':caught});shutil.rmtree(d)
 rejection('missing_completion_manifest',lambda d,h:(d/'evidence.json').unlink())
 rejection('truncated_manifest_zero_bytes',lambda d,h:(d/'evidence.json').write_bytes(b''))
 rejection('truncated_manifest_partial_json',lambda d,h:(d/'evidence.json').write_text('{"status":"PASS"'))
 rejection('explicit_failure_manifest',lambda d,h:h.update(status='FAIL'))
 rejection('incomplete_manifest',lambda d,h:h.update(serialization_complete=False))
 rejection('record_count_mismatch',lambda d,h:h.update(record_count=700))
 rejection('boolean_count_rejected',lambda d,h:h.update(record_count=True))
 rejection('short_record_index',lambda d,h:h['record_files'].pop())
 rejection('missing_record_file',lambda d,h:(d/'records/0345.json').unlink())
 rejection('truncated_record_file',lambda d,h:(d/'records/0345.json').write_bytes(b'{'))
 rejection('duplicate_index_entry',lambda d,h:h['record_files'].__setitem__(1,copy.deepcopy(h['record_files'][0])))
 def reorder(d,h):h['record_files'][0],h['record_files'][1]=h['record_files'][1],h['record_files'][0]
 rejection('reordered_index',reorder)
 rejection('wrong_descriptor_hash',lambda d,h:h['record_files'][0].update(sha256='0'*64))
 rejection('wrong_descriptor_size',lambda d,h:h['record_files'][0].update(bytes=h['record_files'][0]['bytes']+1))
 rejection('path_escape',lambda d,h:h['record_files'][0].update(path='../outside.json'))
 rejection('extra_record_file',lambda d,h:(d/'records/0701.json').write_text('{}'))
 rejection('plan_hash_mismatch',lambda d,h:h.update(plan_sha256='0'*64))
 def altered_identity(d,h):
  p=d/'records/0000.json';row=json.loads(p.read_text());row['label']='wrong_label';data=json.dumps(row).encode();p.write_bytes(data);h['record_files'][0].update(sha256=sha(data),bytes=len(data))
 rejection('self_consistent_hash_wrong_row_identity',altered_identity)
 def duplicate_row_key(d,h):
  p=d/'records/0000.json';data=b'{"label":"one","label":"two"}';p.write_bytes(data);h['record_files'][0].update(sha256=sha(data),bytes=len(data))
 rejection('duplicate_record_json_key',duplicate_row_key)
 def duplicate_manifest_key(d,h):(d/'evidence.json').write_text('{"status":"PASS",'+(d/'evidence.json').read_text()[1:])
 rejection('duplicate_manifest_key',duplicate_manifest_key)
 # Reader rejects invalid files even when their bytes/hash are internally consistent.
 def nonfinite_row(d,h):
  p=d/'records/0000.json';data=p.read_bytes().replace(b'"synthetic_order_fixture_index": 0',b'"synthetic_order_fixture_index": NaN');assert b'NaN' in data;p.write_bytes(data);h['record_files'][0].update(sha256=sha(data),bytes=len(data))
 rejection('nonfinite_record_json',nonfinite_row)
 again=read_evidence(clean,expected,plan_hash);assert list(again['records'])==rows
 report['tests'].append({'name':'Clean701 fixture remains unchanged after all negative tests','status':'PASS'})
report.update(status='PASS_OFFLINE_ONLY',new_engine_invocations=0,record_array_retention_in_reader=False,actual_performance_gate_passed=False,fixture_files_disposed=True)
target=P/'OFFLINE_SCHEMA_TESTS.json';assert not target.exists();target.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':report['status'],'tests':len(report['tests']),'real_complete_records':7,'synthetic_order_records':701,'engine_invocations':0}))

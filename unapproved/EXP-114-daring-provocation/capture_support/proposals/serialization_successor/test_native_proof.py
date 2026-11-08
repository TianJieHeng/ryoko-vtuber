from pathlib import Path
import ast,copy,hashlib,json,subprocess,sys
P=Path(__file__).resolve().parent;W=P.parents[1];sys.path.insert(0,str(W))
from verify_native_record_files import validate_render_invariance
from verify_native_stream_inputs import verify
for p in P.glob('*.py'):ast.parse(p.read_text(),filename=str(p))
done=subprocess.run(['/bin/sh','-n',str(P/'EXP114_NATIVE_STREAM_ONCE.sh')],capture_output=True,text=True);assert done.returncode==0,done.stderr
original=json.loads((W.parent/'daring_provocation_fit_work/native_capture_01/evidence.json').read_text())['records'][0];controls=original['public_controls'];h=hashlib.sha256(json.dumps(original['actual_owners'],sort_keys=True).encode()).hexdigest()
proof={'exact_owners_equal':True,'exact_public_controls_equal':True,'before_tree_sha256':h,'after_tree_sha256':h,'before_instance_tree_sha256':h,'after_instance_tree_sha256':h,'public_controls_before':controls,'public_controls_after':controls,'tree_node_count':476}
r={'actual_owners_sha256':h,'public_controls':controls,'native':{'render_invariance':proof}}
validate_render_invariance(r,'native');tests=[{'name':'Positive exact invariance fixture from real neutral data','status':'PASS','actual_new_capture':False}]
for name,mutate in [('owners_flag',lambda p:p.update(exact_owners_equal=False)),('controls_flag',lambda p:p.update(exact_public_controls_equal=False)),('after_tree_hash',lambda p:p.update(after_tree_sha256='0'*64)),('instance_hash',lambda p:p.update(after_instance_tree_sha256='0'*64)),('owner_count',lambda p:p.update(tree_node_count=475)),('changed_control',lambda p:p['public_controls_after'].update(mouth_open=.1))]:
 x=json.loads(json.dumps(r));mutate(x['native']['render_invariance']);rejected=False
 try:validate_render_invariance(x,'native')
 except AssertionError:rejected=True
 assert rejected,name;tests.append({'name':name,'status':'PASS_EXPECTED_REJECTION'})
identity=verify();result={'status':'PASS_OFFLINE_ONLY','tests':tests,'python_ast_all_proposals':True,'minimal_wrapper_shell_syntax_only':True,'original_source_and_failed_evidence_identity':'PASS','accepted_runtime_checks':identity['accepted_completed_checks'],'no_new_engine_or_capture':True}
p=P/'OFFLINE_NATIVE_PROOF_TESTS.json';assert not p.exists();p.write_text(json.dumps(result,indent=2)+'\n');print('PASS offline native proof checks; no engine or display')

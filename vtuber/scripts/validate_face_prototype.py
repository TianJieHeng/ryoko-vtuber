import bpy, json, math
from pathlib import Path
ROOT=Path('/mnt/agents/output/app')
SOURCE=ROOT/'assets/ryoko_mesh_uv_textured_v001.blend'
DEST=ROOT/'assets/ryoko_face_prototype_v001.blend'
OUT=ROOT/'assets/face_prototype_validation_v001.json'

bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
source_objects={o.name:o.type for o in bpy.data.objects}
source_images={i.name:bool(i.packed_file) for i in bpy.data.images if i.source=='FILE'}

bpy.ops.wm.open_mainfile(filepath=str(DEST))
scene=bpy.context.scene
control=bpy.data.objects['RYOKO_FACE_CONTROLS']
root=bpy.data.objects['RYOKO_PRODUCTION_ROOT']
props=['blink_left','blink_right','gaze_x','gaze_y','jaw_open','smile','funnel','wide']
missing_objects=sorted(set(source_objects)-set(bpy.data.objects.keys()))
changed_types={name:{'source':kind,'destination':bpy.data.objects[name].type} for name,kind in source_objects.items() if name in bpy.data.objects and bpy.data.objects[name].type!=kind}
images=[]
for image in bpy.data.images:
    if image.source!='FILE': continue
    path=Path(bpy.path.abspath(image.filepath)) if image.filepath else None
    images.append({'name':image.name,'packed':bool(image.packed_file),'path_exists':bool(path and path.exists())})

shape_keys={}
for obj in bpy.data.objects:
    if obj.type=='MESH' and obj.data.shape_keys:
        shape_keys[obj.name]=[k.name for k in obj.data.shape_keys.key_blocks]

expected={
 'RYOKO_Skin_HeadAndNeck':['Basis','JawOpen','MouthSmile'],
 'RYOKO_EyeWhite_CharacterLeft':['Basis','Blink'],
 'RYOKO_EyeWhite_CharacterRight':['Basis','Blink'],
 'RYOKO_Eyelids_CharacterLeft':['Basis','Blink'],
 'RYOKO_Eyelids_CharacterRight':['Basis','Blink'],
 'RYOKO_Lashes_CharacterLeft':['Basis','Blink'],
 'RYOKO_Lashes_CharacterRight':['Basis','Blink'],
 'RYOKO_IrisAssembly_CharacterLeft':['Basis','Blink','GazeLeft','GazeRight','GazeUp','GazeDown'],
 'RYOKO_IrisAssembly_CharacterRight':['Basis','Blink','GazeLeft','GazeRight','GazeUp','GazeDown'],
}
for name in ['RYOKO_Mouth_CavityInsert','RYOKO_Lips_Deforming','RYOKO_Teeth_Upper','RYOKO_Teeth_Lower','RYOKO_Tongue']:
    expected[name]=['Basis','JawOpen','MouthSmile','MouthFunnel','MouthWide']
shape_key_failures={name:{'expected':keys,'actual':shape_keys.get(name)} for name,keys in expected.items() if shape_keys.get(name)!=keys}

character=set(root.children_recursive)|set(bpy.data.collections['RYOKO_FACE_PROTOTYPE'].objects)
character={o for o in character if o.type=='MESH'}

def geometry_report():
    deps=bpy.context.evaluated_depsgraph_get()
    total=0; nan_objects=[]; object_triangles={}
    for obj in sorted(character,key=lambda o:o.name):
        ev=obj.evaluated_get(deps); mesh=ev.to_mesh()
        mesh.calc_loop_triangles(); count=len(mesh.loop_triangles)
        object_triangles[obj.name]=count; total+=count
        if any(not math.isfinite(c) for v in mesh.vertices for c in v.co): nan_objects.append(obj.name)
        ev.to_mesh_clear()
    return {'triangles':total,'object_triangles':object_triangles,'nonfinite_coordinate_objects':nan_objects}

def driver_report():
    drivers=[]
    for key in bpy.data.shape_keys:
        ad=key.animation_data
        if ad:
            for curve in ad.drivers:
                drivers.append({'owner':key.name,'data_path':curve.data_path,'valid':curve.driver.is_valid,'expression':curve.driver.expression})
    for mat in bpy.data.materials:
        if mat.node_tree and mat.node_tree.animation_data:
            for curve in mat.node_tree.animation_data.drivers:
                drivers.append({'owner':mat.name,'data_path':curve.data_path,'valid':curve.driver.is_valid,'expression':curve.driver.expression})
    return {'count':len(drivers),'invalid':[d for d in drivers if not d['valid']],'drivers':drivers}

states={
 'neutral':{},'blink':{'blink_left':1.0,'blink_right':1.0},'gaze_left':{'gaze_x':-1.0},
 'gaze_right_up':{'gaze_x':1.0,'gaze_y':.35},'jaw_open':{'jaw_open':1.0},
 'smile_jaw':{'smile':1.0,'jaw_open':.65},'funnel':{'funnel':1.0},'wide':{'wide':1.0}
}
action=control.animation_data.action if control.animation_data else None
control.animation_data.action=None
state_results={}
for name,state in states.items():
    scene.frame_set(1)
    for prop in props: control[prop]=state.get(prop,0.0)
    control.update_tag(refresh={'OBJECT'}); bpy.context.view_layer.update()
    state_results[name]={'controls':{p:float(control[p]) for p in props},'geometry':geometry_report()}
static_drivers=driver_report()
control.animation_data.action=action
frames={}
for frame in [1,13,25,37,49,61,73,85,97]:
    scene.frame_set(frame); bpy.context.view_layer.update()
    frames[str(frame)]={p:round(float(control[p]),5) for p in props}
action_drivers=driver_report()
neutral_recovery=all(abs(frames['97'][p])<1e-6 for p in props)
control_ranges={p:{'min':control.id_properties_ui(p).as_dict().get('min'),'max':control.id_properties_ui(p).as_dict().get('max')} for p in props}
report={
 'blender_version':bpy.app.version_string,'fresh_process_reopen':True,'source':str(SOURCE),'destination':str(DEST),
 'source_objects_preserved':not missing_objects and not changed_types,'missing_source_objects':missing_objects,'changed_source_object_types':changed_types,
 'source_file_image_count':len(source_images),'destination_file_images':images,'all_file_images_packed_or_existing':all(i['packed'] or i['path_exists'] for i in images),
 'shape_keys':shape_keys,'shape_key_failures':shape_key_failures,'controller_ranges':control_ranges,
 'static_state_checks':state_results,'static_driver_check':{'count':static_drivers['count'],'invalid':static_drivers['invalid']},
 'action':action.name if action else None,'action_frames':frames,'neutral_recovery_at_frame_97':neutral_recovery,
 'action_driver_check':{'count':action_drivers['count'],'invalid':action_drivers['invalid']},
 'limitations':['Early surface-fitted facial feasibility prototype, not final joined facial/oral topology.','Not the complete 52-clip ARKit set.','No body rig, production animation library, VRM export, tracking runtime, hardware test, or projection validation.']
}
report['passed']=bool(report['source_objects_preserved'] and report['all_file_images_packed_or_existing'] and not shape_key_failures and not static_drivers['invalid'] and not action_drivers['invalid'] and neutral_recovery and all(not s['geometry']['nonfinite_coordinate_objects'] for s in state_results.values()))
OUT.write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k not in ['shape_keys','static_state_checks','destination_file_images']},indent=2))
print('TOTAL_TRIANGLES',state_results['neutral']['geometry']['triangles'])
print('VALIDATION_JSON',OUT)

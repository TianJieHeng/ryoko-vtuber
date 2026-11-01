import bpy,bmesh,json
from pathlib import Path
ROOT=Path('/mnt/agents/output/app')
BLEND=ROOT/'assets/ryoko_mesh_uv_textured_v001.blend'
OUT=ROOT/'assets/mesh_uv_validation_v001.json'
bpy.ops.wm.open_mainfile(filepath=str(BLEND)); bpy.context.view_layer.update()
production=bpy.data.collections['RYOKO_PRODUCTION']
main_names={
 'RYOKO_Outfit_Trousers','RYOKO_Hair_ScalpAndBun','RYOKO_Outfit_BlazerAndBlouse',
 'RYOKO_Outfit_Sleeve_CharacterLeft','RYOKO_Outfit_Sleeve_CharacterRight',
 'RYOKO_Footwear_CharacterLeft','RYOKO_Skin_Hand_CharacterLeft','RYOKO_Footwear_CharacterRight',
 'RYOKO_Skin_Hand_CharacterRight','RYOKO_Skin_HeadAndNeck'}
rows=[]
for obj in sorted((o for o in production.objects if o.type=='MESH' and o.name in main_names),key=lambda o:o.name):
 mesh=obj.data;mesh.calc_loop_triangles();bm=bmesh.new();bm.from_mesh(mesh)
 textures=[]
 for mat in mesh.materials:
  if mat and mat.use_nodes:
   for node in mat.node_tree.nodes:
    if node.type=='TEX_IMAGE' and node.image:
     textures.append({'name':node.image.name,'size':list(node.image.size),'packed':bool(node.image.packed_file),'filepath':node.image.filepath})
 rows.append({'object':obj.name,'vertices':len(mesh.vertices),'polygons':len(mesh.polygons),'triangles':len(mesh.loop_triangles),
  'quad_faces':sum(len(p.vertices)==4 for p in mesh.polygons),'boundary_edges':sum(e.is_boundary for e in bm.edges),
  'non_manifold_edges':sum(not e.is_manifold for e in bm.edges),'uv_layers':len(mesh.uv_layers),'materials':len(mesh.materials),
  'textures':textures,'visible_shadow':obj.visible_shadow,'small_boundary_loops_repaired':int(obj.get('small_boundary_loops_repaired',0))})
 bm.free()
access=[o for o in production.objects if o.type=='MESH' and o.name not in main_names]
access_bounds={}
for obj in access:
 vs=[obj.matrix_world@v.co for v in obj.data.vertices]
 access_bounds[obj.name]={'min':[min(v[i] for v in vs) for i in range(3)],'max':[max(v[i] for v in vs) for i in range(3)]}
report={'source_blend':str(BLEND),'reopened':True,'main_part_count':len(rows),'main_part_vertices':sum(r['vertices'] for r in rows),
 'main_part_triangles':sum(r['triangles'] for r in rows),'main_part_quad_faces':sum(r['quad_faces'] for r in rows),
 'main_part_boundary_edges':sum(r['boundary_edges'] for r in rows),'main_part_non_manifold_edges':sum(r['non_manifold_edges'] for r in rows),
 'all_main_parts_have_one_uv_layer':all(r['uv_layers']==1 for r in rows),
 'all_main_parts_have_base_color_and_roughness':all(len(r['textures'])==2 for r in rows),
 'all_texture_images_packed':all(t['packed'] for r in rows for t in r['textures']),
 'accessory_core_objects':len(access),'accessory_core_triangles':sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in access),
 'total_character_triangles':sum(r['triangles'] for r in rows)+sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in access),
 'chopstick_shafts':sum('TaperedShaft' in o.name for o in access),
 'chain_links':sum('ChainLink' in o.name for o in access),'armatures':sum(o.type=='ARMATURE' for o in bpy.data.objects),
 'shape_key_blocks':sum(o.type=='MESH' and o.data.shape_keys is not None for o in bpy.data.objects),
 'accessory_bounds':access_bounds,'parts':rows,
 'certification':'Modular visual/UV foundation only. Original clothing/hair open topology and generated skin internal shells are not certified for deformation. No facial rig, armature, ARKit clips, VRM export, or runtime validation.'}
OUT.write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k not in {'parts','accessory_bounds'}},indent=2))

import bpy, bmesh, json, math
from pathlib import Path
ROOT=Path('/mnt/agents/output/app')
path=ROOT/'assets/ryoko_blockout_v002.blend'
bpy.ops.wm.open_mainfile(filepath=str(path))
s=bpy.context.scene
root=bpy.data.objects['RYOKO_BLOCKOUT_ROOT']
base=[o for o in s.objects if o.type=='MESH' and o.parent==root and o.name.startswith('node_')]
assert len(base)==1
m=base[0]; m.data.calc_loop_triangles()
bm=bmesh.new(); bm.from_mesh(m.data)
access=list(bpy.data.collections['RYOKO_ACCESSORIES'].objects)
shafts=[o for o in access if o.name.endswith('_TaperedShaft')]
finials=[o for o in access if o.name.endswith('_RoundFinial')]
assert len(shafts)==2, len(shafts)
assert len(finials)==2, len(finials)
assert len([o for o in access if 'ChainLink' in o.name])==3
assert abs(root.rotation_euler.z-math.radians(-90))<1e-5
report={
'blend_reopened':True,'file':str(path),'base_mesh_objects':1,
'base_vertices':len(m.data.vertices),'base_triangles':len(m.data.loop_triangles),
'base_boundary_edges':sum(e.is_boundary for e in bm.edges),
'base_non_manifold_edges':sum(not e.is_manifold for e in bm.edges),
'accessory_and_bun_core_objects':len(access),
'clean_chopstick_shafts':len(shafts),'rounded_finials':len(finials),'chain_links':3,
'armatures':len([o for o in s.objects if o.type=='ARMATURE']),
'shape_key_blocks':len(m.data.shape_keys.key_blocks) if m.data.shape_keys else 0,
'root_rotation_z_degrees':round(math.degrees(root.rotation_euler.z),3),
'status':'PASS as revised visual blockout: exactly two clean chopsticks; temporary bun core and non-manifold base still require production reconstruction.'
}
bm.free()
(ROOT/'assets/blockout_v002_validation.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))

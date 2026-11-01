import bpy, bmesh, json, math
from pathlib import Path
from mathutils import Vector
ROOT=Path('/mnt/agents/output/app')
path=ROOT/'assets/ryoko_blockout_v001.blend'
bpy.ops.wm.open_mainfile(filepath=str(path))
s=bpy.context.scene
root=bpy.data.objects.get('RYOKO_BLOCKOUT_ROOT')
meshes=[o for o in s.objects if o.type=='MESH' and o.parent==root]
assert root is not None
assert len(meshes)==1, f'Expected one generated character mesh, got {len(meshes)}'
assert abs(root.rotation_euler.z-math.radians(-90))<1e-5
assert 'REVIEW_FACE_FILL' in bpy.data.objects
assert abs(bpy.data.objects['REVIEW_FACE_FILL'].data.energy-180)<1e-5
m=meshes[0]
m.data.calc_loop_triangles()
bm=bmesh.new(); bm.from_mesh(m.data)
report={
'blend_reopened':True,
'file':str(path),
'character_mesh_objects':len(meshes),
'vertices':len(m.data.vertices),
'triangles':len(m.data.loop_triangles),
'armatures':len([o for o in s.objects if o.type=='ARMATURE']),
'shape_key_blocks':len(m.data.shape_keys.key_blocks) if m.data.shape_keys else 0,
'root_rotation_z_degrees':round(math.degrees(root.rotation_euler.z),3),
'review_fill_watts':bpy.data.objects['REVIEW_FACE_FILL'].data.energy,
'boundary_edges':sum(e.is_boundary for e in bm.edges),
'non_manifold_edges':sum(not e.is_manifold for e in bm.edges),
'loose_vertices':sum(not v.link_edges for v in bm.verts),
'render_engine':s.render.engine,
'status':'PASS as an inspected blockout; not production topology, facial geometry, rig, or VRM export.'
}
bm.free()
(ROOT/'assets/blockout_validation.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))

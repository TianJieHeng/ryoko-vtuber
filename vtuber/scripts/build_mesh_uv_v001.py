import bpy, bmesh, math, json
from pathlib import Path
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree

ROOT=Path('/mnt/agents/output/app')
SOURCE=ROOT/'assets/ryoko_blockout_v002.blend'
PARTS=Path('/mnt/agents/output/vtuber/generation/ryoko_semantic_parts.glb')
DEST=ROOT/'assets/ryoko_mesh_uv_v003.blend'
REPORT=ROOT/'assets/mesh_uv_build_v003.json'

bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
bpy.context.view_layer.update()
scene=bpy.context.scene
old_root=bpy.data.objects['RYOKO_BLOCKOUT_ROOT']
approval_transform=old_root.matrix_world.copy()
base=next(o for o in scene.objects if o.type=='MESH' and o.parent==old_root and o.name.startswith('node_'))
access=list(bpy.data.collections['RYOKO_ACCESSORIES'].objects)
base_world=base.matrix_world.copy()
base_vertices=[base_world@v.co for v in base.data.vertices]
base_faces=[tuple(p.vertices) for p in base.data.polygons]
base_centers=[sum((base_vertices[i] for i in f),Vector())/len(f) for f in base_faces]

production=bpy.data.collections.new('RYOKO_PRODUCTION')
scene.collection.children.link(production)
root=bpy.data.objects.new('RYOKO_PRODUCTION_ROOT',None)
production.objects.link(root)

# Preserve approved accessories in their actual world-space positions.
for obj in access:
    world=obj.matrix_world.copy()
    obj.parent=None
    obj.matrix_parent_inverse=Matrix.Identity(4)
    obj.matrix_world=Matrix.Identity(4)
    obj.data.transform(world)
    obj.parent=root
    obj.matrix_parent_inverse=Matrix.Identity(4)
    obj.matrix_basis=Matrix.Identity(4)
    for coll in list(obj.users_collection): coll.objects.unlink(obj)
    production.objects.link(obj)

bpy.data.objects.remove(base,do_unlink=True)
bpy.data.objects.remove(old_root,do_unlink=True)
before=set(scene.objects)
bpy.ops.import_scene.gltf(filepath=str(PARTS))
bpy.context.view_layer.update()
parts=[o for o in scene.objects if o not in before and o.type=='MESH']
assert len(parts)==10

names={
 'part_0':'RYOKO_Outfit_Trousers','part_1':'RYOKO_Hair_ScalpAndBun',
 'part_2':'RYOKO_Outfit_BlazerAndBlouse','part_3':'RYOKO_Outfit_Sleeve_CharacterLeft',
 'part_4':'RYOKO_Outfit_Sleeve_CharacterRight','part_5':'RYOKO_Footwear_CharacterLeft',
 'part_6':'RYOKO_Skin_Hand_CharacterLeft','part_7':'RYOKO_Footwear_CharacterRight',
 'part_8':'RYOKO_Skin_Hand_CharacterRight','part_9':'RYOKO_Skin_HeadAndNeck'}

# Semantic surfaces are labels only; they never replace the approved geometry.
bvhs={}
for obj in parts:
    world=approval_transform@obj.matrix_world
    verts=[world@v.co for v in obj.data.vertices]
    faces=[tuple(p.vertices) for p in obj.data.polygons]
    bvhs[obj.name]=BVHTree.FromPolygons(verts,faces)

labels={name:i for i,name in enumerate(sorted(names))}
face_labels=[]
for center in base_centers:
    best=None; best_d=float('inf')
    for source,bvh in bvhs.items():
        hit=bvh.find_nearest(center)
        if hit[0] is not None and hit[3]<best_d:
            best_d=hit[3]; best=source
    face_labels.append(best)
# Sleeve shells extend over the wrist in the semantic source. Below the cuff,
# the approved surface is skin, not a glove.
for i,source in enumerate(face_labels):
    center=base_centers[i]
    if source in {'part_3','part_4'} and center.z<1.03 and abs(center.x)>.13:
        face_labels[i]='part_6' if center.x>0 else 'part_8'
for obj in parts: bpy.data.objects.remove(obj,do_unlink=True)

def material(name,color,roughness,metallic=0.0):
    mat=bpy.data.materials.new(name); mat.diffuse_color=(*color,1); mat.use_nodes=True
    bs=mat.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value=(*color,1)
    bs.inputs['Roughness'].default_value=roughness
    bs.inputs['Metallic'].default_value=metallic
    return mat

skin=material('RYOKO_Skin_WarmNeutral',(0.64,0.43,0.32),.58)
hair=material('RYOKO_Hair_MintSage',(0.20,0.48,0.39),.48)
suit=material('RYOKO_Suit_Charcoal',(0.025,0.032,0.042),.68)
blouse=material('RYOKO_Blouse_Ivory',(0.82,0.80,0.74),.72)
shoe=material('RYOKO_Shoes_BlackLeather',(0.018,0.020,0.025),.32)
sole=material('RYOKO_Shoes_LeatherSole',(0.20,0.105,0.055),.62)
gold=bpy.data.materials['RYOKO_HairStick_Gold_Identification']

build=[]
for source in sorted(names):
    selected=[i for i,label in enumerate(face_labels) if label==source]
    if not selected: continue
    used=sorted({v for i in selected for v in base_faces[i]})
    remap={old:new for new,old in enumerate(used)}
    mesh=bpy.data.meshes.new(names[source]+'_Mesh')
    mesh.from_pydata([base_vertices[i] for i in used],[],[tuple(remap[v] for v in base_faces[i]) for i in selected])
    mesh.update()
    obj=bpy.data.objects.new(names[source],mesh); production.objects.link(obj); obj.parent=root
    bpy.ops.object.select_all(action='DESELECT'); obj.select_set(True); bpy.context.view_layer.objects.active=obj
    bm=bmesh.new(); bm.from_mesh(mesh)
    # Repair narrow generated slits by physical loop size, not edge count.
    # Large part boundaries remain open for later joining and deformation work.
    unvisited={e for e in bm.edges if e.is_boundary}
    repaired_loops=0
    while unvisited:
        seed=unvisited.pop(); component={seed}; stack=[seed]
        while stack:
            edge=stack.pop()
            for vertex in edge.verts:
                for linked in vertex.link_edges:
                    if linked.is_boundary and linked in unvisited:
                        unvisited.remove(linked); component.add(linked); stack.append(linked)
        perimeter=sum(e.calc_length() for e in component)
        if perimeter<.055:
            bmesh.ops.holes_fill(bm,edges=list(component),sides=0); repaired_loops+=1
    obj['small_boundary_loops_repaired']=repaired_loops
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces)); bm.to_mesh(mesh); bm.free()
    for p in mesh.polygons: p.use_smooth=True

    # Add density only where later deformation needs it, without replacing the surface.
    if source in {'part_6','part_8','part_9'}:
        sub=obj.modifiers.new('Deformation-area density','SUBSURF'); sub.levels=1; sub.render_levels=1
        bpy.ops.object.modifier_apply(modifier=sub.name)
        # Generated internal shells otherwise cast narrow self-shadow artifacts.
        # This is a presentation workaround, not a claim of clean skin topology.
        obj.visible_shadow=False

    if source=='part_1': mesh.materials.append(hair)
    elif source in {'part_5','part_7'}:
        mesh.materials.append(shoe); mesh.materials.append(sole)
        for p in mesh.polygons:
            z=sum(mesh.vertices[i].co.z for i in p.vertices)/len(p.vertices)
            p.material_index=1 if z<.025 else 0
    elif source=='part_9': mesh.materials.append(skin)
    elif source in {'part_6','part_8'}:
        mesh.materials.append(skin); mesh.materials.append(suit); mesh.materials.append(blouse)
        for p in mesh.polygons:
            z=p.center.z
            p.material_index=1 if z>=1.03 else (2 if z>=.95 else 0)
    elif source=='part_2':
        mesh.materials.append(suit); mesh.materials.append(blouse)
        for p in mesh.polygons:
            c=p.center
            width=.028+.045*max(0,min(1,(c.z-1.08)/.37))
            p.material_index=1 if (c.y<-.055 and 1.06<c.z<1.47 and abs(c.x)<width) else 0
    else: mesh.materials.append(suit)

    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(66),island_margin=.018,correct_aspect=True,scale_to_bounds=True)
    bpy.ops.object.mode_set(mode='OBJECT')
    mesh.calc_loop_triangles()
    bm=bmesh.new(); bm.from_mesh(mesh)
    build.append({'object':obj.name,'source_part':source,'source_faces':len(selected),
      'vertices':len(mesh.vertices),'polygons':len(mesh.polygons),'triangles':len(mesh.loop_triangles),
      'quad_faces':sum(len(p.vertices)==4 for p in mesh.polygons),
      'boundary_edges':sum(e.is_boundary for e in bm.edges),
      'non_manifold_edges':sum(not e.is_manifold for e in bm.edges),
      'uv_layers':len(mesh.uv_layers),'materials':[m.name for m in mesh.materials]})
    bm.free()

for obj in access:
    obj.data.materials.clear(); obj.data.materials.append(hair if obj.name.startswith('RYOKO_Bun_Core') else gold)
    for p in obj.data.polygons: p.use_smooth=True

scene['RYOKO_PHASE']='03 production topology UV material foundation'
scene['RYOKO_SOURCE_APPROVAL']='Phase 02 v002 approved by user; approved surface retained without voxel replacement'
scene['RYOKO_PRODUCTION_NOTE']='Semantic labels split the approved surface into modular parts. Head and hands have one subdivision density pass. Original open/generated topology remains a deformation-rigging limitation.'
scene.unit_settings.system='METRIC'; scene.unit_settings.scale_length=1.0
bpy.ops.wm.save_as_mainfile(filepath=str(DEST))
report={'source_blend':str(SOURCE),'semantic_parts':str(PARTS),
 'semantic_task_id':'370e5e56-a084-4f07-a529-acae63195812','smart_retopology_task_id':'ae55137b-d423-4c9a-87ab-cb729cf33c2c',
 'destination_blend':str(DEST),'construction':'Approved v002 surface retained; Tripo semantic parts used only as nearest-surface labels. No voxel replacement.',
 'parts':build,'total_part_vertices':sum(r['vertices'] for r in build),
 'total_part_triangles':sum(r['triangles'] for r in build),'total_part_quad_faces':sum(r['quad_faces'] for r in build),
 'total_part_boundary_edges':sum(r['boundary_edges'] for r in build),
 'total_part_non_manifold_edges':sum(r['non_manifold_edges'] for r in build),'accessory_objects':len(access),
 'status':'Visually preserved modular UV foundation; original generated open/non-manifold topology is explicitly not certified for rigging.'}
REPORT.write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))

import bpy, bmesh, math, json
from pathlib import Path
from mathutils import Vector
ROOT=Path('/mnt/agents/output/app')
SRC=ROOT/'assets/ryoko_blockout_v001.blend'
DST=ROOT/'assets/ryoko_blockout_v002.blend'
OUT=ROOT/'renders/blockout_final'
bpy.ops.wm.open_mainfile(filepath=str(SRC))
scene=bpy.context.scene
root=bpy.data.objects['RYOKO_BLOCKOUT_ROOT']
mesh=next(o for o in scene.objects if o.type=='MESH' and o.parent==root)
# Identify the same disconnected high-head components used in the diagnostic render.
n=len(mesh.data.vertices); adj=[[] for _ in range(n)]
for e in mesh.data.edges:
    a,b=e.vertices; adj[a].append(b); adj[b].append(a)
seen=bytearray(n); comps=[]
for start in range(n):
    if seen[start]: continue
    stack=[start]; seen[start]=1; ids=[]
    while stack:
        i=stack.pop(); ids.append(i)
        for j in adj[i]:
            if not seen[j]: seen[j]=1; stack.append(j)
    if len(ids)<8: continue
    pts=[mesh.matrix_world @ mesh.data.vertices[i].co for i in ids]
    if max(p.z for p in pts)>1.62: comps.append((len(comps),start,ids))
# Remove the coarse left/right sticks, finials, old chains and tassels.
remove_components={17,18,29,30,31,33,42,50,55,71}
remove=set()
for cid,start,ids in comps:
    if cid in remove_components: remove.update(ids)
# Remove the old shaft path, then close the bun with a separate neutral core.
a=Vector((0.020,0.035,1.712)); b=Vector((0.094,0.132,1.819)); ab=b-a
comp0=next(ids for cid,start,ids in comps if cid==0)
for i in comp0:
    p=mesh.matrix_world @ mesh.data.vertices[i].co
    t=(p-a).dot(ab)/ab.length_squared
    nearest=a+ab*max(0,min(1,t))
    if -0.05<t<1.08 and (p-nearest).length<0.020: remove.add(i)
bm=bmesh.new(); bm.from_mesh(mesh.data)
bm.verts.ensure_lookup_table()
verts=[bm.verts[i] for i in sorted(remove)]
bmesh.ops.delete(bm,geom=verts,context='VERTS')
bm.to_mesh(mesh.data); bm.free(); mesh.data.update()

# Accessory collection and warm identification material; the body remains neutral clay.
coll=bpy.data.collections.get('RYOKO_ACCESSORIES') or bpy.data.collections.new('RYOKO_ACCESSORIES')
if coll.name not in scene.collection.children: scene.collection.children.link(coll)
gold=bpy.data.materials.new('RYOKO_HairStick_Gold_Identification')
gold.diffuse_color=(0.48,0.29,0.075,1); gold.use_nodes=True
bs=gold.node_tree.nodes.get('Principled BSDF')
bs.inputs['Base Color'].default_value=(0.48,0.29,0.075,1)
bs.inputs['Metallic'].default_value=0.65
bs.inputs['Roughness'].default_value=0.30
created=[]
def finish(obj,name,material=gold):
    obj.name=name
    for c in list(obj.users_collection): c.objects.unlink(obj)
    coll.objects.link(obj)
    bpy.context.view_layer.update()
    world=obj.matrix_world.copy()
    obj.parent=root
    obj.matrix_world=world
    if obj.type=='MESH':
        obj.data.materials.append(material)
        for p in obj.data.polygons: p.use_smooth=True
    created.append(obj)
    return obj

def cone_between(name,p1,p2,r1,r2,vertices=32):
    p1,p2=Vector(p1),Vector(p2); d=p2-p1
    bpy.ops.mesh.primitive_cone_add(vertices=vertices,radius1=r1,radius2=r2,depth=d.length,location=(p1+p2)/2)
    o=bpy.context.object; o.rotation_euler=d.to_track_quat('Z','Y').to_euler()
    return finish(o,name)

def sphere(name,p,r):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,radius=r,location=p)
    return finish(bpy.context.object,name)

def torus(name,p,rotation):
    bpy.ops.mesh.primitive_torus_add(major_segments=20,minor_segments=8,major_radius=0.0034,minor_radius=0.00075,location=p,rotation=rotation)
    return finish(bpy.context.object,name)

# Reconstructed neutral bun core closes the exposed generated surface without gold leakage.
bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=16,radius=1.0,location=(0.030,0.065,1.750))
core=bpy.context.object
core.scale=(0.060,0.060,0.055)
finish(core,'RYOKO_Bun_Core_Neutral',mesh.data.materials[0])
bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,radius=1.0,location=(0.075,0.095,1.770))
side_fill=bpy.context.object
side_fill.scale=(0.030,0.035,0.032)
finish(side_fill,'RYOKO_Bun_Core_SideFill',mesh.data.materials[0])

sticks=[
    ('A',(-0.045,0.015,1.700),(0.105,0.130,1.825)),
    ('B',(-0.035,0.055,1.735),(0.115,0.100,1.780)),
]
for label,start,end in sticks:
    p1,p2=Vector(start),Vector(end); axis=(p2-p1).normalized()
    cone_between(f'RYOKO_Chopstick_{label}_TaperedShaft',p1,p2,0.0022,0.0060 if label=='A' else 0.0042)
    sphere(f'RYOKO_Chopstick_{label}_RoundFinial',p2,0.010)
    cone_between(f'RYOKO_Chopstick_{label}_FinialCollar',p2-axis*0.018,p2-axis*0.007,0.0055,0.0055)
# One short chain and pendant on lower stick B, matching the accessory sheet.
end=Vector(sticks[1][2])
for i in range(3):
    torus(f'RYOKO_HairStick_ChainLink_{i+1:02d}',end+Vector((0,0,-0.014-i*0.0065)),(math.pi/2,0,(i%2)*math.pi/2))
cone_between('RYOKO_HairStick_Pendant_Bail',end+Vector((0,0,-0.034)),end+Vector((0,0,-0.040)),0.0022,0.0022,16)
pendant=cone_between('RYOKO_HairStick_Pendant',end+Vector((0,0,-0.041)),end+Vector((0,0,-0.078)),0.0042,0.0012,6)

# Render the revised construction before saving the final source.
cam=scene.camera
head=(0,0.035,1.715)
for name,loc in [
    ('revision_hair_front',(0,-2.6,1.74)),
    ('revision_hair_back',(0,2.6,1.74)),
    ('revision_hair_left',(2.6,0,1.74)),
    ('revision_hair_three_quarter',(1.85,-1.85,1.82)),
]:
    cam.location=loc; cam.rotation_euler=(Vector(head)-cam.location).to_track_quat('-Z','Y').to_euler(); cam.data.ortho_scale=.55
    scene.render.filepath=str(OUT/f'{name}.png'); bpy.ops.render.render(write_still=True)
cam.location=(0,-6,1.02); cam.rotation_euler=(Vector((0,0,.93))-cam.location).to_track_quat('-Z','Y').to_euler(); cam.data.ortho_scale=2.02
scene.render.filepath=str(OUT/'revision_full_front.png'); bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(DST))
report={
    'source_blend':str(SRC),'revised_blend':str(DST),
    'removed_generated_vertices':len(remove),
    'removed_component_ids':sorted(remove_components),
    'new_accessory_mesh_objects':len(created),
    'design':'Exactly two tapered chopstick-style hair sticks with rounded finials; one short chain and pendant on the lower stick.',
    'placement':'Both sticks cross the bun and project to character-left (+X), matching the approved accessory reference.'
}
(ROOT/'assets/hair_stick_revision.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))

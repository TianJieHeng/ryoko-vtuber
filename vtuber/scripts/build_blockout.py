import bpy, math, json
from pathlib import Path
from mathutils import Vector

ROOT=Path('/mnt/agents/output/app')
SRC=ROOT/'assets/ryoko_blockout_tripo.glb'
BLEND=ROOT/'assets/ryoko_blockout_v001.blend'
OUT=ROOT/'renders/blockout_orbit'
OUT.mkdir(parents=True,exist_ok=True)

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for datablocks in (bpy.data.materials, bpy.data.cameras, bpy.data.lights):
    for block in list(datablocks):
        if block.users == 0:
            datablocks.remove(block)

bpy.ops.import_scene.gltf(filepath=str(SRC))
imported=list(bpy.context.selected_objects)
mesh_objects=[o for o in imported if o.type=='MESH']
if not mesh_objects:
    raise RuntimeError('No mesh geometry imported')

# Normalize as a provisional blockout. Final skull-based height is refined later.
bpy.context.view_layer.update()
def bounds(objects):
    pts=[o.matrix_world @ Vector(c) for o in objects for c in o.bound_box]
    return Vector((min(p.x for p in pts),min(p.y for p in pts),min(p.z for p in pts))), Vector((max(p.x for p in pts),max(p.y for p in pts),max(p.z for p in pts)))
lo,hi=bounds(mesh_objects)
height=hi.z-lo.z
if height <= 0:
    raise RuntimeError('Invalid imported height')
root=bpy.data.objects.new('RYOKO_BLOCKOUT_ROOT',None)
bpy.context.collection.objects.link(root)
for o in imported:
    if o.parent is None:
        o.parent=root
scale=1.83/height
root.scale=(scale,scale,scale)
bpy.context.view_layer.update()
lo,hi=bounds(mesh_objects)
center_x=(lo.x+hi.x)/2
center_y=(lo.y+hi.y)/2
root.location=(-center_x,-center_y,-lo.z)
bpy.context.view_layer.update()
lo,hi=bounds(mesh_objects)

clay=bpy.data.materials.new('RYOKO_Clay_Neutral')
clay.diffuse_color=(0.56,0.60,0.62,1)
clay.use_nodes=True
bsdf=clay.node_tree.nodes.get('Principled BSDF')
bsdf.inputs['Base Color'].default_value=(0.56,0.60,0.62,1)
bsdf.inputs['Roughness'].default_value=0.72
bsdf.inputs['Metallic'].default_value=0.0
for o in mesh_objects:
    o.data.materials.clear()
    o.data.materials.append(clay)
    for poly in o.data.polygons:
        poly.use_smooth=True

# Ground and neutral studio light.
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-0.002))
ground=bpy.context.object
ground.name='STUDIO_Ground'
mat=bpy.data.materials.new('STUDIO_Ground_Mat')
mat.diffuse_color=(0.12,0.14,0.16,1)
mat.use_nodes=True
gbsdf=mat.node_tree.nodes.get('Principled BSDF')
gbsdf.inputs['Base Color'].default_value=(0.12,0.14,0.16,1)
gbsdf.inputs['Roughness'].default_value=0.9
ground.data.materials.append(mat)

world=bpy.data.worlds.new('STUDIO_World')
world.use_nodes=True
world.node_tree.nodes['Background'].inputs['Color'].default_value=(0.32,0.35,0.38,1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value=0.65
bpy.context.scene.world=world
sun_data=bpy.data.lights.new('STUDIO_Sun','SUN')
sun_data.energy=2.2
sun_data.angle=math.radians(18)
sun=bpy.data.objects.new('STUDIO_Sun',sun_data)
bpy.context.collection.objects.link(sun)
sun.rotation_euler=(math.radians(28),math.radians(-24),math.radians(-32))

cam_data=bpy.data.cameras.new('STUDIO_Camera')
cam=bpy.data.objects.new('STUDIO_Camera',cam_data)
bpy.context.collection.objects.link(cam)
cam_data.type='ORTHO'
cam_data.ortho_scale=2.18
cam_data.clip_start=0.01
cam_data.clip_end=100
bpy.context.scene.camera=cam

def point_camera(location,target,scale=2.18):
    cam.location=location
    cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler()
    cam_data.ortho_scale=scale

def render(name):
    scene=bpy.context.scene
    scene.render.filepath=str(OUT/f'{name}.png')
    bpy.ops.render.render(write_still=True)

scene=bpy.context.scene
scene.render.engine='CYCLES'
scene.cycles.device='CPU'
scene.cycles.samples=24
scene.cycles.use_denoising=True
scene.render.resolution_x=800
scene.render.resolution_y=800
scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.render.film_transparent=False
scene.unit_settings.system='METRIC'
scene.unit_settings.scale_length=1.0
scene.view_settings.view_transform='AgX'
scene.render.image_settings.color_mode='RGB'

# Save reopenable source before rendering.
bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))

target=Vector((0,0,0.93))
radius=6.0
elev=math.radians(15)
for i in range(8):
    a=2*math.pi*i/8
    loc=(radius*math.cos(a)*math.cos(elev),radius*math.sin(a)*math.cos(elev),target.z+radius*math.sin(elev))
    point_camera(loc,target)
    render(f'orbit_{i:02d}_deg_{i*45:03d}')
point_camera((0,0,7),(0,0,0),2.6)
render('top')

triangles=0
vertices=0
for o in mesh_objects:
    vertices+=len(o.data.vertices)
    triangles+=sum(max(1,len(p.vertices)-2) for p in o.data.polygons)
metrics={
    'source':'Tripo API multiview v3.1',
    'task_id':'d8fd4168-12f1-4175-810d-02e05ceace79',
    'mesh_objects':len(mesh_objects),
    'vertices':vertices,
    'triangles':triangles,
    'bounds_min':list(lo),
    'bounds_max':list(hi),
    'provisional_total_height_m':hi.z-lo.z,
    'blend':str(BLEND),
}
(ROOT/'assets/blockout_metrics.json').write_text(json.dumps(metrics,indent=2))
print(json.dumps(metrics,indent=2))

import bpy
from pathlib import Path
from PIL import Image, ImageDraw
from mathutils import Vector
ROOT=Path('/mnt/agents/output/app')
OUT=ROOT/'renders/mesh_uv_textured_v001'
checker=Image.new('RGB',(1024,1024)); d=ImageDraw.Draw(checker)
for y in range(16):
 for x in range(16):
  color=(224,231,229) if (x+y)%2 else (38,91,91)
  d.rectangle((x*64,y*64,x*64+63,y*64+63),fill=color)
  d.text((x*64+5,y*64+4),f'{x:X}{y:X}',fill=(235,190,85) if (x+y)%2 else (215,230,224))
path=ROOT/'assets/uv_checker_grid.png'; checker.save(path)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'assets/ryoko_mesh_uv_textured_v001.blend'))
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=24;s.cycles.use_denoising=True
s.render.resolution_x=800;s.render.resolution_y=800;s.render.resolution_percentage=100
mat=bpy.data.materials.new('UV_CHECKER_ONLY');mat.use_nodes=True
n=mat.node_tree.nodes;l=mat.node_tree.links;bs=n.get('Principled BSDF');tex=n.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(path));l.new(tex.outputs['Color'],bs.inputs['Base Color']);bs.inputs['Roughness'].default_value=.75
for obj in bpy.data.collections['RYOKO_PRODUCTION'].objects:
 if obj.type=='MESH' and obj.name.endswith(('_FittedMaterial')): pass
 if obj.type=='MESH' and any(m and m.name.endswith('_FittedMaterial') for m in obj.data.materials):
  obj.data.materials.clear();obj.data.materials.append(mat)
c=s.camera
for name,loc,target,scale in [('uv_checker_front',(0,-6,1.02),(0,0,.93),2.02),('uv_checker_head',(0,-2.6,1.69),(0,0,1.665),.55)]:
 c.location=loc;c.rotation_euler=(Vector(target)-c.location).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=scale
 s.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
print('UV checker views rendered; source blend was not modified.')

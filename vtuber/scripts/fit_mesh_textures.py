import bpy, json, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path('/mnt/agents/output/app')
SOURCE=ROOT/'assets/ryoko_mesh_uv_v003.blend'
DEST=ROOT/'assets/ryoko_mesh_uv_textured_v001.blend'
TEX=ROOT/'assets/textures/mesh_uv_textured_v001'
TEX.mkdir(parents=True,exist_ok=True)
REPORT=ROOT/'assets/texture_build_v001.json'
bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
scene=bpy.context.scene
scene.render.engine='CYCLES'; scene.cycles.device='CPU'; scene.cycles.samples=8
scene.render.bake.margin=8; scene.render.bake.use_clear=True

# Smooth world-space blouse mask, baked to the blazer UVs rather than assigned per face.
blazer=bpy.data.objects['RYOKO_Outfit_BlazerAndBlouse']
mat=bpy.data.materials.new('RYOKO_BlazerBlouse_FittedSource'); mat.use_nodes=True
n=mat.node_tree.nodes; l=mat.node_tree.links; n.clear()
out=n.new('ShaderNodeOutputMaterial'); bs=n.new('ShaderNodeBsdfPrincipled')
bs.inputs['Roughness'].default_value=.68; l.new(bs.outputs['BSDF'],out.inputs['Surface'])
geo=n.new('ShaderNodeNewGeometry'); sep=n.new('ShaderNodeSeparateXYZ'); l.new(geo.outputs['Position'],sep.inputs[0])
def mathnode(op,a,b=None):
    node=n.new('ShaderNodeMath'); node.operation=op
    for i,value in enumerate([a,b]):
        if value is None: continue
        if isinstance(value,(float,int)): node.inputs[i].default_value=value
        else: l.new(value,node.inputs[i])
    return node.outputs[0]
def maprange(value,a,b,c,d):
    node=n.new('ShaderNodeMapRange'); node.interpolation_type='SMOOTHSTEP'; node.clamp=True
    l.new(value,node.inputs['Value'])
    for key,v in [('From Min',a),('From Max',b),('To Min',c),('To Max',d)]:
        if isinstance(v,(float,int)): node.inputs[key].default_value=v
        else: l.new(v,node.inputs[key])
    return node.outputs['Result']
width=mathnode('ADD',mathnode('MULTIPLY',maprange(sep.outputs['Z'],1.08,1.45,0,1),.045),.028)
absx=mathnode('ABSOLUTE',sep.outputs['X'])
xmask=maprange(absx,mathnode('SUBTRACT',width,.003),mathnode('ADD',width,.003),1,0)
ymask=maprange(sep.outputs['Y'],-.045,-.065,0,1)
zmask=mathnode('MULTIPLY',maprange(sep.outputs['Z'],1.055,1.065,0,1),maprange(sep.outputs['Z'],1.465,1.475,1,0))
mask=mathnode('MULTIPLY',mathnode('MULTIPLY',xmask,ymask),zmask)
mix=n.new('ShaderNodeMixRGB'); mix.blend_type='MIX'; l.new(mask,mix.inputs[0])
mix.inputs[1].default_value=(.025,.032,.042,1); mix.inputs[2].default_value=(.82,.80,.74,1)
l.new(mix.outputs[0],bs.inputs['Base Color'])
blazer.data.materials.clear(); blazer.data.materials.append(mat)
for p in blazer.data.polygons: p.material_index=0

objects=[o for o in bpy.data.collections['RYOKO_PRODUCTION'].objects if o.type=='MESH' and o.name in {
 'RYOKO_Outfit_Trousers','RYOKO_Hair_ScalpAndBun','RYOKO_Outfit_BlazerAndBlouse',
 'RYOKO_Outfit_Sleeve_CharacterLeft','RYOKO_Outfit_Sleeve_CharacterRight',
 'RYOKO_Footwear_CharacterLeft','RYOKO_Skin_Hand_CharacterLeft','RYOKO_Footwear_CharacterRight',
 'RYOKO_Skin_Hand_CharacterRight','RYOKO_Skin_HeadAndNeck'}]
records=[]

def bake_one(obj,kind,path,size):
    image=bpy.data.images.new(path.stem,width=size,height=size,alpha=False)
    image.colorspace_settings.name='sRGB' if kind=='DIFFUSE' else 'Non-Color'
    for material in obj.data.materials:
        nodes=material.node_tree.nodes
        target=nodes.new('ShaderNodeTexImage'); target.image=image; target.name='BAKE_TARGET'
        nodes.active=target
        for node in nodes: node.select=False
        target.select=True
    bpy.ops.object.select_all(action='DESELECT'); obj.select_set(True); bpy.context.view_layer.objects.active=obj
    if kind=='DIFFUSE': bpy.ops.object.bake(type='DIFFUSE',pass_filter={'COLOR'})
    else: bpy.ops.object.bake(type='ROUGHNESS')
    image.filepath_raw=str(path); image.file_format='PNG'; image.save()
    for material in obj.data.materials:
        nodes=material.node_tree.nodes
        target=nodes.get('BAKE_TARGET')
        if target: nodes.remove(target)
    bpy.data.images.remove(image)
    loaded=bpy.data.images.load(str(path),check_existing=True)
    loaded.colorspace_settings.name='sRGB' if kind=='DIFFUSE' else 'Non-Color'
    loaded.pack()
    return loaded

for obj in sorted(objects,key=lambda o:o.name):
    size=2048 if obj.name in {'RYOKO_Outfit_BlazerAndBlouse','RYOKO_Skin_HeadAndNeck','RYOKO_Hair_ScalpAndBun'} else 1024
    slug=obj.name.replace('RYOKO_','')
    base=bake_one(obj,'DIFFUSE',TEX/(slug+'_BaseColor.png'),size)
    rough=bake_one(obj,'ROUGHNESS',TEX/(slug+'_Roughness.png'),size)
    fitted=bpy.data.materials.new(obj.name+'_FittedMaterial'); fitted.use_nodes=True
    nodes=fitted.node_tree.nodes; links=fitted.node_tree.links
    bs=nodes.get('Principled BSDF')
    bt=nodes.new('ShaderNodeTexImage'); bt.image=base; bt.label='Model-fitted base color'; links.new(bt.outputs['Color'],bs.inputs['Base Color'])
    rt=nodes.new('ShaderNodeTexImage'); rt.image=rough; rt.label='Model-fitted roughness'; links.new(rt.outputs['Color'],bs.inputs['Roughness'])
    obj.data.materials.clear(); obj.data.materials.append(fitted)
    for p in obj.data.polygons: p.material_index=0
    records.append({'object':obj.name,'resolution':size,'base_color':str(TEX/(slug+'_BaseColor.png')),'roughness':str(TEX/(slug+'_Roughness.png'))})
    print('Fitted textures:',obj.name,size,flush=True)

scene['RYOKO_TEXTURE_NOTE']='Each major modular part has its own UV-fitted base-color and roughness texture. Gold accessories remain uniform rigid materials.'
bpy.ops.wm.save_as_mainfile(filepath=str(DEST))
REPORT.write_text(json.dumps({'source_blend':str(SOURCE),'destination_blend':str(DEST),'texture_sets':records},indent=2))

# UV layout contact sheet: each part owns an independent 0–1 texture space.
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',22)
small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
panel=620; header=58
sheet=Image.new('RGB',(panel*2,(panel+header)*5+72),(19,25,30)); draw=ImageDraw.Draw(sheet)
draw.text((24,18),'PHASE 03  /  UV LAYOUTS — INDEPENDENT TEXTURE SETS',font=font,fill=(230,237,239))
for index,obj in enumerate(sorted(objects,key=lambda o:o.name)):
    ox=(index%2)*panel; oy=72+(index//2)*(panel+header)
    draw.text((ox+18,oy+14),obj.name.replace('RYOKO_','').replace('_',' '),font=small,fill=(220,231,232))
    x0=ox+18; y0=oy+header; side=panel-36
    for g in range(17):
        c=(48,61,67) if g%2 else (40,51,57)
        draw.line((x0+g*side/16,y0,x0+g*side/16,y0+side),fill=c)
        draw.line((x0,y0+g*side/16,x0+side,y0+g*side/16),fill=c)
    uv=obj.data.uv_layers.active.data
    for poly in obj.data.polygons:
        pts=[]
        for li in poly.loop_indices:
            co=uv[li].uv; pts.append((x0+co.x*side,y0+(1-co.y)*side))
        draw.line(pts+[pts[0]],fill=(104,211,174),width=1)
    draw.rectangle((x0,y0,x0+side,y0+side),outline=(151,167,171),width=2)
preview=Path('/mnt/agents/output/vtuber/previews/phase_03'); preview.mkdir(parents=True,exist_ok=True)
sheet.save(preview/'UV Layouts — Modular Texture Sets.png')
sheet.save(ROOT/'assets/uv_layouts_v001.png')
print('Texture fitting and UV board complete.',flush=True)

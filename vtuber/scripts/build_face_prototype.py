import bpy, math, json
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT=Path('/mnt/agents/output/app')
SOURCE=ROOT/'assets/ryoko_mesh_uv_textured_v001.blend'
DEST=ROOT/'assets/ryoko_face_prototype_v001.blend'
REPORT=ROOT/'assets/face_prototype_build_v001.json'
OUT=ROOT/'renders/phase_04'
OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
bpy.context.view_layer.update()
scene=bpy.context.scene
head=bpy.data.objects['RYOKO_Skin_HeadAndNeck']
world_verts=[head.matrix_world@v.co for v in head.data.vertices]
bvh=BVHTree.FromPolygons(world_verts,[tuple(p.vertices) for p in head.data.polygons])
root=bpy.data.objects['RYOKO_PRODUCTION_ROOT']
collection=bpy.data.collections.new('RYOKO_FACE_PROTOTYPE')
scene.collection.children.link(collection)
control=bpy.data.objects.new('RYOKO_FACE_CONTROLS',None)
collection.objects.link(control); control.parent=root; control.empty_display_size=.035
properties={
 'blink_left':0.0,'blink_right':0.0,'gaze_x':0.0,'gaze_y':0.0,
 'jaw_open':0.0,'smile':0.0,'funnel':0.0,'wide':0.0}
for name,value in properties.items():
    control[name]=value
    control.id_properties_ui(name).update(min=-1.0 if name.startswith('gaze_') else 0.0,max=1.0,description='Phase 04 feasibility control; 0 neutral, 1 full prototype range')
control['checkpoint']='Phase 04 early facial feasibility only; not the complete ARKit rig'

def surface_y(x,z):
    hit=bvh.ray_cast(Vector((x,-1,z)),Vector((0,1,0)),2)
    if hit[0] is not None: return hit[0].y
    near=bvh.find_nearest(Vector((x,-.08,z)))
    return near[0].y if near[0] is not None else -.08

def point(x,z,offset):
    return Vector((x,surface_y(x,z)-offset,z))

def material(name,color,roughness=.55,metallic=0.0,emission=0.0):
    mat=bpy.data.materials.new(name); mat.diffuse_color=(*color,1); mat.use_nodes=True
    bs=mat.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value=(*color,1)
    bs.inputs['Roughness'].default_value=roughness
    bs.inputs['Metallic'].default_value=metallic
    if emission:
        bs.inputs['Emission Color'].default_value=(*color,1)
        bs.inputs['Emission Strength'].default_value=emission
    return mat

skin=head.data.materials[0].copy(); skin.name='RYOKO_FacePrototype_FittedSkin'
# Reuse the head's fitted skin texture; a vertex mask fades only the outer lid seam.
skin_nodes=skin.node_tree.nodes; skin_links=skin.node_tree.links
skin_bs=skin_nodes.get('Principled BSDF')
fade_node=skin_nodes.new('ShaderNodeVertexColor'); fade_node.layer_name='LidFade'
skin_links.new(fade_node.outputs['Color'],skin_bs.inputs['Alpha'])
white=material('RYOKO_Eye_WarmWhite',(.91,.88,.80),.38)
lash=material('RYOKO_Lash_Espresso',(.022,.010,.008),.48)
brow=material('RYOKO_Brow_MintShadow',(.075,.22,.17),.62)
iris_dark=material('RYOKO_Iris_OuterAmber',(.24,.085,.012),.4)
iris_mid=material('RYOKO_Iris_Amber',(.72,.32,.025),.36)
iris_gold=material('RYOKO_Iris_Gold',(.95,.60,.065),.34)
pupil=material('RYOKO_Pupil',(.006,.004,.003),.32)
highlight=material('RYOKO_Eye_Catchlight',(.98,.96,.84),.25,emission=.35)
lips=material('RYOKO_Lips_MutedRose',(.48,.19,.15),.5)
mouth_dark=material('RYOKO_Mouth_Cavity',(.055,.008,.011),.72)
teeth=material('RYOKO_Teeth_Ivory',(.88,.84,.73),.42)
tongue=material('RYOKO_Tongue_Rose',(.48,.12,.15),.55)

created=[]
def mesh_object(name,verts,faces,materials,indices=None):
    mesh=bpy.data.meshes.new(name+'_Mesh'); mesh.from_pydata(verts,[],faces); mesh.update()
    obj=bpy.data.objects.new(name,mesh); collection.objects.link(obj); obj.parent=root
    for mat in materials: mesh.materials.append(mat)
    for i,p in enumerate(mesh.polygons):
        p.use_smooth=True
        if indices is not None: p.material_index=indices[i]
    created.append(obj)
    return obj

def shape(obj,name,coords):
    if obj.data.shape_keys is None: obj.shape_key_add(name='Basis')
    key=obj.shape_key_add(name=name)
    for v,co in zip(key.data,coords): v.co=co
    return key

def drive(obj,key_name,prop,expression='v'):
    key=obj.data.shape_keys.key_blocks[key_name]
    curve=key.driver_add('value'); driver=curve.driver; driver.type='SCRIPTED'
    var=driver.variables.new(); var.name='v'; var.type='SINGLE_PROP'
    var.targets[0].id=control; var.targets[0].data_path='["'+prop+'"]'
    driver.expression=expression

EX=.0345; EZ=1.651; EHW=.0185; EHH=.0068

def eye_point(side,t):
    c=math.cos(t); s=math.sin(t)
    x=side*EX+EHW*c
    z=EZ+EHH*s+side*.0025*c
    return x,z

def closed_eye_point(side,t):
    c=math.cos(t)
    return side*EX+EHW*c,EZ-.0005+side*.0025*c

def eye_ring_coords(side,blink):
    n=64; rings=5; verts=[]
    for j in range(rings):
        f=j/(rings-1)
        for i in range(n):
            t=2*math.pi*i/n
            x,z=eye_point(side,t); cx,cz=closed_eye_point(side,t)
            x=side*EX+(x-side*EX)*(1+.36*f)
            z=EZ+(z-EZ)*(1+.72*f)
            cx=side*EX+(cx-side*EX)*(1+.36*f)
            cz=EZ+(cz-EZ)*(1+.72*f)
            closed_band_z=cz+(z-EZ)*.18*f
            z=z*(1-blink)+closed_band_z*blink
            # The eye insert compresses with the lid; the closed lid is a shallow skin band, not a folded membrane.
            base_offset=.0026*(1-f)+.00015*f
            offset=base_offset*(1-blink)+.0032*blink
            verts.append(point(x,z,offset))
    return verts

def eye_ring_faces():
    n=64; rings=5; faces=[]
    for j in range(rings-1):
        for i in range(n):
            ni=(i+1)%n
            faces.append((j*n+i,j*n+ni,(j+1)*n+ni,(j+1)*n+i))
    return faces

def lash_coords(side,blink):
    verts=[]
    # One continuous upper ribbon avoids corner and lower-lid overlap in the feasibility mesh.
    for i in range(33):
        t=math.pi*i/32
        x,z=eye_point(side,t); cx,cz=closed_eye_point(side,t)
        z=z*(1-blink)+cz*blink
        taper=.70+.30*math.sin(t)
        width=.00155*(1-.15*blink)*taper
        verts.append(point(x,z+width,.0040))
        verts.append(point(x,z-width,.0040))
    return verts

def lash_faces():
    return [(2*i,2*i+1,2*i+3,2*i+2) for i in range(32)]

def closed_eye_coords(coords,side,offset):
    closed=[]
    for co in coords:
        x,y,z=co
        cz=EZ-.0005+side*.0025*(x-side*EX)/EHW
        closed.append(point(x,cz,offset))
    return closed

def fit_skin_uv_and_fade(obj):
    uv=obj.data.uv_layers.new(name='FittedSkinUV')
    source_uv=head.data.uv_layers.active
    attr=obj.data.color_attributes.new(name='LidFade',type='FLOAT_COLOR',domain='POINT')
    for v in obj.data.vertices:
        f=(v.index//64)/4
        fade=1.0 if f<=.55 else max(0.0,(1-f)/.45)
        fade=fade*fade*(3-2*fade)
        attr.data[v.index].color=(fade,fade,fade,1)
    for poly in obj.data.polygons:
        for li in poly.loop_indices:
            v=obj.data.vertices[obj.data.loops[li].vertex_index]
            hit=bvh.find_nearest(obj.matrix_world@v.co)
            if hit[0] is not None:
                source_poly=head.data.polygons[hit[2]]
                source_li=min(source_poly.loop_indices,key=lambda si:(head.matrix_world@head.data.vertices[head.data.loops[si].vertex_index].co-hit[0]).length_squared)
                uv.data[li].uv=source_uv.data[source_li].uv
    obj.visible_shadow=False

def blink_material(obj,prop):
    mat=obj.data.materials[0]
    nodes=mat.node_tree.nodes; links=mat.node_tree.links
    bs=nodes.get('Principled BSDF')
    fade=next(n for n in nodes if n.bl_idname=='ShaderNodeVertexColor')
    value=nodes.new('ShaderNodeValue'); value.name='BlinkVisibility'; value.label='Blink visibility'
    mult=nodes.new('ShaderNodeMath'); mult.operation='MULTIPLY'
    links.new(fade.outputs['Color'],mult.inputs[0]); links.new(value.outputs[0],mult.inputs[1]); links.new(mult.outputs[0],bs.inputs['Alpha'])
    curve=value.outputs[0].driver_add('default_value'); driver=curve.driver; driver.type='SCRIPTED'
    var=driver.variables.new(); var.name='v'; var.type='SINGLE_PROP'
    var.targets[0].id=control; var.targets[0].data_path='["'+prop+'"]'; driver.expression='v'

for side,label,prop in [(1,'CharacterLeft','blink_left'),(-1,'CharacterRight','blink_right')]:
    white_verts=[point(side*EX,EZ,.0011)]; white_faces=[]
    for j in range(1,5):
        r=j/4
        for i in range(64):
            x,z=eye_point(side,2*math.pi*i/64)
            white_verts.append(point(side*EX+r*(x-side*EX),EZ+r*(z-EZ),.0011))
    for i in range(64): white_faces.append((0,1+i,1+(i+1)%64))
    for j in range(3):
        a=1+j*64; b=a+64
        for i in range(64):
            ni=(i+1)%64; white_faces.append((a+i,a+ni,b+ni,b+i))
    white_obj=mesh_object('RYOKO_EyeWhite_'+label,white_verts,white_faces,[white])
    drive(white_obj,shape(white_obj,'Blink',closed_eye_coords(white_verts,side,.0011)).name,prop)
    ring=mesh_object('RYOKO_Eyelids_'+label,eye_ring_coords(side,0),eye_ring_faces(),[skin])
    ring.data.materials[0]=skin.copy(); ring.data.materials[0].name='RYOKO_FittedEyelid_'+label
    fit_skin_uv_and_fade(ring); blink_material(ring,prop)
    drive(ring,shape(ring,'Blink',eye_ring_coords(side,1)).name,prop)
    lashes=mesh_object('RYOKO_Lashes_'+label,lash_coords(side,0),lash_faces(),[lash])
    drive(lashes,shape(lashes,'Blink',lash_coords(side,1)).name,prop)


def iris_coords(side,dx,dz):
    verts=[]; faces=[]; indices=[]
    cx=side*EX+dx; cz=EZ+dz
    def disk(cx,cz,rx,rz,mat,rings=1,offset=.0018):
        base=len(verts); n=48
        verts.append(point(cx,cz,offset))
        for j in range(1,rings+1):
            r=j/rings
            for i in range(n):
                t=2*math.pi*i/n
                verts.append(point(cx+rx*r*math.cos(t),cz+rz*r*math.sin(t),offset))
        for i in range(n):
            faces.append((base,base+1+i,base+1+(i+1)%n)); indices.append(mat)
        for j in range(rings-1):
            a=base+1+j*n; b=a+n
            for i in range(n):
                ni=(i+1)%n
                faces.append((a+i,a+ni,b+ni,b+i)); indices.append(mat)
    disk(cx,cz,.0063,.0065,0,rings=3)
    # Material rings are assigned after construction by radial face groups.
    disk(cx,cz,.00275,.0032,3,offset=.00195)
    disk(cx-.0018,cz+.0024,.00135,.00135,4,offset=.00205)
    disk(cx+.0019,cz-.0021,.00065,.00065,4,offset=.00205)
    return verts,faces,indices

for side,label,prop in [(1,'CharacterLeft','blink_left'),(-1,'CharacterRight','blink_right')]:
    verts,faces,indices=iris_coords(side,0,0)
    iris=mesh_object('RYOKO_IrisAssembly_'+label,verts,faces,[iris_mid,iris_dark,iris_gold,pupil,highlight],indices)
    drive(iris,shape(iris,'Blink',closed_eye_coords(verts,side,.0018)).name,prop)
    # Outer/middle/inner amber rings on the first disk.
    for p in iris.data.polygons:
        if p.index<48: p.material_index=1
        elif p.index<144: p.material_index=0
        elif p.index<240: p.material_index=2
    for name,dx,dz,expr in [
        ('GazeLeft',-.003,0,'max(-v,0)'),('GazeRight',.003,0,'max(v,0)'),
        ('GazeUp',0,.0014,'max(v,0)'),('GazeDown',0,-.0014,'max(-v,0)')]:
        coords,_,_=iris_coords(side,dx,dz)
        drive(iris,shape(iris,name,coords).name,'gaze_x' if dx else 'gaze_y',expr)
    # Mint brow ribbon; long fringe intentionally remains untouched.
    verts=[]; faces=[]
    for i in range(25):
        u=-1+2*i/24
        x=side*EX+.020*u
        z=1.673+.0032*(1-u*u)+side*.0010*u
        width=.00135*(.65+.35*(1-u*u))
        verts.extend([point(x,z+width,.0016),point(x,z-width,.0016)])
    for i in range(24): faces.append((2*i,2*i+1,2*i+3,2*i+2))
    mesh_object('RYOKO_Brow_'+label,verts,faces,[brow])

MCZ=1.588; MHW=.0165

def mouth_point(t,jaw=0,smile=0,funnel=0,wide=0,outer=False):
    c=math.cos(t); s=math.sin(t)
    hw=MHW*(1+.18*smile-.45*funnel+.28*wide)
    hh=.0010+.014*jaw+.0015*smile+.007*funnel+.005*wide
    cz=MCZ-.006*jaw-.002*funnel+.0005*smile
    if outer:
        hw+=.0015; hh+=.0018
    x=hw*c
    z=cz+hh*s+smile*.0035*abs(c)**4
    return x,z

def mouth_ring_coords(jaw=0,smile=0,funnel=0,wide=0):
    n=64; rings=4; verts=[]
    for j in range(rings):
        f=j/(rings-1)
        for i in range(n):
            t=2*math.pi*i/n
            xi,zi=mouth_point(t,jaw,smile,funnel,wide,False)
            xo,zo=mouth_point(t,jaw,smile,funnel,wide,True)
            x=xi*(1-f)+xo*f; z=zi*(1-f)+zo*f
            verts.append(point(x,z,.00225*(1-f)+.00045*f))
    return verts

def mouth_disk_coords(jaw=0,smile=0,funnel=0,wide=0):
    n=64; rings=7
    cz=MCZ-.006*jaw-.002*funnel+.0005*smile
    verts=[point(0,cz,.00165)]
    for j in range(1,rings+1):
        r=j/rings
        for i in range(n):
            x,z=mouth_point(2*math.pi*i/n,jaw,smile,funnel,wide)
            verts.append(point(r*x,cz+r*(z-cz),.00165))
    return verts

def mouth_disk_faces():
    n=64; rings=7; faces=[(0,1+i,1+(i+1)%n) for i in range(n)]
    for j in range(rings-1):
        a=1+j*n; b=a+n
        for i in range(n):
            ni=(i+1)%n; faces.append((a+i,a+ni,b+ni,b+i))
    return faces

def teeth_coords(upper=True,jaw=0,smile=0,funnel=0,wide=0):
    verts=[]; faces=[]; n=49
    openness=max(jaw,funnel,wide,.55*smile)
    for i in range(n):
        u=-.78+1.56*i/(n-1)
        hw=MHW*(1+.18*smile-.45*funnel+.28*wide)
        x=hw*u
        t=math.acos(max(-1,min(1,u))) if upper else (2*math.pi-math.acos(max(-1,min(1,u))))
        _,z=mouth_point(t,jaw,smile,funnel,wide)
        h=.00012+(.0035 if upper else .0024)*openness
        z0=z+(.0001 if upper else -.0001)
        z1=z0-h if upper else z0+h
        verts.extend([point(x,z0,.00210),point(x,z1,.00210)])
    for i in range(n-1): faces.append((2*i,2*i+1,2*i+3,2*i+2))
    return verts,faces

def tongue_coords(jaw=0,smile=0,funnel=0,wide=0):
    openness=max(jaw,funnel,wide,.45*smile)
    rx=.0090*(1-.30*funnel+.12*wide)
    rz=.00015+.0045*openness
    cz=MCZ-.0010-.0090*jaw-.0040*funnel-.0030*wide+.0010*smile
    n=48; rings=5; verts=[point(0,cz,.00205)]
    for j in range(1,rings+1):
        r=j/rings
        for i in range(n):
            t=2*math.pi*i/n
            verts.append(point(r*rx*math.cos(t),cz+r*rz*math.sin(t),.00205))
    return verts

def tongue_faces():
    n=48; rings=5; faces=[(0,1+i,1+(i+1)%n) for i in range(n)]
    for j in range(rings-1):
        a=1+j*n; b=a+n
        for i in range(n):
            ni=(i+1)%n; faces.append((a+i,a+ni,b+ni,b+i))
    return faces

cavity=mesh_object('RYOKO_Mouth_CavityInsert',mouth_disk_coords(),mouth_disk_faces(),[mouth_dark])
lipring=mesh_object('RYOKO_Lips_Deforming',mouth_ring_coords(),eye_ring_faces()[:0] if False else [],[lips])
# Rebuild lip-ring faces with four radial rings.
lipring.data.clear_geometry()
verts=mouth_ring_coords(); faces=[]; n=64; rings=4
for j in range(rings-1):
    for i in range(n):
        ni=(i+1)%n; faces.append((j*n+i,j*n+ni,(j+1)*n+ni,(j+1)*n+i))
lipring.data.from_pydata(verts,[],faces); lipring.data.update()
for p in lipring.data.polygons: p.use_smooth=True
upper=mesh_object('RYOKO_Teeth_Upper',*teeth_coords(True),[teeth])
lower=mesh_object('RYOKO_Teeth_Lower',*teeth_coords(False),[teeth])
tongue_obj=mesh_object('RYOKO_Tongue',tongue_coords(),tongue_faces(),[tongue])

mouth_objects=[cavity,lipring,upper,lower,tongue_obj]
for obj in mouth_objects:
    for key_name,prop in [('JawOpen','jaw_open'),('MouthSmile','smile'),('MouthFunnel','funnel'),('MouthWide','wide')]:
        kwargs={'jaw':0,'smile':0,'funnel':0,'wide':0}
        kwargs[{'JawOpen':'jaw','MouthSmile':'smile','MouthFunnel':'funnel','MouthWide':'wide'}[key_name]]=1
        if obj==cavity: coords=mouth_disk_coords(**kwargs)
        elif obj==lipring: coords=mouth_ring_coords(**kwargs)
        elif obj==upper: coords=teeth_coords(True,**kwargs)[0]
        elif obj==lower: coords=teeth_coords(False,**kwargs)[0]
        else: coords=tongue_coords(**kwargs)
        drive(obj,shape(obj,key_name,coords).name,prop)

# Deform the real head underneath the separate facial assembly.
head.shape_key_add(name='Basis')
inv=head.matrix_world.inverted()
jaw_coords=[]; smile_coords=[]
for v in head.data.vertices:
    w=head.matrix_world@v.co
    x,y,z=w
    # Keep the oral aperture clear; only the chin below the mouth drops.
    jaw_weight=max(0,min(1,(1.572-z)/.045))*max(0,1-(abs(x)/.075)**2)*max(0,min(1,(-y-.015)/.05))
    smile_weight=math.exp(-((z-MCZ)/.025)**2-((abs(x)-.026)/.025)**2)*max(0,min(1,(-y-.015)/.05))
    jaw_w=Vector((x,y+.0010*jaw_weight,z-.013*jaw_weight))
    smile_w=Vector((x+(1 if x>=0 else -1)*.0020*smile_weight,y,z+.0025*smile_weight))
    jaw_coords.append(inv@jaw_w); smile_coords.append(inv@smile_w)
drive(head,shape(head,'JawOpen',jaw_coords).name,'jaw_open')
drive(head,shape(head,'MouthSmile',smile_coords).name,'smile')
created.append(head)

# A short feasibility performance, intentionally separate from later production actions.
states=[
 (1,{}),(13,{'gaze_x':-1.0}),(25,{'blink_left':1.0,'blink_right':1.0}),
 (37,{'gaze_x':1.0,'gaze_y':.35}),(49,{'jaw_open':1.0}),
 (61,{'jaw_open':.65,'smile':1.0}),(73,{'funnel':1.0}),
 (85,{'wide':1.0,'gaze_y':.35,'blink_left':.20,'blink_right':.20}),(97,{})]
for frame,state in states:
    for name in properties:
        control[name]=state.get(name,0.0)
        control.keyframe_insert(data_path='["'+name+'"]',frame=frame,group='FACE_FEASIBILITY')
if control.animation_data and control.animation_data.action:
    control.animation_data.action.name='RYOKO_FACE_FEASIBILITY_PREVIEW'
scene.frame_start=1; scene.frame_end=97; scene.render.fps=24
scene.frame_set(1)
scene['RYOKO_PHASE']='04 early facial feasibility prototype'
scene['RYOKO_FACE_NOTE']='Separate surface-fitted anime eye/mouth assembly plus real head JawOpen and MouthSmile keys. Prototype only; final joined oral topology, complete ARKit set, and production UVs remain open.'
bpy.context.view_layer.update()
bpy.ops.wm.save_as_mainfile(filepath=str(DEST))
report={
 'source_blend':str(SOURCE),'destination_blend':str(DEST),'control_object':control.name,
 'controls':sorted(properties),'facial_objects':[o.name for o in created],
 'shape_keys':{o.name:[k.name for k in o.data.shape_keys.key_blocks] for o in created if o.type=='MESH' and o.data.shape_keys},
 'action':'RYOKO_FACE_FEASIBILITY_PREVIEW','frame_range':[1,97],
 'construction':'Surface-fitted separate anime eyes, eyelid rings, lashes, brows, mouth insert, teeth and tongue; real head jaw/smile keys. No source reference image modified.',
 'status':'Early feasibility prototype only; not complete ARKit, final oral topology, final UVs, VRM, or runtime certification.'}
REPORT.write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))

scene.render.engine='CYCLES'; scene.cycles.device='CPU'; scene.cycles.samples=24; scene.cycles.use_denoising=True
scene.render.resolution_x=800; scene.render.resolution_y=800; scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'; scene.render.image_settings.color_mode='RGB'
cam=scene.camera
cam.data.ortho_scale=.255; cam.data.clip_start=.01
# Static expression inspections must not be reset by the feasibility action.
preview_action=control.animation_data.action if control.animation_data else None
control.animation_data.action=None

def aim(loc,target):
    cam.location=loc; cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler()

def set_state(state):
    scene.frame_set(1)
    for name in properties: control[name]=state.get(name,0.0)
    control.update_tag(refresh={'OBJECT'})
    bpy.context.view_layer.update()

def render(name,state,loc=(0,-2.6,1.64),target=(0,0,1.625)):
    set_state(state); aim(loc,target)
    scene.render.filepath=str(OUT/(name+'.png')); bpy.ops.render.render(write_still=True)

render('prototype_neutral',{})
render('prototype_blink',{'blink_left':1.0,'blink_right':1.0})
render('prototype_gaze_left',{'gaze_x':-1.0})
render('prototype_jaw_open',{'jaw_open':1.0})
render('prototype_smile',{'smile':1.0})
render('prototype_smile_jaw',{'smile':1.0,'jaw_open':.65})
render('prototype_funnel',{'funnel':1.0})
render('prototype_wide_gaze',{'wide':1.0,'gaze_y':.35})
render('prototype_blink_side',{'blink_left':1.0,'blink_right':1.0},(2.6,0,1.64),(0,0,1.625))
render('prototype_jaw_side',{'jaw_open':1.0},(2.6,0,1.64),(0,0,1.625))
render('prototype_neutral_three_quarter',{},(1.85,-1.85,1.72),(0,0,1.625))
render('prototype_smile_jaw_three_quarter',{'smile':1.0,'jaw_open':.65},(1.85,-1.85,1.72),(0,0,1.625))
print('Phase 04 prototype and first inspection renders saved.')

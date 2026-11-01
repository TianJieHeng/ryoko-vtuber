import bpy, math, json
from pathlib import Path
from mathutils import Vector
ROOT=Path('/mnt/agents/output/app')
BLEND=ROOT/'assets/ryoko_blockout_v001.blend'
OUT=ROOT/'renders/blockout_final'
OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(BLEND))
scene=bpy.context.scene
root=bpy.data.objects.get('RYOKO_BLOCKOUT_ROOT')
if root is None: raise RuntimeError('Missing blockout root')
# Align generated forward +X to the locked authoring forward -Y.
root.rotation_euler.z=math.radians(-90)
# Idempotent final review lighting: broad fill without clipped facial values.
light=bpy.data.objects.get('REVIEW_FACE_FILL')
if light is None:
    light_data=bpy.data.lights.new('REVIEW_FACE_FILL','AREA')
    light=bpy.data.objects.new('REVIEW_FACE_FILL',light_data)
    scene.collection.objects.link(light)
light.data.energy=180
light.data.shape='DISK'
light.data.size=4.0
light.location=(0,-3.0,3.2)
light.rotation_euler=(Vector((0,0,1.15))-light.location).to_track_quat('-Z','Y').to_euler()
bpy.context.view_layer.update()
cam=scene.camera
cam_data=cam.data
scene.cycles.samples=32
scene.cycles.use_denoising=True
scene.render.resolution_x=800
scene.render.resolution_y=800
scene.render.resolution_percentage=100

def point(location,target,scale):
    cam.location=location
    cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler()
    cam_data.ortho_scale=scale
    cam_data.clip_start=0.01
    cam_data.clip_end=100

def render(name,folder=OUT):
    scene.render.filepath=str(folder/f'{name}.png')
    bpy.ops.render.render(write_still=True)

# Store corrected authoring source before final shot set.
bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))

# Matched neutral views.
t=(0,0,0.93)
point((0,-6,1.02),t,2.02); render('matched_front')
point((6,0,1.02),t,2.02); render('matched_left_side')
point((0,6,1.02),t,2.02); render('matched_back')
point((4.4,-4.4,1.35),t,2.02); render('matched_three_quarter')

# Full orbit after orientation correction.
for i in range(8):
    a=2*math.pi*i/8
    elev=math.radians(15)
    loc=(6*math.cos(a)*math.cos(elev),6*math.sin(a)*math.cos(elev),0.93+6*math.sin(elev))
    point(loc,t,2.18); render(f'orbit_{i:02d}_deg_{i*45:03d}')
point((0,0,7),(0,0,0),0.75); render('top')

# Head/hair close-ups: five required angles plus rear construction.
head=(0,0,1.665)
head_views={
'close_head_front':(0,-2.6,1.69),
'close_head_three_quarter_left':(1.85,-1.85,1.78),
'close_head_left':(2.6,0,1.69),
'close_head_three_quarter_right':(-1.85,-1.85,1.78),
'close_head_right':(-2.6,0,1.69),
'close_hair_back':(0,2.6,1.72),
}
for name,loc in head_views.items():
    point(loc,head,0.55); render(name)

# Hand construction close-ups.
point((0.25,-2.2,0.90),(0.175,-0.015,0.79),0.32); render('close_hand_character_left')
point((-0.25,-2.2,0.90),(-0.175,-0.015,0.79),0.32); render('close_hand_character_right')

print('Final corrected blockout shot set rendered.')

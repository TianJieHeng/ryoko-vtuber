import bpy, math
from pathlib import Path
from mathutils import Vector
ROOT=Path('/mnt/agents/output/app')
BLEND=ROOT/'assets/ryoko_mesh_uv_textured_v001.blend'
OUT=ROOT/'renders/mesh_uv_textured_v001'
OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(BLEND))
scene=bpy.context.scene
scene.render.engine='CYCLES'; scene.cycles.device='CPU'; scene.cycles.samples=32; scene.cycles.use_denoising=True
scene.render.resolution_x=800; scene.render.resolution_y=800; scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'; scene.render.image_settings.color_mode='RGB'
cam=scene.camera; data=cam.data

def point(location,target,scale):
    cam.location=location
    cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler()
    data.ortho_scale=scale; data.clip_start=.01; data.clip_end=100

def render(name):
    scene.render.filepath=str(OUT/f'{name}.png'); bpy.ops.render.render(write_still=True)

t=(0,0,.93)
point((0,-6,1.02),t,2.02); render('matched_front')
point((6,0,1.02),t,2.02); render('matched_left_side')
point((0,6,1.02),t,2.02); render('matched_back')
point((4.4,-4.4,1.35),t,2.02); render('matched_three_quarter')
for i in range(8):
    a=2*math.pi*i/8; elev=math.radians(15)
    loc=(6*math.cos(a)*math.cos(elev),6*math.sin(a)*math.cos(elev),.93+6*math.sin(elev))
    point(loc,t,2.18); render(f'orbit_{i:02d}_deg_{i*45:03d}')
point((0,0,7),(0,0,0),.75); render('top')
head=(0,0,1.665)
views={
'close_head_front':(0,-2.6,1.69),
'close_head_three_quarter_left':(1.85,-1.85,1.78),
'close_head_left':(2.6,0,1.69),
'close_head_three_quarter_right':(-1.85,-1.85,1.78),
'close_head_right':(-2.6,0,1.69),
'close_hair_back':(0,2.6,1.72),
}
for name,loc in views.items(): point(loc,head,.55); render(name)
point((.35,-2.2,.92),(.205,-.015,.85),.28); render('close_hand_character_left')
point((-.35,-2.2,.92),(-.205,-.015,.85),.28); render('close_hand_character_right')
print('Phase 3 material shot set rendered.')

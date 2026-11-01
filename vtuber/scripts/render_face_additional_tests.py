import bpy
from pathlib import Path
from mathutils import Vector
ROOT=Path('/mnt/agents/output/app'); OUT=ROOT/'renders/phase_04'
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'assets/ryoko_face_prototype_v001.blend'))
scene=bpy.context.scene; control=bpy.data.objects['RYOKO_FACE_CONTROLS']; control.animation_data.action=None
props=['blink_left','blink_right','gaze_x','gaze_y','jaw_open','smile','funnel','wide']
scene.render.engine='CYCLES'; scene.cycles.device='CPU'; scene.cycles.samples=24; scene.cycles.use_denoising=True
scene.render.resolution_x=800; scene.render.resolution_y=800; scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'; scene.render.image_settings.color_mode='RGB'
cam=scene.camera; cam.location=(0,-2.6,1.64); target=Vector((0,0,1.625)); cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler(); cam.data.ortho_scale=.255; cam.data.clip_start=.01
cases={
 'prototype_blink_left_only':{'blink_left':1.0},'prototype_blink_right_only':{'blink_right':1.0},
 'prototype_gaze_right':{'gaze_x':1.0},'prototype_gaze_up':{'gaze_y':1.0},'prototype_gaze_down':{'gaze_y':-1.0}}
for name,state in cases.items():
    scene.frame_set(1)
    for p in props: control[p]=state.get(p,0.0)
    control.update_tag(refresh={'OBJECT'}); bpy.context.view_layer.update()
    scene.render.filepath=str(OUT/(name+'.png')); bpy.ops.render.render(write_still=True)
print('Independent blink and gaze tests rendered.')

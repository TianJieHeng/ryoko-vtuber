import bpy, os
from pathlib import Path
from mathutils import Vector
ROOT=Path('/mnt/agents/output/app')
FRAMES=ROOT/'renders/phase_04/motion_frames'
FRAMES.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'assets/ryoko_face_prototype_v001.blend'))
scene=bpy.context.scene
scene.render.engine='CYCLES'; scene.cycles.device='CPU'; scene.cycles.samples=16; scene.cycles.use_denoising=True
scene.render.resolution_x=720; scene.render.resolution_y=720; scene.render.resolution_percentage=100
scene.render.fps=24; scene.frame_start=int(os.environ.get('START_FRAME','1')); scene.frame_end=int(os.environ.get('END_FRAME','97'))
scene.render.image_settings.file_format='PNG'; scene.render.image_settings.color_mode='RGB'
scene.render.film_transparent=False
cam=scene.camera; cam.location=(0,-2.6,1.64); target=Vector((0,0,1.625))
cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler(); cam.data.ortho_scale=.255; cam.data.clip_start=.01
scene.render.filepath=str(FRAMES/'frame_')
scene.frame_set(scene.frame_start)
bpy.ops.render.render(animation=True)
print(f'Rendered frames {scene.frame_start}-{scene.frame_end} at 24 fps.')

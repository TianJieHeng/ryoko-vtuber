#!/usr/bin/env python3
"""Register individually cut body parts, never an assembled fullbody/bust raster."""
import json, math
from pathlib import Path
from PIL import Image

BASE = Path(__file__).resolve().parents[1]
RIG = BASE.parent

def read(path):
    return json.loads(path.read_text())

old = read(BASE / 'registration.json')
upper = read(BASE / 'pieces_v2/upper/registration_fragment.json')
lower = read(BASE / 'pieces_v2/lower/registration_fragment.json')
layers = []
for fragment, z_offset in [(lower, -300), (upper, -200)]:
    for original in fragment['layers']:
        e = dict(original)
        if not e['file'].startswith('res://'):
            e['file'] = 'res://' + e['file']
        angle = math.radians(e.get('rotation_degrees', 0))
        if e.get('pivot_space') == 'scaled cropped pixels':
            px, py = e['pivot']
            tx, ty = e['target_pivot']
            e['position'] = [tx - math.cos(angle)*px + math.sin(angle)*py,
                             ty - math.sin(angle)*px - math.cos(angle)*py]
        e['z'] += z_offset
        image = Image.open(RIG / e['file'][6:])
        e['alpha_bounds'] = list(image.getbbox())
        layers.append(e)

joints = old['joints']
for joint in joints:
    if joint['id'].startswith('ankle_'):
        shoe = next(e for e in lower['layers'] if e['parent'] == joint['id'])
        joint['position'] = shoe['pivot']
    if joint['id'].startswith('wrist_'):
        hand = next(e for e in upper['layers'] if e['parent'] == joint['id'])
        joint['position'] = hand['target_pivot']
    if joint['id'].startswith('elbow_'):
        arm = next(e for e in upper['layers'] if e['parent'] == joint['id'])
        joint['position'] = arm['target_pivot']

manifest = {
    'version': 3, 'canvas': [1024,1536],
    'status': 'Unapproved separate-part registration and skeletal wiring review',
    'side_convention': 'Anatomical L is screen-right; anatomical R is screen-left.',
    'source_policy': 'Body garment/anatomy owners are individually cut from avatar_build_assets/body/layers and accessories/layers. No combined fullbody or bust raster is instantiated.',
    'joints': joints, 'frame_pivot': [512,650], 'layers': layers,
    'head_binding': {'parent':'head','position':[329,4],'scale':0.32,
                     'source_size':[1136,1384], 'remove_legacy':['FixedNeckTorso'],
                     'keep_objects':['existing live head and all approved face controls'],
                     'extra_parts':[
                         {'id':'earring_tip_R','file':'res://full_body/pieces_v2/head_audit/earring_tip_R.png','z':20},
                         {'id':'earring_tip_L','file':'res://full_body/pieces_v2/head_audit/earring_tip_L.png','z':20}
                     ]},
    'limitations': upper['limitations'] + lower['limitations'] + [
        'No action choreography. Body controls are manual, small calibration ranges.',
        'Native renderer capture unavailable in current environment; CPU neutral composites do not verify shader output.',
        'Head retains original expression objects; earrings remain baked in head backing except separated final tips.'
    ]
}
(BASE / 'registration.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(f'Registered {len(layers)} independent body parts.')

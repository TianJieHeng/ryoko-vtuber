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

# Visible jacket fronts exclude their construction facing strips. The blouse
# collar tabs are separate front owners, removed from the rear blouse pixels.
jacket = read(BASE / 'jacket_review/registration_candidate.json')
for replacement in jacket['layers']:
    e = dict(replacement)
    if not e['file'].startswith('res://'):
        e['file'] = 'res://' + e['file']
    if 'canvas_affine_abcdxy' in e and ('position' not in e or 'scale' not in e):
        a,b,c,d,x,y = e['canvas_affine_abcdxy']
        assert abs(b) < 1e-8 and abs(c) < 1e-8, 'Collar requires unsupported shear'
        e['position'], e['scale'] = [x,y], [a,d]
    image = Image.open(RIG / e['file'][6:])
    e['alpha_bounds'] = list(image.getbbox())
    indexes = [i for i, prior in enumerate(layers) if prior['id'] == e['id']]
    if indexes:
        layers[indexes[0]] = e
    else:
        layers.append(e)

elbow = read(BASE / 'elbow_review/registration_candidate.json')
for replacement in elbow['layers']:
    e = dict(replacement)
    if not e['file'].startswith('res://'):
        e['file'] = 'res://' + e['file']
    image = Image.open(RIG / e['file'][6:])
    e['alpha_bounds'] = list(image.getbbox())
    indexes = [i for i, prior in enumerate(layers) if prior['id'] == e['id']]
    if indexes:
        layers[indexes[0]] = e
    else:
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
for replacement in elbow.get('joint_replacements', []):
    joint = next(j for j in joints if j['id'] == replacement['id'])
    joint['position'] = replacement['position']

manifest = {
    'version': 5, 'canvas': [1024,1536],
    'status': 'Unapproved separate-part registration and skeletal wiring review',
    'side_convention': 'Anatomical L is screen-right; anatomical R is screen-left.',
    'source_policy': 'Body garment/anatomy owners are individually cut from avatar_build_assets/body/layers and accessories/layers. Jacket fronts exclude inner construction facings; collar tabs and fastener are separate owners. No combined fullbody or bust raster is instantiated.',
    'jacket_fit': {'method':jacket['method'], 'provenance':'jacket_review/registration_candidate.json'},
    'elbow_fit': {'provenance':'elbow_review/registration_candidate.json', 'method':'Register real painted sleeve folds at a single elbow; exclude open construction tube; fit continuous neutral upper and lower arm.'},
    'joints': joints, 'frame_pivot': [512,650], 'layers': layers,
    'head_binding': {'parent':'head','position':[329,4],'scale':0.32,
                     'source_size':[1136,1384], 'remove_legacy':['FixedNeckTorso'],
                     'keep_objects':['existing live head and all approved face controls'],
                     'extra_parts':[
                         {'id':'earring_tip_R','file':'res://full_body/pieces_v2/head_audit/earring_tip_R.png','z':20},
                         {'id':'earring_tip_L','file':'res://full_body/pieces_v2/head_audit/earring_tip_L.png','z':20}
                     ]},
    'limitations': [line for line in upper['limitations'] if 'rowwise' not in line] + lower['limitations'] + [
        'Jacket exterior panels, front collar tabs and fastener are individually owned. Landmark fit and silhouette remain subject to user review.',
        'No action choreography. Body controls are manual, small calibration ranges.',
        'Native renderer capture unavailable in current environment; CPU neutral composites do not verify shader output.',
        'Head retains original expression objects; earrings remain baked in head backing except separated final tips.'
    ]
}
(BASE / 'registration.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(f'Registered {len(layers)} independent body parts.')

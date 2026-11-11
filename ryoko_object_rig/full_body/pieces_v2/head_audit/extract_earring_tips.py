#!/usr/bin/env python3
"""Retain only exact approved earring-tip pixels. No resampling or painting."""
from pathlib import Path
import hashlib
import json
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
SOURCE = ROOT / 'rig_assets/object_face/fixed_neck_torso.png'
NEUTRAL = OUT / 'neutral_head_reference.png'
# Bounds are exclusive at right/bottom. Anatomical L is screen-right.
# Visually audited against alpha-composited crops: only dangling gold tips.
MASKS = {
    'earring_tip_L': (704, 720, 731, 736),
    'earring_tip_R': (397, 720, 422, 736),
}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

# Diagnostic neutral head only: no torso pixels are retained.
head = Image.open(ROOT / 'canonical_sources/approved_neutral.png').convert('RGBA')
a = np.array(head.getchannel('A'))
a[720:] = 0
head.putalpha(Image.fromarray(a))
hair_manifest = json.loads((ROOT / 'rig_assets/object_face/manifest.json').read_text())
for key, spec in sorted(hair_manifest['objects'].items(), key=lambda item: item[1]['z']):
    if key.startswith('hair_') and 'hidden' not in key:
        part = Image.open(ROOT / 'rig_assets/object_face' / spec['file']).convert('RGBA')
        head.alpha_composite(part, tuple(spec['xy']))
head.save(NEUTRAL)
source = np.array(Image.open(SOURCE).convert('RGBA'))
assert source.shape == (1384, 1136, 4)
entries = []
combined = Image.new('RGBA', (1136, 1384))
for name, box in MASKS.items():
    x0, y0, x1, y1 = box
    keep = np.zeros(source.shape[:2], dtype=bool)
    keep[y0:y1, x0:x1] = source[y0:y1, x0:x1, 3] > 0
    pixels = np.zeros_like(source)
    pixels[keep] = source[keep]
    assert np.array_equal(pixels[keep], source[keep])
    assert not pixels[~keep].any()
    image = Image.fromarray(pixels)
    output = OUT / (name + '.png')
    image.save(output)
    combined.alpha_composite(image)
    entries.append({
        'id': name,
        'file': str(output.relative_to(ROOT)),
        'anatomical_side': name[-1],
        'screen_side': 'right' if name.endswith('_L') else 'left',
        'mask_bounds_xyxy_exclusive': list(box),
        'alpha_bounds_xyxy_exclusive': list(image.getchannel('A').getbbox()),
        'nonzero_alpha_pixels': int(keep.sum()),
        'source_pixel_rgba_exact': True,
        'canvas': [1136, 1384],
        'position_under_existing_head': [0, 0],
        'scale_under_existing_head': [1, 1],
        'z_under_existing_head': 20,
        'sha256': sha(output),
    })
# Tips sit below original live head owners, matching original body/head order.
combined.alpha_composite(Image.open(NEUTRAL).convert('RGBA'))
proof = OUT / 'neutral_head_complete.png'
combined.save(proof)
manifest = {
    'source': str(SOURCE.relative_to(ROOT)),
    'source_sha256': sha(SOURCE),
    'purpose': 'Only earring tips removed when FixedNeckTorso is detached. No neck, skin, collar or clothing.',
    'binding': 'Add Sprite2D children under existing live RigidHead, centered=false, position=(0,0), scale=(1,1), z_index=20, relative z=true. Existing head binding scale .32 is inherited; do not apply .32 twice. Tips are disjoint from backing alpha and lie below hair z60–80.',
    'layers': entries,
    'neutral_proof': {'file': str(proof.relative_to(ROOT)), 'sha256': sha(proof), 'source': str(NEUTRAL.relative_to(ROOT)), 'source_sha256': sha(NEUTRAL), 'scope': 'CPU neutral source composition; not native facial rendering. Tips composited below neutral head.'},
}
(OUT / 'earring_tip_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps(manifest, indent=2))

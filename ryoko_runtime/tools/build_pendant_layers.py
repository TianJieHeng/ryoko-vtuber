"""Derive a restrained pendant hinge from the approved bust, never atlas art.

The chain and upper bail stay fixed. Skin behind the diamond is a deterministic
local harmonic estimate, not recovered artwork. All original PNGs are preserved.
"""
from pathlib import Path
import hashlib
import json
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'rig_assets'
REVIEW = ROOT.parent / 'review'
VALID = ROOT.parent / 'output'
for directory in (OUT, REVIEW, VALID):
    directory.mkdir(exist_ok=True)

generated = {'pendant_cutout.png', 'pendant_cleared_base.png'}
originals = [p for p in ROOT.rglob('*.png') if p.name not in generated]
before = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in originals}
source = ROOT / 'artwork/bust_base.png'
src = np.array(Image.open(source).convert('RGBA'))
h, w = src.shape[:2]
assert (w, h) == (1136, 1384)
pivot = (563.5, 933.0)

# Preserve all chain/bail pixels through y932. The diamond, ink and cast shadow
# fit inside this source-registered silhouette; no collar or neck edge is cut.
polygon = [(558,933), (569,933), (577,942), (580,947), (578,952),
           (567,963), (564,965), (560,963), (550,954), (547,948), (549,942)]
mask_image = Image.new('L', (w, h), 0)
ImageDraw.Draw(mask_image).polygon(polygon, fill=255)
mask = np.array(mask_image) > 0
assert not mask[:933].any()
assert np.all(src[mask, 3] == 255), 'Expected an opaque skin region'

# Interpolate in a small padded local box, with fixed surrounding source skin.
x0, y0, x1, y1 = 541, 927, 587, 972
local = mask[y0:y1, x0:x1]
fill = src[y0:y1, x0:x1, :3].astype(np.float64)
for row in range(local.shape[0]):
    xs = np.flatnonzero(local[row])
    if not len(xs):
        continue
    left, right = xs[0], xs[-1]
    a = fill[row, left-2:left].mean(axis=0)
    b = fill[row, right+1:right+3].mean(axis=0)
    for x in xs:
        t = (x-left+1) / (right-left+2)
        fill[row, x] = a*(1-t) + b*t
for _ in range(2400):
    padded = np.pad(fill, ((1,1), (1,1), (0,0)), mode='edge')
    mean = (padded[:-2,1:-1] + padded[2:,1:-1] + padded[1:-1,:-2] + padded[1:-1,2:]) / 4
    fill[local] = mean[local]

cleared = src.copy()
region = cleared[y0:y1, x0:x1, :3]
region[local] = np.clip(np.rint(fill[local]), 0, 255).astype(np.uint8)
cutout = np.zeros_like(src)
cutout[mask] = src[mask]
Image.fromarray(cleared).save(OUT / 'pendant_cleared_base.png')
Image.fromarray(cutout).save(OUT / 'pendant_cutout.png')
ys, xs = np.nonzero(mask)
rect = [int(xs.min()), int(ys.min()), int(xs.max()-xs.min()+1), int(ys.max()-ys.min()+1)]
manifest = {
    'version': 1,
    'canvas': [w, h],
    'pivot': list(pivot),
    'source_rect': rect,
    'cutout': 'pendant_cutout.png',
    'cleared_base': 'pendant_cleared_base.png',
    'source': 'artwork/bust_base.png',
    'source_sha256': before['artwork/bust_base.png'],
    'fixed_chain_max_y': 932,
    'source_polygon': polygon,
    'coordinate_system': 'Source pixels, x right, y down; pivot is the original lower bail attachment.',
    'limits': [
        'Only the diamond and its small source shadow move; the chain and upper bail stay fixed.',
        'Hidden skin is local harmonic interpolation, not recovered original artwork.',
        'The cutout retains existing torso, chest and breath mesh deformation; it is not perfectly rigid in screen space.',
        'Runtime uses the exact original base at zero relative angle or when disabled.'
    ],
}
(OUT / 'pendant_layers.json').write_text(json.dumps(manifest, indent=2) + '\n')

restored = np.array(Image.alpha_composite(Image.fromarray(cleared), Image.fromarray(cutout)))
assert np.array_equal(src, restored), 'Opaque source restoration changed pixels'
assert np.array_equal(cleared[~mask], src[~mask]), 'Pixels outside mask changed'
after = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in originals}
assert before == after, 'Inherited source artwork changed'
assert len(before) == 629, f'Expected 629 inherited PNGs, got {len(before)}'
report = {
    'inherited_png_count': len(before), 'inherited_pngs_unchanged': before == after,
    'source_sha256': before['artwork/bust_base.png'],
    'source_rect': rect, 'pivot': list(pivot), 'mask_pixels': int(mask.sum()),
    'fixed_chain_and_bail_unchanged': bool(np.array_equal(src[:933], cleared[:933])),
    'outside_mask_unchanged': bool(np.array_equal(src[~mask], cleared[~mask])),
    'zero_angle_rgba_restoration_exact': bool(np.array_equal(src, restored)),
    'limitations': manifest['limits'],
}
(VALID / 'pendant_asset_validation.json').write_text(json.dumps(report, indent=2) + '\n')

# Derivative inspection only. Actual acceptance uses separate Godot captures.
crop = (520, 905, 607, 984)
variants = [('Source', Image.fromarray(src)), ('Estimated skin', Image.fromarray(cleared)),
            ('Restored', Image.fromarray(restored))]
for angle in (-10, 10):
    # Match the runtime's bilinear sampling; bicubic alpha overshoot would add
    # artificial bright fringes that are not present in the Godot cutout.
    moved = Image.fromarray(cutout).rotate(angle, Image.Resampling.BILINEAR, center=pivot)
    variants.append((f'{angle:+} degrees', Image.alpha_composite(Image.fromarray(cleared), moved)))
scale = 3
cw, ch = crop[2]-crop[0], crop[3]-crop[1]
sheet = Image.new('RGB', (len(variants)*cw*scale, ch*scale+24), (35,36,38))
draw = ImageDraw.Draw(sheet)
for i, (label, im) in enumerate(variants):
    draw.text((i*cw*scale+4, 5), label, fill='white')
    sheet.paste(im.crop(crop).convert('RGB').resize((cw*scale,ch*scale)), (i*cw*scale,24))
sheet.save(REVIEW / 'pendant_source_derivatives.jpg', quality=92)
print(json.dumps(report, indent=2))

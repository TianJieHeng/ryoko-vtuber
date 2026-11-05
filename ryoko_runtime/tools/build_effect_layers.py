"""Register existing transparent source effects; no repainting or expression generation."""
from pathlib import Path
import argparse, hashlib, json, shutil
from PIL import Image

LAYERS = {
    'blush_R': ('RYO_FX_blush_character_R.png', [432, 530], [110, 60]),
    'blush_L': ('RYO_FX_blush_character_L.png', [590, 530], [110, 60]),
    'tear_R': ('RYO_FX_tear_character_R.png', [468, 514], [26, 134]),
    'tear_L': ('RYO_FX_tear_character_L.png', [638, 514], [26, 134]),
    'sweat': ('RYO_FX_sweatdrop.png', [695, 397], [32, 66]),
    'anger': ('RYO_FX_anger_mark.png', [663, 340], [48, 48]),
    'sparkle': ('RYO_FX_sparkle_cluster.png', [735, 335], [70, 80]),
}

def build(source_assets, output):
    output.mkdir(parents=True, exist_ok=True)
    effects = {}
    for key, (filename, position, size) in LAYERS.items():
        source = source_assets / 'effects' / 'layers' / filename
        with Image.open(source) as image:
            assert image.mode == 'RGBA', source
            bbox = image.getchannel('A').getbbox()
            assert bbox is not None, source
            rect = [bbox[0], bbox[1], bbox[2]-bbox[0], bbox[3]-bbox[1]]
        copied = output / filename
        shutil.copyfile(source, copied)
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        assert hashlib.sha256(copied.read_bytes()).hexdigest() == digest
        effects[key] = {'file': filename, 'source_rect': rect, 'position': position,
                        'size': size, 'source_sha256': digest,
                        'source': 'avatar_build_assets/effects/layers/' + filename}
    manifest = {'version': 1, 'coordinate_space': [1136, 1384],
                'side_convention': 'L is character-left/viewer-right; R is character-right/viewer-left.',
                'scope': 'Optional overlays from original transparent source art, separate from authored expression effects.',
                'registration': 'Source alpha bounding boxes are placed and scaled to the existing bust. PNG bytes remain unchanged.',
                'effects': effects}
    (output/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    return manifest

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-assets', type=Path, default=Path(__file__).resolve().parents[2]/'avatar_build_assets')
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parents[1]/'rig_assets'/'effects')
    args = parser.parse_args()
    manifest = build(args.source_assets, args.output)
    print('Registered', len(manifest['effects']), 'existing transparent source layers; source PNGs copied byte-identically.')

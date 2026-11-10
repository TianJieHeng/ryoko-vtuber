"""Independently decode native output and check pinned source preservation."""
from pathlib import Path
import hashlib
import json
from PIL import Image

ROOT = Path(__file__).resolve().parent
h = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
expected = json.loads((ROOT / 'expected_checkpoints.json').read_text())
result = json.loads((ROOT / 'RESULT.json').read_text())
records = []
for profile in expected:
    for checkpoint in profile['checkpoints']:
        for i, (view, size) in enumerate((('full', (568, 800)), ('detail', (400, 360)))):
            path = ROOT / 'captures' / profile['id'] / f"{checkpoint['frame']:04d}_{view}.png"
            with Image.open(path) as image:
                rgba = image.convert('RGBA')
                actual_hash = hashlib.sha256(rgba.tobytes()).hexdigest()
                actual_size = list(image.size)
            records.append({'path': str(path.relative_to(ROOT)), 'size': actual_size,
                            'sha256_rgba': actual_hash, 'expected': checkpoint['hashes'][i],
                            'pass': actual_hash == checkpoint['hashes'][i] and actual_size == list(size)})
actual_count = len(list((ROOT / 'captures').rglob('*.png')))
expected_count = len(records)
checks = {'native_harness_pass': result['status'] == 'PASS',
          'native_comparisons_exact': result['image_comparisons_run'] == expected_count == result['pixel_matches'],
          'native_checkpoint_count_exact': result['captured_checkpoints'] * 2 == expected_count,
          'file_count_exact': actual_count == expected_count,
          'all_png_hashes_and_dimensions_exact': all(record['pass'] for record in records)}
verification = {'status': 'PASS' if all(checks.values()) else 'FAIL', 'checks': expected_count,
                'summary_checks': checks, 'actual_png_count': actual_count, 'records': records}
(ROOT / 'independent_png_verification.json').write_text(json.dumps(verification, indent=2) + '\n')
before = json.loads((ROOT / 'native_preflight_baseline.json').read_text())
source = Path(before['source'])
after = {str(p.relative_to(source)): h(p) for p in source.rglob('*') if p.is_file()
         and not any(part in p.relative_to(source).parts for part in ('.git', '.godot', '__pycache__'))}
changes = [{'path': name, 'before': before['files'].get(name), 'after': after.get(name)}
           for name in sorted(set(before['files']) | set(after)) if before['files'].get(name) != after.get(name)]
receipt = json.loads((ROOT / 'source_copy_receipt.json').read_text())
copy_changes = [name for name, digest in receipt['files'].items()
                if not (ROOT / 'native_launcher' / name).is_file() or h(ROOT / 'native_launcher' / name) != digest]
preservation = {'status': 'PASS' if not changes and not copy_changes else 'FAIL',
                'source_files_before': len(before['files']), 'source_files_after': len(after),
                'production_differences': changes, 'copied_files': len(receipt['files']),
                'copied_source_differences': copy_changes,
                'source_runtime_sha256': h(source / 'expression_rig.gd')}
(ROOT / 'source_preservation.json').write_text(json.dumps(preservation, indent=2) + '\n')
print(json.dumps({'independent_png': {k:v for k,v in verification.items() if k != 'records'},
                  'source_preservation': preservation}, indent=2))
raise SystemExit(0 if verification['status'] == preservation['status'] == 'PASS' else 1)

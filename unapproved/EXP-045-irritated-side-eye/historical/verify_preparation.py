"""Read-only source checks and independent numerical timeline comparison."""
import hashlib
import json
import math
import re
from pathlib import Path

W = Path(__file__).resolve().parent
h = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
load = lambda p: json.loads(p.read_text())
write = lambda p, d: p.write_text(json.dumps(d, indent=2, allow_nan=False) + '\n')
f = load(W / 'BASELINE_FREEZE.json')
profile = load(W / 'EXP-045.json')
static = load(W / 'state_checks.json')
motion = load(W / 'motion_state_checks.json')
assert static['status'] == motion['status'] == 'PASS'
assert static['failures'] == motion['failures'] == []
assert static['visual_capture'] is motion['visual_capture'] is False
assert motion['display'] == 'headless'
assert motion['profile_sha256'] == h(W / 'EXP-045.json')
assert static['plan_sha256'] == h(W / 'plan.json')
assert static['baseline_freeze_sha256'] == motion['baseline_freeze_sha256'] == h(W / 'BASELINE_FREEZE.json')
expected_files = f['source_files_sha256'] | f['extra_manifests_sha256']
for root in [Path(f['source_rig']), W / 'rig']:
    for name, digest in expected_files.items():
        assert h(root / name) == digest, str(root / name)
for n,digest in f['published41_runtime_artwork_parity']['files_sha256'].items():
    assert h(Path(f['published41_runtime_artwork_parity']['path'])/n) == digest, n
assert len(f['source_files_sha256']) == 999
assert sum(n.endswith('.png') for n in f['source_files_sha256']) == 184
assert h(Path(f['source_sheet'])) == f['source_sheet_sha256']
assert h(Path(f['source_catalogue'])) == f['catalogue_sha256']
reference = load(W / 'SOURCE_REFERENCE.json')
root_ref = Path(f['source_catalogue']).parent.parent
for name, digest in reference['panel_hashes'].items():
    assert h(root_ref / name) == digest, name
assert reference['pixels_inspected'] is True
plan = load(W / 'plan.json')
assert len(plan) == 8 and len(profile['keyframes']) == 11
assert profile['duration'] == 4.0
for root in [Path(f['source_rig']), W / 'rig', W / 'native_launcher']:
    registry = load(root / 'expressions/registry.json')
    assert len(registry['entries']) == 36
    assert 'EXP-045' not in [r['id'] for r in registry['entries']]

# Check the unique launcher is a separate copy, with one explicit pinned override.
for name, digest in expected_files.items():
    if name != 'project.godot':
        assert h(W / 'native_launcher' / name) == digest, name
base_config = (W / 'rig/project.godot').read_text()
expected_config = re.sub(r'run/main_scene=.*', 'run/main_scene="res://launcher.tscn"', base_config)
expected_config = re.sub(r'config/name=.*', 'config/name="Ryoko EXP045 Irritated Side-eye PREVIEW ONLY"', expected_config)
assert (W / 'native_launcher/project.godot').read_text() == expected_config
for name in ['static', 'motion', 'launcher']:
    log = (W / f'launcher_{name}_parse.log').read_text()
    assert 'SCRIPT ERROR' not in log and 'Parse Error' not in log and 'ERROR:' not in log
for name, source in [('static', 'check_and_capture.gd'), ('motion', 'render_motion.gd')]:
    generated = (W / source).read_text().replace('extends SceneTree', 'extends Node\nvar root\nvar exit_code=0')
    generated = generated.replace('var w=get_script().resource_path.get_base_dir()', 'var w='+json.dumps(str(W)))
    generated = generated.replace('func _initialize():\n visual="--capture" in OS.get_cmdline_user_args()\n call_deferred("run")', 'func _ready():\n root=get_tree().root\n visual=true\n call_deferred("run")')
    generated = generated.replace('await process_frame', 'await get_tree().process_frame').replace('quit(', 'finish(')
    generated += '\nfunc finish(code):\n exit_code=code\n if is_instance_valid(rig):rig.queue_free()\n queue_free()\n'
    assert (W / 'native_launcher' / (name+'.gd')).read_text() == generated
for name in ['check_and_capture.gd', 'render_motion.gd', 'native_launcher/static.gd', 'native_launcher/motion.gd']:
    text = (W / name).read_text()
    assert 'Vector2i(568,800)' in text and 'Vector2i(400,360)' in text
    assert 'if im.get_size()!=expected:return' in text

def sample(d, t, channels):
    keys = d['keyframes']
    for a, b in zip(keys, keys[1:]):
        if a['time'] <= t <= b['time']:
            break
    u = max(0, min(1, (t - a['time']) / (b['time'] - a['time'])))
    q = u*u*(3-2*u)
    restart = 1.0
    if t < .3:
        v = t / .3
        restart = v*v*(3-2*v)
    return {k: (a['values'].get(k, 0) + (b['values'].get(k, 0)-a['values'].get(k, 0))*q)*restart for k in channels}

records = motion['records']
assert len(records) == 121
channels = set(records[0]['pose'])
errors = []
for i, row in enumerate(records):
    assert row['frame'] == i and abs(row['time'] - i/30) < 1e-12
    assert row['hashes'] == []  # No invented native evidence.
    expected = sample(profile, i/30, channels)
    opening, purse = expected["mouth_open"], expected["mouth_purse"]
    gap = max(0, opening*.55*54-1.5*purse*min(opening*4, 1))
    assert abs(row["central_lip_gap_native_px"]-gap) < 1e-6
    for k, value in row['pose'].items():
        assert math.isfinite(value)
        errors.append(abs(expected[k] - value))
assert max(errors) < 1e-6, max(errors)
assert motion['lifecycle_assertions'] == 36 and len(motion['lifecycle_interruption_times']) == 9

comparison = []
source = Path(f['source_rig'])
registry = load(source / 'expressions/registry.json')
earlier = [source / r['path'].removeprefix('res://') for r in registry['entries']]
earlier += [W.parent / 'mental_arithmetic_work/EXP-129.json',
            W.parent / 'controlled_anger_work/EXP-041.json',
            W.parent / 'broad_surprise_work/EXP-061.json',
            W.parent / 'puzzled_work/EXP-123.json', W.parent / 'open_sobbing_work/EXP-023.json', W.parent / 'mild_disgust_work/EXP-081.json', W.parent / 'sleepy_work/EXP-161.json']
active = lambda d: sorted({k for frame in d['keyframes'] for k, v in frame['values'].items() if v != 0})
candidate_active = active(profile)
for path in earlier:
    other = load(path)
    maximum = 0.0
    sums = 0.0
    count = 0
    for i in range(121):
        a = sample(profile, 4*i/120, channels)
        b = sample(other, other['duration']*i/120, channels)
        for k in channels:
            diff = abs(a[k] - b[k])
            maximum = max(maximum, diff)
            sums += diff*diff
            count += 1
    assert maximum > .01, ('duplicate trajectory', path)
    comparison.append(dict(id=other['id'], title=other['title'], path=str(path.resolve()),
        sha256=h(path), active_controls=active(other), same_active_control_set=active(other)==candidate_active,
        max_control_difference_at_normalized_time=maximum, rms_control_difference=(sums/count)**.5))
unique_controls = all(not r['same_active_control_set'] for r in comparison)
write(W / 'DISTINCTNESS_CHECK.json', dict(status='PASS', compared_profiles=len(comparison),
    candidate_active_controls=candidate_active, unique_active_control_set=unique_controls,
    interpretation='Deliberate screen-right glance with unequal opposed brows and narrowed unequal lids; gaze begins only after lid support and centers before lids release. No mouth control is authored because independent downturned corner is unsupported. Compare with EXP-042 frontal glare, EXP-081 mouth-led disgust and EXP-144 startled embarrassed glance-away.',
    limitations='Normalized-time numeric and control-set differences are not proof of perceptual distinction. Native motion comparison is pending.', comparisons=comparison))
launcher = dict(status='PASS', unchanged_pinned_launcher_files=998,
    only_pinned_launcher_override='project.godot: unique name and launcher main scene',
    external_manifests_preserved=True, scripts_parse=['static.gd', 'motion.gd', 'launcher.gd'],
    native_rendered=False, capture_outputs_exist=(W/'capture').exists() or (W/'motion').exists(), candidate_approval='UNAPPROVED')
write(W / 'launcher_preparation_verification.json', launcher)
out = dict(status='PASS', source_files=999, source_png_files=184, approved_profiles=36,
    production_and_copied_pinned_files_unchanged=True, reference_art_and_catalogue_unchanged=True,
    checks={'state_checks.json': static['checks'], 'motion_state_checks.json': motion['checks']},
    independent_timeline_samples=121, max_smoothstep_error=max(errors),
    lifecycle_interruption_points=9, lifecycle_assertions=36, compared_profiles=len(comparison),
    native_capture='PENDING. Separate copied GUI launcher prepared; no native renderer, UI, display server or socket workaround was invoked.',
    candidate_approval='UNAPPROVED', publication='No registry changes or publication',
    extra_manifests=f['extra_manifests_sha256'])
write(W / 'preparation_verification.json', out)
print(json.dumps(out, indent=2))

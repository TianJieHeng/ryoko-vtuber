# EXP-091 Overly Sweet Taste: new unapproved reconstruction

This is **NEW 20261111 r1**, not restoration of the missing old v2 candidate. The recovered, pinned approved39 rig is copied unchanged into `rig/`; no production profile, registry, runtime, shader or artwork was edited. The exact approved EXP-096 review profile is copied solely as a comparator. Its historical approved36 base is not conflated with current approved39.

## Source interpretation

The actual recovered 1159 × 1358 nine-panel sheet was visually inspected before authoring. The peak is a strained sweet-overload reaction: closed curved lashes, strong cheek blush, raised-inner-brow strain and a small sealed smile-pucker. KP2 briefly parts the mouth. KP7 reopens the eyes with residual tension. `SOURCE_MAP.json` records each panel and every approximation.

The candidate uses existing rigid brows, smile-eye joints, lip pressure, symmetric purse, shared corner lift and separate blush FX only. No cheek compression, new pucker anatomy, kiss part, independent width, gaze, hair, speech or body acting is introduced. At peak the analytical mouth span is 49.16 source pixels, reduced from 71; corners are 0.84 source pixels higher than the center. This does **not** prove the resulting mouth looks tiny or source-faithful. The rig cannot reproduce source-specific brow curvature, cheek volume or lip protrusion.

Four-second interpretation, not recovered animation:

- 0–0.20: exact neutral lead-in, KP1.
- 0.55: small intake opening (.07), KP2.
- 0.90: sealed mouth, blush and sweet recognition, KP3.
- 1.25: narrowed eyes and increasing strain, KP4.
- 1.65–2.25: curved closed smile-eyes, pressed purse and strong blush, KP5–6.
- 2.75: reopened eyes with residual tension, KP7.
- 3.30: near-neutral settling, KP8.
- 3.75–4.00: exact neutral hold, KP9.

## What is verified and what is not

`numeric_model.py` is a read-only standard-library analytical model of the existing runtime equations. It checks 121 frame positions, 130 dense segment samples, 270 restart/release samples from nine interruption times, control bounds, neutral bookends, baseline hashes and sorted deterministic numeric comparisons against all 39 registered profiles plus EXP-096. Lifecycle scope is deliberately limited to this profile's channels; it does not prove all cross-expression bridges or actual native behavior.

`test_candidate.py` exercises invalid data, timing, lifecycle continuity, reset, manual takeover, source preservation, deterministic accumulation and fail-closed evidence gates. The modeled source-space geometry is a prediction, not an observed transform, native frame or perceptual finding.

The comparator gate stays **PENDING**: compare against EXP-197 kiss, EXP-160 shy laughter, EXP-090 queasy and EXP-096 headache at native detail and normal speed. A generic bashful smile is a source-fit failure even when every numerical difference passes.

## Frozen inputs and repeatability

`INPUT_FREEZE.json` and `INPUT_FREEZE.sha256` are a new author handoff identity. They pin all copied inputs, profile, mapping, preparation scripts and tests. They are created once with exclusive writes. Validation never rewrites them or repins changed inputs. Any author change after freeze requires a separately named revision and a new explicit freeze, preserving this one.

`STATIC_VALIDATION.json`, `TEST_RESULTS.log` and `MULTISEED_CHECK.json` are new static/model evidence only. Run read-only checks with bytecode creation disabled:

    PYTHONDONTWRITEBYTECODE=1 python numeric_model.py
    PYTHONDONTWRITEBYTECODE=1 python -m unittest test_candidate -v
    PYTHONDONTWRITEBYTECODE=1 python encode_preflight.py

The last command must exit 2 while actual native captures are absent. It never launches an encoder or renderer. Different PYTHONHASHSEED runs must produce byte-identical validator output and leave every input hash unchanged.

## Guarded future capture preparation

`scaffold/` contains exact historical EXP-096 source scaffolds for provenance, not usable EXP-091 receipts. New `native_capture.gd` adapts the original capture geometry and in-memory registration approach, adding EXP-091 control checks. It is explicitly disabled by a frozen constant and has **not been parsed or run** in Godot. No launch command is provided while the native blocker is active. The guard inside a script is not permission to start Godot, which initializes its display before running scripts.

The prepared protocol calls for nine static anchors in two views and 121 endpoint-inclusive frames at 30 Hz, using actual 568 × 800 bust and 400 × 360 detail viewports, ordered RGBA hashes and native lifecycle checks. It must refuse existing output folders. `encode_preflight.py` would validate fresh receipts, all 260 PNGs, hashes, dimensions, chronology, trajectories and exact neutral pixels before emitting a non-overwriting encoding command. It never executes that command. Intended review format: 968 × 800, 121 frames, 30 fps, roughly 4.033 seconds. Decoding and normal-speed visual review would still be required after a future authorized encode.

**Native runtime, parse checks, captures, MP4, visual source fit, independent perceptual review, user approval and publication remain pending.** Prior native launch was denied twice. This task did not retry it, launch a headless alternative, use a remote machine, synthesize a substitute video, or run CI. Nothing was pushed. All copied approved39 and Headache bytes remain unchanged.

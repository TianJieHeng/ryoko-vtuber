# Approved necklace-pendant validation

Based on approved main `bd4888a906a9d15950f3913833e7b08119367470`. The user approved the supplied actual Godot runtime review on 2026-11-06. Automated checks, actual Godot captures and decoded-frame inspection were completed on 2026-11-06. Native-speed playback was unavailable.

## Implementation scope

- Original green pendant only, pivot `(563.5,933)`, source region `(547,933,34,33)` on the existing `1136 × 1384` canvas.
- Fixed chain and upper bail through y932. No replacement necklace, new expression or full-body work.
- Original facial viewport and existing mesh. No new sampler, viewport, shader edit or mesh edit.
- Two derived full-canvas PNGs plus metadata. Zero/off restores the original texture resource, not a reconstructed substitute.
- Source rotation still passes through the existing varying chest/breath mesh deformation and therefore is not perfectly rigid in screen space.

## Focused automated checks

`test_pendant.gd`: **22,076 checks passed, zero failures** on Godot 4.6.3 headless.

Coverage includes:

- Stationary and returned-to-rest exact zero; deterministic repeated inputs; short damped settling; 6° transient and 10° total bounds.
- NaN/positive and negative infinity, zero/negative/tiny/large frame deltas, finite extreme anchors/frame angles, bounded history and recovery from corrupted nonfinite state.
- Fixed source pivot, region registration, exact original-resource bypass, full-canvas textures, unchanged local scale and intended facial-layer ordering.
- Attachment calculations matching the existing mesh triangle, with torso/chest/bounce/controlled breath included and independent head/periodic baseline breathing excluded.
- Immediate off/reset/cancel texture refresh, reset/timeout/cancel preference retention, pause freezing all pendant history, and direct paused off/on behavior.
- Strict direct/clip/UDP booleans, direct atomic rejection before reset or other changes, active and paused invalid late clip replacement, stale sequence rejection and real localhost UDP acceptance/rejection/takeover/timeout.
- All 93 inherited expression IDs plus neutral, both-eye blink, all existing mouth states, authored effects, and all seven independent optional effects while the pendant is separated.

All **26 GDScript suites passed**: 205,117 explicitly counted checks plus the inherited bounce suite's 304 assertions, for **205,421 checks/assertions in total**. That includes 25 inherited suites unchanged and the new pendant suite. Every process exited zero with no script/runtime errors. The inherited loose-hair geometry audit also passed.

Recorded suite counts:

- `test_audio_mouth.gd`: 376 passed.
- `test_body_controls.gd`: 534 passed.
- `test_bounce.gd`: 304 assertions (300 bounded-motion frames plus 4 final checks) passed.
- `test_breath.gd`: 15974 passed.
- `test_brows.gd`: 7752 passed.
- `test_chest_secondary.gd`: 298 passed.
- `test_clip_channels.gd`: 348 passed.
- `test_clips.gd`: 45 passed.
- `test_controls.gd`: 89 passed.
- `test_earrings.gd`: 2065 passed.
- `test_expression_cues.gd`: 3951 passed.
- `test_expression_gaze.gd`: 7135 passed.
- `test_expressions.gd`: 58504 passed.
- `test_eyelids.gd`: 120 passed.
- `test_gaze.gd`: 42103 passed.
- `test_gestures.gd`: 256 passed.
- `test_hair_secondary.gd`: 289 passed.
- `test_integrated_bust.gd`: 11 passed.
- `test_live_input.gd`: 40 passed.
- `test_look_at.gd`: 1107 passed.
- `test_loose_hair.gd`: 22731 passed.
- `test_motion_rig.gd`: 3204 passed.
- `test_optional_effects.gd`: 15118 passed.
- `test_ornament.gd`: 826 passed.
- `test_pendant.gd`: 22076 passed.
- `test_pose_store.gd`: 165 passed.

The test run used writable local HOME/XDG directories for Godot fixtures. All reported results are from clean successful runs.

## Source preservation

The builder audit verifies all **629 inherited PNGs** unchanged, unchanged chain/upper bail and every pixel outside the 730-pixel moving mask, and exact source-pixel reconstruction when the separated layer is placed at zero. The original `artwork/bust_base.png` SHA-256 remains `30e37ee3c3dd6cfa959b31263e7f0f469bcd1b8c06fa5ccfaaf96d236fa63287`.

`motion_deform.gdshader`, `motion_vertex.gdshaderinc` and `optional_effects.gdshader` are byte-identical to approved main. Existing tests and demo clip files are unchanged. All 737 inherited project files are present.

## Actual Godot rendering and visual inspection

- `review_pendant.gd` plays the actual `demo_pendant_clip.json` and records torso reversals, held settling, head-only input, combined breathing/expression/mouth/effects, pause/resume, off/on, real loopback UDP takeover of a paused clip and timeout recovery.
- The main H.264 MP4 contains 871 frames at 30 fps, 568 × 760, lasting 29.033 seconds. A 1100 × 900 detail MP4 enlarges the necklace region from the same runtime capture.
- 117 logged runtime samples validate a fixed source pivot, bounded angle, frozen paused state, no sustained head-only drive, immediate original-source restoration when off, one actual UDP takeover packet, and timeout recovery with the enabled preference retained. The sampled review's peak relative angle was 2.901 degrees; this is intentionally small finishing motion.
- Three actual runtime captures with the pendant disabled were pixel-identical to approved main, including neutral, supported-expression gaze and authored-effect states with optional overlays. Neutral on/off captures also matched exactly.
- Source-AVI frames at 17.5 and 18.0 seconds were pixel-identical across the full paused frame.
- Fifty-nine chronological half-second frames were inspected in both full-view and necklace close-ups. The chain/bail connection remained attached in those samples, with no visible duplicated stone, stationary shadow ghost or new collar/neck seam.
- Eight additional actual Godot captures covered neutral on/off, forced ±10-degree hinge limits, independent head motion, bounce and combined controlled breath. The enlarged limit and combined-control views were inspected. The small skin reconstruction and retained source fringe remain limitations at enlargement.

## Remaining limits and approval

Hidden skin is interpolated locally, not recovered from the source; the original shadow/fringe moves with the stone. There is no collision, relighting, 3D chain or independent-link model. The 29-second movie took 1 minute 29 seconds to render, reported as 32% of real-time speed. Decoded-frame inspection is not native-speed playback or a target-device performance measurement. Native-speed motion, target-machine performance and low-limit graphics compatibility remain unverified. The user approved the video with these limits disclosed. No CI, paid resources, hardware flashing or remote-machine execution was used.

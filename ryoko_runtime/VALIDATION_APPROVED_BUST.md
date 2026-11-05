# Approved bust integration validation

Date: 2026-11-05. Base main: `c940508462584087000125b321c9cdecf758c622`.

## Scope

Integrates the user-approved rigid iris gaze, controlled breathing, neutral brows, coordinated look-at and hanging hairpin ornament with the existing bust rig. Full-body artwork and gestures are excluded. No CI, paid resources, hardware or remote machines were used.

The candidates were reviewed separately and approved by the user. Integration preserves their driver code and artwork. O retains brow raise; Shift+O is the independent ornament toggle.

## Local checks

All 19 local Godot suites pass, with 131,693 counted assertions plus the separate bounce amplitude/settling suite.

- `AUDIO_MOUTH_CHECKS_PASS count=376`
- `INDEPENDENT_BODY_CHECKS_PASS count=534`
- `BOUNCE_CHECKS_PASS body_peak=14.8804968419234 chest_peak=7.58371686935425 settled=true`
- `BREATH_CHECKS_PASS count=15974 peak=0.99703496502315`
- `BROW_CHECKS_PASS count=7752`
- `CHEST_SECONDARY_CHECKS_PASS count=298 peak_source_pixels=3.06753778457642`
- `CLIP_CHECKS_PASS count=45`
- `FACIAL_CONTROL_CHECKS_PASS count=89`
- `EXPRESSION_CONTROL_CHECKS_PASS count=58504`
- `EYELID_CHECKS_PASS count=120`
- `GAZE_CHECKS_PASS count=42103`
- `GESTURE_CHECKS_PASS count=256`
- `HAIR_SECONDARY_CHECKS_PASS count=289 head_peak=6.67058324813843`
- `INTEGRATED_BUST_CHECKS_PASS count=11`
- `LIVE_INPUT_CHECKS_PASS count=40`
- `LOOK_AT_CHECKS_PASS count=1107`
- `COUPLED_MOTION_RIG_CHECKS_PASS count=3204`
- `ORNAMENT_CHECKS_PASS count=826 driver_peak=0.08071931663141 rig_peak=0.06538102594081`
- `POSE_STORE_CHECKS_PASS count=165`

`test_integrated_bust.gd` covers simultaneous feature controls, shared shader composition, timed-clip pause/resume, O/Shift+O isolation, reset with the ornament enable setting preserved, combined real UDP packets and shared timeout release.

All 594 original artwork PNGs are byte-identical to remote main. The six approved rigid iris assets are unchanged. The six approved brow derivative textures are added. Brow skin masks do not overlap iris aperture masks.

## Rendered inspection

`capture_integrated_bust.gd` produces five actual Godot/OpenGL screenshots: neutral, simultaneous look/brows/breath/ornament with speaking mouth and body tilt, non-neutral expression fallback, held blink, and reset. All five were visually inspected. Eyes remain clipped, brows and mouth are registered, and the hanging ornament remains attached. Rendering completed without script or shader errors; the dummy display reports only an unsupported V-Sync warning.

These screenshots check final GPU composition, not native-speed temporal quality. The user approved the separate runtime motion videos. This integration adds no new animation amplitudes or artwork.

## Boundaries

The new channels work through local API/keyboard and opt-in loopback UDP. Existing timed clips pause them correctly, but their cue allowlist has not been extended to animate these new channels directly. Eye and brow cutouts are neutral-expression-only; authored expression presets retain their own eyes and brows. Earrings, necklace, full-body rigging and camera tracking remain outside this update.

## Reproduce

With Godot 4.6, import the project and run every `test_*.gd` script headlessly. Run `capture_integrated_bust.gd` under a local OpenGL-capable display for visual composition checks. Temporary import caches, user data, video captures and machine-specific paths are not source assets.

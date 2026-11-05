# Approved lower side-lock motion

Built on approved main `b7255357201c8148b663bc403abb0ae1e0dbfa39`. The existing crown/bun spring stops above the face; the outer loose hair beside the jaw and neck previously remained rigid. This revision gives those lower tips restrained independent left/right follow-through using the existing mesh and artwork.

The user reviewed the actual runtime footage and close-up and approved this revision on 2026-11-05. It adds no expressions, image assets, cutouts, underpaint, texture samplers or mesh vertices. All 610 inherited PNGs remain byte-identical. The face, ear studs, earrings, necklace and clothing retain their existing controls.

## Controls

- **X:** toggle lower side-lock motion. This takes over from a running timed clip before applying the toggle.
- API, opt-in loopback input and version-1 timed clips: `loose_hair_secondary: true` or `false`.
- F still controls the crown/bun; Shift+F still controls earrings.
- Disabled mode supplies zero additional displacement. Neutral enabled/disabled GPU captures are pixel-identical.
- R / reset clears both spring states, preserving the enabled setting. Clip cancellation and live-input timeout likewise preserve this setting.
- Clip pause freezes both springs; resume continues without jumping the cue clock.

Example with the existing `--live-input` opt-in:

    python send_live.py --seq 1 '{"loose_hair_secondary":true,"head_tilt":0.8,"body_tilt":0}'

The existing loopback-only input, strict boolean validation, stale-packet rejection and two-second timeout remain in force. No socket opens by default.

## Deformation

Each side has its own damped spring driven by the transformed root position. Horizontal motion is primary; vertical anchor motion is attenuated. Offset length is limited to 10 source pixels, under 5 screen pixels at the default scale, and the existing spatial weights further reduce visible motion. Stationary poses settle to exactly zero. There is no added idle oscillation, and periodic breathing does not drive the springs.

Weights on the unchanged 32 × 40 mesh are:

- Vertical: smoothstep(600,690,y) × (1 − smoothstep(750,795,y)).
- Screen-left: 1 − smoothstep(335,390,x).
- Screen-right: smoothstep(746,790,x).

Actual triangle interpolation extends support to y588.2–795.8, left of x390.5 and right of x745.5. These boundaries deliberately exclude the inner hair overlapping ears, face and jewelry. Do not widen them without rerunning the geometry audit and visual checks.

## Evidence

`test_loose_hair.gd` covers dynamics, finite bounds, exact settling, protected mesh boundaries, existing-control parity, uniforms, pause/resume/reset, manual takeover, timed cue typing and dispatch, and actual loopback UDP delivery/timeout.

`tools/validate_loose_hair_geometry.py` uses Pillow and NumPy to audit the actual piecewise-linear mesh weights at the four corners and center of every source-pixel footprint. It verifies zero influence on all registered facial overlays, gaze/brow masks, earring masks, ear/stud landmarks, central face/neck and visible clothing. Its color heuristic supplements, not replaces, image inspection.

`review_loose_hair.gd` records the actual runtime through head reversals, torso movement, settling, off/on comparison, an existing expression with blink/mouth, combined gaze/brow/breath controls and reset. `capture_loose_hair_qa.gd` captures neutral on/off and a frozen moving pose on dark and light backgrounds. See `VALIDATION_LOOSE_HAIR.md`.

## Limits

This is small weighted deformation of outer hair tips, not individually separated strands, front-bang physics, collision detection, wind simulation or a new head-turn rig. Inner strands remain attached to the existing head/neck transform. The existing faint low-alpha source fringes are preserved, not cleaned up or repainted.

Native-speed playback is unavailable to the assistant. Review uses chronological decoded frames, enlarged dark/light comparisons, state logs and tests; the user reviewed and approved the actual MP4 before publication. Rendering was verified in desktop Godot 4.6.3 with Mesa llvmpipe. The inherited shader's low-limit graphics compatibility and real-time performance remain unverified.

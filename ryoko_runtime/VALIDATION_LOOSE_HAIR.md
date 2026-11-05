# Approved lower side-lock validation

User-approved revision based on approved `b7255357201c8148b663bc403abb0ae1e0dbfa39`, 2026-11-05. The user reviewed and approved the actual runtime MP4 and close-up before publication.

## Automated tests

All 22 local Godot 4.6.3 suites passed: 156,837 counted checks plus the existing bounce amplitude/settling suite. The new suite passes 22,731 checks, including real ephemeral-port UDP control, stale-packet rejection and timeout release; its targeted run passed twice.

Measured solver peak: 9.9990 source pixels within a 10-pixel limit. The dedicated runtime test peaks at 4.3427 pixels, with distinct left/right responses. Tests cover finite inputs, stalls, monotonic protected weight boundaries, rest, settling, disable/re-enable, reset, retained settings, pause/resume, X takeover, typed clip loading and actual timed on/off cues. Existing gaze, brows, breathing, earrings, hairpin, crown, face, expression, torso, audio, gesture and clip suites pass.

All 610 inherited PNGs are SHA-256-identical to the approved project. No artwork, registrations, image samplers or mesh vertices were added.

## Source and geometry audit

The actual mesh's piecewise-linear weights are evaluated at each source pixel's four corners and center, rather than testing the analytic weight function alone.

- Zero influence on all 592 registered overlays, covering 13,453,075 alpha-bearing overlay pixel footprints.
- Zero influence on both earring clear masks, both gaze apertures, both brow masks, fixed ear/stud regions, central face/neck and visible clothing from y796 down.
- 7,474 affected visible source pixels on the left and 2,158 on the right; all pass the conservative mint-hair color heuristic at alpha above 76/255.
- Additional-deformation Jacobian lower bounds are 0.7455 left and 0.7373 right for any offset vector of length at most 10. These are positive; they concern this added displacement, not a new proof of every inherited deformation.
- A separate 225-case extreme-offset/head/body mesh check also found no inverted triangles.
- Existing faint warm fringes are retained: 12 left pixels, maximum alpha 9/255; 15 right pixels, maximum alpha 14/255.

Reproduce the source audit with `python3 tools/validate_loose_hair_geometry.py`. It writes a JSON report to the sibling output directory. The heuristic and landmark boxes do not substitute for runtime visual review.

## Actual GPU evidence

The MP4 is actual Godot OpenGL movie-writer output, encoded by FFmpeg: 29.033 seconds, 871 frames at 30 fps, 568 × 760. The 930 × 690 close-up is a crop of that same footage. Recording reached `LOOSE_HAIR_REVIEW_COMPLETE` without script or shader errors; 117 state samples record an observed peak of 7.879 source pixels and a final exact-zero offset on both sides.

Neutral enabled/disabled captures have zero differing pixels. Frozen-pose on/off captures, enlarged dark/light edge comparisons, and chronological frames sampled at 2 fps were inspected. Visible changes stay at the lower outer hair, without detaching the ear studs, earrings or collar. Small one-level rasterization differences exist elsewhere in the frozen comparison; it is not a claim of pixel identity for every moving frame.

Native-speed playback was unavailable to the assistant. The fixed-frame renderer ran slower than real time and does not establish playback performance. The user reviewed and approved the MP4 before publication. No CI, paid resources, remote-machine execution, full-body changes or new expressions were included.

# EXP-096 Headache tension: unapproved headless preparation

This candidate lives outside the production rig and registry. It uses the unchanged approved36 baseline at `3ce98774282ad6c20dfbd7018d20838ff861b762`: all 999 manifest-pinned files, including 184 PNGs, remain exact in the source and `rig/` copy. Both source manifests are retained. The disk registry still contains 36 profiles; the candidate and probes are registered only in memory. All 993 common runtime/artwork files match approved41. The six explicitly excluded newer-tree files are registry, release, readme and aggregate-validation metadata, not runtime or artwork.

## Source inspection and limitations

The actual 1159 × 1358 nine-panel sheet and catalogue entry were inspected before authoring. `SOURCE_REFERENCE.json`, `SOURCE_CATALOGUE_ENTRY.json` and `BASELINE_FREEZE.json` preserve source locations, SHA-256 hashes, exact catalogue data, observations and limitations. All nine panel images are independently checked as exact lossless crops of the sheet.

The image sequence is decisive: central brow tension develops, ordinary bilateral lids progressively close, KP5–6 remain fully closed, KP7 softens brow and mouth tension with the eyes still closed, and only then do the eyes reopen. The source has a small pressed/downturned lip line, not a smile, open mouth or lateral gaze.

The frozen rig cannot create real central furrows, horizontal brow convergence, new brow contour deformation or independent downturned mouth corners. This candidate is explicitly an approximation:

- Equal lowered rigid brows at peak translate down 5.5 source pixels; opposed tilts rotate the screen-left brow +5.2 degrees and screen-right brow −5.2 degrees. Their pivots do not converge horizontally.
- Ordinary blink_R and blink_L both reach 1.0. The actual upper lashes travel 36 source pixels; iris closure is checked separately. No smile-eye or extra eye opening is used.
- Existing lip-pressure owners use .65 pressure. Their shader amount and visibility are checked individually across static poses and the whole timeline.
- Tiny symmetric purse .05 reduces total mouth width by 1.4 source pixels (.686 pixels at bust scale). It moves the center down .2 source pixels and both endpoints down .6. This small symmetric contour is not a genuine independent downturned corner. Mouth aperture is zero throughout.

Brow names use screen sides. Blink names use character sides: blink_R closes the screen-left eye, and blink_L closes the screen-right. All mouth opening, smile, corner lift, spread, independent width, kiss, eye_smile, opening_px, gaze and aversion controls stay exactly zero. There is no head/body acting, blush, speech, hair motion, effect, new anatomy, artwork, runtime or shader change.

## Four-second interpretation

This is newly authored timing from a static reference, not recovered animation. The catalogue's proposed 1.9-second timing is retained as reference metadata, not claimed as implemented motion.

| Time | Source role | Candidate action |
| --- | --- | --- |
| 0.00–0.20 | KP1 | Exact neutral lead-in |
| 0.60 | KP2 | Brow tension, pressure and ordinary lid closure begin |
| 1.00 | KP3 | Lid closure .38; tension develops |
| 1.30 | KP4 | Lid closure .70; gradual approach to peak |
| 1.60–2.40 | KP5–6 | Fully closed ordinary lids and sustained pressed tension |
| 2.80 | KP7 | Brows and mouth soften; lids remain exactly fully closed |
| 3.20 | KP8 | Reopen to closure .18 after tension release |
| 3.70–4.00 | KP9 | Exact neutral return and hold |

There are eight unique static anchors, eleven timeline keys and 121 endpoint-inclusive samples at 30 Hz. KP5 and KP6 deliberately share the held peak anchor. Unchanged smoothstep interpolation provides zero-velocity joins. Every acting channel changes by less than .20 per frame. The closed interval is explicitly checked from 1.6 through 2.8 seconds, including the relaxed KP7 endpoint.

## Distinctness and headless verification

All 36 baseline profiles and nine later candidates are compared at 121 normalized times; none is numerically duplicated. Key comparisons are EXP-043 Silent Fury (open eyes, more severe brow tension), EXP-174 Sleepy Annoyance (partly open irritated lids) and EXP-177 Meditative Calm (relaxed closed eyes). Full closure under tension followed by a still-closed relaxation phase is the intended distinguishing sequence. Numerical differences do not establish visual fidelity or perceptual distinctness.

Passed author checks:

- 1,806 static assertions, including actual brow/lash/iris/lip geometry, pressure-owner state, body preservation, bounds, excluded controls and exact reset.
- 16,260 motion assertions across all 121 frames, with the source ordering, full closure, sealed pressure/purse, exact neutral and disk-registry preservation checked.
- Nine interruption points, 36 continuity/reset/neutral assertions and 252 sampled restart/release states. Release is tested directly from each interrupted pose, not only after restart.
- 10,338 independently calculated numerical/source checks reproduce the entire timeline and all 252 lifecycle poses. Maximum timeline error is below 2.92e-8; lifecycle error is below 4.48e-8. Nine source panels match their sheet crops exactly.
- 74 author guard tests: 20 encoder guards, 26 numerical mutation tests and 28 evidence-validator tests. These are synthetic/headless tests, not native visual evidence.
- Headless Godot 4.6.3 import and all three launcher script parse checks pass. The inherited export warning for `uneasy_clear_parting.png` is recorded, not suppressed or modified.

Run from this directory:

    sh run_motion.sh --state
    python verify_preparation.py
    python independent_geometry.py
    python -m unittest test_encode_preview test_independent_geometry test_review_validation -v
    python verify_input_freeze.py
    python review_validation.py

The final command must report **PENDING** and exit 2 while native evidence is absent. The encoder must refuse to encode without successful current native receipts. Any later input change or regeneration requires a new explicit author handoff freeze. Preserve existing capture evidence rather than overwriting it.

## Separate native launcher: prepared, not run

`native_launcher/project.godot` is named **Ryoko EXP096 Headache tension PREVIEW ONLY**. Its only baseline-file override is the project name/main scene. The other 998 pinned files and extra source manifest remain byte-identical. Generated wrappers are verified against the headless probe scripts. The inherited default project window is 1136 pixels wide; capture code sets and strictly checks the actual **568 × 800** full/bust and **400 × 360** detail viewports before saving any image. Merely requesting a size is not accepted as evidence.

The launcher refuses to overwrite existing `capture/` or `motion/` directories. Preparation did not launch the native UI, native shell, display server, display socket, remote machine or graphical workaround. Future native capture needs a separately authorized step and visual inspection. No native fidelity or normal-speed observation is claimed here.

`encode_preview.py` accepts only successful current native receipts, all 242 ordered RGBA frame hashes, strict dimensions and exact neutral return. It refuses an existing output. The intended future file is `Headache_tension_review_v1.mp4`: 968 × 800, 30 fps, 121 frames, approximately 4.033 seconds. The read-only review validator checks all native image sets and complete video decoding/order when those inputs exist, but does not claim human-like continuous observation or source fidelity.

`review_input_freeze.json` pins author-produced preparation files only. It excludes actual independent reviewer outputs, later capture/MP4 evidence, test logs and generated review reports. This avoids inventing independent review or a circular freeze.

**Status: UNAPPROVED. Native captures, MP4, normal-speed observation, independent reviewer sign-off, production integration and publication remain pending.** No other candidate, approved-unpublished backlog entry or denied main update was changed. No CI, paid resource, purchase, hardware action or remote-machine execution was used.

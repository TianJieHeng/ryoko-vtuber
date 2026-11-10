# EXP-045 Irritated Side-eye: unapproved shared-rig candidate

This isolated candidate uses the frozen approved36 baseline at commit `3ce98774282ad6c20dfbd7018d20838ff861b762`. All 999 manifest-pinned source files, including 184 PNGs, remain exact in the original source and `rig/` copy. Both source manifests are retained (one is already among the 999 pinned files). The production disk registry still contains 36 entries; the candidate and probes are registered only in memory. All 993 common runtime/artwork files also match approved41. Six registry, release, readme and aggregate-validation files are explicitly excluded from that newer-tree comparison.

## Inspected reference and supported interpretation

The actual 1159 × 1358 nine-panel EXP-045 sheet was viewed before authoring. Source paths, sheet/catalogue/panel SHA-256 hashes, the exact catalogue entry, observations and limitations are preserved in `SOURCE_REFERENCE.json`, `SOURCE_CATALOGUE_ENTRY.json` and `BASELINE_FREEZE.json`. All nine linked panel images are checked as exact lossless crops of the sheet.

The reference deliberately shifts both irises toward screen-right, narrows the upper lids, lowers the screen-left brow and relatively raises the screen-right brow with unequal opposed inclinations. A restrained sealed mouth develops a downturned corner. Gaze and facial tension then recover.

**The frozen rig has no independent downturned-mouth-corner control. That reference feature is not implemented.** Every mouth channel remains exactly neutral and sealed. An upward sneer or symmetric purse is not substituted. This candidate therefore approximates the reference through gaze, lids and brows only. It needs independent source and native visual review before any user-facing preview or approval decision.

Seven existing channels act: two rigid brow heights, two rigid brow tilts, two ordinary lid closures and positive source-pixel aversion. At peak:

- Both original irises move 12 source pixels toward screen-right (5.88 pixels at bust scale). Iris sprites and iris/sclera shader offsets are checked separately.
- Screen-left/right upper-lash travel is 13.68/10.8 source pixels, from character-side blink_R=.38 and blink_L=.30.
- Screen-left brow moves 6.5 source pixels down and rotates +4 degrees. Screen-right brow moves 2.2 source pixels up and rotates −2.24 degrees.
- Mouth contours, mouth width and central lip gap remain neutral. There is no new anatomy, drawing, texture, runtime, shader, head/body motion, ordinary gaze, eye-opening, eye-smile, smile, blush, speech, hair motion or effect.

Brow names use screen sides. Blink names use character sides. Positive aversion_px is explicitly screen-right, in original source pixels.

## Newly authored four-second timing

There are eight static anchors, eleven timeline keys and 121 endpoint-inclusive samples at 30 Hz:

- 0.00–0.20: exact neutral lead-in.
- 0.60: unequal brows and narrowed supporting lids established, gaze still centered.
- 1.00: deliberate 6-pixel rightward glance.
- 1.60–2.40: sustained 12-pixel side-eye with unequal opposed brows and narrowed lids.
- 2.80: gaze recovers to 5 pixels with supporting lids retained.
- 3.20: gaze fully centered while both lid closures are still at least .18.
- 3.50: lids and brows settle.
- 3.70–4.00: exact neutral hold.

This is a new interpretation of static reference art, not recovered original motion. The unchanged smoothstep interpolation has zero-velocity anchor joins. Every adjoining aversion-active segment has both endpoint lid closures at least .18, including its zero-aversion entrance and exit. Ordinary gaze, eye-smile and opening stay zero. Independent endpoint analysis and dense samples near segment boundaries verify the whole-segment invariant, not just the 30 Hz sample grid.

The largest permitted aversion frame-step guard is .9 source pixels. The analytic smoothstep derivative bound for the fastest 7-pixel return over 12 frames is .875 pixels/frame. Other controls retain a .20 per-frame limit. Source sprite positions use a 1e-4-pixel tolerance because the engine stores positions near x=500 in single precision; shader offsets and numerical poses are checked independently.

## Distinctness, not visual approval

All 36 baseline profiles and seven later candidates were independently compared at 121 normalized times. No trajectory duplicates this candidate. The intended distinctions are:

- EXP-042 Cold glare is frontal, bilateral and still. EXP-045 intentionally glances sideways with unequal opposed brows.
- EXP-081 Mild disgust is mouth-led with an asymmetric lifted contour. EXP-045 leaves the mouth neutral and has a deliberate lateral look.
- EXP-144 Caught staring has wide-eyed startle, blush, worried inner-brow lift and embarrassed downward recovery. EXP-045 has none of these and keeps the irritated side-eye hold.

Numerical differences do not establish perceptual distinctness or reference fidelity. Those remain pending native review.

## Headless verification

- 1,582 static assertions cover actual brow, lash, iris and lip geometry, scope, bounds, excluded channels, fixed body, exact reset and registry preservation.
- 12,701 motion assertions cover all 121 states, held peak, aversion ordering, actual source-pixel iris offsets, exact neutral and lifecycle behavior.
- At nine interruption points, 36 continuity/reset/neutral assertions and 252 restart/release samples are recorded. Releases are tested directly from the interrupted pose, including active side-eye, not merely after a restart has centered the gaze.
- A separate Python implementation performs 9,990 numerical/source checks, reproducing the entire timeline and all 252 lifecycle poses, including the two-stage scoped aversion handoff. Maximum timeline error is below 2.64e-8; maximum lifecycle error is below 4.04e-8. All nine reference panels match their sheet crops.
- All 66 mutation tests pass: 20 encoder guards, 19 numerical checks and 27 read-only evidence-validator checks. They reject unsupported lid/gaze joins, shifted geometry, added mouth acting, stale inputs, malformed frames, headless evidence and missing native captures.
- Headless Godot 4.6.3 import and three launcher script parse checks pass. The inherited image-load export warning for `uneasy_clear_parting.png` is not suppressed or modified.

Re-run from this directory:

    sh run_motion.sh --state
    python verify_preparation.py
    python independent_geometry.py
    python -m unittest discover -s . -p 'test_*.py' -v
    python verify_input_freeze.py
    python review_validation.py

The final command returns PENDING with exit code 2 until native captures and the MP4 exist. That is not a native pass. Re-running mutable probes or changing inputs requires a new explicit handoff freeze. Preserve any existing native evidence.

## Separate native launcher, prepared but not run

`native_launcher/project.godot` is named **Ryoko EXP045 Irritated Side-eye PREVIEW ONLY**. Its only baseline-file override is project name/main scene; 998 other baseline files and the extra source manifest remain exact. Generated wrappers match the headless-probe transformation. This inherited project configuration uses the original 1136-wide default; the capture probes set and strictly verify actual viewports at **568 × 800 full/bust** and **400 × 360 detail** before writing any PNG. Requested sizes alone are not proof of correct native dimensions.

Under separate authorization, the native Godot UI can run this project. It refuses to overwrite existing `capture/` or `motion/` directories. No native capture, UI, native shell launch, display server or socket workaround was used in preparation. Native evidence must be produced and inspected before encoding. Failed evidence must be preserved rather than overwritten or relabeled.

`encode_preview.py` only accepts successful, current native receipts, exact dimensions and RGBA mode, all 242 frame hashes, ordered times and exact neutral. It refuses an existing output. Intended output is `Irritated_side_eye_review_v1.mp4`, 968 × 800 at 30 fps, 121 frames and approximately 4.033 seconds. The read-only validator checks full native image sets and MP4 decode/order. It does not claim normal-speed observation or perceptual fidelity.

`review_input_freeze.json` freezes only author-produced preparation inputs and receipts. It deliberately excludes independent reviewer artifacts so those can be created by the actual reviewer later without inventing review or creating a circular freeze. Test logs and later reports are not inputs.

**Status: UNAPPROVED. No native captures, MP4, normal-speed observation, independent reviewer sign-off, production integration or publication exist at this handoff.** No CI, paid resource, remote-machine execution or hardware action was used.

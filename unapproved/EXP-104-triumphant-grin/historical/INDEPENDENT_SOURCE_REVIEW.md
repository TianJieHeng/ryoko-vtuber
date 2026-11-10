# EXP-104 Triumphant Grin: independent source review

## Decision and evidence boundary

**Source interpretation and frozen numerical preparation pass this independent review. Native appearance, complete motion/video evidence, normal-speed observation, perceptual distinction and user approval remain PENDING. The candidate remains UNAPPROVED.**

This review pins the author contract `review_input_freeze.json` to SHA-256 `40f54ee01529ef96d18404cd2f3ebb1e2bf3004662cf2c45055434fb063aef7a`. The reviewer did not modify that contract, any of its 47 pinned inputs, the profile, source artwork, rig, runtime, launcher, probes or production registry. No renderer, UI, native launch, encoding, publication, CI or remote execution was performed by this review.

The author-owned `independent_geometry.py` and its tests are not independent reviewer sign-off. This report and the separate `independent_review_validation.py` / `test_independent_review_validation.py` are reviewer-owned. The capture/decode infrastructure is adapted from the established reviewer-only validator scaffold; the EXP-104 interpretation contract, geometry and trajectory assertions are expression-specific and independently evaluated.

## Actual source inspected

The actual 1159 × 1358 nine-panel `RYO_EXP-104_triumphant-grin_sheet_v001.png` was visually inspected in this review, rather than inferred from a title or the author's observations. Its SHA-256 is `f94654b74f3d08894027c9ab094c4d867c99282931c14d7e4038756f244c1678`. The accepted catalogue's intent is: “Brows lower with energetic certainty; eyes focus brightly; a wide teeth-showing grin spreads.”

- Panels 1–4 develop from a neutral mouth through a centered smile. The brows lower and angle inward on both sides, while the irises remain directed toward the viewer and the eyes remain visibly open.
- Panel 5 is a broad tooth-showing grin under stronger inward brow tension. Panel 6 opens the grin further. This is the clearest source basis for a shallow tooth-grin hold followed by a somewhat more open grin, rather than a single undifferentiated smile peak.
- Panels 7–9 relax the smile and brow tension toward neutral. The source does not require unilateral corner bias, a downcast glance, closed smile-eyes, head motion, speech or body gestures.
- The neutral endpoint here means the shared rig's canonical neutral, not a claim that separate source-sheet neutral panels are pixel-identical.

The validator checks the exact catalogue entry, sheet dimensions/hash, all nine panel hashes and equality of every panel to its specified lossless integer crop of the sheet. The catalogue hash is `ded1b313c36b66daf46f3426288ef4670b04703497323314754bba18e872b2bf`.

## Supported implementation and limits

The candidate uses only nine existing controls: equal bilateral brow heights, opposed inward brow tilts, equal ordinary partial eyelid closure, smile, public spread and opening. Brow names use screen sides. Positive screen-left tilt and negative screen-right tilt lower the inner ends. Eyelid channels use character sides: `blink_R` controls screen-left and `blink_L` controls screen-right.

At the shallow grin, the independently pinned vector is height −0.32 on both sides, tilts +0.42/−0.42, equal closure 0.12, smile 0.84, spread 0.86 and opening 0.30. The later open grin uses −0.30, +0.40/−0.40, closure 0.10, smile 0.88, spread 0.90 and opening 0.46.

The reviewer independently evaluates the existing geometry:

- Brow translation is −10 × height source pixels, and rigid rotation is 8 × tilt degrees. Both recorded outer-anchor coordinates and their composed positions are checked against the unchanged object pivots. Inner-brow lift remains zero.
- Upper-lash travel is 36 × closure source pixels, with no horizontal travel. Ordinary lid closure is not an independently reshaped focused eye or a smile-eye deformation.
- Effective spread is public spread × smile. The shallow grin adds 28.896 source pixels of mouth width, not the 34.4 pixels that incorrectly treating public spread alone would imply. The later open grin adds 31.68 pixels.
- The shallow grin's central split-lip aperture is 8.91 source pixels, or 4.3659 pixels at bust scale 0.49. The later grin reaches 13.662 source pixels, or 6.69438 bust pixels. Shallow-grin upper corner offsets are equal at −9.28368 source pixels.
- The upper and lower lip contours are independently checked at both corners and the center. Gaze, inner brow lift, independent corners, purse, pressure, sealed-only widths, smile-eyes, blush, hair and other excluded channels remain zero.

**This is a shallow open tooth-bearing grin approximation, not an exact dental clench.** It uses the existing upper-tooth arch and passively coupled spread support. There is no independent dental control, new opposing tooth-row anatomy, sealed clenched-teeth shape, jaw rotation, cheek deformation or chin movement. Author probes assert passive tooth-node positions/rotations/visibility; those node transforms are not separately serialized in the receipts. This reviewer does not misrepresent a visibility flag or calculated aperture as observed enamel pixels. Tooth exposure, mouth seams and the readable focused expression must be checked on real native captures.

## Trajectory and distinction

The reviewer independently pins all eleven times and vectors, all eight static anchor names/vectors and all 30 shared pose channels. A separate smoothstep calculation, including the existing 0.30-second restart factor, agrees with all 121 endpoint-inclusive recorded samples to a maximum control error of `1.4790782043583306e-08`.

The four-second trajectory has a neutral 0.00–0.20 lead-in, sealed smile and brows at 0.60, grin development at 1.00, shallow grin held at 1.60–2.00, more open grin at 2.40, recovery at 2.80, reseal with residual smile/brow tension at 3.20, and exact neutral from 3.70 through 4.00. Opening and smile have one monotone build and recovery; no extra oscillation is introduced. The static references do not supply this timing. This is newly authored motion, not recovered source animation. Smoothstep's zero-velocity joins and the shallow hold remain deliberate stylistic choices whose rhythm needs normal-speed review.

I also visually inspected the actual EXP-114 v002, EXP-152 v002 and EXP-001 v001 source sheets, checked their hashes/dimensions against the same catalogue, and read their profiles from the approved36 baseline:

- **EXP-114 Daring Provocation:** source and profile emphasize an unequal-eyed, asymmetrically raised/lowered-brow challenge and crooked corner-biased grin. EXP-104's intended distinction is bilateral low inward brows with a centered grin. Its neutral and toothy moments may still resemble this neighbor, so numerical differences alone are not enough.
- **EXP-152 Private Pride:** source and profile use a downcast gaze, soft ordinary lids and a restrained sealed smile. EXP-104 keeps direct gaze and progressively opens a broader grin. EXP-152 has additional gaze, pressure and common-corner controls that remain excluded here.
- **EXP-001 Bright Welcome:** source and profile are a friendly open smile with raised brows. Its peak mouth opening is 0.80, versus EXP-104's 0.46, and EXP-104 uses lowered, inward-angled brows. This is an intent/control difference; it is not yet proof of native perceptual separation.

Independent normalized-time comparison against every one of the 36 frozen baseline profiles found no duplicate trajectory. Maximum control differences from EXP-114, EXP-152 and EXP-001 are respectively 0.78, 1.00 and approximately 0.59428. These measurements are not perceptual scores. No candidate-versus-approved native image comparison has been passed at this stage.

## Preserved inputs and validation outcome

The review verifies all 999 pinned baseline files, including 184 PNGs, in the source and candidate rig; 998 baseline files in the native launcher, with only its authorized project override; both extra manifests; the original 36-profile registries; and all 993 common runtime/artwork files against each of approved40 and approved41. The six explicitly excluded newer metadata/registry/aggregate-validation files are not confused with runtime or artwork changes.

At this source-review checkpoint:

- All 36 available top-level reviewer checks pass. There are no failures.
- All 58 reviewer-owned tests pass; all 105 author-plus-reviewer unit tests also pass. They include mutations of the pinned contract, anchors, timing, symmetry, gaze, brow positions/rotations/outer anchors, lash travel, smile-coupled spread, lip contours, native hashes/dimensions/modes/counts, neutral/held/body pixels, static-motion correspondence, stale/headless receipts, MP4 metadata/order/similarity and complete/partial decode behavior.
- Synthetic arrays and receipts exist only inside unit tests. They are not native artwork, capture evidence or approval.
- The main validator returns **PENDING, exit 2**, not PASS: 17 required static files and 243 required motion files are absent, and no review MP4 exists. The frozen author check remains byte-exact.

## Native completion gate

After a separately authorized native capture and encoding, rerun:

    python independent_review_validation.py
    python -m unittest -v test_independent_review_validation
    python verify_input_freeze.py

The reviewer validator only reads already captured native evidence and decodes an existing MP4. It never starts Godot, a renderer, a UI or encoding. It requires exactly 16 static PNGs, exactly 121 full and 121 detail RGBA frames at 568 × 800 and 400 × 360, frozen-input-matching native receipts, all 242 motion pixel hashes, exact static-to-motion anchors, neutral bookends/holds, the shallow held grin and unchanged pixels outside the fixed face region. Missing evidence stays pending; invalid evidence fails.

For `TriumphantGrin_review_v1.mp4`, it checks H.264/yuv420p, 968 × 800, 30 fps, 121 decoded frames, about 4.033 seconds and every frame timestamp. It fully decodes and compares all full/detail panels to their same-index native frames, plus nearest-face comparisons to detect material reordering. Lossy encoding and pixel-identical/near-identical holds limit the ability to distinguish swaps of indistinguishable frames; that limitation is explicit. FFmpeg errors or a partial decode fail.

Even an eventual technical PASS does not assert source likeness, visible tooth quality, normal-speed continuous observation, user approval or production readiness. Those must be reported separately. In particular, native review must establish that the shallow grin actually reads as triumphant rather than merely a generic smile, a clenched-mouth approximation, or EXP-114's crooked challenge.

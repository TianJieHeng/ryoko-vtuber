# Separate canonical eyes and bounded gaze

This preserves the prior gaze and ordinary-lid review record. Its one-performance counts describe that phase. The combined candidate additionally authors EXP-005; see SMILE_VALIDATION.md and validation/laughter_final_review.json for current evidence.

Historical context: this report records the delivered pre-correction gaze candidate. See LID_HANDOFF_CORRECTION.md for the subsequent ordinary-lid transition correction and its current validation.

Local review candidate. Internal source, rendering and control checks pass; user approval and publication are still pending. EXP-163 remains the only authored performance. This phase adds no AI model, TTS, tracking, remote execution, CI or additional expression.

## Contract and rendering

`control_limits.gd` supplies the shared registry, controller, viewer and loopback contract. Gaze is enabled in this exact review candidate. Each normalized axis accepts [-1, 1]. The corresponding rigid iris travel is left or right 4 source pixels, up 2 source pixels and down 1 source pixel. Wider commands are rejected atomically.

Sclerae, eye aperture, lower contours, head, neck and body stay fixed. Existing upper-lash closure motion is unchanged. Foreground hair retains its own pivots and layer order. Normalized mouth opening 0–1 still maps to physical aperture 0–0.55; hair remains bounded to ±0.07. Non-neutral legacy visemes remain gated.

The shader evaluates the aperture, endpoints and upper/lower clipping in fixed eye coordinates, not translating sprite UV coordinates. Alpha factoring applies aperture coverage once across independent sclera and iris owners. Hiding an iris reveals its complete stationary sclera. There is no gaze-zero branch, crossfade, eye/face UV warp, animated feature scale or full-face patch.

## Provenance and ownership corrections

All 103 original PNGs are unchanged; `GAZE_SOURCE_ORIGINALS.json` records their hashes. `tools/build_gaze_eyes.py` produces separate derivatives and provenance masks without modifying those originals. No different source-assembly iris or sclera drawing is substituted.

- The canonical opaque iris core and highlights retain original RGB and registration wherever clean source iris artwork exists.
- Boundary alpha and continuous sclera behind the iris are inferred from the flattened canonical eye. The earlier ellipse partition included whites and caused moving slivers.
- Clean stationary sclera removes the bright old-footprint rim in the initial nearly pixel-exact candidate. Flattened-edge equality was not preserved at the expense of correct ownership.
- Hidden iris caps and boundaries are labeled inferred artwork. A distinct 3–4 source-pixel completion band uses bounded local inward-color continuation, without inventing a bright upper highlight. Continuous bilinear-footprint analysis covers the full permitted gaze rectangle without relying on hair or lash occlusion.
- A screen-left hair-tip diagonal was embedded in the old iris pixels. Its contour is recut from the original registered `blink_R` artwork, with explicitly inferred alpha and color. It now follows the existing front-fringe pivot at (529, 218), with angle multiplier 0.6. An 84-pixel iris-under-hair region is reconstructed, and the old skin-colored notch is filled. This changes a small crossing region in neutral and during the yawn.
- `observed_iris_*` masks exclude foreign hair and pale-white contamination. Some support-edge locations still use inferred mattes; only the opaque subset claims unchanged source RGB. `iris_hidden_estimate_*` includes both concealed caps and visible inferred locations, counted separately in the manifest. These are not recovered original hidden layers.

Only the two runtime iris `.png.import` files disable alpha-border RGB rewriting. They are required source configuration. Original textures and global import defaults remain unchanged.

## Final rendered comparison

These measurements compare the final enabled candidate against the approved pre-gaze renderer, not against an intermediate prototype. Counts refer to changed rendered pixels; maximum differences are per RGB channel on the 0–255 scale.

- Native neutral: 193 changed pixels, maximum difference 201, within inclusive bounds (452, 486)–(671, 515).
- Native lids at 25%, 50%, 75% and 100%: respectively 143, 89, 58 and 58 changed pixels; maximum differences 120, 136, 136 and 136.
- Native actual EXP-163 at 1.5, 2.2, 3.0 and 3.8 seconds: respectively 81, 78, 78 and 74 changed pixels; maximum differences 132, 133, 132 and 133. These peak differences are confined to the corrected left hair/iris crossing. Mouth artwork, white teeth, the mouth cap and the authored yawn timeline remain unchanged.
- At the viewer's 0.49 display scale, neutral changes 203 pixels, maximum difference 98, within inclusive bounds (227, 308)–(335, 323).

The candidate is deliberately not pixel-identical to the old flattened eye edges. The larger local differences arise from correcting hair ownership and its old skin-colored notch, not from moving or stretching the face. Returning to this candidate's own neutral is exact at native and display scales.

## Verification

Independent testing of the frozen runtime/art source passed:

- Fresh Godot import: no tracked source or configuration changed. A clean full rebuild reproduced all 249 files in the runtime/art freeze byte-for-byte. The final test/documentation package adds the narrow migration record described below, without changing runtime or art.
- Original-source, asset and alpha-algebra checks: 1,215. Continuous coverage proof: left maximum inferred distance 4 pixels, right 3.606 pixels, with no contributing texel outside completed artwork.
- Python base, yawn and teeth checks: 131, 29 and 303. The teeth test preserves historical hashes and uses exact vetted eye-migration hashes. Three actual mouth function bodies independently match the published baseline.
- Godot base, yawn, teeth, backbone and gaze checks: 8,254; 57,367; 17,017; 101,957; and 330,814. Gaze testing includes 2,002 fractional samples and 108 endpoint combinations.
- Actual rendered matrix: 519 checks across 472 frames at native and bust scales. It covers seven lid states, nine gaze positions, three hair positions, fractional reversals, ownership isolation, actual yawn playback and lifecycle/rejection cases.
- Across 378 same-lid/hair gaze comparisons, no differences occur outside the eyes. All 28 fractional reversal pairs match exactly. Iris-hidden stationary backing is identical across five gaze positions.
- Viewer layout: 21 checks. Independent actual pointer/keyboard events: another 21 checks, including scrolling, manual takeover, the visible re-enable button, shortcuts and close/reopen behavior.
- Real subprocess loopback transport: 332 checks. The listener is off by default; manual control fencing remains intact. No AI or TTS service is connected.

Actual-yawn capture asserts a successful trigger, active EXP-163 ownership, elapsed timeline and non-neutral pose. Earlier rejected-command captures were discarded and are not evidence. Synthetic gaze/lid/hair coverage is labeled separately from the authored yawn.

## Review movie and reproduction

`ryoko_separate_eye_gaze_review_2026-11-07.mp4` is an external review artifact, not a repository asset: 34 seconds, 1,020 frames, 30 fps, 1136×800, no audio. It shows the actual Godot renderer through one active public controller, with mirrored fixed close-up render views. The sequence includes bounded sweeps, partial and unilateral lids, hair motion, reversals, an asserted unchanged EXP-163 timeline, interruption, release and reset. Full decoding reported no errors. Normal-speed playback is not claimed.

Run the verification commands in README.md. `tools/review_gaze.gd` captures asserted native or display matrices; `tools/review_gaze_movie.gd` produces the review sequence. Keep all outputs outside source. Use `--baseline` only on an isolated approved baseline copy. No diagnostic writes to the original approved project.

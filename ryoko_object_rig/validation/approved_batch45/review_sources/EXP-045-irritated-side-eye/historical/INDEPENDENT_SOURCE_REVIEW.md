# EXP-045 Irritated Side-eye: independent source and contract review

**Source-intent and numerical review: PASS WITH A MATERIAL REPRESENTATION LIMITATION. Candidate remains UNAPPROVED. Native visual fidelity, perceptual distinctness and continuous normal-speed observation are not established by this review.**

## What I inspected

I independently viewed the actual 1159 × 1358 nine-panel reference sheet, not a description or a generated substitute. Its SHA-256 is `5e3287f39ac6102934cfa2001150036345103d398760f738b6f1055c45b7f3ad`. I read the exact catalogue entry, candidate, static plan, frozen runtime's interpolation and scoped handoff, headless geometry/pose receipts, and numerical comparison inputs. All nine panel files were independently checked against their exact lossless sheet crops.

The source progresses from neutral into a deliberate screen-right glance with narrowed lids and unequal opposed brows. The screen-left brow becomes lower, while the screen-right brow is relatively raised. The sealed mouth develops an asymmetric downturned contour before the expression relaxes. The sheet does not specify the candidate's four-second timing; the catalogue's 1.9-second proposal is explicitly not an implemented animation. The candidate is a new timing interpretation, not recovered source motion.

## Representation and limitation

The candidate's seven acting channels are appropriate for the supported eye/brow part of this intent. Both iris sprites and their shader offsets move **12 original source pixels screen-right** at peak. At the .49 bust scale this is 5.88 pixels. Character-side `blink_R=.38` and `blink_L=.30` map to screen-left and screen-right lash descents of 13.68 and 10.8 source pixels. Screen-left/right brow heights produce +6.5/−2.2 source-pixel vertical translations, with +4/−2.24-degree rigid rotations.

**The independent downturned mouth corner is not implemented.** The existing positive corner-lift control is not a downward-corner control. The candidate does not misuse it, introduce an upward sneer, or substitute a purse. Every mouth control, side displacement, sampled lip-contour offset and central gap remains exactly neutral. This is a defensible, disclosed eye/brow approximation, not full fidelity to all of the reference's distinctive facial intent. Rigid eyebrow rotation also cannot reproduce every drawn contour.

Ordinary gaze, eye opening, eye smile, blush, inner-brow lift, hair motion, speech and all other excluded controls remain zero. No anatomy, artwork, shader, runtime, production registry, head or body acting is added by this candidate.

## Whole-transition aversion safety

Checking only the peak or only 30 Hz samples would be insufficient. I independently recomputed the timeline and reviewed the actual frozen runtime's smoothstep and scoped handoff rules.

- The five adjoining aversion-active segments are .6–1.0, 1.0–1.6, 1.6–2.4, 2.4–2.8 and 2.8–3.2 seconds. **Both endpoints of every one of these segments have both lids at least .18**, including the zero-aversion .6-second entrance and 3.2-second exit. No ordinary gaze, eye-smile or eye-opening conflict appears at either endpoint. Convex smoothstep interpolation therefore preserves this invariant over each entire segment.
- The initial .3-second restart blend is complete before authored aversion begins. Lids are established at .6 seconds, before the first lateral movement. Gaze reaches zero at 3.2 seconds, before the lids are released. The .8-second peak hold is exact.
- All 121 timeline poses match the independent calculation. Maximum control error is `2.6376485773305092e-08`. The tightest analytic aversion step bound is .875 source pixels per frame, below the .9 guard.
- All 252 recorded restart/release poses at nine interruption points match the separate lifecycle calculation. Maximum control error is `4.03578225283141e-08`. Direct release is tested from the interrupted active side-eye, rather than only after a restart has already centered the gaze.
- During the first half of a scoped handoff, ordinary supporting lids stay fixed while aversion decreases to exactly zero. Only in the second half do the ordinary channels blend. The restart target through .3 seconds has zero aversion and no conflicting channels. This supplies the continuous support argument; 216 additional mathematical boundary samples, including immediately before/after the halfway join, supplement the 252 recorded poses. These extra samples are model calculations, not additional runtime observations.
- Exact neutral is required during the opening and closing holds and after every completed release. The runtime probes' immediate continuity and reset checks are frozen evidence, not a claim of newly observed native motion.

## Numerical distinctness

I independently resampled all 36 frozen baseline profiles and seven later candidates at 121 normalized times, verified the comparison file hashes, and reproduced the recorded differences. All 43 trajectories differ from EXP-045. These comparisons use raw channel units, including pixel-valued aversion, so their RMS values are not perceptual similarity scores.

- **EXP-042 Cold glare:** frontal/bilateral rather than a lateral glance. Maximum raw control difference 12; RMS 1.3155826890.
- **EXP-081 Mild disgust:** mouth-led asymmetric lift/opening rather than a sealed neutral-mouth side-eye. Maximum difference 12; RMS 1.3097953125.
- **EXP-144 Caught staring:** wide-eyed alertness, blush, worried inner brows and embarrassed downcast recovery rather than a sustained irritated glance. Maximum difference 8.5020576132; RMS .6486889060.

Numerical nonduplication does not establish that viewers will perceive the intended emotion or that these candidates read distinctly at normal speed. Native inspection must address that question, especially given the omitted mouth corner.

## Reviewer-owned validation

`independent_review_validation.py` and `test_independent_review_validation.py` are separate reviewer artifacts. They do not import or overwrite author validators, source, profile, probes or the author freeze. The independent trust root is hardcoded:

- Author freeze SHA-256: `7f9e1bd006a91ff30d66b6da8231b4cb86e4b0bdd72162d9bc794401e51cc5ae`.
- Candidate SHA-256: `53f59fc53968bc626e0f3ead5e9f66f03e24d06c1a900106e442cc04dc28180d`.
- 38 author files, all 999 source files/184 PNGs in each preserved tree, additional manifest, registry, 993 approved41 runtime/artwork parity files, exact catalogue and nine source crops are checked.

The independent validator checks every static pose, every timeline pose, every lifecycle pose, actual sprite/shader iris displacements, lids, brows and neutral mouth. For future native evidence it requires current successful native receipts, 16 static RGBA images, 242 ordered motion RGBA images, exact dimensions, all frame hashes, equality to frozen poses/geometry, neutral/peak pixels, static-to-motion correspondence and unchanged pixels outside the face region. Missing images remain pending; malformed partial images fail. Once present, the MP4 must have the expected H.264/yuv420p 968 × 800 layout, 121 frames, 30 fps, ordered timestamps and approximately 4.033-second duration. Every decoded frame is compared to its same-index native full/detail panels and the all-frame face sequence. Identical or nearly identical held frames cannot be uniquely ordered through lossy encoding; that limitation is explicit.

Mutation tests cover unsupported adjoining zero-aversion boundaries, either unsupported lid, conflicting/excluded channels, false mouth corners, wrong iris sprite or shader displacement, numeric or geometry drift, frame/lifecycle reorder and omissions, unsafe direct-release blending, stale/rebased freezes, false native receipts, partial/bad dimensions or image modes, wrong RGBA hashes, neutral/peak/body drift, timestamps, frame counts, decoded truncation/extra frames, and material face reordering. Decoder mocks and synthetic test pixels are not native capture evidence.

Run from this directory:

    python -m unittest test_independent_review_validation -v
    python independent_review_validation.py

The validator exits 2 for incomplete native evidence, 1 for a failed check, and 0 only for complete machine evidence. No exit code grants artistic approval or claims normal-speed viewing. Its report is `independent_review_evidence/independent_review_checks.json`.

## Concurrent native-editor observation

The first full independent preparation audit passed with native evidence pending. While the authorized native operator opened the launcher, Godot reordered the existing `[editor]` section and normalized whitespace in `native_launcher/project.godot`. Its frozen hash `36aee2940f41d0dff851989e06f260a70805c295da9caba2583ac0663be43979` temporarily became `7873e47eaa50ac4dfbc4b693ea6125a893ae14373d6b2b3456c236135e170758`. The independent tests correctly rejected the stale input. The settings were independently compared and are semantically identical; the observation is preserved in `independent_review_evidence/freeze_change_observation.json`.

The parent directed the native operator to restore the exact frozen bytes only after the editor exits. No re-freeze or weakened acceptance rule is allowed. The reviewer did not edit this project or operate the native UI. The current machine result must be taken from the latest independent report after that restoration and any native capture, not inferred from the earlier passing preparation stage.

While restoration was pending, native evidence arrived. I viewed the native neutral and peak detail PNGs: the narrowed lateral gaze is visible, and the mouth remains neutral rather than matching the reference's downturned corner. A separately labeled partial native audit passed all 16 static images, 242 motion images, both receipts, all poses/lifecycle samples, image dimensions/RGBA hashes, neutral/peak holds, static-to-motion matching and fixed body pixels. It recorded 260 evidence-file hashes. This partial result is preserved in `independent_review_evidence/partial_native_checks_during_editor.json`; it does not waive the frozen-project mismatch. No MP4 existed at that partial audit, and I did not operate the UI or observe normal-speed motion.

## Final post-restoration result

The native operator exited the editor and restored the exact original launcher bytes. The hardcoded author freeze now passes unchanged. **All 54 reviewer tests pass. The final independent machine audit is `PASS_MACHINE_EVIDENCE_ONLY`, with no failed or pending checks.** The MP4 SHA-256 is `e323bd40288f1907033a94ad7a24418ecd9ace7e8e39dd2da609e2d61357bae7`. All 121 frames decoded cleanly at the required 968 × 800 / 30 fps / 4.033333-second format. Maximum same-index mean absolute error was 1.2952 for the full panel and 2.0660 for the detail panel; maximum expected-minus-best face error was .003644, below the .10 order threshold. All 260 native PNG/receipt file hashes are recorded, with the video hash separately recorded.

I additionally inspected all eight actual native detail anchors and the native peak bust. The narrowed/lateral eye progression and unequal brows are visible, recovery returns to the same neutral face, and the mouth stays neutral. These static inspections and complete numeric/pixel/decode checks do not constitute a continuous normal-speed viewing or an artistic/source-fidelity approval. The downturned-corner limitation and perceptual-distinctness caveat still apply.

**Decision:** proceed only as a disclosed, unapproved eye/brow approximation for native review. Do not claim the downturned corner is implemented, do not equate numeric distinctness with perceptual distinction, and do not label missing or unobserved native evidence a visual pass.

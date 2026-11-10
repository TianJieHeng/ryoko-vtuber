# EXP-161 Sleepy: independent native and MP4 review

## Decision

**Technical native/MP4 audit PASS; suitable for user review as an UNAPPROVED approximation.** The candidate's heavy partial lids read as drowsy, and the native sequence shows one sustained sink and recovery, without Fighting Sleep's repeated effortful reopening. It is visibly different from the available Sleepy Annoyance native peak: less brow tension, heavier lids and a parted mouth rather than a compact sealed pout.

**Material fidelity limitation:** the native mouth is a thin horizontal, tooth-visible slit. The EXP-161 reference has a softer, rounder dark opening. This preview therefore suggests sleepy/tired lips parting, but does not reproduce the reference mouth shape or anatomically relaxed jaw. At small scale the pale slit can also suggest a restrained toothy expression. Do not describe this as exact source fidelity or approved work.

No renderer, artwork, source reference or candidate adjustment was made during review. No user approval, production integration, publication or normal-speed playback observation is implied by the technical pass.

## Exact artifact and restored source

- Video: `Sleepy_review_v1.mp4`, **203,037 bytes**.
- SHA-256: `9ee4cbb7cee2dd79549363c472dd0ff7f0234e40282951745e90f921aef38475`.
- H.264, yuv420p, **968 × 800**, **121 frames at 30 fps**, **4.033333 seconds**. The left panel is the native 568 × 800 bust; the right detail is 400 × 360 at y=220.
- All **47 frozen author inputs** remain exact, including restored launcher `project.godot` SHA-256 `539521988aef23415cfba992334789a83b2fc03dac48c1c3982e259086011d6e`.
- Review-input freeze remains `4e223d817db9d3c57a5afccf105e147b27130571292c8215c5aab94cc0442490`; candidate remains `c260d3a88b6e3ed02877cf9f334de5e6e43f921f14c96f952b78193498b3486e`.
- Independently verified all 999 baseline/copied-rig files, 184 PNGs, both source manifests, 998 non-project launcher files, unchanged 36-profile disk registry, and all 993 runtime/artwork files against approved39 and approved40.

The operator preserved the editor's configuration-only rewrite and preliminary failed validator outputs in `native_review_audit/`, exited the editor and restored the frozen project. This reviewer made no UI/configuration change. The final audit below was freshly rerun after restoration, rather than excusing the earlier identity mismatch.

## Fresh independent checks

Executed:

    python independent_review_validation.py --output independent_native_final
    python -m unittest test_independent_review_validation -v

**87/87 independent technical checks PASS**, exit 0, zero pending categories and zero failures. **50/50 reviewer tests PASS** after native capture. Earlier combined Python execution passed 107/107 tests; no tests or implementation were changed for this native review.

Evidence: `independent_native_final/review_checks.json`, `native_frame_hashes.json`, `decoded_frame_order.json`, `comparison_evidence.json`, `independent_native_final.log` and `independent_native_tests.log`.

- The actual native receipts pass **1,590 static** and **12,125 motion** assertions, including **36 lifecycle assertions at nine interruption times**. Renderer/display fields identify a native X11 capture, not headless pixels.
- All **16 static PNGs** have exact names, dimensions and RGBA mode. Their geometry/state records match the frozen headless preparation. Every one of the eight bust/detail anchors matches its exact motion frame.
- All **242 motion PNGs** decode successfully with correct native dimensions and RGBA mode. All raw-RGBA hashes match their per-frame capture records. Exact 121-frame names, times, shared channel sets and poses pass independent checks.
- All 121 recorded poses and gaps match independent Sleepy-only smoothstep/geometry math; maximum control difference is **2.825701528319513e-08**. The five-channel scope, symmetric low brows and lids, 0.57 peak closure, 0.16 small opening, no repeated sag and reseal-before-final-lid-recovery are enforced.
- All pixels outside the bounded facial region remain unchanged across the full sequence. Actual full-view union difference bounds are **[209, 287, 356, 390]**. Hair, torso, costume, background and staging do not move.
- Exact neutral pixel holds pass for frames **0–6** and **111–120** in both views. Peak pixels are identical for **48–72 inclusive**. All eight static anchors align exactly with motion frames **0, 18, 30, 48, 84, 96, 105, 120**.

## Complete MP4 decode and order

Freshly decoded **all 121 frames**, with clean decoder exit, no stderr, correct size/rate/duration and monotonic 30 Hz timestamps. Every decoded full/detail panel was compared to its same-index native frame.

- Full-panel mean absolute RGB error: mean **1.29219**, maximum **1.29518** on the 0–255 scale.
- Detail-panel error: mean **2.03775**, maximum **2.06709**.
- Maximum same-index face-region error: **2.23122**.
- Maximum expected-minus-best all-frame nearest-face error: **0.002816**, below the 0.10 material-reordering threshold.

No material frame-order mismatch was found. Identical peak/neutral holds and nearly identical frames remain ambiguous under lossy encoding; the nearest-frame result is not claimed to uniquely identify every duplicate. The MP4 is a clean encoding of the captured sequence, not a newly synthesized performance.

## Actual pixel review

Inspected all eight native static face anchors, peak bust, the native Sleepy Annoyance detail comparator, nine decoded MP4 anchors, and all **121 native detail frames** in three labelled contact sheets. Those dense still images are not continuous playback.

The lids visibly descend while retaining a narrow amber eye trace at peak. The mouth starts sealed, becomes a small pale/tooth-visible opening, sustains, reseals, and returns to the exact neutral image. The face stays centered and symmetrical. I did not see a new contour jump or detached oral/lid fragment in the inspected still sequence. Existing small high-contrast hair/lash boundary details remain visible in the unchanged rig; this is not a general renderer cleanup pass.

The ordinary rigid lid/brow artwork does not recreate all drawn contours or shading from the reference. Brows remain more angular than the relaxed reference at some poses. The horizontal tooth-visible mouth is the clearest source mismatch. No chin descent, jaw rotation, breathing or body gesture was added to compensate.

Reference and comparator limits:

- **EXP-174 Sleepy Annoyance:** inspected the actual existing native peak PNG as well as its source sheet. Sleepy's mouth/eye/brow relationship is visibly different at peak. Exact comparator path/hash is recorded in `comparison_evidence.json`. This is a selected-pose comparison, not a fresh complete audit of EXP-174.
- **EXP-164 Fighting Sleep:** inspected its actual source sheet and frozen fifteen-key profile. Sleepy's single sustained open-lip sink is structurally distinct from that profile's sealed-mouth near-closure/reopening sequence. Matching historical native PNG/MP4 files were not available in this workspace, so **no native A/B playback comparison is claimed**.
- **EXP-177 Meditative Calm:** inspected its actual source sheet and frozen seven-key profile. Sleepy visibly retains partial eyes and opens the lips, unlike the profile's full closure with sealed mouth. Matching historical native evidence was not available here; **no direct native A/B comparison is claimed**.

The shared smoothstep still pauses velocity at its intermediate keys, and the held peak has no micro-motion. Dense still inspection and numerical monotonicity do not prove that the pacing feels natural at normal speed. No continuous temporally streamed playback observation was available to this reviewer. Any separate operator playback note should retain its own sampled-versus-continuous qualification.

## Delivery qualification

Safe description: **“Sleepy preview, using heavy lids and a small lip opening. The mouth shape is an approximation, and the jaw does not move.”**

Deliver the verified MP4 for the user's judgment. Keep EXP-161 **UNAPPROVED** until they accept it. Technical pass alone does not authorize integrating it as an approved expression or remove the disclosed mouth-shape and playback limitations.

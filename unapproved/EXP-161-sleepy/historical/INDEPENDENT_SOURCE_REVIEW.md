# EXP-161 Sleepy: independent source and preparation review

## Decision

**Suitable for a limited native preview; UNAPPROVED.** The frozen preparation passes the available independent source, scope, geometry and timing checks. No source-preservation or numerical blocker was found. Native pixels, perceptual fidelity, normal-speed playback and user approval are still **pending**, not passed.

The intended distinction is credible: one sustained heavy-lid sink with a small relaxed mouth opening, rather than Fighting Sleep's repeated effortful reopening, Sleepy Annoyance's sharp brow/pout tension, or Meditative Calm's closed eyes and sealed mouth. Those are source and control distinctions, not yet demonstrated native perceptual distinctions.

The key approximation is **lip separation, not anatomical jaw relaxation**. The existing rig provides no jaw rotation, chin descent, new relaxed lip outline or cheek deformation. The source's subtle brow contour changes also exceed a rigid vertical translation of the baseline brow. These limitations are disclosed rather than hidden by control names.

## Independently examined inputs

- Viewed actual pixels of the complete 1254 × 1254 EXP-161 nine-panel sheet, plus the full EXP-164 v002 Fighting Sleep, EXP-174 Sleepy Annoyance and EXP-177 Meditative Calm sheets. Exact paths and hashes are recorded in `independent_review_evidence/comparison_sources.json`.
- EXP-161 sheet SHA-256: `8284aa280149fd4a61cffd1d5f0fd35e0efbebce6310916d4b433cda1f30933a`.
- Independently checked the complete source catalogue hash, exact EXP-161 catalogue entry, all nine panel hashes and pixel-exact sheet crops. The sheet's panels differ slightly in height; the catalogue crop bounds, rather than an assumed uniform grid, are used.
- Reviewer-pinned preparation freeze SHA-256: `4e223d817db9d3c57a5afccf105e147b27130571292c8215c5aab94cc0442490`. All **47** frozen files match. The reviewer pins this hash independently, rather than trusting a modifiable adjacent checksum file.
- Candidate SHA-256: `c260d3a88b6e3ed02877cf9f334de5e6e43f921f14c96f952b78193498b3486e`. Read all eleven timeline keys, eight static anchors, capture probes, headless receipts, shared interpolation/control definitions and actual brow/lash/lip geometry formulas.
- Frozen baseline: **approved36**, published commit `3ce98774282ad6c20dfbd7018d20838ff861b762`. All **999** pinned source and copied-rig files, including **184 PNGs**, remain exact. Both manifests remain exact; the original 36 disk-registry entries remain unchanged and EXP-161 is absent.
- Launcher: all 998 non-project pinned files and both manifests remain exact. The intended `project.godot` name/main-scene override is separately included in the 47-file freeze.
- All **993** common runtime/artwork files independently match both approved39 and approved40. Six explicitly listed registry, metadata and aggregate-validation files are excluded. This does not claim registry equality across checkpoints.
- All 36 baseline trajectories plus six later candidates were sampled independently. Numeric nonduplication is established against all **42**, without treating mixed-unit control distances as perceptual distances.

## Source interpretation and bounded candidate

The actual sheet starts neutral. Upper lids become heavier together in the second panel, before obvious lip parting. The third through sixth panels show a small opening and sustained drowsiness; eyelids remain partly open rather than completely closed. Brows look relaxed relative to Sleepy Annoyance, although their drawn contour is not identical to the neutral brows. The last row releases the opening and lid droop toward neutral.

The source catalogue's sentence is: “Brows rest low; heavy upper lids droop; lips part slightly with relaxed jaw.” Its timing is a proposed, unimplemented 1.9-second reference schedule. This candidate is a **new four-second interpretation**, not recovered animation. It uses:

- 0.00–0.20: exact neutral.
- 0.60: low-brow/heavy-lid onset while lips remain sealed.
- 1.00: deeper droop and first slight parting.
- 1.60–2.40: uninterrupted held peak.
- 2.80 and 3.20: progressively gentler recovery.
- 3.50: lips resealed while a little lid droop remains.
- 3.70–4.00: exact neutral.

The unchanged cubic smoothstep has zero velocity at intermediate anchors. The descent is monotone, but is not claimed to be constant-speed or to have nonzero velocity across every join. All eight static anchors are exactly on the 30 Hz sampling grid. There is no extra reopening/sag cycle.

Only five channels act: equal screen-left/right brow lowering, equal ordinary blink values and mouth opening. Peak values and geometry are:

- Brows −0.22 / −0.22: **2.2 source pixels downward** each, zero rotation and zero inner lift.
- Lids 0.57 / 0.57: **20.52 source pixels** of upper-lash travel each. Character-side `blink_R` controls screen-left; `blink_L` controls screen-right. Equal values are intentional, not an asymmetry test inherited from Mild Disgust.
- Mouth opening 0.16: `54 × 0.55 × 0.16 = 4.752` source pixels of lip separation, or **2.32848 bust pixels** at scale 0.49. The upper contour remains at its neutral offset; the lower contour receives the same offset at the tested left/center/right positions. Mouth endpoints have zero horizontal movement, and the nominal source width remains 71 pixels.

There is no purse, lip pressure, corner bias, smile, smile-eye, brow tilt/inner lift, gaze shift, head/body movement, hair motion, breathing, speech or effect. The paired BOD-019 sleepy lean and BOD-038 relaxed weight-shift reference gestures are not implemented. Aperture math is not a measurement of visible cavity, tooth, jaw or chin anatomy.

## Distinction from the nearest expressions

**EXP-164 Fighting Sleep:** The actual v002 sheet visibly alternates drooping/near-closed eyes with effortful reopenings and a sealed mouth. Its published 3.47-second profile has a first 0.70-lid sink, a reopening to zero, a second 0.33-lid sink and a second reopening, plus brow inner lift up to 0.55, opposing tilt up to ±0.80 and purse up to 0.20. Sleepy instead holds partial lids at 0.57 with opening 0.16, no brow effort/tilt or purse, and no rebound. Normalized-time maximum control difference: **0.80**. Sustained-open-lip drowsiness versus effortful repeated recovery must still be judged at normal speed on native output.

**EXP-174 Sleepy Annoyance:** The actual sheet develops strongly knitted/angled brows and a sealed pout. Its profile reaches brows −1/−1, tilts +1/−1, lids 0.40/0.40 and purse 0.75. Sleepy uses much gentler untilted low brows, somewhat heavier partial lids and small open lips. Maximum control difference: **1.0**. The rigid baseline brows may still look mildly stern; native inspection must confirm the overall expression reads relaxed rather than annoyed. Neither candidate literally implements the source's lower-lip projection.

**EXP-177 Meditative Calm:** The actual sheet closes both eyes completely while keeping lips sealed. Its 3.9-second profile uses only ordinary bilateral blink, reaches 1.0 at 1.20 seconds and holds closure through 2.35. Sleepy retains partial eyes, lowers the brows slightly and parts the lips. Maximum normalized-time control difference: **0.6306401802554871**. Half-lidded recovery frames can resemble one another in isolation; the peak mouth/eye relationship and the complete sequence are the relevant distinction.

These measured differences are not a perceptual score. Native images of Sleepy do not yet exist at this review checkpoint, so no native A/B or readability pass is claimed.

## Independent validator and mutation tests

`independent_review_validation.py` is a **separate** read-only reviewer implementation derived from the prior EXP-081 evidence scaffold. It does not overwrite or import the author's frozen review validator. Sleepy-specific geometry is reduced to its actual five-channel subset: rigid vertical brows, bilateral ordinary lash travel, unchanged mouth width and stationary-upper/constant-lower lip separation. No inherited disgust corner-bias, purse, asymmetric-lid, suppressed-mouth or off-grid-anchor assertion is treated as Sleepy's desired result.

Run from this directory:

    python independent_review_validation.py
    python -m unittest test_independent_review_validation -v

Default reviewer reports go to `independent_review_evidence/`. An output destination inside capture, motion, rig, launcher or development-audit input trees is rejected. No native UI, renderer, Godot process, encoder, publication or external service is launched. The validator can only decode an **existing** MP4.

Current result: **PENDING, exit 2**, with **33/33 available checks passing**, zero failures, and three pending categories (native static, native motion and MP4). Independent recomputation matches all 121 motion poses/gaps; maximum smoothstep control error is **2.825701528319513e-08**. Eight static geometry records match separate Sleepy-only formulas. The author's 1,558 static, 11,640 motion and 36 lifecycle assertion receipts are hash-bound and checked; those are not misrepresented as fresh native evidence.

**50/50 reviewer tests pass; 107/107 combined Python tests pass.** Tests cover malformed/nonfinite times and poses, wrong frame count/order, missing channels, too-large opening, premature lip parting, asymmetric/full lids, repeated sink/rebound, bad brow depth/rotation, prohibited inner lift/tilt/pout/smile/pressure, peak/neutral/reseal timing, static lash/lip/scale/width errors, dimensions and RGBA mode, body-region changes, freeze forgery including checksum-sidecar forgery, candidate hash drift, failed/forged native receipts hidden by missing files, unexpected native filenames, and protected output paths. Synthetic decode tests check full stream consumption, byte order, truncated-frame rejection, retained decoder failure and material nearest-frame swaps; identical holds remain explicitly ambiguous. Synthetic fixtures are temporary test data and never count as native artwork evidence.

When native evidence arrives, the same validator checks:

1. All 16 exact static PNG names, 568 × 800 bust and 400 × 360 detail dimensions, RGBA mode, file/pixel hashes, frozen geometry records and input hashes; exact neutral return and fixed body/outside-face pixels. Static PNG hashes are recorded by the reviewer and cross-bound to the aligned motion frames, not falsely described as capture-receipt hashes when the static receipt has no such fields.
2. All 121 full plus 121 detail native frames and every receipt-bound raw-RGBA hash; exact numbered filenames, 121 time/pose records, native display/renderer identity, 12,125 native motion assertions and 1,590 native static assertions, 36 lifecycle checks and unchanged baseline.
3. Exact neutral pixel holds through frame 6 and from frame 111, nontrivial acting pixels, fixed body pixels, and identical sustained peak frames **48–72 inclusive**. All eight static anchors compare exactly with their matching motion frame: 0, 18, 30, 48, 84, 96, 105 and 120.
4. Complete existing H.264 MP4 decode at 968 × 800, yuv420p, 30 fps, all 121 frames, approximately 4.033 seconds, monotonic 30 Hz timestamps and clean decoder exit. Every decoded full/detail panel is compared to its same-index native source, plus all-frame nearest-face errors for material reordering. Lossy identical or near-identical holds are expressly not uniquely order-identifiable.

## Pending native gate

At this source-review checkpoint, all 17 required static files including the receipt, all 243 required motion files including the receipt, and the MP4 are absent. This is pending evidence, **not a denied action** and not a failed source-preparation result. No native dimensions, seams, oral cavity, moving-lid pixels, normal-speed timing or perceptual distinction has passed.

The authorized native operator should capture the frozen launcher without changing the candidate, source, runtime or renderer, then run this independent validator and inspect both bust/detail output. Preserve any failed capture and project rewrite rather than overwriting history. Key visual questions are whether 0.57 lids still show enough eye to read drowsy, whether the tiny lip opening looks relaxed instead of speech/surprise, and whether the gentle unchanged brows avoid Sleepy Annoyance. Keep the candidate UNAPPROVED until the user reviews it.

# EXP-096 Headache tension: independent native review

**Technical result: PASS. Visual interpretation: restrained tense closure, with material source-fidelity limits. Approval: UNAPPROVED.**

This addendum supersedes the earlier source review's statement that native evidence was absent. It does not change the frozen candidate, erase that historical checkpoint, or turn technical success into visual/user approval.

## Evidence inspected

The reviewer inspected the actual EXP-096 source sheet and peak panel, all eight native detail anchors, native bust neutral/build/peak/relaxation views, and the decoded MP4 keyframes. Native Silent Fury and Sleepy Annoyance peak pixels, plus the verified existing Meditative Calm full/detail closed-arrival capture, were also viewed. The Fury and Sleepy Annoyance neutral detail images are pixel-identical to this candidate's neutral detail, so those comparisons share the same visible baseline.

The final MP4 is `Headache_tension_review_v1.mp4`, SHA-256 `2b410146ed28ec4d6240e3e47c6b6f27d9c33b1a8087c101941da9a6a2d58716`, 197,614 bytes. It is H.264/yuv420p, 968 × 800, 30 fps, 121 frames and 4.033333 seconds. It places the native 568 × 800 bust at left and native 400 × 360 detail at right.

The independent validator ran against the same pinned 38-file author freeze, SHA-256 `6f076e4127e9c07d4083c6a26560ce32dfcb25a9d9c7981ad0401d291a509520`. No profile, renderer, configuration, artwork or production file was changed. This reviewer did not invoke a UI, renderer or encoder. The supplied capture receipts report 1,838 static and 16,745 motion checks.

## What the native pixels actually communicate

The eyes progressively become heavy, close completely, hold closed, and reopen after the brow/mouth tension has relaxed. Both eyes visibly close with no iris sliver at the peak. The mouth remains sealed and does not turn into a smile, show teeth or open into a grimace. The small inward brow tilt and slight pressed-mouth treatment support a restrained, inwardly tense pause.

The peak is **not an unmistakable headache/pain expression**. Compared with the actual source peak, the native forehead stays smooth and the central brow knit is much weaker. The source has visibly converging, shaped brows and central crease cues; the rig supplies only lowering and rotation of existing rigid brows. The tiny purse/pressure changes keep the mouth compact, but do not reproduce the source's genuine small downturned corners. No furrow, brow convergence or independent corner anatomy should be claimed.

At detail scale the peak's lower/inward brows are distinguishable from the later still-closed softened pose. At normal bust scale that difference is restrained and the closed-eye shape dominates. Peak-to-softening changes occupy 797 bust pixels and 3,288 detail pixels; this confirms a real change, not strong semantic readability. The native sequence reasonably reads as tension followed by release, but it could also be read as tired irritation, concentration or a deliberate pause. Missing pain-specific detail remains a material limitation, not a technical defect hidden by passing numbers.

The source's important ordering is preserved: frame 84 at 2.8 seconds is still fully closed after the brows and lips have softened. Only then does reopening proceed. The source itself becomes calm-looking during this recovery, so similarity of the late closed recovery frame to calm is expected.

In the inspected anchors and encoded keyframes I saw no new mouth opening, iris leak at full closure, gross facial displacement or body movement. Small existing hair/eyelash compositing edges remain visible in detail; this is not a declaration that the shared art has flawless edges. Native neutral comparator equality and fixed-body checks isolate the candidate's changes rather than treating all baseline edges as new defects.

## Comparison findings

- **Silent Fury (EXP-043):** the actual native peak has open eyes and stronger brow opposition. Headache's sustained complete closure is an obvious visual difference. Both reuse similar brow and pressed-mouth components, so the difference should be described as closed, inward tension rather than a newly modeled pain face.
- **Sleepy Annoyance (EXP-174):** the actual native peak keeps heavy eyes partly open and has a considerably more puckered, visibly curved pout. Headache is fully closed with a much smaller mouth adjustment. These two peak images are distinguishable in native detail and bust view, though early heavy-lid build frames have some shared mood.
- **Meditative Calm (EXP-177):** the actual reference sheet, approved profile and existing native full/detail closed-arrival capture were inspected. Calm has relaxed brows and a softer neutral mouth with the same closed-eye contour. Headache's lower/inward brows and pressed line make its peak modestly tenser, not dramatically pain-specific. Compared with Calm, Headache peak changes 829 bust / 3,372 detail pixels, while softened closure changes only 438 / 1,782. The late recovery's close visual proximity to Calm is therefore visible, expected and explicitly retained as a caveat. This is a verified single-anchor comparison, not an all-frame or normal-speed Meditative Calm comparison.

The Meditative Calm comparator is `stunned_silence_work/runtime_parity/baseline/EXP-177_full.png` and `EXP-177_detail.png`. The adjacent harness resets, plays EXP-177, disables automatic blink and advances to 1.2 seconds. Both baseline/patched receipts pass (98/122 checks); the RGBA hashes match their PNGs and both variants are pixel-identical. The profile in both harness source roots and the current Headache rig has approved SHA-256 `4fb88990455fc4ba799e30ce2987b17151fe0ca00d31e562aa38680a7349f211`; at 1.2 seconds it has blink_L=blink_R=1 and all other channels zero. This establishes useful historical single-anchor native evidence. It does not claim a fresh current render or a capture-time profile-hash field that the old receipt did not record. Full verification is in `independent_native_review_evidence/meditative_comparator_verification.json`.

Native comparison peak SHA-256 values:

- `silent_fury_work/capture/silent_fury_detail.png`: `6e77840c6052bfdec2134a1c9da2ad12a191a7e25adbeca379d64bf813ec2368`.
- `sleepy_annoyance_work/capture/sleepy_annoyance_detail.png`: `582af8a1bd08ae2afb57546a103836eac497b5abfa4132ba91d73ed672cb84a7`.
- Meditative Calm full PNG: `5b54bf5889556532e6560cbcee2330b2127e1eba49fd6d95e4c574710b28b883`; detail PNG: `161db33a9b7fc15b17cb32ba9cf23ede2295a2531942ac52ae74853808fe929b`.

## Independent technical results

`python independent_review_validation.py --output independent_native_review_evidence` returned **PASS, exit 0, 96/96 checks, zero failures and no missing technical inputs**.

The checks confirm:

- All frozen source, runtime, artwork, author-input and source-reference identities still match; the candidate remains absent from the production registry.
- All 16 static images and 242 ordered native motion images exist at exact RGBA dimensions. Every motion RGBA hash matches the native receipt. All eight static anchors match their corresponding motion frames exactly.
- Independent full-pose trajectory, geometry and 252 lifecycle-sample checks still pass. The native poses equal the headless poses.
- Exact neutral holds at frames 0–6 and 111–120, exact peak hold at frames 48–72, and exact pixel neutral return in both views.
- All full-view changes lie within bounding box [209, 287, 356, 388]. Every pixel outside the fixed face box [200, 270, 360, 410] remains unchanged, including hair outside that box, body, clothing, background and framing.
- Complete MP4 decode of all 121 frames, clean exit code 0 and empty error output. Every presentation timestamp matches 30 fps; each decoded full/detail panel is compared with the corresponding native frame.
- Maximum same-index panel error is 1.294667/255 for bust and 2.069561/255 for detail. Maximum face error is 2.238965/255. Maximum same-index versus best-matching-frame excess error is .011181, below the .10 material-reorder threshold. No material frame reorder is detected. Identical and near-identical hold frames remain ambiguous under lossy encoding.

The 72 reviewer tests were rerun after native evidence arrived and pass. Those test fixtures are not additional native captures. The native validation above uses the actual supplied PNGs and MP4.

## Review boundary and disposition

Full computational decoding and ordered native/encoded image inspection are complete. **Continuous normal-speed playback was not independently observed by this reviewer.** No UI was invoked, consistent with this assignment. Neither all-frame decoding nor a contact sheet substitutes for watching the temporal feel at normal speed.

The result is technically suitable to show for user evaluation, with the stated restrained-tense-closure interpretation and missing furrow/convergence/corner limitations. It is not a source-faithful pain reconstruction and is not approved for integration or publication by this report. A normal-speed visual decision remains separate from the successful technical checks.

Evidence: `independent_native_review_evidence/review_checks.json`, `native_frame_hashes.json`, `decoded_frame_order.json`, `static_faces.png`, `encoded_keyframes.png`, `bust_progression.png`, `independent_native_review.log` and `independent_native_reviewer_tests.log`.

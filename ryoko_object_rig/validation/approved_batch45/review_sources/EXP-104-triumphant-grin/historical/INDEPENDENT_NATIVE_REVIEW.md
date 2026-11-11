# EXP-104 Triumphant Grin: independent native review

## Result

**Technical native/video validation PASS. Suitable to present as an UNAPPROVED review candidate, with the restrained-intensity and dental-shape limits below.** This is not user approval or a production-integration decision. Normal-speed continuous observation was not performed by this reviewer.

The final run used the restored author contract SHA-256 `40f54ee01529ef96d18404cd2f3ebb1e2bf3004662cf2c45055434fb063aef7a`. All author-frozen inputs, the source artwork, baseline/rig files and launcher override match that contract. The operator owned native capture, configuration restoration and encoding. This reviewer performed no UI operation, renderer launch, source/profile edit, encoding or publication.

The initial `INDEPENDENT_SOURCE_REVIEW.md`, `independent_source_review_checkpoint.json` and `INDEPENDENT_REVIEW_FREEZE.json` remain unchanged historical preparation checkpoints. Their then-pending native stage is superseded by this separate native review, not retroactively rewritten.

## Actual pixel inspection

I inspected the actual EXP-104 nine-panel source sheet and all eight native static detail anchors, native full-bust progression, individual shallow/open-grin detail captures and the decoded MP4 keyframe contact sheet. I also inspected actual historical native comparison images for EXP-114, EXP-152 and EXP-001, individually and side by side. These were image inspections, not normal-speed video playback.

The native sequence has a centered tooth-bearing grin, symmetric acting controls and direct, visibly open eyes. Both brows move into the intended lowered/inward relationship without an independent raised inner brow. The shallow peak exposes a narrow white tooth strip; the later open grin makes the dark opening below it visibly larger. Recovery reduces the mouth aperture and reseals before neutral. The full-bust frames retain the same identity, hair, costume, pose and camera framing. The inspected keyframes do not show a gross new open lip seam or displaced tooth strip.

**Source-fit limitation:** the native grin is noticeably more restrained and narrower relative to the face than the energetic panel-5/panel-6 source grin. The brow/eye change is also subtler at bust scale. It reads as a controlled confident grin; the stronger “triumphant” intensity remains a user-facing judgment. This review does not claim literal reproduction of the source's expression strength or anatomy.

**Dental limitation:** visible native enamel is now confirmed, rather than inferred from a node visibility flag. However, this is an existing upper-tooth-supported, shallow open grin. It is not an exact clenched-teeth shape or independently modeled opposing tooth rows. The narrow shallow strip and more open follow-through should not be advertised as a true sealed dental clench. No new dental, cheek or jaw anatomy was introduced.

Fine existing lash/hair intersections and the shared rig's tooth/lip styling remain visible. The inspected anchors do not establish defect-free pixels at every instant; all-frame numerical/image checks and sampled human visual inspection have different scopes.

## Comparison with approved neighbors

The comparator PNGs come from the historical `stunned_silence_work/runtime_parity/baseline` native run: EXP-114 at 1.20 s, EXP-152 at 0.75 s and EXP-001 at 1.02 s. Their RGBA hashes match that run's receipt; full/detail dimensions match; and the three profile files are byte-identical to the frozen approved36 profiles. Historical patched counterparts have identical pixels. These are existing prior24 native parity anchors, not freshly captured comparison movies or a new current-baseline all-frame parity claim. Exact provenance is recorded in `independent_native_review_evidence/comparator_provenance.json`.

- **EXP-114 Daring Provocation:** this is the closest visual neighbor. Its native anchor has unequal eyelid narrowing and an upward-biased screen-right mouth corner, giving a crooked challenge. EXP-104's lids and grin are more even, and its later opening is centered. The difference is visible side by side, but modest at small bust size. Strong whole-sequence perceptual discrimination has not been demonstrated.
- **EXP-152 Private Pride:** its native anchor is visibly downcast and closed-mouth. EXP-104 keeps forward eyes and visible teeth. This distinction is clearer than the distinction from EXP-114.
- **EXP-001 Bright Welcome:** its native anchor has raised brows, more open eyes and a much larger mouth aperture. EXP-104 is lower-browed, more focused and shallower. The native anchors support the intended contrast.

The previously verified nonduplicate control trajectories remain supporting numerical evidence, not perceptual scores. User review of the full performance is still needed.

## Final independent checks

Command:

    python independent_review_validation.py --output independent_native_review_evidence

Result: **exit 0, PASS, 94 top-level checks, zero failures, zero pending items.**

- Native static receipt: PASS, 1,614 checks, exactly 16 PNGs.
- Native motion receipt: PASS, 13,131 checks, exactly 121 full and 121 detail frames.
- All native images have the required RGBA mode and dimensions: full/bust 568 × 800, detail 400 × 360.
- All 242 motion RGBA hashes match their native receipts. All eight static anchors match the corresponding motion frames exactly in both views.
- The independent expression-specific pose/geometry/trajectory contract passes. Every native pose matches the frozen headless counterpart. Shallow-grin frames 48–60 hold exact pixels.
- Initial/final neutral holds and bookends are pixel-exact. All full-view changes remain inside the fixed face region. The measured full-view change union is `[209, 287, 356, 393]`; the detail-view union is `[34, 64, 333, 279]`. Body, hair, costume and background outside the reviewed face region remain unchanged across every captured frame.
- All baseline/source/manifest/registry guards pass, including the 999-file source/rig freezes and 993 common runtime/artwork files against approved40 and approved41.
- All 58 reviewer mutation/guard tests pass again after native capture. The earlier combined 105-test run remains recorded; it was not re-labeled as a new post-capture run.

## MP4 integrity and limits

File: `TriumphantGrin_review_v1.mp4`

SHA-256: `caa4914959146c87fa371a17e829ca3c5d85b4db4a273b341f62781a8b33d17b`

The independent validator fully decoded all 121 frames with exit code 0 and empty FFmpeg error output. H.264/yuv420p, 968 × 800, 30 fps, approximately 4.033 seconds and all frame timestamps pass. Every decoded full/detail panel was compared to its same-index native input. Maximum mean absolute RGB error is 1.29421 for the full panel and 2.06922 for the detail panel. Maximum expected-face error is 2.23446; maximum expected-minus-best frame-match error is 0.00638, below the 0.10 material-order threshold.

This confirms a complete decodable video faithful to the captured panels, with no material frame-order mismatch detected. Lossy encoding and pixel-identical/near-identical holds make swaps of indistinguishable frames inherently ambiguous. Full decode and contact-sheet inspection do not substitute for watching the four-second performance continuously at normal speed.

## Handoff

The preview may be delivered for review with the clear description “a restrained, centered triumphant-grin interpretation using the existing shared rig.” Preserve the narrower expression and non-clench limitations. No further source/profile change is recommended solely to conceal those limits, and no new user approval or production readiness is inferred.

Evidence:

- `independent_native_review_evidence/review_checks.json`
- `independent_native_review_evidence/native_frame_hashes.json`
- `independent_native_review_evidence/decoded_frame_order.json`
- `independent_native_review_evidence/static_faces.png`
- `independent_native_review_evidence/bust_progression.png`
- `independent_native_review_evidence/encoded_keyframes.png`
- `independent_native_review_evidence/native_comparator_faces.png`
- `independent_native_review_evidence/comparator_provenance.json`

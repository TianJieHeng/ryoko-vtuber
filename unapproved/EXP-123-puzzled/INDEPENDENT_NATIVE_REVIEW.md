# EXP-123 Puzzled: independent native and MP4 evidence review

## Result

**PASS for the independent evidence checks; candidate remains UNAPPROVED.** All **73 checks** pass with no failed or pending input stages, and all **16 validator tests** pass. The full native/MP4 path has now been exercised on the actual EXP-123 capture, not synthetic fixtures.

This establishes capture integrity, numerical consistency, preservation, and video correspondence. It does not turn the approximation into a source-faithful diagonal/translated pout, establish normal-speed continuous observation, or authorize approval, integration, or publication.

## Evidence reviewed

- Native static receipt: **1,526 assertions, PASS**; eight anchors × two views.
- Native motion receipt: **9,387 assertions, PASS**; 121 frames × two views, sampled at 30 Hz over 0–4 seconds.
- All 16 stills have exact native dimensions and RGBA mode. All 242 motion images have matching receipt hashes, exact expected filenames, dimensions, and RGBA mode.
- Native full/bust: **568 × 800**. Native detail: **400 × 360**.
- Native renderer receipt: non-headless X11/llvmpipe. This reviewer read the captured evidence and did not launch the renderer or UI.
- Review MP4: `Puzzled_review_v1.mp4`, **968 × 800**, H.264/yuv420p, **30 fps**, **121 decoded frames**, **4.033333 seconds**, **182,736 bytes**. The slightly longer video duration includes both endpoints of the four-second sampled performance.
- MP4 SHA-256: `5df48deb24bc3a86084799084fd65a004bd7b4af4459ed1eea6d838225930db3`.

Every recorded native pose matches the corresponding headless pose. The independent interpolation and source-specific intent checks pass. All peak-hold frames 42–57 are pixel-identical within each view. Exact static/motion identity passes at true grid-aligned anchors: neutral, puzzled, reconsider, and neutral return. Non-grid-aligned anchors were not incorrectly compared with the nearest sample.

Neutral frames 0–6 and 111–120 match exactly within each native view, including the final return. Maximum changed-pixel count is 1,886 at bust size and 7,609 at detail size. The union of changed pixels is `[209,287,356,389]` in the bust and `[34,64,333,272]` in detail, using exclusive right/bottom coordinates. All bust pixels outside the defined face box remain unchanged.

## MP4 correspondence

The whole video decodes cleanly. All 121 presentation timestamps match the expected monotonic 30 fps sequence. Same-index native/decoded panel comparisons have maximum mean absolute errors of **1.29321/255** for the full panel and **2.05292/255** for detail. The maximum expected-versus-nearest face error excess is **0.007412/255**, below the validator's material-reorder threshold.

This is strong correspondence evidence, not proof of unique ordering among visually identical or near-identical frames. For example, the held peak can match multiple native frames equally well, and lossy encoding can make an adjacent soft-release frame marginally nearer. No temporal viewing or normal-speed pacing claim follows from that math alone.

## Pixel inspection and source assessment

I opened the actual native static-face sheet, native bust progression, decoded MP4 keyframe sheet, and the native puzzled detail image. I also opened the existing Mental Arithmetic `left_lift_up_detail.png` for a limited still comparison. These are actual image observations, not claims derived only from control values.

The candidate visibly develops an asymmetric questioning/skeptical face: the screen-left inner-brow region becomes flatter/higher relative to its neutral slope, the opposite brow stays lower, and the screen-left eye narrows more. The reconsideration image narrows the eyes further while retaining the question. The lip contour stays closed in the inspected static and decoded keyframes; no obvious new open-cavity or split-lip defect appears in those inspected views. The bust sequence keeps head, hair, shoulders, and clothing fixed, also supported by the all-frame pixel check.

The most conspicuous mouth change is a **compact, downturned/curved sealed pout**. The sideways bias is subtle even in detail and is not a clearly translated mouth at bust size. The painted source's diagonal lip line and head tilt are absent. This confirms, rather than removes, the main limitation from `INDEPENDENT_SOURCE_REVIEW.md`. “Small width-biased sealed pout” is accurate; “faithful sideways/diagonal pout” is not.

The inspected Mental Arithmetic still has a different brow/eye relationship from the Puzzled peak, consistent with the different controls and upward-gaze beat. That is a limited detail-still distinction, not a side-by-side review of both whole performances. Perceptual overlap with generic skepticism, displeasure, or other existing narrowed-eye expressions is not fully settled. No complete all-profile visual comparison was performed.

## Frozen-input restoration audit

The permitted editor import reordered the existing `[editor]` and `[rendering]` sections and blank lines in the separate launcher's `project.godot`, without changing any values. The initial independent validator correctly failed the byte-freeze check rather than silently accepting the rewrite.

After the capture worker confirmed that the game stopped, the project editor exited, and its embed setting was restored, the parent directed a configuration-only exact restoration. This reviewer archived the editor-saved bytes and failed reports, reconstructed the documented prepared launcher configuration from the frozen source, verified its expected hash, and restored exactly those bytes. No candidate, probe, runtime, shader, source image, or capture evidence was changed.

- Restored launcher SHA-256: `021475e8c28f882460ca070520dcdb7f2b1f5e3fe919aec354d9105ed99d5dfd`.
- Original review-input freeze remains unchanged: `d715fd00b418e2f4f60e886477e95844433f1c5312460fd090bfe4d63406d6ef`.
- Audit: `review_evidence/launcher_import_audit/`, including saved project bytes, the exact diff, initial failed report, full-evidence failed report, and `restoration_receipt.json`.
- Final `review_evidence/review_checks.json`: **PASS, 73/73**, no pending stages.

Fresh final hashing still confirms all **999 pinned files / 184 PNGs** unchanged in both source and candidate rig, the extra approved manifests, reference sheet/catalogue/panels, all frozen candidate/probe inputs, and the intentionally separate approved36 registries. This is not approved39 integration parity.

## Remaining acceptance limits

- **Normal-speed continuous observation was not performed by this reviewer.** Contact sheets, complete decode, frame ordering, and isolated image inspection are not substitutes. The report's observation flag stays false.
- Source fidelity remains intentionally partial: rigid brows, fixed head/body/gaze, symmetric vertical purse contour, and approximately two-source-pixel outline midpoint bias rather than translated/diagonal lips.
- Live interaction, natural blink blending, lip-sync combinations, graphical lifecycle interruptions, and later integration are not established by these isolated native recordings.
- If a genuine shifted/oblique pout is mandatory, that requirement remains unmet despite technical PASS.

The artifacts are ready for explicit visual review with those limits disclosed. No approval, registry integration, CI, publication, or external delivery was performed by this reviewer.

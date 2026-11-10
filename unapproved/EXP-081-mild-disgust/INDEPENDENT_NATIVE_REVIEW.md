# EXP-081 Mild Disgust: independent native review

## Decision

**Technical evidence PASS, 79/79 checks. Expression remains UNAPPROVED.** All native capture, frozen-input preservation, pose, pixel-hash, anchor, neutral/body and complete-video checks pass.

**Source fidelity is limited, not passed as unambiguous disgust.** In the actual native detail and bust images, the peak reads more readily to this reviewer as a restrained tooth-showing smirk or skeptical objection than the source's one-sided upper-lip disgust. The slightly upturned, thin mouth and unequal narrowed eyes are visible, but the source's stronger upper-lip-only rise/curl is not. The common-corner limitation identified before capture is visible in the result rather than merely theoretical.

This is a usable review preview of the disclosed approximation, not approval to describe it as a faithful anatomical reproduction. User acceptance of that compromise is still needed. No UI, native renderer, encoder, production integration or publication was invoked by this reviewer, and no candidate profile, rig, artwork or frozen input was changed.

## What was actually inspected

- Previously inspected the actual nine-panel EXP-081 source sheet and all linked panel identity/crop checks. Referred to that source during this native review, rather than using the catalogue sentence alone.
- Opened native neutral, peak and suppressed detail images and the peak bust directly.
- Inspected the complete eight-anchor native detail contact sheet, nine selected decoded MP4 detail frames, and native bust progression at frames 0, 30, 42 and 65.
- Opened additional native detail frames 34, 38, 58 and 62 to examine mouth opening and closure around the brief peak.
- Compared with the actual Bitter taste and Queasy source sheets and their existing native peak-detail captures, inspected during source review. Those prior images are comparative context, not newly recertified expression packages.
- Independently decoded and numerically compared **every one of the 121 MP4 frames**, not only the contact-sheet selections.

This is static/sequential pixel inspection plus full decode and numerical timing checks. **Continuous normal-speed observation was not performed by this reviewer.** Neither the native receipt nor the independent validator claims it was.

## Visual findings and limits

### Mild Disgust versus its source

The candidate visibly narrows the screen-left eye more than the screen-right eye, and slightly lowers/tilts the brows. The mouth opens briefly into a thin white tooth-bearing band, then closes while the narrowed eyes persist. The sampled release returns to the exact neutral state.

The source peak has a stronger slanted one-sided upper-lip gesture. The native peak's mouth remains close to horizontal at bust scale, with a subtle corner rise rather than an isolated upper-lip curl. Its lower lip follows the common corner. That supports an understated objection but leaves a smile/smirk interpretation plausible. At bust scale the mouth gap is only about 2.56 pixels, so the anatomical distinction is especially weak.

The closed-mouth suppression reads as reserved or mildly displeased. That does not independently establish disgust. No nose wrinkle, cheek tension, head recoil or body gesture appears, as expected from the frozen control scope. The reviewer therefore does not award a source-fidelity or perceptual-distinctness pass from numerical nonduplication alone.

### Compared with Bitter Taste and Queasy

Bitter Taste's prior native peak has a larger, more visibly open mouth and stronger bilateral narrowing/brow lowering. Mild Disgust's smaller opening and unequal eyes are visibly different in the inspected stills, but the shared frozen mouth construction means both are approximations of their painted source anatomy. “Different from Bitter Taste” does not by itself make this recognizable disgust.

Queasy's prior native peak stays closed and strongly pursed, with different worried-brow controls. Mild Disgust's tooth-bearing peak differs visibly. During the closed-mouth portions, both still use the same underlying half-lidded facial artwork, so no categorical emotion distinction is claimed from that overlap.

### Render quality and preservation

The sampled native frames retain coherent face placement and the intended opening/closure progression. The mouth exposes a very thin, segmented white strip rather than a newly articulated sneer. Existing sharply rasterized lash/hair intersections remain visible in both neutral and acting states. This review does not relabel those inherited geometric/raster limitations as a new anatomical solution or claim a defect-free redraw.

Every native body/background pixel outside the tested face box is unchanged. No hair, head or body movement is being used to suggest disgust. These conclusions are supported by all-frame comparisons, not only by visual still inspection.

## Complete technical verification

Final command:

    python mild_disgust_work/review_validation.py --output mild_disgust_work/native_review_evidence

Result: **PASS, 79/79 checks, no failures or pending technical checks.** The 32 independent validator unit/mutation tests were rerun after capture and all pass. The earlier combined run passed all 63 tests.

- Native static receipt: **1,558 checks**, no failures, eight records equal to the frozen headless records. All **16 static PNGs** have exact expected filenames, RGBA mode and dimensions: 568 × 800 bust, 400 × 360 detail. Each file/raw-pixel hash is recorded.
- Native motion receipt: **11,815 checks**, no failures, **121 frames at 30 Hz**, duration 4.0 seconds, **36 lifecycle assertions** at the specified nine interruption times. Provenance reports X11 and `llvmpipe (LLVM 19.1.7, 256 bits)`, not headless.
- All **242 motion raw-RGBA hashes** match the capture receipt. Every frame's pose and time matches the frozen headless evidence and independent interpolation math. All excluded controls remain zero.
- Six exact static/motion anchors match in both views: neutral 0, detect 18, recoil 30, peak 42, release 81 and neutral return 120. Half-frame suppress/settle anchors are not falsely compared with nearby nonidentical samples.
- Native frames 0–6 and 111–120 are exact neutral. Peak frames 42–52 are pixel-identical. The native first/last images are identical in both views.
- Native changed-pixel union is `[209, 287, 356, 391]` in full view and `[34, 64, 333, 274]` in detail. At the peak, 1,974 full-view and 7,906 detail pixels differ from neutral. All full-view pixels outside `[200, 270, 360, 410]` remain unchanged.

### MP4

`Mild_disgust_review_v1.mp4` SHA-256:

`71bf7075205155776165e147b06ae5ada1c1158f2a0401dcc8be94d39babbc6f`

- H.264, yuv420p, **968 × 800**, **30 fps**, **121 decoded frames**, **4.033333 seconds**, 188,969 bytes.
- Full decode exits 0 with no stderr. All frame timestamps match the 30 Hz grid.
- Every decoded left bust and right detail panel was compared with its same-index native PNG. Maximum mean absolute RGB error is **1.292702** for bust and **2.052819** for detail, on the 0–255 scale.
- Maximum face-feature error is **2.201863**; the largest same-index error above the best matching native face is **0.004679**, below the material-reordering threshold.
- Identical and near-identical held/neutral frames cannot have unique order proved under lossy encoding. The report retains that limitation. Native bookends are bit-identical; decoded MP4 bookends are not claimed bit-identical after compression.

## Frozen input and editor restoration evidence

The operator's editor rewrote only section order and whitespace in `native_launcher/project.godot`; setting values did not change. The original and rewritten files and failed pre-restoration guard are retained in `native_capture_audit/`. This reviewer read the diff and independently verified the final restoration; the reviewer did not restore or edit the project.

- Original/final project SHA-256: `9de6f885a00d424884a83ecc1ceb17c3bec57bde734edc3a67e2c4fa5b8f9821`.
- Preserved editor rewrite SHA-256: `8430380e79b1ecacea50480510f3fbf22b0c94dbd56b2b508ac40faddc26e90a`.
- Review-input freeze remains `22509ab2bf568edc6291e261fc0310bdac3818bbc08f4db6656be9ee30748086`; all 46 pinned inputs match.
- All 999 source/rig files, 184 PNGs, additional manifests and 998 unchanged launcher files match. The approved36 disk registry is unchanged and still excludes EXP-081.
- All 993 pinned runtime/artwork parity files also match approved39, with only the six documented newer registry/status/documentation/aggregate-check files excluded.

The temporary identity failure was expected evidence of an editor byte rewrite, not silently ignored. The final exact guard passes.

## Remaining decision

Technical capture and encoding are complete. There is no outstanding failed evidence check or access denial. **Visual acceptance remains the blocker:** the source's upper-lip-only disgust gesture is not available in this frozen rig, and the actual preview has a plausible smirk/objection reading. Present the preview with that limitation, retain UNAPPROVED status, and do not equate this technical PASS with user approval or an unmistakable disgust performance.

Evidence is in `native_review_evidence/review_checks.json`, `native_frame_hashes.json`, `decoded_frame_order.json`, the inspected contact sheets, `review_validator_native.log` and `review_validator_native_unit_tests.log`. This final report supersedes the native-pending status in the earlier source-review checkpoint.

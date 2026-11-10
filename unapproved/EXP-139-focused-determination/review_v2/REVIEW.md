# Focused determination v2: independent image and sequence review

Reviewed 2026-11-10. **Unapproved revision, suitable to present for expression feedback.** The stronger selected C pose is visible relative to v1, and the new blink supplies a much clearer motion cue. No blocking new mouth or persistent reopened-eye defect was found in the inspected captures. This reviewer did not operate the GUI or observe continuous normal-speed playback. User acceptance and continuous normal-speed perception are not established by this image-and-sequence review. `REVIEW_RESULT.json` separately records sampled normal-speed desktop playback.

## Perceived change from v1

V1 was judged imperceptible during user review. It remains preserved and is not approved. Its earlier technical pass did not establish adequate perceptibility.

At the original 568×800 full-bust scale, C has visibly lower, steeper brows and a wider sealed mouth line than the exact v1 reference. It reads as firmer concentration without a commanded squint, smile or pout. **It is still restrained, not a dramatic facial transformation.** Hair obscures part of the brows and the face occupies a small part of the bust. The blink closure is much more conspicuous than the static peak difference and is the strongest new answer to the “no movement” feedback.

The unscaled neutral/v1/v2 comparison retained locally supports this judgment. Pixel diagnostics also confirm a real increase, but are not used as a substitute for looking at the expression:

- Native full-bust neutral-to-peak changes: v1 478 pixels, v2 1,015 pixels. The summed absolute RGB change increases from 25,978 to 80,012.
- In the 400×360 detail view, brow-region changes increase from 1,895 to 2,649 pixels. Mouth-region changes increase from 35 to 1,433 pixels.
- The wider line makes the mouth cue less negligible than v1, but the painted lip contour is still not the source's fully flattened/compressed mouth. Horizontal widening is not proof of lip compression.

The captured sequence closes the eyes briefly, reopens them by 0.70 seconds, reaches exact C at the first 30 Hz sample after 0.78 seconds, holds it through 2.40 seconds, and returns exactly to neutral. The 1.62-second peak hold is intentionally still. Whether that hold and the new arrival feel right in continuous playback remains a separate perceptual judgment.

## Visible defects and inherited limits

The source sheet and the native neutral, v1 reference, selected C, partial blink, closed blink and reopened face were inspected directly. Native and decoded detail frames 0, 10, 12, 15, 18, 21, 24, 48, 72, 78, 90, 100, 109, 110 and 120 cover onset, closure, reopening, peak, release and reset. Full-bust frames 12, 15 and 18 were also inspected alongside neutral and peak.

- The brows stay continuous in the inspected poses. No detached brow fragment or eyelid collision was observed. Eyes are fully open at the focused peak, rather than held in a glare.
- The mouth stays closed. No exposed oral cavity, tooth/tongue flash, mouth-corner split or newly opened seam was observed in the inspected frames. The slightly wider contour does not read as a smile or pout to this reviewer.
- **Existing hard hair/upper-eyelid cutout edges are still visible.** They are especially conspicuous in enlarged partial-blink frames. This is not a claim of seamless eye animation. The source runtime and artwork are byte-exact, and the measured outer hair/lid seam regions return to and remain pixel-identical to neutral from the reopened frame onward. A separate ordinary-blink visual regression was not rendered in this review, so inherited-runtime identity alone is not presented as proof that every blink combination is flawless.
- No new persistent seam change, face drift or body motion was found. All full-bust pixels below y=400 stay identical across the complete native sequence.

Native and decoded detail contact sheets remain in the local review evidence; they are omitted from this compact source-and-video backup.

## Source fidelity

The EXP-139 sheet's peak calls for converging brows, open eyes and a purposeful lip line. Its stronger inward gathering remains only approximated here. The rig has no inward brow translation or local brow squeeze; rigid lowering and rotation cannot reproduce the painted source curvature. C reaches the existing lowering and tilt bounds. The mouth width is an authored tension cue, not a recovered source measurement.

The source allows ordinary blinking, but this deliberate onset blink and four-second timing are **newly authored interpretation, not recovered source animation**. The catalogue's 1.9-second schedule is proposed reference timing, not implemented motion. No source body gesture was added. The source sheet SHA-256 remains `a10a347e6d949606d346e65bd07b11cd9546f7e2e96944a8ded6be00fa8258b1`.

## Integrity and complete sequence checks

The [compact independent review receipt](review/compact_review_metrics.json) records **42 passed checks**. Existing native evidence records 600 static-alternative checks, 592 onset checks and 63,948 motion checks. Those counts describe their scopes, not a whole-runtime certification.

- All 1,112 frozen rig files, including 184 PNGs, are byte-exact. All 2,490 frozen v1 evidence files are preserved. The original review receipt found all 28 static-alternative files unchanged. Before publication, `README.md` was amended to report completed motion review, so the final inventory has 27 unchanged static files and one documentation-only difference. The original freeze and review receipt remain historical evidence; `PUBLICATION_INVENTORY.json` records the final state.
- The production registry remains the same 27-profile baseline and excludes EXP-139. Inherited release metadata describing 26 profiles remains historical metadata, not a new release claim.
- Both native frame directories contain exactly `0000.png` through `0120.png`. All 242 decoded image hashes match native capture records.
- All 121 native pose/time records match headless records. Only the nine declared brow, sealed-mouth and onset-blink channels act. An independent reconstruction of the shared smoothstep timeline and existing initial/retrigger blend matches the native controls to within 2.97×10⁻⁸.
- Neutral frames 0–7 and 110–120 are pixel-identical in both views and match the static neutral captures. Frames 24–72 are an exact repeated C peak, matching the static selection. Frame 15 exactly matches the closed-blink study and frame 21 the reopened study.
- Each view has 54 distinct decoded native images. Repeated peak and neutral frames are intentional holds, not missing captures.
- The eye core below the moving brow tip is pixel-identical to neutral after reopening. The complete native changed-pixel union is confined to the face: bust x209–355/y287–387; detail x34–332/y64–267.

Two initial independent-test assumptions were corrected, with the original diagnostic receipt retained locally. The timeline comparison initially omitted the unchanged 0.30-second initial/retrigger blend; the same 10⁻⁶ threshold passes after modeling it. The initial eye rectangle included 25 newly lowered brow-tip pixels at y110–112. Direct crop inspection identified them as brow, and the actual eye-core rectangle begins at y113. These were test-model/region corrections, not candidate edits or loosened thresholds.

## MP4 verification

`motion_study/Focused_determination_review_v2.mp4` is H.264, 968×800, 30 fps, 121 frames, 4.033333 seconds and 163,085 bytes. The duration includes the final endpoint frame. SHA-256:

`101456109207dcc9389f9c6053bc664fbad5369dab28232c39375889991bc955`

Every frame decoded without errors. Presentation timestamps run in 1/30-second increments from 0 to 4 seconds. All decoded bust and detail frames were compared to their native numbered sources; mean RGB error from lossy encoding is 1.292/255 and 2.035/255 respectively.

A separate encode of the verified native numbered sequences, using the documented composition and codec settings, produces the same MP4 hash. **All 121 decoded YUV frame hashes and timestamp records match exactly**, proving this MP4 contains the verified captured sequence in order. Receipts: [delivered frame hashes](review/delivered_video.framemd5), [independent chronological reconstruction](review/expected_chronological_sequence.framemd5). This does not establish live engine pacing or continuous normal-speed observation.

## Scope and reproduction

Run `python -B focused_determination_v2_work/review/verify_review.py` from the workspace root. It reads capture evidence and writes only review diagnostics and an independently reconstructed comparison MP4 under `review/`; it does not launch Godot or interact with the GUI.

V1, the rig, artwork, production registry and candidate data remain unchanged. The publication-stage README, preparation note and this report were corrected to describe the completed work and the later README amendment. No CI, paid resources, purchases, hardware flashing or remote-machine execution was used. Full runtime regression, exported packaging, lip-sync, production integration, normal-speed acceptance and user approval remain outside this review.

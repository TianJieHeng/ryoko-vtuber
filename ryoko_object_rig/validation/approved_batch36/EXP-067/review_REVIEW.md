# EXP-067 Creeping dread: independent native preview review

**Ready to show as an unapproved candidate, with a source-fidelity caveat. Not approved or integrated.**

The native preview presents a slow change toward mild concern/apprehension. The brows and mouth change visibly at the actual 568 × 800 bust size. It does not reach the source sheet's strongly widened, tense-eyed dread. The upper-tooth strip gives the partly open mouth a small nervous-smile ambiguity, especially during build. It does not read as an outright happy smile because the corners do not lift and the brows retain a worried relationship.

## Visual finding

The actual EXP-067 sheet and peak panel were inspected alongside all seven static face captures, native bust progression, and nine decoded MP4 keyframes. The source is verified by its catalogue and panel hashes, not inferred from the title.

- **Brows:** The retained inner ends rise progressively while the outer ends remain anchored. Screen-left change is clearer; screen-right is shorter and partly hidden by the unchanged fringe. This creates visible concern but not the source's curved, strongly pleading brow shape. It is rigid rotation, not new brow drawing.
- **Eyes:** The four-source-pixel upper opening is visible in the face comparison but subtle at bust size, where its maximum is 1.96 pixels. The irises stay large and the upper lids retain much of their baseline contour. The source's more exposed eye whites, apparent pupil-size change, and tense lid shape are not reproduced. No closure, gaze, aversion, or automatic blink accompanies opening.
- **Mouth:** The mouth remains sealed through the 0.8-second pressure key, then progressively parts. Peak central separation is 9.723 source pixels, or 4.764 bust pixels. The pressure-only change is slight visually; the rendered outer lip does not visibly flatten into a newly drawn pressed contour. At build and peak, bright inherited upper teeth contrast with the dark mouth slit. The source's opening is more dark/downturned and its tooth cue much less conspicuous. This is the main smile-like ambiguity, not a numerical smile control leaking into the pose.
- **Temporal interpretation:** Indexed native and encoded frames progress from neutral to pressed, onset, build, peak, softening, and exact neutral. The authored peak is 2.5–3.0 seconds, with neutral reached by 4.55 seconds. This is a 4.8-second interpretation of static art, not recovered source motion. No normal-speed GUI playback or subjective live pacing review was performed.
- **Artifacts:** The visible lash/hair overlaps and small segmented joins are already present in neutral. No new detached facial patch, head/body drift, or gross opening artifact was identified in the inspected static and decoded samples. This does not claim pixel-by-pixel visual inspection of every frame. Quantitative checks cover every native and decoded frame.

## Independent validation

`review_validation.py` reads existing captures only. It does not start Godot or overwrite production assets.

- Native static report: **496 checks, PASS**. Native motion report: **9,021 checks, PASS**, covering 145 inclusive 30 Hz samples and restart/release/reset state checks.
- **All 290 native RGBA frame hashes** independently recomputed and matched the capture records. All 145 captured pose records match the prior headless samples.
- Neutral, pressed, build, peak, softening, and neutral-return static renders exactly match their corresponding sampled native motion frames in both views. The 1.35-second onset key lies between 30 Hz samples, so no exact static-onset equality is claimed.
- Native first and last pixels match exactly in both views. All differences across the complete sequence remain inside `[215,285,345,393)` in the bust and `[47,59,312,279)` in the detail. Every bust pixel outside the conservative face box `[200,270,360,410)` stays identical, preserving body, clothing, jewelry and surrounding hair/background.
- Both the candidate rig and source baseline preserve **all 1,124 frozen files, including all 184 PNGs**. Production registry retains the exact 27 baseline IDs. EXP-067 is absent from it. Frozen baseline commit: `816d77fafb6e016dc70f0802743d444e618f7b0f`.
- The source sheet, catalogue, and all nine separate panels match their recorded SHA-256 values.
- MP4 independently decoded completely with no errors: **145 frames, H.264/yuv420p, 968 × 800, 30 fps, 4.833333 seconds**. The extra 1/30 second is the inclusive final frame. All presentation timestamps match frame index / 30.
- Each decoded bust and detail panel was compared to its expected same-index native frame. Mean RGB absolute error is 1.292/255 for bust and 2.030/255 for detail. Keyframe matches and an all-frame nearest-source-face check support correct order; the greatest excess error against the best source match is 0.00721/255. Compression and repeated/near-identical poses prevent treating this as a lossless frame-identity proof.
- Native logs contain no `ERROR` or `SCRIPT ERROR`. They retain the unsupported V-Sync warning and the inherited uneasy-overlay image-loading warning. The headless-only upper-opening shader diagnostic is not present in these native logs. This is not an export test or a fix for that inherited warning.

## Evidence and delivery boundary

- Preview: `Creeping_dread_review_v1.mp4`
- SHA-256: `21a3ad3f8af3763660ee60a7a4afeeac43d0eddb1814d42a2ee522af811bd739`
- Compact verification: `review_evidence/review_checks.json`
- Complete frame integrity: `review_evidence/native_frame_hashes.json`
- Per-decoded-frame comparisons: `review_evidence/decoded_frame_order.json`
- Visual evidence: `review_evidence/static_faces.png`, `encoded_keyframes.png`, and `bust_progression.png`.

This review establishes a technically coherent, bounded preview worth showing for an artistic decision. It does not establish strong source likeness, approval, integration, live pacing, whole-runtime stability, export readiness, or lip-sync compatibility. No new art, production runtime changes, CI, paid resources, hardware, remote execution, or approval/integration was performed by this review.

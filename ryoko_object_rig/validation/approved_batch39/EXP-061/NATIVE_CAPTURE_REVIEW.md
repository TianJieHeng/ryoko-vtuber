# EXP061 Broad Surprise: native capture and sampled playback

Date: 2026-11-10 UTC. **UNAPPROVED review candidate.** No integration, baseline edits, Library operation or publication was performed by this capture worker.

## Native evidence

The prepared `native_launcher/project.godot` was imported through the existing Godot UI. Editor Settings showed Game Embed Mode `Use Per-Project Configuration`; it was changed to `Disabled`, the project was reloaded, and Run Project visibly opened a standalone native render window. The original preference was restored and visually verified after capture.

- Static capture: **PASS, 870 checks**, 16 PNGs (eight full/detail pairs), strictly 568 × 800 full and 400 × 360 detail.
- Motion capture: **PASS, 9,508 checks**, 121 full and 121 detail PNGs at authored 30 fps sample times across four seconds. Renderer: llvmpipe (LLVM 19.1.7, 256 bits), display: X11.
- `Broad_surprise_review_v1.mp4`: H.264/yuv420p, 968 × 800, 30 fps, 121 frames, 4.033333-second container duration. It contains the native full panel left and native detail panel right at y=220.
- `review_evidence/review_checks.json`: final **PASS**, no missing evidence or failures. The validator independently recomputed the timeline, checked all 242 native RGBA frame hashes and 16 stills, exact neutral holds/bookends, fixed pixels outside the face box, sustained peak, static/motion anchors, all 121 decoded video frames and timestamps, same-index panel similarity and nearest-frame error.
- Maximum full/detail decoded panel MAE: 1.29624 / 2.05357. Maximum expected-minus-best face MAE: 0.00373. Lossy repeated/near-identical holds do not support unique frame identity.
- The 999 pinned approved36 files, 184 source PNGs, reference sheet/catalogue and disk registries remain unchanged. EXP061 is not added to a disk registry.

## Configuration bookkeeping

Godot rewrote only the prepared launcher's `project.godot` section order and whitespace. The first complete validator run correctly failed its byte-identity guard on that file; all other checks passed. The editor-written text and initial failed report are preserved under `review_evidence/`. Its values were unchanged. The original exact reviewed file was restored and its SHA-256 matched the frozen value `649e4bd8b6fcc9e70a2626d9563e8a0cee7f423de1b3309115478982c3b64b69`; the complete validator then passed. See `review_evidence/launcher_config_restore.json`. No guard was weakened and no candidate control values were changed.

## Pixels actually inspected

The actual EXP061 source sheet, historical EXP064 Shocked Gasp and EXP004 held Delight detail captures, this candidate's native peak full/detail stills, decoded nine-pose keyframe contact sheet and four-frame native bust progression were inspected.

The candidate makes a coherent bilateral brow rise with an opening mouth, sustains the open state, and returns to the same neutral. The whole-brow elevation is visually different from Shocked Gasp's inner-brow slope, and the aperture is less pinched. However the approximately one-bust-pixel central gap increase is not a strong distinction by itself. At bust scale the expression remains restrained; the sustained timing and brow geometry carry most of the difference. Unlike the held Delighted Discovery comparator, there is no spread-smile conversion. Exposed upper teeth and the existing mouth contour can still give individual frames a mildly speaking or cheerful read, so control-level zero smile is not proof that every viewer will read surprise.

Source fidelity remains partial: the rendered eyes stay almond-shaped and much less round than the source peak, and the face/jaw/chin silhouette does not drop. The mouth is an approximation with existing split-lip parts, not the source's rounded jaw anatomy. Head/body, gaze and blink remain fixed as intended. These limitations do not disappear because validation passes.

## Playback evidence and limits

`Broad_surprise_review_v1.mp4` was opened in Kdenlive's Clip Monitor. Home and normal Play (Space) were invoked twice. Screenshots showed the correct selected clip, start/reset, early playhead progression and final neutral endpoint. The first run's endpoint displayed 00:00:04:01. No speed alteration was requested or made. This is supported UI playback with sampled observations, **not a claim of continuous full-motion viewing**. Full normal-speed pacing, every transition, live-engine real-time performance, interruption playback, lip-sync and body gestures remain unvalidated. `PLAYBACK_REVIEW.json` records the exact scope. The UI slot was released after playback.

The static/keyframe evidence is coherent for user review with those caveats; approval and perceptual sufficiency remain the user's decision.

# EXP-161 Sleepy native capture and sampled playback review

## Result

Native evidence and MP4 validation pass. The candidate remains **UNAPPROVED** and isolated. This is a technical evidence pass, not a claim of exact source fidelity or a production release.

- Video: `Sleepy_review_v1.mp4`, 203,037 bytes, SHA-256 `9ee4cbb7cee2dd79549363c472dd0ff7f0234e40282951745e90f921aef38475`.
- H.264 / yuv420p, 968 × 800, 30 fps, 121 endpoint-inclusive frames, 4.033333 seconds.
- Native static: 16 PNGs, eight poses, 1,590 assertions, zero failures.
- Native motion: 121 full and 121 detail PNGs, 12,125 assertions including 36 lifecycle assertions, zero failures. Display X11; renderer llvmpipe (LLVM 19.1.7, 256 bits).
- Full/bust captures are exactly 568 × 800 RGBA; detail captures exactly 400 × 360 RGBA.
- Author validator: 84/84 checks, no pending checks or failures (`native_review_evidence/review_checks.json`).
- Separate reviewer validator: 87/87 checks, no pending checks or failures (`independent_native_review_evidence/review_checks.json`). Neither validator was edited.
- All 107 Python tests rerun and passed. The independent review checksum list still passes.

## Authorized native route and preservation

The existing Godot Project Manager imported the exact isolated launcher through its native file chooser. Game Embed Mode initially showed **Use Per-Project Configuration**. It was changed through the UI to **Disabled**, and the project was reloaded before Run. The standalone debug window was observed at 568 × 800, and the native probes produced the complete outputs on the first capture attempt. No failed native PNG capture was discarded.

Godot reordered the project configuration's `[editor]` section without changing setting values. The rewritten file and exact diff were archived as `native_review_audit/project.godot.editor_reordered` and `editor_reorder.diff`. The freeze check and both validators correctly failed solely on `reviewed_candidate_and_capture_inputs_unchanged`; those failed reports remain under `native_review_audit/reordered_*_evidence/` with invocation logs. No freeze or validator was weakened to accept the rewrite.

After capture, Run was stopped. Game Embed Mode was restored through the UI to its observed original **Use Per-Project Configuration**. The Sleepy editor exited to Project Manager, verified visibly, before the exact frozen original `project.godot` bytes were restored. The final freeze check confirms all 47 handoff files, all 999 source/copied-rig files, 998 non-project launcher files and both source manifests match. The allowed project name/main-scene override remains exact to its handoff bytes.

Only supported native CUA actions were used to import, configure, reload, run and stop Godot. No native-shell launch, display-server, socket, remote-machine, CI or paid-resource workaround was used. The existing encoder ran on already captured files. No Library, publication, production registry, source artwork, rig runtime or candidate changes were made.

## Pixel and decode review

Both validators completely decoded the video: 121 frames, clean decoder exit and no stderr. Every frame was compared to its same-index native full/detail panels, with nearest-face checks for material reordering. Identical/near-identical holds cannot be uniquely ordered by lossy pixels and are not claimed to be.

Mean absolute decoded-panel error was 1.2922 for full and 2.0377 for detail on the 0–255 channel scale. Maximum per-frame values were 1.2952 and 2.0671 respectively. Native neutral holds through frame 6 and from frame 111 are exact; frames 48–72 share the held peak. Static anchors match motion frames exactly. Native body/outside-face pixels stay fixed.

Actual pixels inspected: the complete source sheet, the peak detail PNG, all eight native static faces, native bust progression and nine decoded keyframes (0, 18, 30, 48, 72, 84, 96, 105, 120). No missing panels or black decoded frames appeared in these inspections; full decode coverage is supplied by the validators, not by a claim of watching each frame.

## Sampled normal-play observation and visual limits

The final MP4 was opened in existing Kdenlive. Normal Play and then Loop Zone were used without changing clip speed. Full-screen playback screenshots sampled neutral/onset, heavy-lid peak and recovery with a moving timeline cursor. These are **sampled normal-play observations**, not continuous uninterrupted viewing or independent human approval. Playback was paused at 00:00:00:16, full-screen mode exited, and Kdenlive was left with Sleepy selected. The shared UI slot was released.

The bilateral lids visibly sink into a sustained drowsy pose with a narrow gold iris strip still visible, then recover. The broad sustained trajectory is distinguishable from repeated effortful reopenings (EXP-164), a tense sealed pout with sharper brows (EXP-174), and fully closed eyes with sealed lips (EXP-177). This observation does not establish a formal perceptual A/B pass against native videos of those profiles.

The strongest source-fidelity limitation is the mouth: native peak lip separation exposes a narrow bright tooth-like strip, whereas the source shows a smaller rounded dark opening and a softer relaxed-mouth contour. The implementation supplies no actual jaw rotation or chin descent. The ordinary lowered lash shape also reads heavier/narrower than some source panels. Fine jagged or stitched-looking pixels at hair/lid boundaries are visible in the unchanged neutral rendering and remain noticeable in detail views; no claim of seam-free artwork is made. Bust-size readability is less sensitive to these edges.

These limits should accompany any user review. Do not represent the technical checks as proof of exact relaxed-jaw anatomy, flawless source fidelity, or user approval.

# EXP-096 Headache tension native review

## Result

Native capture, encoding and technical review are complete. This isolated candidate remains **UNAPPROVED**. No Library, GitHub, production registry or backlog write was made.

- `Headache_tension_review_v1.mp4`: 197,614 bytes; SHA-256 `2b410146ed28ec4d6240e3e47c6b6f27d9c33b1a8087c101941da9a6a2d58716`.
- H.264/yuv420p, 968 × 800, 30 fps, 121 endpoint-inclusive frames, 4.033333 seconds.
- Native static capture: eight anchors, 16 RGBA PNGs, 1,838 checks PASS with no failures.
- Native motion capture: 121 full and 121 detail RGBA PNGs, 16,745 checks PASS with no failures. X11 / llvmpipe (LLVM 19.1.7, 256 bits).
- Full/bust capture dimensions are exactly 568 × 800. Detail captures are exactly 400 × 360.
- Unchanged author evidence validator: 84/84 checks PASS. Unchanged independent reviewer validator: 96/96 checks PASS. No pending checks or failures.
- Both validators completely decoded all 121 MP4 frames, with exit 0 and empty stderr. All-frame native hash, frame-order and timestamp checks pass.
- All 146 combined author/reviewer unit tests pass after exact project restoration.

Detailed evidence is in `native_session_evidence/author_final/` and `native_session_evidence/independent_final/`. The final author input freeze remains `6f076e4127e9c07d4083c6a26560ce32dfcb25a9d9c7981ad0401d291a509520`.

## Supported native route and preservation

The existing Godot Project Manager imported the exact `headache_tension_work/native_launcher` directory through the native chooser. Editor Settings visibly showed Game Embed Mode as Use Per-Project Configuration. It was temporarily set to Disabled, then Project → Reload Current Project was explicitly selected. The restarted editor visibly reported Embedding is disabled before F5.

The standalone debug window was visibly observed in both full and detail sizes. The unmodified launcher completed all captures on its first run. No failed capture was removed or recaptured. F8 stopped the finished run.

Use Per-Project Configuration was then restored and visibly verified. The candidate editor exited to Project Manager, confirmed in the desktop screenshot and window inventory, before restoring the original project bytes. The unrelated Controlled Anger editor and preexisting Broad Surprise editor/dialog were left untouched.

Godot had reordered the `[editor]` section before `[rendering]` and inserted a normal blank line; no setting values changed. The original project bytes, editor rewrite, exact diff, failed freeze guard, failed author evidence guard and intermediate unit-test failures remain under `native_session_evidence/`. The seven intermediate test failures were caused by the intentional editor-byte mismatch. None was suppressed: after the editor exited and the exact original bytes were restored, the freeze and all 146 tests passed. No frozen validator, profile, artwork, runtime or capture wrapper was edited.

Only supported CUA Godot and Kdenlive controls were used for native work. Encoding and validators read the completed native captures. No native-shell launch, display-server/socket access, remote machine, CI or paid-resource workaround was used.

## Actual pixel and source review

The actual nine-panel source sheet was inspected. Native pixel inspection covered all eight static detail anchors and full/bust frames 0, 30, 48 and 84. Decoded MP4 detail inspection covered frames 0, 18, 30, 39, 48, 72, 84, 96 and 120. These contact sheets contain actual native or decoded pixels, not synthetic rerenders.

The sequence follows the reference's important order: ordinary bilateral lids progressively close, remain fully closed through KP5–7, and reopen only after the brow and lip tension softens. Mouth aperture remains sealed, gaze stays forward and there is no smile or unrelated body acting. Neutral return and body preservation are checked at the native pixel level.

The headache acting is visibly much milder than the source. Without true central furrows, horizontal brow convergence or independent downturned mouth corners, the result can read as a restrained long eye-close or discomfort rather than a strong headache grimace. The sealed lip-pressure/purse change and the tension-to-softened-closed transition are subtle at bust scale. This is an approximation, not an exact source-fidelity pass or a proven perceptual distinction from calm/closed-eye expressions.

Fine jagged or stitched-looking pixels at lash/hair boundaries are visible in neutral and intermediate detail views. The neutral baseline already contains these features; no seam-free claim is made.

All-frame lossy decode mean absolute error on the 0–255 scale is 1.288655 full and 2.023949 detail, with maxima 1.294666 and 2.069560. Frame order comparisons include same-index native panels and all-frame nearest-face comparisons; identical and near-identical holds remain ambiguous under lossy compression.

## Playback observation

The existing Kdenlive loaded this exact MP4 at the unchanged 30 fps. Standard Play was initiated from 00:00:00:00 and the neutral 00:00:04:00 endpoint was observed. Normal Loop Zone playback was also started; screenshots sampled the closed-eye phase and reopening, with clip transport observations including 00:00:01:15 and 00:00:03:14. Playback was then stopped and left at the neutral 00:00:04:00 endpoint with Play available. UI control was released immediately afterward.

This is sampled normal-speed playback, not continuous uninterrupted viewing. Technical PASS, source-sequence support and these observations do not constitute user approval.

# EXP-161 Sleepy: unapproved shared-rig candidate

This isolated data-only candidate uses the frozen approved36 baseline at commit `3ce98774282ad6c20dfbd7018d20838ff861b762`. All 999 manifest-pinned files, including 184 PNGs, remain exact in the source and `rig/` copy. Both available source manifests are retained. The disk registry still contains its original 36 profiles. The candidate and static probes are loaded only in memory.

Direct local comparisons confirm all 993 common runtime/artwork files remain identical in approved39 and approved40. Six registry/release/readme/aggregate-validation files are explicitly excluded from that newer-tree comparison. No runtime, artwork, scene, shader, control or source-reference change was made.

## Reference interpretation

The actual 1254 × 1254 nine-panel EXP-161 sheet was viewed before authoring. `SOURCE_CATALOGUE_ENTRY.json` preserves its catalogue record. `SOURCE_REFERENCE.json` records the actual sheet, catalogue and all nine panel hashes, observations and limitations. All nine linked panels are checked as exact lossless crops of the sheet.

The sheet develops low relaxed brows, heavy bilateral upper lids and slightly parted lips, sustains the drowsy expression, then recovers. The four-second candidate has eight static anchors and eleven timeline keys:

- 0.00–0.20: neutral lead-in.
- 0.20–0.60: low brows and gently heavy lids arrive before lip parting.
- 0.60–1.00: lids sink further and lips begin separating.
- 1.00–1.60: gradual build to the heavy-lid, slightly open-mouth peak.
- 1.60–2.40: sustained drowsy hold, without a catch-and-reopen cycle.
- 2.40–2.80–3.20: recover through two gentler poses.
- 3.50: lips reseal while a slight residual lid droop remains.
- 3.70–4.00: exact neutral hold.

This is newly authored timing from static references, not recovered motion or an approved animation. All 121 endpoint-inclusive samples are tested at 30 Hz. The unchanged smoothstep interpolation pauses in velocity at anchor joins; this is a monotone sink, not a claim of uninterrupted constant-speed movement.

## Supported approximation and distinction

Only five existing channels act: equal vertical brow lowering, equal ordinary partial lid closure, and mouth opening. Peak values are −0.22 brow, 0.57 lid closure and 0.16 opening. That yields 2.2 source pixels of downward brow travel, 20.52 source pixels of upper-lash travel and a 4.752-source-pixel split-lip gap (2.32848 at bust scale).

- “Relaxed jaw” is approximated only by lip separation. No jaw rotation, chin descent, cheek inflation, skull motion or new relaxed lip shape is implemented.
- Brows stay untilted and have no inner-lift action. There is no purse, pout, lip pressure, mouth-corner bias, smile-eye, smile, gaze shift, head/body movement, hair motion, breathing, speech or effect.
- Blink channel names use character sides: `blink_R` controls screen-left and `blink_L` controls screen-right. Equal bilateral values avoid unilateral expression.
- EXP-164 Fighting Sleep has repeated sealed-mouth droop/reopen efforts and brow changes. This candidate has one sustained sink and slight lip parting.
- EXP-174 Sleepy Annoyance adds sharp opposing brow tilt, much stronger brow lowering and a sealed pout. This candidate has none of those actions.
- EXP-177 Meditative Calm fully closes its eyes and keeps its mouth sealed. This candidate keeps the eyes partially open and parts the lips.
- Numeric comparison against all 36 baseline profiles and six later candidates establishes nonduplicate trajectories, not perceptual distinction or source fidelity. Native visual review is still required.

## EXP-192 read-only feasibility decision

The actual Cheeks Puffed sheet was also inspected. Expanded cheeks are essential to its named intent. The frozen registry has no cheek inflation control, and lip purse cannot create that anatomy. `SKIPPED_EXP-192.json` records the source and registry hashes. It is skipped, with no pout substitute, source-art edit or runtime extension.

## Headless verification

- 1,558 static assertions cover actual brow/lash/lip geometry, bounds, scope, excluded channels, fixed gaze/body, exact reset and unchanged registry.
- 11,640 motion assertions cover every timeline sample, monotone sink/recovery, sustained hold, small lip separation, exact neutral, and 36 lifecycle assertions at nine interruption times.
- 8,422 separate Python numerical/source checks reproduce static geometry, independent smoothstep samples and aperture math. Maximum pose error is below 2.83e-8. All nine source panels match exact sheet crops.
- 20 encoder guard tests and 11 independent numerical mutation tests pass. A further read-only review-validator suite covers native-evidence gating, source/launcher preservation, malformed records, prohibited controls and source-specific timing.
- Headless Godot 4.6.3 import and all three launcher script parse checks pass. The frozen runtime’s inherited image-load warning for `uneasy_clear_parting.png` is not suppressed or altered.

Re-run headless preparation from this directory:

    sh run_motion.sh --state
    python verify_preparation.py
    python independent_geometry.py
    python -m unittest discover -s . -p 'test_*.py' -v
    python verify_input_freeze.py
    python review_validation.py

The last command returns PENDING with exit code 2 until actual native captures and the MP4 exist. This is not a failed preparation or a false native pass. Re-running checks may change receipts/logs and then requires a new explicitly pinned handoff freeze. Do not overwrite previous native evidence.

## Separate native launcher, not executed

The prepared project is `native_launcher/project.godot`, named **Ryoko EXP161 Sleepy PREVIEW ONLY**. Its only baseline-file override is the project name/main scene; the other 998 pinned files and both source manifests remain exact. Generated wrapper scripts match the documented headless-probe transformation byte for byte.

Under separate authorization, the existing native Godot UI may run this project. It captures eight static anchors and all 121 motion samples, refusing existing `capture/` or `motion/` directories. Both probes require actual bust/full dimensions **568 × 800** and detail dimensions **400 × 360**, checked before PNG writes. Embedded-game behavior may ignore requested sizes: actual capture dimensions are the gate, not the requested size. Preserve failed evidence and correct settings through the authorized UI before a fresh attempt. No display server or socket workaround is supplied.

After successful native capture, `python encode_preview.py` can create `Sleepy_review_v1.mp4`. It rejects missing/headless/failed/stale receipts, wrong dimensions or modes, incomplete/extra frames, incorrect timing or pixel hashes, failed neutral return and an existing output video. Intended output is 968 × 800 at 30 fps, approximately 4.033 seconds for 121 endpoint-inclusive frames. The read-only review validator additionally checks all native frames and the full MP4 decode/order against captures.

**No native capture, video, normal-speed observation, independent human/agent visual sign-off or user approval exists at this handoff.** Native evidence remains pending. No production integration, publication, CI, paid resource, remote-machine execution, hardware action, UI launch, native shell launch, display server or socket workaround occurred.

# EXP-123 Puzzled: unapproved shared-rig candidate

Prepared independently against approved36 commit `3ce98774282ad6c20dfbd7018d20838ff861b762`. This is not an approved39 integration. All 999 manifest-pinned baseline files, including 184 PNGs, and both available manifest identities remain unchanged in the source and `rig/` copy. The production registry still contains 36 profiles. Candidate and probe JSON are external and registered only in memory.

## Source and interpretation

The actual 1159 × 1358 EXP-123 nine-panel sheet was inspected before authoring. Sheet and all nine linked panel hashes match the catalogue. See `SOURCE_REFERENCE.json` and `SOURCE_CATALOGUE_ENTRY.json`.

The new four-second performance begins with a questioning screen-left inner-brow lift and lowered opposite brow. Uneven narrowing and a compact side-biased sealed pout gather into a held peak, followed by a small rechecking squint. The lip bias releases before the questioning brow, then the model returns exactly to neutral. Eight static anchors and eleven timeline keys produce 121 samples at 30 Hz, including both endpoints.

- Existing rigid outer-anchor rotation approximates the raised inner brow. It does not reshape the brow pigment or make a localized curve.
- Symmetric purse plus small screen-right width biases the endpoint midpoint by two source pixels at peak. The center stays fixed. This is not whole-mouth translation or a faithful reproduction of the painted diagonal pout.
- The sheet's head tilt is deliberately omitted. No gaze, smile, speech, blush, hair, head or body movement is added.
- Explicit brow/width names use screen sides. Blink names use character sides: `blink_R` narrows the screen-left eye, `blink_L` narrows screen-right. Geometry tests verify this rather than assuming labels.
- This does not repeat Mental arithmetic's alternating lifts/upward glance, Frustrated pout's bilateral construction, or the smile controls of Knowing smirk. Numerical comparisons cover all 36 frozen profiles plus the three later candidates. Perceptual distinction still needs native review.

## Passed headless checks

- 1,494 static assertions: bounded poses, actual outer-anchored brow geometry, uneven lash travel/iris closure, fixed gaze, sealed contour and monotonic horizontal lip mapping, exact reset and untouched disk registry.
- 8,902 motion assertions over 121 samples, including source-specific timing, bounded frame steps, neutral holds and restart/release/reset at nine interruption times (36 lifecycle assertions).
- Independent Python smoothstep comparison: maximum control error below `1.5e-8`.
- Source preservation: 999 pinned files and 184 PNGs remain exact in source and copied rig. Reference catalogue, sheet and nine panel hashes remain exact.
- Thirteen encoder guard unit tests pass using temporary receipts and mocked pixels, never generated artwork. Running the encoder here correctly refuses missing native captures.
- Separate native launcher imports and all three launcher scripts parse under headless Godot 4.6.3. Its only pinned-file override is its own project name and main scene, so 998 baseline launcher files remain exact. Manifest copies are retained too.

An initial numerical failure exposed a candidate/test blink-side convention mismatch. That authoring and test issue was corrected without changing runtime. The first failure is preserved under `development_audit/`, with the correction documented. Final receipts are at this directory's root.

Re-run numerical checks:

    sh run_motion.sh --state
    python verify_preparation.py
    python -m unittest discover -s . -p test_encode_preview.py -v

The run helper supports headless state checks only. No native renderer, UI, display server or socket workaround was invoked. The inherited runtime emits a known warning about loading `uneasy_clear_parting.png` as an Image; no warning suppression or runtime change was made.

## Prepared native review, not yet executed

Open `native_launcher/project.godot` through a separately permitted existing native Godot UI and run that project. The unique project name is **Ryoko EXP123 Puzzled PREVIEW ONLY**. It captures eight static anchors before the timeline. It refuses pre-existing capture/motion directories. The launcher never creates a display server.

Both probes enforce actual full/bust size **568 × 800** and detail size **400 × 360** before saving. An embedded game can ignore the requested size; receipt dimensions, not a setting alone, are the gate. Use the normal permitted UI for any needed standalone-game setting and preserve prior captures if a size check fails.

After successful native capture, run `python encode_preview.py`. The encoder requires passing native static/motion receipts, matching profile/plan/baseline hashes, all 121 RGBA frames per view, exact pixel-receipt hashes, dimensions and neutral return. It refuses existing MP4s. Expected output is `Puzzled_review_v1.mp4`, 968 × 800 at 30 fps. The profile spans 4.0 seconds; encoding all 121 endpoint-inclusive samples produces approximately 4.033 seconds. No video exists yet.

Review actual frames, source fidelity and normal-speed motion before asking for approval. Numerical success is not visual approval. No production registry, artwork, shaders or runtime were changed. No publication, CI, paid resources, remote-machine execution or hardware actions were performed.

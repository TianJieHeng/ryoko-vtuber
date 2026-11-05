# Approved expression-specific gaze validation

Based on approved main `ac597f02308f447d667a7766dc692adb917e3c9c`. The user approved the actual runtime review and eye close-up on 2026-11-05 before publication.

## Scope and preservation

Only existing EXP-064 and EXP-189 gain rigid iris translation. No expression IDs, facial poses, shader samplers or mesh vertices are added. All 610 inherited PNGs are SHA-256-identical to the approved project. The facial controller, registration and deformation shader are unchanged. The other 91 expressions retain their authored gaze; neutral retains its previously approved gaze behavior. Brow control remains neutral-only.

Twelve small derivative textures contain four original iris cutouts, matching fixed apertures and reconstructed sclera beneath the cutouts. Hidden sclera is estimated from neighboring source pixels, not recovered unseen artwork. Iris detail and size are retained without scaling, shear or warping. Travel stays within seven source pixels horizontally and two vertically.

## Local automated checks

All 23 Godot suites passed again before publication: 163,972 counted checks plus the bounce amplitude/settling suite. The new expression-gaze suite passed 7,135 checks. It covers supported/unsupported profiles, blink and mouth independence, repeated switches, look-at, paused selection, reset, timed gaze cues, real loopback UDP delivery and timeout release. No script errors or failed checks were found.

Run the Godot suites from this directory with:

```sh
for script in test_*.gd; do
  godot --headless --path . --script "res://$script" || exit 1
done
```

The Python layer builder checks all 75 integer travel offsets for each of the four eyes. Original iris RGB values and center reconstruction are exact at native pixel centers; no source pixels outside the safe eye interiors change. Separate saved-PNG checks cover all 12 textures and report zero native-center or iris RGB error. Filtering and runtime rendering are separate checks.

## Actual runtime evidence and limits

The review uses actual Godot movie-writer output: 841 frames, 28.033 seconds at 30 fps, 568 by 760. The 960 by 480 eye close-up is cropped from that same recording. The recording finished without script or shader errors. Chronological frames, enlarged eye views and state logs were reviewed before the user approved the candidate.

Centered rendered captures differ from the authored reference at 35 pixels per supported expression, with maximum RGB-channel differences of 5 for EXP-064 and 2 for EXP-189. This is a small filtering difference, not a claim of pixel-identical rendered compositing. The unsupported-expression comparison is identical.

Native-speed playback was unavailable to the assistant. The recording ran slower than real time, so it does not establish live playback performance. Low-limit graphics hardware remains unverified. This is not general gaze support for all expressions. No CI, paid resources, remote-machine execution or full-body changes were included.

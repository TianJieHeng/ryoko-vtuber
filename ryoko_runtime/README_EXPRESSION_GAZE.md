# Approved gaze on two existing expressions

Built on approved main `ac597f02308f447d667a7766dc692adb917e3c9c`. This is a bounded feasibility proof for an original handoff requirement: eye direction should remain controllable when an expression is selected.

Only the already-authored **EXP-064** and **EXP-189** gain rigid iris movement. Their complete small irises are visible in the existing artwork, with enough surrounding sclera for the approved seven-pixel horizontal and two-pixel vertical travel. The expressions, eye shapes, lids, brows, pupil sizes and visible iris detail are retained. No new expression IDs or facial poses are produced.

The user approved the runtime review on 2026-11-05. The other 91 expressions keep their original eye artwork and authored gaze. Neutral retains its previously approved gaze textures and behavior. Brow control remains neutral-only. See [VALIDATION_EXPRESSION_GAZE.md](VALIDATION_EXPRESSION_GAZE.md) for checks and review limits.

## Use

Select EXP-064 or EXP-189 through the existing expression API, loopback input or expression-cycle keys, then use the existing gaze controls:

- V: pointer-driven iris gaze.
- `gaze_x`, `gaze_y`: numbers in [-1,1]. Positive X looks screen-right; positive Y looks down.
- Y / `look_x`, `look_y`: the existing eyes-first attention control now also moves the irises of these two selected expressions.
- Independent blink/wink hides the corresponding gaze layers and uses the expression's own closed-eye artwork. Mouth and speech controls remain separate.
- Reset returns to the approved neutral expression and centers gaze.

With the existing `--live-input` opt-in:

    python send_live.py --seq 1 '{"expression":"EXP-064","gaze_x":-0.7,"gaze_y":0.2}'

Existing timed gaze cues work on a supported expression selected before the clip starts. This revision does not add expression-selection cues to the clip format. Pausing freezes motion; changing the selected expression while paused refreshes the matching eye textures and neutral-only brow gate without advancing the clock or moving the drivers.

## Composition

The two expressions have their own iris, sclera and aperture textures. The fixed aperture is limited to the small safe eye interior required for travel. Every moving iris texel receives the same translation; there is no scaling, shear, pupil resizing or eye-interior UV warp.

Visible iris detail comes from that expression's original pixels, never from the neutral eye. Only the sclera hidden behind the original iris is reconstructed from neighboring sclera. This is an underpaint approximation, not recovery of unseen source artwork.

The runtime swaps the six existing eye samplers when the selected expression changes. It adds no shader samplers and leaves the deformation shader, facial controller and expression registration unchanged. Unsupported expressions disable these overlays rather than replacing their eyes with neutral ones.

`tools/build_expression_gaze_layers.py` reproduces the derivative assets from preserved source artwork. `test_expression_gaze.gd` checks profile selection, every unsupported expression, blink/mouth independence, repeated switches, look-at, paused selection, reset, timed gaze cues and real loopback delivery/timeout.

## Review limits

This is not general gaze support for all 93 expressions. The remaining expressions include partly hidden irises, closed eyes, winks, deliberate eye directions and very different eye shapes. Each would need appropriate rig layers and separate validation. The neutral-only guard is retained for them.

Native-speed playback was unavailable to the assistant. Review used decoded chronological frames, enlarged eye comparisons, source-preservation checks and actual Godot state logs. The user approved the review before publication. Desktop Godot rendering is verified for this revision; low-limit graphics hardware and real-time performance remain unverified.

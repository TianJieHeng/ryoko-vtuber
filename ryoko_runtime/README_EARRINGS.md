# Approved independent hanging earrings

Built on approved main `d87d5b696ee8afaff6a1b279dd75ad04d7e5beac`. The original [handoff](https://github.com/TianJieHeng/ryoko-vtuber/blob/d87d5b696ee8afaff6a1b279dd75ad04d7e5beac/ryoko_2d/HANDOFF.md) calls for hair and accessory motion. This addition separates the two long earrings below their fixed ear studs, allowing restrained rigid sway instead of rotating each whole earring with the head.

The user reviewed the full runtime footage and close-up and approved this revision on 2026-11-05. It preserves the approved bust controls and all 93 existing expressions. No full-body or new expression work is included.

## Controls

- **Shift+F:** enable/disable both earrings. Plain F retains the crown/bun hair toggle.
- API, opt-in loopback input and version-1 timed clips: `earring_secondary: true` or `false`.
- Off uses the original attached artwork, not a replacement layer.
- R / `reset: true`: clear earring dynamics along with the other channels. Reset, clip cancellation and input timeout preserve the enabled/disabled preference.
- A paused clip freezes the complete rig, including both earrings. Manual Shift+F takes over from a running clip.

Example local command with the existing `--live-input` opt-in:

    python send_live.py --seq 1 '{"earring_secondary":true,"head_tilt":0.7,"body_tilt":0}'

The original loopback-only binding, typed validation and timeout behavior are unchanged. No socket is opened by default.

## Rig and artwork

- Fixed ear studs remain part of the face. Hanging pivots are `(409,602)` and `(716,600)` in the `1136 × 1384` source canvas.
- Each hanging piece is a rigid Sprite2D with its own pendulum state. It follows the deformed ear attachment and responds to horizontal acceleration. At a held head tilt it settles toward vertical instead of remaining tilted with the head.
- No idle sine wave is added. Swing is bounded to 6 degrees and total relative rotation to 15 degrees; the solver uses 240 Hz substeps, caps large-delta impulses and rejects non-finite inputs.
- All 606 approved PNGs remain byte-identical. Four derivative PNGs supply two rigid cutouts, a packed RGBA underpaint and a packed RG clear mask. The original source remains intact.
- At zero relative angle or with the feature disabled, the shader bypasses the derivative layers entirely. GPU-rendered neutral on/off captures are pixel-identical.
- Away from zero, the shader replaces only the masked earring region with reconstructed hair/background and overlays the moving rigid cutout. Source alpha is respected rather than painting an opaque rectangle behind the pendant.

The reproducible Python helper is `tools/build_earring_layers.py` (Pillow, NumPy and SciPy). It writes derivative assets and local validation/review output, never changes the source PNGs, verifies disjoint masks and checks the fixed studs.

## Visual limitations

The original artwork does not contain the hair hidden by the earrings. Small exposed patches are interpolated in premultiplied RGBA, not recovered original hair. Enlarged crops show some smooth fill. Cutouts retain a restrained fringe and tiny source hair islands inside the links, which can move with the gold at enlargement. Fractional-alpha edges are not an exact neutral reconstruction when the derivative layers are active; the exact-original bypass avoids changing a stationary neutral pose.

The two sides share packed underpaint and mask textures to reduce sampler use. Rendering was tested in desktop Godot OpenGL with Mesa llvmpipe. The inherited facial shader plus these layers still has a high sampler count; low-limit graphics devices and WebGL are unverified. The movie writer ran slower than real time, so the recording does not establish native playback performance.

This is restrained 2D accessory motion, not a collision solver, 3D chain rig or individually articulated metal links. It has no hair/neck collision detection. The necklace remains in the original artwork. Native-speed playback is unavailable to the assistant; chronological decoded frames, enlarged crops, state logs and tests support review, and the user reviewed and approved the actual MP4 before publication.

## Runtime proof and tests

`review_earrings.gd` drives the actual Godot runtime through original off/on neutral, head reversals, torso motion, held tilt, off/on at tilt, combined look/brow/breath/mouth controls, and reset. `capture_earring_qa.gd` captures exact neutral comparison, maximum held tilt, reversal and an existing expression with blink.

    godot --headless --path . --script res://test_earrings.gd

The new suite checks independent dynamics, settling, bounds, invalid inputs, stalls, exact attachment positions, rigid scale, combined approved controls, clip pause, reset, keyboard separation, typed clip input and real loopback delivery/timeout. See `VALIDATION_EARRINGS.md` for measured results.

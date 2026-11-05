# Approved earring validation

User-approved revision based on approved `d87d5b696ee8afaff6a1b279dd75ad04d7e5beac`, 2026-11-05. The user reviewed and approved the full runtime MP4 and close-up before publication.

## Automated checks

All 21 local Godot 4.6.3 suites passed: 134,106 counted checks plus the existing bounce amplitude/settling suite. The new earring suite passed 2,065 checks with zero failures. It also covers hidden cutouts before their first attachment update, fixing a pre-existing hairpin flash at the viewport origin on the first frame.

Coverage includes stationary settling, independent left/right acceleration response, angular limits, invalid inputs, large frame deltas, fixed deformed attachment positions, combined gaze/brows/breath/mouth/head/body controls, rigid scale, held gravity alignment, clip pause freezing, reset preserving the toggle, separate F/Shift+F controls, typed UDP/clip validation, actual loopback delivery and timeout release. Existing clip ownership/cancellation, facial, gaze, look-at, breath, brow, hair, ornament, torso, gesture, audio and pose suites passed unchanged.

All 606 inherited PNGs are SHA-256-identical to the approved project. Four new derivative PNGs are scoped to the earrings. Their clear masks do not overlap; source pixels outside them and fixed upper studs are unchanged.

## GPU evidence

Actual Godot OpenGL movie writer output, encoded to H.264 MP4 by FFmpeg: 26.033 seconds, 781 frames at 30 fps, 568 × 760. The enlarged detail movie is a crop of that same runtime footage, not a separate composited animation. Recording reached `EARRING_REVIEW_COMPLETE` with no script or shader errors. The local llvmpipe display emits an unsupported V-Sync warning, which does not affect fixed-frame recording.

Enabled and disabled neutral GPU captures have **zero differing pixels**. All five static GPU captures are also pixel-identical before and after packing the shader textures. Maximum held tilt, reversal, combined controls and an existing expression/blink have separate GPU captures. Chronological decoded frames and enlarged attachment crops are used for inspection; native-speed playback is unavailable to the assistant.

## Known quality limits

Underpaint uses harmonic premultiplied RGBA interpolation where the original hair is hidden. Smooth fill patches and small source edge fringes are visible in enlarged crops. The derivatives are not a pixel-perfect neutral reconstruction at fractional-alpha edges, so zero-angle/disabled rendering uses the original source directly. User approval of the visual result does not imply clean hand-painted separation or collision-aware physics. No full-body, necklace rigging or new expression artwork is included.

No CI, paid resources or remote-machine execution was used. Publication was authorized after visual review.

The packed earring layers add two shader samplers instead of four. The inherited facial layers already consume many samplers and Godot reserves additional units, so this is not a claim of 16-unit/WebGL portability. Validation used desktop Godot with llvmpipe only. Fixed-frame movie recording was slower than real time and is not a playback performance benchmark.

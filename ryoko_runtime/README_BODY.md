# Independent head and torso controls

Based on approved audio-mouth commit 57f14bb. No new artwork, expression changes or deformation-shader changes.

## Controls
- A/D and arrow keys retain their existing head controls.
- Q/E: torso tilt; W/S: torso vertical offset; Z/C: torso horizontal offset. Using any of these switches to independent torso control. Release returns that torso axis to neutral.
- H: restore automatic torso following of the head.
- R: reset everything and restore the approved follow behavior.
- Existing mouth/audio, blink, expression and mouse controls remain available.

## Local API
`apply_controls` accepts `body_tilt`, `body_x`, and `body_y` in [-1,1]. Supplying any of them switches off automatic torso following; unspecified axes retain their target values. `body_follow: true` restores following. If supplied together, `body_follow` takes precedence. Non-finite body values become zero.

The default is still the approved head/torso follow relationship. Both channels have the same 0.22-second monotonic easing. Torso tilt is bounded to 3 degrees, horizontal motion to 8 source pixels and vertical motion to 5 source pixels; head-relative tilt remains bounded to 6 degrees. Shoulders and chest remain in one upper-torso transform. Independent control does not introduce chest stretching or separate shoulder rotation.

For an upright head on a tilted torso, use `head_tilt = -0.5 * body_tilt`. These are local 2D controls, not 3D yaw or motion capture.

## Proof
Run with `--body-proof` after Godot's `--` separator. The 20-second runtime demonstration includes neutral, head-only motion, torso-led motion, counterbalanced head, and recovery. No synthetic speech distracts from the body test.

`test_body_controls.gd` adds 534 checks covering legacy follow equivalence, independent transforms, shoulder/chest distances, bottom anchoring, head counterbalance, finite bounds, persistence, easing, audio coexistence, reset and physical key input. All previous 62,173 checks also pass.

Approved by the user on 2026-11-05. Published with existing artwork, audio controls and default body-follow behavior preserved.

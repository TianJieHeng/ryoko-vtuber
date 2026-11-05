# Rigid hanging hairpin ornament

The gold ornament hanging from the screen-right hair stick is now a separate rigid cutout, attached at the first chain link. It reacts to head/body acceleration and gravity, then settles. It does not run an idle oscillation.

The user approved this runtime proof on 2026-11-05. The feature is integrated with rigid gaze, look-at, breathing and brows. No full-body changes, CI, paid resources, remote-machine execution or new expression artwork are included.

## Controls

- **Shift+O:** toggle ornament motion. O alone retains the independent brow control. Off restores the original attached artwork.
- **R / `reset: true`:** clear its dynamics together with the other rig channels.
- API / opt-in loopback input: `ornament_secondary: true` or `false`.
- All existing head, torso, bounce, facial expression, blink, gaze, gesture, audio, and clip controls remain.

Example local command:

    python send_live.py --seq 1 '{"ornament_secondary":true,"head_tilt":0.6,"body_tilt":0}'

As before, the runtime only listens with `--live-input`. It binds to `127.0.0.1:9122`, and the adapter rejects invalid packet types. A two-second input timeout resets dynamics and releases live poses. Reset preserves the user's enabled/disabled ornament setting, as with hair and chest secondary motion.

## Implementation

- Source rectangle: `(781,184,22,131)` in the existing `1136 × 1384` face viewport.
- Attachment pivot: `(790.5,184)` in source pixels.
- The original pin, bun, face, and body pixels are untouched.
- A Sprite2D samples the existing viewport directly. No bitmap is regenerated or edited. All 600 existing PNGs remain byte-identical.
- The source ornament rectangle is hidden only while the separate cutout is active. Disabled mode uses the exact original shader sampling and artwork.
- The pivot follows the head, torso, crown-hair root motion, and torso lift. Its world rotation includes the head/body frame plus the damped relative angle.
- Gravity cancels a held head tilt so the pendant hangs vertically. Small anchor acceleration produces a restrained swing. Swing is limited to 9 degrees, and total relative rotation to 14 degrees.
- The damped solver uses 240 Hz substeps and bounds impulses from stalls or discontinuous commands. A stationary anchor settles to zero swing.

Only the hanging hairpin ornament is added here. Earrings and the necklace remain part of the original artwork. This is a 2D rig feature, not camera tracking or a completed full-body rig.

## Run and verify

Open `project.godot` in Godot 4.6 or run:

    godot --path .
    godot --path . -- --ornament-proof
    godot --headless --path . --script res://test_ornament.gd

The proof runs for 20 seconds: neutral, head left, head right, torso/lift, held settle, disabled baseline, and reset. The MP4 is actual Godot OpenGL movie-writer output encoded by FFmpeg. The detail MP4 is a crop of the same rendered footage.

Validation includes the 826-check ornament suite, all 14 inherited suites, actual loopback UDP toggling, and rendered on/off comparisons. The neutral GPU captures have zero differing pixels between enabled and disabled modes. Review used chronological decoded frames and enlarged attachment crops. Native-speed playback was unavailable to the assistant; the user reviewed and approved the supplied runtime MP4.

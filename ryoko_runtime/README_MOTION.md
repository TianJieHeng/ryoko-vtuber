# Ryoko live 2D motion rig

Based on the published `ryoko_runtime` project at df32fd48c493accb2da85d02b02c46b3ae3cff4c. All 594 artwork PNGs and the 93 expression registrations are byte-identical to that baseline. No experimental eye/hair edits are included.

## Run
Open project.godot in Godot 4.6 and run the project. It starts the interactive motion rig, not the scripted proof.

- A / D: lean and tilt.
- Arrow keys: horizontal/vertical head positioning with small upper-body follow.
- M: toggle mouse follow.
- Hold B: blink.
- Hold Space: demonstrate mouth shapes (silent, not audio lip-sync).
- Comma / period: select existing expressions.
- R: release controls and smoothly return to neutral.

The API is `apply_controls(dictionary)` on MotionRig. Commands persist until replaced or keyboard/mouse controls take over. Supported fields: head_tilt, head_x, head_y (clamped -1..1); expression; mouth; speech_active; blink; auto_blink; reset. Multiple fields can be sent together.

## Motion model
The facial layers render into a transparent SubViewport. A 1,353-vertex mesh deforms that live texture. All facial layers share the same transform, so eyes, mouths and blinks remain registered during motion.

Head-relative motion blends only through the neck (source y710..855). Shoulders, clavicles, clothing and chest share one rigid upper-torso frame through y1260; only the lower abdomen blends to the anchored bottom edge. Head tilt is limited to 6 degrees relative to a 3-degree upper-body lean. Breathing is a tiny shared upper-body rise, not independent chest stretching.

Controls settle with a monotonic exponential response (0.22-second time constant), with no spring overshoot. The proof uses discrete held poses, not continuous sinusoidal head sweeps.

This is a bounded frontal 2D rig approximation, not a 3D anatomical model or independent skeletal arms/hair physics. Webcam tracking, microphone analysis and a network listener are not included. Those can feed the local control API through a future adapter.

## Proof and tests
Run `godot --path . --fixed-fps 30 --write-movie motion.avi -- --motion-proof` for the 25-second proof. Its log is saved to user://motion_proof.jsonl. The default app remains interactive.

Run headless scripts test_motion_rig.gd, test_controls.gd and test_expressions.gd. Results: 3,204 coupled-motion checks, 89 baseline facial checks and 58,504 expression checks passed. Tests cover shared shoulder/chest coordinates and pairwise distances, bottom anchoring, monotonic settling, no overshoot, control clamping/persistence, combined commands, blink/reset, and physical keyboard press/release.

Revision status: revised motion approved by the user on 2026-11-05. Published with the existing artwork and expression controls unchanged.

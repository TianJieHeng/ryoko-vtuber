# One-shot gestures

Based on approved whole-chest rig f5704d7. Existing head/body controls, audio mouth driver, bounce and chest secondary behavior are preserved. No artwork or expression changes.

- N: one acknowledgment dip. This is a small frontal 2D head dip, not a simulated 3D pitch rotation.
- G: one greeting lean and return.
- Escape: cancel the gesture and ease back to the current live pose.
- R: reset all controls, including the gesture.

The local API accepts `gesture: "acknowledge"` or `gesture: "greet"`, optional `gesture_strength` from 0 to 1, and `gesture_cancel: true`. Unknown names return false without replacing a current gesture. A valid new trigger replaces the current gesture. There is no queue, automatic repetition, expression switching or speech triggering.

Gestures add bounded head/body offsets to the current control targets without overwriting them. Existing 0.22-second rig easing smooths entry, cancellation and replacement. After a gesture finishes, the rig returns to the current live targets, which may have changed while it played. Final combined controls stay in [-1,1]. Secondary chest motion continues to respond to the resulting torso movement.

`--gesture-proof` runs a 16-second actual runtime sequence: rest, acknowledgment dip, greeting lean, a nonzero live pose, and an interrupted gesture returning to that pose.

`test_gestures.gd` adds 256 checks for bounded finite offsets, one-shot completion, intensity handling, invalid names, preserved live targets, return, cancellation, audio coexistence, reset and keyboard triggering. Previous motion, body, audio, expressions, chest and bounce suites also pass.

Approved by the user on 2026-11-05 and published with existing artwork and whole-chest behavior preserved.

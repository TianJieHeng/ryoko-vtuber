# Reusable head/body pose presets

Based on approved eyelid rig e896dac. No artwork, expressions, gesture curves, audio driver or secondary-motion changes.

## Use
- Ctrl+1, Ctrl+2, Ctrl+3 save the current head/body control targets into that slot.
- 1, 2, 3 recall the slot with the existing smooth easing.
- R returns the rig to neutral without deleting saved slots.
- Existing gestures, eyelids, audio and chest motion continue over a recalled pose.

The API accepts `pose_save: 1` or `pose_load: 1` (slots 1–3). Saves in a combined control command happen after the new targets are applied. Loads happen before explicit head/body fields, so explicit fields can override a recalled component. Empty slots return false and leave the pose untouched. Status appears below the normal control hints.

Presets store head tilt/position, torso tilt/position and automatic body-follow mode. They store control targets, not a freeze-frame of an in-flight gesture, blink, bounce, mouth shape or expression. This keeps a recalled pose compatible with live animation. Recall takes control from mouse following; normal movement keys or M can take control again.

The three slots persist in Godot's user data directory as `rig_poses.json`. A temporary-file rename is used when saving; invalid input is rejected. Invalid file contents are reported without replacing the file during loading. The demonstration uses a separate `proof_poses.json`, so it cannot overwrite the user's interactive slots.

`--pose-proof` captures an actual 20-second sequence saving two poses, returning to neutral, recalling each pose and playing an acknowledgment dip over the second pose.

`test_pose_store.gd` adds 165 checks covering fresh-instance persistence, exact round trips, snapshot isolation, invalid slots/data/files, smooth recall, stable targets, settling, gesture/eyelid/audio coexistence, reset and keyboard recall. All prior test suites also pass.

Approved by the user on 2026-11-05 and published with previous rig behavior and artwork preserved.

# Coordinated look-at rig

Eyes acquire a normalized target immediately; the head begins to follow after a 180 ms acquisition delay. Motion eases toward a held pose, without an idle loop. Iris layers translate rigidly, retaining the approved fixed eyelid/hair masks. This is stylized 2D attention, not a 3D head turn or camera face tracking.

- Press Y to toggle pointer look-at. Press it again to release smoothly.
- API / opt-in loopback input: `look_x` and `look_y` in [-1,1], screen-right/down positive.
- `look_release: true` smoothly returns the attention overlay to zero, retaining the underlying pose.
- R / `reset: true` clears it immediately, as with other rig controls.
- V switches to the existing independent eye pointer control and releases look-at.

The overlay adds restrained head tilt/translation and eye offset to the existing pose. It never drives the torso. The existing head/body, gestures, eyelids, mouth and hair controls remain available. Extreme combinations are clamped to the original head and gaze limits. Authored non-neutral expressions still use their existing eyes; gaze is available on the neutral eyes only.

This user-approved feature is integrated with rigid iris gaze, controlled breathing, brows and hairpin ornament. All 600 inherited PNG files are unchanged; the six approved brow derivative textures are additional assets. No new expression art is made.

Run `godot --path . res://motion_rig.tscn -- --look-proof` for the 18-second runtime sequence. Tests: `godot --headless --path . --script res://test_look_at.gd` plus all prior suites.

Visual review uses chronological decoded frames and enlarged eye crops. Native-speed playback was unavailable. The user reviewed and approved the runtime proof on 2026-11-05 before publication.

# Base control API

Call object_rig.apply_controls(dictionary). It returns true on success and false without state mutation if any key/value is invalid. last_error describes rejection.

## Accepted controls

- reset and auto_blink: boolean. Reset restores original neutral lips, centered gaze, open eyes, resting brows/hair, and disables auto-blink.
- blink, blink_L, blink_R: continuous closure in[0, 1]. 0 = open, 1 = closed. L/R retain anatomical naming: L is screen-right, R is screen-left.
- gaze_x, gaze_y:[-1, 1], bounded rigid iris translation of 6×2 source pixels.
- brow_raise, brow_screen_left, brow_screen_right:[-1, 1], bounded rigid brow translation of 10 source pixels.
- brow_tilt_screen_left, brow_tilt_screen_right:[-1, 1], rigid rotation up to 8 degrees around each recorded pivot.
- hair_sway:[-1, 1], individual source-part rotations up to 0.6 degrees fringe,1.6 degrees temple locks,2 degrees short tail,0.4 degrees bun and 0.25 degrees rear scalp. These are restrained generic controls, not the previous secondary-motion implementation.
- mouth or viseme: A,E,I,O,U selects one original mouth variant. REST, RELEASE or NEUTRAL restores the original neutral-lips object. Only one mouth object is visible.

Example:

    rig.apply_controls({"reset": true, "blink_R": 0.4, "gaze_x": -0.8, "brow_screen_left": 0.5})
    rig.apply_controls({"mouth": "E"})
    rig.apply_controls({"mouth": "REST"})

When auto-blink is enabled, its smoothly timed closure combines with manual closure as a floor. It can close an eye further; it does not force a manually closed eye open. All controls use the same independent objects.

## Rejected/deferred controls

expression, perform_expression and every legacy expression ID are deliberately unavailable. mouth_open is deliberately unavailable: continuous oral opening must be authored after the base is published without replacing natural neutral lips or introducing a threshold pop. Other legacy head/body/effect/preset/live controls also reject rather than silently falling back to old rendering.

## Registration and ownership

rig_assets/object_face/manifest.json records source hashes, visible-core crops, fixed registered size/position, drawing order, parent and pivot for each object. Alpha cleanup removes faint extraction residue at 16/255 before registration. This fixed source preparation is not runtime deformation.

The eye shader samples original UVs and clips alpha only. No skin or hair pixels are in the moving brow, iris, sclera or lash source objects. Face/nose/jaw remain one stationary clean foundation. Six hair objects own the hairstyle, and the neck/torso derivative excludes old baked hair. Ears and accessories are separately inspectable. body remains fixed; its neck silhouette is a deliberate visible-source crop, not new hidden-neck artwork.

No performance timelines are part of this project. Generic base functionality and source appearance must not be mistaken for 93 migrated/approved emotions.

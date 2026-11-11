# Full-body wiring v1 — unapproved review

This is an additive manual rigging checkpoint based on approved main `c976b11ea42d6de984242444212259cafa84e17c`. It is not a new approved release. No existing approved runtime, facial profile, scene, shader or artwork is changed. The default expression app remains unchanged.

## Open the workbench

From `ryoko_object_rig` with Godot 4.6.3:

```sh
godot --path . full_body/full_body_viewer.tscn
```

Full body, Bust and Head buttons frame the same live rig. The overlay shows skeletal attachment points. Body sliders apply small manual joint rotations; face sliders operate the unchanged approved controller. Reset all restores both body and face. Reset body leaves the face alone. There is no action library, gesture choreography, automatic sway, jumping or new expression here.

## What is wired

- 17 named Bone2D joints: pelvis, spine, chest, neck, head and paired shoulder/elbow/wrist/hip/knee/ankle chains.
- 17 registered body sprites, with explicit source provenance, alpha bounds, position, fixed bind scale, pivot parent and draw order in `registration.json`.
- The existing live head and all 263 independent face sprites are attached to the head bone. Its native local geometry and all 47 approved facial profiles remain unchanged.
- The old fixed bust sprite is hidden in this new scene only. Registered suit, arms, hands, pelvis, legs and shoes replace its cropped torso. Approved neck/chest/necklace pixels are retained through the blouse opening, with a real source collar underlap.
- An anatomical-left joint is on screen right. Body sprite z values are negative; the existing face stack retains its own positive indices.
- Bone scales remain one. Layer and head scales are fixed registration transforms, never animated deformations.

The retained `ryoko_2d_update` registered body artwork already matches the character and costume. This checkpoint reuses those source cuts rather than creating a replacement character. Derived copies live under `assets/`; originals are unchanged. Knee splits duplicate 56 source pixels, giving 28 canvas pixels of overlap. Hand-edge matte cleanup changes only derived copies.


## Head-proportion correction

The first review preview used an undersized head and was not approved. This revision increases the functional head uniformly from .285 to .320 (+12.3%), at origin [329,4], keeping its chin attachment near [510,234]. Body/suit dimensions and the independently fitted neck/chest are unchanged. The original full-body master's crown is at approximately canvas y29, the rejected preview at y51, and this correction at y28. With chin near y234, crown-to-chin / shoulder-span ratio is .641 in the reference and .644 after correction. The hair-width proxy remains about 5% wider than the source, reflecting the retained approved head artwork. See assets/proportion_source_comparison.png. This correction is still awaiting user review.


## Arm-ownership correction

The first arm preview exposed a second, torso-owned sleeve beneath the moving arm. Both sides now have that static sleeve removed from the derived torso garment. Upper and lower sleeves are re-cut from the original full-body reference, with a 40-canvas-pixel elbow overlap and elbow pivots at anatomical R [374,535] and L [650,535], matching the drawn creases. Jacket hems, source cuff/hand shapes and the .320 head correction are retained. See assets/arm_ownership_comparison.png and assets/arm_ownership_provenance.json. Original files remain unchanged; this corrected checkpoint is still unapproved.

## Control API

`full_body_rig.gd` wraps, rather than replaces, `expression_rig.gd`.

- `apply_controls(dictionary)`, `play_expression(id)`, `list_expressions()` and the face portion of `get_state()` delegate to the existing approved controller. A successful global reset also resets body joints.
- `apply_body_controls(dictionary)` validates the complete body request before changing anything. Numeric controls accept finite values in [-1,1]; booleans, strings, unknown keys and nonfinite numbers reject. Omitted controls retain their value. `{"reset":true}` restores body neutral before applying any supplied controls.
- Each joint's exact degree range is recorded in the manifest. Current ranges are deliberately small: head ±3°, shoulder/elbow ±2°, wrist ±3°, spine ±1.5°, chest/pelvis/knee/ankle ±1°, hips ±0.7°.
- Independent neck tilt is not advertised; the neck is attached to the chest because its current skin and collar underlap are not separated for articulation.
- `frame_x` and `frame_y` translate the whole assembly ±18 and ±10 canvas pixels. `frame_roll` rotates the whole assembly ±2° about the pelvis. This is a rigid presentation transform, not grounded locomotion or inverse kinematics.
- Facial and body requests have separate ownership. Playing a facial expression does not erase a body pose; a body slider does not cancel facial playback. This workbench does not expose a network control listener or change the original loopback bridge.

## Verification and review media

`review/headless_checks.json` records focused **actual Godot** checks: all joint endpoints, unit bone scales, invalid-request rejection, exact skeleton/face reset, live face controls while body-posed and starting/advancing all 47 existing facial profiles. The workbench also passes headless load.

`review/ryoko_full_body_wiring_v1.mp4` is explicitly a **CPU layer composite**, not a native Godot capture. Body/head transforms come from actual engine nodes sampled by `tests/sample_wiring.gd`. Its neutral head is a source-derived diagnostic image; the movie does not demonstrate animated facial shaders. The bust panel is a crop from the same composited frame. The clip only sweeps small attachment/joint/frame ranges; it is not an authored action.

Local native rendering could not start because the X display could not create its listening sockets, including an escalated attempt. No alternate socket route was used. Therefore native pixels, interactive UI appearance, smooth real-time pacing and joint-seam quality in the native renderer remain unverified. CPU light/dark neutral and ±3° head-tilt checks are useful assembly diagnostics, not native-render proof.

Known boundaries: front-facing cutouts only, no yaw/pitch drawing set, no large joint ranges, no new hidden-area artwork, no soft deformation, no tracking/export certification and no final visual approval. Existing source alpha/matte quality can remain visible under magnification. Final rendered seam review and any required approved overlap artwork remain next steps. No CI, paid service or remote-machine execution was used.

## Reproduce

From repository root:

```sh
python ryoko_object_rig/full_body/tools/assemble_registered_body.py
python ryoko_object_rig/full_body/tools/check_head_tilt_seams.py
godot --headless --path ryoko_object_rig --editor --import --quit
godot --headless --path ryoko_object_rig --script res://full_body/tests/test_wiring.gd
godot --headless --path ryoko_object_rig --script res://full_body/tests/sample_wiring.gd
python ryoko_object_rig/full_body/tools/render_wiring_preview.py
```

Python needs Pillow and NumPy; the preview encoder uses FFmpeg. When the host's default Godot data folders are not writable, set XDG_DATA_HOME, XDG_CONFIG_HOME and XDG_CACHE_HOME to writable local directories. No broad historical test replay is required for this additive wiring checkpoint.

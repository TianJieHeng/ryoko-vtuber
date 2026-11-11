# Full-body individual-part assembly and spring-motion review

This replaces the rejected combined-body/bust approach. The user accepted the corrected neutral pose and requested a small bounce to review jiggle physics. The new motion remains a review candidate, not an approved release. Approved main remains `c976b11ea42d6de984242444212259cafa84e17c`; its expression app, artwork, shaders and 47 profiles are unchanged.

## Actual ownership

The runtime uses individual cutouts from `avatar_build_assets/body/layers` and `accessories/layers`: blouse, blazer front L/R, upper and lower sleeves, hands, pelvis, thighs/shins, front shoes, belt, necklace chain and pendant. Front/back and alternative view drawings are not stacked. The final sleeve fit is in `elbow_review`: painted elbow folds are registered to one anatomical joint, not to the forearm image’s construction top. The upper sleeve’s open tube end is excluded, forearm overlap sits behind it, and the original hands sit inside the opened cuffs. The source PNGs have independent scale/framing and faint alpha outliers; the build records cleanup, source hashes, crop, bind transform, parent, pivot and draw order.

`pieces_v2/upper` and `pieces_v2/lower` contain reproducible cutout/registration scripts and isolated assets. The final jacket override is built by `jacket_review/build_candidate.py`: it cuts exterior panels along their painted lapel seams, excludes the inner-facing strips, and registers collar/shoulder/bust/button/hem landmarks. The blouse body and two collar tabs have complementary ownership masks; the gold fastener is its own part. Shirt side excess is tucked behind the fitted jacket, and surplus belt strap is clipped to the pelvis. The prior narrow-opening panel fit is superseded. Trouser legs have overlapping knee splits; the pelvis construction hem is feathered into matching leg artwork. This is an editable 2D cutout rig. Five existing upper-body owners now use textured deformation grids for secondary motion; there is no duplicate artwork or 3D character.

The asset pack explicitly lacks standalone neck/chest skin. `pieces_v2/upper/sources` retains a new unapproved compatible edit that removes baked necklace artwork. Its runtime derivative is masked to skin only, with a documented hidden upper extension. No collar, blouse or jacket is retained in that part. The raw chain and pendant are separate owners.

The existing live head and all face-control objects are attached to the head bone at fixed scale .32. The legacy `FixedNeckTorso` node is **freed**, not hidden or overlaid. The live backing owns face/ears and most earrings, but no clothing. Exact final earring-tip pixels formerly stored in the torso texture are isolated into two head children. `pieces_v2/head_audit` records the alpha audit and masks. Earrings are not yet fully independent articulation owners.

## Runtime

Open from `ryoko_object_rig` with Godot 4.6.3:

```sh
godot --path . full_body/full_body_viewer.tscn
```

Full body, Bust and Head frame the same scene. The workbench offers manual joint sliders, existing face sliders, an attachment overlay, body-only reset and global reset. There is no action library. The optional Small bounce button triggers the requested short vertical motion and its spring response; it does not play automatically.

Seventeen unit-scale Bone2D owners form pelvis/spine/chest/neck/head and paired shoulder/elbow/wrist/hip/knee/ankle chains. `registration.json` is the complete bind manifest. Draw order is explicit; body layers remain behind the existing head stack.

`apply_controls`, `play_expression` and `list_expressions` delegate to the approved face controller. `apply_body_controls` validates the whole request atomically and accepts finite normalized values in [-1,1]. Face and body control ownership remain separate. Small joint ranges are calibration limits, not proof of large-pose coverage. `frame_x/y` translate the assembly; whole-frame roll has been removed. No tracking bridge, network listener or default project entry point is changed.

## Verification and limits

`review/headless_checks.json` records focused actual Godot checks for bind ownership, joint endpoints, atomic validation, resets, independent face/body controls and all 47 facial profiles. These numerical checks do not prove visual quality.

`review/ryoko_full_body_wiring_v1.mp4` is a **CPU cutout composite driven by actual Godot transforms**. The diagnostic head is neutral source artwork, not animated native facial shader output. The close-up is a crop of the same assembled frame. The current review clip is a four-second neutral hold with full-body and sleeve detail, without gestures or movement. The optional sampler flag `--joint-checks` enables isolated head/elbow diagnostics for development; it is not used in this neutral review clip. No coupled limb demo or leaning sequence remains.

Native capture could not start because the local X display could not create its listening sockets. Native pixels, interactive appearance and real-time pacing are unverified. This is not a completed tracking/export rig. Current frontal art and tiny overlap ranges do not support large rotations, head yaw/pitch or new actions. Source shading and silhouette differ from the original combined illustration and require review. The neutral pose was accepted. Approval of the new spring motion is not assumed.

## Reproduce

```sh
python ryoko_object_rig/full_body/pieces_v2/upper/assemble_upper.py
python ryoko_object_rig/full_body/pieces_v2/lower/assemble_lower.py
python ryoko_object_rig/full_body/pieces_v2/head_audit/extract_earring_tips.py
python ryoko_object_rig/full_body/jacket_review/build_candidate.py
python ryoko_object_rig/full_body/elbow_review/build_candidate.py
python ryoko_object_rig/full_body/tools/assemble_from_parts.py
godot --headless --path ryoko_object_rig --editor --import --quit
godot --headless --path ryoko_object_rig --script res://full_body/tests/test_wiring.gd
godot --headless --path ryoko_object_rig --script res://full_body/tests/sample_wiring.gd
python ryoko_object_rig/full_body/tools/render_wiring_preview.py
```

Python uses Pillow, NumPy and SciPy; the preview encoder uses FFmpeg. Set XDG_DATA_HOME, XDG_CONFIG_HOME and XDG_CACHE_HOME to writable folders if required locally. No CI or remote-machine execution is needed.

## Small bounce / real secondary-motion simulation

The new optional bounce uses two small vertical root pulses. Damped mass-spring states are integrated in the actual Godot runtime at 120 Hz and driven by root acceleration. The clothed chest has a smooth shared deformation field across the existing blouse, blazer panels and skin owner, anchored away from the neck, shoulders and waist. The chain deforms from a fixed upper attachment toward the independently spring-driven pendant. Reset restores the neutral pose and clears all spring state.

`review/ryoko_small_bounce_jiggle_v1.mp4` is a new motion review, separate from the accepted neutral-pose clip. Its spring states, layer transforms, triangle topology and every deformed mesh vertex are sampled from Godot. The Python renderer rasterizes those sampled triangles; it does not invent an independent jiggle curve. This is still a **CPU-rendered approximation of the engine's visuals**, not a native Godot screen recording. The face is the same neutral diagnostic source. Native renderer parity, live playback pacing and tracking integration remain unverified.

To reproduce the motion sample and movie:

```sh
godot --headless --path ryoko_object_rig --script res://full_body/tests/sample_bounce.gd
python ryoko_object_rig/full_body/tools/render_bounce_preview.py
```

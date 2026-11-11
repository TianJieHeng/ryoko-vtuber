# EXP-123 Puzzled native capture review

Status: UNAPPROVED preview candidate. Native capture and media validation pass; this is not artistic approval or integration.

## Artifact

- `Puzzled_review_v1.mp4`: H.264/yuv420p, 968 × 800, 30 fps, 121 frames, 4.033333 seconds, 182,736 bytes.
- SHA-256: `5df48deb24bc3a86084799084fd65a004bd7b4af4459ed1eea6d838225930db3`.
- Source performance spans exactly 4.0 seconds; endpoint-inclusive encoding accounts for the extra frame.

## Native workflow observed

The prepared `native_launcher/project.godot` was imported through the existing Godot Project Manager using supported CUA/Sky desktop input. The original Game Embed Mode was visibly Use Per-Project Configuration. It was temporarily changed to Disabled, the project was reloaded, and Run Project was invoked from the editor. A standalone Puzzled game window was observed rendering the face and completing capture. No shell-native launch, display server, socket, remote executor, or CI was used.

Native receipts passed: 1,526 static checks and 9,387 motion checks; X11, llvmpipe (LLVM 19.1.7, 256 bits). There are sixteen static PNGs and 121 RGBA motion PNGs for each exact-size view: full 568 × 800 and detail 400 × 360. The game was closed and the editor displayed Debugging process stopped. The original Game Embed Mode was visibly restored, and the Puzzled editor was exited to Project Manager.

Godot rewrote launcher project configuration section order/whitespace without changing values. The independent reviewer archived the changed config, exact diff and initial failed guard, then restored the exact frozen prepared bytes after editor exit. See `review_evidence/launcher_import_audit/`. No freeze or validation threshold was changed.

## Validation

The existing encoder passed its capture guards and encoded only the captured PNGs. Its complete ffmpeg decode passed. Independent validation passed all 73 checks, including all 242 native RGBA hashes, exact neutral holds, fixed body pixels, static/motion agreement, independent timeline/geometry calculations, 121 cleanly decoded MP4 frames, monotonic 30 fps timestamps, and same-index native/decoded panel comparisons. The operator reran that independent validator to `capture_operator_review/`; it also passed with no failures or pending checks.

All 999 frozen source files including 184 PNGs remain unchanged in both baseline and copied rig; the 36-profile registry is unchanged and Puzzled is absent. This separate candidate is not an approved39 integration.

## Visual inspection and limits

The original nine-panel source sheet, all eight captured detail anchors, nine decoded keyframe details and four bust progression frames were visually inspected. The candidate visibly gathers a one-sided questioning brow, uneven squint and compact sealed pout, holds, makes a restrained rechecking squint, and returns to neutral. Mouth/pixel views did not show an obvious new tear, open-mouth flash, or body displacement in the inspected samples.

The source's diagonal, sideways pout is only weakly approximated: peak endpoint-midpoint bias is 2 source pixels (about 0.98 bust pixels), with no whole-mouth translation and no diagonal contour. The rigid brow does not reproduce painted local curvature. Head tilt is omitted. At bust scale this reads as a restrained puzzled/skeptical look, with the mouth asymmetry less obvious than the reference. These are source-fit limitations for the user's approval decision, not cleared by numerical checks.

The MP4 was imported into the existing Kdenlive project bin. Supported UI playback was started and samples showed mid-pose and the neutral endpoint as the playhead advanced to the end. Observation was intermittent. Continuous normal-speed viewing, smooth real-time engine pacing and perceptual distinctness against every other performance remain unverified.

No upload, publication, registry update, artwork change, shader change or runtime change was performed by this capture task. UI ownership was released after playback inspection.

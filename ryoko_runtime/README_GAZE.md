# Rigid independent iris motion

User-approved revision based on approved main c940508, replacing the rejected eye-interior warp. The prior shader distorted the lower iris during horizontal glances. This revision translates a fixed iris texture for each eye; no eye-interior UV warp remains.

## Controls and composition

- V toggles pointer-driven gaze, independent of M head-follow.
- API/live UDP: gaze_x and gaze_y from -1 to 1. Positive X looks screen-right; positive Y looks down.
- R/reset returns gaze to center. Controls ease over 0.12 seconds.
- Maximum translation is seven source pixels horizontally and two vertically. Every iris texel receives the same offset, with no scale, shear or per-pixel deformation.
- Fixed eye-aperture masks clip the moving iris under the upper/lower eyelids. The screen-left foreground hair strand is excluded from the mask and stays in front.
- Each closed eyelid disables its own gaze layers. Non-neutral expression presets use their unchanged authored artwork and eye direction.

The neutral bust source contains baked-in irises, not separate complete circles or hidden sclera. The six new rig_assets textures therefore include a reconstructed sclera background and small reconstructed upper/strand-covered iris regions. Visible lower iris and pupil detail is sampled from the original image without stretching. Hidden texture is filled from neighboring visible iris colors; it is not an exact recovery of unseen original artwork. The separated neutral eye is used consistently at center and during glances so it cannot morph between the original and separated rendering as gaze starts.

All 594 original artwork PNGs remain unchanged. The neutral eye cleanup is a reviewable derivative, not a new expression or a claim of pixel-identical neutral compositing. The original source and rejected warp project remain available separately for comparison.

## Validation

The gaze test checks uniform translation and preserved inter-pixel distances, finite/clamped controls, easing/reset, independent mouth and blink, expression fallback, real UDP delivery and timeout centering. All prior suites are also rerun. See the accompanying test logs for actual counts.

The actual Godot proof shows centered eyes, left/right/up/down, head tilt with mouth and blink, and return to center. Enlarged comparisons are decoded from runtime videos. Review uses chronological decoded frames and eye crops; native-speed playback is unavailable here.

Visually reviewed and approved by the user before publication.

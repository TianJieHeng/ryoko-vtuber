# Canonical likeness correction

Historical checkpoint. The later local eye-part/gaze candidate is documented in GAZE_VALIDATION.md; its derived owners supersede the zero-gaze limitation below without replacing any original PNG.

This correction restores the approved original bust rather than fitting a different clean-source head to it. Source/native visual and temporal checks have passed. User approval of the delivered correction is still pending.

## What caused the rejected appearance

- The different source face crop 781×1099 had been registered as 341×410, widening its aspect ratio by 17%. The fringe and bun were widened independently by about 22%.
- The neck matte removed everything above source y700 and capped the remaining neck to 97 pixels wide at that row, against about 167 pixels in the canonical bust. The center remained connected, but artificial side gaps made the head look detached.
- The source eye outline contained both upper and lower lash contours. Sliding that entire outline downward while hiding the eye interior left skin-filled open-eye outlines at closure.
- The replacement face, nose, lashes, irises, hair and thin neutral lips were different drawings from the approved bust. Correcting scale alone could not restore the original likeness.

## What the corrected source owns

The approved bust remains immutable at 1136×1384. Face/nose/jaw/neck/outfit geometry stays at native coordinates. Four separate canonical hair owners preserve the original visible silhouette. Eyebrows, upper lashes, lower contours, irises, sclerae and closed lashes have separate owners. Hair and feature hiding are checked separately from neutral recomposition so a matching neutral cannot conceal baked duplicates.

The canonical neutral is the original bust plus its original mouth source at (480,590). The mouth feature is now recut at native coordinates instead of using the unrelated 85×13 lip line. The continuous oral mechanism retains separate upper/lower lips, cavity, teeth and tongue, with an additional stationary underlip-shadow owner. The shadow is covered by the opening cavity rather than dragged with the lower lip.

Only the upper lash moves during closure. Lower contours do not slide with it. Original closed-lash art supplies the closed contour, and visibility is clipped spatially. Texture coordinates, node opacity and local feature scales are unchanged. Foreground hair remains separately layered over the eyes.

## Reconstructed and unavailable pixels

The approved source is flattened, not a complete latent drawing of every hidden part. All inferred regions are labeled in the generated manifests and masks:

- One coherent hidden-skin field behind removed eye features and bounded rigid-hair reveal margins. Original opaque-source coverage is checked so ownership changes cannot open transparent holes.
- Internal hair seam underlaps, limited to nearby original hair colors.
- Bounded hair-edge mattes and original registered closed-source strand recuts where the neutral source was blended against dark open lashes.
- Small hair continuations hidden beneath the original outer lash wings.
- Hidden lash continuation and antialiased feature-edge mattes.
- Same-strand continuation at the left brow crossing and both ends of the right brow, where the flattened source mixes brow and hair. These masked estimates change the neutral locally; no pixel-exact original-art claim is made for them.

These are estimates, not recovered original artwork. They do not license replacing the visible original face with a different head. No upper scalp or full hidden head is invented. The original earrings remain static backing pixels.

The canonical iris/sclera layers do not yet have verified hidden travel extensions. Nonzero gaze is therefore rejected atomically, including mixed-control requests, rather than moving visibly truncated eye artwork. This is a disclosed limitation of the corrected source. Manual hair_sway is similarly limited to [−0.07,+0.07]; the yawn retains its exact −0.045 to +0.07 motion. Actual ±0.10 margin views were checked, but ±1 exposes missing hidden cheek/neck artwork and is rejected.

## Scope

EXP-163 is the only authored performance. Other legacy expression IDs remain gated. Discrete legacy source-assembly visemes are now gated in the yawn controller so no supported route bypasses the reference maximum. See MOUTH_LIMIT_CORRECTION.md. No full-body motion, tracking, head/face deformation or new EXP-005 implementation is claimed.

Published main and recovered source snapshots are unchanged. This source is not user-approved merely because control and regeneration tests pass.

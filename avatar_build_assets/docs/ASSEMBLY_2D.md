# Assemble and rig the full-body 2D character

## 1. Inspect and choose the master
Inspect the original character sheets and canonical neutral face/full-body front drawing. Choose one consistent front-facing master pose and canvas, with hands and heels visible. Maintain the supplied adult human identity and costume. Use character-left/right, not viewer-left/right.

## 2. Cut and prepare real layers
Reuse the 69 separated PNGs where suitable. Cut remaining needed parts from the retained sheets. These images have independent scale and framing: align them deliberately; do not assume they already share a registration canvas. Preserve source PNGs and save edited derivatives separately.

Prepare rear hair/scalp, bun/tail, face/neck, ears, eyes, lids/lashes, brows, mouth, front fringe/temple locks, torso/clothing panels, upper/lower arms, cuffs, hands, pelvis, legs, shoes, jewelry and optional effects. Complete areas hidden beneath moving neighbors so motion will not expose holes. A standalone neck layer is currently absent; make or obtain a compatible 2D neck part before claiming a complete assembly. Do not stretch the chin or blouse to conceal the gap.

Keep original crop metadata when useful, but do not confuse a crop rectangle with a pivot or rig-ready registration transform. Record canvas dimensions, each part's position/scale, alpha bounds, pivot, parent and drawing order in the assembled project's manifest.

## 3. Prove the assembled neutral character
Create a real composite from the actual parts. Match face/body proportions and silhouette to the references. Inspect seams and alpha edges against light and dark backgrounds. Show the complete assembled neutral character before rigging a large animation collection.

Suggested ordering is rear hair and rear accessories behind face/body; face/neck beneath ears, eye whites, irises, lids/lashes, brows and mouth; front hair and temple locks above face edges; sleeve/hand overlaps coordinated with torso; trouser/foot overlaps coordinated at hips, knees and ankles. Actual order must be tested in the chosen master pose. Use masks and parent relationships where appropriate.

The rear scalp image is a rear-view source, not a front-face overlay. Front/back and side shoe views are alternatives/construction sources. The longer temple lock is character-right. Use exactly two hairsticks. Combined necklace artwork and separate chain/pendant artwork are alternative assembly routes, not extra jewelry.

## 4. Rig the artwork in 2D
Use 2D bones/deformers and image swaps as supported by the chosen tool. If using Blender, use planar artwork with an orthographic camera; use depth only to order layers. Do not rebuild the character as a volumetric 3D mesh.

Prove breathing/body sway, head tilt, modest simulated head turns, independent blink/gaze, brows, mouth states/lip-sync, one arm gesture, hair and jewelry motion. Keep joints overlapped through their intended range. Use alternate drawings when a view or gesture cannot be represented by deforming the frontal artwork.

Implement clip masks for iris motion, compatible blink/expression channels, and mouth-swap exclusivity. Keep blush, tears, sweat, anger and sparkles individually controllable and off in neutral.

## 5. Build the performances
Use the 200 expression IDs and 40 body gesture IDs in the retained catalogues. Preserve facial intent, suggested timing, key poses and body pairings. Implement them as named presets/actions on the same assembled 2D character. The sheets are visual guides; raw crops are not pre-aligned playback frames. Register/clean any images used for actual swaps. Author transitions, holds, easing, interruptions and return to neutral, and test interaction with blink/gaze/lip-sync.

## 6. Deliver and validate
Deliver the editable layered source, individual PNGs, editable 2D rig project, registration/layer/pivot manifest, expression/action mapping and short test animations. Do not label flattened artwork a layered document. If Blender is used, provide its project with correctly linked or packed images and the orthographic scene.

A rendered animation is not by itself a live VTuber rig. Confirm the intended live 2D runtime and test live controls/export there before claiming completion. Report missing parts or tools promptly rather than repeatedly pursuing a different pipeline. No CI or paid calls without approval.

## Current limitations
No full-body registered composite, hidden-area completion, working 2D rig, tracking integration or runtime export has been verified. Native artwork sizes vary. Some painted shading must be reconciled between neighboring parts during assembly. Current PNG checks establish file/alpha integrity and crop preservation, not puppet readiness.

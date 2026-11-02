# Ryoko — full-body 2D cutout VTuber

**Build a layered 2D character from the supplied artwork, then rig that artwork.** This repository is not a volumetric 3D character project. Previous 3D build instructions and implementation files have been removed from the current branch.

All retained assembly inputs are in [avatar_build_assets/](avatar_build_assets/). Read [the 2D assembly guide](avatar_build_assets/docs/ASSEMBLY_2D.md).

## What is retained
- 69 separated transparent character/effect PNGs and 18 useful source atlases.
- Six original character reference PNGs.
- 273 reference sheets: 200 facial expressions, 40 full-body gestures, 22 facial-control studies, seven character construction references and four detail sheets.
- 2,352 extracted reference panels and 200 peak copies, plus useful expression/gesture/crop catalogues.
- Five contact sheets showing the separated parts.

## Actual readiness
The parts are **not yet aligned into a rig-ready layer stack**. Cutting, registration to a common canvas, hidden overlap completion, pivots, clipping, layered assembly and 2D rigging remain to be done. A separate neck artwork part is missing. The expression crops are acting references, not registered animation frames.

If Blender is used, use image planes or planar deformable artwork with an orthographic camera and layer-depth ordering. Do not reconstruct a 3D body, retopologize it, bake fitted character UV atlases or target a VRM character export. Choose and verify a 2D live runtime with the user before committing to its integration.

Do not replace this with a generic character. Preserve the human Ryoko design: sage/mint hair, amber eyes, dark trouser suit, white blouse, gold ornaments, green pendant and black pumps.

No CI. No paid services or API calls without approval. This cleanup is an ordinary recoverable Git commit; earlier work remains in history.

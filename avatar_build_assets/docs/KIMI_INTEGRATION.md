# Integrating the corrective art with the current Blender build

## Preserve the current work

The repository's Phase 03 and Phase 04 notes were inspected at commit `ddd41e98b502c8a7dc93073b673697d7f873f85e`. They document a retained modular 3D surface, per-part UVs and 20 interim fitted maps, plus a facial feasibility prototype with separate eyes/lids/lashes/irises/brows/lips/teeth/tongue. The final anime likeness/material pass is unfinished. Do not discard this work or rebuild a 2D avatar merely because new transparent art is supplied.

The `.blend` and its actual UV coordinates are delivered through the builder's browser checkpoint rather than as binary files in this Git tree. This corrective art pass has not inspected those actual UV layouts. The repository notes also state that UV islands are fragmented and need refinement. Therefore none of the newly generated artwork is certified to fit those islands without mapping.

## Apply the images deliberately

- Use the canonical face and body guides to compare likeness, eye silhouette, hairstyle, costume and proportions at matched views.
- Treat transparent iris, lash, brow and mouth artwork as texture-source or image-plane elements. Map them to the corresponding facial surfaces with appropriate UVs, alpha blending/clipping and depth ordering. Do not assume existing procedural face inserts have usable UVs.
- Keep sclera, iris/pupil, lashes, eyebrows, lips and mouth interior distinct. Do not bake a complete illustrated eye or mouth onto unrelated clothing or the entire head UV atlas.
- Use outfit/hair artwork as source material for the actual modular surfaces. Do not paste a posed full-body illustration directly into a fragmented UV atlas. Preserve the approved sleeve/cuff/hand boundaries.
- Keep blush, tears, sweat and anger marks separate and disabled in neutral. Define attachment, visibility and blend rules rather than permanently painting them into skin.
- Gold sticks, hair danglers, earrings and pendant are separate accessory sources. Preserve the approved geometry and attachment locations; do not create duplicates merely because an image is supplied.
- Retain originals and generate fitted textures as new derivatives. Record source image, image hash, object/material, UV layer, transform and output path. Pack or correctly link final texture files in the Blender project.

## Required visual tests

Render neutral front, three-quarter and side views against the canonical master. Check that eyes/lashes/brows stay aligned through independent blink and gaze; mouth art does not cross lips, teeth or tongue during jaw/smile/funnel/wide; hair and suit seams remain coherent; optional effects are absent in neutral. Test alpha edges against both light and dark backgrounds. Test full-body framing with hands and heels visible.

The new PNGs alone do not certify any of these tests. Record actual render results before proceeding to bulk expressions. No new user approval of the builder's Phase 04 candidate or next modeling phase is implied by this asset-repair request.

## Optional cutout use

Separated images may additionally be arranged on Blender planes or used in a layered 2D system. That requires explicit pivots, parent anchors, z order, clipping masks, swap exclusivity and assembly verification. It is an optional consumption route, not a replacement for the user's established full-character 3D project. Any assembly evidence included with the artwork must state what was actually tested.

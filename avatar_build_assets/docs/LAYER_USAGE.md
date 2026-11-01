# Component assembly and material usage

## Primary route: existing 3D avatar

Retain the latest editable Blender checkpoint. Assign the new artwork to that model; do not start a replacement mesh. Exact named Phase 03 targets are in `metadata/existing_3d_material_targets.json`.

1. **Head and skin.** Use `head/layers/RYO_HEAD_face_base_v001.png` as the painted face source for `RYOKO_Skin_HeadAndNeck`, excluding the unpainted background. Fit/project against front landmarks, then reconcile side views. This artwork ends at the chin; keep the existing neck material. Ear L/R artwork maps to the corresponding ears, behind hair and earring attachment points.
2. **Eyes.** On each side, use sclera behind iris/pupil, followed by the upper lash/lid edge. Place the iris inside the eyelid aperture, not directly on the face skin. Retain the existing eye geometry and gaze/blink controls. Clamp or mask the iris to the visible eye surface. Brows sit on the forehead above the eye and below any covering fringe.
3. **Blink alternatives.** Closed-lid PNGs are visual/material alternatives. If using them as overlays, hide the corresponding open sclera/iris/lash artwork. For the existing 3D blink rig, preferentially use them as shape/surface references and maintain actual geometry closure. Do not leave a visible open eye under a closed-lid card.
4. **Mouth.** Depth order is cavity behind teeth and tongue, with the lip edge in front. Keep the cavity inside the mouth aperture. The five `RYO_HEAD_viseme_*.png` images are complete alternative mouth sprites, not five simultaneous layers. Either map/reference individual oral pieces for the existing deforming mouth, or deliberately use a single sprite alternative; do not overlay both implementations.
5. **Hair.** Apply `hair/rear_scalp_nape.png` to the rear-facing scalp/nape source region, never across the face. Bun and short tail attach at the gathered rear hair location. Place side locks at their anatomical temple sides. The front fringe overlaps the forehead; the longer character-right side lock provides the reference's asymmetric silhouette. Keep the existing hair volume and project/bake source images to appropriate surfaces or mapped cards.
6. **Clothing.** Blouse front/back map to the blouse regions. Rear blazer lies behind the torso; blazer front panels overlap blouse edges. Upper-sleeve and forearm components belong to the corresponding sleeve surfaces, meeting at the existing elbow without visible seams. Trouser front/back regions belong to the trousers. Do not apply both front and back artwork to the same visible surface. Preserve the existing charcoal-sleeve/ivory-cuff/skin-hand transitions.
7. **Hands and shoes.** Use each anatomical-side source on its matching part. Preserve actual finger/hand geometry and heel shape. Images of posed hands or footwear are source/reference surfaces, not flat replacements for the modeled extremities.
8. **Ornaments.** Hair sticks are rigid objects anchored in the updo. Hair danglers are child components anchored at their top attachment. Earrings attach to ear lobes. Necklace/pendant sits above the blouse/skin; belt/buckle sits at the trouser waist. Reuse the corresponding existing accessory geometry rather than duplicating it.
9. **Effects.** Blush, tears, sweat, anger and other optional overlays are disabled in neutral. Attach face effects to stable head/face coordinates and scale them to the final model. Use separate visibility/material parameters. Do not bake temporary effects into skin or make them part of every expression.

## If using image planes as a temporary assembly

Create separate named objects and preserve alpha. Work from the canonical neutral reference in front view. Fit the head pieces locally first, then place the head group on the full body; independently generated sources do not share one pixel scale. Use the layer order above, and put far-side body parts behind near-side parts according to the pose. Define pivots at the actual shoulder, elbow, wrist, hip, knee, ankle and accessory attachment points. Keep overlap beneath adjacent parts to avoid gaps.

These instructions establish intended hierarchy, not measured registration coordinates. A usable plane assembly must save its actual transforms and show a neutral reconstruction, independent blink states, mouth swaps and modest joint movement tests. A separately generated picture is not proof of layer alignment. Do not call a collection of these PNGs a finished assembled puppet until that test exists.

## First proof before bulk production

Render the actual textured existing model front, three-quarter and side, with neutral, left blink, right blink, gaze and open/smiling mouth. Compare against `references/`. Check white and dark backgrounds for alpha edges, double lighting, seams, clipping, misplaced ornaments and mismatched skin. Present that material/likeness checkpoint before authoring the 200 presets. Retain old textures until the replacement is verified.

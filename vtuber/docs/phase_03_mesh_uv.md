# Phase 03 — modular surface, UV, texture, and material foundation

**Checkpoint date:** 2026-11-02  
**Status:** candidate for manual visual/UV approval; not deformation-certified  
**Source authority:** user-approved Phase 02 v002 blockout

## Scope and approval boundary

This checkpoint preserves the approved full-character surface while separating it into modular parts, increasing density in the head and hands, creating UVs, fitting textures, and correcting outfit material regions. It is a visual and UV foundation for subsequent reconstruction and feasibility testing.

Approval of this checkpoint does **not** certify clean animation topology, facial identity, expressions, a body skeleton, skin weights, ARKit clips, VRM export, tracking, AI control, runtime performance, or wall projection. Phase 04 facial feasibility remains gated until the user explicitly approves this checkpoint.

## Evaluated and rejected topology routes

Whole-character automatic replacement was not accepted:

- QuadriFlow testing produced scattered surface fragments despite apparently useful mesh metrics. It was rejected after visual inspection.
- Voxel replacement tests either changed the approved surface, produced severe holes, or exceeded a useful density range. A later 202,556-main-part-triangle test still had severe holes and was rejected.
- Selective skin voxel union improved some hand regions but introduced severe head/right-arm holes and increased the main-part total to 346,603 triangles. It was reverted.
- **Tripo API** smart retopology used `decimate --model v2.0 --face-limit 20000` on source task `d8fd4168-12f1-4175-810d-02e05ceace79`. Returned task: `ae55137b-d423-4c9a-87ab-cb729cf33c2c`. Read-back found 28,090 vertices, 25,627 triangles, zero quad faces, and 24,753 boundary/non-manifold edges. It was not accepted as production-ready deformation topology.

These routes are not hidden behind the final renders and are not represented as successful production retopology.

## Retained construction

The final candidate retains the user-approved v002 surface instead of replacing it:

1. The approved body faces and the thirteen approved accessory/core objects are captured in world space.
2. **Tripo API** semantic segmentation used `segment --model v2.0 --granularity balanced`. Returned task: `370e5e56-a084-4f07-a529-acae63195812`.
3. The ten semantic GLB parts are used only as nearest-surface labels. They do not replace the approved body geometry.
4. The approved surface is split into ten modular objects: hair/scalp/bun, head/neck, blazer/blouse, two sleeves, two arm/hand regions, trousers, and two footwear objects.
5. Only narrow boundary loops below 0.055 m perimeter are filled. Large garment and hair boundaries remain open for later reconstruction.
6. One subdivision pass adds density to the head/neck and both arm/hand objects without changing the overall construction route.
7. Smart-projected UVs and model-fitted base-color/roughness textures are created per major part. Gold accessories remain rigid uniform materials.

## Reference-comparison correction

The first comparison board exposed bare upper arms even though the approved outfit has full blazer sleeves. The arm/hand material regions were corrected before this checkpoint was offered for approval:

- `Z >= 1.03`: charcoal blazer sleeve
- `0.95 <= Z < 1.03`: ivory wrist-cuff region
- `Z < 0.95`: skin hand

All textures were then baked again, all comparison views were rendered again, and both cuff/hand transitions were inspected. The current boards show full sleeves on both arms. The correction is a material-region repair, not a claim that the sleeve or wrist deformation topology is finished.

## Read-back inventory and budget

The saved textured `.blend` was reopened in a separate Blender process and measured:

- 10 major modular parts
- 78,095 main-part vertices
- 140,767 main-part triangles
- 39,217 main-part quad faces
- 13 accessory/core objects and 4,080 accessory/core triangles
- 144,847 total character triangles, before any later facial/hidden-geometry additions
- 14,865 boundary edges and 14,865 non-manifold edges on the major parts
- one UV layer on every major part
- two fitted textures on every major part: base color and roughness
- 20 packed texture images total
- three 2048×2048 material sets for blazer/blouse, head/neck, and hair; seven 1024×1024 sets for the other major parts
- exactly two chopstick shafts and three chain links
- zero armatures and zero shape-key blocks

The current total is below the initial approximate 150k–220k evaluated-triangle working range, leaving limited room for later facial and hidden geometry. This is an authoring inventory, not a measured 1440p60 runtime result. Hardware and VSeeFace/VRM validation remain outstanding.

## UV and material inspection

The evidence set includes matched front/left-side/back reference comparisons, a face/hair board, both hands and cuffs, an eight-angle orbit, UV checker views, and a ten-part UV-layout contact sheet.

Observed result:

- Fitted textures cover the actual modular surfaces and no external texture is missing from the saved source.
- The checker confirms coverage but also shows heavily fragmented islands and inconsistent checker scale/texel density.
- Manual UV consolidation and final facial UV refinement remain necessary.
- No eye, mouth, source-sheet border, caption, or comic-panel pixels are baked into the outfit textures.
- The ivory blouse transition is baked from a smooth world-space mask rather than the earlier jagged per-face assignment.

## Known limitations

- Open clothing/hair boundaries and generated internal skin shells are not deformation-certified.
- Essential eyelid, lip, jaw, shoulder, elbow, wrist, finger, hip, and knee animation loops are not all authored or approved.
- Hands remain anatomically simplified; nails, knuckle loops, finger weights, and gesture deformation tests are pending.
- The face remains a soft placeholder without separate eyeballs, an eyelid rig, mouth cavity, teeth, tongue, or ARKit shapes. Hidden mouth work is deferred to facial feasibility rather than falsely marked complete here.
- Temporary bun-core patches remain construction geometry.
- `visible_shadow=False` on the skin objects suppresses generated internal-shell self-shadow artifacts in checkpoint renders. This is a presentation workaround, not a topology repair.
- No major body-proportion correction, facial identity resculpt, animation, or runtime optimization is claimed by this phase candidate.

## Reproducible files

- `vtuber/scripts/build_mesh_uv_v001.py` — retained-surface modular construction
- `vtuber/scripts/fit_mesh_textures.py` — fitted base-color/roughness baking and UV-layout sheet
- `vtuber/scripts/render_mesh_uv_v001.py` — matched, orbit, head, hair, and hand views
- `vtuber/scripts/render_uv_checker.py` — temporary checker-map inspection without overwriting the source
- `vtuber/scripts/validate_mesh_uv.py` — saved-source reopen and structural/texture read-back
- `vtuber/scripts/package_phase3_boards.py` — unchanged-reference comparison packaging
- `vtuber/data/mesh_uv_build_v003.json`
- `vtuber/data/texture_build_v001.json`
- `vtuber/data/mesh_uv_validation_v001.json`

The downloadable Phase 03 browser checkpoint contains the packed textured Blender foundation and the final evidence boards. Rejected meshes, broken diagnostic renders, redundant `.blend1` saves, and browser-verification captures are not part of the checkpoint delivery.

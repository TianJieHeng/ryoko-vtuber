# Phase 03 comparison and evidence index

**Browser review version:** `650df90`  
**Review state:** ready for manual Phase 03 visual/UV approval

The saved browser checkpoint contains the packed textured Blender source and six final evidence boards. All reference pixels used in the comparisons are unchanged source-pack images.

## Boards inspected

1. **Reference vs Blender Full Body** — front, left-side, and back comparisons. Confirms the retained silhouette, full charcoal sleeves, ivory blouse/cuffs, trousers, pumps, hair, and two-chopstick accessory.
2. **Reference vs Blender Face and Hair** — neutral bust and hair-construction comparisons. Confirms that facial identity and expression work remain outstanding and that temporary bun-core geometry is still identified.
3. **Reference vs Blender Hands** — character-left and character-right hand/cuff close-ups. Confirms that the bare-upper-arm material error is corrected and that both ivory cuff regions sit above skin hands.
4. **UV Checker** — full-body and head/hair checker renders. Confirms coverage while exposing fragmented islands and uneven texel density.
5. **UV Layouts — Modular Texture Sets** — ten independent 0–1 UV spaces, one for each major modular part.
6. **Blender Orbit** — eight fitted-material angles inspected for silhouette, material, accessory, and placement regressions.

## Verification record

- Complete matched, orbit, head/hair, and hand shot set rendered after the sleeve/cuff correction.
- UV checker rendered without saving over the textured source.
- Textured `.blend` reopened in a separate Blender process and validated.
- Read-back: 10 major parts, 140,767 main-part triangles, 13 accessory/core objects, 4,080 accessory/core triangles, 144,847 total character triangles, 20 packed textures, two chopstick shafts, three chain links, zero armatures, and zero shape-key blocks.
- Static browser verification passed with zero failures and no missing assets. The loop test was intentionally skipped because the page is static.
- Desktop and 375 px mobile review captures were inspected. No horizontal overflow was present at 375 px.
- Every navigation link was clicked in a real browser and reached its intended section. Final browser console: zero errors and zero warnings.
- Process captures, rejected diagnostic renders, redundant backup saves, and rejected Phase 03 mesh variants were removed from the browser checkpoint.

## Approval limit

This evidence supports a modular visual/UV foundation only. It does not establish deformation-certified topology, expression correctness, a body or facial rig, ARKit coverage, animation playback, VRM/VSeeFace compatibility, tracking, AI control, runtime frame rate, or projection validation. Phase 04 remains gated on explicit user approval.

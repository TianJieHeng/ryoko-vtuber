# Phase 02 — full-character blockout checkpoint

**Status:** implementation and internal visual review complete; awaiting user approval before Phase 03 production topology, UVs, and material separation.

## Source and generation

The approved front, left-side, and back full-body reference sheets were used as multiview inputs to **Tripo API**, generation model `v3.1`, with an 80,000-face target and textures disabled. The successful upstream task ID is `d8fd4168-12f1-4175-810d-02e05ceace79`. The resulting GLB was imported into Blender 5.2.1 LTS and normalized as a provisional 1.83 m total-height blockout.

Tripo API generated the full-body blockout only. It did not generate a rig, expressions, animation, UV production layout, mouth interior, or runtime-ready VRM.

## Measured Blender result

- Character mesh objects: 1
- Vertices: 43,766
- Triangles: 76,402
- Armatures: 0
- Shape-key blocks: 0
- Boundary edges: 10,724
- Non-manifold edges: 10,724
- Loose vertices: 0
- Authoring root rotation: -90 degrees about Z
- Render engine: Cycles CPU

The saved `.blend` was reopened in a separate Blender process and these values were read back successfully. The topology counts make the mesh unsuitable for direct production rigging; Phase 03 must rebuild or retopologize it rather than hiding the defect.

## Visual review and correction rounds

1. Eight orbit views and a top view were rendered and inspected.
2. The generated forward axis was +X, conflicting with the locked authoring forward -Y. `RYOKO_BLOCKOUT_ROOT` was rotated -90 degrees about Z and the matched views were rendered again.
3. Head close-ups showed that the single directional key left the face too dark to inspect. A broad frontal area fill was added. Its initial 650 W setting clipped the clay face, so only that light's energy was reduced to 180 W and the test was repeated. Geometry and clay material were not changed by the lighting correction.
4. Five head angles, a rear-hair view, both hands, matched front/left-side/back/three-quarter views, and the full orbit were inspected.
5. The initial top camera used a 2.6 m orthographic scale and made the character footprint too small. The top view alone was reframed to 0.75 m and inspected again.

## Observed reference mismatches

- The generated pose is arms-down neutral, not the separate A-pose construction sheet.
- The overall suit, trousers, heels, asymmetric fringe, rear hair, and hair sticks are present.
- Body volumes read fuller through bust, hips, and thighs than the approved references; knees and jacket hem are less sharp.
- The jaw and cheeks are softer and younger-looking than the approved neutral bust. Eye/eyelid definition, nose, and lips are shallow placeholders.
- There are no separate eyeballs, eyelids, mouth cavity, teeth, or tongue.
- Rear bun/ponytail masses exist, but hair sticks and ornaments are coarse angular forms.
- Hands have coarse finger volumes and incomplete clean separations; they are not ready for a finger rig.
- The 1.83 m normalization currently includes hair and ornaments. The final natural-skull height convention still needs to be restored during production modeling.

## Approval boundary

Approval of this checkpoint means only that the full-character blockout is an acceptable basis for production reconstruction. It does **not** approve facial identity, expressions, topology, hand deformation, materials, rigging, or runtime behavior.

The next manual comparison must occur before dependent expression work. Phase 04 remains the early facial feasibility gate; Phase 02 does not substitute for it.

## Evidence

The browser phase preview contains the final reference-versus-Blender full-body board, face/hair board, hand close-ups, and eight-angle-plus-top orbit sheet. The editable Blender source is available from that preview. Repository text evidence includes the generation/correction scripts and JSON read-back reports under `vtuber/scripts/` and `vtuber/data/`.

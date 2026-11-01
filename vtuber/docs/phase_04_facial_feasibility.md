# Phase 04 — early facial feasibility prototype

**Checkpoint date:** 2026-11-02  
**Status:** candidate complete; awaiting explicit user expression approval  
**Source authority:** user-approved Phase 03 modular visual/UV foundation  
**Browser review:** version `997bb29`

## Scope and approval boundary

Phase 04 tests whether the retained character source can support editable, combinable basic facial controls before body rigging or bulk facial production. The candidate includes neutral, independent full blinks, four-way gaze, jaw opening, smile, smile plus jaw, funnel, wide mouth, and a short authored action. Direct unchanged-reference comparison boards and a rendered motion preview accompany the editable Blender source.

Approval of this checkpoint is limited to early expression-control feasibility. It does not approve final anime facial likeness, final joined facial/oral topology, production textures, the complete ARKit set, a body rig, a production animation library, VRM export, tracking, AI runtime integration, hardware performance, or wall projection.

## Construction

The approved textured source is retained. New geometry is organized under `RYOKO_FACE_PROTOTYPE` and driven by `RYOKO_FACE_CONTROLS`.

- Separate warm-white eye surfaces, amber iris/pupil/catchlight assemblies, continuous upper lashes, mint brows, and fitted-skin eyelids.
- Separate deforming lips, dark mouth cavity, upper/lower teeth, and tongue.
- Real `RYOKO_Skin_HeadAndNeck` shape keys: `Basis`, `JawOpen`, and `MouthSmile`.
- Blink shape keys on both eye whites, eyelid meshes, lashes, and iris assemblies. Whites and irises compress with the closing lids so the open eye does not remain behind a folded membrane.
- Four directional gaze keys on each iris assembly.
- `JawOpen`, `MouthSmile`, `MouthFunnel`, and `MouthWide` keys on the five oral objects.

The eye and mouth assemblies are surface-fitted feasibility inserts, not a claim of final joined facial or oral topology. No source reference image was modified and no new Tripo operation was used in Phase 04.

## Controller contract

| Property | Range | Feasibility purpose |
|---|---:|---|
| `blink_left` | 0–1 | Character-left eyelid, lash, white, and iris closure |
| `blink_right` | 0–1 | Character-right eyelid, lash, white, and iris closure |
| `gaze_x` | −1–1 | Left/right iris displacement |
| `gaze_y` | −1–1 | Down/up iris displacement |
| `jaw_open` | 0–1 | Oral opening plus restricted chin drop |
| `smile` | 0–1 | Mouth-corner/oral smile plus real head cheek-region deformation |
| `funnel` | 0–1 | Initial narrow rounded lip-sync form |
| `wide` | 0–1 | Initial wide lip-sync form |

These properties are an authoring contract for the feasibility prototype. They are not VRM or ARKit mappings yet.

## Authored motion

`RYOKO_FACE_FEASIBILITY_PREVIEW` contains keyframes at frames 1, 13, 25, 37, 49, 61, 73, 85, and 97. At 24 fps, the rendered 97-frame MP4 lasts 4.041667 seconds.

Sequence: neutral → gaze left → bilateral blink → gaze right/up → jaw open → smile plus jaw → funnel → wide/gaze/partial blink → neutral.

The action is Blender source material for inspection. It is not itself an AI runtime controller; later baking/export or translation into runtime control data remains necessary.

## Render-driven correction record

- Detached the action for static inspections after action evaluation reset manually assigned controls.
- Corrected eye/lid depth ordering and increased blink clearance.
- Reused the fitted head skin and nearest-source UVs on the lids, with a soft outer fade, instead of a visibly mismatched skin patch.
- Increased oral radial density and restricted head jaw deformation below the aperture after front/depth inspection found lower-face skin crossing the mouth.
- Increased teeth and tongue tessellation and corrected their depth ordering.
- Simplified the feasibility lash to one continuous upper ribbon to avoid lower-lid/corner overlap.
- Isolated the remaining oblique blink defect to the eyelid rings. The final construction deforms whites and irises with blink and forms a shallow closed-lid band. Bilateral, independent, mid-blink, front, and side evidence was regenerated.

## Validation and budget

Fresh-process Blender read-back passed:

- 40 valid evaluated drivers; no invalid shape-key or material drivers.
- Expected shape keys and controller ranges present.
- All Phase 03 source objects preserved.
- All 20 source file textures packed or available.
- No non-finite evaluated coordinates in the tested static states.
- Action values verified at all nine authored keyframes; all controls return to zero at frame 97.
- 149,599 evaluated character triangles, near the lower end of the provisional 150k–220k authoring budget.

The triangle count is an authoring inventory only. No 1440p60, VSeeFace, VRM, iPhone, webcam-body, AI-runtime, or projection performance test has occurred.

Detailed results: `vtuber/tests/facial_feasibility.md` and `vtuber/data/face_prototype_validation_v001.json`.

## Evidence and browser verification

The browser checkpoint contains:

1. Neutral identity-boundary comparison.
2. Eye/blink front, three-quarter, and side comparison.
3. Mouth/jaw/smile/funnel comparison.
4. Eight-state facial control contact sheet.
5. Independent left/right blink and directional-gaze contact sheet.
6. Rendered 720×720, 24 fps motion preview.
7. Validation summary and downloadable report.
8. Downloadable editable facial prototype.

Desktop and 375 px mobile layouts were opened and inspected. All seven navigation links reached their sections; the MP4 loaded and played; local assets and downloads resolved; touch targets met the 44 px check; mobile scroll width equaled viewport width; console errors and warnings were zero.

## Known limitations and next gate

- Final eye silhouette, lash wing, iris shading, facial likeness, and production anime materials remain unfinished.
- Oral contours, tooth/tongue surfaces, mouth corners, and exact reference forms need production refinement.
- Separate inserts, lid fading, and presentation shadow settings are not final joined deformation topology.
- Fragmented UVs and the Phase 03 open/internal-shell topology limitations remain carried forward.
- The full 52-clip ARKit set is absent; `jawLeft` and `lowerLipDepress` still require real-mesh design and validation.
- No body skeleton, skin weights, production performance library, secondary motion, VRM0X export, tracking, AI runtime, or hardware/projection validation is claimed.

Explicit Phase 04 approval is required before Phase 05 body rigging or Phase 06 bulk facial production begins.

## Reproducible files

Run in this order after setting the project paths in the scripts:

1. `vtuber/scripts/build_face_prototype.py` — build source and base expression renders.
2. `vtuber/scripts/render_face_additional_tests.py` — independent blink/gaze evidence.
3. `vtuber/scripts/validate_face_prototype.py` — fresh-process structural and action validation.
4. `vtuber/scripts/render_face_motion.py` — render the authored 97-frame action; encode the resulting PNG sequence at 24 fps.
5. `vtuber/scripts/package_phase4_boards.py` — assemble unchanged-reference comparison and control boards.

Data:

- `vtuber/data/face_prototype_build_v001.json`
- `vtuber/data/face_prototype_validation_v001.json`

The editable `.blend`, final boards, MP4, and validation-report download are delivered through browser review version `997bb29`; binary source files are not misrepresented as text-published repository artifacts.

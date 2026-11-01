# Phase 04 — facial feasibility test report

**Checkpoint date:** 2026-11-02  
**Candidate:** `ryoko_face_prototype_v001.blend`  
**Source authority:** user-approved Phase 03 textured modular foundation  
**Blender:** 5.2.1 LTS, fresh-process reopen validation  
**Status:** internal technical and visual checks complete; explicit user expression approval pending

## Test boundary

This is an early feasibility prototype made from separate surface-fitted anime eye and mouth assemblies plus real head `JawOpen` and `MouthSmile` shape keys. It is not final joined facial/oral topology, the complete ARKit rig, a body rig, a production action library, a VRM export, or a runtime compatibility result.

## Controls inspected

- `blink_left`, `blink_right`: independent 0–1 controls.
- `gaze_x`, `gaze_y`: independent −1–1 controls driving left/right and up/down shape keys.
- `jaw_open`, `smile`, `funnel`, `wide`: independent 0–1 controls.
- All eight properties remain separate on `RYOKO_FACE_CONTROLS` for later authored-state blending and AI selection.

## Visual test matrix

| Test | Evidence inspected | Result and remaining boundary |
|---|---|---|
| Neutral | Front and three-quarter renders; neutral reference board | Separate eyes, lashes, brows, lips, and oral insert are readable. Final almond-eye likeness, lash design, iris shading, and production textures remain unfinished. |
| Full bilateral blink | Front and side renders; eye comparison board | Eyes close to a clean skin-and-lash line. The earlier folded-lid corner artifact is corrected. |
| Character-left blink only | Independent front render | Character-left closes while character-right remains open. |
| Character-right blink only | Independent front render | Character-right closes while character-left remains open. |
| Mid-blink | Frames 17 and 21 of the rendered action | Deformation progresses without the former eye-corner crumpling. |
| Gaze left/right | Independent front renders; action frames 13 and 37 | Horizontal iris movement is visible and remains separable. |
| Gaze up/down | Independent front renders | Vertical iris movement is visible and remains separable. |
| Jaw open | Front and side renders; mouth comparison board | Oral aperture stays open; teeth and tongue remain visible. Chin deformation is restricted below the aperture. |
| Smile | Front render; mouth comparison board | Teeth-visible smile control works. Exact smile contour and tooth surfaces remain provisional. |
| Smile plus jaw | Front and three-quarter renders; action frame 61 | Combined controls remain readable without the former lower-face skin crossing. |
| Funnel | Front render; action frame 73 | Narrow rounded mouth form is produced; final artwork-matched contour remains open. |
| Wide plus gaze | Front render; action frame 85 | Wide mouth and vertical gaze combine; oral surface refinement remains necessary. |
| Authored action | 97-frame MP4 and sampled transition contact sheet | Gaze, blink, jaw, smile, funnel, wide, and recovery play in sequence. This is not a runtime controller. |
| Neutral recovery | Frame 97 control read-back and final rendered frame | All eight properties return to zero. |

## Saved-source technical checks

The final `.blend` was reopened in a separate Blender process. The validation script evaluated every static state and all authored key frames.

- **Passed:** all Phase 03 source objects are preserved with their original object types.
- **Passed:** all expected shape-key inventories are present on the head, eye whites, eyelids, lashes, iris assemblies, lips, mouth cavity, teeth, and tongue.
- **Passed:** 40 evaluated drivers are valid in both static and action checks.
- **Passed:** controller ranges match the specified 0–1 and −1–1 limits.
- **Passed:** no non-finite evaluated mesh coordinates were found in the tested states.
- **Passed:** all 20 source file textures are packed or have an existing path.
- **Passed:** the action is named `RYOKO_FACE_FEASIBILITY_PREVIEW`, runs from frame 1–97 at 24 fps, and returns to neutral.
- **Measured:** 149,599 evaluated character triangles, including the facial additions. This is near the lower end of the provisional 150k–220k authoring range, not a measured 1440p60 runtime result.

Machine-readable results: `vtuber/data/face_prototype_validation_v001.json`.

## Corrections caught by render inspection

1. Static poses initially remained neutral because the saved action reapplied its frame values. Static inspection now detaches the action and explicitly updates the control object and dependency graph.
2. Eye inserts remained visible through closure because of depth intersections. Lid/eye depth ordering was corrected.
3. The first substitute eyelid skin produced a visible patch. The lid now reuses fitted head material and UVs with an outer fade.
4. Coarse mouth-fan triangles and broad chin deformation allowed skin to cross the oral aperture. The cavity received more radial rings and the head jaw weight was restricted below the mouth.
5. Teeth/tongue and lash depth/segment counts were adjusted after close-up inspection.
6. The remaining blink artifact was isolated to the eyelid membrane. The final candidate deforms whites and irises with the blink and closes the lid into a shallow band; front, side, independent, and mid-blink tests were rendered again.

## Remaining visual limitations

- The neutral eye opening, lash wing, iris detail, and skin shading do not yet match the final anime artwork closely enough to be called final likeness.
- Mouth forms establish control feasibility only. Tooth/tongue contours, small oral-surface irregularities, mouth corners, and exact reference proportions still require production refinement.
- Eye and mouth assemblies are separate surface-fitted inserts. Final joined facial/oral topology and consolidated facial UVs are not complete.
- Lid material fading and disabled shadow casting are feasibility/presentation techniques, not substitutes for final deformation topology.
- `jawLeft`, `lowerLipDepress`, the other required ARKit clips, procedural conflict rules, VRM mapping, tracking, and runtime tests are not implemented.

## Checkpoint verdict

The candidate is ready for the user’s manual expression-comparison checkpoint. Approval is requested only for the early control direction and observed deformation feasibility. Fundamental production likeness or oral-topology concerns remain valid reasons to reject or request another correction round. Phase 05 body rigging and Phase 06 bulk facial production remain gated until explicit approval.

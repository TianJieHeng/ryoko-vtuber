# Ryoko VTuber — Phased Build Plan

**Version:** 1.0  
**Prepared:** 2026-11-01  
**Working folder:** `vtuber/`  
**Status:** Planning complete; implementation not started

## 1. Project goal

Create a full-body, anime-style 3D Ryoko avatar in Blender for VTuber use and full-character wall projection. The finished avatar must preserve Ryoko's established identity and costume while supporting expressive facial acting, lip sync, head and body movement, readable hand gestures, and secondary hair/accessory motion.

The project must produce a real, editable 3D model and rig. Reference sheets and extracted panels are visual guidance only; they are not a model, animation curves, or proof of runtime compatibility.

## 2. Source material and current boundary

Primary guidance:

- `handoff/BUILDER_HANDOFF.md` — asset navigation and practical build requirements
- `handoff/NOT_INCLUDED.md` — explicit missing deliverables and validation limits
- `references/REFERENCE_REVIEW.md` — source-design observations and conflicts
- `assets/modeling/` — neutral, full-body, side, back, and A-pose modeling masters
- `assets/details/` — hair, accessories, outfit, hands, and footwear details
- `metadata/controls_inventory.json` — available facial-control references
- `metadata/expressions.json` — 200 authored expression performances
- `metadata/body_gestures.json` — 40 reusable body performances
- Supplied 21-page PDF, *3D VTuber Model Creation: Complete Blender Workflow Guide*

Current state:

- Source-art production and reference QA are complete.
- No production mesh, UV unwrap, fitted texture atlas, `.blend` project, skeleton, skin weights, facial shape keys, physics, animation clips, or tested runtime export exists.
- The 22 generic facial-control references are not a certified ARKit 52-shape set.
- `jawLeft` and `lowerLipDepress` references are unavailable and must be designed and validated on the actual mesh.
- The target application, tracking route, export version, and target hardware remain to be confirmed.

## 3. Working principles

1. Preserve all source references unchanged; keep implementation files inside `vtuber/`.
2. Follow the neutral facial master and front/back full-body masters when secondary references conflict.
3. Preserve mint/sage hair, amber eyes, dark trouser suit, white blouse, gold ornaments and jewelry, and black heels. Do not substitute an unrelated masked or black-haired Ryoko design.
4. Treat drawings as visual guides, not measured orthographic geometry. Resolve perspective, hidden surfaces, rear hair volume, mouth construction, and accessory attachments on the model.
5. Use character-left/character-right for all controls and documentation.
6. Work in meters, apply transforms at the required milestones, and use consistent mesh, material, bone, shape-key, and action names.
7. Save recoverable Blender milestones before destructive or large changes.
8. Prove the facial and skeletal foundations on the real mesh before mass-producing performances.
9. Do not claim export, tracking, lip-sync, playback, hardware, or projection compatibility until it has been tested.

## 4. Proposed working structure

```text
vtuber/
  phasedbuildplan.md          This plan
  blender/                    Editable Blender projects and milestone saves
  textures/                   Model-fitted texture source and export maps
  scripts/                    Reproducible Blender helpers and validation scripts
  actions/                    Reusable facial/body performance source data
  exports/                    Tested runtime exports and accompanying files
  previews/                   Turntables, expression grids, and animation previews
  tests/                      Validation reports, test scenes, and recorded evidence
  docs/                       Design lock, control mapping, dependencies, and release notes
```

## 5. Phase plan

### Phase 0 — Target and environment specification

**Purpose:** Establish the technical destination before making runtime-dependent choices.

**Tasks**

- Confirm the target VTuber/runtime application and version.
- Confirm webcam tracking, iPhone/ARKit capture, scripted playback, or a combination.
- Confirm lip-sync method and whether full-body tracking is required; the model remains full-body regardless.
- Confirm target hardware, expected rendering resolution, frame-rate goal, and wall-projection setup.
- Select the Blender version and required add-ons.
- Select the intended export route, such as VRM or FBX, without assuming different applications accept identical mappings.
- Record which illustrated effects are wanted: tears, blush, sweat, sparkle eyes, graphic marks, or chibi cutaways.

**Deliverables**

- `docs/target_specification.md`
- `docs/dependencies.md`
- Initial export and tracking decision record

**Exit gate**

The target route is explicit enough to choose facial-control naming, export format, and validation procedures. If a decision remains open, subsequent work must stay runtime-neutral and the limitation must be recorded.

### Phase 1 — Design lock and reference preparation

**Purpose:** Convert the reference pack into an actionable modeling specification.

**Tasks**

- Inspect the neutral bust, full-body front/side/back, and A-pose masters together.
- Review hair, eye, mouth, accessory, outfit, hand, and pump detail sheets.
- Lock proportions, palette, costume construction, accessory placement, and character-left/right.
- Document contradictions and propose geometry for unseen or ambiguous surfaces.
- Separate rigid components from deformable hair, cloth, and accessories.
- Define the initial polygon, texture, and material budgets appropriate to the target hardware.

**Deliverables**

- `docs/design_lock.md`
- `docs/open_design_decisions.md`
- Reference comparison board in `previews/`

**Exit gate**

One coherent production design is documented, with unresolved hidden-surface choices explicitly identified rather than silently invented.

### Phase 2 — Full-character blockout

**Purpose:** Establish the whole figure and silhouette before detailed topology or rigging.

**Tasks**

- Block the head, torso, hips, limbs, hands, feet, hair masses, clothing, and accessories.
- Check front, side, back, three-quarter, and A-pose proportions against the masters.
- Keep major components separate and clearly named.
- Establish the mouth cavity and eye placement early enough to test facial construction.
- Render neutral-light comparison views at streaming-relevant framing.

**Deliverables**

- `blender/ryoko_blockout_v001.blend`
- Blockout turntable and matched reference comparisons

**Exit gate**

The full head-to-heels silhouette, proportions, identity, costume, and major attachment points are coherent from all required views.

### Phase 3 — Production topology, UVs, textures, and materials

**Purpose:** Build an efficient mesh that can deform predictably in real time.

**Tasks**

- Retopologize eyelids, lips, jaw, shoulders, elbows, wrists, fingers, hips, knees, and other deformation areas.
- Build the mouth interior, teeth, tongue, and other necessary hidden geometry.
- Keep hair, clothing, jewelry, and accessories modular where practical.
- Create and inspect the UV unwrap before authoring fitted atlases.
- Produce model-fitted color and required utility textures without baking in panel borders, captions, illustrative lighting, or comic effects.
- Create efficient anime-appropriate materials and test their appearance under neutral lighting.
- Check topology and material budgets against the selected runtime.

**Deliverables**

- `blender/ryoko_mesh_uv_v001.blend`
- Fitted textures in `textures/`
- Mesh/UV/material review renders

**Exit gate**

UVs and textures fit the actual mesh, essential facial and joint loops are present, and no major modeling issue prevents deformation testing.

### Phase 4 — Early facial feasibility prototype

**Purpose:** Prove the facial foundation before building the complete control library.

**Tasks**

- Prototype neutral, full blink, gaze, jaw opening, smile, and initial lip-sync shapes.
- Check eyelid closure over the eye, lip sealing, teeth/tongue intersections, and silhouette preservation.
- Test combined controls, including smile plus mouth opening and gaze plus blink.
- Resolve asymmetric controls using character-left/right.
- Render direct comparisons against the relevant reference images.

**Deliverables**

- `blender/ryoko_face_prototype_v001.blend`
- Facial prototype comparison sheet and short motion preview
- `tests/facial_feasibility.md`

**Exit gate**

The real mesh supports clean, combinable basic facial deformation. Do not proceed to bulk facial production while fundamental eyelid, mouth, or identity problems remain unresolved.

### Phase 5 — Body skeleton, skinning, and deformation

**Purpose:** Produce stable full-body and finger motion.

**Tasks**

- Build the spine, neck, head, shoulders, arms, hands/fingers, hips, legs, and feet hierarchy.
- Use consistent axes and symmetrical names suitable for retargeting.
- Add animator-friendly controls and any required FK/IK mechanisms.
- Skin the body, clothing, hands, and accessories; paint smooth joint-weight gradients.
- Add corrective shapes or drivers where extreme poses collapse volume.
- Test crossed arms, finger wag, stern stance, sitting/standing basics, head turns, and neutral recovery.
- Inspect hand contacts, jacket penetration, balance, and full-body silhouette.

**Deliverables**

- `blender/ryoko_body_rig_v001.blend`
- Body deformation test previews
- `tests/body_rig_validation.md`

**Exit gate**

Required poses and transitions are stable, fingers are usable, weights are clean, and the character returns reliably to neutral without major intersections or deformation artifacts.

### Phase 6 — Complete facial-control rig

**Purpose:** Build the production facial system required by the selected tracking and performance route.

**Tasks**

- Implement the required blink, gaze, brow, cheek, jaw, and mouth controls.
- If ARKit is selected, implement and verify the required approximately 52 standard shapes using exact target-compatible names.
- Design and test `jawLeft` and `lowerLipDepress` on the mesh; do not infer success from missing reference art.
- Add visemes/lip-sync controls required by the chosen application.
- Define conflict rules for procedural blink, gaze, and lip sync versus authored expressions.
- Add corrective shapes and calibrated control ranges where needed.
- Produce a contact sheet showing every control and representative combinations.

**Deliverables**

- `blender/ryoko_face_rig_v001.blend`
- `docs/facial_control_mapping.md`
- Facial-control contact sheet and combination tests

**Exit gate**

The complete required control set works individually and in common combinations, with unambiguous names, sides, ranges, and procedural override behavior.

### Phase 7 — Secondary motion and special effects

**Purpose:** Add controlled polish without excessive runtime cost.

**Tasks**

- Add spring bones or equivalent controls for hair and loose accessories.
- Tune stiffness, damping, limits, and collision behavior in the target environment.
- Implement approved blush, tears, sweat, sparkle, or graphic effects as appropriate materials, overlays, geometry, or scene effects.
- Keep chibi cutaways, captions, dividers, and source-sheet backgrounds out of avatar textures.
- Test secondary motion during idle, head turns, body actions, interruptions, and neutral recovery.

**Deliverables**

- Updated rig with secondary-motion controls
- Effect implementation notes and previews
- `tests/secondary_motion_validation.md`

**Exit gate**

Hair/accessory motion is stable and useful, effects are controllable, and no effect depends on unregistered source-sheet pixels.

### Phase 8 — Reusable expressions and body performances

**Purpose:** Convert the acting catalogue into reusable 3D controls and actions.

**Tasks**

- Build the 200 expression presets/performances from shared facial controls rather than 200 unrelated base meshes.
- Build the 40 body actions as separate reusable clips.
- Stage catalogue face/body pairings deliberately; do not treat them as pre-synchronized source animation.
- Author timing, easing, holds, interruption behavior, loop boundaries, and neutral returns on actual curves.
- Test each expression with live blink, gaze, and lip sync according to its blend/override policy.
- Prioritize wall-projection readability for crossed arms, finger-wag reprimands, stern stances, and scolding performances.
- Render expression and body-action review previews.

**Deliverables**

- Reusable expression and body-action library
- `docs/performance_mapping.md`
- Review previews and `tests/performance_validation.md`

**Exit gate**

Performances are distinct, readable, interruptible where required, and free of uncontrolled channel conflicts. Nine reference poses are not treated as proof of a seamless animation.

### Phase 9 — Export and runtime integration

**Purpose:** Produce and configure the avatar in its actual destination.

**Tasks**

- Run a final naming, transform, scale, topology, material, and control inventory check.
- Export the selected format and version with required textures and mapping data.
- Import into the target application and configure materials, bones, expressions, lip sync, blink, gaze, hotkeys, and profiles.
- Connect the chosen webcam/iPhone/other tracking input.
- Test orientation, mirrored bones, shape names, expression mappings, audio sync, and tracking stability.
- Measure runtime performance and adjust mesh, textures, shaders, or physics where necessary.

**Deliverables**

- Tested export in `exports/`
- Runtime configuration instructions
- `tests/runtime_validation.md`

**Exit gate**

The exported avatar works in the actual target application with the selected tracking route. A successful file export alone does not pass this gate.

### Phase 10 — Final validation and release

**Purpose:** Verify the complete experience and package a maintainable delivery.

**Tasks**

- Test idle, extremes, repeated actions, interrupted performances, loops, and return to neutral.
- Test facial capture, lip sync, body motion, effects, hotkeys, and audio under realistic streaming conditions.
- Inspect wall projection at the intended distance: full figure visible, hands readable, scolding pose legible, and face expressive.
- Record remaining limitations and untested configurations explicitly.
- Clean and organize the editable Blender project, textures, dependencies, exports, and test evidence.

**Deliverables**

- Final editable `.blend` project
- Tested runtime export and required textures
- Version, dependency, and export-setting notes
- Control and performance documentation
- Recorded validation evidence and known-issues list
- Release summary in `docs/release_notes.md`

**Exit gate**

All required release tests pass, or any exception is documented and accepted without claiming unsupported compatibility.

## 6. Required validation throughout

Maintain evidence for the following rather than relying on visual reference approval alone:

- Identity and silhouette comparisons from multiple views
- Eyelid closure, lip sealing, teeth/tongue clearance, and combined facial shapes
- Joint deformation, finger articulation, clothing intersections, contacts, and balance
- Control names, character-left/right, ranges, and procedural conflict behavior
- Animation timing, interruption, looping, and neutral recovery
- Export scale, orientation, materials, textures, and runtime mappings
- Tracking stability, lip sync, CPU/GPU load, and streaming frame rate
- Full-body wall-projection framing and gesture readability

## 7. Immediate next actions

1. Complete Phase 0 target and environment decisions.
2. Inspect the modeling masters and produce the Phase 1 design lock.
3. Begin the full-character blockout in Blender.
4. Prioritize the Phase 4 facial feasibility checkpoint before expanding the full expression library.
5. Update this plan with actual milestone paths, test evidence, and remaining issues as work proceeds.

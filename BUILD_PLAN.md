# Ryoko VTuber Phased Build Plan

**Version:** 1.0 draft for approval  
**Prepared:** 2026-11-01  
**Repository:** TianJieHeng/ryoko-vtuber  
**Current authorization:** review and preserve six supplied character sheets, create this plan, and publish those materials. Image generation and Blender production have not started.

## Goal and delivery boundary

Create a consistent visual production pack for the supplied human Ryoko character, then hand it to the user's Kimi workflow for construction and rigging in Blender. The target is 200 distinct expression performances, each with a nine-panel motion reference sheet, alongside modeling references and separate facial-control references.

This is a plan for both stages, not a claim that either is complete. Images communicate design intent. They do not contain mesh topology, UV coordinates, skin weights, shape keys, animation curves, or a working avatar. Those must be authored and tested on the actual model. The 200 performances can combine reusable controls; they do not require 200 independent morph targets.

The supplied references depict a green/mint-haired businesswoman with amber/gold eyes, a dark trouser suit, open white blouse, gold hair ornaments and jewelry, and black heels. Do not import the appearance of any earlier masked or black-haired Ryoko design. Preserve the six originals unchanged. Their visual differences must be resolved before declaring one production design canonical.

## Status and ownership

| Phase | Deliverable | Owner | Current status |
|---|---|---|---|
| 0 | Reference intake and design decisions | G and user | Six references reviewed and preserved; design decisions open |
| 1 | Modeling reference pack | G | Planned |
| 2 | Five expression pilots and control prototype references | G | Planned |
| 3 | Blender facial feasibility prototype | User's Kimi workflow | Planned |
| 4 | Complete facial-control reference pack | G | Planned |
| 5 | 200 expression performances and motion sheets | G | Planned |
| 6 | Visual pack QA and production handoff | G | Planned |
| 7 | Mesh, textures, rig and animation implementation | User's Kimi workflow | Planned |
| 8 | Target application testing and release | User and build workflow | Planned |

Owner labels describe the intended division of work, not an active connection to Kimi or authorization to send it files. Approve the production plan before starting image generation. Use phase-level approval and agreed checkpoints rather than requesting permission for every routine asset.

## Phase 0 Reference intake and design lock

**Inputs:** six supplied PNG sheets and the 21-page Blender workflow guide. Preserve original bytes, record original filename, repository path, pixel dimensions and SHA-256, and inspect the actual images. Record findings in `references/REFERENCE_REVIEW.md` and inventory in `references/manifest.json`.

The [visual review](references/REFERENCE_REVIEW.md) proposes REF-001 for silhouette, REF-006 for technical details, REF-005 for facial range, and REF-002–004 for acting intent. This hierarchy is unapproved. REF-005 has 16 portraits; the three special sheets add 18 numbered performances with overlaps, not 34 guaranteed unique production expressions. Resolve hair bun/ponytail construction, jewelry placement, collar/buttons and pocket details explicitly.

Resolve these choices before production:

- Which turnaround controls anatomy, hair silhouette, costume, footwear and accessories when sheets differ?
- Are all supplied costumes one outfit, or are any alternates? Do not average contradictory details.
- Is the delivered rig full-body, waist-up or bust-only? Full-body drawings do not settle the required rig coverage.
- What application, export format/version and tracking input will receive the avatar? Confirm webcam, iPhone facial capture, prerecorded animation, or a combination.
- Which exaggerated effects are desired: blush, tears, sweat marks, sparkle eyes, comic symbols, or chibi transformations?

Create a short design lock identifying approved references, proportions, palette, accessory placement and character left/right. Treat source captions as reference annotations, not permission to invent missing back/side details or change the design. New unseen details require an explicit design proposal.

**Exit gate:** originals verified; conflicts documented; neutral master and scope approved. Unresolved implementation choices may remain listed, but do not label dependent assets compatible or production-ready.

## Phase 1 Modeling reference pack

**Depends on:** Phase 0 design lock and approval to generate.

Prepare clean, consistently scaled front, side and back full-character views for the approved coverage, plus three-quarter checks. Use straight, orthographic-style presentation without dramatic camera distortion. Generated drawings are visual guides, not dimensionally certified CAD projections.

Add a neutral A-pose or T-pose as chosen for the build; head front/profile/three-quarter close-ups; hair silhouette and section breakdown; eye and mouth-interior details; hands; outfit construction; footwear; and accessories. Mark rigid pieces separately from hair, cloth and other intended moving parts. Show occluded structures separately where necessary rather than claiming that one silhouette defines their geometry.

Use neutral lighting, a fixed background and restrained shading so facial planes and color are readable. Keep character scale, eye line, crop and camera consistent across matched sets. Produce independent view images as well as assembled review sheets.

**Exit gate:** matching silhouette and landmarks across views, resolved costume and hair continuity, no missing required part, and user approval of the neutral master. Record any artistic interpretation remaining for the modeler.

## Phase 2 Small expression pilot

**Depends on:** approved master.

Produce five varied performances first: restrained confidence, affectionate warmth, embarrassment, controlled anger and broad surprise. Each receives an individual peak-expression image, a nine-panel key-pose sheet, separated panel files, and motion notes. Include neutral, blink and a few mouth-shape reference tests for the model prototype.

Review identity, hair and accessory stability, eyelid anatomy, mouth construction, expression clarity, and unwanted changes in head scale or pose. A face-only deformation sheet keeps the head still. Gestures and head turns belong in separately identified performance references, so Kimi can distinguish facial deformation from skeletal motion.

**Exit gate:** pilot demonstrates the intended style and enough consistency to scale. Revise the master if recurring errors appear; do not produce 195 more variations of a broken template.

## Phase 3 Blender feasibility checkpoint

**Depends on:** pilot references and a model built by the user's workflow.

Kimi blocks and tests the neutral head, eyelid closure, eye motion, jaw opening, a smile and initial lip-sync shapes. Check silhouette against the references and test how controls combine. Obtain rendered comparisons or the relevant model evidence before declaring this gate passed.

This is deliberately early. Image approval alone cannot prove that eyelids close correctly, teeth stay inside the mouth or facial shapes deform cleanly. While this gate is pending, organize the expression catalogue and prompts; do not report model validation or automatically proceed through the dependent production gate.

**Exit gate:** prototype judged feasible on the real mesh; observed issues returned to the visual pack or model implementation with clear ownership.

## Phase 4 Facial control reference pack

**Depends on:** chosen tracking route and prototype findings.

Build isolated references for brows, eyelids, gaze, cheeks, jaw and mouth, including asymmetric left/right movements. Neutral remains the common baseline. If the chosen route uses ARKit, cover its approximately 52 standard facial controls with exact names verified against the selected implementation. These controls are separate from the 200 performances and are not counted as emotions.

If VRM is selected, define the version-specific expression mapping, including supported emotion, lip-sync, blink and gaze behavior. Define whether each custom performance allows, blends or suppresses procedural lip sync, blinking and gaze. Do not assume all target applications expose every custom expression identically.

Add mouth-shape references suitable for the selected lip-sync system, with visible teeth/tongue guidance where needed. Do not treat a painted mouth or a flat facial grid as an implemented blendshape.

**Exit gate:** complete control inventory for the selected target, unambiguous left/right convention, and reference-to-control mapping reviewed by the builder.

## Phase 5 Expression and motion production

**Depends on:** approved pilot, prototype gate and stable control plan.

Allocate 200 distinct performances, provisionally 20 per family:

| IDs | Family |
|---|---|
| EXP-001 to EXP-020 | Joy and affection |
| EXP-021 to EXP-040 | Sadness and vulnerability |
| EXP-041 to EXP-060 | Anger and frustration |
| EXP-061 to EXP-080 | Surprise and fear |
| EXP-081 to EXP-100 | Disgust and discomfort |
| EXP-101 to EXP-120 | Confidence and smugness |
| EXP-121 to EXP-140 | Curiosity and concentration |
| EXP-141 to EXP-160 | Embarrassment and shyness |
| EXP-161 to EXP-180 | Tiredness and relaxation |
| EXP-181 to EXP-200 | Playfulness and exaggerated reactions |

The five pilots occupy appropriate IDs within these 200; they are not five extras. Before bulk generation, name and describe every performance so near-duplicates can be removed. Different labels alone do not establish different expressions. Define the recognizable combination of brows, eyes, cheeks and mouth, with any gesture or overlay separately specified.

Each performance has nine key poses: neutral, anticipation, onset, build, peak, follow-through or hold, release, settle and neutral. This creates **200 motion sheets and 1,800 reference panels**. The repeated neutral panels are intentional boundaries, not 1,800 distinct expressions. Laughing, crying and other cycles use an appropriate revised sequence and explicit loop boundaries rather than a forced one-shot arc.

Specify key-pose timestamps, hold duration, easing intent, total duration, loop behavior and return-to-neutral behavior. Nine images do not imply nine evenly spaced playback frames. Blender will create the interpolated motion and rendered animation later. Hand/body gestures use separate skeletal performance references; chibi panels in source sheets do not automatically authorize changing the avatar's proportions.

**Exit gate:** all 200 IDs have reviewed peak and motion references, complete metadata, distinct readable intent, and no unresolved identity drift.

## Phase 6 Quality control and handoff

Check every sheet for correct panel order/count, consistent face and eye line, stable costume/accessories, coherent anatomy, clear silhouettes and readable movement. Check facial controls independently and in combinations such as smile plus lip sync, gaze plus blink, or tears plus an expression. On images, this is a visual review; deformation and collision checks still belong to the actual rig.

Preserve generation originals and record their real dimensions. Never describe resized images as native higher-resolution output. Any cropping, panel extraction, scaling, alpha work or alignment must be documented; retain originals and obtain any necessary processing approval before those operations. A transparent-background requirement must produce genuine alpha, not a painted checkerboard.

Package a contact-sheet index, asset manifest, control mapping, expression catalogue, timing notes, design decisions, open issues and builder checklist. Distinguish facial deformation from texture/material effects, floating graphics and bone motion. Blush, sweat marks and sparkle overlays are not automatically facial topology.

**Exit gate:** local checks pass, manifest links resolve, all required IDs exist, limitations are explicit, and the uploaded commit is verified. No CI or GitHub Actions are used.

## Phase 7 Blender implementation

The user's build workflow creates the mesh, topology, UV unwrap, model-fitted textures, materials, skeleton, weights, corrective shapes, facial controls, expression combinations and animation curves. Hair and loose accessories receive appropriate secondary-motion controls. Texture atlases and placement masks may be authored only against the actual approved UV layout; do not guess them from a character sheet.

Kimi maps reference performances to reusable controls and authored actions, tests extremes and control conflicts, and renders animation previews for comparison. Record the Blender version, dependencies, export settings and actual test evidence. Keep implementation files distinct from source drawings.

**Exit gate:** real model and animation tests pass; known remaining issues are documented. Generated reference art alone cannot pass this gate.

## Phase 8 Application validation and release

Import the chosen export into the actual destination application. Test scale/orientation, expression names and hotkeys, facial capture or lip sync, blink/gaze combinations, hair motion, clipping, and performance on the user's target hardware. Test startup, neutral recovery, interrupted performances and loops as well as peak poses.

Deliver the editable Blender project, supported runtime export, required textures and dependency/version notes only when produced and verified. Mark untested compatibility explicitly. A successful export is not proof of successful tracking or animation playback.

## File and metadata conventions

Proposed future layout, beyond today's plan and references:

```text
references/originals/                 Unchanged supplied PNGs
references/manifest.json             Source inventory and hashes
references/REFERENCE_REVIEW.md        Observations and unresolved conflicts
assets/modeling/                     Approved visual modeling references
assets/controls/                     Isolated facial controls
assets/expressions/EXP-001_slug/      Peak, sheet and separate reference panels
metadata/expressions.json            Performance and timing records
previews/                            Contact sheets and review previews
handoff/                             Builder instructions and acceptance results
blender/                             Future actual model implementation
exports/                             Future tested runtime deliverables
```

Example filenames: `RYO_EXP-001_soft-smile_sheet_v001.png`, `RYO_EXP-001_soft-smile_kp01_v001.png` through `kp09`, and `RYO_CTL_eyeBlinkLeft_front_v001.png`. Use the approved tracking spelling for control identifiers and character-left/right, never viewer-left/right without labeling it.

Each expression record must include ID, slug, family, description, source master version, asset paths, facial-control intent, head/body motion, overlays, key-pose order and timestamps, duration, easing/hold notes, loop/exit behavior, blink/gaze/lip-sync interactions, review status, issues, native/export dimensions and hashes. Numeric control weights remain proposed until tested on the real rig.

Proposed production cadence: coherent batches of ten approved sheets, with a journal update and concise progress report. This is a proposal for this repository, not inherited authorization from another project. Use direct commits, never CI; avoid credentials, unrelated source material or generated caches in Git.

## Not included in this planning delivery

No new generated character art; no completed 200-expression catalogue or 1,800 panels; no actual animation files; no mesh, UV map or fitted texture atlas; no Blender rig, weights, shape keys or physics; no runtime export; no app/tracking compatibility validation; and no communication with Kimi. Only the plan, reference intake/review and supplied reference images are being delivered now.

## Sources

- [3D VTuber Model Creation guide](https://vtubergame.com/blog/how-to-make-a-3d-vtuber-model), supplied as a 21-page PDF: pages 5–6 for visual references, topology and an early facial prototype; pages 7–8 for modular parts and rigging; pages 9–12 for export, tracking and testing. The 200-performance target and nine-key-pose format are project proposals, not requirements from that guide.
- [VRM 1.0 expression specification](https://github.com/vrm-c/vrm-specification/blob/master/specification/VRMC_vrm-1.0/expressions.md), for presets, custom expressions and procedural overrides. Confirm the actual runtime/version before adopting this mapping. Use the target application's primary documentation for compatibility rather than assuming the guide's broad app examples are interchangeable.

# Ryoko VTuber Phased Build Plan

**Version:** 1.2 source production and builder handoff  
**Prepared:** 2026-11-01  
**Repository:** TianJieHeng/ryoko-vtuber  
**Current status:** source-art production and local QA are complete: 273 accepted primary sources, 2,352 extracted panels and 200 peak copies, published in five batches of 50 plus a final 23-source remainder. Full-character wall projection is confirmed. Actual model, UV, rig, animation and runtime implementation remain separate future work; see publication metadata for remote verification.

## Goal and delivery boundary

Create a consistent visual production pack for the supplied human Ryoko character, then hand it to the user's Kimi workflow for construction and rigging in Blender. The target is 200 distinct expression performances, each with a nine-panel motion reference sheet, alongside modeling references and separate facial-control references.

The source-reference stage is complete to the delivered inventory, with two rejected control references explicitly omitted. The model/runtime stage is not complete. Images communicate design intent. They do not contain mesh topology, UV coordinates, skin weights, shape keys, animation curves, or a working avatar. Those must be authored and tested on the actual model. The 200 performances can combine reusable controls; they do not require 200 independent morph targets.

The supplied references depict a green/mint-haired businesswoman with amber/gold eyes, a dark trouser suit, open white blouse, gold hair ornaments and jewelry, and black heels. Do not import the appearance of any earlier masked or black-haired Ryoko design. Preserve the six originals unchanged. Their visual differences must be resolved before declaring one production design canonical.

## Status and ownership

| Phase | Deliverable | Owner | Current status |
|---|---|---|---|
| 0 | Reference intake and design decisions | G and user | Six originals preserved; working source-art masters reviewed; modeling decisions remain |
| 1 | Modeling reference pack | G | Seven modeling and four detail sources accepted and delivered |
| 2 | Five expression pilots and control prototype references | G | Pilot source sheets produced; reference art only |
| 3 | Blender facial feasibility prototype | User's Kimi workflow | Not started or validated by this workflow |
| 4 | Facial-control reference pack | G | 22 generic references; jawLeft and lowerLipDepress unavailable; not ARKit certification |
| 5 | 200 expression performances and motion sheets | G | All 200 expression sheets accepted and delivered; reference art only |
| 6 | Visual pack QA and production handoff | G | Final source inventory reconciled; builder handoff delivered; remote verification recorded in metadata |
| 7 | Mesh, textures, rig and animation implementation | User's Kimi workflow | Not started by this workflow |
| 8 | Target application testing and release | User and build workflow | Not performed; runtime unspecified |

Owner labels describe the intended division of work, not an active connection to Kimi or authorization to send it files. Generation approval now covers the source-image phase. Use the common neutral master and documented design choices, with quality checkpoints rather than requesting permission for every routine asset. Do not imply that the pending Blender stages have been started or validated.

## Phase 0 Reference intake and design lock

**Inputs:** six supplied PNG sheets and the 21-page Blender workflow guide. Preserve original bytes, record original filename, repository path, pixel dimensions and SHA-256, and inspect the actual images. Record findings in `references/REFERENCE_REVIEW.md` and inventory in `references/manifest.json`.

The [visual review](references/REFERENCE_REVIEW.md) proposes REF-001 for silhouette, REF-006 for technical details, REF-005 for facial range, and REF-002–004 for acting intent. This hierarchy informed the working visual interpretation, not a measured or user-certified model specification. The reviewed neutral master and front/back body masters govern source-art consistency. REF-005 has 16 portraits; the three special sheets add 18 numbered performances with overlaps, not 34 guaranteed unique production expressions. Resolve hair bun/ponytail construction, jewelry placement, collar/buttons and pocket details explicitly.

Implementation choices to preserve or resolve on the actual model:

- Which turnaround controls anatomy, hair silhouette, costume, footwear and accessories when sheets differ?
- Are all supplied costumes one outfit, or are any alternates? Do not average contradictory details.
- **Resolved:** full character, not bust-only. The user intends to project her onto a wall. Include readable full-body silhouette and gestures alongside facial close-ups. The exact runtime and tracking method remain open.
- What application, export format/version and tracking input will receive the avatar? Confirm webcam, iPhone facial capture, prerecorded animation, or a combination.
- Which exaggerated effects are desired: blush, tears, sweat marks, sparkle eyes, comic symbols, or chibi transformations?

Create a short design lock identifying approved references, proportions, palette, accessory placement and character left/right. Treat source captions as reference annotations, not permission to invent missing back/side details or change the design. New unseen details require an explicit design proposal.

**Source-stage record:** originals verified, conflicts documented, and working masters visually reviewed under the approved source-production scope. Unresolved implementation choices may remain listed, but do not label dependent assets compatible or production-ready.

## Phase 1 Modeling reference pack

**Depends on:** supplied design references and the common production master. Source generation is approved. Document interpretation choices; unresolved runtime details do not prevent model-independent reference art.

Prepare clean, consistently scaled front, side and back full-character views for the approved coverage, plus three-quarter checks. Use straight, orthographic-style presentation without dramatic camera distortion. Generated drawings are visual guides, not dimensionally certified CAD projections.

Add a neutral A-pose or T-pose as chosen for the build; head front/profile/three-quarter close-ups; hair silhouette and section breakdown; eye and mouth-interior details; hands; outfit construction; footwear; and accessories. Mark rigid pieces separately from hair, cloth and other intended moving parts. Show occluded structures separately where necessary rather than claiming that one silhouette defines their geometry.

Use neutral lighting, a fixed background and restrained shading so facial planes and color are readable. Keep character scale, eye line, crop and camera consistent across matched sets. Produce independent view images as well as assembled review sheets.

**Delivered source-stage record:** seven modeling and four detail references are included. Additional optional view studies mentioned above are not implied by those counts; resolve missing viewpoints, perspective and artistic interpretation during actual modeling.

## Phase 2 Small expression pilot

**Depends on:** common production master.

Produce five varied performances first: EXP-101 restrained-confidence, EXP-002 affectionate-warmth, EXP-141 embarrassment, EXP-041 controlled-anger and EXP-061 broad-surprise. Each receives a nine-panel key-pose source sheet and motion notes. The user has approved lossless peak and panel extraction. Actual extracted files, crop bounds and hashes are recorded in `metadata/frame_extraction.json`; do not count unrecorded derivatives as produced. Include neutral, blink and a few mouth-shape reference tests for the model prototype.

Review identity, hair and accessory stability, eyelid anatomy, mouth construction, expression clarity, and unwanted changes in head scale or pose. A face-only deformation sheet keeps the head still. Gestures and head turns belong in separately identified performance references, so Kimi can distinguish facial deformation from skeletal motion.

**Exit gate:** pilot demonstrates the intended style and enough consistency to scale. Revise the master if recurring errors appear; do not produce 195 more variations of a broken template.

## Phase 3 Blender feasibility checkpoint

**Depends on:** pilot references and a model built by the user's workflow.

Kimi blocks and tests the neutral head, eyelid closure, eye motion, jaw opening, a smile and initial lip-sync shapes. Check silhouette against the references and test how controls combine. Obtain rendered comparisons or the relevant model evidence before declaring this gate passed.

This is deliberately early. Image approval alone cannot prove that eyelids close correctly, teeth stay inside the mouth or facial shapes deform cleanly. While this gate is pending, continue authorized model-independent reference production and maintain the expression catalogue. Do not report model validation. This is an implementation checkpoint, not a blocker for the source-image phase.

**Exit gate:** prototype judged feasible on the real mesh; observed issues returned to the visual pack or model implementation with clear ownership.

## Phase 4 Facial control reference pack

**Depends on:** common master for generic visual control references. Exact tracking mappings depend on the selected route and later prototype findings. The current inventory contains 22 generic control references, not certified ARKit coverage. jawLeft and lowerLipDepress attempts failed isolation and are not delivered; jawRight is a three-panel comparison.

Build isolated references for brows, eyelids, gaze, cheeks, jaw and mouth, including asymmetric left/right movements. Neutral remains the common baseline. If the chosen route uses ARKit, cover its approximately 52 standard facial controls with exact names verified against the selected implementation. These controls are separate from the 200 performances and are not counted as emotions.

If VRM is selected, define the version-specific expression mapping, including supported emotion, lip-sync, blink and gaze behavior. Define whether each custom performance allows, blends or suppresses procedural lip sync, blinking and gaze. Do not assume all target applications expose every custom expression identically.

Add mouth-shape references suitable for the selected lip-sync system, with visible teeth/tongue guidance where needed. Do not treat a painted mouth or a flat facial grid as an implemented blendshape.

**Exit gate:** complete control inventory for the selected target, unambiguous left/right convention, and reference-to-control mapping reviewed by the builder.

## Phase 5 Expression and motion production

**Depends on:** common master, pilot quality review and stable semantic control plan. Blender prototype validation may remain pending while authorized model-independent references are produced.

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

The five pilots occupy appropriate IDs within these 200; they are not five extras. The complete authored [200-expression catalogue](metadata/expressions.json) names and describes every performance, including all nine key poses and proposed timings. Review near-duplicates during production. Different labels alone do not establish different expressions. Define the recognizable combination of brows, eyes, cheeks and mouth, with any gesture or overlay separately specified.

Each performance has nine key poses: neutral, anticipation, onset, build, peak, follow-through or hold, release, settle and neutral. This creates **200 motion sheets and 1,800 reference panels**. The repeated neutral panels are intentional boundaries, not 1,800 distinct expressions. Laughing, crying and other cycles use an appropriate revised sequence and explicit loop boundaries rather than a forced one-shot arc.

Specify key-pose timestamps, hold duration, easing intent, total duration, loop behavior and return-to-neutral behavior. Nine images do not imply nine evenly spaced playback frames. Blender will create the interpolated motion and rendered animation later. For wall projection, include full-body crossed arms, raised-eyebrow stares, finger-wag reprimands and stern balanced stances with clear silhouettes. Hand/body gestures use separate skeletal performance references; chibi panels in source sheets do not automatically authorize changing the avatar's proportions.

**Exit gate:** all 200 IDs have reviewed peak and motion references, complete metadata, distinct readable intent, and no unresolved identity drift.

## Phase 6 Quality control and handoff

Check every sheet for correct panel order/count, consistent face and eye line, stable costume/accessories, coherent anatomy, clear silhouettes and readable movement. Check facial controls independently and in combinations such as smile plus lip sync, gaze plus blink, or tears plus an expression. On images, this is a visual review; deformation and collision checks still belong to the actual rig.

Preserve generation originals and record their real dimensions. Never describe resized images as native higher-resolution output. Lossless integer panel extraction and peak copying were authorized and completed with original sheets preserved. Further scaling, alpha work or registration is separate work and is not implied by that crop approval. A transparent-background requirement must produce genuine alpha, not a painted checkerboard.

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

**Approved production cadence:** push completed source assets in batches of 50, update the journal and manifest, and verify the remote files. Publish the final remainder when the authorized batch is complete; do not leave fewer than 50 final assets stranded. Count source assets and expression performances separately from panels and derivative files. Use direct commits, never CI; avoid credentials, unrelated source material or generated caches in Git.

## Current implementation boundary

The delivered catalogue contains 200 accepted expression source sheets and 1,800 expression key-pose panels, alongside 40 body and 22 generic-control references. The full pack totals 273 primary sources, 2,352 cropped panels and 200 peak copies; actual paths, dimensions, hashes and review records are present. The earlier 275-source planning target was reduced by the two rejected controls, jawLeft and lowerLipDepress. Extraction is complete and recorded in `metadata/frame_extraction.json`; crops are not registered or interpolated animation frames.

No actual animation files, mesh, UV map, fitted texture atlas, Blender rig, weights, shape keys, physics, runtime export or app/tracking validation is claimed. No direct communication with Kimi is implied. Facial close-ups supplement the full-character pack; they do not replace it.

## Builder handoff

Use [BUILDER_HANDOFF.md](handoff/BUILDER_HANDOFF.md) for the actual pack navigation and practical model/rig workflow, and [NOT_INCLUDED.md](handoff/NOT_INCLUDED.md) for explicit missing or unvalidated deliverables. Final accepted and published counts come from QA and publication metadata, not the target counts in this plan. EXP-094 is now about-to-sneeze; use the current catalogue and replacement provenance.

## Sources

- [3D VTuber Model Creation guide](https://vtubergame.com/blog/how-to-make-a-3d-vtuber-model), supplied as a 21-page PDF: pages 5–6 for visual references, topology and an early facial prototype; pages 7–8 for modular parts and rigging; pages 9–12 for export, tracking and testing. The 200-performance target and nine-key-pose format are project proposals, not requirements from that guide.
- [VRM 1.0 expression specification](https://github.com/vrm-c/vrm-specification/blob/master/specification/VRMC_vrm-1.0/expressions.md), for presets, custom expressions and procedural overrides. Confirm the actual runtime/version before adopting this mapping. Use the target application's primary documentation for compatibility rather than assuming the guide's broad app examples are interchangeable.

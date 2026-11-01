# Ryoko VTuber Build Journal

## 2026-11-01 Planning and reference intake

**Requested scope:** review six attached character sheets, add the references to `TianJieHeng/ryoko-vtuber`, and create a phased build plan. No image generation or Blender implementation was requested for this pass.

**Prepared:** phased plan, repository overview, reference inventory and visual review. The plan separates source images, tracking-control references, 200 expression performances, motion key poses, and the later model/UV/rig/runtime stages. It includes an early Blender facial prototype gate before bulk production.

**State at initial planning:** not started. Approval of the plan, resolution of reference conflicts, avatar coverage and target application/tracking are still required before dependent work.

**Publication verification:** commit `57ebde4489b634f5bde55a28ab7e400ebad979e4` was confirmed on `main`. All 11 remote file blobs matched the local Git hashes: three root documents, the reference review and manifest, and six unchanged original PNGs totaling 16,063,442 bytes. Original PNG SHA-256 values and byte lengths also matched the reference manifest. No CI or model/runtime validation was run. This follow-up journal entry records that verified publication; it does not claim production is complete.

## 2026-11-01 Source production authorized

The user approved image generation and Git pushes in batches of 50, then explicitly confirmed full-character coverage rather than bust-only. Intended presentation is a wall-projected character, including scolding performances. Exact runtime/tracking remains unspecified.

Prepared `metadata/expressions.json` with 200 unique authored expression IDs/slugs across ten families, 20 per family, and nine timed key-pose specifications per expression. The five pilots map to EXP-002, EXP-041, EXP-061, EXP-101 and EXP-141. Planned filenames, separate gesture/overlay fields and procedural interaction notes are present. No numerical rig weights are invented.

Local validation passed: 200 records, 200 unique slugs and 1,800 key-pose records. Image statuses in this catalogue start as planned; producers must record actual completion evidence. Separate peak/panel extraction is not claimed complete. Generic control sheets must not be advertised as certified ARKit coverage.

Updated the build plan so pending Blender validation does not block model-independent reference production. Actual mesh, UV, rig, animation and runtime stages remain unstarted. Source-image completion and remote publication evidence are maintained by the production/publishing workflow.

## 2026-11-01 — source-art batch 001

The user authorized generation, batches of 50, full-character coverage and splitting finished nine-panel sheets into individual frames. This batch contains exactly 50 accepted primary images: 7 modeling, 4 detail, 8 control, 28 expression and 3 full-body gesture sources. It also contains 351 lossless integer-cropped panels and 28 peak copies from 39 source sheets; derivatives do not inflate the primary count.

The frozen asset manifest lists 529 image/sidecar/prompt files totaling 189,048,869 bytes. Every listed local file was checked against its frozen SHA-256 and length before publication. Source images and six original reference PNGs are unchanged. Catalogue/index/extraction metadata is restricted to this batch's published assets; later arrivals and unaccepted variants are excluded. Remote verification is recorded in the subsequent journal checkpoint after the committed tree is checked. No CI, model/UV/rig or runtime validation is claimed.

Metadata-only refresh: eight control sidecars gained `panel_count: 9` and `layout: 3x3_keyposes`. Removing these fields exactly reproduced their frozen original SHA-256 and size. The frozen 50-source list and all image bytes are unchanged; the asset-related total increased by 384 bytes to 189,048,869.

### Batch 001 remote verification

Commit `b9bf8316ec37a5f637e38cd650485ade0c07a5f7` was confirmed on `main`. All 548 remote file blobs matched the expected local Git hashes, including the 50 primary generated images, 351 extracted panels and 28 peak copies. The eight existing reference files (six original PNGs, manifest and review) are unchanged. Only the three root planning documents were intentionally updated among the prior files. No files from later batches or unaccepted variants were included. This records source-art publication and byte integrity, not model/rig/runtime validation.

## 2026-11-01 — source-art batch 002

A second separate batch publishes 50 new accepted primary images with no overlap with batch 001, plus 444 derived panels and 27 peak copies. One jaw comparison has three panels; the other 49 sheets have nine. The frozen asset manifest lists 621 asset-related files total 203,513,439 bytes; all SHA-256 values and sizes matched the approved snapshot.

Cumulative publication: 100 primary source images, 795 extracted panels and 55 peak copies. Catalogue, index, body and extraction metadata is filtered to these 100 published sources, not later local arrivals. Source images and original reference PNGs remain byte-identical. Remote verification follows the atomic batch commit. No CI, model/UV/rig/runtime implementation is claimed.

### Batch 002 remote verification

Commit `fd4ddddd794976ec4264dd22918a8fb14e5bf416` was confirmed on `main`. All 1,171 remote file blobs matched expected local Git hashes. This verifies 100 cumulative primary source images, 795 derived panels and 55 peak copies. Every previously published image and the six original user references remain byte-identical. Later local arrivals and rejected variants are excluded. This is reference-art byte verification, not a working model, rig or runtime.

## 2026-11-01 — source-art batch 003

A third separate batch contains 50 new accepted primary source images, 450 lossless panels and 32 peak copies, with no prior source overlap. Cumulative delivery is 150 primary images, 1,245 panels and 87 peak copies. Three EXP-091–093 JSON sidecars were finalized after review: status, actual reference IDs and visual-review notes only. Reversing precisely these approved fields reproduces each original frozen JSON hash and size; all source PNG, prompt and crop bytes are unchanged. The manifest records this metadata-only refresh. Rejected BOD-031 is excluded. Remote verification follows the atomic batch commit; no CI or model/UV/rig/runtime implementation is claimed.

### Batch 003 remote verification

Commit `617d2c9eba1c632e3f1c85eafcca560ce0052cd7` was confirmed on `main`. All 1,805 remote file blobs matched the expected local Git hashes. Cumulative delivery: 150 primary sources, 1,245 derived panels and 87 peak copies. Prior images and six original reference PNGs remain byte-identical. Later local arrivals and unaccepted variants are excluded. This verifies reference-art publication, not a working model, rig or runtime.


## 2026-11-01 — source-art batch 004

A fourth separate batch contains 50 new accepted primary images, 450 derived panels and 40 peak copies. All 640 frozen image/metadata/prompt files matched their approved SHA-256 and size (210,581,308 bytes), with no previous source overlap. Cumulative delivery is 200 primary sources, 1,695 panels and 127 peak copies. Metadata is restricted to these published sources; later arrivals and unaccepted variants are excluded. Integer crops preserve source pixels and are not registered animation. Remote verification follows the atomic batch commit; no CI or actual model/runtime validation is claimed.

### Batch 004 remote verification

Commit `df8069eac63a03e9abcb52d8316557ec124e58cd` was confirmed on `main`. All 2,447 remote file blobs matched the expected local Git hashes. Cumulative delivery: 200 primary sources, 1,695 derived panels and 127 peak copies. Prior images and six original reference PNGs remain byte-identical. Later local arrivals and rejected variants are excluded. This verifies reference-art publication, not a working model, rig or runtime.


## 2026-11-01 — source-art batch 005

A fifth separate batch contains 50 new accepted expression sheets, 450 derived panels and 50 peak copies. All 650 frozen asset-related files matched their approved SHA-256 and size (226,923,390 bytes), with no overlap with prior source paths. Cumulative publication is 250 primary sources, 2,145 derived panels and 177 peak copies. Metadata is filtered to these 250 sources; final remainder and handoff drafts are not included. Original images remain unchanged. Remote verification follows the atomic commit; no CI or actual model/runtime validation is claimed.

### Batch 005 remote verification

Commit `985012b0f3f267491a11be3ce5ae05d5cc98007a` was confirmed on `main`. All 3,099 remote file blobs matched the expected local Git hashes. This verifies 250 cumulative primary source images, 2,145 derived panels and 177 peak copies. Prior images and six original reference PNGs remain byte-identical. Later local arrivals and rejected variants are excluded. This verifies source-art publication, not a working model, rig or runtime.


## 2026-11-01 — final source-art remainder, batch 006

The final remainder contains 23 new accepted expression sheets, 207 lossless panels and 23 peak copies. All 299 frozen asset-related files matched approved SHA-256 and size (105,240,709 bytes), with no previous source overlap. Cumulative inventory is 273 primary sources: 200 expressions, 40 body gestures, 22 generic controls, 7 modeling views and 4 details, plus 2,352 panels and 200 peak copies. These are 2,825 asset PNGs, excluding 6 original references.

The planned jawLeft and lowerLipDepress references were rejected because attempts did not isolate their motions reliably; no accepted versions are included. This explains 273 delivered sources versus the earlier 275 planning target. Source-art production and local QA are complete; actual model/UV/rig/runtime work is not. Approved builder handoff and limitations accompany the final source pack. Remote verification follows the atomic batch commit.

### Final source-pack remote verification

Commit `ee148303b007d85a274c3c670eccfbbb0858d196` was confirmed on `main`. All 3,408 remote file blobs matched the expected local Git hashes. The published inventory contains 273 unique primary source images, 2,352 losslessly extracted panels and 200 peak copies: 2,825 asset PNGs, plus the six unchanged original reference PNGs. Every earlier published image remains byte-identical. Final catalogue and pixel-integrity reports contain no errors.

The builder handoff, explicit omissions and publication-status report are included. jawLeft and lowerLipDepress remain unavailable rather than being falsely labeled complete. No 3D model, UV fitting, rig, runtime compatibility or animation playback is claimed. No CI ran. This final report-only checkpoint updates the journal and publication status; its complete remote tree is checked again after publication.

## 2026-11-01 — implementation Phase 0: target and environment

The user authorized phase-by-phase implementation with GitHub and build-journal checkpoints, plus matched Blender/reference comparisons and explicit approval before dependent visual work proceeds.

The user selected **VSeeFace with VRM**, **iPhone facial capture plus webcam body tracking**, and a **high-detail 1440p60** target. The user subsequently clarified that idle and other performances will be authored in Blender because an AI will control the avatar. The target specification therefore treats Blender actions as the primary performance library and live tracking as an optional input/override. The AI will select, blend, interrupt, and recover authored states; the exact control bridge and possible Unity/VRM layer remain integration work.

The current VSeeFace manual confirms that VRM0X/VRM 0.x is required and VRM 1.0 is unsupported. Its iPhone perfect-sync route requires all 52 ARKit blendshape clips. Ordinary VSeeFace webcam tracking is not treated as built-in full-body tracking; webcam body input requires a compatible VMC route. No runtime compatibility is claimed from these documentation checks.

Environment verification succeeded: `/usr/local/bin/3dpy` launched Blender **5.2.1 LTS**, and the character-generation dependency check reported `agent-gw` **0.3.0**. No model generation, mesh, rig, or expression implementation has occurred.

Phase files published:

- `vtuber/docs/target_specification.md` — runtime, AI-directed animation architecture, tracking, performance target, and validation boundary
- `vtuber/docs/dependencies.md` — verified authoring environment, later runtime dependencies, and checkpoint evidence rules

Phase 0 documentation commits before this journal checkpoint: `be751c2e0dcfb84c55185f2c3c856529485b8b8b` and `8ee1eccd89115d91347459baea319d453bb6fb39`. A prior parallel-write race produced one 409 response; the target specification was then written sequentially with the AI-control requirement included. No file content was lost.

**Phase 0 status:** documentation complete and awaiting user checkpoint approval. No Blender-versus-image comparison applies because no geometry has been built. Phase 1 design lock has not started.

## 2026-11-01 — implementation Phase 1: visual design lock

Phase 1 began after the user gave no preference on the Phase 0 checkpoint and the implementation workflow proceeded with the committed specification. The user clarified that Blender-authored idle and other actions will be controlled by an AI; this is recorded in the Phase 0 target and carried into the Phase 1 layering/performance contract.

The private repository initially prevented binary reference downloads. The user made the repository public. Direct sandbox connections to GitHub's raw host still timed out, so the same public repository images were retrieved through an image proxy for local visual review. The repository source files were not modified; proxy-derived local review copies are not claimed to be byte-identical preservation copies.

Eleven approved images were actually opened and visually inspected: neutral bust, front/side/back/A-pose full-body masters, eye and mouth sheets, and hair/accessory/outfit/hands-pumps detail sheets. Two rendered reference boards were assembled, opened, and inspected for framing and readability: a turnaround board and a face/construction board.

The proposed design lock resolves the rear hairstyle as a high bun-loop with a short loose ponytail fan, locks the long fringe to character-right, places the pocket square on character-left, and distinguishes rigid accessories from moving chains and hair groups. It defines scale/axes, the A-pose, construction order, mouth/eye requirements, initial high-detail budgets, and AI-compatible channel separation.

Published in commit `ce4735cd0b11394fefc650d37aa73c1bf1bf7641`:

- `vtuber/docs/design_lock.md`
- `vtuber/docs/open_design_decisions.md`
- `vtuber/previews/phase_01_reference_board.md`

**Phase 1 status:** visual design proposal and reference checkpoints complete; awaiting user approval before Phase 2 blockout. No model generation, Blender geometry, rig, expression shape, animation, or runtime validation has occurred.

## 2026-11-02 — implementation Phase 2: full-character blockout

The user approved Phase 1 with “Lookin good continue to the next stage.” The approved front, left-side, and back full-body references were used as multiview inputs to **Tripo API** model `v3.1`, with an 80,000-face target and textures disabled. Successful upstream task: `d8fd4168-12f1-4175-810d-02e05ceace79`. Tripo API generated the untextured full-body blockout only; it did not generate production topology, a rig, expressions, animation, or a VRM.

The GLB was imported into Blender 5.2.1 LTS, normalized to a provisional 1.83 m total height, assigned neutral clay, and rendered through CPU Cycles. The saved source was reopened in a separate Blender process. Read-back measured one character mesh, 43,766 vertices, 76,402 triangles, zero armatures, zero shape-key blocks, zero loose vertices, and 10,724 boundary/non-manifold edges. It is therefore a visual blockout, not a mesh suitable for direct production rigging.

Eight orbit views and a top view were inspected, followed by matched front/left-side/back/three-quarter comparisons, five head angles, rear hair, and both hands. Correction rounds were recorded: generated forward +X was aligned to authoring forward -Y; an underlit face received a frontal review fill, reduced from a clipping 650 W test to 180 W; and an oversized top-camera frame was tightened from 2.6 m to 0.75 m. Final boards and the browser review were opened and visually inspected. The static browser check passed with zero failures and no missing assets; its animation-loop check was intentionally skipped because the review page is static.

The comparison records real mismatches rather than treating generation as final quality: fuller bust/hip/thigh volumes, softer and younger facial proportions, shallow eye/nose/lip forms, no separate eye or mouth structures, coarse hands and ornaments, and an arms-down pose rather than the A-pose construction sheet. These corrections carry into production reconstruction. No expression approval is implied.

Published before this journal checkpoint:

- Commit `ebd4f08442ed4614d6fea55e311b4cbe6f9598c4`: `vtuber/docs/phase_02_blockout.md`, `vtuber/CREDITS.md`, and measured correction/validation JSON under `vtuber/data/`.
- Commit `b483450c9c223265be55cffbf4d4c1cfeb9b9ca8`: Blender build, final-render, and reopen-validation scripts under `vtuber/scripts/`.

The editable `.blend`, generated GLB, final renders, and reference-versus-Blender boards are delivered through the Phase 2 browser review version `22e43dc`; the source is also downloadable from that review.

**Phase 2 status:** full-character blockout and internal visual verification complete; awaiting explicit user approval before Phase 03 production topology, UVs, and material separation. No facial expression, body rig, animation, VRM export, or runtime certification has occurred.

## 2026-11-02 — implementation Phase 2 revision: two-chopstick hair accessory

The user approved the overall blockout but identified the generated hair spikes as two chopsticks and requested a correction. The generated side protrusions and coarse accessory forms were removed. Exactly two separate tapered gold shafts now cross the bun and project together toward character-left (+X), with two rounded finials and one short three-link chain and pendant on the lower stick. The edit removed 650 generated vertices. Two neutral bun-core objects temporarily close the edited generated hair surface; they are explicitly blockout patches and will be replaced during production hair reconstruction.

The revised v002 `.blend` was reopened in a separate Blender process and validated: one generated-base mesh with 43,116 vertices, 75,366 triangles, 10,472 boundary edges, and 10,475 non-manifold edges; 13 separate accessory/core objects; exactly two shafts, two finials, and three chain links; zero armatures and zero shape-key blocks; and the locked -90-degree authoring-root rotation. This passes only as a revised visual blockout, not as production topology.

The complete matched-view, close-up, hand, eight-angle orbit, and top-view set was rendered again. The focused accessory reference-versus-Blender board and refreshed full-body, face/hair, hands, and orbit boards were opened and inspected. The browser review now includes the focused revision board and v002 source download. Static browser verification passed with zero failures, no page errors, and no missing assets; all links and local images resolve. Its animation-loop check was intentionally skipped because the review is static.

Published before this journal checkpoint:

- Commit `1170a2ea0c1097087df23ed5392c02653cf46c41`: the v002 revision, final-render, and reopen-validation scripts; revision and validation JSON; and the Phase 2 documentation addendum.
- Browser review version `e84e90b`: revised comparison boards and downloadable v002 Blender source.

**Phase 2 revision status:** accessory correction and internal visual verification complete; awaiting explicit user confirmation before Phase 03 production topology, UVs, and material separation. No facial expression, body rig, animation, VRM export, or runtime certification has occurred.

## 2026-11-02 — implementation Phase 3: modular surface, UVs, and fitted textures

The user approved the revised Phase 2 checkpoint with “Nice I approve you can move to the next phase,” authorizing Phase 3 only. Automatic whole-body replacement routes were evaluated but not accepted: QuadriFlow fragmented the surface; voxel replacements produced severe holes or excessive density; selective skin voxel union damaged the head/right arm and was reverted. **Tripo API** smart retopology (`decimate --model v2.0 --face-limit 20000`, returned task `ae55137b-d423-4c9a-87ab-cb729cf33c2c`) produced 25,627 triangles but retained 24,753 boundary/non-manifold edges and no quad faces, so it was rejected as production-ready deformation topology.

The final candidate retains the approved v002 surface. **Tripo API** semantic segmentation (`segment --model v2.0 --granularity balanced`, returned task `370e5e56-a084-4f07-a529-acae63195812`) supplied ten semantic parts used only as nearest-surface labels for modular separation, not replacement geometry. Blender construction created ten major parts, preserved all thirteen accessory/core objects, repaired only narrow boundary loops, added one subdivision density pass to the head/neck and arm/hand regions, created UVs, and baked fitted base-color/roughness textures. The face, hidden mouth, essential deformation loops, body rig, and expression system remain unfinished.

The first reference comparison caught bare upper arms conflicting with the approved full-sleeve blazer. The arm material regions were corrected to charcoal sleeves, ivory wrist cuffs, and skin hands; all affected textures, full-body views, orbit views, hand close-ups, and comparison boards were rebuilt and inspected. Both arms now show full sleeves and both cuff transitions are visible. This is a material correction, not a certification of wrist deformation topology.

The saved textured source was reopened and validated: 78,095 main-part vertices, 140,767 main-part triangles, 39,217 main-part quad faces, 14,865 boundary/non-manifold edges, 13 accessory/core objects with 4,080 triangles, and 144,847 total character triangles. Every major part has one UV layer and base-color/roughness textures; all 20 images are packed. Exactly two chopstick shafts and three chain links remain; there are zero armatures and zero shape-key blocks. The triangle inventory is within the provisional authoring budget but is not a measured 1440p60 runtime result. UV coverage is complete, while fragmented islands and uneven texel density remain documented limitations. Skin shadow visibility is disabled only to suppress internal-shell artifacts in checkpoint rendering.

Published before this journal checkpoint:

- Commit `a64b055624389706b81767c3bbc2f9fc3a494558`: six Phase 3 build, texture, render, checker, validation, and comparison-packaging scripts.
- Commit `3fe1f8147740dc7194efe6c54f35b2fdca75cc4e`: modular mesh and fitted-texture metrics.
- Commit `4d43fa1b52425065cc38ca6c507e3a8b146acfb0`: saved-source geometry, UV, packed-texture, accessory, and budget validation.
- Commit `c5854ea096fcfabf029b50bbbf02b505857bb6bd`: Phase 3 documentation, evidence index, and Tripo API attribution.
- Browser review version `650df90`: six final evidence boards and the downloadable packed textured Blender foundation.

Static browser verification passed with no missing assets; all navigation links were clicked and reached their sections; desktop and 375 px mobile layouts were inspected; final console errors and warnings were zero. Rejected meshes, diagnostic renders, redundant backup saves, and process captures were removed from the checkpoint.

**Phase 3 status:** modular visual/UV foundation and internal verification complete; awaiting explicit user approval. Open clothing/hair topology, generated skin shells, incomplete deformation loops, facial identity, UV consolidation, and hand anatomy remain known limitations. Phase 4 facial feasibility and expression comparisons have not started and remain gated. No body rig, ARKit clips, animation, VRM export, VSeeFace/tracking/AI runtime, or projection validation is claimed.

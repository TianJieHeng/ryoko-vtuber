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

Commit `b9bf8316ec37a5f637e38cd650485ade0c07a5f7` was confirmed on `main`. All 548 remote file blobs matched the expected local Git hashes, including the 50 primary generated images, 351 extracted panels and 28 peak copies. The eight existing reference files (six original PNGs, manifest and review) are unchanged. No files from later batches or unaccepted variants were included. Only the three root planning documents were intentionally updated among the prior files. This records source-art publication and byte integrity, not model/rig/runtime validation.

## 2026-11-01 — source-art batch 002

A second separate batch publishes 50 new accepted primary images with no overlap with batch 001, plus 444 derived panels and 27 peak copies. One jaw comparison has three panels; the other 49 sheets have nine. The frozen 621 asset-related files total 203,513,439 bytes; all SHA-256 values and sizes matched the approved snapshot.

Cumulative publication: 100 primary source images, 795 extracted panels and 55 peak copies. Catalogue, index, body and extraction metadata is filtered to these 100 published sources, not later local arrivals. Source images and original references remain unchanged. No CI or model/rig/runtime implementation is claimed. Remote verification follows the atomic batch commit.

### Batch 002 remote verification

Commit `fd4ddddd794976ec4264dd22918a8fb14e5bf416` was confirmed on `main`. All 1,171 remote file blobs matched the expected local Git hashes. This verifies 100 cumulative primary source images, 795 derived panels and 55 peak copies. Every previously published image and the six original user references remain byte-identical. Later local arrivals and rejected variants are excluded. This is reference-art byte verification, not model/rig/runtime validation.

## 2026-11-01 — source-art batch 003

A third separate batch contains 50 new accepted primary source images, 450 lossless panels and 32 peak copies, with no prior source overlap. Cumulative delivery is 150 primary images, 1,245 panels and 87 peak copies. Three EXP-091–093 JSON sidecars were finalized after review: status, actual reference IDs and visual-review notes only. Reversing precisely these approved fields reproduces each original frozen JSON hash and size; all source PNG, prompt and crop bytes are unchanged. The manifest records this metadata-only refresh. Rejected BOD-031 is excluded. Remote verification follows the atomic commit; no CI or model/runtime validation is claimed.

### Batch 003 remote verification

Commit `617d2c9eba1c632e3f1c85eafcca560ce0052cd7` was confirmed on `main`. All 1,805 remote file blobs matched expected local Git hashes. Cumulative delivery: 150 primary source images, 1,245 derived panels and 87 peak copies. Prior images and six original reference PNGs remain byte-identical. Later local arrivals and unaccepted variants are excluded. This verifies reference-art publication, not a working model, rig or runtime.


## 2026-11-01 — source-art batch 004

A fourth separate batch contains 50 new accepted primary images, 450 derived panels and 40 peak copies. All 640 frozen image/metadata/prompt files matched their approved SHA-256 and size (210,581,308 bytes), with no previous source overlap. Cumulative delivery is 200 primary sources, 1,695 panels and 127 peak copies. Metadata is restricted to these published sources; later local arrivals and rejected variants are excluded. Integer crops preserve source pixels and are not registered animation. Remote verification follows the atomic commit; no CI or model/runtime validation is claimed.

### Batch 004 remote verification

Commit `df8069eac63a03e9abcb52d8316557ec124e58cd` was confirmed on `main`. All 2,447 remote file blobs matched expected local Git hashes. Cumulative delivery: 200 primary source images, 1,695 derived panels and 127 peak copies. Prior images and six original reference PNGs remain byte-identical. Later local arrivals and unaccepted variants are excluded. This verifies reference-art publication, not a working model, rig or runtime.


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

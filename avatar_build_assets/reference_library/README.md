# Ryoko Full-Character Source Pack

**Source-art production complete: 273 primary images**, with **2,352 losslessly extracted panels and 200 peak copies**. The six original user reference PNGs remain unchanged. This is a modeling and acting reference pack for a full-character, wall-projected VTuber—not a working 3D avatar.

## Start here

- [Builder handoff](handoff/BUILDER_HANDOFF.md) · [What is not included](handoff/NOT_INCLUDED.md)
- [Asset inventory](metadata/asset_index.json) · [Publication status and verification](metadata/publication_status.json)
- [200-expression catalogue](metadata/expressions.json) · [40 body gestures](metadata/body_gestures.json) · [Control inventory](metadata/controls_inventory.json)
- [Extraction records](metadata/frame_extraction.json) · [QA boundaries](metadata/QA_LIMITATIONS.md)
- [Original references](references/originals/) · [Reference review](references/REFERENCE_REVIEW.md)
- [Phased build plan](BUILD_PLAN.md) · [Build journal](BUILD_JOURNAL.md)

## Delivered inventory

| Primary sources | Count |
|---|---:|
| Expression sheets | 200 |
| Full-body gesture sheets | 40 |
| Generic facial-control references | 22 |
| Modeling references | 7 |
| Detail references | 4 |
| **Total primary images** | **273** |

The 2,352 cropped panels and 200 peak copies are derivatives, not extra generated source images. There are 2,825 PNGs under `assets/`, excluding the six originals under `references/`. Native dimensions and hashes are recorded per file. Source sheets are preserved; crops use exact integer bounds without resizing. They are visual key poses, not registered or interpolated animation frames.

**Two planned control references are not included:** `jawLeft` and `lowerLipDepress` failed isolated-motion fidelity and were rejected rather than mislabeled. This explains 273 delivered sources versus the earlier 275-source target. The 22 generic control guides are not a complete or certified ARKit 52-shape set. `jawRight` is a three-panel comparison, not nine temporal poses.

Facial close-ups pair with reusable body-gesture references; the pack does not contain 200 bespoke synchronized full-body animations. No mesh, UV unwrap, fitted texture atlas, Blender rig, shape keys, skin weights, animation curves, tested export or runtime/tracking compatibility is supplied. Hidden structures and anatomical continuity still need decisions and testing on the real model. No task has been sent to Kimi.

## Publication batches

| Batch | Primary images | Extracted panels | Peak copies |
|---|---:|---:|---:|
| [001](metadata/batch_001_manifest.json) | 50 | 351 | 28 |
| [002](metadata/batch_002_manifest.json) | 50 | 444 | 27 |
| [003](metadata/batch_003_manifest.json) | 50 | 450 | 32 |
| [004](metadata/batch_004_manifest.json) | 50 | 450 | 40 |
| [005](metadata/batch_005_manifest.json) | 50 | 450 | 50 |
| [006](metadata/batch_006_manifest.json) | 23 | 207 | 23 |
| **Total** | **273** | **2,352** | **200** |

[Final catalogue QA](metadata/final_catalogue_validation.json) and [pixel-integrity validation](metadata/integrity_validation.json) report no errors. Current acceptance and publication status lives in the cumulative inventories; per-generation sidecars preserve their generation provenance. Rejected variants and generated caches are excluded. No CI or GitHub Actions were run.

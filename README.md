# Ryoko VTuber

Visual reference and production planning for a 3D VTuber avatar based on the supplied human Ryoko character sheets.

## Start here

- [Phased build plan](BUILD_PLAN.md)
- [Reference review](references/REFERENCE_REVIEW.md)
- [Original reference images](references/originals/)
- [Reference manifest](references/manifest.json)
- [Build journal](BUILD_JOURNAL.md)

## Current production scope

The repository contains the phased plan, six unchanged user references, their inventory and review, and the [complete 200-expression catalogue](metadata/expressions.json).

Source image generation is now authorized. The user confirmed a **full-character avatar for wall projection**, including readable scolding performances, with Git pushes in batches of 50. Facial close-ups supplement full-body views and gesture references.

The plan targets 200 expression performances with nine-key-pose source sheets. The planned 1,800 panels are visual references, not automatically rigged animations or 1,800 separately delivered files. Actual generated file status is recorded separately; planned paths do not prove completion.

No mesh, UV textures, Blender rig, shape keys, weights, physics, runtime export or tracking compatibility is claimed. The neutral/blink/viseme model test remains an important later implementation checkpoint, but does not block authorized model-independent source-art production. Runtime and tracking choices remain open.

No CI or GitHub Actions. Preserve reference originals and record actual native image dimensions for future assets.

## Published source-art batch 001

**50 primary generated reference images:** 7 modeling views/details, 4 construction-detail images, 8 facial-control sheets, 28 expression sheets and 3 full-body gesture sheets. [Frozen batch manifest](metadata/batch_001_manifest.json) · [Asset index](metadata/asset_index.json).

The 39 nine-panel sheets also include **351 extracted key-pose PNGs** and **28 peak-panel copies**. These are authorized integer crops/copies from unchanged source sheets, with no resizing; they do not increase the primary image count. They are visual references, not registered animation frames or a working rig. [Extraction records](metadata/frame_extraction.json) retain bounds, source hashes and crop checks.

The full 200-expression catalogue remains a plan: only 28 expression sheets are published in this batch; remaining entries are marked planned/not published. Later local production is not included here. The six original user reference images remain unchanged.

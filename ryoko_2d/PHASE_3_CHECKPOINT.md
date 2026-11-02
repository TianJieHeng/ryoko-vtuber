# Phase 3 — Registered Body Gestures

## Completed

- Registered and cleaned three canonical full-body alternates on the approved 1024 × 1536 reference space and 2048 × 3072 master canvas:
  - `BOD-002` — scolding / finger-wag.
  - `BOD-001` — stern crossed arms.
  - `BOD-011` — greeting wave.
- Replaced the overlapping upper/lower-body copies with one coherent, source-matched registered drawing per gesture. Each drawing preserves its own jacket hem, pelvis, trousers, ankles, and heels, including the wave pose's jacket-to-hip alignment.
- Preserved the approved canonical head, face, hair, and accessories. Cleaned rear hair contains hair only and remains behind the body; face and front-head layers composite once above each gesture.
- Added a narrow canonical neck bridge and a feathered body transition without stretching the face or blouse. Removed the duplicate body copies and non-hair rear-layer pixels that caused the reported neck, collar, and shoulder overlap lines.
- Restored pale hand interiors with source-space chroma guards and retained complete fingers and true background gaps.
- Removed the identified enclosed thumb-gap sheet components in `BOD-002` and `BOD-011`, with cleanup restricted to small source-registered gap boxes so pale finger edges elsewhere remain intact.
- Corrected the wave head alignment with a 12-reference-pixel horizontal offset applied to the complete canonical head, rear hair, and neck bridge; other gestures remain unchanged.
- Removed alternate-head remnants after registration, residual matte, duplicate neutral parts, rectangular hip fragments, and detached components.
- Preserved original collar, blouse, shoulders, cuffs, pocket details, and garment artwork.

## Tested

`python3 tools/validate_gestures.py` reports `status: passed` for:

- Three registered gestures and their BOD action mappings.
- Single registered full-body artwork and source-matched paths for all three gestures.
- Required neutral-layer hide list and shared neck bridge.
- One significant connected component per gesture body and neck bridge; valid separated hair components for the hair-only rear layer.
- Pixel-identical canonical central face across all three gestures after accounting for the intentional wave-only head offset.
- Zero opaque neutral-white sheet pixels in the source-registered finger-wag and wave thumb-gap regions.
- PNG dimensions matching gesture metadata.

Final full-size and close-up visual review covered the wave head alignment, transparent thumb gaps, preserved raised-hand finger edges, face, neck, shoulders, collar, crossed arms, jacket-to-hip joins, trousers, ankles, and heels against a dark background. The review found no retained white hand-background patches, duplicate torso copies, dark neck notches, wave jacket/hip copy seam, or isolated matte/hair specks.

## Approval and scope

- User approval: approved after review of the corrected finger-wag and wave PNGs (“Good work”).
- Phase 4 runtime integration, motion proof, and UDP live-control verification have not started; the user requested this handoff before runtime work resumes.
- These are registered 2D alternate drawings, not volumetric models or runtime-verified animation yet.

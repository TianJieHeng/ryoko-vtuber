# Phase 3 — Registered Body Gestures

## Completed

- Registered and cleaned three canonical upper-body alternates on the approved 1024 × 1536 reference space and 2048 × 3072 master canvas:
  - `BOD-002` — scolding / finger-wag.
  - `BOD-001` — stern crossed arms.
  - `BOD-011` — greeting wave.
- Preserved the approved canonical head, face, hair, and accessories. Rear hair remains behind the torso; face and front-head layers composite once above each gesture.
- Added a narrow canonical neck bridge without stretching the face or blouse.
- Added one continuous canonical lower-body derivative for all gestures, excluding neutral hands and preventing flat leg-top seams.
- Restored pale hand interiors with source-space chroma guards and retained complete fingers and true background gaps.
- Removed alternate-head remnants after torso registration, residual matte, duplicate neutral parts, rectangular hip fragments, and detached components.
- Preserved original collar, blouse, shoulders, cuffs, pocket details, and garment artwork.

## Tested

`python3 tools/validate_gestures.py` reports `status: passed` for:

- Three registered gestures and their BOD action mappings.
- Required neutral-layer hide list.
- Shared neck bridge and continuous lower body.
- One significant connected component per gesture derivative.
- Pixel-identical canonical central face across all three gestures.
- Pixel-identical continuous legs across all three gestures.
- PNG dimensions matching gesture metadata.

Full-size and close-up visual reviews covered the face, neck, shoulders, collar, raised and lowered hands, crossed arms, jacket-to-hip joins, trousers, ankles, and heels against a dark background.

## Approval and scope

- User approval: pending PNG review.
- Phase 4 runtime integration, motion proof, and UDP live-control verification have not started.
- These are registered 2D alternate drawings, not volumetric models or runtime-verified animation yet.

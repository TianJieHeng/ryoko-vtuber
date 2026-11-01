# Corrective asset build journal

## 2026-11-01 — recovery and additive scope

- User requested missing separated character artwork in a new folder.
- Established `avatar_build_assets/` as the only new publication scope.
- Inspected current builder Phase 03/04 notes and preserved its existing 3D direction.
- Recovered two original reference sheets, four canonical masters and four detail sheets; copied original bytes into `references/`.
- New image generation and alpha/assembly validation are in progress. No completed 3D model, UV-fitted maps or runtime validation is claimed.

## First generated artwork checkpoint

- Accepted `hair/front_fringe.png`: isolated sage hair fringe with real RGBA transparency, reviewed against the canonical face and a neutral-grey composite.
- This is a source layer for projection, cards or manual fitting, not a registered head assembly or mesh-fitted UV map.
- Remaining hair, facial, outfit, accessory and effect production is still underway.

## Second artwork checkpoint

- Added front/back blouse torso components and their accepted transparent source atlas.
- Added two hair sticks and two dangling hair ornaments, with their accepted source atlases and generation prompts.
- Components were visually checked on flat backgrounds by their generating workers. They remain placement/mapping source art; no registered full-body stack or fitted 3D texture claim is made.

## Facial components and accessories checkpoint

- Added 23 accepted individual head PNGs: face base, ears, sclera, irises/pupils, lash/lid shapes, brows, closed lids, oral interior pieces, neutral lips and five vowel-mouth alternatives.
- Added earrings, necklace/green pendant and belt/buckle source artwork. Source atlases and exact crop/alpha provenance accompany the accepted layers.
- Generating workers inspected actual images composited on flat backgrounds. Original alpha and crop pixels are preserved.
- These are separate source components, not a guaranteed pixel-registered head or UV-mapped facial rig. Vowel mouths are mutually exclusive alternatives; do not stack them simultaneously.

## Hair and clothing expansion

- Accepted six total hair components: frontal fringe, rear-view scalp/nape, bun, short tail and two side locks, with source/crop provenance.
- Added accepted blazer, sleeve and trouser source components; native scale differs between independent sources and requires fitting.
- A separate neck-paint generation was blocked by the image tool safety filter and produced no output; no neck layer is claimed. The current 3D head/neck material is preserved.

## Self-contained reference library

- Included the entire original completed source-pack tree under `reference_library/`: 3,408 byte-identical file blobs, with internal paths and relative links preserved.
- This reuses existing Git objects, avoiding binary reupload and retaining all 200 expression and 40 body-reference sheets. It does not duplicate or modify the later `vtuber/` implementation.

## Final corrective source-art checkpoint

- Accepted 69 individual component/effect PNGs: head 23, body 23, hair 6, accessories 10, effects 7.
- Included 19 accepted generation sources/atlases, 10 key reference copies and five independently reviewed contact sheets.
- Independent QA verified all 69 component files decode with real alpha, hashes remain unchanged and meaningful content is clear of canvas edges. Head/hair crop evidence accompanies the report.
- Combined necklace and separate chain/pendant are alternatives, not three items to render simultaneously.
- Actual per-model UV fitting, full registered assembly, rig/export and runtime testing remain with the existing Blender build. The missing separate neck-paint output is explicitly recorded.
- No paid API call, CI run or modification of existing source/model files was performed in this pass.

## Final publisher integrity check

- Verified 98 accepted/reference image records against their SHA256 values, with 61 declared component crops checked pixel-for-pixel against preserved source PNGs. No errors.
- Normalized head crop-source links to repository-local paths by source hash, retaining original generation basenames for provenance.
- Rechecked revised diagnostic contact-sheet labels; previews do not claim assembled or rigged results.

# Upper-iris repair proposal: unapproved source backup

Review-only part repair for the shared Ryoko rig. User approval is pending. This backup does not integrate the repair, add an expression, or qualify production eye opening. The twenty approved expressions and their assets remain unchanged.

## Base and files

Base commit: `8e7cc9a0335c4e47b71c013bbe5e24b24f32f0e9`.
Approved `ryoko_object_rig` Git tree: `e01bda668f821c1bd57210f4eabfa5975859daa7`.
Originals: `ryoko_object_rig/rig_assets/gaze_eyes/iris_screen_left.png` and `iris_screen_right.png` at that commit. Screen directions are viewer-relative.

This folder contains two frozen full RGBA proposals and their exact binary authoring masks. Left is 147×92 pixels; right is 136×90. To recover a separate transparent cap exactly at the pixel level, copy the proposal RGBA where the matching mask is nonzero and set all other RGBA values to zero. The separate caps are therefore omitted as redundant.

SHA-256 identities:

- Original left: `86f2b2481173577fa947cdaad842d9fc0ddc0cd29cfaee1eba3a56b53dde7e14`
- Original right: `e6bdd07fd8c3867a785aee205f233c583a572df00abccbdcaba266c40f5d0450`
- `proposal_iris_screen_left.png`: `74f3ff38e8edd8c88f04bc446e316d8ecfd7da7bc618f1ff0f5c6da729d65b6d`
- `proposal_iris_screen_right.png`: `4fe24f2f2f26aa846c4f906a71c044561ece963ea6c587bae109fbb148d8a390`
- `authored_cap_mask_screen_left.png`: `3b06a9107a1d463d6b6a4e5a219f0faa5da5955b09ad81d4f0d6d68b3617b57b`
- `authored_cap_mask_screen_right.png`: `3c53086fb19463ee8ad6a269895331c3d26975fbd66bebdc7d4a2ce95bd4670c`

## Provenance and preservation

One image-generation edit authored a paired hidden upper-iris/pupil continuation. This is new art, not recovered original detail. The generated pair was resized from 1254×1254 to 128×128 with Pillow LANCZOS, registered to the source crops, and copied into the masks with the existing Python layer-assembly pipeline. There was no procedural pigment painting or color adjustment. The frozen proposals are the authoritative authored output; regenerating the image model is not required.

The guarded masks select inherited hidden-estimate cells with existing iris alpha, above the first nonzero neutral-aperture cell in each column, excluding a one-pixel dilation of the neutral aperture placed at iris padding (12,16). Final mask coverage is 1,097 left and 886 right pixels, with zero observed-pixel overlap. Of these, 1,096 left and 880 right pixels actually changed. All RGBA values outside the masks, and all original alpha values everywhere, are unchanged. Inherited content outside the masks retains its original provenance, including any inferred detail; it is not newly authored or newly verified here.

The completed native review capture found original and proposal centered-neutral eyes and bust exactly pixel-identical. The unchanged fixed 4px-opening fixture differed by 176 eye-frame pixels and 55 bust pixels. These are recorded review results; this preservation commit adds no new renderer run, control, profile, shader, geometry, or runtime change.

## Limits

Upper texture and pupil continuity improve, but a thin transition and some inherited right highlight streak remain. The fixed opening exposes only a small cap strip. Larger openings, general gaze/blink behavior and production quality remain unqualified. Review media, raw generated canvases, logs and duplicate cap PNGs are intentionally omitted from this minimal backup. Approval is still required before integration.

# Independent source-art review

Reviewed 2026-11-01. This is image-input QA, not Blender model, UV, rig or runtime certification.

## Verified

- 23 head parts: inspected actual alpha composites on neutral gray; recorded SHA256 values match. All 22 derived crops are pixel-exact against preserved source images. The face base is a separate whole-image output.
- 6 hair parts: hashes match; all four derived crops are pixel-exact. The rear scalp/nape is a rear-view source, not a frontal face overlay. The longer temple lock belongs to character-right (viewer-left in a front view).
- 23 body parts: visually reviewed garment pieces, front/back trousers, four hand views and four pump views. These are individual source pieces with independent framing, not a pre-registered complete body.
- 10 accessories (including a separate chain and pendant alternative to the combined necklace): viewed on neutral gray; the two sticks, two dangling ornaments, paired earrings, necklace/pendant and belt are separately addressable.
- All inspected component PNGs decoded and had real alpha. At inspection, no pixel with alpha greater than 64 touched the canvas boundary. Very faint antialias pixels may remain near borders.
- Source PNGs were not resized or repainted for this review. Diagnostic previews use independent alpha-bounds cropping and resampled thumbnails only; their filenames and native sizes are shown.

The mouth-cavity crop's parent image is preserved under `head/sources/audit_only/`. That parent atlas was rejected as a whole. Only the plain cavity crop is accepted; the hash and exact crop were independently checked after this provenance correction.

Machine-readable head/hair checks: `../metadata/independent_head_hair_crop_checks.json`.

## Consumer boundaries and known omission

A separate neck-art patch is not included. Keep the existing head/neck mesh material and fit the supplied face artwork deliberately. Do not fill a gap by distorting the head or blouse.

No full-body registered image assembly was performed. No actual model UV islands were available to this review, and no image is certified as a fitted UV atlas. Existing 3D geometry and the builder's work must remain intact. Illustrated shading/highlights should be reconciled with toon/runtime materials rather than blindly double-lit. Native sizes vary; no 2K/4K delivery is implied.

The 200 existing expression references are not 200 separate segmented character kits. New viseme images are artwork alternatives, not verified speech timing or shape-key deformation.

## Frozen optional effects and final preview check

The seven optional effects (paired blush, paired tears, sweatdrop, anger mark and sparkle cluster) were independently inspected after production froze. All composite cleanly on neutral gray and have real transparency. They must remain optional overlays disabled in neutral. The separate necklace chain and pendant are an alternative to the combined necklace, not extra jewelry to stack on top of it.

Final checks cover **69 individual components**: 23 head, 23 body, six hair, ten accessory and seven effect images. All decode as RGBA, all preview-source hashes remain unchanged, and none has an alpha-greater-than-64 pixel touching a canvas edge. The five labeled diagnostic sheets in `../previews/` include accepted parts only; no rejected source atlas is shown. See `../metadata/independent_component_alpha_checks.json` for per-file evidence.

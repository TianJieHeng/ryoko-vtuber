# EXP-006 separate blush FX: registration and provenance

These are two separately registered original assembly-pack effects. Source identity is retained; their registration and cheek masks are newly authored, not recovered rig anchors. Approval of another expression does not approve EXP-006.

## Original Git sources

Repository: `TianJieHeng/ryoko-vtuber`. Paths and hashes below come from the assembly-pack asset manifest, whose path base is `avatar_build_assets/`.

**Anatomical character right, displayed screen-left:**
- Git path: `avatar_build_assets/effects/layers/RYO_FX_blush_character_R.png`
- SHA-256: `a818395e9cf1be5023edc62f2d79b24bb3ee19efe634e35639b2770d53536081`
- Git blob SHA: `1cdef2537798e4681b776df470dd3f7845aff5ec`
- Original atlas crop: `[0, 0, 1086, 724]`.

**Anatomical character left, displayed screen-right:**
- Git path: `avatar_build_assets/effects/layers/RYO_FX_blush_character_L.png`
- SHA-256: `12efc27caceed6475110b7e17bee91044dda15da21f9a453923abda25a64a824`
- Git blob SHA: `c8a355febf73403fc64ba3656022c7e76be70115`
- Original atlas crop: `[1086, 0, 2172, 724]`.

Source atlas: `avatar_build_assets/effects/sources/RYO_FX_blush_source_v001.png`, SHA-256 `9cdfb66936a8f83f18c839ba1e1560f3f1a35462a8013325b3a835c2a62ecb21`. Both separated 1086×724 originals are retained byte-for-byte in `source_originals/`.

## Fixed registration

The builder clears source pixels with alpha below 4 to remove faint canvas-wide specks, crops R to `[114,196,789,581]` and L to `[301,196,982,584]`, and resamples each crop to 148×84 with premultiplied-alpha Lanczos. It does not mirror or deliberately recolor either source.

- Screen-left: `blush_screen_left.png`, top-left `[407,519]`, center pivot `[481,561]`.
- Screen-right: `blush_screen_right.png`, top-left `[577,519]`, center pivot `[651,561]`.
- Both use `centered = false`, z29, fixed rotation and unit local scale. Only intensity changes at runtime; the recommended EXP-006 peak is 0.55.

Conservative cheek polygons are clipped away from existing foreground-owned pixels and feathered inward by 12 pixels. This avoids the skin-colored patches carried by foreground hair without modifying or painting through the hair. Disconnected alpha islands are removed. The supplied masks are already baked into runtime PNG alpha and must not be applied again.

## Reference fit and limitations

Exact reference sheet SHA-256: `59a58716099bdd126e7ab4a106fdfb5ae9b75471e4d4bdd0b978997428e1a848`. KP04 has lighter visible hatching; KP05 has the strongest. KP06 has much less wash and no clear individual hatch lines. KP01–03 and KP07–09 have no clear hatching. These are visual observations from a static sheet, not recovered animation timings.

The original effects have **three long diagonal strokes per cheek and a pinker wash**. The reference has **many finer hatch lines and a peachier wash**. These differences remain: no matching hatching was invented and no color correction was painted into the sources. Position and mask registration are inferred. Visual confinement was assessed with the zero hair sway used by EXP-006; other performances need separate review.

## Reproduction and checks

When installed at `rig_assets/blush_support/`, run `python build_registered_blush.py`; its default rig root is `HERE.parents[1]`. For other layouts, pass `--rig-root /path/to/ryoko_object_rig`. The builder checks both original hashes and the exact existing foreground-file hashes and positions recorded in `manifest.json` before reconstructing the masks.

Required source package: the two originals, two runtime textures, two cheek masks, manifest and builder. Unmasked registered textures and `authoring_foreground_alpha.png` are optional reproducible diagnostics, not required inputs.

Repeated builds are byte-identical. Source-registration checks confirm one connected alpha region per cheek and no eye, nose, mouth or neck coverage. Seven static CPU composites preserve all protected pixels and return exactly to baseline at zero intensity. Actual Godot rendering, lifecycle and performance validation are separate integration tests, not claims made by this source-registration package.

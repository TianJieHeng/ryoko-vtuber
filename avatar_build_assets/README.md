# Ryoko avatar build assets

**Status: corrective image-asset production in progress.** This new folder is additive. The existing reference collection and the builder's `vtuber/` project are unchanged.

## Start here

1. Inspect `references/`: two original character sheets, four canonical generated masters and four detail sheets are copied byte-for-byte for identity, costume, pose and palette context.
2. Read `metadata/asset_manifest.json` for the exact files present, hashes, dimensions, transparency and acceptance status. An image is not delivered merely because it appears in a proposed plan.
3. Read `docs/KIMI_INTEGRATION.md` before importing new imagery into the existing 3D build.
4. Read `BUILD_JOURNAL.md` for actual completed checkpoints and remaining work.

## Design authority

Adult human Ryoko: mint/sage hair, amber eyes, dark trouser suit, white blouse, gold hair ornaments/earrings, green pendant and black pumps. Match the supplied human design; do not substitute the unrelated masked character. Character-left/right refer to anatomy, not the viewer.

## Image types and limitations

The corrective pass creates separated artwork and transparent components. Each record identifies whether it is an individual layer, a source sheet requiring extraction, an optional effect, or an assembly preview. A composite preview must be created from the actual layers before claiming that those layers form a registered cutout assembly.

These images do not replace the builder's existing 3D mesh, UVs, facial geometry, rig or project. They are not automatically fitted to its UV islands. Existing 200 expression sheets remain performance references, not 200 complete segmented animated models. Native dimensions and transparency must be verified per file; no upscaled image is described as native 2K/4K.

This folder is still being populated. Do not infer a finished avatar, complete layer stack, tested rig, exported VRM or runtime approval from the presence of this README.

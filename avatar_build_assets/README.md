# 2D assembly inputs

Use the individual artwork in `head/layers/`, `body/layers/`, `hair/`, `accessories/layers/` and `effects/layers/`. The `sources/` directories contain useful sheets for recutting. `metadata/asset_manifest.json` lists the 69 parts and 18 source atlases; paths there are relative to this folder.

[Assembly instructions](docs/ASSEMBLY_2D.md) describe the required cut, align, assemble and rig sequence. No completed layered puppet or working rig is supplied yet.

## Reference library
- `reference_library/references/originals/`: six original character sheets.
- `reference_library/assets/modeling/`: canonical neutral face and body views, used as drawing references only.
- `reference_library/assets/details/`: hairstyle, outfit, hands/shoes and accessory design references.
- `reference_library/assets/expressions/`: 200 expression sheets, panels and peak images.
- `reference_library/assets/body/`: 40 body-gesture sheets and panels.
- `reference_library/assets/controls/`: facial movement reference studies and panels.
- `reference_library/metadata/`: expression, gesture, control, source-image and crop catalogues. Their `assets/...` paths resolve from `reference_library/`, not repository root.

`previews/` contains diagnostic contact sheets, not assembled-model previews. Different views and mouth/necklace alternatives must not all be enabled at once. The original file names containing “modeling” are retained for stable catalogue paths; they are images, not an instruction to build a 3D model.

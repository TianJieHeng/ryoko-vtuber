# Hair source artwork generation

Generated with the built-in image tool from the copied canonical references. The front neutral master governs identity; the back master and hair construction sheet supply rear and attachment forms.

## Accepted parts
- `front_fringe.png`: isolated frontal sage/mint hair without head, skin, face or jewelry. Requested completed hidden roots. Final tool pass requested cleaning edge contamination; gray compositing confirms clean alpha. This includes the broad swept front section; separate temple locks allow controlled asymmetric detail.
- `rear_scalp_nape.png`: rear-view scalp and nape source from the back canonical reference. It is not meant to be stacked in front of the face.
- `bun.png` and `short_tail.png`: complete detached looped bun and short loose tail. Exact left/right half crops of `sources/bun_tail_atlas.png` (1774×887).
- `temple_lock_character_right.png`: longer lock shown viewer-left.
- `temple_lock_character_left.png`: shorter tucked lock shown viewer-right. Both are exact half crops of `sources/side_locks_atlas.png` (1536×1024).

The original image tool outputs are preserved for atlases. There was no resizing or repainting during extraction. Source shading is illustrative; do not bake it blindly over physically shaded materials. Use a toon shader and inspect highlight consistency on the actual mesh.

## Suggested component arrangement
For the existing 3D hair: fit/project the scalp artwork on the scalp surface, the fringe onto matching front sections, and the updo/tail onto their corresponding meshes. Fit temple locks independently. Roots overlap adjacent surfaces so no transparent gap appears during movement. Preserve exactly two gold hairsticks from the accessory folder.

For optional image-card use only: rear scalp behind face, bun behind/above scalp, tail behind side hair, fringe in front of forehead, asymmetric temple locks in front of temples, ornaments above hair. The separate sources have independent framing and require placement and scaling; no automatic registered stack or Blender rig is claimed.

## Excluded attempts
An extra full-body master and an over-combined scalp attempt were not used in this pack. They do not replace the established canonical design.

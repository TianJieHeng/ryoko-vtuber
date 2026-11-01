# Credits and source use

## Phase 02 blockout

- **Tripo API** generated the untextured full-body Ryoko blockout from the repository's approved front, left-side, and back reference images. Generation model: `v3.1`; upstream task: `d8fd4168-12f1-4175-810d-02e05ceace79`.
- Blender 5.2.1 LTS was used for import, provisional scale/orientation normalization, neutral-clay presentation, lighting, rendering, and structural read-back validation.
- Character reference art comes from `TianJieHeng/ryoko-vtuber`; repository originals were not edited.
- No third-party mesh, texture, rig, or animation library asset was added in Phase 02.

## Phase 03 modular surface and fitted textures

- **Tripo API** processed the original full-body blockout with smart retopology: `decimate --model v2.0 --face-limit 20000`; returned task `ae55137b-d423-4c9a-87ab-cb729cf33c2c`. The result was evaluated and rejected as production-ready deformation topology.
- **Tripo API** semantically segmented the blockout with `segment --model v2.0 --granularity balanced`; returned task `370e5e56-a084-4f07-a529-acae63195812`. The ten returned parts were used only as nearest-surface labels for modular separation of the approved v002 surface, not as replacement body geometry.
- Blender 5.2.1 LTS was used for retained-surface separation, narrow-loop repair, local subdivision density, UV projection, material-region correction, fitted base-color/roughness baking, texture packing, rendering, and saved-source read-back validation.
- Character reference art remains unchanged and belongs to the original `TianJieHeng/ryoko-vtuber` source pack. No third-party texture, rig, animation, or material library asset was added in Phase 03.

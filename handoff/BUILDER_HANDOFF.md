# Ryoko Full Character Builder Handoff

## Purpose and current status

Build the supplied human Ryoko as a full-character 3D avatar for wall projection, with expressive facial acting and readable full-body gestures, including scolding. This pack provides visual references and performance intent. It is not a Blender model or a playable animation library.

The accepted and delivered source-art set contains **273 primary images**: 200 expression sheets, 40 full-body gesture sheets, 22 generic facial-control references, seven modeling references and four detail references. Local final QA passed with no recorded integrity errors. It also includes **2,352 losslessly cropped panels and 200 peak copies**, counted separately from primary sources; the six original user reference PNGs are unchanged. Read [asset_index.json](../metadata/asset_index.json), [integrity_validation.json](../metadata/integrity_validation.json) and [publication_status.json](../metadata/publication_status.json) for exact inventories and remote verification. Model, rig and runtime implementation remain future work.

## Read the pack in this order

1. [Reference review](../references/REFERENCE_REVIEW.md) and [originals](../references/originals/) establish the supplied design and its inconsistencies.
2. The [neutral facial master](../assets/modeling/RYO_MOD_neutral-bust_front_v001.png), [full-body front](../assets/modeling/RYO_MOD_fullbody_front_v001.png), [side](../assets/modeling/RYO_MOD_fullbody_side_v001.png), [back](../assets/modeling/RYO_MOD_fullbody_back_v001.png) and [A-pose](../assets/modeling/RYO_MOD_fullbody_Apose_front_v001.png) guide the build.
3. [Eye](../assets/modeling/RYO_MOD_eye-details_v001.png), [mouth](../assets/modeling/RYO_MOD_mouth-details_v001.png), [hair](../assets/details/RYO_DET-001_hair-construction_v002.png), [accessory](../assets/details/RYO_DET-002_gold-accessories_v003.png), [outfit](../assets/details/RYO_DET-003_outfit-construction_v003.png) and [hands and pumps](../assets/details/RYO_DET-004_hands-pumps_v002.png) sheets supplement those masters.
4. Use [controls_inventory.json](../metadata/controls_inventory.json), [expressions.json](../metadata/expressions.json) and [body_gestures.json](../metadata/body_gestures.json) to resolve accepted asset paths and intended behavior. Do not infer filenames from a stale version suffix.
5. Read [QA limits](../metadata/QA_LIMITATIONS.md) and [what is not included](NOT_INCLUDED.md) before estimating implementation completeness.

Follow the neutral face and front/back body masters for identity and costume when a secondary detail contradicts them. Preserve mint/sage hair, amber eyes, dark trouser suit, white blouse, gold ornaments and heels. Do not import an unrelated masked Ryoko design. The illustrations are not measured orthographic geometry; resolve perspective, proportions and hidden surfaces explicitly during modeling.

## How to consume the performance files

Each expression has a stable EXP ID, facial intent, source-image path, proposed key-pose timing, procedural interaction notes and suggested reusable body references. Prefer `asset_production.actual_path` and actual extracted-path fields over `planned_assets`. QA has already linked the body suggestions; preserve those catalogue records rather than overwriting them with an assumed one-to-one animation mapping.

Most expression and body sheets read left to right, top to bottom through nine key poses. Timing is an acting proposal, not measured playback. A body pairing supplies separately authored visual references, not a bespoke synchronized face/body clip. Build independent facial presets and body actions, then combine them deliberately.

The user authorized lossless panel extraction. [frame_extraction.json](../metadata/frame_extraction.json) records exact source hashes, crop bounds, panel paths and pixel equality. The crops preserve source pixels and may retain grid borders or annotations. They are **not registered, aligned, interpolated or seamless animation frames**. Do not play the PNG sequence and call it a tested 3D animation. Do not assume every sheet is a time sequence: jawRight is a three-panel comparison; vowelChart is a mouth-shape comparison; eye/mouth detail sheets are construction studies.

EXP-094 is now **about-to-sneeze**, replacing the original food-reaction concept. Follow its current catalogue path and intent; [replacement provenance](../metadata/generation-issues/EXP-094.json) preserves that change. Do not recreate or relabel the old concept as delivered.

## Practical Blender build sequence

### 1 Establish the actual target

Confirm runtime application, export format/version, facial tracking or scripted playback, audio/lip-sync method and target hardware. Full-character wall projection is confirmed; the software route is not. Choose framing and display background for the wall rather than assuming the cream drawing background belongs in the final avatar.

### 2 Construct the character

Block the whole figure against the masters and check face/body proportions from several views. Model the hair arrangement, jewelry, jacket, trousers, blouse and shoes as sensible separate parts. Resolve the rear hair volume and accessory attachments on the actual geometry. Keep source drawings unchanged and record any necessary design decisions.

Retopologize for eyelid, mouth, jaw, shoulder, elbow, hip and finger deformation. Build the mouth interior and other unseen structures as geometry, not as facts supposedly supplied by a painted close-up. Create and check the UV unwrap **before** authoring fitted texture atlases. Then develop runtime-appropriate materials without baking illustrative lighting, panel borders or comic effects into base color.

### 3 Prove the facial and skeletal foundations

Build the body skeleton and weights, then prototype neutral, full blink, gaze, jaw opening, a smile and initial lip-sync shapes. Render comparisons against the reference before expanding the rig. Check eyelid closure over the eye, lip sealing, teeth/tongue intersections, silhouette preservation and combined deformations. Resolve asymmetric controls using character-left/right, not viewer-left/right.

There are 22 generic control references, not a certified 52-shape ARKit pack. `jawLeft` and `lowerLipDepress` were not delivered because attempts failed to isolate the intended motion reliably. Design and test any needed missing controls on the mesh; do not mirror a picture or reuse an incorrect reference and claim validation.

### 4 Build reusable controls and performances

Use reusable facial controls to author the 200 emotional presets/performances. Do not require 200 unrelated base meshes or copy every image's incidental anatomical variation. Create the 40 body actions as separate clips, then stage catalogue pairings. For finger wags, crossed arms and stern stances, check finger articulation, hand contacts, jacket penetration, balance and the full head-to-heels silhouette.

Treat tears, blush, sweat marks, sparkle eyes, motion lines and similar illustrated effects as separate implementation decisions: material changes, overlays, geometry or scene effects as appropriate. The drawings do not provide ready UV overlays or runtime effect assets. Keep chibi cutaways and page captions out of avatar textures.

Test expression conflicts with live blink, gaze and lip sync. Decide where to blend or override those channels; do not add two incompatible mouth openings or eyelid closures blindly. Author easing, holds, interrupted-action recovery and neutral returns in Blender. Test loops on the actual curves rather than assuming nine reference poses create a seamless cycle.

### 5 Validate the finished avatar

Test the chosen exported model in the actual application. Verify orientation, scale, names, materials, control mappings, head/body motion, hair/accessory motion and performance. Inspect wall-projection framing at the intended distance: whole figure visible, hands readable, scolding pose legible and face still expressive. Check idle, extreme poses, interruption, repeated actions and return to neutral.

The eventual implementation delivery should include the editable Blender project, necessary textures, tested export, version/dependency notes and recorded test evidence. None of those runtime deliverables is implied by accepting this source-art pack.

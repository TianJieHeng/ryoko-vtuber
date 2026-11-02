# Ryoko 2D VTuber — Build Handoff

**Handoff date:** 2026-11-03  
**Repository:** `https://github.com/TianJieHeng/ryoko-vtuber`  
**Required checkpoint branch:** remote `main`  
**Remote state immediately before this handoff:** `43edc9e8bea376e0e8df7614d1b00d00aa9e0416`  
**Current production directory:** `/mnt/agents/output/ryoko_2d/`  
**Recovered source checkout:** `/mnt/agents/output/ryoko-vtuber/`

## 1. Executive status

Ryoko is being built as a **full-body 2D cutout VTuber**, using the canonical repository artwork. This is not a 3D modeling task.

Current phase status:

| Phase | Status | Meaning |
|---|---|---|
| Source recovery and artwork preparation | Complete | Canonical source library restored; originals preserved; derivatives written separately. |
| Phase 2 — neutral full-body assembly | Complete and approved | Layered neutral character, explicit neck artwork, transparent side/arm gaps, individual PNGs, placement metadata, and light/dark previews. |
| Phase 3 — registered body gestures | Complete and approved | Finger-wag, crossed arms, and wave corrected and reviewed. Remote checkpoints pushed. |
| Phase 4 — Godot runtime, motion proof, and live control | **Not started in the rebuilt project** | A recovered controller exists, but the current project is not yet a runnable or verified Godot rig. |
| Phase 5 — final package and documentation | Not started | Final editable package, runtime instructions, mappings, motion previews, and completed build journal remain. |

The latest user feedback, “Good work,” accepted the corrected finger-wag and wave PNGs. The user then requested this handoff. **Do not interpret the handoff as permission to skip the remaining runtime and delivery work.**

## 2. Non-negotiable production constraints

1. **2D assembly and rigging only.** Cut, register, layer, and rig the supplied artwork.
2. Do not sculpt or reconstruct a volumetric character.
3. No retopology, UV baking, VRM pipeline, or other 3D-character workflow.
4. Preserve source originals. Write cleaned and registered artwork as separate derivatives.
5. Do not switch to paid tools without approval.
6. No CI or paid services/API calls without approval.
7. Do not revive the obsolete 3D directions or repeat an unverified approach for hours.
8. Show PNG previews between phases and obtain approval before advancing.
9. **User-facing approval previews must be PNGs only.** Do not ask the user to open ORA, Godot, or another specialized application for approval.
10. **Push to remote `main` between phases and verify the remote commit.** A local commit alone is not a checkpoint.
11. Continue to distinguish completed, tested, approved, blocked, and unstarted work. Do not present a rendered video as proof of live tracking or live control.
12. Character-left is viewer-right. Keep this convention consistent in artwork, metadata, controls, and documentation.

## 3. Canonical character target

The assembled character must remain the canonical adult human Ryoko from the repository, not a generic replacement:

- Sage/mint hair with the canonical bun and straight hair sticks.
- Amber eyes.
- Adult facial proportions and the approved canonical face.
- Black trouser suit.
- White blouse.
- Gold ornaments and jewelry.
- Green pendant.
- Black heels.
- Full head-to-heels silhouette on one coherent canvas.

The approved neutral face and upper-head artwork must not be redrawn, stretched, or replaced to conceal registration problems.

## 4. Source material and reference library

Primary source root:

`/mnt/agents/output/ryoko-vtuber/avatar_build_assets/`

The build script also supports a repository layout where `ryoko_2d/` and `avatar_build_assets/` are siblings.

Important source files:

- Neutral/full-body target:  
  `reference_library/assets/modeling/RYO_MOD_fullbody_front_v001.png`
- Finger-wag:  
  `reference_library/assets/body/RYO_BOD-002_finger-wag_kp03_v001.png`
- Crossed arms:  
  `reference_library/assets/body/RYO_BOD-001_arms-crossed-stern_kp05_v001.png`
- Wave:  
  `reference_library/assets/body/RYO_BOD-011_greeting-wave_kp04_v001.png`
- Expression metadata:  
  `reference_library/metadata/expressions.json`
- Body-gesture metadata:  
  `reference_library/metadata/body_gestures.json`
- Controls inventory:  
  `reference_library/metadata/controls_inventory.json`
- Assembly guidance:  
  `docs/ASSEMBLY_2D.md`
- Asset manifest:  
  `metadata/asset_manifest.json`

The reference library contains 200 expression sheets and 40 body-gesture references. They are acting guides for the same rig; they are not yet 200 tested runtime expressions or 40 tested runtime body swaps.

## 5. Canvas, registration, and layering conventions

- Canonical reference canvas: **1024 × 1536**.
- Master working canvas: **2048 × 3072**.
- Master scale factor: **2×** reference coordinates.
- Character-left is viewer-right.
- Use one frontal master pose and registered coordinates for all swaps.
- Source PNGs are not assumed to be pre-registered.
- Gesture drawings use source-matched registration and tapered torso alignment, not independent unregistered panel crops.
- Placement and pivot values are stored in master coordinates, with reference pivots where applicable.

## 6. Phase 2 — approved neutral assembly

### Delivered artwork

- Editable OpenRaster document:  
  `artwork/Ryoko_Neutral_Layered.ora`
- Individual transparent PNGs:  
  `artwork/layers/`
- Registered transparent PNGs:  
  `artwork/registered/`
- Background-removed canonical derivative:  
  `artwork/derivatives/canonical_fullbody_background_removed.png`
- Placement, layer, and pivot metadata:  
  `manifest/placement_manifest.json`
- Neutral validation:  
  `manifest/neutral_validation.json`

### Layer structure

The neutral build contains **54 genuine layers**, with **40 enabled in neutral**. It includes separate artwork for:

- Rear and front hair, bun, temple pieces, tail, and hair accessories.
- Face, ears, sclera, irises, lashes, eyelids, and brows.
- Neutral mouth and A/E/I/O/U mouth alternates.
- Neck, torso, arms, hands, pelvis, legs, and shoes.
- Jewelry, green pendant, and belt buckle.
- Blush, tears, sweat, anger, and sparkles as independent optional effects.

Blush, tears, sweat, anger, and sparkles are off in neutral. Mouth states are exclusive. Blink artwork is independent of gaze and mouth selection.

### Explicit neck resolution

A separate canonical neck layer was created and registered. The face and blouse were not stretched to hide missing neck artwork. A narrow neck bridge was also derived for gesture use while retaining each gesture’s original collar and blouse.

### Background cleanup

The neutral cleanup removes border-connected neutral sheet background. Two enclosed white arm-to-torso wedges required explicit seeded removal at reference coordinates `(397,500)` and `(615,500)`. These were background wedges, not blouse or cuff artwork.

Neutral previews:

- `previews/ryoko_neutral_transparent.png`
- `previews/ryoko_neutral_light.png`
- `previews/ryoko_neutral_dark.png`

### Neutral validation result

`manifest/neutral_validation.json` records:

- `layers_total`: 54
- `layers_enabled_neutral`: 40
- `canonical_foreground_pixels`: 1,271,279
- `missing_foreground_pixels`: 0
- `extra_foreground_pixels`: 0
- `mean_abs_rgb_difference_shared_pixels`: 0.0

The neutral phase received user approval before gesture work began.

## 7. Phase 3 — approved registered gestures

### Authoritative final derivatives

Use these files:

- `artwork/gestures/gesture_finger_wag_registered.png`
- `artwork/gestures/gesture_crossed_arms_registered.png`
- `artwork/gestures/gesture_wave_registered.png`
- `artwork/gestures/gesture_rear_hair.png`
- `artwork/gestures/gesture_neck_bridge.png`

Gesture metadata:

- `manifest/gesture_layers.json`
- `manifest/gesture_validation.json`

Final approval previews:

- `previews/gesture_finger_wag_dark.png`
- `previews/gesture_crossed_arms_dark.png`
- `previews/gesture_wave_dark.png`

### Final gesture architecture

Each gesture uses **one coherent, source-matched, registered full-body drawing**. Do not restore the rejected split upper/lower-body architecture.

The composite order is:

1. Hair-only gesture rear hair behind the body.
2. One registered full-body gesture drawing.
3. Narrow canonical neck bridge.
4. Approved canonical face and front-head layers once above the body.

This preserves each source drawing’s own jacket hem, pelvis, trousers, ankles, and heels. In particular, the wave jacket and hip remain aligned because there is no second lower-body copy.

The approved canonical face remains pixel-identical across gestures after accounting for the intentional wave-only head offset.

### Corrections completed during review

- Removed duplicate upper/lower body copies that caused neck, collar, shoulder, and hip seams.
- Removed non-hair neck, collar, jacket, and accessory contamination from gesture rear hair.
- Added a feathered fixed-head/body transition beginning at reference `y=235`.
- Preserved original collar, blouse, shoulders, cuffs, pocket details, hands, legs, and heels.
- Restored pale hand interiors with source-space chroma guards.
- Removed enclosed white thumb-gap sheet components in finger-wag and wave.
- Restricted final hand cleanup to small source-registered gap boxes so raised-hand finger edges were not eroded.
- Shifted the complete wave head/neck group **12 reference pixels right** (`24` master pixels). This includes canonical head layers, rear hair, and neck bridge. Other gestures have zero head offset.

### Gesture action mappings

| Runtime gesture | Source action |
|---|---|
| `gesture_finger_wag` | `BOD-002` |
| `gesture_crossed_arms` | `BOD-001` |
| `gesture_wave` | `BOD-011` |

### Obsolete local derivatives — do not use

The workspace still contains experimental files from rejected iterations. They are not referenced by current final metadata:

- `artwork/gestures/gesture_finger_wag.png`
- `artwork/gestures/gesture_crossed_arms.png`
- `artwork/gestures/gesture_wave.png`
- `artwork/gestures/gesture_lower_body.png`
- `artwork/gestures/gesture_*_lower_body.png`

Do not build Phase 4 from these files. Use only the `_registered.png` full-body files listed above.

## 8. Validation and reproducible build scripts

Scripts:

- `tools/assemble_neutral.py` — approved neutral build; do not modify casually.
- `tools/prepare_gestures.py` — reproducible final gesture derivatives, metadata, and previews.
- `tools/validate_gestures.py` — current gesture validation.

Run from `/mnt/agents/output/ryoko_2d/`:

```bash
python3 tools/validate_gestures.py
```

Only regenerate gesture artwork if necessary:

```bash
python3 tools/prepare_gestures.py
python3 tools/validate_gestures.py
```

Latest gesture validation is `status: passed` and checks:

- Three registered gestures and action mappings.
- Single registered full-body artwork for each gesture.
- Source-matched `_registered.png` paths and full-body dimensions.
- Required neutral-layer hide list.
- Shared neck bridge.
- One significant connected component per gesture body and neck bridge.
- Valid separated components for hair-only rear hair.
- Canonical face identity after applying each gesture’s declared head offset.
- Zero opaque neutral-white pixels in the registered finger-wag and wave hand-gap regions.
- PNG dimensions matching metadata.

Latest recorded foreground counts:

- Finger-wag body: 1,054,830 pixels.
- Crossed-arms body: 1,085,882 pixels.
- Wave body: 1,167,734 pixels.
- Gesture rear hair: 3,477 pixels.
- Neck bridge: 32,314 pixels.

These automated checks supplement, not replace, full-size visual inspection.

## 9. Remote checkpoint history

Important remote `main` commits:

| Commit | Purpose |
|---|---|
| `f013b50c53c2e70402ad31aacbd4043c097629bb` | Approved neutral rebuild and transparent side gaps. |
| `bf40c96083ef390de4aeb59dfd6a4fef843ce71f` | Earlier Phase 3 metadata/validation; superseded. |
| `d239744781c412450bba65abd8622e67bd029689` | Earlier gesture preparation; superseded overlap version. |
| `49436eb6244acd7d8e622a22b4514664815a58f0` | Single-body overlap correction records. |
| `dbcf8d47dda199603714b389504a4c202a3000c7` | Reproducible single-body gesture build. |
| `c00a1ff80701ae868ce93e31eb122b7f925ce2f9` | Wave-head alignment and hand-background correction records. |
| `43edc9e8bea376e0e8df7614d1b00d00aa9e0416` | Reproducible precise hand cleanup and wave alignment; pre-handoff head. |

Do not resume from the superseded overlap architecture in `bf40c96` or `d239744`.

The remote Phase 3 checkpoints contain the reproducible scripts, manifests, validation, and checkpoint documentation. Generated binary derivatives and approval previews are currently in the production workspace. Before final delivery, ensure the complete binary artwork set is included in the distributable package/repository; do not assume a text checkpoint alone contains the PNG or ORA files.

## 10. Runtime decision and current recovered controller

The user had no runtime preference. The selected target is:

- **Godot 4**
- Local, open-source 2D `Node2D`/`Sprite2D` cutout rig
- UDP JSON control on **port 9122**
- No paid tracking service required

Recovered controller:

`rig/rig_controller.gd`

It contains provisional logic for:

- Sprite/layer construction from manifests.
- Breathing and restrained sway.
- Head tilt and restrained turn scaling/translation.
- Independent blink and gaze.
- Brow controls.
- Exclusive mouth/viseme selection.
- Optional effects.
- Expression/action/gesture channels.
- UDP JSON commands.
- A timed proof sequence and capture hooks.

**This controller has not been integrated or verified against the rebuilt final artwork.** It is not evidence of a working live VTuber.

The current production tree does not yet contain a complete runnable Godot project. The recovered controller references assets that must be restored or recreated, including:

- `project.godot` and an entry scene.
- `shaders/iris_clip.gdshader`.
- `manifest/expression_map.json`.
- `manifest/body_action_map.json`.

The controller’s current `set_gesture()` still resets `gesture_head_offset` to zero and does not implement the final gesture rear-hair/body/front-head depth ordering. It must be updated rather than assumed correct.

## 11. Phase 4 — next implementation phase

Phase 4 has not started. Resume with these tasks:

### A. Restore a runnable Godot project

1. Create or restore `project.godot` and the main scene.
2. Restore the iris clipping shader and expression/action map files.
3. Import the approved neutral and final registered gesture artwork.
4. Confirm all `res://` paths resolve from `ryoko_2d/`.
5. Start from the approved neutral pose before adding motion.

### B. Update the controller for final Phase 3 artwork

1. Use `gesture_*_registered.png` full-body files only.
2. Use the current five-entry `gesture_layers.json` structure.
3. Apply the current `gesture_hide` list.
4. Add hair-only `gesture_rear_hair` behind the body.
5. Composite face/front-head layers once above the gesture body.
6. Read `registration.head_offset_ref`; wave is `[12,0]`, others `[0,0]`.
7. Apply the head offset to the complete head group and neck bridge, not just the face.
8. Do not reintroduce `gesture_lower_body` or split upper/lower gesture copies.
9. Keep the gesture body locked against accidental rotation that would detach it at the neck or pelvis.

### C. Complete independent rig channels

Implement and test:

- Breathing.
- Restrained body sway.
- Neck-pivot head tilt.
- Restrained head turns, using registered alternates where deformation is unsuitable.
- Independent left/right blink.
- Independent gaze with iris clipping.
- Brow raise/lower.
- Exclusive neutral/A/E/I/O/U mouth states and lip-sync override.
- Expression overrides compatible with blink, gaze, and lip-sync.
- Gesture/action selection.
- Hair motion and accessory motion.
- Optional blush, tears, sweat, anger, and sparkles, all off in neutral.

### D. Map the acting library

1. Build the 200-expression mapping from the expression metadata onto the same rig.
2. Build the 40 body-action mapping from the body-gesture metadata.
3. Clearly distinguish mapped presets from fully tested unique artwork.
4. Keep the approved readable finger-wag/scolding and crossed-arms actions.
5. Use registered alternate drawings for poses that cannot be deformed cleanly.

### E. Produce a motion proof

Prove in a short animation:

1. Neutral.
2. Blink.
3. Mouth movement/lip-sync.
4. Head tilt.
5. At least one arm gesture; include the approved finger-wag.
6. Return to neutral.

Inspect moving joints at full size for gaps, clipping, detached pieces, and incorrect depth order. Pay particular attention to the neck, collar, shoulders, raised hands, jacket/hip region, and gesture transitions.

### F. Verify actual live control

A rendered proof video is insufficient. Run the Godot project and send real local UDP JSON commands to port 9122. Verify visible state changes and logs for at least:

- Reset/neutral.
- Blink.
- Gaze.
- Head tilt.
- Mouth/viseme selection.
- Expression selection.
- Gesture/action selection.
- Optional effects on/off.

Record exactly what was tested, commands used, observed results, and any blocked controls.

### G. Phase 4 checkpoint and approval

1. Save validation results and motion/live-control evidence.
2. Push Phase 4 to remote `main` and verify the remote commit and files.
3. Present PNG previews for approval.
4. Do not begin final packaging until the user approves Phase 4.

## 12. Existing provisional UDP control vocabulary

The recovered controller already recognizes the following fields; preserve or deliberately document any changes:

```json
{
  "reset": true,
  "blink": 1.0,
  "blink_L": 1.0,
  "blink_R": 1.0,
  "gaze_x": 0.0,
  "gaze_y": 0.0,
  "head_tilt": 0.0,
  "head_turn": 0.0,
  "brow_raise": 0.0,
  "brow_lower": 0.0,
  "mouth": "A",
  "viseme": "A",
  "lip_sync": 0.0,
  "expression": "neutral",
  "action": "BOD-002",
  "gesture": "gesture_finger_wag",
  "effects": {
    "blush_L": false,
    "blush_R": false,
    "tear_L": false,
    "tear_R": false,
    "sweat": false,
    "anger": false,
    "sparkle": false
  },
  "background": "dark"
}
```

These are provisional controller capabilities, not a claim that live control has already passed.

## 13. Phase 5 — final delivery work

After Phase 4 approval:

1. Package the editable neutral ORA and all transparent individual PNGs.
2. Include final registered gesture derivatives and no obsolete duplicates in the clean delivery folder.
3. Include placement, layer, pivot, expression, action, and gesture metadata.
4. Include the complete Godot project, shader, controller, and local UDP setup.
5. Include neutral light/dark/transparent previews and final gesture previews.
6. Include the short motion proof and live-control test evidence.
7. Write setup instructions covering Godot version, project opening, running, keyboard controls, UDP port, example commands, and troubleshooting.
8. Complete a build journal separating completed, tested, approved, blocked, and unstarted items.
9. Remove or quarantine experimental derivatives from the clean package.
10. Push the final delivery to remote `main`, verify the commit and file contents, and present final PNG previews.

## 14. End goals / acceptance checklist

The project is finished only when all of the following are true:

- [ ] Canonical adult Ryoko is preserved with mint hair, amber eyes, black suit, white blouse, gold ornaments, green pendant, and black heels.
- [ ] The character is a coherent full-body 2D cutout, not a 3D reconstruction.
- [ ] Editable layered artwork and transparent individual PNGs are delivered.
- [ ] Placement, layer ordering, and pivots are documented.
- [ ] Neutral, blink, mouth movement, head tilt, and arm gestures work in the runtime.
- [ ] Breathing, sway, hair, accessories, brows, gaze, expressions, and effects work compatibly.
- [ ] Mouth/lip-sync states are exclusive and overrides do not break blink or gaze.
- [ ] Optional effects are off in neutral.
- [ ] Finger-wag/scolding and crossed arms remain readable.
- [ ] The 200 expression references and 40 body references are mapped as acting guides on the same rig.
- [ ] Registered alternates are used where deformation is unsuitable.
- [ ] Moving joints have been visually inspected for gaps, clipping, and detached pieces.
- [ ] Actual live UDP control has been verified in Godot, not only rendered.
- [ ] Setup instructions, mappings, previews, and build journal are delivered.
- [ ] Every phase has been pushed to remote `main` and verified.
- [ ] Required PNG approvals have been obtained between phases.

## 15. Immediate resume instructions

1. Restore the production workspace and source checkout paths listed at the top.
2. Confirm remote `main` includes this handoff and the approved Phase 3 records.
3. Run `python3 tools/validate_gestures.py` and confirm `status: passed`.
4. Read `manifest/gesture_layers.json`; use only the authoritative `_registered.png` bodies.
5. Do not modify the approved neutral build or final gesture artwork unless a new visual defect is identified.
6. Begin Phase 4 by restoring the runnable Godot project and updating `rig/rig_controller.gd` for the final gesture architecture.
7. Keep a new `PHASE_4_CHECKPOINT.md` as work progresses, clearly marking runtime and live-control tests as unverified until actually executed.
8. Push and verify Phase 4 on remote `main`, then send PNG previews for approval.

# Approved live head ownership audit

Source-only audit, 2026-11-11. No approved files, registration, renderer, or rig code changed. The PNG is an alpha-composited diagnostic contact sheet, not a native-render proof. Sources retain misleading RGB beneath zero alpha; inspecting RGB alone falsely suggests a whole bust in the head.

## Findings

- `object_face.gd` replaces the live `stationary_backing` texture with `rig_assets/smile_support/stationary_backing_eye_reassigned.png`. Its nonzero alpha bounds are (377,337)-(746,720). There are zero nonzero-alpha pixels at y>=720. It contains face, ears, most earrings, and a small upper-neck wedge behind/below the jaw around y675–719. It contains no collar, blouse, jacket, shoulders or sleeves.
- The independent hair owners are hair temple left/right, crown/bun/rear, fringe, their underlaps, and smile-specific fringe continuation/pigment owners. Keep all unchanged. Their source cutouts include tiny inherited skin/color fragments; this audit does not authorize repainting them.
- `FixedNeckTorso` is a separate Sprite2D sibling of `RigidHead`, instantiated by `object_rig.gd`. Its nonzero alpha bounds are (45,720)-(1135,1384). It contains neck/chest, necklace, collar, blouse/jacket/sleeves, and the dangling earrings' final tips.
- Current approved manifest does NOT instantiate independent earring objects. Earrings are baked into stationary backing above y720, with tips in FixedNeckTorso below that boundary. Separate earring files exist, but their existence is not live independent ownership. Their alpha bounds are left (397,600)-(422,736), right (704,598)-(731,735).
- The separate earring textures are not pixel-identical to the corresponding FixedNeckTorso tip pixels. Do not substitute them while claiming exact approved visual parity. Left tip mask has 250 nonzero pixels (235 also nonzero in FixedNeckTorso); right has 231 (183 also nonzero there).

## Safe additive adapter boundary

After the approved expression controller finishes `_ready` and passes readiness, keep and reparent its existing live `RigidHead` exactly as the adapter already does. Detach/free `expression_rig.body` and set that reference to null. No approved runtime code reads `body` after construction: source search across object_rig.gd, expression_rig.gd and parts confirms construction-only references. Preserve the controller, face tree, all existing textures/shaders/owners and timelines. This keeps all 47 profiles and existing eye, mouth, brow and hair controls.

Do not move, hide, flatten, or crop stationary_backing wholesale. It is essential face skin and facial coverage. Use independently owned raw body pieces for neck/collar/chest/garment. Do not carry `approved_neck_chest` or the full FixedNeckTorso texture into that new body.

Removing FixedNeckTorso alone loses the bottom 15–16 source-pixel earring tips. Before asserting complete head anatomy, preserve those exact source pixels in additive head-owned tip-only sprites selected by an explicitly reviewed earring-only alpha mask. Never attach a full bust texture to recover them. This preserves static existing earring appearance, NOT independent earring motion. Truly independent earrings require reviewed removal of embedded earring pixels from an additive backing copy plus full earring owners; that is a separate ownership change, not already approved behavior.

## Proof plan instead of motion demo

Current `tests/sample_wiring.gd` couples spine/chest from 5–9 s, all limbs from 9–13 s, and frame x/y/roll from 13–16 s. This hides which owner causes an error and looks like a choreographed leaning demo. The CPU renderer flattens the neutral head, so it cannot demonstrate live facial ownership.

1. Static neutral full figure plus labeled piece inventory/exploded ownership layout, on a contrasting background. Show separate neck, collar, chest, garment, upper/lower arms, hands, pelvis, thighs, shins, shoes. Include exact parent IDs and pivots.
2. Neutral close-up of face/jaw/earring tips/neck/collar before any motion.
3. For each joint individually: neutral, small negative endpoint, neutral, positive endpoint, neutral. All other control values zero. Start head, then neck if genuinely supported, chest, spine, each shoulder/elbow/wrist, each hip/knee/ankle. Keep frame_roll zero. No combined limb or torso sweeps.
4. Test frame_x and frame_y separately only after anatomical wiring is verified; omit roll from the main proof.
5. Show live facial controls with body neutral as a separate native-render check when permitted. Clearly label CPU source composites as insufficient evidence for shaders or expression coverage.

See `alpha_correct_source_proof.png` and `source_alpha_inventory.json` for alpha-correct source evidence. The JSON lists base manifest objects and specific audited sources; it is not an exhaustive inventory of dynamically added smile/oral owners.

## Exact additive earring tips generated

`extract_earring_tips.py` now extracts approved FixedNeckTorso pixels without resampling. `earring_tip_manifest.json` records source/output hashes and masks. Anatomical L is screen-right: mask [704,720,731,736], 186 nonzero-alpha pixels. Anatomical R is screen-left: mask [397,720,422,736], 235 pixels. Bounds are right/bottom exclusive. Both PNGs retain the full 1136×1384 canvas; all pixels outside the retained source-alpha selection are zero RGBA. The masks contain only the dangling gold tips, as verified in alpha-correct magnified source crops.

Use `earring_tip_L.png` and `earring_tip_R.png` as centered=false Sprite2D children at head-local origin, local scale ONE, relative z_index=20. Inherit head scale .32 once. No full-neck/body node is required. `neutral_head_complete.png` composites these tips under the existing neutral head source. `earring_tip_join_proof.png` shows the resulting alpha-correct jaw/earring detail and was visually inspected: both earrings continue through the original y720 cutoff without duplicated whole-earring owners. It also exposes the retained small upper-neck wedge ending at y720, which the independent body neck piece must meet. This is CPU neutral source proof, not native expression rendering.

# Ryoko VTuber — Phase 1 Visual Design Lock

**Status:** Proposed and awaiting user visual-checkpoint approval  
**Prepared:** 2026-11-01

## Source review completed

The following approved sheets were downloaded from the public repository and visually inspected during this phase:

- Neutral bust, full-body front, side, back, and A-pose masters
- Eye and mouth construction sheets
- Hair construction sheet
- Gold accessories sheet
- Outfit construction sheet
- Hands and pumps sheet

The neutral facial master and front/back body masters govern identity and costume. Secondary sheets clarify construction but do not override those masters. The drawings remain visual guides rather than measured orthographic projections.

## Canonical visual interpretation

### Scale, axes, and build pose

- Working height convention: **1.83 m** from the sole-contact plane to the top of the natural skull in neutral standing pose and pumps. Rear hair and hair sticks extend above this height.
- Ground/contact plane: Blender `Z = 0`; vertical axis: `+Z`.
- Neutral forward direction: `-Y` in the Blender authoring scene. Export conversion is a later validated step.
- Character-left is `+X`; character-right is `-X`. All asymmetrical controls and documentation use character sides, never viewer sides.
- Use the supplied A-pose as the build-pose target: arms clear of the torso and hips, relaxed wrists, and individually articulable fingers.

### Body and silhouette

- Tall, slender adult woman with long legs, a fitted waist, moderate shoulders, and a composed upright posture.
- Preserve the illustrated bust and torso proportions without exaggerating or minimizing them into a different design.
- No chibi proportions in the main avatar. Chibi source panels remain optional effect/style references only.
- Hands must support relaxed, open, pointing/finger-wag, fist, crossed-arm, and contact poses.

### Face and eyes

- Use the neutral bust for facial identity: restrained adult anime planes, softly pointed chin, small nose and mouth, and amber/gold almond-shaped eyes.
- Use black upper eyeliner/lashes, restrained lower lashes, dark pupils, and clean iris catchlights.
- The long side fringe falls on **character-right**; the **character-left** ear is more exposed.
- Eyelids must close over the actual eye geometry without leaving the eyeball visible through the skin.
- Expressions will be authored on one consistent head using shape keys and controls, not by swapping unrelated heads.

### Mouth

- Neutral lips are closed and understated.
- Build a real mouth cavity, upper and lower teeth, and tongue. The painted close-ups are construction guides, not measured internal geometry.
- Jaw opening, lip sealing, visemes, smiles, and asymmetric controls must work on the same face and avoid teeth/tongue intersections.

### Hair

- Mint/sage hair with an asymmetric layered fringe, loose temple strands, and layered nape coverage.
- Resolve the rear style as a **high bun-loop with a short loose ponytail fan**, matching the neutral and hair-construction masters rather than choosing an unrelated bun or long ponytail.
- Keep the rigid gathered base distinct from deformable loose sections.
- Use separate secondary-motion groups for the ponytail fan and selected loose strands; do not make every hair card independently physical.

### Accessories

- Two diagonal gold hair sticks at the rear crown, with the visible ornamentation biased toward **character-left**.
- Follow the accessory detail sheet for the lower stick's short hanging chain/drop construction; overlapping visibility in the masters is not proof that only one chain exists.
- Long matched gold earrings: open diamond upper link and two slim hanging bars of unequal length.
- Fine gold necklace with a small green diamond-shaped pendant.
- Hair sticks, earring links/bars, buttons, buckle, and pendant are rigid parts. Chains and earrings receive restrained secondary motion and collision limits.

### Outfit and footwear

- Dark charcoal/black tailored, single-button blazer with a gold waist button, notch lapels, flap pockets, center-back seam, and three gold cuff buttons per sleeve.
- White rectangular pocket square on the **character-left** breast.
- White open-collar blouse with pointed collar, visible buttons, and a tucked lower construction.
- Matching dark tapered trousers, black belt, and rectangular gold buckle.
- Black pointed stiletto pumps with a dark upper and tan/leather-colored sole.
- Illustrated wrinkles and shadows are not permanent albedo. Model construction seams and major folds; let posing and runtime lighting produce secondary creasing.

## Layering and assembly contract

Build and review the avatar in this order:

1. Body and neutral head
2. Eyes, eyelids, mouth cavity, teeth, and tongue
3. Blouse and tucked lower construction
4. Trousers and belt
5. Blazer, lapels, pockets, buttons, cuffs, and pocket square
6. Pumps
7. Scalp/hair cap, fringe, nape, bun-loop, and ponytail sections
8. Hair sticks, earrings, necklace, and pendant
9. Facial controls and expression presets
10. Optional overlays/effects, kept separate from base textures

Every visual construction or layering checkpoint must compare Blender against the matched source view. Face checkpoints must include consistent neutral/deformed cameras and side or close-up views where front views can hide defects.

## Initial production budgets

These budgets serve the high-detail 1440p60 target but remain subject to user-hardware testing:

- Working visible-avatar budget: approximately **150k–220k evaluated triangles**, with face, eyes, hands, and hair silhouette prioritized.
- Avoid unnecessary runtime subdivision and duplicated hidden surfaces.
- Use fitted UV atlases; 4K maps only where they provide visible value, with lower-resolution fallback maps if needed.
- Consolidate materials where practical and limit transparent overdraw, especially in hair and effects.
- Keep secondary-motion groups limited and purposeful.

These are starting budgets, not a performance guarantee.

## AI-directed performance implications

- Neutral idle, breathing, blinking, gaze, and return-to-neutral behavior must be built from the beginning as reusable systems.
- Facial, head, body, and secondary-motion channels remain separable for AI-controlled composition.
- The 200 expressions will reuse the common facial-control system; the 40 body gestures will be separate Blender actions.
- No expression mass production begins before the early facial feasibility checkpoint is approved.

## Phase 1 approval gate

Approval confirms this visual interpretation and layering contract as the target for the Phase 2 full-character blockout. It does not certify geometry, rigging, expression correctness, VRM export, AI control, tracking, or runtime performance.

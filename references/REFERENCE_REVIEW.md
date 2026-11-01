# Ryoko character reference review

Reviewed: 2026-11-01. All six supplied PNGs were opened and visually inspected. Original bytes are retained under `originals/`; file hashes, dimensions, original names, and stable reference IDs are in [manifest.json](manifest.json). This is a review of reference art, not validation of a model or rig.

## Shared design actually visible

- Adult human woman with a tall, slender silhouette. REF-001 and REF-005 label her as Ryoko, age 28, height 183 cm, corporate strategy director at Shirotani Global Holdings. These are character-sheet labels, not verified facts about a real person.
- Mint/sage green hair, swept asymmetric fringe, gathered rear hair/updo with a short loose ponytail-like section; gold hair sticks and dangling accents.
- Amber/gold eyes, light warm skin, black eyeliner/lashes, restrained anime facial construction and cel-like shaded illustration.
- Tailored black blazer and matching trousers, open-collar white blouse, belt, black pointed pumps with heels. Narrow gold details/buttons occur in the outfit.
- Long gold earrings and a fine necklace with a small green pendant. REF-006 includes accessory, shoe, hair, eye, collar, and hand close-ups.
- Composed and authoritative baseline with warmth, embarrassment, humor, vulnerability, and exaggerated comic reactions. She is not limited to a stern expression.
- These references define the human corporate Ryoko design for this project. Do not import a black-haired masked or gloved variant from unrelated artwork.

## Source inventory and intended use

| ID | Original | Visible contents | Proposed use |
| --- | --- | --- | --- |
| REF-001 | `ryoko02(20261101-114212).png` | Front, side, back full-body presentation; two face/upper-body close-ups; palette and character labels | Primary silhouette, costume and proportion reference |
| REF-002 | `ryokoexpresshuman1.png` | Six special performances, numbered 1–6; gestures, props, comic effects and chibi annotations | Acting intent and expression extremes, not neutral geometry |
| REF-003 | `ryokoexpresshuman2.png` | Six special performances, numbered 7–12; crossed arms, hand-to-face poses, confident and affectionate behavior | Acting intent and hand/body accompaniment |
| REF-004 | `ryokoexpresshuman3.png` | Six special performances, numbered 13–18; cold glare, silent fury, reprimand, concentration, disappointment and restrained rage | Distinguish subtle anger/focus families instead of duplicating one angry face |
| REF-005 | `ryokoexpressions.png` | **Sixteen** labeled bust expressions in a 4×4 grid, plus left-hand biography/palette | Broad facial range and relatively consistent frontal framing |
| REF-006 | `ryokov1.png` | Front/back character presentation, head close-up, six small head studies, color/accessory/shoe/prop/detail panels | Secondary technical detail and palette reference |

REF-005 contains happy, laughing, excited, proud, surprised, shocked, confused, embarrassed, angry, annoyed, determined, serious, sad, crying, worried and neutral. It contains 16 portraits, not 15.

Special references include flustered, pouting, panicking, suspicious side-eye, sparkling admiration, comic devastation; tsundere, shocked, hiding embarrassment, smug confidence, serious/battle mode, affection; and the six anger/focus performances listed above. These are existing concepts to incorporate and refine, not 18 approved completed production assets. Some overlap the base grid and should not be counted as automatically distinct new expressions.

## Proposed precedence, pending design lock

1. Use REF-001 for overall human character silhouette and outfit.
2. Use REF-006 to propose specific accessory construction and palette details where REF-001 is too small.
3. Use REF-005 for neutral-facing expression comparisons.
4. Use REF-002–004 for performance intent, gestures, comic exaggeration, and optional effects.

This hierarchy is a proposal for approval, not an assumption that every inconsistency has already been resolved. Do not average contradictory details invisibly. Preserve all supplied references and record decisions in the eventual character bible.

## Differences and decisions to resolve before mass generation

- **Geometry and framing:** These are posed illustrations. Front/side/back views are not proven matched orthographic projections; hands, shoulders, head angles and stance vary. Build aligned modeling references from an approved master rather than directly treating these as measured blueprints.
- **Hair construction:** The gathered section alternates visually between bun-like mass and loose ponytail. Lock volume, tie location, strand groups, fringe side and ear exposure in a neutral turnaround. Avoid accidentally mirroring the asymmetry.
- **Jewelry:** Lock exact number, position and attachment of hair sticks, hanging chains/charms and earrings. Their overlaps and visibility change among poses. Clarify rigid sticks versus moving strands, chains and earrings.
- **Clothing:** Collar spread, blouse opening, button details, chest-pocket white detail and blazer fit vary with pose/illustration. Fix one neutral construction. Wrinkles are pose-dependent, not permanent surface geometry.
- **Face consistency:** Jaw, eye shape, fringe overlap and head proportions vary subtly across expressive images. Preserve identity while deforming approved facial controls; do not reinterpret each portrait as a different face.
- **Palette:** REF-006 provides stylized swatches/codes, but those codes are not a complete calibrated numeric color specification. Sample and approve a clean palette in a later phase; lighting and existing painted shadows must not become permanent albedo by accident.
- **Scale:** 183 cm is the sheet's proposed character height; shoe height and model origin need an explicit convention before modeling/export.
- **Runtime:** Full-body references are available, but final model coverage, tracking input, target application and export format are still undecided. Availability of a full-body sheet alone does not approve a specific runtime or rig.

## Facial motion, effects, and props are separate systems

The sheets combine facial deformation with blush, sweat drops, tears, sparkle eyes, blank white comic eyes, forehead shadows, anger symbols, speed lines, aura/flame shapes, speech balloons, hearts and chibi cutaways. A normal facial morph cannot alone reproduce all of those effects.

The future expression manifest should separately specify:

- Facial deformation controls and left/right asymmetry.
- Eye/mouth material or geometry swaps where required.
- Optional transparent overlays or scene effects, with attach point and visibility timing.
- Head/shoulder/hand action clips and contact constraints.
- Props such as a folder/papers, mug or business card, only where explicitly included in the approved scope.
- Lip-sync, blink and gaze behavior while an expression/effect is active.

No decorative text, page borders, corporate footer, comic speech balloon or chibi figure should silently be baked into the main avatar face/body texture. Chibi cutaways are style references unless separately scoped as an alternate avatar.

## Missing production information

The supplied sheets are valuable design references, but do not contain a 3D mesh, matched neutral orthographic turnaround, A/T pose, topology, UV unwrap, texture atlas, bone hierarchy, weights, authored shape keys, animation curves, tracking mappings, runtime materials or tested export. They also do not provide a complete mouth interior, unobstructed face/hair construction, finger articulation breakdown, or temporal frame sequences.

Later image work can propose the missing visual designs; Blender construction must create and validate the model-dependent assets. A 3×3 expression sheet is a nine-key-pose visual guide, not nine already rigged or guaranteed temporally consistent animation frames.

## Preservation and current scope

Original PNGs remain unchanged, including all embedded sheet labels and background graphics. No cropping, repainting, rescaling, transparency alteration or image generation was performed in this setup pass. Names are preserved for provenance and stable REF IDs provide organization. Future generated derivatives should go into separate asset folders, never overwrite these originals.

Current task: repository references and phased planning only. Any later image-generation or Blender execution phase requires the corresponding user go-ahead and unresolved design choices to be settled.

# Ryoko facial-control checkpoint

Approved isolated 2D Godot facial checkpoint. Original full-body rig is untouched. This folder is self-contained and does not replace it.

## Implemented
- Approved neutral artwork as a bust foundation, with generated seamless mouthless skin beneath the interchangeable mouth region.
- Independent registered neutral, A, E, I, O and U mouth sprites. Vowels retain the actual existing rig's artwork, scaled 1.45x and positioned to this approved bust.
- Independently controlled left and right eyelid replacement sprites, derived from an image-generated closed-eye variation and registered without the previous erroneous 10-pixel upward shift.
- Mouth/viseme, paired and independent blink commands; amplitude-only mouth fallback; reset; optional demonstration loop.
- Binary blink swaps only, no continuous eyelid deformation.

## Actual tests
Godot 4.6.3 headless imported the project and passed 89 control assertions: all six mouth textures exist, exclusivity of active mouth, both eyelids independent, mouth/blink coexistence, invalid-state rejection, amplitude fallback and reset. See `control_tests.log`.

Neutral sprite reconstruction is pixel-identical to the approved neutral after near-opaque alpha normalization. Generated pixels with alpha >=240 were normalized to255 to avoid translucent stacked skin changing opacity. RGB artwork was not recolored. The original approved file remains preserved outside this project.

`previews/facial_states_contact.jpg` and `approved_and_source_comparison.jpg` show actual registered-sprite composites. `facial_sprite_sequence.gif` demonstrates the composited state sequence, NOT a Godot runtime capture. No graphical live-render verification occurred.

## Review limits
This is genuinely separate facial control on a fixed bust foundation, not a completed full-body re-rig. Head turns, gaze, head/neck deformation, dedicated emotions, breathing and secondary physics are not implemented here. The eyes are fixed open artwork unless replaced by eyelid sprites. Blink overlays include local skin and some hair-edge pixels; inspect these borders in the comparison before approval. Mouths are source visemes, not a claim of phonetic accuracy for every language. The app must supply mouth/viseme commands or amplitude values; this project does not itself analyze audio.

## Running
Open `project.godot` in Godot4.6.3. For a demonstration: `godot --path . -- --demo`.
Headless control test: `godot --headless --path . --script res://test_controls.gd`.
Controller `_handle_command` accepts existing-style dictionaries such as `{"viseme":"A","blink_L":0,"blink_R":1}`. No network listener or microphone access is active.

## Next approval gate
Review likeness, blink borders, mouth size/placement and vowel shape. Only after approval: integrate further facial features/emotions or head/body motion. No secondary-motion quality claims are made.

## Blink overlap correction
User identified residual open upper lashes during closed eyes. Expanded opaque eyelid coverage upward and sideways, reduced edge feathering, and removed an incorrect 10-pixel source shift. Close-up comparison includes approved open-eye artwork, rejected old blink, and corrected blink/winks. All six mouth composites remain pixel-identical to the previous checkpoint. No new expression artwork or network changes were made.

## Phase approval and provenance
User approved the neutral likeness, then approved this corrected blink on 2026-11-04 and requested Git checkpoints between phases. This commit records the approved facial foundation before dedicated emotion work. Original repository files are unchanged.

The source approved neutral and generated blink/mouthless variant are in `sources/`; original A/E/I/O/U mouth cutouts are in `sources/source_mouths/`. `tools/build_assets.py` reproduces registration and composites using Pillow and NumPy. It performs crop/mask/registration operations, not new artwork generation. Runtime needs only the Godot project assets and registration JSON.

The earlier 3D-related materials elsewhere in the repository are not inputs to this checkpoint. This project is 2D. Open `project.godot` in THIS folder. Do not infer a finished avatar, phoneme analyzer or production integration from these tests.

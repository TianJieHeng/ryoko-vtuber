# Ryoko separate-part base assembly

This standalone Godot project is the reusable base assembly requested before more emotion work. Its default scene is **object_rig.tscn**. No EXP-005/EXP-163 performance timelines, old face renderer, or emotion-patch fallback are included.

## What is assembled

- The original clean face foundation and two ears.
- Six separate original hair objects: rear scalp, bun, short tail, front fringe and two temple locks.
- Two separate sclerae, complete irises, lashes and brows.
- The original neutral-lips object plus exclusive original A/E/I/O/U mouth variants.
- Separate existing earring and hairstick/ornament cutouts.
- A fixed neck/outfit crop from the canonical bust, with old baked hair/accessory fragments removed.

The clean source face contains no eyes, eyebrows, mouth or hair. All moving features are separate objects. Iris movement uses rigid translation behind an alpha-only aperture; lashes translate and brows/hair rotate or translate. No face mesh deformation, local UV warp, animated scale, or emotion opacity crossfade is used.

The source pack has different face shading, nose/eye drawings and hair framing from the previous flattened bust. This new fixed registration is not claimed pixel-identical to that older composition. The original source PNGs are unchanged. The prior approved EXP-005 project remains separate and recoverable, but its old face deformation is not represented as compliant with this base.

## Run

Use Godot 4.6.3. Open project.godot and run the default scene.

- B: blink hold/release; O: raise/release brows.
- M: select A mouth / restore original neutral lips.
- H: toggle restrained independent hair sway.
- Left/right arrows: rigid iris gaze; 0: reset all controls.

The base opens at neutral with auto-blink off, so registration can be inspected without motion. See CONTROL_API.md for programmatic controls and limitations.

## Deliberately deferred

All 93 legacy expressions and all emotion performances are disabled in this base. Continuous mouth opening is also disabled until a smooth mechanism can preserve the real neutral-lip silhouette. The base exposes discrete, exclusive source visemes instead. Full head/neck/body articulation, tracking/live input, old secondary physics/effects and preset compatibility are not included.

## Rebuild and verify

Runtime does not need Python. Asset regeneration needs Python 3, Pillow, NumPy and SciPy.

    python tools/build_object_face.py
    python tools/verify_object_base.py
    godot --headless --path . --script res://test_object_rig.gd
    bash tools/capture_object_rig.sh <output-directory>

For restricted environments, use writable HOME and XDG_CONFIG_HOME/XDG_DATA_HOME/XDG_CACHE_HOME. The capture script creates these automatically and uses the local Godot OpenGL movie writer. See VALIDATION.md for actual checks and viewing limits.

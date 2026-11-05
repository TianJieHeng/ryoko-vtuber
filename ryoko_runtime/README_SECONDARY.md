# Whole-chest bounce revision

Approved by the user on 2026-11-05 for publication. This revision keeps the accepted bounce timing and amplitude, but replaces the narrow central deformation mask with a broad whole-chest region. Both sides of the bust, the shirt and nearby jacket now follow through together. The full-strength area spans x=258–878, y=1050–1280 in the source artwork, with soft transitions toward shoulders, outer jacket and the anchored bottom. Previously the full-strength area spanned only x=423–713, y=1070–1190.

The neck and shoulder line remain unaffected by secondary displacement. The body still rises and settles as a single torso, with secondary chest motion layered on top. No idle loop is introduced. No artwork is changed.

Runtime preview: actual Godot 4.6.3 movie capture, 568×760 at 30fps, 14 seconds. Three isolated bounces at 2, 5 and 8 seconds followed by quiet rest. Existing bounce amplitude remains approximately 7.3 screen pixels body lift and 3.7 pixels peak chest follow-through.

Validation: all seven suites pass, including whole-chest weight coverage, shoulder isolation, settling, clamping, audio and expression regressions. Temporal review uses extracted frames; native-speed playback cannot be watched here, the user reviewed and approved the actual runtime MP4. No CI was run or added.

## Controls and reproduction

`apply_controls({"bounce": true})` triggers one vertical torso bounce. `apply_controls({"chest_secondary": false})` disables the chest follow-through and restores rigid torso motion. Secondary motion is driven by torso movement, not an idle sine wave.

Run `godot --path ryoko_runtime res://motion_rig.tscn -- --secondary-proof` for the approved three-bounce sequence. Run `godot --headless --path ryoko_runtime --script res://test_bounce.gd` and `test_chest_secondary.gd` for focused regression checks. The previous five regression scripts remain unchanged.

The deformation is a weighted 2D mesh, not separate 3D breast geometry. Videos and temporary render caches are excluded from this source checkpoint.

# Approved EXP-005 hearty laughter

This release adds only **EXP-005 hearty laughter**. The existing 93 registered static expressions, original PNG artwork, existing effects, and EXP-064/EXP-189 gaze layers remain unchanged. Other expression performances and experimental morph/gaze layers are not included.

## Use

Run the default Godot scene. Enter plays hearty laughter from neutral or an unsupported static face; on a supported expression it replays that expression. Shift+comma/period cycles supported performances (currently only EXP-005). Plain comma/period continues to cycle all 93 static faces. R resets. Existing motion, expression, speech, eyelid, clip, and performance-preset controls remain available.

The public command is `apply_controls({"perform_expression":"EXP-005"})`. Supported options on a new request are `expression_strength` (0–1), `expression_speed` (0.25–2), and `expression_loop` (boolean). `expression_paused` pauses/resumes; `expression_cancel` eases back to neutral. A static `expression` command takes over immediately. A repeated performance request releases the current performance before starting the queued one. Live speech uses the original visemes and hides the emotional mouth until speech is released.

The existing opt-in localhost UDP adapter and version-1 clip controls accept the same performance commands. Runtime validation uses the loaded performance registry, not the static-expression registry. Unsupported requests, including a registered static expression other than EXP-005, are rejected before changing ownership, stopping a clip, or mutating the current performance. The standalone validators retain their legacy default behavior when no explicit performance allowlist is supplied.

## Rendering and preservation

The mouth is a source-derived oral feature over harmonic skin underpaint. The shader transforms oral pixels only, retains the original patch alpha, protects the nose/chin, and samples the original source exactly at the undeformed full-open peak. The oral-feature texture uses mipmaps with `filter_linear_mipmap`. Preserve `rig_assets/expression_mouths/EXP-005_feature.png.import`, including `mipmaps/generate=true`.

The generator estimates RGB for 9,406 explicitly masked mouth-underpaint pixels. This is not new teeth/tongue artwork: teeth and tongue remain part of one 2D cutout. Eyes and non-articulated face layers use opacity handovers. The approved isolated-mouth shader assigns its own alpha, so its mouth appears/disappears at the visible handover boundary rather than following the face opacity fade. This release preserves that exact user-approved behavior; it is not a seamless anatomical morph. Unused experimental morph code and assets are excluded.

## Reproduce locally

Requires Godot 4.6.x. `godot --headless --path . --editor --quit` imports the project. Run `godot --headless --path . --script res://test_hearty_laughter.gd`, `res://test_release_performance_controls.gd`, and each inherited `test_*.gd` in separate writable HOME/XDG directories. No CI is needed.

`python tools/build_performance_mouth_layers.py` regenerates EXP-005 derivatives only; Python dependencies are NumPy, Pillow, and SciPy. The generator never edits artwork. The preserved feature import sidecar enables mipmaps on Godot import.

`bash tools/capture_isolated_mouth_qa.sh` captures the full oral timeline using an isolated local Xorg dummy display and runs the pixel validator. On Linux this additionally needs Xorg with the dummy driver and xauth. `review_hearty_laughter.gd` plays two complete cycles through the public API for actual Godot movie-writer review. See the validation report for exact evidence and limitations.

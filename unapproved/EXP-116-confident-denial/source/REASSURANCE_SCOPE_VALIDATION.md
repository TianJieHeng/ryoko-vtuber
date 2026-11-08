# Scoped EXP-107 confident reassurance

Local candidate for separate review. Parent: `4f3deaa2de3eedb691a9f0c795c7b8563663e472`, project tree `1dc4895b0e0fbf5a7498cf853b267d19a44e8b3d`. Five data-only performances share the same registry, player and app. All 182 PNGs and four prior definitions are byte-identical. No new artwork, expression-specific project or controller is added.

## Reference and performance

Exact catalogue commit `7693d1b8718c3bb1c717bd586fb472a7efc42403`, path `avatar_build_assets/reference_library/assets/expressions/EXP-107_confident-reassurance/RYO_EXP-107_confident-reassurance_sheet_v001.png`. Sheet SHA256 `08e4f43e20144930411dd49087eaa76d70bde1fb0214b70b6d56bd5ed42797d0`; Git blob `beb8ee82e3edde215da08097552b7de88432e731`. All nine panel hashes and exact integer crops are preserved in reference metadata. KP05 is the published peak, not another expression.

The reference intent is centrally softened brows, direct eyes and a relaxed open smile without dominance. Eleven keys across 3.0 seconds interpret the static pose sequence: neutral, preparation, closed smile at .60, one modest open accent at 1.20, closed follow-through at 1.56, lingering smile at 1.92, release at 2.35, settle and exact neutral at 3.0. The catalogue's 1.9-second timing is explicitly a proposal, not recovered animation. No unsolicited blink, gaze drift, hair/head/body acting, blush or other effect is authored.

## Only added capability

`mouth_oral_lift` translates the existing lower oral-surface owner upward by `40 * (1 - mouth_spread * mouth_smile) * lift`, within the pre-existing 40-pixel total envelope. It uses fixed source, UV, atlas region, unit scale and full opacity. It does not affect any other owner, anatomy, mouth width or clipping aperture. Zero preserves predecessor arithmetic. The central white upper teeth remain at (533,626). Public mouth_open is still 0–1 with a .55 physical multiplier and maximum 30.8-source-pixel integrated aperture.

## Reproducible checks

Clean source checks:

    python tools/verify_reassurance_scope.py
    python tools/verify_giggle_scope.py
    python tools/verify_welcome_scope.py
    python tools/verify_closed_smile_support.py
    python tools/verify_blush_source.py
    sha256sum -c SOURCE_FILES.sha256

In a separate rebuild copy, run build_object_face, verify_object_base, verify_yawn, verify_teeth, verify_gaze_assets, verify_gaze_coverage, verify_lid_handoff, verify_smile_support, verify_spread_support, verify_closed_smile_support and verify_blush_source from tools/. Builders generate diagnostic images which are not shipping assets.

Godot 4.6.3 import then these fifteen scripts with `--headless --path . --script res://SCRIPT`, using writable HOME/XDG paths:

- test_object_rig.gd, test_yawn.gd, test_teeth.gd, test_expression_backbone.gd
- tests/test_gaze_runtime.gd, tests/test_viewer_layout.gd, tests/test_smile_controls.gd
- tests/test_laughter_runtime.gd, tests/test_spread_runtime.gd, tests/test_giggle_runtime.gd
- tests/test_corner_lift_runtime.gd, tests/test_closed_smile_contract.gd, tests/test_blush_controls.gd
- tests/test_oral_lift_contract.gd, tests/test_reassurance_runtime.gd

Real rendering uses the existing supported desktop display, Godot Compatibility OpenGL Mesa llvmpipe, and rewrites controls after every fixed review scale change to refresh clipping coordinates. Headless dummy rendering is not image evidence. Review harnesses capture two complete cycles at 30 fps, exact keyposes, repeatability and prior-performance/gaze parity. Physical aperture is checked with the unchanged production clipping shader. Source hashes and rendered pixel parity are distinct gates.

Current execution results and exact freeze/media identities belong in `validation/reassurance_final_review.json`; historical receipts are not evidence of new execution. The optional loopback API is preparation only, not an AI/TTS connection. Fresh socket transport tests are blocked by sandbox listening-socket restrictions and are not claimed. Normal-speed audiovisual playback is not claimed unless an explicit new receipt says it was performed.

## Limits

The canonical approved character differs stylistically from the catalogue drawings. The rig preserves its existing white enamel and face structure rather than repainting the reference. Rigid brows cannot reproduce painted curvature exactly; no body/open-palm accompaniment is included. Existing faint fringe traces can occur with nonzero manual hair_sway; authored EXP-107 uses zero sway. Those inherited traces are not claimed fixed by this scope.

# Scoped EXP-006 suppressed giggle

This is a local review candidate, not user approval or publication. Base: published main `69e74ce5049a13ad5aa33014cacb1287f494787a`, subtree `ryoko_object_rig/`. Exactly four data-only performances share the existing registry, controller and app: EXP-163, EXP-005, EXP-001 and EXP-006.

## Source and scope

All 174 published parent PNGs and the complete EXP-163/005/001 profile bytes are preserved. The new generic `mouth_corner_lift` and `mouth_lip_press` controls are normalized 0–1 with default zero. Lip joints are rigid; cubic lift uses endpoint secants without hooked corners. Four source pixels of inferred inner-upper-lip continuation are exposed by spatial clipping across 14 fixed-source rigid children. The original seam is not lowered. The two inferred PNGs are documented in `rig_assets/pressed_lip_support/manifest.json`.

`blush_intensity` is a separate bounded 0–1 effect control, default zero. It changes alpha only on two independent original-source cheek FX sprites. Fixed positions, masks and registration are documented in `rig_assets/blush_support/manifest.json` and `REGISTRATION_PROVENANCE.md`. The two original FX PNGs are preserved exactly. Static crop/resampling and conservative cheek/foreground-clearance masks are authoring registration, not animated facial scaling or opacity crossfading. No core face/eye/brow/mouth/hair object receives expression-opacity changes.

No wide-eye assets, EXP-003/007, oral-lift control, tracking, body/hand acting, external model/TTS, CI or paid service is included. Central upper teeth remain white at (533,626). Public mouth_open remains 0–1 with physical multiplier 0.55 and a 30.8-source-pixel per-column cap.

## Reference and timing

The exact reference is `avatar_build_assets/reference_library/assets/expressions/EXP-006_suppressed-giggle/RYO_EXP-006_suppressed-giggle_sheet_v001.png` at repository commit `7693d1b8718c3bb1c717bd586fb472a7efc42403`. Git blob: `6d74152c9c12e6f6a1030336f2f90e2eddd62d55`. SHA256: `59a58716099bdd126e7ab4a106fdfb5ae9b75471e4d4bdd0b978997428e1a848`.

The corrected 13-key, 2.8-second no-blush profile is retained exactly in `source_references/EXP-006_no_blush_profile.json`. Every original key time, phase and mouth/eye/brow value remains identical in the live profile. The only added timeline channel is blush: 0,0,0,.275,.55,.25,.055,.0275,0,0,0,0,0. It builds once to the pressed smile and fades after the brief leak; there is no second strong re-press pulse. Animation timing and effect intensity are interpretations of the static sheet, not recovered authored animation data.

The matched-reference board associates neutral KP01, pressed peak KP05, leak KP06 and final neutral KP09 with their full-face actual-render keyposes. It does not reuse a blushing full-face target for the later no-blush re-press.

## Verification commands

On the clean source:

    python tools/verify_giggle_scope.py
    python tools/verify_welcome_scope.py
    python tools/verify_closed_smile_support.py
    python tools/verify_blush_source.py
    sha256sum -c SOURCE_FILES.sha256

In an isolated rebuild copy, run the historical object/yawn/teeth/gaze/lid/smile/spread builders and checks listed in PACKAGING.md, then the closed-smile and blush verifiers. The blush builder works with its default shipping-root location and verifies all original FX and foreground dependency hashes.

Run Godot 4.6.3 import and all shared runtime suites: test_object_rig, test_yawn, test_teeth, test_expression_backbone, tests/test_gaze_runtime, test_viewer_layout, test_smile_controls, test_laughter_runtime, test_spread_runtime, test_giggle_runtime, test_corner_lift_runtime, test_closed_smile_contract and test_blush_controls. Use writable HOME and XDG data/config/cache directories. The effect suite covers source/geometry/opacity invariance, bounds, invalid-transaction atomicity, ownership, release, reset, retrigger, cross-expression interruption and exact neutral clearing.

Actual rendering uses the supported desktop display and OpenGL Mesa llvmpipe, never headless dummy-render pixels. `tools/review_giggle_scope.gd` captures an eight-second 30 fps movie with two complete cycles and neutral ending at both full-bust and native detail sizes. Its optional `--zero-blush` test override suppresses only the effect scalar for exact comparison with the retained no-blush source. `tools/review_welcome_movie.gd` and `tools/review_giggle_regression.gd` capture the prior performances and bounded gaze cases.

Current evidence status is recorded in `validation/giggle_final_review.json`. Pixel comparisons and independent review are separate from source guards. The optional loopback bridge's new control is statically/runtime validated, but this sandbox cannot bind listening sockets, so a fresh process-level loopback test is not claimed. Normal-speed audiovisual playback is not claimed; actual decoded frames and chronological contact sheets are inspected.

## Known limits

The original blush FX have three longer diagonal pink strokes, while the reference has finer peach hatching. Registration deliberately preserves original source artwork rather than repainting it. Painted eyebrow-curvature changes and body/hand acting in the reference are not reproduced by this bust-up rigid rig. This is not a pixel-perfect full reference reproduction. Subpixel/antialiased boundary coverage is measured separately from the physical mouth cap; unchanged existing raster limitations are not recategorized as newly fixed.

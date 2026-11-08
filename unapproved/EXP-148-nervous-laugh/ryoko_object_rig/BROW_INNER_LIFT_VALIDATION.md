# Rigid outer-anchor inner-brow capability v1

Nine user-approved performances share one rig: EXP-163/005/001/006/107/007/002/152/160. The published002/152 profiles, hidden-iris support and gaze_down_extra semantics are preserved. EXP-160 adds the approved default-zero rigid outer-anchor brow capability without new artwork. EXP-003/177/161/153 remain excluded. See SHY_MERGED_PUBLICATION_VALIDATION.md for merged scope and evidence; preceding frozen review stages are historical.

Status: local capability candidate, unapproved and unpublished. This revises the previously unapproved 14-degree center-pivot mapping. Neither EXP-160 nor EXP-161 is implemented or registered here. Only the six previously approved performances remain: EXP-163, EXP-005, EXP-001, EXP-006, EXP-107 and EXP-007.

## Exact scope and compatibility

The baseline is published commit `8c349e29fb1e742231918260d7db56026492a6c9`: 450 files, 182 PNGs, compact sorted inventory SHA-256 `70e8593da87a240bfa024c58677f53560f4ff7afc6d6fa07f7f54665d1072cf6`. All original artwork, shaders, profiles, timings and registry entries remain byte-identical. Both tracked iris `.import` files are retained. There are no hidden-iris or other unapproved expression dependencies.

The separately retained v0 checkpoint is a different, unapproved mapping: up to 14 degrees of additive rotation around the old center. Its nonzero inner-lift commands are deliberately NOT compatible with this revision. All published commands, which omit or default the new channels to zero, must retain exact legacy state fields and pixels. Whole state dictionaries add only the two normalized channels; old-state projection removes only those two keys.

## Shared control contract

`brow_inner_lift_screen_left` and `brow_inner_lift_screen_right` each accept finite normalized values from 0 to 1, default 0. They add up to 26 degrees of inward-up rigid rotation, negative on screen-left and positive on screen-right. Published `brow_tilt_*` controls remain exactly ±8 degrees around their original centers. Published vertical translation remains ±10 native pixels. Combined rotation bounds are left [−34°, 8°] and right [−8°, 34°]. The new rotation preserves the outer-tail anchor after those existing controls have acted.

For original center C, canonical anchor A, local offset a=A−C, existing tilt angle theta, additive angle delta and existing vertical offset v:

- Final angle is theta+delta.
- Final center-pivot position is C+v+R(theta)(a−R(delta)a).
- The outer tail therefore remains C+v+R(theta)a.

Canonical anchors are left (466.550, 452.350) and right (646.227, 453.773). They are alpha-weighted pixel-center centroids of the outermost three opaque green-pigment columns in the actual retained canonical brow layers, rather than inferred hidden anatomy. The right tail is partly covered by foreground hair. `source_references/brow_outer_anchor_geometry.json` records the exact pixel bands, PNG hashes, coordinates and method. An explicit zero-inner-lift branch retains the prior position and rotation assignments without a compensation calculation.

There is one existing rigid pivot owner per brow. Pigment, UV, texture regions, opacity, scale, shaders and artwork are unchanged. The implementation adds no eyebrow layer or backing patch and never moves hair to conceal a defect. Foreground hair stays above the brow. The inherited blunt right inner contour and fine fringe traces are not claimed to have been repaired.

Shared controller/player, registry validation, viewer, API and preparation-only bridge use the same channels. Omitted manual fields retain their current value; omitted timeline fields and neutral/reset default to zero. Reset followed by explicit controls behaves as before. Entry, retrigger, interruption, release and auto-blink saved-intent behavior remain shared. Bridge capabilities expose the bound, canonical anchors, rigid composition and explicit nonzero-v0 incompatibility. No actual AI, TTS or socket service is connected.

## Source fit and bound selection

Source catalogue commit `7693d1b8718c3bb1c717bd586fb472a7efc42403`; exact EXP-160 sheet `avatar_build_assets/reference_library/assets/expressions/EXP-160_shy-laughter/RYO_EXP-160_shy-laughter_sheet_v001.png`, SHA-256 `e07d769749529ff31dbedfd4eb427bcef4f8b802c39cc9fd10b91ddc78d5acba`. Source peak panel SHA-256 is `d20164ccc478a65ded050dbf10c1fb10d3f21ddfdc8c4227014ab90fbaee6073`.

The actual v0 maximum of 22 degrees total remained too flat for the source's tender inner-high direction. Raising the center-rotation limit alone would drop the left outer tail by about 18 pixels, beyond the existing vertical compensation. The outer-anchor composition addresses this with rigid geometry, without widening the old control or establishing any need for new curved artwork.

Fresh Godot native and full-bust probes compared total 30, 32 and 34 degrees at existing raise 0 and 0.25, with mouth/lids fixed. Both reviewers found 32 degrees and raise 0 a plausible static EXP-160 fitting pose, with no justification for increasing the 26-degree additive cap further. Per-side fitting values may differ within the same range. The source-right uncovered segment is only nine pixels wide; its numerical slope is not a precision target. Source-fit diagnostics are not a likeness score, a complete acting trajectory or expression approval. The canonical right contour differs from the source art and is retained.

## Executed numerical verification

Clean import passed on Godot 4.6.3 with writable HOME and XDG paths. All 20 frozen-runtime suites passed, with 11,120,692 final reported assertions. The revised inner-lift contract passed 84,990 checks across 6,459 poses. It covers independent sides, old tilt/translation extrema, lid/gaze/hair corners, other-owner invariance, fixed pigment/UV/alpha/unit scale, monotone 1,001-step fractional paths, old trajectories at 30 and 60 Hz, entry/retrigger/release/interruption/manual/reset, cross-profile transitions, automatic-blink saved intent, invalid/atomic transactions, omitted fields and schema loading.

The separate outer-anchor preflight passed 6,602 checks over 900 mixed poses. Its maximum tail-position residual was 0.000061 pixels. Independent frozen-copy checks passed 21,846 assertions over 2,268 mixed poses, plus 1,773 exact old-state checkpoints against published main. These are numerical checks, not evidence of watching playback.

Callable bridge dispatch/capabilities and bounded response serialization passed without opening a listener. A real socket transport test was intentionally not run.

## Fresh graphical verification

Fresh exact-main/candidate captures compared 801 old-domain states in both native and full-bust presentations, covering complete 30 Hz paths of all six profiles, lifecycle/manual/retrigger/reset samples and old combined corners. All state and raster hashes match exactly. An additional 4,224 dense checkpoints cover repeated 30/60 Hz cycles and match after removing only the two new keys. The new-domain capture passed 104,359 assertions over 193 poses: 128 independent old/new brow extrema crossed with hair ±0.07 and representative lid/gaze corners, 63 smoothstep fractional poses, and exact 32/34-degree source-fit repeats. Both fresh fitting poses reproduce the initial bracket pixels exactly. Numerical tests cover more lid/gaze combinations than the representative raster set.

The supported existing desktop renderer was Godot 4.6.3 Compatibility, OpenGL 4.5, Mesa 25.0.7/llvmpipe. No display or socket server was created. Full-bust frames are 568×800; native frames are 1136×1384. The pose is rewritten after presentation changes so spatial shader coordinates are current.

Builder and independent review covered every new-domain native crop with an expanded full-sweep region, enlarged low-brow/open-lid and high-inner/hair cases, and selected actual-bust extrema and fitting poses. No new backing hole, detached or duplicate brow, lid collision, skin seam or foreground ordering break was found in this bounded set. The inherited right blunt inner contour and darker outer terminal patch remain artistic limitations. The darker terminal patch is also visible in neutral and legacy tilt, so these observations do not establish newly missing support. Independent final raster audit checks all saved PNG hashes and actual requested states; package reconstruction is separately verified.

No normal-speed playback was observed. Deterministic pose sampling does not establish every possible artistic combination or approve any new expression.

## Reproduction and provenance

Use `python tools/verify_brow_inner_lift_scope.py`, the seven retained scope/source validators, and `sha256sum -c SOURCE_FILES.sha256`. The scoped migration pins every changed path and preserves all 450 predecessor paths; historical hash receipts remain intact and forward only through exact new hashes. It does not broadly exclude changed runtime files.

Run the four top-level `test_*.gd` and 16 `tests/test_*.gd` scripts with `godot --headless --path . --script res://<test>` and writable HOME/XDG paths. `tools/test_outer_anchor_preflight.gd` is a separate focused invariant test. `tools/review_brow_parity.gd` runs identical commands in isolated exact-parent/candidate copies. `tools/review_brow_extension.gd` takes a fixed external JSON plan. Graphical evidence requires the existing supported desktop route, not a headless renderer.

The recovery delta requires the exact published parent; it is not a standalone character archive. Its reconstruction script verifies all baseline and delta hashes before writing a new output tree, then verifies the complete result. Runtime, artwork, tests and capture harnesses remain identical to the frozen captures. Final documentation and exact source manifests are completed separately. Diagnostic PNGs and generated imports/caches are not included in the scoped source recovery ZIP.

No Git publication, CI, paid resource, source-art replacement or expression approval is implied by this checkpoint. The unrelated primary cumulative archive is untouched.
